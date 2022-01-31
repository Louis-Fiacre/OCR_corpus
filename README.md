# OCR_corpus

Dans le cadre de mon master d'Humanités numérique, je cherche à obtenir un corpus de texte pamphlétaire français issu de la fin du XIXè-début XXè siècle et lui appliquer des outils de lemmatisation.

Création d'un corpus depuis Gallica, comparaison de l'océrisation de Gallica et de Tesseract.
Le but de ce repository est de mettre en place méthodiquement une comparaison des OCR produits par Gallica et par Tesseract (par son binding pytesseract). L'objectif est d'obtenir pour un corpus de texte donné les taux d'erreur CER et WER les plus faibles. 
L'hypothèse la plus probable est que l'OCR de pytesseract avec le prétraitement adéquat des images sera plus efficient.


## API_Gallica.py

Construit sur la base de pyllica, il permet de créer une arborescence de dossiers et de fichiers depuis un fichier texte listant les identifiants ark d'ouvrages sur gallica. Il télécharge les images et les xml_alto de l'océrisation de gallica si ils existent.

## XML_ALTO->TXT.py

Extrait pour chaque XML_ALTO contenu dans le corpus, le contenu texte et le retourne dans dans un dossier TXT_GALLICA au format .txt

## JPG->TXT.py

Océrise les images des ouvrages avec pytesseract et retourne le contenu texte dans dossier TXT_TESSERACT au format .txt

### TO DO
Affiner le prétraitement des images pour chaque ouvrage et non pas, comme actuellement dans mon code, seulement appliquer un prétraitement général.

## CER_WER.py

Prend les textes des dossiers TXT_TESSERACT, TXT_GALLICA et TXT_GROUNDTRUE et retourne le taux d'erreur par caractère et par mot.
Le but étant de comparer la précision des OCRs de gallica et de pytesseract mais aussi de pouvoir mesurer l'efficacité du prétraitement des images pour l'océrisation de pytesseract.

### TO DO

Trouver une manière plus clair de retourner les résultats.

