## TP-IA-CLINIQUE

Éditeur de texte intelligent pour la langue malagasy, avec un **frontend Next.js** moderne et une **API NLP Python** dédiée au traitement automatique du malagasy (tokenisation, lemmatisation, correction, sentiment, n‑grams, etc.).


### **1\. Informations sur le Groupe**

Merci de lister tous les membres de l'équipe ayant participé au Hackathon.

#### Membre 1 : 
* nom : RAZAFINDRAMENA 
* prénom(s) : Stephano
* classe : ISAIA 5
* numéro : 09
* rôle : Développeur

#### Membre 2 : 
* nom : RALAIARISON 
* prénom(s) : Mahery
* classe : ISAIA 5
* numéro : 07
* rôle : Développeur

#### Membre 3 : 
* nom : NIRINARIVONJY
* prénom(s) : Andoniaina Ifaliana
* classe : ISAIA 5
* numéro : 11
* rôle : Analyste

#### Membre 4 : 
* nom : ANJARAMBOLATIANA
* prénom(s) : Mélanie
* classe : IGGLIA 5
* numéro : 31
* rôle : Analyste

#### Membre 5 : 
* nom : RAMANGALAHY
* prénom(s) : Nirina Nathanael
* classe : ISAIA 5
* numéro : 05
* rôle : Développeur

#### Membre 6 : 
* nom : ANDRIAMAMPIANINA
* prénom(s) : Fitia Nomena Andrianina
* classe : IGGLIA 5
* numéro : 03
* rôle : Présentateur

#### Membre 7 : 
* nom : RAMAROVAO
* prénom(s) : Tombontsoa Harisanda
* classe : IGGLIA 5
* numéro : 21
* rôle : Développeur


### Structure du projet

- **frontend/** : application web (Next.js, React, Tailwind) – interface d’édition et de démonstration.
- **IA/** : backend Python (FastAPI) – API NLP Malagasy + scripts de traitement (correcteur, analyseur de sentiment, nettoyage de corpus, pipeline NLP).

### Prérequis

- **Node.js** (version compatible avec votre environnement, recommandé ≥ 20)
- **Python 3.10+**
- `pip` pour installer les dépendances Python

### Installation et lancement – Frontend

```bash
cd frontend
npm install          # installe les dépendances Node
npm run dev          # lance le serveur Next.js en mode développement
```

Puis ouvrez `http://localhost:3000` dans votre navigateur.  
La page principale décrit l’éditeur, et la route `/demo` contient la démo interactive.

### Installation et lancement – Backend IA

```bash
cd IA
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L’API sera disponible sur `http://localhost:8000`. La documentation interactive Swagger se trouve sur `http://localhost:8000/docs`.

### Principaux endpoints FastAPI (IA/main.py)

- **GET `/`** : informations générales sur l’API NLP Malagasy.
- **POST `/api/analyser-texte`** : analyse complète (tokens, lemmes, POS, entités, sentiment, stats).
- **POST `/api/corriger`** : correction orthographique et suggestions.
- **POST `/api/tokenize`** : découpage du texte en tokens.
- **POST `/api/lemmatiser`** : lemmatisation d’un mot.
- **POST `/api/pos-tag`** : étiquetage grammatical.
- **POST `/api/entites`** : extraction d’entités nommées.
- **POST `/api/sentiment`** : analyse de sentiment.
- **POST `/api/predire-mot-suivant`** : prédiction de mot via n‑grams.
- **GET `/api/synonymes/{mot}`** : obtention de synonymes à partir du dictionnaire.
- **GET `/health`** : health check de l’API.

### Scripts NLP principaux (dossier `IA/`)

- **`main.py`** : API NLP (tokenisation, POS, NER, sentiment, n‑grams, analyse complète).
- **`nlp_malagasy.py`** : pipeline NLP (tokenisation, POS, NER, sentiment, n‑grams, analyse complète).
- **`corrector.py`** : correcteur orthographique basé sur dictionnaire + RapidFuzz.
- **`sentiment_analyzer.py`** : analyseur de sentiment utilisant les champs de sentiment du dictionnaire.
- **`cleaner.py`** : nettoyage de fichiers PDF (PyMuPDF) pour produire un corpus texte (`cleaned_bible.txt`).
- **`dictionary.json`** : dictionnaire de test.

### Développement et contributions

- Frontend : adapter les appels API (via `axios`) pour consommer les endpoints listés ci‑dessus.
- Backend : étendre le dictionnaire et les règles linguistiques pour améliorer la qualité des suggestions, de l’analyse et de la prédiction.

Ce projet sert de **preuve de concept** pour montrer comment l’IA peut soutenir une langue à faibles ressources comme le malagasy dans un contexte clinique / éditorial.

### Bibliographie

- **Dictionnaire malagasy Tenymalagasy** – données lexicales et exemples d’usage : [`https://tenymalagasy.org/bins/alphaLists`](https://tenymalagasy.org/bins/alphaLists)
- **Wikipédia (versions malagasy et française)** – articles encyclopédiques pour enrichir le corpus généraliste.
- **Corpus biblique en malagasy** – texte biblique nettoyé et utilisé comme corpus de référence (`cleaned_bible.txt`).
- **Baiboly malagasy en ligne** – texte biblique en malagasy pour la constitution du corpus : [`https://nybaiboly.net/Bible/BibleMalagasyHtm-at01-Genese.htm`](https://nybaiboly.net/Bible/BibleMalagasyHtm-at01-Genese.htm)