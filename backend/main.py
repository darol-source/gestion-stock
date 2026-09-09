from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    produits,
    depots,
    utilisateurs,
    unites,
    entrees,
    transferts,
    sorties,
    inventaires,
    inventaire_details,
    signalements,
    journal_actions,
    auth
)


app = FastAPI(
    title="Gestion de Stock API",
    description="API de gestion des produits, dépôts, unités et inventaires",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produits.router)
app.include_router(depots.router)
app.include_router(utilisateurs.router)
app.include_router(unites.router)
app.include_router(entrees.router)
app.include_router(transferts.router)
app.include_router(sorties.router)
app.include_router(inventaires.router)
app.include_router(inventaire_details.router)
app.include_router(signalements.router)
app.include_router(journal_actions.router)

app.include_router(auth.router)
app.include_router(journal_actions.router)

@app.get("/")
def accueil():
    return {
        "message": "API Gestion de Stock opérationnelle"
    }


@app.get("/api/test")
def test_api():
    return {
        "message": "Connexion API réussie"
    }