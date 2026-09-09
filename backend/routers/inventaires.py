from fastapi import APIRouter, HTTPException

from schemas import (
    InventaireCreate,
    InventaireTerminer,
    InventaireResponse
)

import crud


router = APIRouter(
    prefix="/api/inventaires",
    tags=["Inventaires"]
)


@router.post("/", response_model=InventaireResponse)
def creer_inventaire(inventaire: InventaireCreate):

    resultat = crud.creer_inventaire(
        inventaire.idDepot,
        inventaire.idUtilisateur,
        inventaire.dateDebut
    )

    if isinstance(resultat, dict) and "erreur" in resultat:
        raise HTTPException(
            status_code=400,
            detail=resultat["erreur"]
        )

    return resultat


@router.put("/{idInventaire}/terminer", response_model=InventaireResponse)
def terminer_inventaire(
    idInventaire: int,
    donnees: InventaireTerminer
):

    resultat = crud.terminer_inventaire(
        idInventaire,
        donnees.dateFin
    )

    if isinstance(resultat, dict) and "erreur" in resultat:
        raise HTTPException(
            status_code=400,
            detail=resultat["erreur"]
        )

    return resultat


@router.get("/")
def obtenir_inventaires():
    return crud.obtenir_inventaires()


# IMPORTANT :
# Cette route doit être avant /{idInventaire}
@router.get("/depot/{idDepot}")
def obtenir_inventaires_depot(idDepot: int):

    return crud.obtenir_inventaires_depot(idDepot)


@router.get("/{idInventaire}")
def obtenir_inventaire(idInventaire: int):

    inventaire = crud.obtenir_inventaire(idInventaire)

    if inventaire is None:
        raise HTTPException(
            status_code=404,
            detail="Inventaire introuvable"
        )

    return inventaire