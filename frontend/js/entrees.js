const ENTREES_API_URL = `${API_URL}/api/entrees`;


// =====================================================
// ELEMENTS
// =====================================================

const entreesTableBody = document.getElementById("entreesTableBody");
const entreesCount = document.getElementById("entreesCount");
const entreesMessage = document.getElementById("entreesMessage");
const btnRafraichirEntrees = document.getElementById("btnRafraichirEntrees");

let entreesChargees = false;


// =====================================================
// CHARGEMENT DE L'HISTORIQUE DES ENTREES
// =====================================================

async function chargerEntrees() {

    cacherMessageInline(entreesMessage);

    entreesTableBody.innerHTML = `
        <tr><td colspan="6" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(ENTREES_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer l'historique des entrées."
            );
        }

        const entrees = await reponse.json();

        afficherEntrees(entrees);

    } catch (erreur) {

        console.error("Erreur chargement entrées :", erreur);

        entreesTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Impossible de charger les entrées.
            </td></tr>
        `;

        afficherMessageInline(
            entreesMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function afficherEntrees(entrees) {

    entreesCount.textContent =
        `${entrees.length} entrée(s)`;

    if (entrees.length === 0) {

        entreesTableBody.innerHTML = `
            <tr><td colspan="6" class="table-empty">
                Aucune entrée enregistrée pour le moment.
            </td></tr>
        `;

        return;
    }

    entreesTableBody.innerHTML = "";

    entrees.forEach(entree => {

        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${entree.idEntree}</td>
            <td>${echapperHtml(String(entree.idProduit))}</td>
            <td>${echapperHtml(String(entree.idDepot))}</td>
            <td>${echapperHtml(String(entree.idUtilisateur))}</td>
            <td>${echapperHtml(String(entree.quantite))}</td>
            <td>${echapperHtml(entree.dateEntree)}</td>
        `;

        entreesTableBody.appendChild(ligne);
    });
}


// =====================================================
// ACTUALISATION MANUELLE
// =====================================================

btnRafraichirEntrees.addEventListener("click", () => {

    chargerEntrees();
});


// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="entrees"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!entreesChargees) {

                entreesChargees = true;
                chargerEntrees();
            }
        });
    }
);
