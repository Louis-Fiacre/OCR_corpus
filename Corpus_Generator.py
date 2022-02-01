import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import os
import sys

class Ouvrage():

    def __init__(self, author, title, identifier, firstpage, lastpage):

    	self.author = author
    	self.title = title
    	self.identifier = identifier
    	self.firstpage = int(firstpage)
    	self.lastpage = int(lastpage)

def data_reader(filename):

    """Créé un objet ouvrage composé des informations de chaque ouvrage depuis fichier filename"""

    with open(filename, "r") as f:

        for line in f:

            (author, title, identifier, firstpage, lastpage) = line.split(",")
            ouvrage = Ouvrage(author, title, identifier, firstpage, lastpage)
            OEUVRES.append(ouvrage)

def make_dir(path_, dir_):

        """ créer dossier dir_ dans path_ s'il n'existe pas"""
        
        new_path = os.path.join(path_, dir_)
        
        if not os.path.exists(new_path):

            os.mkdir(new_path)

        return(new_path)

def make_metadonnees(path_, identifier, name='metadonnees.xml'):

    """ créer xml du dublin core des metadonnees nommé name
    depuis un identifiant ark 
    dans le path_""" 

    biblio_path = os.path.join(path_, name)

    if not os.path.isfile(biblio_path):

        url = 'https://gallica.bnf.fr/services/OAIRecord?ark='+identifier[7:]
        urllib.request.urlretrieve(url, biblio_path)

    return biblio_path



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

        print_path = path_.replace('/home/lf/Bureau/Mémoire/Corpus/','')
        percent = round((page / ouvrage.lastpage)*100)
        sys.stdout.write("\r"+ print_path + " : " + str(percent) + "% " + zero+str(page)+"/"+str(ouvrage.lastpage)+ext)
        sys.stdout.flush()
    sys.stdout.write("\r\n")

def xml_alto_to_txt(xml_path, txt_path):

    """ f : nom du fichier xml
        xml_dir : dossier du fichier xml
        txt_dir : dossier du fichier txt créé"""

    files = sorted(os.listdir(xml_path))

    firstpage = int(files[0][0:-4])
    lastpage = int(files[-1][0:-4])

    for f in files:

        if f.endswith(".xml"):

            xml_file = os.path.join(xml_path,f)
            ftxt = f.replace(".xml",".txt")
            txt_file = os.path.join(txt_path,ftxt)

            if not os.path.isfile(txt_file):


                fd = open(xml_file, 'r')
                doc = fd.read()
                fd.close()

                soup = BeautifulSoup(doc, 'lxml')
                strin = soup.find_all('string')
                content = ""

                for data in strin:
                
                    content+=data['content']+" "

                with open(txt_file,'w') as txtfile:
                    txtfile.write(content)

        print_path = txt_path.replace('/home/lf/Bureau/Mémoire/Corpus/','')
        percent = round((int(f[0:-4]) / lastpage)*100)
        sys.stdout.write("\r"+ print_path + " : " + str(percent) + "% " + str(f[0:-4])+"/"+str(files[-1].replace(".xml",'.txt')))
        sys.stdout.flush()
    sys.stdout.write("\r\n\n")


	
def make_corpus(cwd, data):
    """ construit un corpus des textes en format jpg et plein text depuis fichier identifiant gallica(data)"""

    print("Main ->", cwd)
    data_reader(data)

    corpus_path = make_dir(cwd, main_dir)

    for ouvrage in OEUVRES:

        author_path = make_dir(corpus_path, ouvrage.author)

        ouvrage_path = make_dir(author_path, ouvrage.title)

        meta = make_metadonnees(ouvrage_path, ouvrage.identifier)
        

        img_path = make_dir(ouvrage_path, img_dir)
        scrapper(ouvrage, img_path, '.jpg')

        if isocr(meta) == True:

            xml_path = make_dir(ouvrage_path, xml_dir)
            scrapper(ouvrage, xml_path, '.xml')

            txt_path = make_dir(ouvrage_path, txt_dir)

            xml_alto_to_txt(xml_path, txt_path)


if __name__ == "__main__":

    OEUVRES = list()

    cwd = '/home/lf/Bureau/Mémoire/'
    data = 'gallica_data.txt'

    main_dir = 'Corpus'
    img_dir = 'IMG'
    xml_dir = 'XML'
    txt_dir = 'TXT_GALLICA'

    make_corpus(cwd, data)