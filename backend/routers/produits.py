from fastapi import APIRouter, HTTPException

from schemas import ProduitCreate, ProduitResponse
import crud


router = APIRouter(
    prefix="/api/produits",
    tags=["Produits"]
)


@router.post("/", response_model=ProduitResponse)
def creer_produit(produit: ProduitCreate):

    idProduit = crud.creer_produit(
        produit.nomProduit,
        produit.paysFournisseur,
        produit.referenceProduit,
        produit.dateCreation
    )

    return {
        "idProduit": idProduit,
        "nomProduit": produit.nomProduit,
        "paysFournisseur": produit.paysFournisseur,
        "referenceProduit": produit.referenceProduit,
        "dateCreation": produit.dateCreation
    }


@router.get("/")
def obtenir_produits():

    return crud.obtenir_produits()


@router.get("/{idProduit}")
def obtenir_produit(idProduit: int):

    produit = crud.obtenir_produit(idProduit)

    if produit is None:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )

    return produit


@router.put("/{idProduit}")
def modifier_produit(
    idProduit: int,
    produit: ProduitCreate
):

    modification = crud.modifier_produit(
        idProduit,
        produit.nomProduit,
        produit.paysFournisseur,
        produit.referenceProduit,
        produit.dateCreation
    )

    if modification == 0:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )

    return {
        "message": "Produit modifié avec succès"
    }


@router.delete("/{idProduit}")
def supprimer_produit(idProduit: int):

    suppression = crud.supprimer_produit(idProduit)

    if suppression == 0:
        raise HTTPException(
            status_code=404,
            detail="Produit introuvable"
        )

    return {
        "message": "Produit supprimé avec succès"
    }