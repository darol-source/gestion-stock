const API_URL = "http://127.0.0.1:8000";


// =====================================================
// ELEMENTS
// =====================================================

const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const sidebarOverlay = document.getElementById("sidebarOverlay");

const navItems = document.querySelectorAll(".nav-item[data-section]");
const contentSections = document.querySelectorAll(".content-section");

const pageTitle = document.getElementById("pageTitle");
const userName = document.getElementById("userName");
const userAvatar = document.getElementById("userAvatar");

const logoutButton = document.getElementById("logoutButton");


// Titres affichés dans la topbar pour chaque section

const titresSections = {
    overview: "Vue d'ensemble",
    produits: "Produits",
    depots: "Dépôts",
    entrees: "Entrées",
    sorties: "Sorties",
    transferts: "Transferts",
    inventaires: "Inventaires",
    signalements: "Signalements",
    journal: "Journal des actions"
};


// =====================================================
// VERIFICATION DE SESSION
// =====================================================

function verifierSession() {

    console.log("[DASHBOARD] Vérification de la session...");

    const donnees = sessionStorage.getItem("utilisateur");

    console.log("[DASHBOARD] Contenu brut de sessionStorage.utilisateur :", donnees);

    if (!donnees) {

        console.warn("[DASHBOARD] Aucune donnée trouvée, redirection vers login.html");
        window.location.href = "login.html";
        return null;
    }

    let utilisateur;

    try {

        utilisateur = JSON.parse(donnees);

    } catch (error) {

        console.error("[DASHBOARD] Erreur de parsing JSON :", error);
        sessionStorage.removeItem("utilisateur");
        window.location.href = "login.html";
        return null;
    }

    console.log("[DASHBOARD] Utilisateur parsé :", utilisateur);

    if (!utilisateur || utilisateur.role !== "ADMIN") {

        console.warn(
            "[DASHBOARD] Rôle invalide ou utilisateur manquant. Rôle reçu :",
            utilisateur ? utilisateur.role : "aucun utilisateur"
        );
        sessionStorage.removeItem("utilisateur");
        window.location.href = "login.html";
        return null;
    }

    console.log("[DASHBOARD] Session valide, accès autorisé.");

    return utilisateur;
}


function afficherUtilisateur(utilisateur) {

    userName.textContent = utilisateur.nom || "Administrateur";

    const initiales = (utilisateur.nom || "AD")
        .trim()
        .split(/\s+/)
        .map(mot => mot[0])
        .slice(0, 2)
        .join("")
        .toUpperCase();

    userAvatar.textContent = initiales || "AD";
}


// =====================================================
// NAVIGATION ENTRE SECTIONS
// =====================================================

function afficherSection(nomSection) {

    navItems.forEach(item => {

        item.classList.toggle(
            "active",
            item.dataset.section === nomSection
        );
    });

    contentSections.forEach(section => {

        section.classList.toggle(
            "active",
            section.id === `section-${nomSection}`
        );
    });

    pageTitle.textContent =
        titresSections[nomSection] || "";

    fermerMenuMobile();
}


navItems.forEach(item => {

    item.addEventListener("click", () => {

        afficherSection(item.dataset.section);
    });
});


// =====================================================
// SIDEBAR : REDUIRE / DEPLIER (desktop)
// =====================================================

sidebarToggle.addEventListener("click", () => {

    sidebar.classList.toggle("collapsed");
});


// =====================================================
// SIDEBAR : MENU MOBILE
// =====================================================

function ouvrirMenuMobile() {

    sidebar.classList.add("mobile-open");
    sidebarOverlay.classList.add("visible");
}

function fermerMenuMobile() {

    sidebar.classList.remove("mobile-open");
    sidebarOverlay.classList.remove("visible");
}

mobileMenuBtn.addEventListener("click", ouvrirMenuMobile);
sidebarOverlay.addEventListener("click", fermerMenuMobile);


// =====================================================
// DECONNEXION
// =====================================================

logoutButton.addEventListener("click", () => {

    sessionStorage.removeItem("utilisateur");
    window.location.href = "login.html";
});


// =====================================================
// NOTIFICATIONS (TOAST)
// =====================================================

const toastContainer = document.getElementById("toastContainer");

function afficherToast(message, type = "success") {

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    const icone = type === "success"
        ? `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
               <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/>
               <path d="M8 12.5L10.5 15L16 9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
           </svg>`
        : `<svg class="toast-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
               <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/>
               <path d="M12 8V13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
               <path d="M12 16V16.01" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
           </svg>`;

    toast.innerHTML = `
        ${icone}
        <span class="toast-text"></span>
    `;

    toast.querySelector(".toast-text").textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("closing");

        setTimeout(() => {
            toast.remove();
        }, 200);

    }, 3000);
}


// =====================================================
// CONFIRMATION GENERIQUE (partagée entre les sections)
// =====================================================

const confirmModalOverlay = document.getElementById("confirmModalOverlay");
const confirmModalText = document.getElementById("confirmModalText");
const confirmModalClose = document.getElementById("confirmModalClose");
const confirmCancelBtn = document.getElementById("confirmCancelBtn");
const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

let actionConfirmee = null;

function demanderConfirmation(texte, callback) {

    confirmModalText.textContent = texte;
    actionConfirmee = callback;
    confirmModalOverlay.classList.add("visible");
}

function fermerModalConfirmation() {

    confirmModalOverlay.classList.remove("visible");
    actionConfirmee = null;
}

confirmModalClose.addEventListener("click", fermerModalConfirmation);
confirmCancelBtn.addEventListener("click", fermerModalConfirmation);

confirmModalOverlay.addEventListener("click", (evenement) => {

    if (evenement.target === confirmModalOverlay) {
        fermerModalConfirmation();
    }
});

confirmDeleteBtn.addEventListener("click", async () => {

    if (!actionConfirmee) {
        return;
    }

    confirmDeleteBtn.disabled = true;

    try {

        await actionConfirmee();

    } finally {

        confirmDeleteBtn.disabled = false;
        fermerModalConfirmation();
    }
});


// =====================================================
// INITIALISATION
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    const utilisateur = verifierSession();

    if (!utilisateur) {
        return;
    }

    afficherUtilisateur(utilisateur);
    afficherSection("overview");
});