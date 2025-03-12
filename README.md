# Tracking à l'aide de filtres de Kalman

### Installation
Afin d'installer le programme, il faut vous munir de python 3.9.5 (seule version testé où tous les modules sont compatibles avec les versions demandés) et d'entrer la commande "pip install -r requirements.txt" dans un terminal.
Le programme n'a été testé que sous Windows mais il devrait aussi bien fonctionner sous MacOS et Linux.

### Utilisation

Il y a deux types d'arguments possible:
- "-d": vous donner un chemin d'accès sans guillemets vers un dossier contenant toutes les vidéos sur lesquelles vous voulez faire la reconnaissance. Le programme se charge d'aller chercher les vidéos.
- "-f": vous donner les chemins d'accès sans guillemets vers les fichiers vidéos sur lesquelles vous voulez faire la reconnaissance.

### Compatibilité logicielle

Le programme a été testé sur Windows 11, avec python 3.9.5 et les modules avec les versions comme précisé dans le fichier "requierement.txt". Le programme ne fonctionne pas sur python <=3.12 à cause d'une incompatibilité de module entre numpy et scipy-image. 
Sous la même installation python, le programme fonctionne sur Ubuntu 20.04.6 sous WSL. Aucun test n'a été effectué sur une autre distribition de Linux, y compris MacOS. 
