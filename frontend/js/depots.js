const DEPOTS_API_URL = `${API_URL}/api/depots`;


// =====================================================
// ELEMENTS
// =====================================================

const depotsTableBody = document.getElementById("depotsTableBody");
const depotsCount = document.getElementById("depotsCount");
const depotsMessage = document.getElementById("depotsMessage");

const btnAjouterDepot = document.getElementById("btnAjouterDepot");

const depotModalOverlay = document.getElementById("depotModalOverlay");
const depotModalTitle = document.getElementById("depotModalTitle");
const depotModalClose = document.getElementById("depotModalClose");
const depotCancelBtn = document.getElementById("depotCancelBtn");

const depotForm = document.getElementById("depotForm");
const depotFormMessage = document.getElementById("depotFormMessage");
const depotSubmitBtn = document.getElementById("depotSubmitBtn");

const depotIdDepot = document.getElementById("depotIdDepot");
const depotNom = document.getElementById("depotNom");
const depotDescription = document.getElementById("depotDescription");

let depotsCharges = false;


// =====================================================
// CHARGEMENT DE LA LISTE DES DEPOTS
// =====================================================

async function chargerDepots() {

    cacherMessageInline(depotsMessage);

    depotsTableBody.innerHTML = `
        <tr><td colspan="4" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(DEPOTS_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer la liste des dépôts."
            );
        }

        const depots = await reponse.json();

        afficherDepots(depots);

    } catch (erreur) {

        console.error("Erreur chargement dépôts :", erreur);

        depotsTableBody.innerHTML = `
            <tr><td colspan="4" class="table-empty">
                Impossible de charger les dépôts.
            </td></tr>
        `;

        afficherMessageInline(
            depotsMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function afficherDepots(depots) {

    depotsCount.textContent =
        `${depots.length} dépôt(s)`;

    if (depots.length === 0) {

        depotsTableBody.innerHTML = `
            <tr><td colspan="4" class="table-empty">
                Aucun dépôt enregistré pour le moment.
            </td></tr>
        `;

        return;
    }

    depotsTableBody.innerHTML = "";

    depots.forEach(depot => {

        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${depot.idDepot}</td>
            <td>${echapperHtml(depot.nomDepot)}</td>
            <td>${echapperHtml(depot.description || "—")}</td>
            <td>
                <div class="actions-cell">
                    <button class="btn-icon-only btn-edit-depot" data-id="${depot.idDepot}" aria-label="Modifier">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4 20H8L18.5 9.5C19.3 8.7 19.3 7.4 18.5 6.6L17.4 5.5C16.6 4.7 15.3 4.7 14.5 5.5L4 16V20Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
                        </svg>
                    </button>
                    <button class="btn-icon-only danger btn-delete-depot" data-id="${depot.idDepot}" aria-label="Supprimer">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5 7H19" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
                            <path d="M9 7V5C9 4.4 9.4 4 10 4H14C14.6 4 15 4.4 15 5V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
                            <path d="M7 7L7.6 19C7.6 19.6 8.1 20 8.7 20H15.3C15.9 20 16.4 19.6 16.4 19L17 7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                </div>
            </td>
        `;

        depotsTableBody.appendChild(ligne);
    });


    // Boutons "modifier"
    document.querySelectorAll(".btn-edit-depot").forEach(bouton => {

        bouton.addEventListener("click", () => {

            const id = bouton.dataset.id;

            const depot = depots.find(
                d => String(d.idDepot) === String(id)
            );

            if (depot) {
                ouvrirModalDepot(depot);
            }
        });
    });


    // Boutons "supprimer"
    document.querySelectorAll(".btn-delete-depot").forEach(bouton => {

        bouton.addEventListener("click", () => {

            const id = bouton.dataset.id;

            demanderConfirmation(
                "Voulez-vous vraiment supprimer ce dépôt ?",
                () => supprimerDepot(id)
            );
        });
    });
}


// =====================================================
// MODAL DEPOT (Ajout / Modification)
// =====================================================

function ouvrirModalDepot(depot = null) {

    cacherMessageInline(depotFormMessage);
    depotForm.reset();

    if (depot) {

        depotModalTitle.textContent = "Modifier le dépôt";
        depotIdDepot.value = depot.idDepot;
        depotNom.value = depot.nomDepot;
        depotDescription.value = depot.description || "";

    } else {

        depotModalTitle.textContent = "Ajouter un dépôt";
        depotIdDepot.value = "";
    }

    depotModalOverlay.classList.add("visible");
}


function fermerModalDepot() {

    depotModalOverlay.classList.remove("visible");
}


btnAjouterDepot.addEventListener("click", () => {

    ouvrirModalDepot();
});

depotModalClose.addEventListener("click", fermerModalDepot);
depotCancelBtn.addEventListener("click", fermerModalDepot);

depotModalOverlay.addEventListener("click", (evenement) => {

    if (evenement.target === depotModalOverlay) {
        fermerModalDepot();
    }
});


// =====================================================
// SOUMISSION DU FORMULAIRE (Ajout / Modification)
// =====================================================

depotForm.addEventListener("submit", async (evenement) => {

    evenement.preventDefault();

    cacherMessageInline(depotFormMessage);

    const idExistant = depotIdDepot.value;

    const donnees = {
        nomDepot: depotNom.value.trim(),
        description: depotDescription.value.trim() || null
    };

    depotSubmitBtn.disabled = true;

    try {

        let reponse;

        if (idExistant) {

            reponse = await fetch(
                `${DEPOTS_API_URL}/${idExistant}`,
                {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(donnees)
                }
            );

        } else {

            reponse = await fetch(
                DEPOTS_API_URL + "/",
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
                "Impossible d'enregistrer le dépôt."
            );
        }

        fermerModalDepot();
        chargerDepots();

        afficherToast(
            idExistant
                ? "Dépôt modifié avec succès."
                : "Dépôt ajouté avec succès."
        );

    } catch (erreur) {

        console.error("Erreur enregistrement dépôt :", erreur);

        afficherMessageInline(
            depotFormMessage,
            erreur.message || "Erreur de connexion au serveur."
        );

    } finally {

        depotSubmitBtn.disabled = false;
    }
});


// =====================================================
// SUPPRESSION D'UN DEPOT
// =====================================================

async function supprimerDepot(idDepot) {

    try {

        const reponse = await fetch(
            `${DEPOTS_API_URL}/${idDepot}`,
            { method: "DELETE" }
        );

        const resultat = await reponse.json();

        if (!reponse.ok) {

            throw new Error(
                resultat.detail ||
                "Impossible de supprimer le dépôt."
            );
        }

        chargerDepots();

        afficherToast("Dépôt supprimé avec succès.");

    } catch (erreur) {

        console.error("Erreur suppression dépôt :", erreur);

        afficherMessageInline(
            depotsMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="depots"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!depotsCharges) {

                depotsCharges = true;
                chargerDepots();
            }
        });
    }
);