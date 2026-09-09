const SIGNALEMENTS_API_URL = `${API_URL}/api/signalements`;


// =====================================================
// ELEMENTS
// =====================================================

const signalementsTableBody = document.getElementById("signalementsTableBody");
const signalementsCount = document.getElementById("signalementsCount");
const signalementsMessage = document.getElementById("signalementsMessage");
const btnRafraichirSignalements = document.getElementById("btnRafraichirSignalements");

let signalementsCharges = false;


// =====================================================
// CHARGEMENT DES SIGNALEMENTS
// =====================================================

async function chargerSignalements() {

    cacherMessageInline(signalementsMessage);

    signalementsTableBody.innerHTML = `
        <tr><td colspan="6" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(SIGNALEMENTS_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer la liste des signalements."
            );
        }

        const signalements = await reponse.json();

        afficherSignalements(signalements);

    } catch (erreur) {

        console.error("Erreur chargement signalements :", erreur);

        signalementsTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Impossible de charger les signalements.
            </td></tr>
        `;

        afficherMessageInline(
            signalementsMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function afficherSignalements(signalements) {

    signalementsCount.textContent =
        `${signalements.length} signalement(s)`;

    if (signalements.length === 0) {

        signalementsTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Aucun signalement enregistré pour le moment.
            </td></tr>
        `;

        return;
    }

    signalementsTableBody.innerHTML = "";

    signalements.forEach(signalement => {

        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${signalement.idSignalement}</td>
            <td>${echapperHtml(String(signalement.idInventaire))}</td>
            <td>${echapperHtml(signalement.typeSignalement)}</td>
            <td>${echapperHtml(signalement.description)}</td>
            <td><span class="${classeStatutBadge(signalement.statut)}">${echapperHtml(signalement.statut)}</span></td>
            <td>${echapperHtml(signalement.dateSignalement)}</td>
        `;

        signalementsTableBody.appendChild(ligne);
    });
}


// =====================================================
// ACTUALISATION MANUELLE
// =====================================================

btnRafraichirSignalements.addEventListener("click", () => {

    chargerSignalements();
});


// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="signalements"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!signalementsCharges) {

                signalementsCharges = true;
                chargerSignalements();
            }
        });
    }
);
