"""
Analyseur de Sentiment pour le Malagasy
Utilise le champ 'sentiment' du nouveau format du dictionnaire
"""

import json
import re
from typing import Dict, List

class AnalyseurSentiment:
    def __init__(self, dictionnaire_path: str):
        """
        Charge le dictionnaire avec les sentiments
        
        Format: {"mot": {"sentiment": "positif|negatif|neutre", ...}}
        """
        with open(dictionnaire_path, 'r', encoding='utf-8') as f:
            self.dictionnaire = json.load(f)
        
        # Créer des index par sentiment pour recherche rapide
        self.mots_positifs = set()
        self.mots_negatifs = set()
        self.mots_neutres = set()
        
        for mot, info in self.dictionnaire.items():
            sentiment = info.get('sentiment', 'neutre')
            if sentiment == 'positif':
                self.mots_positifs.add(mot.lower())
            elif sentiment == 'negatif':
                self.mots_negatifs.add(mot.lower())
            else:
                self.mots_neutres.add(mot.lower())
        
        print(f"✅ Analyseur initialisé:")
        print(f"   - Mots positifs: {len(self.mots_positifs)}")
        print(f"   - Mots négatifs: {len(self.mots_negatifs)}")
        print(f"   - Mots neutres: {len(self.mots_neutres)}")
    
    def analyser_mot(self, mot: str) -> str:
        """
        Analyse le sentiment d'un mot unique
        
        Returns:
            'positif', 'negatif' ou 'neutre'
        """
        mot_lower = mot.lower()
        
        if mot_lower in self.mots_positifs:
            return 'positif'
        elif mot_lower in self.mots_negatifs:
            return 'negatif'
        else:
            return 'neutre'
    
    def analyser_texte(self, texte: str) -> Dict:
        """
        Analyse le sentiment d'un texte complet
        
        Returns:
            {
                'sentiment_global': str,
                'score_positif': float,
                'score_negatif': float,
                'score_neutre': float,
                'mots_positifs': List[str],
                'mots_negatifs': List[str],
                'details': List[Dict]
            }
        """
        # Tokeniser le texte
        mots = re.findall(r'\b\w+\b', texte.lower())
        
        # Compter les sentiments
        count_positif = 0
        count_negatif = 0
        count_neutre = 0
        
        mots_positifs_trouves = []
        mots_negatifs_trouves = []
        details = []
        
        for mot in mots:
            sentiment = self.analyser_mot(mot)
            
            if sentiment == 'positif':
                count_positif += 1
                mots_positifs_trouves.append(mot)
            elif sentiment == 'negatif':
                count_negatif += 1
                mots_negatifs_trouves.append(mot)
            else:
                count_neutre += 1
            
            # Ajouter les détails pour chaque mot reconnu
            if mot in self.dictionnaire:
                details.append({
                    'mot': mot,
                    'sentiment': sentiment,
                    'definitions': self.dictionnaire[mot].get('definitions', [])[:1]
                })
        
        # Calculer les scores (pourcentages)
        total = len(mots)
        if total == 0:
            return {
                'sentiment_global': 'neutre',
                'score_positif': 0.0,
                'score_negatif': 0.0,
                'score_neutre': 0.0,
                'mots_positifs': [],
                'mots_negatifs': [],
                'details': []
            }
        
        score_positif = count_positif / total
        score_negatif = count_negatif / total
        score_neutre = count_neutre / total
        
        # Déterminer le sentiment global
        if score_positif > score_negatif:
            sentiment_global = 'positif'
        elif score_negatif > score_positif:
            sentiment_global = 'negatif'
        else:
            sentiment_global = 'neutre'
        
        return {
            'sentiment_global': sentiment_global,
            'score_positif': round(score_positif * 100, 2),
            'score_negatif': round(score_negatif * 100, 2),
            'score_neutre': round(score_neutre * 100, 2),
            'mots_positifs': mots_positifs_trouves,
            'mots_negatifs': mots_negatifs_trouves,
            'total_mots': total,
            'details': details
        }
    
    def obtenir_mots_par_sentiment(self, sentiment: str, limite: int = 10) -> List[Dict]:
        """
        Retourne une liste de mots avec un sentiment donné
        Utile pour affichage ou suggestions
        """
        if sentiment == 'positif':
            mots = list(self.mots_positifs)[:limite]
        elif sentiment == 'negatif':
            mots = list(self.mots_negatifs)[:limite]
        else:
            mots = list(self.mots_neutres)[:limite]
        
        resultat = []
        for mot in mots:
            if mot in self.dictionnaire:
                resultat.append({
                    'mot': mot,
                    'definitions': self.dictionnaire[mot].get('definitions', []),
                    'type': self.dictionnaire[mot].get('type')
                })
        
        return resultat

