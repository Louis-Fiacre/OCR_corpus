import os

def levenshtein(s1, s2, mod = 'cer'):

	""" Calcul distance de Levenshtein
	s1 : texte de référence
	s2 : teste hypothese
	mod : 'cer' ou 'wer', par défaut cer. 'wer' coupe la chaine de caractère par mot
	retourne le nombre d'erreur et le taux d'erreur.
	"""

	if mod == 'wer': 
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

def corpus(cwd):

	def reader(path):
		with open(path, 'r') as f:
			text = f.read()
		return text

	os.chdir(cwd)

	print("Main ->",os.getcwd())

	authors = os.listdir(cwd)

	for author in authors:

		print("->", author)

		ouvrages = os.listdir(author)

		for ouvrage in ouvrages:

			print("\n->", author+' '+ouvrage)

			path_groundtrue_dir = os.path.join(cwd, author, ouvrage, GROUNDTRUE_DIR)

			if os.path.isdir(path_groundtrue_dir):

				groundtrue_files = sorted(os.listdir(path_groundtrue_dir))	

				for file in groundtrue_files:

					# donne les trois chemins pour plein text gallica, tesseract et groundtrue
					path_groundtrue_file = os.path.join(path_groundtrue_dir, file)
					path_tesseract_file = os.path.join(cwd,author,ouvrage,TESSERACT_DIR, file)
					path_gallica_file = os.path.join(cwd,author,ouvrage, TXT_DIR, file)
					

					t1 = reader(path_groundtrue_file)
					t2 = reader(path_tesseract_file )
					

					print('\n',file, ' CER(%) ', ' WER(%) ')

					_ , error_rate = levenshtein(t1,t2,'cer')
					_ , error_rate1 = levenshtein(t1,t2,'wer')

					print('tesseract',round(error_rate,3), ' ',round(error_rate1,3))

					if os.path.isfile(path_gallica_file):
					
						t3 = reader(path_gallica_file)

						_ , error_rate2 = levenshtein(t1,t3,'cer')
						_ , error_rate3 = levenshtein(t1,t3,'wer')

						print('gallica  ',round(error_rate2,3),' ',round(error_rate3,3))
		

if __name__ == '__main__':

	CWD = '/home/lf/Bureau/Memoire/Corpus'

	GROUNDTRUE_DIR = 'TXT_GROUNDTRUE'
	TESSERACT_DIR = 'TXT_TESSERACT'
	TXT_DIR = 'TXT_GALLICA'

	corpus(CWD)