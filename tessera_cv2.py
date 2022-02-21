import pytesseract
from PIL import Image
import numpy as np
import cv2
import os
import sys

from constants import *

def levenshtein(s1, s2, mod = 'wer'):

    """ Calcul distance de Levenshtein
    s1 : texte de référence
    s2 : teste hypothese
    mod : 'cer' ou 'wer', par défaut cer. 'wer' coupe la chaine de caractère par mot
    retourne le nombre d'erreur et le taux d'erreur.
    """

    if mod == 'cer': 
        s1 = s1.split()
        s2 = s2.split()

    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    error = previous_row[-1]
    error_rate = (error / max(len(s1),len(s2))*100)

    return error, error_rate

def apply_threshold(img, argument):

        """plusieurs opérations possibles de prétraitement"""
        switcher = {
            1: cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            2: cv2.threshold(cv2.GaussianBlur(img, (7, 7), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            3: cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            4: cv2.threshold(cv2.medianBlur(img, 5), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            5: cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            6: cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
            7: cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        }
        return switcher.get(argument, "Invalid method")

def corpus(cwd):

    def reader(path):
        with open(path, 'r') as f:
            text = f.read()
        return text

    os.chdir(cwd)

    print("Main ->",os.getcwd())

    authors = os.listdir(cwd)

    for author in authors:

        ouvrages = os.listdir(author)
        print(author)

        if author == 'Georges_Bernanos':
            break

        for ouvrage in ouvrages:



            path_groundtrue_dir = os.path.join(cwd, author, ouvrage, GROUNDTRUE_DIR)

            if os.path.isdir(path_groundtrue_dir):

                #print("\n->", author+' '+ouvrage)

                mean_WER_tesseract = 0
                mean_CER_tesseract = 0

                groundtrue_files = sorted(os.listdir(path_groundtrue_dir))  

                for file in groundtrue_files:

                    # donne les deux chemins pour plein text tesseract et groundtrue
                    path_groundtrue_file = os.path.join(path_groundtrue_dir, file)

                    jpg_file = file.replace('.txt','.jpg')
                    path_img_file = os.path.join(cwd,author,ouvrage,IMG_DIR, jpg_file)

                    img = cv2.imread(path_img_file)

                    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    #kernel = np.ones((1, 1), np.uint8)
                    #img = cv2.dilate(img, kernel, iterations=1)
                    #img = cv2.erode(img, kernel, iterations=1)
                    #img_ = apply_threshold(img, 5)

                    pil_img = Image.fromarray(img)

                    t2 = pytesseract.image_to_string(pil_img, lang="fra")
                    t1 = reader(path_groundtrue_file)

                    _ , CER = levenshtein(t1, t2, 'cer')
                    _ , WER = levenshtein(t1, t2, 'wer')

                    mean_WER_tesseract += WER
                    mean_CER_tesseract += CER
                    

                print('CER',round(mean_CER_tesseract,2),'% | WER',round(mean_WER_tesseract,2),'%')
                #with open('cer_wer_data.txt', 'a') as file:

                #   file.write('sans prétraitement')


if __name__ == '__main__':

    CWD = '/home/lf/Bureau/Memoire/Corpus'


    corpus(CWD)

""" 

    psm 4 no traitement
CER 169.63 % | WER 116.92 %
CER 108.94 % | WER 66.04 %
CER 36.23 % | WER 15.93 %
CER 38.56 % | WER 16.01 %
CER 33.09 % | WER 8.13 %
CER 66.46 % | WER 30.5 %
CER 64.84 % | WER 22.91 %

    psm 4 resize
CER 155.78 % | WER 133.36 %
CER 51.29 % | WER 24.55 %
CER 31.56 % | WER 10.79 %
CER 32.96 % | WER 14.97 %
CER 31.15 % | WER 7.84 %
CER 76.37 % | WER 34.25 %
CER 48.49 % | WER 18.21 %

    psm 4 resize grayscale

CER 50.23 % | WER 21.76 %
CER 49.31 % | WER 24.99 %
CER 20.02 % | WER 6.38 %
CER 32.96 % | WER 14.97 %
CER 31.15 % | WER 7.84 %
CER 76.37 % | WER 34.25 %
CER 46.9  % | WER 17.04 %
    
    psm 4 resize grayscale erode dilate

CER 50.23 % | WER 21.76 %
CER 49.31 % | WER 24.99 %
CER 20.02 % | WER 6.38 %
CER 32.96 % | WER 14.97 %
CER 31.15 % | WER 7.84 %
CER 76.37 % | WER 34.25 %
CER 46.9  % | WER 17.04 %

    no psm resize grayscale erode dilate tresold1

CER 54.01 % | WER 23.45 %
CER 29.17 % | WER 13.53 %
CER 20.03 % | WER 6.48 %
CER 32.13 % | WER 14.44 %
CER 31.15 % | WER 7.84 %
CER 98.15 % | WER 51.94 %
CER 46.9  % | WER 16.96 %

    psm 4 resize grayscale erode dilate tresold1-2-3-4

CER 50.23 % | WER 21.76 %
CER 49.31 % | WER 24.99 %
CER 20.02 % | WER 6.38 %
CER 32.96 % | WER 14.97 %
CER 31.15 % | WER 7.84 %
CER 76.37 % | WER 34.25 %
CER 46.9  % | WER 17.04 %

    no psm resize grayscale erode dilate tresol4-5

CER 54.01 % | WER 23.45 %
CER 29.17 % | WER 13.53 %
CER 20.03 % | WER 6.48 %
CER 32.13 % | WER 14.44 %
CER 31.15 % | WER 7.84 %
CER 98.15 % | WER 51.94 %
CER 46.9  % | WER 16.96 %

    no psm grayscale

CER 54.01 % | WER 23.45 %
CER 29.17 % | WER 13.53 %
CER 20.03 % | WER 6.48 %
CER 32.13 % | WER 14.44 %
CER 31.15 % | WER 7.84 %
CER 98.15 % | WER 51.94 %
CER 46.9 % | WER 16.96 %







"""