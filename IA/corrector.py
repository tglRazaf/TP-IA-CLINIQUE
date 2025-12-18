"""
Correcteur Orthographique Malagasy
Adapté au nouveau format du dictionnaire
"""

import json
import re
from rapidfuzz import fuzz, process
from typing import List, Tuple, Dict

class CorrecteurMalagasy:
    def __init__(self, dictionnaire_path: str):
        """
        Args:
            dictionnaire_path: chemin vers le fichier JSON du dictionnaire
            Format: {"mot": {"definitions": [...], "type": "...", "exemples": [...], 
                     "Lemmatisation": "...", "synonymes": [...], "sentiment": "..."}}
        """
        # Charger le dictionnaire
        with open(dictionnaire_path, 'r', encoding='utf-8') as f:
            self.dictionnaire = json.load(f)
        
        # Créer un set de mots valides pour recherche rapide
        self.mots_valides = set(mot.lower() for mot in self.dictionnaire.keys())
        
        # Règles phonotactiques malagasy (combinaisons impossibles)
        self.combinaisons_interdites = [
            'nb', 'mk', 'nk', 'dt', 'bp', 'sz', 'zs', 
            'kg', 'gb', 'pb', 'tp', 'fd', 'gd'
        ]
        
        print(f"✅ Correcteur initialisé avec {len(self.mots_valides)} mots")
    
    def verifier_phonotactique(self, mot: str) -> Tuple[bool, List[str]]:
        """
        Vérifie si le mot respecte les règles phonotactiques du malagasy
        
        Returns:
            (est_valide, liste_violations)
        """
        mot_lower = mot.lower()
        violations = []
        
        for combinaison in self.combinaisons_interdites:
            if combinaison in mot_lower:
                violations.append(f"'{combinaison}' n'existe pas en malagasy")
        
        return len(violations) == 0, violations
    
    def verifier_mot(self, mot: str) -> Dict:
        """
        Vérifie un mot et retourne un rapport complet
        
        Returns:
            {
                'mot': str,
                'est_correct': bool,
                'suggestions': List[str],
                'suggestions_avec_info': List[Dict],  # NOUVEAU
                'violations': List[str],
                'info_mot': Dict ou None
            }
        """
        mot_clean = re.sub(r'[^\w]', '', mot).lower()
        
        if not mot_clean:
            return {
                'mot': mot,
                'est_correct': True,
                'suggestions': [],
                'suggestions_avec_info': [],
                'violations': [],
                'info_mot': None
            }
        
        # 1. Vérifier si le mot existe dans le dictionnaire
        if mot_clean in self.mots_valides:
            return {
                'mot': mot,
                'est_correct': True,
                'suggestions': [],
                'suggestions_avec_info': [],
                'violations': [],
                'info_mot': self.dictionnaire[mot_clean]
            }
        
        # 2. Vérifier la phonotactique
        est_valide_phono, violations = self.verifier_phonotactique(mot_clean)
        
        # 3. Trouver des suggestions avec Levenshtein
        suggestions_brutes = process.extract(
            mot_clean,
            self.mots_valides,
            scorer=fuzz.ratio,
            limit=5,
            score_cutoff=60  # Minimum 60% de similarité
        )
        
        suggestions = [s[0] for s in suggestions_brutes]
        
        # 4. NOUVEAU : Enrichir les suggestions avec infos du dictionnaire
        suggestions_avec_info = []
        for suggestion in suggestions:
            info = self.dictionnaire.get(suggestion, {})
            suggestions_avec_info.append({
                'mot': suggestion,
                'definitions': info.get('definitions', [])[:2],  # 2 premières définitions
                'type': info.get('type'),
                'sentiment': info.get('sentiment')
            })
        
        return {
            'mot': mot,
            'est_correct': False,
            'suggestions': suggestions,
            'suggestions_avec_info': suggestions_avec_info,
            'violations': violations,
            'info_mot': None,
            'confiance': 'faible' if violations else 'moyenne'
        }
    
    def corriger_texte(self, texte: str) -> List[Dict]:
        """
        Corrige un texte complet et retourne toutes les erreurs trouvées
        
        Returns:
            Liste de dictionnaires avec les erreurs et suggestions
        """
        mots = re.findall(r'\b\w+\b', texte)
        resultats = []
        
        for i, mot in enumerate(mots):
            verification = self.verifier_mot(mot)
            
            if not verification['est_correct']:
                resultats.append({
                    'position': i,
                    'mot_original': mot,
                    'suggestions': verification['suggestions'],
                    'suggestions_detaillees': verification['suggestions_avec_info'],
                    'violations_phono': verification['violations'],
                    'confiance': verification.get('confiance', 'moyenne')
                })
        
        return resultats
    
    def obtenir_synonymes_pour_correction(self, mot: str) -> List[str]:
        """
        NOUVEAU : Utilise les synonymes pour des corrections alternatives
        """
        if mot.lower() in self.mots_valides:
            info = self.dictionnaire[mot.lower()]
            return info.get('synonymes', [])
        return []


corrector = CorrecteurMalagasy('dictionary.json')

print(corrector.verifier_mot('alad'))