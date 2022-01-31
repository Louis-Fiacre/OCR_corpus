from bs4 import BeautifulSoup
import os
import sys

def alto_to_txt(f, xml_dir, txt_dir):

    if f.endswith(".xml"):

        xml_path = os.path.join(xml_dir,f)
        ftxt = f.replace(".xml",".txt")
        txt_path = os.path.join(txt_dir,ftxt)

        if not os.path.isfile(txt_path):


            fd = open(xml_path, 'r')
            doc = fd.read()
            fd.close()

            soup = BeautifulSoup(doc, 'lxml')
            strin = soup.find_all('string')
            content = ""

            for data in strin:
                        
                content+=data['content']+" "

            with open(txt_path,'w') as txtfile:
                txtfile.write(content)


if __name__ == "__main__":

    cwd = "/home/lf/Bureau/Mémoire/Corpus"
    ext = '.jpg'
    
    os.chdir(cwd)
    print("Main ->",os.getcwd())
    
    authors = os.listdir(cwd)

    for author in authors:

        print("->", author)

        ouvrages = os.listdir(author)

        for ouvrage in ouvrages:

            print("\n->", author+' '+ouvrage)

            xml_dir = os.path.join(cwd, author, ouvrage,'XML')

            if os.path.isdir(xml_dir):

                txt_dir = os.path.join(cwd, author, ouvrage,'TXT_GALLICA')

                if not os.path.isdir(txt_dir):

                    os.mkdir(txt_dir)

                files = os.listdir(xml_dir)
                files_ordered = sorted(files)
                page = 0

                for f in files_ordered:

                    page += 1

                    alto_to_txt(f, xml_dir, txt_dir)

                    percent = round((page / len(files))*100)
                    sys.stdout.write("\r-> XML/*.xml vers TXT_GALLICA/*.txt " + str(percent) + "% " + str(page)+"/"+str(len(files)))
                    sys.stdout.flush()

                        
            sys.stdout.write("\r\n")

            os.chdir(cwd)           