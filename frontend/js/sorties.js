const SORTIES_API_URL = `${API_URL}/api/sorties`;


// =====================================================
// ELEMENTS
// =====================================================

const sortiesTableBody = document.getElementById("sortiesTableBody");
const sortiesCount = document.getElementById("sortiesCount");
const sortiesMessage = document.getElementById("sortiesMessage");
const btnRafraichirSorties = document.getElementById("btnRafraichirSorties");

let sortiesChargees = false;


// =====================================================
// CHARGEMENT DE L'HISTORIQUE DES SORTIES
// =====================================================

async function chargerSorties() {

    cacherMessageInline(sortiesMessage);

    sortiesTableBody.innerHTML = `
        <tr><td colspan="5" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(SORTIES_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer l'historique des sorties."
            );
        }

        const sorties = await reponse.json();

        afficherSorties(sorties);

    } catch (erreur) {

        console.error("Erreur chargement sorties :", erreur);

        sortiesTableBody.innerHTML = `
            <tr><td colspan="5" class="table-empty">
                Impossible de charger les sorties.
            </td></tr>
        `;

        afficherMessageInline(
            sortiesMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function afficherSorties(sorties) {

    sortiesCount.textContent =
        `${sorties.length} sortie(s)`;

    if (sorties.length === 0) {

        sortiesTableBody.innerHTML = `
            <tr><td colspan="5" class="table-empty">
                Aucune sortie enregistrée pour le moment.
            </td></tr>
        `;

        return;
    }

    sortiesTableBody.innerHTML = "";

    sorties.forEach(sortie => {

        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${sortie.idSortie}</td>
            <td>${echapperHtml(String(sortie.idUnite))}</td>
            <td>${echapperHtml(String(sortie.idUtilisateur))}</td>
            <td>${echapperHtml(sortie.motif || "—")}</td>
            <td>${echapperHtml(sortie.dateSortie)}</td>
        `;

        sortiesTableBody.appendChild(ligne);
    });
}


// =====================================================
// ACTUALISATION MANUELLE
// =====================================================

btnRafraichirSorties.addEventListener("click", () => {

    chargerSorties();
});


// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="sorties"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!sortiesChargees) {

                sortiesChargees = true;
                chargerSorties();
            }
        });
    }
);
