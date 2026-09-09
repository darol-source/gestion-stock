from fastapi import APIRouter, HTTPException

from schemas import TransfertCreate, TransfertResponse
import crud


router = APIRouter(
    prefix="/api/transferts",
    tags=["Transferts"]
)


@router.post("/", response_model=TransfertResponse)
def creer_transfert(transfert: TransfertCreate):

    resultat = crud.creer_transfert(
        transfert.idUnite,
        transfert.idUtilisateur,
        transfert.depotSource,
        transfert.depotDestination,
        transfert.dateTransfert
    )

    if isinstance(resultat, dict) and "erreur" in resultat:
        raise HTTPException(
            status_code=400,
            detail=resultat["erreur"]
        )

    return resultat


@router.get("/")
def obtenir_transferts():
    return crud.obtenir_transferts()


# IMPORTANT :
# Cette route doit être placée avant /{idTransfert}
@router.get("/unite/{idUnite}")
def obtenir_transferts_unite(idUnite: int):

    return crud.obtenir_transferts_unite(idUnite)


@router.get("/{idTransfert}")
def obtenir_transfert(idTransfert: int):

    transfert = crud.obtenir_transfert(idTransfert)

    if transfert is None:
        raise HTTPException(
            status_code=404,
            detail="Transfert introuvable"
        )

    return transfert