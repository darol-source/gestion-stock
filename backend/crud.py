from database import get_connection

# =====================================================
# AUTHENTIFICATION ADMIN
# =====================================================

def compter_admin():
    """
    Retourne le nombre d'administrateurs existants.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM utilisateurs
        WHERE role = 'ADMIN'
    """)

    resultat = cursor.fetchone()[0]

    conn.close()

    return resultat


def creer_premier_admin(nom, email, motDePasse):
    """
    Crée le premier compte administrateur.
    Un seul ADMIN peut exister à la fois.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Vérifier si un ADMIN existe déjà
        cursor.execute("""
            SELECT idUtilisateur
            FROM utilisateurs
            WHERE role = 'ADMIN'
        """)

        admin_existant = cursor.fetchone()

        if admin_existant:
            return None


        # Vérifier si l'email existe déjà
        cursor.execute("""
            SELECT idUtilisateur
            FROM utilisateurs
            WHERE email = ?
        """, (email,))

        email_existant = cursor.fetchone()

        if email_existant:
            raise ValueError(
                "Cette adresse email est déjà utilisée."
            )


        # Identifiant automatique de l'ADMIN
        idExterne = "ADMIN001"


        # Création du compte
        cursor.execute("""
            INSERT INTO utilisateurs (
                idExterne,
                nom,
                email,
                motDePasse,
                role
            )
            VALUES (?, ?, ?, ?, 'ADMIN')
        """, (
            idExterne,
            nom,
            email,
            motDePasse
        ))


        conn.commit()

        id_utilisateur = cursor.lastrowid


        # Récupérer l'administrateur créé
        cursor.execute("""
            SELECT
                idUtilisateur,
                idExterne,
                nom,
                email,
                role
            FROM utilisateurs
            WHERE idUtilisateur = ?
        """, (id_utilisateur,))

        utilisateur = cursor.fetchone()


        return dict(utilisateur)


    finally:
        conn.close()



def connecter_utilisateur(email, motDePasse):
    """
    Vérifie les identifiants d'un utilisateur.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                idUtilisateur,
                idExterne,
                nom,
                email,
                role
            FROM utilisateurs
            WHERE email = ?
            AND motDePasse = ?
        """, (
            email,
            motDePasse
        ))

        utilisateur = cursor.fetchone()


        if utilisateur is None:
            return None


        return dict(utilisateur)


    finally:
        conn.close()
        
        
#employe
def creer_employe(nom, email, motDePasse):
    """
    Crée un compte employé. Plusieurs employés peuvent exister,
    contrairement à l'ADMIN qui est unique.
    """

    import uuid

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Vérifier si l'email existe déjà
        cursor.execute("""
            SELECT idUtilisateur
            FROM utilisateurs
            WHERE email = ?
        """, (email,))

        email_existant = cursor.fetchone()

        if email_existant:
            raise ValueError(
                "Cette adresse email est déjà utilisée."
            )

        idExterne = f"EMP-{uuid.uuid4().hex[:6].upper()}"

        cursor.execute("""
            INSERT INTO utilisateurs (
                idExterne,
                nom,
                email,
                motDePasse,
                role
            )
            VALUES (?, ?, ?, ?, 'EMPLOYE')
        """, (
            idExterne,
            nom,
            email,
            motDePasse
        ))

        connection.commit()

        idUtilisateur = cursor.lastrowid

        cursor.execute("""
            SELECT
                idUtilisateur,
                idExterne,
                nom,
                email,
                role
            FROM utilisateurs
            WHERE idUtilisateur = ?
        """, (idUtilisateur,))

        employe = cursor.fetchone()

        return dict(employe)

    finally:

        connection.close()

#produit
def creer_produit(nomProduit, paysFournisseur, referenceProduit, dateCreation):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO produits (
            nomProduit,
            paysFournisseur,
            referenceProduit,
            dateCreation
        )
        VALUES (?, ?, ?, ?)
    """, (
        nomProduit,
        paysFournisseur,
        referenceProduit,
        dateCreation
    ))

    connection.commit()

    idProduit = cursor.lastrowid

    connection.close()

    return idProduit

def obtenir_produits():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM produits
        ORDER BY idProduit
    """)

    produits = cursor.fetchall()

    connection.close()

    return produits


def obtenir_produit(idProduit):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM produits
        WHERE idProduit = ?
    """, (idProduit,))

    produit = cursor.fetchone()

    connection.close()

    return produit


def modifier_produit(
    idProduit,
    nomProduit,
    paysFournisseur,
    referenceProduit,
    dateCreation
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE produits
        SET
            nomProduit = ?,
            paysFournisseur = ?,
            referenceProduit = ?,
            dateCreation = ?
        WHERE idProduit = ?
    """, (
        nomProduit,
        paysFournisseur,
        referenceProduit,
        dateCreation,
        idProduit
    ))

    connection.commit()

    modification = cursor.rowcount

    connection.close()

    return modification


def supprimer_produit(idProduit):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM produits
        WHERE idProduit = ?
    """, (idProduit,))

    connection.commit()

    suppression = cursor.rowcount

    connection.close()

    return suppression
 
 #depot
def creer_depot(nomDepot, description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO depots (
            nomDepot,
            description
        )
        VALUES (?, ?)
    """, (nomDepot, description))

    connection.commit()

    idDepot = cursor.lastrowid

    connection.close()

    return idDepot


def obtenir_depots():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM depots
        ORDER BY idDepot
    """)

    depots = cursor.fetchall()

    connection.close()

    return depots


def obtenir_depot(idDepot):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM depots
        WHERE idDepot = ?
    """, (idDepot,))

    depot = cursor.fetchone()

    connection.close()

    return depot


def modifier_depot(idDepot, nomDepot, description):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE depots
        SET
            nomDepot = ?,
            description = ?
        WHERE idDepot = ?
    """, (
        nomDepot,
        description,
        idDepot
    ))

    connection.commit()

    modification = cursor.rowcount

    connection.close()

    return modification


def supprimer_depot(idDepot):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM depots
        WHERE idDepot = ?
    """, (idDepot,))

    connection.commit()

    suppression = cursor.rowcount

    connection.close()

    return suppression
 
 
#unite
def creer_unite(idProduit, idDepot, dateEntree, etat):
    import qrcode
    import os

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO unites (
            idProduit,
            idDepot,
            idQrCode,
            dateEntree,
            etat
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        idProduit,
        idDepot,
        "TEMP",
        dateEntree,
        etat
    ))

    idUnite = cursor.lastrowid

    idQrCode = f"QR-{idUnite:06d}"

    cursor.execute("""
        UPDATE unites
        SET idQrCode = ?
        WHERE idUnite = ?
    """, (idQrCode, idUnite))

    connection.commit()

    connection.close()

    dossier_qr = "qrcodes"
    os.makedirs(dossier_qr, exist_ok=True)

    image_qr = qrcode.make(idQrCode)

    chemin_qr = os.path.join(
        dossier_qr,
        f"{idQrCode}.png"
    )

    image_qr.save(chemin_qr)

    return {
        "idUnite": idUnite,
        "idQrCode": idQrCode,
        "cheminQrCode": chemin_qr
    }


def obtenir_unites():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM unites
        ORDER BY idUnite
    """)

    unites = cursor.fetchall()

    connection.close()

    return unites


def obtenir_unite(idUnite):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM unites
        WHERE idUnite = ?
    """, (idUnite,))

    unite = cursor.fetchone()

    connection.close()

    return unite


def obtenir_unite_par_qr(idQrCode):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM unites
        WHERE idQrCode = ?
    """, (idQrCode,))

    unite = cursor.fetchone()

    connection.close()

    return unite

#entree
def creer_entree(idProduit, idDepot, idUtilisateur, quantite, dateEntree):
    import qrcode
    import os

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT idProduit
        FROM produits
        WHERE idProduit = ?
    """, (idProduit,))

    if cursor.fetchone() is None:
        connection.close()
        return {"erreur": "Produit introuvable"}

    cursor.execute("""
        SELECT idDepot
        FROM depots
        WHERE idDepot = ?
    """, (idDepot,))

    if cursor.fetchone() is None:
        connection.close()
        return {"erreur": "Dépôt introuvable"}

    cursor.execute("""
        SELECT idUtilisateur
        FROM utilisateurs
        WHERE idUtilisateur = ?
    """, (idUtilisateur,))

    if cursor.fetchone() is None:
        connection.close()
        return {"erreur": "Utilisateur introuvable"}

    cursor.execute("""
        INSERT INTO entrees (
            idProduit,
            idDepot,
            idUtilisateur,
            quantite,
            dateEntree
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        idProduit,
        idDepot,
        idUtilisateur,
        quantite,
        dateEntree
    ))

    idEntree = cursor.lastrowid

    dossier_qr = "qrcodes"
    os.makedirs(dossier_qr, exist_ok=True)

    unites_creees = []

    for i in range(quantite):

        cursor.execute("""
            INSERT INTO unites (
                idProduit,
                idDepot,
                idQrCode,
                dateEntree,
                etat
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            idProduit,
            idDepot,
            "TEMP",
            dateEntree,
            "NEUF"
        ))

        idUnite = cursor.lastrowid

        idQrCode = f"QR-{idUnite:06d}"

        cursor.execute("""
            UPDATE unites
            SET idQrCode = ?
            WHERE idUnite = ?
        """, (
            idQrCode,
            idUnite
        ))

        image_qr = qrcode.make(idQrCode)

        chemin_qr = os.path.join(
            dossier_qr,
            f"{idQrCode}.png"
        )

        image_qr.save(chemin_qr)

        unites_creees.append({
            "idUnite": idUnite,
            "idQrCode": idQrCode,
            "cheminQrCode": chemin_qr
        })

    connection.commit()
    connection.close()

    return {
        "idEntree": idEntree,
        "quantite": quantite,
        "unites": unites_creees
    }


def obtenir_entrees():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM entrees
        ORDER BY idEntree
    """)

    entrees = cursor.fetchall()

    connection.close()

    return entrees


def obtenir_entree(idEntree):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM entrees
        WHERE idEntree = ?
    """, (idEntree,))

    entree = cursor.fetchone()

    connection.close()

    return entree

#transfere
def creer_transfert(
    idUnite,
    idUtilisateur,
    depotSource,
    depotDestination,
    dateTransfert
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT idUnite, idDepot
        FROM unites
        WHERE idUnite = ?
    """, (idUnite,))

    unite = cursor.fetchone()

    if unite is None:
        connection.close()
        return {"erreur": "Unité introuvable"}

    cursor.execute("""
        SELECT idUtilisateur
        FROM utilisateurs
        WHERE idUtilisateur = ?
    """, (idUtilisateur,))

    utilisateur = cursor.fetchone()

    if utilisateur is None:
        connection.close()
        return {"erreur": "Utilisateur introuvable"}

    cursor.execute("""
        SELECT idDepot
        FROM depots
        WHERE idDepot = ?
    """, (depotSource,))

    source = cursor.fetchone()

    if source is None:
        connection.close()
        return {"erreur": "Dépôt source introuvable"}

    cursor.execute("""
        SELECT idDepot
        FROM depots
        WHERE idDepot = ?
    """, (depotDestination,))

    destination = cursor.fetchone()

    if destination is None:
        connection.close()
        return {"erreur": "Dépôt destination introuvable"}

    # Empêcher source = destination
    if depotSource == depotDestination:
        connection.close()
        return {
            "erreur": "Le dépôt source et le dépôt destination doivent être différents"
        }

    if unite["idDepot"] != depotSource:
        connection.close()
        return {
            "erreur": "Le dépôt source ne correspond pas au dépôt actuel de l'unité"
        }

    cursor.execute("""
        INSERT INTO transferts (
            idUnite,
            idUtilisateur,
            depotSource,
            depotDestination,
            dateTransfert
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        idUnite,
        idUtilisateur,
        depotSource,
        depotDestination,
        dateTransfert
    ))

    idTransfert = cursor.lastrowid

    cursor.execute("""
        UPDATE unites
        SET idDepot = ?
        WHERE idUnite = ?
    """, (
        depotDestination,
        idUnite
    ))

    connection.commit()

    cursor.execute("""
        SELECT *
        FROM transferts
        WHERE idTransfert = ?
    """, (idTransfert,))

    transfert = cursor.fetchone()

    connection.close()

    return transfert


def obtenir_transferts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transferts
        ORDER BY idTransfert
    """)

    transferts = cursor.fetchall()

    connection.close()

    return transferts


def obtenir_transfert(idTransfert):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transferts
        WHERE idTransfert = ?
    """, (idTransfert,))

    transfert = cursor.fetchone()

    connection.close()

    return transfert


def obtenir_transferts_unite(idUnite):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM transferts
        WHERE idUnite = ?
        ORDER BY idTransfert DESC
        LIMIT 2
    """, (idUnite,))

    transferts = cursor.fetchall()

    connection.close()

    return transferts

#Sortie
def creer_sortie(idUnite, idUtilisateur, motif, dateSortie):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT idUnite
        FROM unites
        WHERE idUnite = ?
    """, (idUnite,))

    unite = cursor.fetchone()

    if unite is None:
        connection.close()
        return {
            "erreur": "Unité introuvable ou déjà sortie du stock"
        }

    cursor.execute("""
        SELECT idUtilisateur
        FROM utilisateurs
        WHERE idUtilisateur = ?
    """, (idUtilisateur,))

    utilisateur = cursor.fetchone()

    if utilisateur is None:
        connection.close()
        return {
            "erreur": "Utilisateur introuvable"
        }

    cursor.execute("""
        INSERT INTO sorties (
            idUnite,
            idUtilisateur,
            motif,
            dateSortie
        )
        VALUES (?, ?, ?, ?)
    """, (
        idUnite,
        idUtilisateur,
        motif,
        dateSortie
    ))

    idSortie = cursor.lastrowid

    cursor.execute("""
        DELETE FROM unites
        WHERE idUnite = ?
    """, (idUnite,))

    connection.commit()

    # Récupérer la sortie créée
    cursor.execute("""
        SELECT *
        FROM sorties
        WHERE idSortie = ?
    """, (idSortie,))

    sortie = cursor.fetchone()

    connection.close()

    return sortie


def obtenir_sorties():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM sorties
        ORDER BY idSortie
    """)

    sorties = cursor.fetchall()

    connection.close()

    return sorties


def obtenir_sortie(idSortie):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM sorties
        WHERE idSortie = ?
    """, (idSortie,))

    sortie = cursor.fetchone()

    connection.close()

    return sortie


def obtenir_sorties_unite(idUnite):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM sorties
        WHERE idUnite = ?
        ORDER BY idSortie DESC
    """, (idUnite,))

    sorties = cursor.fetchall()

    connection.close()

    return sorties

#inventaire
def creer_inventaire(idDepot, idUtilisateur, dateDebut):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT idDepot
        FROM depots
        WHERE idDepot = ?
    """, (idDepot,))

    depot = cursor.fetchone()

    if depot is None:
        connection.close()
        return {
            "erreur": "Dépôt introuvable"
        }

    cursor.execute("""
        SELECT idUtilisateur
        FROM utilisateurs
        WHERE idUtilisateur = ?
    """, (idUtilisateur,))

    utilisateur = cursor.fetchone()

    if utilisateur is None:
        connection.close()
        return {
            "erreur": "Utilisateur introuvable"
        }

    cursor.execute("""
        SELECT idInventaire
        FROM inventaires
        WHERE idDepot = ?
        AND idUtilisateur = ?
        AND statut = 'EN_COURS'
    """, (
        idDepot,
        idUtilisateur
    ))

    inventaire_existant = cursor.fetchone()

    if inventaire_existant is not None:
        connection.close()
        return {
            "erreur": "Un inventaire est déjà en cours pour ce dépôt"
        }

    cursor.execute("""
        INSERT INTO inventaires (
            idDepot,
            idUtilisateur,
            dateDebut,
            dateFin,
            statut
        )
        VALUES (?, ?, ?, NULL, 'EN_COURS')
    """, (
        idDepot,
        idUtilisateur,
        dateDebut
    ))

    idInventaire = cursor.lastrowid

    connection.commit()

    cursor.execute("""
        SELECT *
        FROM inventaires
        WHERE idInventaire = ?
    """, (idInventaire,))

    inventaire = cursor.fetchone()

    connection.close()

    return inventaire


def terminer_inventaire(idInventaire, dateFin):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaires
        WHERE idInventaire = ?
    """, (idInventaire,))

    inventaire = cursor.fetchone()

    if inventaire is None:
        connection.close()
        return {
            "erreur": "Inventaire introuvable"
        }

    if inventaire["statut"] != "EN_COURS":
        connection.close()
        return {
            "erreur": "Cet inventaire est déjà terminé"
        }

    # Terminer l'inventaire
    cursor.execute("""
        UPDATE inventaires
        SET dateFin = ?,
            statut = 'TERMINE'
        WHERE idInventaire = ?
    """, (
        dateFin,
        idInventaire
    ))

    connection.commit()

    # Récupérer l'inventaire modifié
    cursor.execute("""
        SELECT *
        FROM inventaires
        WHERE idInventaire = ?
    """, (idInventaire,))

    inventaire = cursor.fetchone()

    connection.close()

    return inventaire


def obtenir_inventaires():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaires
        ORDER BY idInventaire
    """)

    inventaires = cursor.fetchall()

    connection.close()

    return inventaires


def obtenir_inventaire(idInventaire):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaires
        WHERE idInventaire = ?
    """, (idInventaire,))

    inventaire = cursor.fetchone()

    connection.close()

    return inventaire


def obtenir_inventaires_depot(idDepot):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaires
        WHERE idDepot = ?
        ORDER BY idInventaire DESC
    """, (idDepot,))

    inventaires = cursor.fetchall()

    connection.close()

    return inventaires

#inventaire_detail
def creer_inventaire_detail(
    idInventaire,
    idUnite,
    idDepotSysteme,
    idDepotConstate,
    etatSysteme,
    etatConstate,
    emplacementCorrect,
    etatCorrect,
    anomalie
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaires
        WHERE idInventaire = ?
    """, (idInventaire,))

    inventaire = cursor.fetchone()

    if inventaire is None:
        connection.close()
        return {
            "erreur": "Inventaire introuvable"
        }

    if inventaire["statut"] != "EN_COURS":
        connection.close()
        return {
            "erreur": "L'inventaire est déjà terminé"
        }

    cursor.execute("""
        SELECT *
        FROM unites
        WHERE idUnite = ?
    """, (idUnite,))

    unite = cursor.fetchone()

    if unite is None:
        connection.close()
        return {
            "erreur": "Unité introuvable"
        }

    cursor.execute("""
        SELECT idDepot
        FROM depots
        WHERE idDepot = ?
    """, (idDepotSysteme,))

    depot_systeme = cursor.fetchone()

    if depot_systeme is None:
        connection.close()
        return {
            "erreur": "Dépôt système introuvable"
        }

    if idDepotConstate is not None:

        cursor.execute("""
            SELECT idDepot
            FROM depots
            WHERE idDepot = ?
        """, (idDepotConstate,))

        depot_constate = cursor.fetchone()

        if depot_constate is None:
            connection.close()
            return {
                "erreur": "Dépôt constaté introuvable"
            }

    etats_valides = ["NEUF", "ABIME", "PERIMEE"]

    if etatSysteme not in etats_valides:
        connection.close()
        return {
            "erreur": "Etat système invalide"
        }

    if etatConstate is not None and etatConstate not in etats_valides:
        connection.close()
        return {
            "erreur": "Etat constaté invalide"
        }

    if emplacementCorrect not in (0, 1):
        connection.close()
        return {
            "erreur": "emplacementCorrect doit être 0 ou 1"
        }

    if etatCorrect not in (0, 1):
        connection.close()
        return {
            "erreur": "etatCorrect doit être 0 ou 1"
        }

    if unite["idDepot"] != idDepotSysteme:
        connection.close()
        return {
            "erreur": "Le dépôt système ne correspond pas au dépôt actuel de l'unité"
        }

    cursor.execute("""
        INSERT INTO inventaire_details (
            idInventaire,
            idUnite,
            idDepotSysteme,
            idDepotConstate,
            etatSysteme,
            etatConstate,
            emplacementCorrect,
            etatCorrect,
            anomalie
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        idInventaire,
        idUnite,
        idDepotSysteme,
        idDepotConstate,
        etatSysteme,
        etatConstate,
        emplacementCorrect,
        etatCorrect,
        anomalie
    ))

    idDetail = cursor.lastrowid

    connection.commit()

    # Récupérer le détail créé
    cursor.execute("""
        SELECT *
        FROM inventaire_details
        WHERE idDetail = ?
    """, (idDetail,))

    detail = cursor.fetchone()

    connection.close()

    return detail


def obtenir_inventaire_details():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaire_details
        ORDER BY idDetail
    """)

    details = cursor.fetchall()

    connection.close()

    return details


def obtenir_inventaire_detail(idDetail):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaire_details
        WHERE idDetail = ?
    """, (idDetail,))

    detail = cursor.fetchone()

    connection.close()

    return detail


def obtenir_details_inventaire(idInventaire):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaire_details
        WHERE idInventaire = ?
        ORDER BY idDetail
    """, (idInventaire,))

    details = cursor.fetchall()

    connection.close()

    return details


def obtenir_details_unite(idUnite):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM inventaire_details
        WHERE idUnite = ?
        ORDER BY idDetail DESC
    """, (idUnite,))

    details = cursor.fetchall()

    connection.close()

    return details

#signalement
def creer_signalement(
    idInventaire,
    idDetail,
    idUtilisateur,
    typeSignalement,
    description,
    dateSignalement
):
    connection = get_connection()
    cursor = connection.cursor()

    # Vérifier que l'inventaire existe
    cursor.execute("""
        SELECT idInventaire
        FROM inventaires
        WHERE idInventaire = ?
    """, (idInventaire,))

    inventaire = cursor.fetchone()

    if inventaire is None:
        connection.close()
        return {
            "erreur": "Inventaire introuvable"
        }

    # Vérifier que le détail existe
    cursor.execute("""
        SELECT idDetail, idInventaire
        FROM inventaire_details
        WHERE idDetail = ?
    """, (idDetail,))

    detail = cursor.fetchone()

    if detail is None:
        connection.close()
        return {
            "erreur": "Détail d'inventaire introuvable"
        }

    # Vérifier que le détail appartient au bon inventaire
    if detail["idInventaire"] != idInventaire:
        connection.close()
        return {
            "erreur": "Le détail ne correspond pas à cet inventaire"
        }

    # Vérifier que l'utilisateur existe
    cursor.execute("""
        SELECT idUtilisateur
        FROM utilisateurs
        WHERE idUtilisateur = ?
    """, (idUtilisateur,))

    utilisateur = cursor.fetchone()

    if utilisateur is None:
        connection.close()
        return {
            "erreur": "Utilisateur introuvable"
        }

    # Vérifier la description
    if not description.strip():
        connection.close()
        return {
            "erreur": "La description est obligatoire"
        }

    # Créer le signalement
    cursor.execute("""
        INSERT INTO signalements (
            idInventaire,
            idDetail,
            idUtilisateur,
            typeSignalement,
            description,
            statut,
            resolution,
            dateSignalement,
            dateResolution
        )
        VALUES (?, ?, ?, ?, ?, 'EN_ATTENTE', NULL, ?, NULL)
    """, (
        idInventaire,
        idDetail,
        idUtilisateur,
        typeSignalement,
        description,
        dateSignalement
    ))

    idSignalement = cursor.lastrowid

    connection.commit()

    # Récupérer le signalement créé
    cursor.execute("""
        SELECT *
        FROM signalements
        WHERE idSignalement = ?
    """, (idSignalement,))

    signalement = cursor.fetchone()

    connection.close()

    return signalement


def obtenir_signalements():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM signalements
        ORDER BY idSignalement DESC
    """)

    signalements = cursor.fetchall()

    connection.close()

    return signalements


def obtenir_signalement(idSignalement):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM signalements
        WHERE idSignalement = ?
    """, (idSignalement,))

    signalement = cursor.fetchone()

    connection.close()

    return signalement


def obtenir_signalements_inventaire(idInventaire):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM signalements
        WHERE idInventaire = ?
        ORDER BY idSignalement DESC
    """, (idInventaire,))

    signalements = cursor.fetchall()

    connection.close()

    return signalements


def obtenir_signalements_statut(statut):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM signalements
        WHERE statut = ?
        ORDER BY idSignalement DESC
    """, (statut,))

    signalements = cursor.fetchall()

    connection.close()

    return signalements


def modifier_signalement(
    idSignalement,
    statut,
    resolution,
    dateResolution
):
    connection = get_connection()
    cursor = connection.cursor()

    # Vérifier que le signalement existe
    cursor.execute("""
        SELECT *
        FROM signalements
        WHERE idSignalement = ?
    """, (idSignalement,))

    signalement = cursor.fetchone()

    if signalement is None:
        connection.close()
        return {
            "erreur": "Signalement introuvable"
        }

    # Vérifier le statut
    statuts_valides = [
        "EN_ATTENTE",
        "EN_COURS",
        "RESOLU"
    ]

    if statut not in statuts_valides:
        connection.close()
        return {
            "erreur": "Statut invalide"
        }

    # Si résolu, une résolution et une date sont obligatoires
    if statut == "RESOLU":

        if resolution is None or not resolution.strip():
            connection.close()
            return {
                "erreur": "La résolution est obligatoire pour un signalement résolu"
            }

        if dateResolution is None or not dateResolution.strip():
            connection.close()
            return {
                "erreur": "La date de résolution est obligatoire"
            }

    # Mise à jour
    cursor.execute("""
        UPDATE signalements
        SET statut = ?,
            resolution = ?,
            dateResolution = ?
        WHERE idSignalement = ?
    """, (
        statut,
        resolution,
        dateResolution,
        idSignalement
    ))

    connection.commit()

    # Récupérer le signalement modifié
    cursor.execute("""
        SELECT *
        FROM signalements
        WHERE idSignalement = ?
    """, (idSignalement,))

    signalement = cursor.fetchone()

    connection.close()

    return signalement


#journal_action
def creer_journal_action(
    idUtilisateur,
    action,
    dateAction,
    details
):
    connection = get_connection()
    cursor = connection.cursor()

    # Si un utilisateur est fourni,
    # vérifier qu'il existe
    if idUtilisateur is not None:

        cursor.execute("""
            SELECT idUtilisateur
            FROM utilisateurs
            WHERE idUtilisateur = ?
        """, (idUtilisateur,))

        utilisateur = cursor.fetchone()

        if utilisateur is None:
            connection.close()
            return {
                "erreur": "Utilisateur introuvable"
            }

    # Vérifier que l'action n'est pas vide
    if not action.strip():
        connection.close()
        return {
            "erreur": "L'action est obligatoire"
        }

    # Créer l'entrée dans le journal
    cursor.execute("""
        INSERT INTO journal_actions (
            idUtilisateur,
            action,
            dateAction,
            details
        )
        VALUES (?, ?, ?, ?)
    """, (
        idUtilisateur,
        action,
        dateAction,
        details
    ))

    idJournal = cursor.lastrowid

    connection.commit()

    # Récupérer l'action créée
    cursor.execute("""
        SELECT *
        FROM journal_actions
        WHERE idJournal = ?
    """, (idJournal,))

    journal = cursor.fetchone()

    connection.close()

    return journal


def obtenir_journal_actions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM journal_actions
        ORDER BY idJournal DESC
    """)

    journal = cursor.fetchall()

    connection.close()

    return journal


def obtenir_journal_action(idJournal):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM journal_actions
        WHERE idJournal = ?
    """, (idJournal,))

    journal = cursor.fetchone()

    connection.close()

    return journal


def obtenir_journal_utilisateur(idUtilisateur):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM journal_actions
        WHERE idUtilisateur = ?
        ORDER BY idJournal DESC
    """, (idUtilisateur,))

    journal = cursor.fetchall()

    connection.close()

    return journal


def obtenir_journal_action_type(action):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM journal_actions
        WHERE action = ?
        ORDER BY idJournal DESC
    """, (action,))

    journal = cursor.fetchall()

    connection.close()

    return journal