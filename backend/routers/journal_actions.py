from fastapi import APIRouter, HTTPException
from database import get_connection


router = APIRouter(
    prefix="/journal-actions",
    tags=["Journal des actions"]
)


# =====================================================
# FONCTION INTERNE
# =====================================================

def enregistrer_action(
    id_utilisateur,
    action,
    description
):
    """
    Enregistre une action dans le journal.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO journal_actions (
                idUtilisateur,
                action,
                details,
                dateAction
            )
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            id_utilisateur,
            action,
            description
        ))

        conn.commit()

    finally:

        conn.close()


# =====================================================
# AFFICHER LE JOURNAL
# =====================================================

@router.get("/")
def lire_journal():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                j.idJournal,
                j.idUtilisateur,
                u.nom,
                j.action,
                j.details,
                j.dateAction
            FROM journal_actions j
            LEFT JOIN utilisateurs u
                ON j.idUtilisateur = u.idUtilisateur
            ORDER BY j.dateAction DESC
        """)

        lignes = cursor.fetchall()

        resultat = []

        for ligne in lignes:

            resultat.append({
                "idJournal": ligne[0],
                "idUtilisateur": ligne[1],
                "nom": ligne[2],
                "action": ligne[3],
                "description": ligne[4],
                "dateAction": ligne[5]
            })

        return resultat


    finally:

        conn.close()


# =====================================================
# JOURNAL D'UN UTILISATEUR
# =====================================================

@router.get("/utilisateur/{id_utilisateur}")
def journal_par_utilisateur(id_utilisateur: int):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                idJournal,
                idUtilisateur,
                action,
                details,
                dateAction
            FROM journal_actions
            WHERE idUtilisateur = ?
            ORDER BY dateAction DESC
        """, (id_utilisateur,))

        lignes = cursor.fetchall()

        resultat = []

        for ligne in lignes:

            resultat.append({
                "idJournal": ligne[0],
                "idUtilisateur": ligne[1],
                "action": ligne[2],
                "description": ligne[3],
                "dateAction": ligne[4]
            })

        return resultat


    finally:

        conn.close()