const API_URL = "http://127.0.0.1:8000";


// =====================================================
// ELEMENTS
// =====================================================

// Sections
const loginSection = document.getElementById("loginSection");
const registerSection = document.getElementById("registerSection");

// Boutons de changement
const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");

// Formulaires
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

// Connexion
const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");
const loginMessage = document.getElementById("loginMessage");
const loginButton = document.getElementById("loginButton");

// Création
const registerName = document.getElementById("registerName");
const registerEmail = document.getElementById("registerEmail");
const registerPassword = document.getElementById("registerPassword");
const registerConfirmPassword =
    document.getElementById("registerConfirmPassword");

const registerMessage =
    document.getElementById("registerMessage");

const registerButton =
    document.getElementById("registerButton");


// =====================================================
// CHANGER DE FORMULAIRE
// =====================================================

showRegister.addEventListener("click", () => {

    cacherMessage(loginMessage);

    loginSection.classList.remove("active");

    registerSection.classList.add("active");

    registerName.focus();
});


showLogin.addEventListener("click", () => {

    cacherMessage(registerMessage);

    registerSection.classList.remove("active");

    loginSection.classList.add("active");

    loginEmail.focus();
});


// =====================================================
// AFFICHER / MASQUER MOT DE PASSE
// =====================================================

const passwordButtons =
    document.querySelectorAll(".password-toggle");


passwordButtons.forEach(button => {

    button.addEventListener("click", () => {

        const targetId =
            button.getAttribute("data-target");

        const input =
            document.getElementById(targetId);

        const isPassword =
            input.type === "password";


        input.type =
            isPassword ? "text" : "password";


        button.innerHTML =
            isPassword
                ? '<i class="fa-regular fa-eye-slash"></i>'
                : '<i class="fa-regular fa-eye"></i>';


        button.setAttribute(
            "aria-label",
            isPassword
                ? "Masquer le mot de passe"
                : "Afficher le mot de passe"
        );

    });

});


// =====================================================
// MESSAGE
// =====================================================

function afficherMessage(
    element,
    message,
    type = "error"
) {

    const icon =
        type === "success"
            ? "fa-circle-check"
            : "fa-circle-exclamation";


    element.className =
        `auth-message ${type}`;


    element.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <span>${message}</span>
    `;
}


function cacherMessage(element) {

    element.className = "auth-message";

    element.innerHTML = "";
}


// =====================================================
// CHARGEMENT BOUTON
// =====================================================

function activerChargement(button) {

    button.disabled = true;

    button.classList.add("loading");
}


function desactiverChargement(button) {

    button.disabled = false;

    button.classList.remove("loading");
}


// =====================================================
// CONNEXION ADMIN
// =====================================================

loginForm.addEventListener("submit", async (event) => {

    event.preventDefault();


    cacherMessage(loginMessage);


    const email =
        loginEmail.value.trim();

    const motDePasse =
        loginPassword.value;


    console.log("[LOGIN] Tentative de connexion avec :", email);


    // Vérification frontend

    if (!email || !motDePasse) {

        afficherMessage(
            loginMessage,
            "Veuillez remplir tous les champs."
        );

        return;
    }


    activerChargement(loginButton);


    try {

        const response =
            await fetch(
                `${API_URL}/api/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        motDePasse: motDePasse
                    })
                }
            );


        const data =
            await response.json();


        console.log("[LOGIN] Réponse du serveur :", response.status, data);


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Email ou mot de passe incorrect."
            );
        }

        if (data.role !== "ADMIN") {

            throw new Error(
                "Accès refusé. Cette interface est réservée aux administrateurs."
            );
        }


        afficherMessage(
            loginMessage,
            "Connexion réussie. Redirection...",
            "success"
        );


        // Sauvegarde de l'utilisateur connecté

        sessionStorage.setItem(
            "utilisateur",
            JSON.stringify(data)
        );

        console.log(
            "[LOGIN] Sauvegardé dans sessionStorage :",
            sessionStorage.getItem("utilisateur")
        );

        console.log(
            "[LOGIN] Redirection programmée vers dashboard.html dans 2 secondes..."
        );

        setTimeout(() => {

            console.log("[LOGIN] Redirection en cours maintenant.");

            window.location.href =
                "dashboard.html";

        }, 2000);


    } catch (error) {

        console.error(
            "[LOGIN] Erreur de connexion :",
            error
        );


        afficherMessage(
            loginMessage,
            error.message ||
            "Impossible de contacter le serveur."
        );

    } finally {

        desactiverChargement(loginButton);

    }

});


// =====================================================
// CREATION DU PREMIER ADMIN
// =====================================================

registerForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        cacherMessage(registerMessage);


        const nom =
            registerName.value.trim();

        const email =
            registerEmail.value.trim();

        const motDePasse =
            registerPassword.value;

        const confirmation =
            registerConfirmPassword.value;


        // Vérification des champs

        if (
            !nom ||
            !email ||
            !motDePasse ||
            !confirmation
        ) {

            afficherMessage(
                registerMessage,
                "Veuillez remplir tous les champs."
            );

            return;
        }


        // Vérification du mot de passe

        if (motDePasse.length < 6) {

            afficherMessage(
                registerMessage,
                "Le mot de passe doit contenir au moins 6 caractères."
            );

            return;
        }


        // Vérification confirmation

        if (motDePasse !== confirmation) {

            afficherMessage(
                registerMessage,
                "Les deux mots de passe ne correspondent pas."
            );

            return;
        }


        activerChargement(registerButton);


        try {

            const response =
                await fetch(
                    `${API_URL}/api/auth/register`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            nom: nom,
                            email: email,
                            motDePasse: motDePasse
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Impossible de créer le compte."
                );
            }


            // Succès

            afficherMessage(
                registerMessage,
                "Compte administrateur créé avec succès.",
                "success"
            );

            registerForm.reset();
            setTimeout(() => {

                registerSection.classList.remove(
                    "active"
                );

                loginSection.classList.add(
                    "active"
                );

                loginEmail.value =
                    email;

                loginPassword.focus();


                cacherMessage(
                    registerMessage
                );


            }, 1200);


        } catch (error) {

            console.error(
                "Erreur de création du compte :",
                error
            );


            afficherMessage(
                registerMessage,
                error.message ||
                "Impossible de contacter le serveur."
            );

        } finally {

            desactiverChargement(
                registerButton
            );

        }

    }
);