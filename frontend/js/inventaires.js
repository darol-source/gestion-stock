const INVENTAIRES_API_URL = `${API_URL}/api/inventaires`;


// =====================================================
// ELEMENTS
// =====================================================

const inventairesTableBody = document.getElementById("inventairesTableBody");
const inventairesCount = document.getElementById("inventairesCount");
const inventairesMessage = document.getElementById("inventairesMessage");
const btnRafraichirInventaires = document.getElementById("btnRafraichirInventaires");

let inventairesCharges = false;


// =====================================================
// CHARGEMENT DES INVENTAIRES
// =====================================================

async function chargerInventaires() {

    cacherMessageInline(inventairesMessage);

    inventairesTableBody.innerHTML = `
        <tr><td colspan="6" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(INVENTAIRES_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer la liste des inventaires."
            );
        }

        const inventaires = await reponse.json();

        afficherInventaires(inventaires);

    } catch (erreur) {

        console.error("Erreur chargement inventaires :", erreur);

        inventairesTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Impossible de charger les inventaires.
            </td></tr>
        `;

        afficherMessageInline(
            inventairesMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function classeStatutBadge(statut) {

    if (statut === "TERMINE" || statut === "RESOLU") {
        return "status-badge status-done";
    }

    if (statut === "EN_COURS") {
        return "status-badge status-progress";
    }

    return "status-badge status-pending";
}


function afficherInventaires(inventaires) {

    inventairesCount.textContent =
        `${inventaires.length} inventaire(s)`;

    if (inventaires.length === 0) {

        inventairesTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Aucun inventaire enregistré pour le moment.
            </td></tr>
        `;

        return;
    }

    inventairesTableBody.innerHTML = "";

    inventaires.forEach(inventaire => {

        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${inventaire.idInventaire}</td>
            <td>${echapperHtml(String(inventaire.idDepot))}</td>
            <td>${echapperHtml(String(inventaire.idUtilisateur))}</td>
            <td>${echapperHtml(inventaire.dateDebut)}</td>
            <td>${echapperHtml(inventaire.dateFin || "—")}</td>
            <td><span class="${classeStatutBadge(inventaire.statut)}">${echapperHtml(inventaire.statut)}</span></td>
        `;

        inventairesTableBody.appendChild(ligne);
    });
}


// =====================================================
// ACTUALISATION MANUELLE
// =====================================================

btnRafraichirInventaires.addEventListener("click", () => {

    chargerInventaires();
});


// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="inventaires"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!inventairesCharges) {

                inventairesCharges = true;
                chargerInventaires();
            }
        });
    }
);
