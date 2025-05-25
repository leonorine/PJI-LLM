document.addEventListener('DOMContentLoaded', () => {
    const optionsAreaElement = document.getElementById('options-area');
    const feedbackTextElement = document.getElementById('feedback-text');
    const scoreElement = document.getElementById('score');
    const levelElement = document.getElementById('level');
    const animalImageElement = document.getElementById('animal-image');
    const animalFactElement = document.getElementById('animal-fact');
    const progressBarFillElement = document.getElementById('progress-bar-fill');
    const instructionElement = document.getElementById('instruction');

    let score = 0;
    let level = 1;
    let questionsPerLevel = 5;
    let questionsAnsweredInLevel = 0;
    let currentCorrectWord = '';
    let isWaitingForNext = false; // Verrou pour éviter les clics multiples pendant le feedback

    // Base de données de mots (peut être étendue)
    const wordDatabase = {
        1: [
            { word: "chat", distractors: ["cha", "shat"] },
            { word: "vélo", distractors: ["vello", "véloe"] },
            { word: "pomme", distractors: ["pome", "paume"] },
            { word: "rose", distractors: ["roze", "rosse"] },
            { word: "lune", distractors: ["lunne", "leune"] },
            { word: "main", distractors: ["min", "mein"] },
        ],
        2: [
            { word: "maison", distractors: ["maizon", "meson"] },
            { word: "école", distractors: ["ecole", "écolle"] },
            { word: "soleil", distractors: ["solleil", "soleille"] },
            { word: "bateau", distractors: ["bato", "batteau"] },
            { word: "fleur", distractors: ["fleure", "flleur"] },
            { word: "table", distractors: ["tabel", "tablle"] },
        ],
        3: [
            { word: "oiseau", distractors: ["oiso", "oiseux"] },
            { word: "temps", distractors: ["temp", "tan"] },
            { word: "blanc", distractors: ["blan", "blant"] },
            { word: "photo", distractors: ["foto", "photto"] },
            { word: "gâteau", distractors: ["gateau", "gato"] },
            { word: "éléphant", distractors: ["elefant", "éléfan"] },
        ]
    };

    const safariAnimals = [
        { name: "Zèbre Agile", image: "images/zebra.png", fact: "Les zèbres ont des rayures uniques !" },
        { name: "Lion Courageux", image: "images/lion.png", fact: "Le lion est le roi de la savane !" },
        { name: "Girafe Élégante", image: "images/giraffe.png", fact: "La girafe a un très long cou !" },
        { name: "Éléphant Sage", image: "images/elephant.png", fact: "L'éléphant a une excellente mémoire !" },
        { name: "Singe Malin", image: "images/monkey.png", fact: "Les singes adorent jouer !" }
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

    function generateProblem() {
        if (isWaitingForNext) return; // Si on attend déjà, ne rien faire
        isWaitingForNext = true; // Verrouiller pour la génération

        // Sélectionner un ensemble de mots pour le niveau actuel
        // Si le niveau dépasse, on utilise le dernier niveau disponible
        const currentLevelSet = wordDatabase[level] || wordDatabase[Object.keys(wordDatabase).pop()];
        const problemData = getRandomElement(currentLevelSet);

        currentCorrectWord = problemData.word;
        // S'assurer qu'on a assez de distracteurs (ici 2)
        const distractors = shuffleArray(problemData.distractors).slice(0, 2);

        // Créer les options (le mot correct + 2 distracteurs) et les mélanger
        const options = shuffleArray([currentCorrectWord, ...distractors]);

        optionsAreaElement.innerHTML = ''; // Vider les options précédentes
        options.forEach(opt => {
            const button = document.createElement('button');
            button.classList.add('option-button');
            button.textContent = opt;
            button.addEventListener('click', () => {
                if (!isWaitingForNext) { // Vérifier le verrou avant de répondre
                    checkAnswer(opt);
                }
            });
            optionsAreaElement.appendChild(button);
        });

        feedbackTextElement.textContent = '';
        feedbackTextElement.className = '';
        isWaitingForNext = false; // Déverrouiller une fois la question prête
    }

    function updateAnimalDisplay() {
        const animalIndex = Math.floor(score / 30) % safariAnimals.length;
        const currentAnimal = safariAnimals[animalIndex];
        animalImageElement.src = currentAnimal.image;
        animalImageElement.alt = currentAnimal.name;
        animalFactElement.textContent = `Niveau ${level}: ${currentAnimal.fact}`;
    }

    function checkAnswer(selectedWord) {
        if (isWaitingForNext) return; // Empêcher les réponses multiples
        isWaitingForNext = true; // Verrouiller pendant le feedback

        // Désactiver les boutons pendant le feedback
        document.querySelectorAll('.option-button').forEach(btn => btn.disabled = true);

        let feedbackDelay = 1500; // Délai par défaut (bonne réponse)

        if (selectedWord === currentCorrectWord) {
            feedbackTextElement.textContent = "Bravo ! C'est la bonne orthographe !";
            feedbackTextElement.className = 'correct';
            score += 10;
            questionsAnsweredInLevel++;

            if (questionsAnsweredInLevel >= questionsPerLevel) {
                level++;
                questionsAnsweredInLevel = 0;
                feedbackTextElement.textContent = `Fantastique ! Tu passes au Niveau ${level} !`;

                if (level > Object.keys(wordDatabase).length) {
                    feedbackTextElement.textContent = "Bravo, tu as terminé tous les niveaux !";
                    level = Object.keys(wordDatabase).length; // Bloquer au dernier niveau
                    feedbackDelay = 4000; // Plus long délai à la fin
                }
                if (level % 2 === 0 && questionsPerLevel < 8) {
                    questionsPerLevel++;
                }
            }
            updateAnimalDisplay();
        } else {
            feedbackTextElement.textContent = `Oups ! Le mot correct était "${currentCorrectWord}". Essaye encore !`;
            feedbackTextElement.className = 'incorrect';
            score = Math.max(0, score - 3);
            feedbackDelay = 3000; // Délai plus long si incorrect
        }

        scoreElement.textContent = score;
        levelElement.textContent = level;
        updateProgressBar();

        // Planifier la prochaine question
        setTimeout(() => {
            isWaitingForNext = false; // Déverrouiller juste avant de générer
            generateProblem();
        }, feedbackDelay);
    }

    function updateProgressBar() {
        const progressPercentage = (questionsAnsweredInLevel / questionsPerLevel) * 100;
        progressBarFillElement.style.width = `${progressPercentage}%`;
        progressBarFillElement.style.borderRadius = progressPercentage >= 99 ? '10px' : '10px 0 0 10px';
    }

    // Initialisation
    updateAnimalDisplay(); // Affiche le premier animal
    generateProblem(); // Génère la première question
    updateProgressBar(); // Met à jour la barre (à 0%)
});