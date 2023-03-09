# Présentateur

Présentateur est un bot Discord qui génère des présentations complètes sur un sujet donné grâce à GPT-3 d'OpenAI.

![Exemple de présentation](https://raw.githubusercontent.com/Paillat-dev/presentator/main/examples/steve-jobs/Steve-Jobs-1.png)

![Exemple de présentation](https://raw.githubusercontent.com/Paillat-dev/presentator/main/examples/python/the-python-programming-language-1.png)

## Fonctionnement
- Le bot envoie une demande à l'API d'OpenAI avec le sujet donné et des indications au format Markdown Marp.
- Nous extrayons les images du Markdown et les envoyons à l'API de génération d'images.
- Nous générons les fichiers PDF et HTML à partir du Markdown.
- Nous envoyons les fichiers PDF et HTML à l'utilisateur.

## Installation
**IMPORTANT** L'installation pour Linux et MacOS n'est pas encore documentée. Si vous souhaitez la compléter, n'hésitez pas à faire une pull request.
Pour suivre les étapes de cette installation, vous devrez ouvrir un terminal. POur ce faire, tapez cmd dans la barre de recherche de votre ordinateur, puis entrée.

### Prérequis
- Installez Python 3.8 https://www.python.org/downloads/
- Un token pour un bot Discord https://www.writebots.com/discord-bot-token/
- Une clé d'API OpenAI https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key
- Un compte discord et un serveur discord où ajouter l'outil.
  + https://www.ionos.fr/digitalguide/serveur/know-how/creer-un-compte-discord
  + https://www.ionos.fr/digitalguide/serveur/know-how/creer-un-serveur-discord/
- **Ne suivez pas l'étape 5 et à l'étape huit séléctionnez le permissions "administrateur".** Un bot discord https://www.ionos.fr/digitalguide/serveur/know-how/creer-un-bot-discord/#:~:text=help%C2%A0%C2%BB%20du%20bot.-,Cr%C3%A9ez%20votre%20propre%20bot%20Discord,-Si%20vous%20ne

### Installation
- Télécharez le code ici: https://github.com/Paillat-dev/presentator/archive/refs/heads/main.zip
- Extrayez le dossier sur votre disque dur.
- Installez pip en tapant la commande suivante dans le terminal: 
```
py -m ensurepip --upgrade
```
- Redémarrez votre ordinateur.
- Ouvrez un terminal DANS LE DOSSIER téléchargé à l'étape 1. Pour ce faire, ouvrez le dossier éxtrait, tout en maintenant la touche Maj ⇧ enfoncée, faites un clic droit sur une zone vide et sélectionnez Ouvrir une fenêtre de commandes ici.
- Tapez la commande suivante dans le terminal:
```
pip install -r requirements.txt
```
- Téléchargez le fichier Marp ici: https://github.com/marp-team/marp-cli/releases/download/v2.3.0/marp-cli-v2.3.0-win.zip
- Extrayez le contenu du fichier téléchargé dans le dossier présentateur (celui que vous avez téléchargé et éxtrait à l'étape 1).
- Redémarrez votre ordinateur.
- Mettez votre clé d'API OpenAI et votre token de bot Discord dans le fichier `.env.example` et renommez-le en `.env`.

### Génération d'images (optionnel)
- Dans le fichier `.env`, définissez la variable `USE_IMAGES` sur `dalle`. Il devrait ensuite ressebler à ceci:
```
TOKEN=_________________________________________
OPENAI=________________________________________
USE_IMAGES=dalle
COOLDOWN=5
```


## Utilisation
- Exécutez le fichier `main.py` dans un terminal ouvert dans le dossier presentator:
```
python main.py
```
- Rendez vous sur discord
- A gauche de votre écran, vous devriez voir une icone ronde avec une lettre au millieu. Il s'agit de votre serveur.
- Rendez vous dans votre serveur en cliquant dessus, puis rendez vous dans général et tapez `/present` puis la touche tab. Une boite de dialogue devrait s'afficher avec le subject, sujet de votre présentation.
