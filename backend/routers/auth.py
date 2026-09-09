from fastapi import APIRouter, HTTPException
from schemas import AdminRegister, AdminLogin, EmployeRegister, EmployeLogin

from crud import (
    creer_premier_admin,
    connecter_utilisateur,
    creer_employe
)

from routers.journal_actions import enregistrer_action


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentification"]
)

@router.post("/register")
def register_admin(admin: AdminRegister):

    try:

        nouvel_admin = creer_premier_admin(
            admin.nom,
            admin.email,
            admin.motDePasse
        )



        if nouvel_admin is None:

            raise HTTPException(
                status_code=403,
                detail=(
                    "Un compte administrateur existe déjà. "
                    "La création d'un autre administrateur est interdite."
                )
            )


        enregistrer_action(
            nouvel_admin["idUtilisateur"],
            "CREATION_ADMIN",
            (
                "Création du premier compte administrateur : "
                f"{nouvel_admin['email']}"
            )
        )


        return {
            "message": (
                "Compte administrateur créé avec succès."
            ),
            "utilisateur": nouvel_admin
        }


    except ValueError as erreur:

        raise HTTPException(
            status_code=400,
            detail=str(erreur)
        )

@router.post("/login")
def login_admin(donnees: AdminLogin):

    utilisateur = connecter_utilisateur(
        donnees.email,
        donnees.motDePasse
    )


    # Utilisateur introuvable
    if utilisateur is None:

        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect."
        )


    # Cette interface est réservée à l'ADMIN
    if utilisateur["role"] != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail=(
                "Accès refusé. "
                "Cette interface est réservée aux administrateurs."
            )
        )


    # Journalisation de connexion
    enregistrer_action(
        utilisateur["idUtilisateur"],
        "CONNEXION_ADMIN",
        "Connexion réussie à l'espace administrateur."
    )


    return {
        "message": "Connexion réussie.",
        "idUtilisateur": utilisateur["idUtilisateur"],
        "nom": utilisateur["nom"],
        "email": utilisateur["email"],
        "role": utilisateur["role"]
    }


# =====================================================
# AUTHENTIFICATION EMPLOYE (app Android)
# =====================================================

@router.post("/employe/register")
def register_employe(employe: EmployeRegister):

    try:

        nouvel_employe = creer_employe(
            employe.nom,
            employe.email,
            employe.motDePasse
        )

        enregistrer_action(
            nouvel_employe["idUtilisateur"],
            "CREATION_EMPLOYE",
            (
                "Création du compte employé : "
                f"{nouvel_employe['email']}"
            )
        )

        return {
            "message": "Compte employé créé avec succès.",
            "utilisateur": nouvel_employe
        }

    except ValueError as erreur:

        raise HTTPException(
            status_code=400,
            detail=str(erreur)
        )


@router.post("/employe/login")
def login_employe(donnees: EmployeLogin):

    utilisateur = connecter_utilisateur(
        donnees.email,
        donnees.motDePasse
    )

    if utilisateur is None:

        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect."
        )

    if utilisateur["role"] != "EMPLOYE":

        raise HTTPException(
            status_code=403,
            detail=(
                "Accès refusé. "
                "Cette interface est réservée aux employés."
            )
        )

    enregistrer_action(
        utilisateur["idUtilisateur"],
        "CONNEXION_EMPLOYE",
        "Connexion réussie à l'espace employé."
    )

    return {
        "message": "Connexion réussie.",
        "idUtilisateur": utilisateur["idUtilisateur"],
        "nom": utilisateur["nom"],
        "email": utilisateur["email"],
        "role": utilisateur["role"]
    }
