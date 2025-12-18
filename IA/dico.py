"""
Classe pour gérer le dictionnaire Malagasy
Nouveau Format : definitions, type, exemples, Lemmatisation, synonymes, sentiment
"""

import json
from typing import List, Dict, Optional

class DictionnaireMalagasy:
    def __init__(self, fichier_path: str):
        """
        Charge le dictionnaire depuis un fichier JSON
        
        Format attendu:
        {
            "mot": {
                "definitions": [...],
                "type": "nom|verbe|adjectif|nom propre",
                "exemples": [...],
                "Lemmatisation": "racine",
                "synonymes": [...],
                "sentiment": "positif|negatif|neutre"
            }
        }
        """
        with open(fichier_path, 'r', encoding='utf-8') as f:
            self.dictionnaire = json.load(f)
        
        # Créer un index pour recherche rapide
        self.mots = set(mot.lower() for mot in self.dictionnaire.keys())
        
        print(f"✅ Dictionnaire chargé : {len(self.mots)} mots")
    
    def mot_existe(self, mot: str) -> bool:
        """Vérifie si un mot existe dans le dictionnaire"""
        return mot.lower() in self.mots
    
    def obtenir_info(self, mot: str) -> Optional[Dict]:
        """
        Récupère toutes les informations d'un mot
        
        Returns:
            dict avec toutes les clés ou None
        """
        return self.dictionnaire.get(mot.lower())
    
    def obtenir_definitions(self, mot: str) -> List[str]:
        """Récupère uniquement les définitions d'un mot"""
        info = self.obtenir_info(mot)
        if info:
            return info.get('definitions', [])
        return []
    
    def obtenir_type(self, mot: str) -> Optional[str]:
        """Récupère le type grammatical d'un mot"""
        info = self.obtenir_info(mot)
        if info:
            return info.get('type')
        return None
    
    def obtenir_exemples(self, mot: str) -> List[str]:
        """Récupère les exemples d'usage d'un mot"""
        info = self.obtenir_info(mot)
        if info:
            return info.get('exemples', [])
        return []
    
    def obtenir_lemme(self, mot: str) -> Optional[str]:
        """
        Récupère la racine/lemme d'un mot
        NOUVEAU : Utilise directement le champ Lemmatisation
        """
        info = self.obtenir_info(mot)
        if info:
            return info.get('Lemmatisation')
        return None
    
    def obtenir_synonymes(self, mot: str) -> List[str]:
        """
        Récupère les synonymes d'un mot
        NOUVEAU : Utilise le champ synonymes
        """
        info = self.obtenir_info(mot)
        if info:
            return info.get('synonymes', [])
        return []
    
    def obtenir_sentiment(self, mot: str) -> Optional[str]:
        """
        Récupère le sentiment d'un mot
        NOUVEAU : Utilise le champ sentiment
        
        Returns:
            'positif', 'negatif' ou 'neutre'
        """
        info = self.obtenir_info(mot)
        if info:
            return info.get('sentiment')
        return None
    
    def rechercher_par_type(self, type_gram: str) -> List[str]:
        """
        Trouve tous les mots d'un type grammatical donné
        
        Args:
            type_gram: 'nom', 'verbe', 'adjectif', 'nom propre'
        """
        resultats = []
        for mot, info in self.dictionnaire.items():
            if info.get('type') == type_gram:
                resultats.append(mot)
        return resultats
    
    def rechercher_par_sentiment(self, sentiment: str) -> List[str]:
        """
        NOUVEAU : Trouve tous les mots d'un sentiment donné
        
        Args:
            sentiment: 'positif', 'negatif', 'neutre'
        """
        resultats = []
        for mot, info in self.dictionnaire.items():
            if info.get('sentiment') == sentiment:
                resultats.append(mot)
        return resultats
    
    def rechercher_par_lemme(self, lemme: str) -> List[str]:
        """
        NOUVEAU : Trouve tous les mots ayant le même lemme
        Exemple: lemme='faly' → ['faly', 'mahafaly', 'mampifaly']
        """
        resultats = []
        lemme_lower = lemme.lower()
        
        for mot, info in self.dictionnaire.items():
            if info.get('Lemmatisation', '').lower() == lemme_lower:
                resultats.append(mot)
        
        return resultats
    
    def rechercher_definition(self, terme: str) -> List[str]:
        """
        Recherche un terme dans les définitions
        Retourne les mots dont la définition contient le terme
        """
        resultats = []
        terme_lower = terme.lower()
        
        for mot, info in self.dictionnaire.items():
            for definition in info.get('definitions', []):
                if terme_lower in definition.lower():
                    resultats.append(mot)
                    break
        
        return resultats
    
    def trouver_tous_synonymes(self, mot: str) -> List[str]:
        """
        NOUVEAU : Trouve tous les synonymes d'un mot
        et les synonymes de ces synonymes (récursif niveau 1)
        """
        synonymes_directs = self.obtenir_synonymes(mot)
        tous_synonymes = set(synonymes_directs)
        
        # Ajouter les synonymes des synonymes
        for syn in synonymes_directs:
            if syn in self.mots:
                synonymes_indirects = self.obtenir_synonymes(syn)
                tous_synonymes.update(synonymes_indirects)
        
        # Enlever le mot lui-même
        tous_synonymes.discard(mot.lower())
        
        return list(tous_synonymes)
    
    def ajouter_mot(self, mot: str, definitions: List[str], 
                    type_gram: str, exemples: List[str],
                    lemmatisation: str, synonymes: List[str],
                    sentiment: str = "neutre") -> bool:
        """
        Ajoute un nouveau mot au dictionnaire avec le nouveau format
        """
        mot_lower = mot.lower()
        
        if mot_lower in self.mots:
            print(f"⚠️  Le mot '{mot}' existe déjà")
            return False
        
        self.dictionnaire[mot_lower] = {
            "definitions": definitions,
            "type": type_gram,
            "exemples": exemples,
            "Lemmatisation": lemmatisation,
            "synonymes": synonymes,
            "sentiment": sentiment
        }
        self.mots.add(mot_lower)
        
        print(f"✅ Mot ajouté : {mot}")
        return True
    
    def sauvegarder(self, fichier_path: str):
        """Sauvegarde le dictionnaire dans un fichier JSON"""
        with open(fichier_path, 'w', encoding='utf-8') as f:
            json.dump(self.dictionnaire, f, ensure_ascii=False, indent=2)
        print(f"💾 Dictionnaire sauvegardé : {fichier_path}")
    
    def obtenir_stats(self) -> Dict:
        """Retourne des statistiques sur le dictionnaire"""
        stats = {
            'total': len(self.mots),
            'noms': 0,
            'verbes': 0,
            'adjectifs': 0,
            'noms_propres': 0,
            'autres': 0,
            'positifs': 0,
            'negatifs': 0,
            'neutres': 0
        }
        
        for info in self.dictionnaire.values():
            # Compter par type
            type_mot = info.get('type', 'autre')
            if type_mot == 'nom':
                stats['noms'] += 1
            elif type_mot == 'verbe':
                stats['verbes'] += 1
            elif type_mot == 'adjectif':
                stats['adjectifs'] += 1
            elif type_mot == 'nom propre':
                stats['noms_propres'] += 1
            else:
                stats['autres'] += 1
            
            # Compter par sentiment
            sentiment = info.get('sentiment', 'neutre')
            if sentiment == 'positif':
                stats['positifs'] += 1
            elif sentiment == 'negatif':
                stats['negatifs'] += 1
            else:
                stats['neutres'] += 1
        
        return stats


# ===== EXEMPLE D'UTILISATION =====

if __name__ == "__main__":
    # Créer un dictionnaire de test avec le nouveau format
    dico_test = {
        "vary": {
            "definitions": ["céréale cultivée à Madagascar", "riz"],
            "type": "nom",
            "exemples": ["Mihinana vary aho", "Tanimbary"],
            "Lemmatisation": "vary",
            "synonymes": ["vary"],
            "sentiment": "neutre"
        },
        "mandeha": {
            "definitions": ["aller", "partir", "se déplacer"],
            "type": "verbe",
            "exemples": ["Mandeha any Tana aho", "Mandeha daholo"],
            "Lemmatisation": "deha",
            "synonymes": ["mizotra", "mifindra"],
            "sentiment": "neutre"
        },
        "tsara": {
            "definitions": ["bon", "bien", "beau"],
            "type": "adjectif",
            "exemples": ["Tsara loatra io", "Olona tsara"],
            "Lemmatisation": "tsara",
            "synonymes": ["soa", "mendrika"],
            "sentiment": "positif"
        },
        "mahafaly": {
            "definitions": ["rendre heureux", "réjouir"],
            "type": "verbe",
            "exemples": ["Mahafaly ahy io"],
            "Lemmatisation": "faly",
            "synonymes": ["mampifaly", "mahafinaritra"],
            "sentiment": "positif"
        },
        "faly": {
            "definitions": ["joyeux", "content", "heureux"],
            "type": "adjectif",
            "exemples": ["Faly aho"],
            "Lemmatisation": "faly",
            "synonymes": ["sambatra", "ravoravo"],
            "sentiment": "positif"
        }
    }
    
    # Sauvegarder le dictionnaire de test
    with open('dictionnaire_test.json', 'w', encoding='utf-8') as f:
        json.dump(dico_test, f, ensure_ascii=False, indent=2)
    
    # Charger et utiliser
    dico = DictionnaireMalagasy('dictionnaire_test.json')
    
    print("\n=== Test 1 : Obtenir lemme ===")
    lemme = dico.obtenir_lemme('mandeha')
    print(f"Lemme de 'mandeha' : {lemme}")
    
    print("\n=== Test 2 : Obtenir synonymes ===")
    synonymes = dico.obtenir_synonymes('tsara')
    print(f"Synonymes de 'tsara' : {synonymes}")
    
    print("\n=== Test 3 : Obtenir sentiment ===")
    sentiment = dico.obtenir_sentiment('mahafaly')
    print(f"Sentiment de 'mahafaly' : {sentiment}")
    
    print("\n=== Test 4 : Rechercher par sentiment ===")
    mots_positifs = dico.rechercher_par_sentiment('positif')
    print(f"Mots positifs : {mots_positifs}")
    
    print("\n=== Test 5 : Rechercher par lemme ===")
    mots_famille_faly = dico.rechercher_par_lemme('faly')
    print(f"Mots de la famille de 'faly' : {mots_famille_faly}")
    
    print("\n=== Test 6 : Tous les synonymes ===")
    tous_syn = dico.trouver_tous_synonymes('tsara')
    print(f"Tous les synonymes de 'tsara' : {tous_syn}")
    
    print("\n=== Test 7 : Statistiques ===")
    stats = dico.obtenir_stats()
    print(f"Statistiques du dictionnaire :")
    for cle, valeur in stats.items():
        print(f"  {cle}: {valeur}")
    
    print("\n✅ Tous les tests réussis avec le nouveau format !")