# Tracking à l'aide de filtres de Kalman

### Installation
Afin d'installer le programme, il faut cloner ce repo dans un dossier ou copier tout les fichiers de ce repo dans un dossier. Ensuite, il suffit d'installer Python 3.9.5 et une fois installé, d'entrer  la commande "pip install -r requirements.txt" dans un terminal.

Cette installation n'a été testé que sur Windows et Ubuntu. 

### Utilisation

Il suffit maintenant d'aller à la racine du projet puis d'entrer la commande "python monaco_cam.py" puis un des deux arguments ci-dessous: 

- "-d": vous donner un chemin d'accès sans guillemets vers un dossier contenant toutes les vidéos sur lesquelles vous voulez faire la reconnaissance. Le programme se charge d'aller chercher les vidéos.
- "-f": vous donner les chemins d'accès sans guillemets vers les fichiers vidéos sur lesquelles vous voulez faire la reconnaissance.
- "--debug": pour remettre les instructions de debug d'ultralytics. Cet argument doit être ajouté à la toute fin de la commande

Peut importe l'argument utilisé, les fichiers doivent être au format .mp4. Bien que d'autres formats vidéos devrait fonctionner, pour des raisons de fiabilités, de facilité d'écriture du programme et des contraintes qui nous ont été fournis, nous avons choisi de tester uniquement sur des vidéos en .mp4. 

Exemple: "python monaco_cam.py -f test_video.mp4"

**Attention, le chemin d'accès ne doit pas comporter d'espaces, sinon il risque d'y avoir des problèmes pour la récupération**

### Compatibilité logicielle

Le programme a été testé sur Windows 11, avec Python 3.9.5 sur un environement virtuel Conda et les modules avec les versions comme précisé dans le fichier "requierement.txt". Le programme ne fonctionne pas sur python <=3.12 à cause d'une incompatibilité de module entre numpy et scipy-image. 
Sous la même installation python, le programme fonctionne sur Ubuntu 20.04.6 sous WSL. Aucun test n'a été effectué sur une autre distribition de Linux, y compris MacOS. 
Il y a peut-être une erreur d'incompatibilité causé par scikit-image sur Windows 11. L'erreur reste à être documentée. 

### Contributeur

Aladdin Bensalah 

Gabriel Legout

Ce projet utilise une partie du module sort.py dont la licence figure à la racine du projet. 
