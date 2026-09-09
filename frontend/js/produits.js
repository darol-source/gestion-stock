const PRODUITS_API_URL = `${API_URL}/api/produits`;


// =====================================================
// ELEMENTS
// =====================================================

const produitsTableBody = document.getElementById("produitsTableBody");
const produitsCount = document.getElementById("produitsCount");
const produitsMessage = document.getElementById("produitsMessage");

const btnAjouterProduit = document.getElementById("btnAjouterProduit");

const produitModalOverlay = document.getElementById("produitModalOverlay");
const produitModalTitle = document.getElementById("produitModalTitle");
const produitModalClose = document.getElementById("produitModalClose");
const produitCancelBtn = document.getElementById("produitCancelBtn");

const produitForm = document.getElementById("produitForm");
const produitFormMessage = document.getElementById("produitFormMessage");
const produitSubmitBtn = document.getElementById("produitSubmitBtn");

const produitIdProduit = document.getElementById("produitIdProduit");
const produitNom = document.getElementById("produitNom");
const produitPays = document.getElementById("produitPays");
const produitReference = document.getElementById("produitReference");
const produitDate = document.getElementById("produitDate");

let produitsCharges = false;


// =====================================================
// MESSAGES
// =====================================================

function afficherMessageInline(element, texte, type = "error") {

    element.textContent = texte;
    element.className = `inline-message visible ${type}`;
}

function cacherMessageInline(element) {

    element.textContent = "";
    element.className = "inline-message";
}


// =====================================================
// CHARGEMENT DE LA LISTE DES PRODUITS
// =====================================================

async function chargerProduits() {

    cacherMessageInline(produitsMessage);

    produitsTableBody.innerHTML = `
        <tr><td colspan="6" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(PRODUITS_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer la liste des produits."
            );
        }

        const produits = await reponse.json();

        afficherProduits(produits);

    } catch (erreur) {

        console.error("Erreur chargement produits :", erreur);

        produitsTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Impossible de charger les produits.
            </td></tr>
        `;

        afficherMessageInline(
            produitsMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function afficherProduits(produits) {

    produitsCount.textContent =
        `${produits.length} produit(s)`;

    if (produits.length === 0) {

        produitsTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Aucun produit enregistré pour le moment.
            </td></tr>
        `;

        return;
    }

    produitsTableBody.innerHTML = "";

    produits.forEach(produit => {

        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${produit.idProduit}</td>
            <td>${echapperHtml(produit.nomProduit)}</td>
            <td>${echapperHtml(produit.paysFournisseur)}</td>
            <td>${echapperHtml(produit.referenceProduit)}</td>
            <td>${echapperHtml(produit.dateCreation)}</td>
            <td>
                <div class="actions-cell">
                    <button class="btn-icon-only btn-edit" data-id="${produit.idProduit}" aria-label="Modifier">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4 20H8L18.5 9.5C19.3 8.7 19.3 7.4 18.5 6.6L17.4 5.5C16.6 4.7 15.3 4.7 14.5 5.5L4 16V20Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
                        </svg>
                    </button>
                    <button class="btn-icon-only danger btn-delete" data-id="${produit.idProduit}" aria-label="Supprimer">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5 7H19" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
                            <path d="M9 7V5C9 4.4 9.4 4 10 4H14C14.6 4 15 4.4 15 5V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
                            <path d="M7 7L7.6 19C7.6 19.6 8.1 20 8.7 20H15.3C15.9 20 16.4 19.6 16.4 19L17 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                </div>
            </td>
        `;

        produitsTableBody.appendChild(ligne);
    });


    // Boutons "modifier"
    document.querySelectorAll(".btn-edit").forEach(bouton => {

        bouton.addEventListener("click", () => {

            const id = bouton.dataset.id;

            const produit = produits.find(
                p => String(p.idProduit) === String(id)
            );

            if (produit) {
                ouvrirModalProduit(produit);
            }
        });
    });


    // Boutons "supprimer"
    document.querySelectorAll(".btn-delete").forEach(bouton => {

        bouton.addEventListener("click", () => {

            const id = bouton.dataset.id;

            demanderConfirmation(
                "Voulez-vous vraiment supprimer ce produit ?",
                () => supprimerProduit(id)
            );
        });
    });
}


function echapperHtml(texte) {

    const div = document.createElement("div");

    div.textContent = texte ?? "";

    return div.innerHTML;
}


// =====================================================
// MODAL PRODUIT (Ajout / Modification)
// =====================================================

function ouvrirModalProduit(produit = null) {

    cacherMessageInline(produitFormMessage);
    produitForm.reset();

    if (produit) {

        produitModalTitle.textContent = "Modifier le produit";
        produitIdProduit.value = produit.idProduit;
        produitNom.value = produit.nomProduit;
        produitPays.value = produit.paysFournisseur;
        produitReference.value = produit.referenceProduit;
        produitDate.value = produit.dateCreation;

    } else {

        produitModalTitle.textContent = "Ajouter un produit";
        produitIdProduit.value = "";

        // Date du jour par défaut
        const aujourdHui = new Date().toISOString().split("T")[0];
        produitDate.value = aujourdHui;
    }

    produitModalOverlay.classList.add("visible");
}


function fermerModalProduit() {

    produitModalOverlay.classList.remove("visible");
}


btnAjouterProduit.addEventListener("click", () => {

    ouvrirModalProduit();
});

produitModalClose.addEventListener("click", fermerModalProduit);
produitCancelBtn.addEventListener("click", fermerModalProduit);

produitModalOverlay.addEventListener("click", (evenement) => {

    if (evenement.target === produitModalOverlay) {
        fermerModalProduit();
    }
});


// =====================================================
// SOUMISSION DU FORMULAIRE (Ajout / Modification)
// =====================================================

produitForm.addEventListener("submit", async (evenement) => {

    evenement.preventDefault();

    cacherMessageInline(produitFormMessage);

    const idExistant = produitIdProduit.value;

    const donnees = {
        nomProduit: produitNom.value.trim(),
        paysFournisseur: produitPays.value.trim(),
        referenceProduit: produitReference.value.trim(),
        dateCreation: produitDate.value
    };

    produitSubmitBtn.disabled = true;

    try {

        let reponse;

        if (idExistant) {

            reponse = await fetch(
                `${PRODUITS_API_URL}/${idExistant}`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(donnees)
                }
            );

        } else {

            reponse = await fetch(
                PRODUITS_API_URL + "/",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(donnees)
                }
            );
        }

        const resultat = await reponse.json();

        if (!reponse.ok) {

            throw new Error(
                resultat.detail ||
                "Impossible d'enregistrer le produit."
            );
        }

        fermerModalProduit();
        chargerProduits();

        afficherToast(
            idExistant
                ? "Produit modifié avec succès."
                : "Produit ajouté avec succès."
        );

    } catch (erreur) {

        console.error("Erreur enregistrement produit :", erreur);

        afficherMessageInline(
            produitFormMessage,
            erreur.message || "Erreur de connexion au serveur."
        );

    } finally {

        produitSubmitBtn.disabled = false;
    }
});


// =====================================================
// SUPPRESSION D'UN PRODUIT
// =====================================================

async function supprimerProduit(idProduit) {
    try {
        const reponse = await fetch(
            `${PRODUITS_API_URL}/${idProduit}`,
            { method: "DELETE" }
        );
        const resultat = await reponse.json();
        if (!reponse.ok) {

            throw new Error(
                resultat.detail ||
                "Impossible de supprimer le produit."
            );
        }
        chargerProduits();
        afficherToast("Produit supprimé avec succès.");
        afficherMessageInline(
            produitsMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
    catch (erreur) {

        console.error("Erreur suppression produit :", erreur);
        afficherMessageInline(
            produitsMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}

// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="produits"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!produitsCharges) {

                produitsCharges = true;
                chargerProduits();
            }
        });
    }
);