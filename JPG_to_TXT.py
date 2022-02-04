import pytesseract
import numpy as np
import cv2
import os
import sys

def ocrisation(img):

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


    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    # image en nuance de gris
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # dilate et érode
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    #  prétraitement
    img = apply_threshold(img, 1)
    
    # affiche l'image prétraitée
    # cv2.imshow('Image', img)
    
    # océrise
    result = pytesseract.image_to_string(img, lang="fra")
    
    return(result)

def main_ocr(cwd):
    
    os.chdir(cwd)
    print("Main ->",os.getcwd())
    
    authors = os.listdir(cwd)

    for author in authors:

        print("->", author)
        path_author_dir = os.path.join(cwd, author)
        ouvrages = os.listdir(path_author_dir)

        for ouvrage in ouvrages:

            print("->", ouvrage)
            path_ouvrage_dir = os.path.join(path_author_dir, ouvrage)
            path_img_dir = os.path.join(path_ouvrage_dir, IMG_DIR)

            if os.path.isdir(path_img_dir):

                path_tesseract_dir = os.path.join(path_ouvrage_dir, TESSERACT_DIR)

                if not os.path.isdir(path_tesseract_dir):

                    os.mkdir(path_tesseract_dir)

                img_files = os.listdir(path_img_dir)
                img_files = sorted(img_files)
                
                print(" -> "+ ouvrage +" \n-> "+IMG_DIR+"/*.jpg vers"+TESSERACT_DIR+"/*.txt"  )

                page = 0

                for img_file in img_files[0:10]:

                    if img_file.endswith(".jpg"):

                        page += 1

                        path_img_file = os.path.join(path_img_dir, img_file)
                        txt_file = img_file.replace(".jpg",".txt")
                        path_tesseract_file = os.path.join(path_tesseract_dir, txt_file)

                        if not os.path.isfile(path_tesseract_file):


                            img = cv2.imread(path_img_file)

                            text = ocrisation(img)

                            with open(path_tesseract_file,'w') as txtfile:
                                txtfile.write(text)

                        percent = round((page / len(img_files))*100)
                        sys.stdout.write("\r OCR TXT : " + str(percent) + "% " + str(page)+"/"+str(len(img_files)))
                        sys.stdout.flush()

                        
            sys.stdout.write("\r\n")

            os.chdir(cwd)            


if __name__ == "__main__":

    CWD = "/home/lf/Bureau/Memoire/Corpus"
    
    IMG_DIR = 'IMG'
    TESSERACT_DIR = 'TXT_TESSERACT'

    main_ocr(CWD)