document.addEventListener('DOMContentLoaded', () => {
    const questionTextElement = document.getElementById('challenge-question-text');
    const elementImageDisplay = document.getElementById('element-image-display');
    const optionsAreaElement = document.getElementById('options-area');
    const feedbackTextElement = document.getElementById('feedback-text');
    const scoreElement = document.getElementById('score');
    const levelElement = document.getElementById('level');
    const assistantImageElement = document.getElementById('assistant-image');
    const assistantFactElement = document.getElementById('assistant-fact');
    const progressBarFillElement = document.getElementById('progress-bar-fill');

    let score = 0;
    let level = 1;
    let questionsPerLevel = 6; // 2 de chaque type par niveau
    let questionsAnsweredInLevel = 0;
    let currentChallengeData = {};
    let isWaitingForNext = false;

    // DomainSpecificContent: ElementDatabase
    const elementDatabase = {
        1: [ // Niveau 1: Éléments très courants
            { nom: "Hydrogène", symbole: "H", utilite: "Principal composant de l'eau et du Soleil.", image: "images/elements/hydrogene.png", distracteursNom: ["Hélium", "Oxygène"], distracteursSymbole: ["He", "O"], distracteursUtilite: ["Fait voler les ballons", "Essentiel pour respirer"] },
            { nom: "Oxygène", symbole: "O", utilite: "Essentiel pour respirer et pour le feu.", image: "images/elements/oxygene.png", distracteursNom: ["Azote", "Carbone"], distracteursSymbole: ["N", "C"], distracteursUtilite: ["Principal gaz de l'air", "Base de la vie"] },
            { nom: "Carbone", symbole: "C", utilite: "Base de tous les êtres vivants (diamant, crayon).", image: "images/elements/carbone.png", distracteursNom: ["Calcium", "Chlore"], distracteursSymbole: ["Ca", "Cl"], distracteursUtilite: ["Pour des os solides", "Désinfectant (piscine)"] }
        ],
        2: [ // Niveau 2: Autres éléments importants
            { nom: "Fer", symbole: "Fe", utilite: "Utilisé pour fabriquer l'acier (voitures, bâtiments).", image: "images/elements/fer.png", distracteursNom: ["Fluor", "Cuivre"], distracteursSymbole: ["F", "Cu"], distracteursUtilite: ["Dans le dentifrice", "Pour les fils électriques"] },
            { nom: "Aluminium", symbole: "Al", utilite: "Léger, utilisé pour les canettes et les avions.", image: "images/elements/aluminium.png", distracteursNom: ["Argent", "Or"], distracteursSymbole: ["Ag", "Au"], distracteursUtilite: ["Pour les bijoux précieux", "Très précieux, pour les trésors"] },
            { nom: "Sodium", symbole: "Na", utilite: "Un des composants du sel de table.", image: "images/elements/sodium.png", distracteursNom: ["Soufre", "Silicium"], distracteursSymbole: ["S", "Si"], distracteursUtilite: ["Sent mauvais (oeuf pourri)", "Pour les puces électroniques"] }
        ],
        3: [ // Niveau 3: Éléments un peu plus spécifiques
            { nom: "Hélium", symbole: "He", utilite: "Gaz léger qui fait voler les ballons.", image: "images/elements/helium.png", distracteursNom: ["Hydrogène", "Néon"], distracteursSymbole: ["H", "Ne"], distracteursUtilite: ["Composant de l'eau", "Pour les enseignes lumineuses"] },
            { nom: "Chlore", symbole: "Cl", utilite: "Désinfectant, utilisé dans l'eau de Javel et les piscines.", image: "images/elements/chlore.png", distracteursNom: ["Carbone", "Calcium"], distracteursSymbole: ["C", "Ca"], distracteursUtilite: ["Base de la vie", "Pour des os solides"] },
            { nom: "Calcium", symbole: "Ca", utilite: "Important pour des os et des dents solides.", image: "images/elements/calcium.png", distracteursNom: ["Carbone", "Cuivre"], distracteursSymbole: ["C", "Cu"], distracteursUtilite: ["Base de la vie", "Pour les fils électriques"] }
        ]
    };

    const assistantScientists = [
        { name: "Prof. Atomis", image: "images/assistant_chimiste_1.png", fact: "Chaque atome a une histoire unique !" },
        { name: "Dr. Molecula", image: "images/assistant_chimiste_2.png", fact: "Les éléments se combinent pour former tout ce qui nous entoure !" },
        { name: "Chercheuse Elara", image: "images/assistant_chimiste_3.png", fact: "La table périodique est comme une carte au trésor des éléments !" }
    ];

    function getRandomElement(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    // ExerciseGenerator: générerDéfiAtomique
    function generateChallenge() {
        if (isWaitingForNext) return;
        isWaitingForNext = true;

        const currentLevelElements = elementDatabase[level] || elementDatabase[Object.keys(elementDatabase).pop()];
        const selectedElement = getRandomElement(currentLevelElements);

        // AtomDifficultyManager (implicite): choix des distracteurs
        // QCMElementType: détermine le type de question
        const challengeType = Math.floor(Math.random() * 3); // 0: Symbole->Nom, 1: Nom->Symbole, 2: Élément->Utilité

        let question = "";
        let correctAnswer = "";
        let options = [];

        elementImageDisplay.style.display = 'none'; // Cacher par défaut
        if (selectedElement.image) {
            elementImageDisplay.src = selectedElement.image;
            // Afficher l'image pour certains types de questions si pertinent
        }


        switch (challengeType) {
            case 0: // Symbole -> Nom
                question = `Quel est le nom de l'élément de symbole "${selectedElement.symbole}" ?`;
                correctAnswer = selectedElement.nom;
                options = shuffleArray([correctAnswer, ...selectedElement.distracteursNom.slice(0, 2)]);
                if (selectedElement.image) elementImageDisplay.style.display = 'block'; // Montrer l'image pour aider
                break;
            case 1: // Nom -> Symbole
                question = `Quel est le symbole chimique de l'élément "${selectedElement.nom}" ?`;
                correctAnswer = selectedElement.symbole;
                options = shuffleArray([correctAnswer, ...selectedElement.distracteursSymbole.slice(0, 2)]);
                if (selectedElement.image) elementImageDisplay.style.display = 'block';
                break;
            case 2: // Élément -> Utilité
                question = `Quelle est une utilisation principale de l'élément "${selectedElement.nom}" (${selectedElement.symbole}) ?`;
                correctAnswer = selectedElement.utilite;
                options = shuffleArray([correctAnswer, ...selectedElement.distracteursUtilite.slice(0, 2)]);
                // Pas d'image ici pour ne pas donner trop d'indices sur l'utilité
                break;
        }

        currentChallengeData = { question, options, correctAnswer }; // PlayableExercise

        questionTextElement.textContent = currentChallengeData.question;
        optionsAreaElement.innerHTML = '';
        currentChallengeData.options.forEach(optText => {
            const button = document.createElement('button');
            button.classList.add('option-button');
            button.textContent = optText;
            button.addEventListener('click', () => {
                if (!isWaitingForNext) {
                    checkAnswer(optText);
                }
            });
            optionsAreaElement.appendChild(button);
        });

        feedbackTextElement.textContent = '';
        feedbackTextElement.className = '';
        updateAssistantDisplay();
        isWaitingForNext = false;
    }

    function updateAssistantDisplay() {
        const assistant = assistantScientists[level % assistantScientists.length];
        assistantImageElement.src = assistant.image;
        assistantImageElement.alt = assistant.name;
        assistantFactElement.textContent = `${assistant.name} dit : "${assistant.fact}"`;
    }

    // FeedbackEngine: donnerRetourScientifique (partie de checkAnswer)
    function checkAnswer(selectedOption) {
        if (isWaitingForNext) return;
        isWaitingForNext = true;

        document.querySelectorAll('.option-button').forEach(btn => btn.disabled = true);
        let feedbackDelay = 1800;

        if (selectedOption === currentChallengeData.correctAnswer) {
            feedbackTextElement.textContent = "Correct ! Excellente observation scientifique !";
            feedbackTextElement.className = 'correct';
            score += 10;
            questionsAnsweredInLevel++;

            // ProgressionManager: déterminerProchainÉlémentOuNiveau
            if (questionsAnsweredInLevel >= questionsPerLevel) {
                level++;
                questionsAnsweredInLevel = 0;
                feedbackTextElement.textContent = `Bravo ! Vous passez au Niveau ${level} d'exploration atomique !`;

                if (level > Object.keys(elementDatabase).length) {
                    feedbackTextElement.textContent = "Incroyable ! Vous avez maîtrisé tous les éléments de ce safari !";
                    level = Object.keys(elementDatabase).length; // Bloquer au dernier niveau
                    feedbackDelay = 4000;
                }
                // AtomDifficultyManager: ajusterSelonNiveau (implicite par le changement de 'level')
                if (level % 1 === 0 && questionsPerLevel < 9) { // Augmente légèrement le nb de questions
                    questionsPerLevel++;
                }
            }
        } else {
            feedbackTextElement.textContent = `Pas tout à fait... La bonne réponse était : "${currentChallengeData.correctAnswer}". Continuez d'explorer !`;
            feedbackTextElement.className = 'incorrect';
            score = Math.max(0, score - 3);
            feedbackDelay = 3500;
        }

        // UserProfile: enregistrerDécouverte (implicite par score/level)
        scoreElement.textContent = score;
        levelElement.textContent = level;
        updateProgressBar();
        updateAssistantDisplay(); // Peut changer d'assistant avec le niveau

        setTimeout(() => {
            isWaitingForNext = false;
            generateChallenge();
        }, feedbackDelay);
    }

    function updateProgressBar() {
        const progressPercentage = (questionsAnsweredInLevel / questionsPerLevel) * 100;
        progressBarFillElement.style.width = `${progressPercentage}%`;
        progressBarFillElement.style.borderRadius = progressPercentage >= 99 ? '10px' : '10px 0 0 10px';
    }

    // Initialisation de EducationalGameShell
    updateAssistantDisplay();
    generateChallenge();
    updateProgressBar();
});