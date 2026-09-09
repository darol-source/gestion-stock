const OVERVIEW_PRODUITS_URL = `${API_URL}/api/produits/`;
const OVERVIEW_DEPOTS_URL = `${API_URL}/api/depots/`;
const OVERVIEW_UNITES_URL = `${API_URL}/api/unites/`;
const OVERVIEW_INVENTAIRES_URL = `${API_URL}/api/inventaires/`;
const OVERVIEW_SIGNALEMENTS_URL = `${API_URL}/api/signalements/`;
const OVERVIEW_JOURNAL_URL = `${API_URL}/journal-actions/`;


// =====================================================
// ELEMENTS
// =====================================================

const overviewMessage = document.getElementById("overviewMessage");

const statProduits = document.getElementById("statProduits");
const statDepots = document.getElementById("statDepots");
const statUnites = document.getElementById("statUnites");
const statAlertes = document.getElementById("statAlertes");

const repartitionEtats = document.getElementById("repartitionEtats");
const repartitionDepots = document.getElementById("repartitionDepots");
const suiviOperationnel = document.getElementById("suiviOperationnel");
const activiteRecente = document.getElementById("activiteRecente");


// =====================================================
// CHARGEMENT DE LA VUE D'ENSEMBLE
// =====================================================

async function chargerApercu() {

    cacherMessageInline(overviewMessage);

    try {

        const [
            produits,
            depots,
            unites,
            inventaires,
            signalements,
            journal
        ] = await Promise.all([
            fetch(OVERVIEW_PRODUITS_URL).then(r => r.json()),
            fetch(OVERVIEW_DEPOTS_URL).then(r => r.json()),
            fetch(OVERVIEW_UNITES_URL).then(r => r.json()),
            fetch(OVERVIEW_INVENTAIRES_URL).then(r => r.json()),
            fetch(OVERVIEW_SIGNALEMENTS_URL).then(r => r.json()),
            fetch(OVERVIEW_JOURNAL_URL).then(r => r.json())
        ]);

        afficherStatsPrincipales(produits, depots, unites);
        afficherRepartitionEtats(unites);
        afficherRepartitionDepots(unites, depots);
        afficherSuiviOperationnel(inventaires, signalements);
        afficherActiviteRecente(journal);

    } catch (erreur) {

        console.error("Erreur chargement vue d'ensemble :", erreur);

        afficherMessageInline(
            overviewMessage,
            "Impossible de charger certaines statistiques. Vérifie que le backend tourne."
        );
    }
}


// =====================================================
// CARTES PRINCIPALES
// =====================================================

function afficherStatsPrincipales(produits, depots, unites) {

    statProduits.textContent = produits.length;
    statDepots.textContent = depots.length;
    statUnites.textContent = unites.length;

    const alertes = unites.filter(
        u => u.etat === "ABIME" || u.etat === "PERIMEE"
    ).length;

    statAlertes.textContent = alertes;
}


// =====================================================
// REPARTITION PAR ETAT
// =====================================================

function afficherRepartitionEtats(unites) {

    const total = unites.length;

    const compteurs = {
        NEUF: unites.filter(u => u.etat === "NEUF").length,
        ABIME: unites.filter(u => u.etat === "ABIME").length,
        PERIMEE: unites.filter(u => u.etat === "PERIMEE").length
    };

    const libelles = {
        NEUF: "Neuf",
        ABIME: "Abîmé",
        PERIMEE: "Périmé"
    };

    const classes = {
        NEUF: "etat-neuf",
        ABIME: "etat-abime",
        PERIMEE: "etat-perimee"
    };

    if (total === 0) {

        repartitionEtats.innerHTML =
            '<p class="section-placeholder">Aucune unité en stock.</p>';
        return;
    }

    repartitionEtats.innerHTML = "";

    Object.keys(compteurs).forEach(etat => {

        const nombre = compteurs[etat];
        const pourcentage = Math.round((nombre / total) * 100);

        const ligne = document.createElement("div");
        ligne.className = "repartition-row";

        ligne.innerHTML = `
            <div class="repartition-row-labels">
                <span>${libelles[etat]}</span>
                <span>${nombre} (${pourcentage}%)</span>
            </div>
            <div class="repartition-bar-track">
                <div class="repartition-bar-fill ${classes[etat]}" style="width: ${pourcentage}%"></div>
            </div>
        `;

        repartitionEtats.appendChild(ligne);
    });
}


// =====================================================
// REPARTITION PAR DEPOT
// =====================================================

function afficherRepartitionDepots(unites, depots) {

    const total = unites.length;

    if (total === 0 || depots.length === 0) {

        repartitionDepots.innerHTML =
            '<p class="section-placeholder">Aucune donnée disponible.</p>';
        return;
    }

    repartitionDepots.innerHTML = "";

    depots.forEach(depot => {

        const nombre = unites.filter(
            u => u.idDepot === depot.idDepot
        ).length;

        const pourcentage = total > 0
            ? Math.round((nombre / total) * 100)
            : 0;

        const ligne = document.createElement("div");
        ligne.className = "repartition-row";

        ligne.innerHTML = `
            <div class="repartition-row-labels">
                <span>${echapperHtml(depot.nomDepot)}</span>
                <span>${nombre} unité(s)</span>
            </div>
            <div class="repartition-bar-track">
                <div class="repartition-bar-fill" style="width: ${pourcentage}%"></div>
            </div>
        `;

        repartitionDepots.appendChild(ligne);
    });
}


// =====================================================
// SUIVI OPERATIONNEL (inventaires + signalements)
// =====================================================

function afficherSuiviOperationnel(inventaires, signalements) {

    const inventairesEnCours = inventaires.filter(
        i => i.statut === "EN_COURS"
    ).length;

    const signalementsEnAttente = signalements.filter(
        s => s.statut === "EN_ATTENTE"
    ).length;

    const signalementsEnCours = signalements.filter(
        s => s.statut === "EN_COURS"
    ).length;

    suiviOperationnel.innerHTML = `
        <div class="repartition-row">
            <div class="repartition-row-labels">
                <span>Inventaires en cours</span>
                <span>${inventairesEnCours}</span>
            </div>
        </div>
        <div class="repartition-row">
            <div class="repartition-row-labels">
                <span>Signalements en attente</span>
                <span>${signalementsEnAttente}</span>
            </div>
        </div>
        <div class="repartition-row">
            <div class="repartition-row-labels">
                <span>Signalements en cours de traitement</span>
                <span>${signalementsEnCours}</span>
            </div>
        </div>
    `;
}


// =====================================================
// ACTIVITE RECENTE (5 dernières actions du journal)
// =====================================================

function afficherActiviteRecente(journal) {

    if (journal.length === 0) {

        activiteRecente.innerHTML =
            '<p class="section-placeholder">Aucune activité récente.</p>';
        return;
    }

    const dernieresActions = journal.slice(0, 5);

    activiteRecente.innerHTML = "";

    dernieresActions.forEach(entree => {

        const nomUtilisateur =
            entree.nom || `Utilisateur #${entree.idUtilisateur ?? "?"}`;

        const item = document.createElement("div");
        item.className = "activity-item";

        item.innerHTML = `
            <div class="activity-dot"></div>
            <div>
                <div class="activity-text">
                    <strong>${echapperHtml(nomUtilisateur)}</strong>
                    — ${echapperHtml(entree.action)}
                </div>
                <div class="activity-meta">${echapperHtml(entree.dateAction)}</div>
            </div>
        `;

        activiteRecente.appendChild(item);
    });
}


// =====================================================
// CHARGEMENT AU DEMARRAGE ET A CHAQUE RETOUR SUR LA SECTION
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    // Léger délai pour laisser verifierSession() s'exécuter en premier
    setTimeout(() => {

        if (sessionStorage.getItem("utilisateur")) {
            chargerApercu();
        }

    }, 0);
});

document.querySelectorAll('.nav-item[data-section="overview"]').forEach(
    bouton => {

        bouton.addEventListener("click", () => {
            chargerApercu();
        });
    }
);
