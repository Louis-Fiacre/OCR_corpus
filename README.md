# OCR_corpus

Dans le cadre de mon master d'Humanités numérique, je cherche à obtenir un corpus de texte pamphlétaire français issu de la fin du XIXè-début XXè siècle et lui appliquer des outils de lemmatisation.

Le but de ce repository est de mettre en place méthodiquement une comparaison des OCR produits par Gallica et par Tesseract (par son binding pytesseract). L'objectif est d'obtenir un corpus de texte utilisable pour des outils de lemmatisation.

## scrapper + ark_gallica.txt

Construit sur la base de pyllica, permet de créer une arborescence de dossiers et de fichiers depuis un fichier texte listant les identifiants ark d'ouvrages sur gallica. Il télécharge les images et les xml_alto de l'ocr de Gallica. Et si les xml_alto existent, un dossier TXT_GALLICA est créé et le contenu du xml alto est versé dans des fichiers txt pour chaque page. 

## ocr_img_to_txt

Océrise les images des ouvrages avec pytesseract et retourne le contenu texte dans dossier TXT_NOM au format .txt

## join_pages_for_1txt

Concatène l'ensemble des pages en plein texte dans un seul fichier texte pour un ouvrage donné.

## distances.py

Ce module intègre plusieurs solutions de calcul de distance de similarité, utilisable en prenant en entrée deux chaines de caractère.

## distance_df

Prend les textes des dossiers TXT_TESSERACT, TXT_GALLICA et TXT_GROUNDTRUE et retourne un fichier texte issu d'un dataframe l'ensemble des métriques de distances de similarité du module distances.py


# Structure de l'arborescence produite par l'ensemble des programmes

1. Corpus/Auteur/Ouvrage
- /metadonnees.xml (dublin core métadonnées de l'ouvrage depuis Gallica)
- /IMG (jpg depuis Gallica)
- /XML (OCR Xml Alto depuis Gallica. N'existe pas toujours)
- /TXT_Gallica (txt depuis Xml Alto de Gallica)
- /TXT_Tesseract (txt depuis IMG Gallica par pytesseract)
- /TXT_Ground_True (txt saisi à la main des trois premières images)
- /TXT_out (txt issu des images nettoyées avec scantailor-advanced)



