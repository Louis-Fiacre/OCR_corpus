import urllib.request, urllib.error, urllib.parse
import os
import sys

OEUVRES = list()

class Ouvrage():
    """ 
    Classe permettant de définir 
    les caractéristiques d'un ouvrage
    """
    
    def __init__(self, author, title, identifier, firstpage, lastpage):
	
    	self.author = author
    	self.title = title
    	self.identifier = identifier
    	self.firstpage = int(firstpage)
    	self.lastpage = int(lastpage)

def data_reader(filename):

    """
    Créé un objet ouvrage composé des 
    informations de chaque ouvrage depuis fichier filename
    """

    with open(filename, "r") as f:

        for line in f:
	    # extrait les informations du fichier
            (author, title, identifier, firstpage, lastpage) = line.split(",")
            # créer un object ouvrage par ligne
            ouvrage = Ouvrage(author, title, identifier, firstpage, lastpage)
            # ajout à liste de tous les ouvrages
            OEUVRES.append(ouvrage)

def make_dir(path_, dir_):

        """ 
        créer un dossier dir_ dans path_ 
        s'il n'existe pas 
        """
        
        new_path = os.path.join(path_, dir_)
        
        if not os.path.exists(new_path):

            os.mkdir(new_path)

        return(new_path)

def make_metadonnees(path_ouvrage, identifier, name='metadonnees.xml'):

    """ 
    télécharge depuis gallica le xml dublin core des metadonnees 
    d'un ouvrage nommé depuis un identifiant ark 
    dans le dossier path_
    """ 

    metadonnee_path = os.path.join(path_ouvrage, name)

    if not os.path.isfile(metadonnee_path):

        url = 'https://gallica.bnf.fr/services/OAIRecord?ark='+identifier[7:]
        urllib.request.urlretrieve(url, metadonnee_path)

    return metadonnee_path



def isocr(path_xml_file):

    """ 
    cherche dans balise des métadonnées d'un ouvrage gallica 
    si une version océrisée de l'ouvrage existe
    """
    from bs4 import BeautifulSoup
    
    if path_xml_file.endswith(".xml"):

        xml_file = open(path_xml_file, 'r')
        doc = xml_file.read()
        soup = BeautifulSoup(doc, 'lxml')

        ocr = soup.find('nqamoyen') # balise responsable de l'ocr
        ocr = ocr.contents
        ocr = float(ocr[0])

        if ocr >= 50:

            return True

        return False

def scrapper(ouvrage, path_, ext):

    """ 
    récupère les images ou l'xml d'un ouvrage depuis gallica 
    et les dépose dans le répertoire correspondant
    """

    listpage = range(ouvrage.firstpage, ouvrage.lastpage + 1)
    len_last = len(str(ouvrage.lastpage))

    for page in listpage:

        size = len_last - len(str(page))
        zero = "0" * size

        file_ = zero + str(page) + ext 

        path_file = os.path.join(path_, file_)
        
        if not os.path.isfile(path_file):

            if ext == '.jpg':
            	# requête pour les jpg
                url = 'http://gallica.bnf.fr/iiif/ark:' + ouvrage.identifier + '/f' + str(page) + '/full/5000/0/native.jpg'
            
            if ext == '.xml':
		# requête pour les xml
                url = 'https://gallica.bnf.fr/RequestDigitalElement?O='+ouvrage.identifier[7:]+'&E=ALTO&Deb='+str(page)

            try:

                urllib.request.urlretrieve(url, path_file)

            except urllib.error.HTTPError as err:

                print('Error -> ({})'.format(err))
                
        # les lignes suivantes gèrent juste un affichage pour suivre l'evolution des requêtes
        print_path = path_.replace('/home/lf/Bureau/Mémoire/Corpus/','')
        percent = round((page / ouvrage.lastpage)*100)
        sys.stdout.write("\r"+ print_path + " : " + str(percent) + "% " + zero+str(page)+"/"+str(ouvrage.lastpage)+ext)
        sys.stdout.flush()
    sys.stdout.write("\r\n")

def xml_alto_to_txt(xml_path, txt_path):

    """ 
    Transforme les xml téléchargés depuis gallica en plein texte txt
    
    f : nom du fichier xml
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
    """ 
    construit un corpus des textes en format jpg, xml alto et plein text 
    depuis un fichier de données avec les identifiant gallica(data)
    """

    print("Main ->", cwd)
    data_reader(data)
    corpus_path = make_dir(cwd, MAIN_DIR)

    for ouvrage in OEUVRES:

        path_author_dir = make_dir(corpus_path, ouvrage.author)
        path_ouvrage_dir = make_dir(path_author_dir, ouvrage.title)
        path_img_dir = make_dir(path_ouvrage_dir, IMG_DIR)
        scrapper(ouvrage, path_img_dir, '.jpg')
        ocr_flag = make_metadonnees(path_ouvrage_dir, ouvrage.identifier)

        if isocr(ocr_flag) == True:

            path_xml_dir = make_dir(path_ouvrage_dir, XML_DIR)
            path_txt_dir = make_dir(path_ouvrage_dir, TXT_DIR)
            scrapper(ouvrage, path_xml_dir, '.xml')
            xml_alto_to_txt(path_xml_dir, path_txt_dir)
