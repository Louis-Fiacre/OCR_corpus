import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import os
import sys

OEUVRES = list()

class Ouvrage():
    def __init__(self, author, title, identifier, firstpage, lastpage):
    	self.author = author
    	self.title = title
    	self.identifier = identifier
    	self.firstpage = int(firstpage)
    	self.lastpage = int(lastpage)
    	
def reader(filename):
    """Créé un objet ouvrage composé des informations de chaque ouvrage depuis un fichier txt"""
    with open(filename, "r") as f:
    	for line in f:
    	    (author, title, identifier, firstpage, lastpage) = line.split(",")
    	    ouvrage = Ouvrage(author, title, identifier, firstpage, lastpage)
    	    OEUVRES.append(ouvrage)

def isocr(path_file):
    """ cherche dans balise des métadonnées d'un ouvrage gallica si version océrisée existe"""
    if path_file.endswith(".xml"):

        file = open(path_file, 'r')
        doc = file.read()

        soup = BeautifulSoup(doc, 'lxml')

        ocr = soup.find('nqamoyen') # balise responsable de l'ocr
        ocr = ocr.contents
        ocr = float(ocr[0])

        if ocr >= 50:

            return True
        else: 
            return False

def make_metadonnees(path_, identifier, name='metadonnees.xml'):
    """ créer xml du dublin core des metadonnees depuis un identifiantark """ 

    biblio_path = os.path.join(path_, name)
    if not os.path.isfile(biblio_path):
        url = 'https://gallica.bnf.fr/services/OAIRecord?ark='+identifier[7:]
        urllib.request.urlretrieve(url, biblio_path)
    print_path = biblio_path.replace('/home/lf/Bureau/Mémoire/test_corpus/','')
    print("->", print_path)
    return biblio_path

def scrapper(ouvrage, path_, ext):
    """ récupère les images d'un ouvrage depuis gallica et les dépose dans le répertoire correspondant"""

    listpage = range(ouvrage.firstpage, ouvrage.lastpage + 1)
    len_last = len(str(ouvrage.lastpage))

    for page in listpage:

        size = len_last - len(str(page))
        zero = "0" * size

        file_ = zero + str(page) + ext 

        path_file = os.path.join(path_, file_)
        
        if not os.path.isfile(path_file):

            if ext == '.jpg':
                
                url = 'http://gallica.bnf.fr/iiif/ark:' + ouvrage.identifier + '/f' + str(page) + '/full/5000/0/native.jpg'
            
            if ext == '.xml':

                url = 'https://gallica.bnf.fr/RequestDigitalElement?O='+ouvrage.identifier[7:]+'&E=ALTO&Deb='+str(page)

            try:
                urllib.request.urlretrieve(url, path_file)

            except urllib.error.HTTPError as err:
                print('Error -> ({})'.format(err))

        close_path = os.path.join(ouvrage.author, ouvrage.title)
        print_path = path_.replace('/home/lf/Bureau/Mémoire/test_corpus/','')
        print_path = print_path.replace(close_path,'')
        percent = round((page / ouvrage.lastpage)*100)
        sys.stdout.write("\r"+ print_path + " : " + str(percent) + "% " + zero+str(page)+"/"+str(ouvrage.lastpage))
        sys.stdout.flush()
    sys.stdout.write("\r\n")
	
def make_corpus(cwd, data):
    """ construit un corpus des textes en format jpg et plein text depuis fichier identifiant gallica(data)"""

    def make_dir(path_, dir_):
        """make a dir if not exists"""
        new_path = os.path.join(path_, dir_)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        return(new_path)

    print("Main ->", cwd)
    reader("gallica_data.txt")
    
    main_dir = 'Corpus'
    sub_img_dir = 'IMG'
    sub_xml_dir = 'XML'

    corpus_path = make_dir(cwd, main_dir)

    for ouvrage in OEUVRES:

        author_path = make_dir(corpus_path, ouvrage.author)

        title_path = make_dir(author_path, ouvrage.title)

        meta = make_metadonnees(title_path, ouvrage.identifier)
        

        img_path = make_dir(title_path, sub_img_dir)
        scrapper(ouvrage, img_path, '.jpg')

        flag_ocr = isocr(meta)

        if flag_ocr == True:

            xml_path = make_dir(title_path, sub_xml_dir)
            scrapper(ouvrage, xml_path, '.xml')


if __name__ == "__main__":

    cwd = '/home/lf/Bureau/Mémoire/'
    make_corpus(cwd, 'gallica_data.txt')
        
