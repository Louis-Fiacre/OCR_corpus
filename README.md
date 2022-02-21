# OCR_corpus

Dans le cadre de mon master d'Humanités numérique, je cherche à obtenir un corpus de texte pamphlétaire français issu de la fin du XIXè-début XXè siècle et lui appliquer des outils de lemmatisation.

Le but de ce repository est de mettre en place méthodiquement une comparaison des OCR produits par Gallica et par Tesseract (par son binding pytesseract). L'objectif est d'obtenir un corpus de texte utilisable pour des outils de lemmatisation.

## main.py

Permet d'utiliser les différents modules du repository. main.py [-h] ou [--help] pour plus d'info

## scrapper.py

Construit sur la base de pyllica, ce module permet de créer une arborescence de dossiers et de fichiers depuis un fichier texte listant les identifiants ark d'ouvrages sur gallica. Il télécharge les images et les xml_alto de l'océrisation de gallica. Et si les xml_alto existent, un dossier text est créer et le contenu du xml alto déversé dans des fichiers txt pour chaque page. 

## ocr_pytessera.py

Océrise les images des ouvrages avec pytesseract et retourne le contenu texte dans dossier TXT_TESSERACT au format .txt

## tessera_cv2.py - Abandonné

Ce module océrise les images gallica des ouvrages et leur applique des prétaiments d'images de la lib cv2 avant d'utiliser pytesseract. Les résultats sont en commentaires en bas du modules pour les ouvrages de Léon Bloy. J'arrête cette piste de prétraitement par cv2 pour me tourner vers scantailor.

## distances.py

Ce module intègre plusieurs solutions de calcul de distance de similarité, utilisable en prenant en entrée deux chaines de caractère.

## dist_corpus.py

Prend les textes des dossiers TXT_TESSERACT, TXT_GALLICA et TXT_GROUNDTRUE et retourne le taux d'erreur par caractère et par mot par distance de levensthein de distances.py.
Le but étant de comparer la précision des OCRs de gallica et de pytesseract mais aussi de pouvoir mesurer l'efficacité du prétraitement des images de scantailor pour l'océrisation de pytesseract.


# Structure de l'arborescence produite par l'ensemble des programmes

1. Corpus/Auteur/Ouvrage
- /metadonnees.xml (dublin core métadonnées de l'ouvrage depuis Gallica)
- /IMG (jpg depuis Gallica)
- /XML (OCR Xml Alto depuis Gallica. N'existe pas toujours)
- /TXT_Gallica (txt depuis Xml Alto de Gallica)
- /TXT_Tesseract (txt depuis IMG Gallica par pytesseract)
- /TXT_Ground_True (txt saisi à la main des trois premières images)



