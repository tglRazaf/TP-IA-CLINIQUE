"""
API Backend FastAPI pour l'Éditeur de Texte Malagasy
Intègre tous les modules NLP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
from nlp_malagasy import nlp

# Importer vos classes NLP (à créer dans des fichiers séparés)
# from nlp_pipeline import NLPMalagasy
# from correcteur import CorrecteurMalagasy
# from analyseur_sentiment import AnalyseurSentiment

# ===== MODÈLES DE DONNÉES =====

class TexteRequest(BaseModel):
    texte: str

class MotRequest(BaseModel):
    mot: str

class PredictionRequest(BaseModel):
    contexte: str
    limite: Optional[int] = 5

class AnalyseResponse(BaseModel):
    tokens: List[str]
    lemmes: List[str]
    pos_tags: List[tuple]
    entites: Dict[str, List[str]]
    sentiment: Dict
    statistiques: Dict

# ===== INITIALISATION =====

app = FastAPI(
    title="API NLP Malagasy",
    description="API pour l'éditeur de texte augmenté par l'IA",
    version="1.0.0"
)

# CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser les modules NLP (au démarrage de l'application)
# nlp = NLPMalagasy('data/dictionnaire.json', 'data/corpus.txt')
# correcteur = CorrecteurMalagasy('data/dictionnaire.json')
# analyseur_sentiment = AnalyseurSentiment('data/dictionnaire.json')

# Pour la démo, on simule les modules
class NLPDemo:
    def tokenize(self, texte):
        return texte.split()
    
    def lemmatiser(self, mot):
        return mot
    
    def pos_tag(self, tokens):
        return [(t, "nom") for t in tokens]
    
    def extraire_entites(self, texte):
        return {"villes": [], "personnes": []}
    
    def analyser_sentiment(self, texte):
        return {"sentiment_dominant": "neutre", "scores": {"positif": 0}}
    
    def analyser_texte_complet(self, texte):
        tokens = self.tokenize(texte)
        return {
            "tokens": tokens,
            "lemmes": tokens,
            "pos_tags": [(t, "nom") for t in tokens],
            "entites": {},
            "sentiment": {"sentiment_dominant": "neutre"},
            "statistiques": {"nombre_mots": len(tokens)}
        }
    
    def predire_mot_suivant(self, contexte, n):
        return [("vary", 5), ("sakafo", 3)]
    
    def obtenir_synonymes(self, mot):
        return ["soa", "mendrika"]

# ===== ENDPOINTS =====

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "API NLP Malagasy",
        "version": "1.0.0",
        "endpoints": {
            "analyse_complete": "/api/analyser-texte",
            "correction": "/api/corriger",
            "tokenization": "/api/tokenize",
            "lemmatisation": "/api/lemmatiser",
            "pos_tagging": "/api/pos-tag",
            "ner": "/api/entites",
            "sentiment": "/api/sentiment",
            "prediction": "/api/predire-mot",
            "synonymes": "/api/synonymes",
        }
    }

# ===== MODULE 1 : ANALYSE COMPLÈTE =====

@app.post("/api/analyser-texte")
async def analyser_texte(request: TexteRequest):
    """
    Analyse NLP complète d'un texte
    Retourne : tokens, lemmes, POS tags, entités, sentiment, stats
    """
    try:
        analyse = nlp.analyser_texte_complet(request.texte)
        return {
            "success": True,
            "data": analyse
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 2 : CORRECTION ORTHOGRAPHIQUE =====

@app.post("/api/corriger")
async def corriger_texte(request: TexteRequest):
    """
    Vérifie l'orthographe et suggère des corrections
    """
    try:
        # erreurs = correcteur.corriger_texte(request.texte)
        # Simulation
        erreurs = [
            {
                "position": 0,
                "mot_original": "vari",
                "suggestions": ["vary", "voara"],
                "confiance": "haute"
            }
        ]
        
        return {
            "success": True,
            "erreurs": erreurs,
            "nombre_erreurs": len(erreurs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 3 : TOKENIZATION =====

@app.post("/api/tokenize")
async def tokenize(request: TexteRequest):
    """Découpe le texte en tokens"""
    try:
        tokens = nlp.tokenize(request.texte)
        return {
            "success": True,
            "tokens": tokens,
            "nombre_tokens": len(tokens)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 4 : LEMMATISATION =====

@app.post("/api/lemmatiser")
async def lemmatiser(request: MotRequest):
    """Retrouve la racine d'un mot"""
    try:
        lemme = nlp.lemmatiser(request.mot)
        return {
            "success": True,
            "mot": request.mot,
            "lemme": lemme
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 5 : POS TAGGING =====

@app.post("/api/pos-tag")
async def pos_tag(request: TexteRequest):
    """Étiquetage grammatical des mots"""
    try:
        tokens = nlp.tokenize(request.texte)
        pos_tags = nlp.pos_tag(tokens)
        
        return {
            "success": True,
            "pos_tags": [
                {"mot": mot, "type": tag} 
                for mot, tag in pos_tags
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 6 : NER (Named Entity Recognition) =====

@app.post("/api/entites")
async def extraire_entites(request: TexteRequest):
    """Extrait les entités nommées du texte"""
    try:
        entites = nlp.extraire_entites(request.texte)
        return {
            "success": True,
            "entites": entites
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 7 : SENTIMENT ANALYSIS =====

@app.post("/api/sentiment")
async def analyser_sentiment(request: TexteRequest):
    """Analyse le sentiment du texte"""
    try:
        sentiment = nlp.analyser_sentiment(request.texte)
        return {
            "success": True,
            "sentiment": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 8 : N-GRAMS PREDICTION =====

@app.post("/api/predire-mot-suivant")
async def predire_mot(request: PredictionRequest):
    """Prédit le mot suivant basé sur le contexte"""
    try:
        predictions = nlp.predire_mot_suivant(
            request.contexte, 
            request.limite
        )
        
        return {
            "success": True,
            "predictions": [
                {"mot": mot, "frequence": freq}
                for mot, freq in predictions
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MODULE 9 : SYNONYMES =====

@app.get("/api/synonymes/{mot}")
async def obtenir_synonymes(mot: str):
    """Récupère les synonymes d'un mot"""
    try:
        synonymes = nlp.obtenir_synonymes(mot)
        return {
            "success": True,
            "mot": mot,
            "synonymes": synonymes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== HEALTH CHECK =====

@app.get("/health")
async def health_check():
    """Vérifie que l'API fonctionne"""
    return {
        "status": "healthy",
        "modules": {
            "nlp_pipeline": "OK",
            "correcteur": "OK",
            "analyseur_sentiment": "OK"
        }
    }

# ===== STATISTIQUES =====

@app.get("/api/stats")
async def obtenir_stats():
    """Retourne des statistiques sur le système"""
    return {
        "success": True,
        "stats": {
            "mots_dictionnaire": 5000,  # À remplacer par len(nlp.dictionnaire)
            "corpus_size": "100k mots",
            "modules_actifs": 9
        }
    }

# ===== LANCEMENT =====

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Lancement de l'API NLP Malagasy...")
    print("📝 Documentation disponible sur : http://localhost:8000/docs")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True  # Auto-reload en développement
    )