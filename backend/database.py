import sqlite3


DATABASE = "stock.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            idUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
            idExterne TEXT NOT NULL UNIQUE,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            motDePasse TEXT NOT NULL,
            role TEXT NOT NULL
                CHECK (role IN ('ADMIN', 'EMPLOYE'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            idProduit INTEGER PRIMARY KEY AUTOINCREMENT,
            nomProduit TEXT NOT NULL,
            paysFournisseur TEXT NOT NULL,
            referenceProduit TEXT NOT NULL UNIQUE,
            dateCreation TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS depots (
            idDepot INTEGER PRIMARY KEY AUTOINCREMENT,
            nomDepot TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unites (
            idUnite INTEGER PRIMARY KEY AUTOINCREMENT,

            idProduit INTEGER NOT NULL,

            idDepot INTEGER NOT NULL,

            idQrCode TEXT NOT NULL UNIQUE,

            dateEntree TEXT NOT NULL,

            etat TEXT NOT NULL
                CHECK (etat IN ('NEUF', 'ABIME', 'PERIMEE')),

            FOREIGN KEY (idProduit)
                REFERENCES produits(idProduit)
                ON DELETE CASCADE,

            FOREIGN KEY (idDepot)
                REFERENCES depots(idDepot)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entrees (
            idEntree INTEGER PRIMARY KEY AUTOINCREMENT,

            idProduit INTEGER NOT NULL,

            idDepot INTEGER NOT NULL,

            idUtilisateur INTEGER NOT NULL,

            quantite INTEGER NOT NULL
                CHECK (quantite > 0),

            dateEntree TEXT NOT NULL,

            FOREIGN KEY (idProduit)
                REFERENCES produits(idProduit),

            FOREIGN KEY (idDepot)
                REFERENCES depots(idDepot),

            FOREIGN KEY (idUtilisateur)
                REFERENCES utilisateurs(idUtilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sorties (
            idSortie INTEGER PRIMARY KEY AUTOINCREMENT,

            idUnite INTEGER NOT NULL,

            idUtilisateur INTEGER NOT NULL,

            motif TEXT,

            dateSortie TEXT NOT NULL,

            FOREIGN KEY (idUtilisateur)
                REFERENCES utilisateurs(idUtilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transferts (
            idTransfert INTEGER PRIMARY KEY AUTOINCREMENT,

            idUnite INTEGER NOT NULL,

            idUtilisateur INTEGER NOT NULL,

            depotSource INTEGER NOT NULL,

            depotDestination INTEGER NOT NULL,

            dateTransfert TEXT NOT NULL,

            FOREIGN KEY (idUtilisateur)
                REFERENCES utilisateurs(idUtilisateur),

            FOREIGN KEY (depotSource)
                REFERENCES depots(idDepot),

            FOREIGN KEY (depotDestination)
                REFERENCES depots(idDepot)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventaires (
            idInventaire INTEGER PRIMARY KEY AUTOINCREMENT,

            idDepot INTEGER NOT NULL,

            idUtilisateur INTEGER NOT NULL,

            dateDebut TEXT NOT NULL,

            dateFin TEXT,

            statut TEXT NOT NULL
                CHECK (statut IN ('EN_COURS', 'TERMINE')),

            FOREIGN KEY (idDepot)
                REFERENCES depots(idDepot),

            FOREIGN KEY (idUtilisateur)
                REFERENCES utilisateurs(idUtilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventaire_details (
            idDetail INTEGER PRIMARY KEY AUTOINCREMENT,

            idInventaire INTEGER NOT NULL,

            idUnite INTEGER NOT NULL,

            idDepotSysteme INTEGER NOT NULL,

            idDepotConstate INTEGER,

            etatSysteme TEXT NOT NULL
                CHECK (etatSysteme IN ('NEUF', 'ABIME', 'PERIMEE')),

            etatConstate TEXT
                CHECK (
                    etatConstate IS NULL
                    OR etatConstate IN ('NEUF', 'ABIME', 'PERIMEE')
                ),

            emplacementCorrect INTEGER NOT NULL
                CHECK (emplacementCorrect IN (0, 1)),

            etatCorrect INTEGER NOT NULL
                CHECK (etatCorrect IN (0, 1)),

            anomalie TEXT,

            FOREIGN KEY (idInventaire)
                REFERENCES inventaires(idInventaire)
                ON DELETE CASCADE,

            FOREIGN KEY (idDepotSysteme)
                REFERENCES depots(idDepot),

            FOREIGN KEY (idDepotConstate)
                REFERENCES depots(idDepot)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signalements (
            idSignalement INTEGER PRIMARY KEY AUTOINCREMENT,

            idInventaire INTEGER NOT NULL,

            idDetail INTEGER NOT NULL,

            idUtilisateur INTEGER NOT NULL,

            typeSignalement TEXT NOT NULL,

            description TEXT NOT NULL,

            statut TEXT NOT NULL
                CHECK (
                    statut IN ('EN_ATTENTE', 'EN_COURS', 'RESOLU')
                ),

            resolution TEXT,

            dateSignalement TEXT NOT NULL,

            dateResolution TEXT,

            FOREIGN KEY (idInventaire)
                REFERENCES inventaires(idInventaire)
                ON DELETE CASCADE,

            FOREIGN KEY (idDetail)
                REFERENCES inventaire_details(idDetail)
                ON DELETE CASCADE,

            FOREIGN KEY (idUtilisateur)
                REFERENCES utilisateurs(idUtilisateur)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal_actions (
            idJournal INTEGER PRIMARY KEY AUTOINCREMENT,

            idUtilisateur INTEGER,

            action TEXT NOT NULL,

            dateAction TEXT NOT NULL,

            details TEXT,

            FOREIGN KEY (idUtilisateur)
                REFERENCES utilisateurs(idUtilisateur)
        )
    """)

    connection.commit()
    connection.close()

    print("Base de données créée avec succès.")


if __name__ == "__main__":
    create_database()