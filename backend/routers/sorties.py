from fastapi import APIRouter, HTTPException

from schemas import SortieCreate, SortieResponse
import crud


router = APIRouter(
    prefix="/api/sorties",
    tags=["Sorties"]
)


@router.post("/", response_model=SortieResponse)
def creer_sortie(sortie: SortieCreate):

    resultat = crud.creer_sortie(
        sortie.idUnite,
        sortie.idUtilisateur,
        sortie.motif,
        sortie.dateSortie
    )

    if isinstance(resultat, dict) and "erreur" in resultat:
        raise HTTPException(
            status_code=400,
            detail=resultat["erreur"]
        )

    return resultat


@router.get("/")
def obtenir_sorties():
    return crud.obtenir_sorties()


# IMPORTANT :
# Cette route doit être avant /{idSortie}
@router.get("/unite/{idUnite}")
def obtenir_sorties_unite(idUnite: int):

    return crud.obtenir_sorties_unite(idUnite)


@router.get("/{idSortie}")
def obtenir_sortie(idSortie: int):

    sortie = crud.obtenir_sortie(idSortie)

    if sortie is None:
        raise HTTPException(
            status_code=404,
            detail="Sortie introuvable"
        )

    return sortie