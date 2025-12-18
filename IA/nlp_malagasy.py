"""
Pipeline NLP Complet pour le Malagasy
"""

import json
import re
from collections import defaultdict, Counter
from typing import List, Dict, Tuple

class NLPMalagasy:
    """
    Pipeline NLP complet pour le traitement du texte malagasy
    """
    
    def __init__(self, dictionnaire_path: str, corpus_path: str = None):
        """
        Initialise le pipeline NLP
        
        Args:
            dictionnaire_path: Chemin vers le dictionnaire JSON
            corpus_path: Chemin vers un corpus de texte (optionnel, pour n-grams)
        """
        # Charger le dictionnaire
        with open(dictionnaire_path, 'r', encoding='utf-8') as f:
            self.dictionnaire = json.load(f)
        
        print(f"✅ Pipeline NLP initialisé avec {len(self.dictionnaire)} mots")
        
        # Préparer les structures pour NLP
        self._preparer_structures()
        
        # Charger corpus pour n-grams si disponible
        if corpus_path:
            self._entrainer_ngrams(corpus_path)
    
    def _preparer_structures(self):
        """Prépare les index pour accès rapide"""
        self.mots_valides = set(self.dictionnaire.keys())
        
        # Index par type grammatical (POS)
        self.pos_index = defaultdict(set)
        for mot, info in self.dictionnaire.items():
            type_gram = info.get('type', 'inconnu')
            self.pos_index[type_gram].add(mot)
        
        # Index des entités nommées (NER)
        self.entites = {
            'villes': set(),
            'personnes': set(),
            'lieux': set()
        }
        
        for mot, info in self.dictionnaire.items():
            if info.get('type') == 'nom propre':
                # Classifier les noms propres (simple heuristique)
                definitions = ' '.join(info.get('definitions', [])).lower()
                if 'ville' in definitions or 'capitale' in definitions:
                    self.entites['villes'].add(mot)
                elif 'lieu' in definitions or 'région' in definitions:
                    self.entites['lieux'].add(mot)
                else:
                    self.entites['personnes'].add(mot)
        
        # N-grams (initialisé vide, sera rempli par corpus)
        self.bigrams = defaultdict(Counter)
        self.trigrams = defaultdict(Counter)
    
    def _entrainer_ngrams(self, corpus_path: str):
        """Entraîne les modèles n-grams sur un corpus"""
        try:
            with open(corpus_path, 'r', encoding='utf-8') as f:
                texte = f.read().lower()
            
            mots = self.tokenize(texte)
            
            # Créer bigrammes
            for i in range(len(mots) - 1):
                self.bigrams[mots[i]][mots[i+1]] += 1
            
            # Créer trigrammes
            for i in range(len(mots) - 2):
                cle = (mots[i], mots[i+1])
                self.trigrams[cle][mots[i+2]] += 1
            
            print(f"✅ N-grams entraînés sur {len(mots)} mots")
        except FileNotFoundError:
            print("⚠️  Corpus non trouvé, n-grams non disponibles")
    
    # ==================== MODULE 1 : TOKENIZATION ====================
    
    def tokenize(self, texte: str) -> List[str]:
        """
        Découpe le texte en tokens (mots)
        Prend en compte les spécificités du malagasy
        """
        # Normaliser
        texte = texte.lower()
        
        # Extraire les mots (lettres et apostrophes)
        tokens = re.findall(r"\b[\w']+\b", texte)
        
        return tokens
    
    # ==================== MODULE 2 : LEMMATIZATION ====================
    
    def lemmatiser(self, mot: str) -> str:
        """
        Retrouve la racine d'un mot
        Utilise le champ 'Lemmatisation' du dictionnaire
        """
        mot_lower = mot.lower()
        
        # Si le mot est dans le dictionnaire
        if mot_lower in self.dictionnaire:
            return self.dictionnaire[mot_lower].get('Lemmatisation', mot_lower)
        
        # Sinon, appliquer des règles morphologiques
        return self._lemmatiser_par_regles(mot_lower)
    
    def _lemmatiser_par_regles(self, mot: str) -> str:
        """Lemmatisation basée sur les règles morphologiques malagasy"""
        # Préfixes courants
        prefixes = ['mpan', 'mpam', 'maha', 'man', 'mam', 'mi', 'ma', 
                   'fan', 'fam', 'fi', 'an', 'amp']
        
        # Suffixes courants
        suffixes = ['ana', 'ina', 'na', 'nao', 'ko']
        
        racine = mot
        
        # Retirer préfixes
        for prefixe in sorted(prefixes, key=len, reverse=True):
            if racine.startswith(prefixe) and len(racine) > len(prefixe) + 2:
                racine = racine[len(prefixe):]
                break
        
        # Retirer suffixes
        for suffixe in sorted(suffixes, key=len, reverse=True):
            if racine.endswith(suffixe) and len(racine) > len(suffixe) + 2:
                racine = racine[:-len(suffixe)]
                break
        
        return racine
    
    # ==================== MODULE 3 : POS TAGGING ====================
    
    def pos_tag(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """
        Étiquetage grammatical (Part-of-Speech)
        
        Returns:
            Liste de tuples (mot, type_grammatical)
        """
        resultats = []
        
        for token in tokens:
            token_lower = token.lower()
            
            if token_lower in self.dictionnaire:
                type_gram = self.dictionnaire[token_lower].get('type', 'inconnu')
            else:
                # Heuristiques pour mots inconnus
                type_gram = self._deviner_pos(token_lower)
            
            resultats.append((token, type_gram))
        
        return resultats
    
    def _deviner_pos(self, mot: str) -> str:
        """Devine le type grammatical avec des heuristiques"""
        # Verbes actifs commencent souvent par 'mi-', 'man-', 'ma-'
        if mot.startswith(('mi', 'man', 'mam', 'ma')):
            return 'verbe'
        
        # Noms d'action finissent en '-ana'
        if mot.endswith('ana'):
            return 'nom'
        
        # Adjectifs avec préfixe 'maha-'
        if mot.startswith('maha'):
            return 'adjectif'
        
        return 'inconnu'
    
    # ==================== MODULE 4 : NER (Named Entity Recognition) ====================
    
    def extraire_entites(self, texte: str) -> Dict[str, List[str]]:
        """
        Reconnaissance d'entités nommées
        
        Returns:
            {'villes': [...], 'personnes': [...], 'lieux': [...]}
        """
        tokens = self.tokenize(texte)
        
        entites_trouvees = {
            'villes': [],
            'personnes': [],
            'lieux': [],
            'autres': []
        }
        
        for token in tokens:
            # Capitalisation = probablement nom propre
            if token[0].isupper():
                token_lower = token.lower()
                
                if token_lower in self.entites['villes']:
                    entites_trouvees['villes'].append(token)
                elif token_lower in self.entites['personnes']:
                    entites_trouvees['personnes'].append(token)
                elif token_lower in self.entites['lieux']:
                    entites_trouvees['lieux'].append(token)
                else:
                    entites_trouvees['autres'].append(token)
        
        return entites_trouvees
    
    # ==================== MODULE 5 : SENTIMENT ANALYSIS ====================
    
    def analyser_sentiment(self, texte: str) -> Dict:
        """
        Analyse le sentiment d'un texte
        """
        tokens = self.tokenize(texte)
        
        sentiments = {'positif': 0, 'negatif': 0, 'neutre': 0}
        mots_sentiments = {'positif': [], 'negatif': [], 'neutre': []}
        
        for token in tokens:
            if token in self.dictionnaire:
                sentiment = self.dictionnaire[token].get('sentiment', 'neutre')
                sentiments[sentiment] += 1
                mots_sentiments[sentiment].append(token)
        
        total = sum(sentiments.values())
        if total == 0:
            return {
                'sentiment_dominant': 'neutre',
                'scores': sentiments,
                'mots': mots_sentiments
            }
        
        # Trouver le sentiment dominant
        sentiment_dominant = max(sentiments.items(), key=lambda x: x[1])[0]
        
        # Calculer scores en pourcentage
        scores_pct = {k: round(v/total*100, 1) for k, v in sentiments.items()}
        
        return {
            'sentiment_dominant': sentiment_dominant,
            'scores': scores_pct,
            'mots': mots_sentiments
        }
    
    # ==================== MODULE 6 : N-GRAMS PREDICTION ====================
    
    def predire_mot_suivant(self, contexte: str, n: int = 5) -> List[Tuple[str, int]]:
        """
        Prédit les n mots les plus probables après le contexte
        """
        tokens = self.tokenize(contexte)
        
        if len(tokens) >= 2:
            # Utiliser trigrammes
            cle = (tokens[-2], tokens[-1])
            if cle in self.trigrams:
                return self.trigrams[cle].most_common(n)
        
        if len(tokens) >= 1:
            # Utiliser bigrammes
            if tokens[-1] in self.bigrams:
                return self.bigrams[tokens[-1]].most_common(n)
        
        return []
    
    # ==================== MODULE 7 : SYNONYM DETECTION ====================
    
    def obtenir_synonymes(self, mot: str) -> List[str]:
        """Récupère les synonymes d'un mot"""
        mot_lower = mot.lower()
        
        if mot_lower in self.dictionnaire:
            return self.dictionnaire[mot_lower].get('synonymes', [])
        
        return []
    
    # ==================== MODULE 8 : ANALYSE COMPLETE ====================
    
    def analyser_texte_complet(self, texte: str) -> Dict:
        """
        Pipeline NLP complet : analyse tous les aspects du texte
        """
        # 1. Tokenization
        tokens = self.tokenize(texte)
        
        # 2. Lemmatisation
        lemmes = [self.lemmatiser(token) for token in tokens]
        
        # 3. POS Tagging
        pos_tags = self.pos_tag(tokens)
        
        # 4. NER
        entites = self.extraire_entites(texte)
        
        # 5. Sentiment
        sentiment = self.analyser_sentiment(texte)
        
        # 6. Statistiques
        stats = {
            'nombre_mots': len(tokens),
            'mots_uniques': len(set(tokens)),
            'distribution_pos': self._compter_pos(pos_tags)
        }
        
        return {
            'tokens': tokens,
            'lemmes': lemmes,
            'pos_tags': pos_tags,
            'entites': entites,
            'sentiment': sentiment,
            'statistiques': stats
        }
    
    def _compter_pos(self, pos_tags: List[Tuple[str, str]]) -> Dict[str, int]:
        """Compte la distribution des types grammaticaux"""
        compteur = Counter(tag for _, tag in pos_tags)
        return dict(compteur)


# Initialiser le pipeline
nlp = NLPMalagasy('dico_nlp_test.json', 'cleaned_bible.txt')
