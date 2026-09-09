from fastapi import APIRouter, HTTPException

from schemas import UniteCreate, UniteResponse
import crud


router = APIRouter(
    prefix="/api/unites",
    tags=["Unités"]
)


@router.post("/", response_model=UniteResponse)
def creer_unite(unite: UniteCreate):

    resultat = crud.creer_unite(
        unite.idProduit,
        unite.idDepot,
        unite.dateEntree,
        unite.etat
    )

    return crud.obtenir_unite(
        resultat["idUnite"]
    )


@router.get("/")
def obtenir_unites():

    return crud.obtenir_unites()


@router.get("/{idUnite}")
def obtenir_unite(idUnite: int):

    unite = crud.obtenir_unite(idUnite)

    if unite is None:
        raise HTTPException(
            status_code=404,
            detail="Unité introuvable"
        )

    return unite


@router.get("/qr/{idQrCode}")
def obtenir_unite_par_qr(idQrCode: str):

    unite = crud.obtenir_unite_par_qr(idQrCode)

    if unite is None:
        raise HTTPException(
            status_code=404,
            detail="QR Code introuvable"
        )

    return unite