# OCR_corpus

Dans le cadre de mon master d'Humanités numériques, je cherche à obtenir un corpus de texte pamphlétaire français issu de la fin du XIXè-début XXè siècle et lui appliquer divers outils de traitement automatique de la langue.

Ces scripts permettent d'extraire des documents depuis Gallica via son API au format xml si un ocr existe, et image. D'océriser les images avec pyTesseract. De mesurér le taux d'erreur de l'ocr de Gallica et de pyTesseract.

## scrapper + ark_gallica.txt

Construit sur la base de Pyllica, ce script permet de créer une arborescence de dossiers et de fichiers depuis un fichier texte listant les identifiants ark de document sur gallica. Créer un dossier par auteur, un sous dossier par ouvrage. Puis télécharge les images et les places dans un dossier IMG. Télécharge aussi les métadonnées de l'ouvrage. Et si un ocr existe, télécharge les xml_alto de l'ocr de Gallica et les converti en texte dans dossier TXT_GALLICA. 

## ocr_img_to_txt

Océrise les images des ouvrages avec pytesseract et retourne le contenu texte dans dossier TXT_TESSERACT ou TXT_OUT

## join_pages_for_1txt

Concatène l'ensemble des pages de texte dans un seul fichier texte pour un ouvrage donné.

## distances.py

Ce module intègre plusieurs mesure de calcul de distance de similarité, utilisable en prenant en entrée deux chaines de caractère.

## distance_df

Prend les textes des dossiers TXT_TESSERACT, TXT_GALLICA et TXT_GROUNDTRUE et retourne un fichier texte issu d'un dataframe l'ensemble des métriques de distances de similarité du module distances.py


# Structure de l'arborescence produite par l'ensemble des programmes

1. Corpus/Auteur/Ouvrage
- /metadonnees.xml (dublin core métadonnées de l'ouvrage depuis Gallica)
- /IMG (jpg depuis Gallica)
- /XML (OCR Xml Alto depuis Gallica. N'existe pas toujours)
- /TXT_GALLICZ (texte depuis Xml Alto de Gallica)
- /TXT_TESSERACT (texte depuis IMG Gallica par pytesseract)
- /TXT_GROUNDTRUE (texte saisi à la main des trois premières images)
- /TXT_OUT (txt issu des images nettoyées avec scantailor-advanced)



