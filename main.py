import scrapper
import ocr_pytessera
import dist_corpus

if __name__ == '__main__':

	CWD = '/home/lf/Bureau/Memoire/'
	

	DATA = 'id_ark_gallica.txt'
	
	MAIN_DIR = 'Corpus'
	IMG_DIR = 'IMG'
	XML_DIR = 'XML'
	TXT_DIR = 'TXT_GALLICA'
	GROUNDTRUE_DIR = 'TXT_GROUNDTRUE'
	
	_IMG_DIR_ = 'IMG_pretrait'
	TESSERACT_DIR = 'TXT_TESSERACT'

	# créer corpus img, xml et txt depuis gallica
	scrapper.make_corpus(CWD, DATA)
	
	# etape de prétraitement des images avec scantailor
	# ///////// image prétraiter à deverser dans un dossier spécifique
	# _IMG_DIR_ = 'IMG_pretrait'
	
	# océrisation et création fichier texte
	ocr_pytessera.main(CWD, _IMG_DIR_)
	
	# calcul distance similarité
	dist_corpus.main(CWD)
	
	
	
	
	
	
	
	
