from pydantic import BaseModel

#Role=Admin
class AdminRegister(BaseModel):
    nom: str
    email: str
    motDePasse: str


class AdminLogin(BaseModel):
    email: str
    motDePasse: str

class EmployeRegister(BaseModel):
    nom: str
    email: str
    motDePasse: str


class EmployeLogin(BaseModel):
    email: str
    motDePasse: str
    
    
#utilisatuer
class UtilisateurCreate(BaseModel):
    idExterne: str
    nom: str
    email: str
    motDePasse: str
    role: str

class UtilisateurResponse(BaseModel):
    idUtilisateur: int
    idExterne: str
    nom: str
    email: str
    motDePasse: str
    role: str
    
#produit
class ProduitCreate(BaseModel):
    nomProduit: str
    paysFournisseur: str
    referenceProduit: str
    dateCreation: str


class ProduitResponse(BaseModel):
    idProduit: int
    nomProduit: str
    paysFournisseur: str
    referenceProduit: str
    dateCreation: str
    
    #depot
    
class DepotCreate(BaseModel):
    nomDepot: str
    description: str | None = None


class DepotResponse(BaseModel):
    idDepot: int
    nomDepot: str
    description: str | None = None
    
#unite
class UniteCreate(BaseModel):
    idProduit: int
    idDepot: int
    dateEntree: str
    etat: str


class UniteResponse(BaseModel):
    idUnite: int
    idProduit: int
    idDepot: int
    idQrCode: str
    dateEntree: str
    etat: str
    
#entrees
class EntreeCreate(BaseModel):
    idProduit: int
    idDepot: int
    idUtilisateur: int
    quantite: int
    dateEntree: str


class EntreeResponse(BaseModel):
    idEntree: int
    idProduit: int
    idDepot: int
    idUtilisateur: int
    quantite: int
    dateEntree: str
    
    
#transfere
class TransfertCreate(BaseModel):
    idUnite: int
    idUtilisateur: int
    depotSource: int
    depotDestination: int
    dateTransfert: str


class TransfertResponse(BaseModel):
    idTransfert: int
    idUnite: int
    idUtilisateur: int
    depotSource: int
    depotDestination: int
    dateTransfert: str
    
#Sortie
class SortieCreate(BaseModel):
    idUnite: int
    idUtilisateur: int
    motif: str | None = None
    dateSortie: str


class SortieResponse(BaseModel):
    idSortie: int
    idUnite: int
    idUtilisateur: int
    motif: str | None = None
    dateSortie: str
    
#inventaire
class InventaireCreate(BaseModel):
    idDepot: int
    idUtilisateur: int
    dateDebut: str


class InventaireTerminer(BaseModel):
    dateFin: str


class InventaireResponse(BaseModel):
    idInventaire: int
    idDepot: int
    idUtilisateur: int
    dateDebut: str
    dateFin: str | None = None
    statut: str
    
    
#inventaire_detailler
class InventaireDetailCreate(BaseModel):
    idInventaire: int
    idUnite: int
    idDepotSysteme: int
    idDepotConstate: int | None = None
    etatSysteme: str
    etatConstate: str | None = None
    emplacementCorrect: int
    etatCorrect: int
    anomalie: str | None = None


class InventaireDetailResponse(BaseModel):
    idDetail: int
    idInventaire: int
    idUnite: int
    idDepotSysteme: int
    idDepotConstate: int | None = None
    etatSysteme: str
    etatConstate: str | None = None
    emplacementCorrect: int
    etatCorrect: int
    anomalie: str | None = None

#signalement
class SignalementCreate(BaseModel):
    idInventaire: int
    idDetail: int
    idUtilisateur: int
    typeSignalement: str
    description: str
    dateSignalement: str


class SignalementUpdate(BaseModel):
    statut: str
    resolution: str | None = None
    dateResolution: str | None = None


class SignalementResponse(BaseModel):
    idSignalement: int
    idInventaire: int
    idDetail: int
    idUtilisateur: int
    typeSignalement: str
    description: str
    statut: str
    resolution: str | None = None
    dateSignalement: str
    dateResolution: str | None = None
    
    
#journal
class JournalActionCreate(BaseModel):
    idUtilisateur: int | None = None
    action: str
    dateAction: str
    details: str | None = None


class JournalActionResponse(BaseModel):
    idJournal: int
    idUtilisateur: int | None = None
    action: str
    dateAction: str
    details: str | None = None