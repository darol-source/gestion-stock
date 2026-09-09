const JOURNAL_API_URL = `${API_URL}/journal-actions`;


// =====================================================
// ELEMENTS
// =====================================================

const journalTableBody = document.getElementById("journalTableBody");
const journalCount = document.getElementById("journalCount");
const journalMessage = document.getElementById("journalMessage");
const btnRafraichirJournal = document.getElementById("btnRafraichirJournal");

let journalCharge = false;


// =====================================================
// CHARGEMENT DU JOURNAL
// =====================================================

async function chargerJournal() {

    cacherMessageInline(journalMessage);

    journalTableBody.innerHTML = `
        <tr><td colspan="5" class="table-empty">Chargement...</td></tr>
    `;

    try {

        const reponse = await fetch(JOURNAL_API_URL + "/");

        if (!reponse.ok) {

            throw new Error(
                "Impossible de récupérer le journal des actions."
            );
        }

        const journal = await reponse.json();

        afficherJournal(journal);

    } catch (erreur) {

        console.error("Erreur chargement journal :", erreur);

        journalTableBody.innerHTML = `
            <tr><td colspan="5" class="table-empty">
                Impossible de charger le journal des actions.
            </td></tr>
        `;

        afficherMessageInline(
            journalMessage,
            erreur.message || "Erreur de connexion au serveur."
        );
    }
}


function afficherJournal(journal) {

    journalCount.textContent =
        `${journal.length} action(s)`;

    if (journal.length === 0) {

        journalTableBody.innerHTML = `
            <tr><td colspan="5" class="table-empty">
                Aucune action enregistrée pour le moment.
            </td></tr>
        `;

        return;
    }

    journalTableBody.innerHTML = "";

    journal.forEach(entree => {

        const ligne = document.createElement("tr");

        const nomUtilisateur =
            entree.nom || `Utilisateur #${entree.idUtilisateur ?? "?"}`;

        ligne.innerHTML = `
            <td>${entree.idJournal}</td>
            <td>${echapperHtml(nomUtilisateur)}</td>
            <td>${echapperHtml(entree.action)}</td>
            <td>${echapperHtml(entree.description || "—")}</td>
            <td>${echapperHtml(entree.dateAction)}</td>
        `;

        journalTableBody.appendChild(ligne);
    });
}


// =====================================================
// ACTUALISATION MANUELLE
// =====================================================

btnRafraichirJournal.addEventListener("click", () => {

    chargerJournal();
});


// =====================================================
// CHARGEMENT AU PREMIER AFFICHAGE DE LA SECTION
// =====================================================

document.querySelectorAll('.nav-item[data-section="journal"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {

            if (!journalCharge) {

                journalCharge = true;
                chargerJournal();
            }
        });
    }
);
