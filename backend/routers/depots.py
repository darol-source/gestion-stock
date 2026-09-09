from fastapi import APIRouter, HTTPException

from schemas import DepotCreate, DepotResponse
import crud


router = APIRouter(
    prefix="/api/depots",
    tags=["Dépôts"]
)


@router.post("/", response_model=DepotResponse)
def creer_depot(depot: DepotCreate):

    idDepot = crud.creer_depot(
        depot.nomDepot,
        depot.description
    )

    return {
        "idDepot": idDepot,
        "nomDepot": depot.nomDepot,
        "description": depot.description
    }


@router.get("/")
def obtenir_depots():

    return crud.obtenir_depots()


@router.get("/{idDepot}")
def obtenir_depot(idDepot: int):

    depot = crud.obtenir_depot(idDepot)

    if depot is None:
        raise HTTPException(
            status_code=404,
            detail="Dépôt introuvable"
        )

    return depot


@router.put("/{idDepot}")
def modifier_depot(
    idDepot: int,
    depot: DepotCreate
):

    modification = crud.modifier_depot(
        idDepot,
        depot.nomDepot,
        depot.description
    )

    if modification == 0:
        raise HTTPException(
            status_code=404,
            detail="Dépôt introuvable"
        )

    return {
        "message": "Dépôt modifié avec succès"
    }


@router.delete("/{idDepot}")
def supprimer_depot(idDepot: int):

    suppression = crud.supprimer_depot(idDepot)

    if suppression == 0:
        raise HTTPException(
            status_code=404,
            detail="Dépôt introuvable"
        )

    return {
        "message": "Dépôt supprimé avec succès"
    }