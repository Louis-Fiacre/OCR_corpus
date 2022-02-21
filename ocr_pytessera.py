import numpy as np
import cv2
import os
import sys
from scrapper import *

def ocr(cwd, _IMG_DIR_='IMG'):
    
    os.chdir(cwd)
    print("Main ->",os.getcwd())
    
    authors = os.listdir(cwd)

    for author in authors:

        print("->", author)

        for ouvrage in ouvrages:

            print("->", ouvrage)
            path_ouvrage = os.path.join(cwd, author, ouvrage)
            path_img_dir = os.path.join(path_ouvrage, _IMG_DIR_)

            path_tesseract_dir = make_dir(path_ouvrage, TESSERACT_DIR)

            img_files = os.listdir(path_img_dir)
            img_files = sorted(img_files)
                
            print(" -> "+ ouvrage +" \n-> "+_IMG_DIR_+"/*.jpg vers"+TESSERACT_DIR+"/*.txt"  )

            page = 0

            for img_file in img_files[0:3]:


                page += 1

                path_img_file = os.path.join(path_img_dir, img_file)
                txt_file = img_file.replace(".jpg",".txt")
                path_tesseract_file = os.path.join(path_tesseract_dir, txt_file)

                if os.path.isfile(path_tesseract_file):


                    img = cv2.imread(path_img_file)

                    text = pytesseract.image_to_string(img, lang="fra")

                    with open(path_tesseract_file,'w') as txtfile:
                        txtfile.write(text)

                    percent = round((page / len(img_files))*100)
                    sys.stdout.write("\r OCR TXT : " + str(percent) + "% " + str(page)+"/"+str(len(img_files)))
                    sys.stdout.flush()

                        
            sys.stdout.write("\r\n")

            os.chdir(cwd)
