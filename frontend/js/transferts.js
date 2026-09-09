const TRANSFERTS_API_URL = `${API_URL}/api/transferts`;


// =====================================================
// ELEMENTS
// =====================================================

const transfertsTableBody = document.getElementById("transfertsTableBody");
const transfertsCount = document.getElementById("transfertsCount");
const transfertsMessage = document.getElementById("transfertsMessage");
const btnRafraichirTransferts = document.getElementById("btnRafraichirTransferts");

let transfertsCharges = false;


// =====================================================
// CHARGEMENT DE L'HISTORIQUE DES TRANSFERTS
// =====================================================

async function chargerTransferts() {

    cacherMessageInline(transfertsMessage);

    transfertsTableBody.innerHTML = `
        <tr><td colspan="6" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(TRANSFERTS_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer l'historique des transferts."
            );
        }

        const transferts = await reponse.json();

        afficherTransferts(transferts);

    } catch (erreur) {

        console.error("Erreur chargement transferts :", erreur);

        transfertsTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Impossible de charger les transferts.
            </td></tr>
        `;

        afficherMessageInline(
            transfertsMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function afficherTransferts(transferts) {

    transfertsCount.textContent =
        `${transferts.length} transfert(s)`;

    if (transferts.length === 0) {

        transfertsTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Aucun transfert enregistré pour le moment.
            </td></tr>
        `;

        return;
    }

    transfertsTableBody.innerHTML = "";

    transferts.forEach(transfert => {

        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${transfert.idTransfert}</td>
            <td>${echapperHtml(String(transfert.idUnite))}</td>
            <td>${echapperHtml(String(transfert.idUtilisateur))}</td>
            <td>${echapperHtml(String(transfert.depotSource))}</td>
            <td>${echapperHtml(String(transfert.depotDestination))}</td>
            <td>${echapperHtml(transfert.dateTransfert)}</td>
        `;

        transfertsTableBody.appendChild(ligne);
    });
}


// =====================================================
// ACTUALISATION MANUELLE
// =====================================================

btnRafraichirTransferts.addEventListener("click", () => {

    chargerTransferts();
});


// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="transferts"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!transfertsCharges) {

                transfertsCharges = true;
                chargerTransferts();
            }
        });
    }
);
