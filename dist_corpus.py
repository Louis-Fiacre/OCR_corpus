from distances import *
from constants import *
import os

def main(cwd):

	def reader(path):
		with open(path, 'r') as f:
			text = f.read()
		return text

	os.chdir(cwd)

	print("Main ->",os.getcwd())

	authors = os.listdir(cwd)

	for author in authors:

		ouvrages = os.listdir(author)

		for ouvrage in ouvrages:

			path_groundtrue_dir = os.path.join(cwd, author, ouvrage, GROUNDTRUE_DIR)

			if os.path.isdir(path_groundtrue_dir):
			
				print("\n->", author+' '+ouvrage)

				groundtrue_files = sorted(os.listdir(path_groundtrue_dir))
				
				mean_WER_tesseract = 0
				mean_WER_gallica = 0

				for file in groundtrue_files:

					# donne les trois chemins pour plein text gallica, tesseract et groundtrue
					path_groundtrue_file = os.path.join(path_groundtrue_dir, file)
					path_tesseract_file = os.path.join(cwd,author,ouvrage,TESSERACT_DIR, file)
					path_gallica_file = os.path.join(cwd,author,ouvrage, TXT_DIR, file)
					

					t1 = reader(path_groundtrue_file)
					t2 = reader(path_tesseract_file )
					

					#print('\n',file, ' CER(%) ', ' WER(%) ')

					_ , CER_tesseract = levenshtein(t1,t2,'cer')
					_ , WER_tesseract = levenshtein(t1,t2,'wer')
					
					mean_WER_tesseract += WER_tesseract

					#print('tesseract',round(CER_tesseract,3), ' ',round(WER_tesseract,3))

					if os.path.isfile(path_gallica_file):
					
						t3 = reader(path_gallica_file)

						_ , CER_gallica = levenshtein(t1,t3,'cer')
						_ , WER_gallica = levenshtein(t1,t3,'wer')
						
						mean_WER_gallica += WER_gallica

						#print('gallica  ',round(CER_gallica,3),' ',round(WER_gallica,3))
				
				print('Moyenne WER\n tesseract   gallica\n',round(mean_WER_tesseract,3), '% ', round(mean_WER_gallica,3),'%')
						
				
		

if __name__ == '__main__':


	cwd = os.path.join(CWD,MAIN_DIR)
	main(cwd)


