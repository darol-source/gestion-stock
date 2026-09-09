from pydantic import BaseModel


class Produit(BaseModel):
    nomProduit: str
    paysFournisseur: str
    referenceProduit: str
    dateCreation: str