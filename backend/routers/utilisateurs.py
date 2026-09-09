from fastapi import APIRouter, HTTPException

from schemas import UtilisateurCreate, UtilisateurResponse
import crud


router = APIRouter(
    prefix="/api/utilisateurs",
    tags=["Utilisateurs"]
)


@router.post("/", response_model=UtilisateurResponse)
def creer_utilisateur(utilisateur: UtilisateurCreate):

    idUtilisateur = crud.creer_utilisateur(
        utilisateur.idExterne,
        utilisateur.nom,
        utilisateur.motDePasse,
        utilisateur.role
    )

    return {
        "idUtilisateur": idUtilisateur,
        "idExterne": utilisateur.idExterne,
        "nom": utilisateur.nom,
        "motDePasse": utilisateur.motDePasse,
        "role": utilisateur.role
    }


@router.get("/")
def obtenir_utilisateurs():

    return crud.obtenir_utilisateurs()


@router.get("/{idUtilisateur}")
def obtenir_utilisateur(idUtilisateur: int):

    utilisateur = crud.obtenir_utilisateur(idUtilisateur)

    if utilisateur is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    return utilisateur


@router.put("/{idUtilisateur}")
def modifier_utilisateur(
    idUtilisateur: int,
    utilisateur: UtilisateurCreate
):

    modification = crud.modifier_utilisateur(
        idUtilisateur,
        utilisateur.idExterne,
        utilisateur.nom,
        utilisateur.motDePasse,
        utilisateur.role
    )

    if modification == 0:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    return {
        "message": "Utilisateur modifié avec succès"
    }


@router.delete("/{idUtilisateur}")
def supprimer_utilisateur(idUtilisateur: int):

    suppression = crud.supprimer_utilisateur(idUtilisateur)

    if suppression == 0:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    return {
        "message": "Utilisateur supprimé avec succès"
    }