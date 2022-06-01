def levenshtein(a, b, mod = 'WER'):

	""" Calcul distance de Levenshtein
	entrée :
		a & b : str ou list
		mod : 'CER' ou 'WER' 
	
	sortie : nombre d'erreur et le taux d'erreur.
	"""

	if mod == 'CER': 
	
		a = a.split()
		b = b.split()

	if len(a) < len(b):
	
		return levenshtein(b, a)

    # len(a) >= len(b)
	if len(b) == 0:

		return len(a)

	previous_row = range(len(b) + 1)

	for i, c1 in enumerate(a):

		current_row = [i + 1]

		for j, c2 in enumerate(b):

			insertions = previous_row[j + 1] + 1 
			suppressions = current_row[j] + 1      
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, suppressions, substitutions))

		previous_row = current_row

	error = previous_row[-1]
	error_rate = (error / max(len(a),len(b))*100)

	return error, error_rate


def jaccard(a, b, coef=1):

	""" Similarité de Jaccard
	entrée : str ou list
	sortie : float
	"""
	return dice(a, b, coef)


def dice(a, b, coef=2):

	""" Similarité de Jaccard avec un coef de similarité de Dice
	entrée : str ou list
	sortie : float
	"""
	if type(a) == str and type(b) == str:
	
		a, b = list(a), list(b)
		
	if type(a) == list and type(b) == list:
	
		intersection = len(list(set(a).intersection(b)))
		union = (len(a) + len(b)) - intersection
	
		return float(coef*intersection) / union

	return False

if __name__ == '__main__':

	t1 = 'tes yeux sont verts'
	t2 = 'a quoi sert des verres'
	print(levenshtein(t1,t2))
	print(jaccard(t1,t2))