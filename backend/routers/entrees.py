from fastapi import APIRouter, HTTPException

from schemas import EntreeCreate, EntreeResponse
import crud


router = APIRouter(
    prefix="/api/entrees",
    tags=["Entrées"]
)


@router.post("/")
def creer_entree(entree: EntreeCreate):

    if entree.quantite <= 0:
        raise HTTPException(
            status_code=400,
            detail="La quantité doit être supérieure à zéro"
        )

    resultat = crud.creer_entree(
        entree.idProduit,
        entree.idDepot,
        entree.idUtilisateur,
        entree.quantite,
        entree.dateEntree
    )

    if "erreur" in resultat:
        raise HTTPException(
            status_code=404,
            detail=resultat["erreur"]
        )

    return resultat


@router.get("/")
def obtenir_entrees():

    return crud.obtenir_entrees()


@router.get("/{idEntree}")
def obtenir_entree(idEntree: int):

    entree = crud.obtenir_entree(idEntree)

    if entree is None:
        raise HTTPException(
            status_code=404,
            detail="Entrée introuvable"
        )

    return entree