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


if __name__ == "__main__":

    cwd = "/home/lf/Bureau/Mémoire/Corpus"
    ext = '.jpg'
    
    img = 'IMG'
    txt = 'TXT_GALLICA'
    
    os.chdir(cwd)
    print("Main ->",os.getcwd())
    
    authors = os.listdir(cwd)

    for author in authors:

        print("->", author)

        ouvrages = os.listdir(author)

        for ouvrage in ouvrages:

            print("->", ouvrage)

            img_dir = os.path.join(cwd, author, ouvrage, img)

            if os.path.isdir(img_dir):

                tesseract_dir = os.path.join(cwd, author, ouvrage,txt)

                if not os.path.isdir(tesseract_dir):

                    os.mkdir(tesseract_dir)

                files = os.listdir(img_dir)
                print(" -> "+ ouvrage +" \n-> "+img+"*.jpg vers"+txt+"/*.txt"  )
                files_ordered = sorted(files)
                page = 0

                for f in files_ordered[0:10]:

                    if f.endswith(".jpg"):

                        page += 1

                        img_path = os.path.join(img_dir,f)
                        ftxt = f.replace(".jpg",".txt")
                        txt_path = os.path.join(tesseract_dir,ftxt)

                        if not os.path.isfile(txt_path):


                            img = cv2.imread(img_path)

                            text = ocrisation(img)

                            with open(txt_path,'w') as txtfile:
                                txtfile.write(text)

                        percent = round((page / len(files))*100)
                        sys.stdout.write("\r OCR TXT : " + str(percent) + "% " + str(page)+"/"+str(len(files)))
                        sys.stdout.flush()

                        
            sys.stdout.write("\r\n")

            os.chdir(cwd)            
