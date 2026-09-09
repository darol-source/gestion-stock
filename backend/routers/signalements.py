from fastapi import APIRouter, HTTPException

from schemas import (
    SignalementCreate,
    SignalementUpdate,
    SignalementResponse
)

import crud


router = APIRouter(
    prefix="/api/signalements",
    tags=["Signalements"]
)


@router.post("/", response_model=SignalementResponse)
def creer_signalement(signalement: SignalementCreate):

    resultat = crud.creer_signalement(
        signalement.idInventaire,
        signalement.idDetail,
        signalement.idUtilisateur,
        signalement.typeSignalement,
        signalement.description,
        signalement.dateSignalement
    )

    if isinstance(resultat, dict) and "erreur" in resultat:
        raise HTTPException(
            status_code=400,
            detail=resultat["erreur"]
        )

    return resultat


@router.put("/{idSignalement}", response_model=SignalementResponse)
def modifier_signalement(
    idSignalement: int,
    signalement: SignalementUpdate
):

    resultat = crud.modifier_signalement(
        idSignalement,
        signalement.statut,
        signalement.resolution,
        signalement.dateResolution
    )

    if isinstance(resultat, dict) and "erreur" in resultat:
        raise HTTPException(
            status_code=400,
            detail=resultat["erreur"]
        )

    return resultat


@router.get("/")
def obtenir_signalements():
    return crud.obtenir_signalements()



@router.get("/inventaire/{idInventaire}")
def obtenir_signalements_inventaire(idInventaire: int):
    return crud.obtenir_signalements_inventaire(idInventaire)


@router.get("/statut/{statut}")
def obtenir_signalements_statut(statut: str):
    return crud.obtenir_signalements_statut(statut)


@router.get("/{idSignalement}")
def obtenir_signalement(idSignalement: int):

    signalement = crud.obtenir_signalement(idSignalement)

    if signalement is None:
        raise HTTPException(
            status_code=404,
            detail="Signalement introuvable"
        )

    return signalement