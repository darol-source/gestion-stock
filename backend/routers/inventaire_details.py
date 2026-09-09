from fastapi import APIRouter, HTTPException

from schemas import (
    InventaireDetailCreate,
    InventaireDetailResponse
)

import crud


router = APIRouter(
    prefix="/api/inventaire-details",
    tags=["Détails Inventaire"]
)


@router.post("/", response_model=InventaireDetailResponse)
def creer_inventaire_detail(
    detail: InventaireDetailCreate
):

    resultat = crud.creer_inventaire_detail(
        detail.idInventaire,
        detail.idUnite,
        detail.idDepotSysteme,
        detail.idDepotConstate,
        detail.etatSysteme,
        detail.etatConstate,
        detail.emplacementCorrect,
        detail.etatCorrect,
        detail.anomalie
    )

    if isinstance(resultat, dict) and "erreur" in resultat:
        raise HTTPException(
            status_code=400,
            detail=resultat["erreur"]
        )

    return resultat


@router.get("/")
def obtenir_inventaire_details():
    return crud.obtenir_inventaire_details()


@router.get("/inventaire/{idInventaire}")
def obtenir_details_inventaire(idInventaire: int):
    return crud.obtenir_details_inventaire(idInventaire)


@router.get("/unite/{idUnite}")
def obtenir_details_unite(idUnite: int):
    return crud.obtenir_details_unite(idUnite)


@router.get("/{idDetail}")
def obtenir_inventaire_detail(idDetail: int):

    detail = crud.obtenir_inventaire_detail(idDetail)

    if detail is None:
        raise HTTPException(
            status_code=404,
            detail="Détail d'inventaire introuvable"
        )

    return detail