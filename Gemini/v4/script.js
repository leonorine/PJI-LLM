document.addEventListener('DOMContentLoaded', () => {
    const questionTextElement = document.getElementById('question-text');
    const questionImageElement = document.getElementById('question-image');
    const optionsAreaElement = document.getElementById('options-area');
    const feedbackTextElement = document.getElementById('feedback-text');
    const scoreElement = document.getElementById('score');
    const levelElement = document.getElementById('level');
    const animalImageElement = document.getElementById('animal-image');
    const animalFactElement = document.getElementById('animal-fact');
    const progressBarFillElement = document.getElementById('progress-bar-fill');

    let score = 0;
    let level = 1;
    let questionsPerLevel = 5; // Nombre de questions pour passer au niveau suivant
    let questionsAnsweredInLevel = 0;
    let currentQuestionData = {};
    let isWaitingForNext = false;

    // Base de données de questions pour les grandeurs et mesures
    const measurementDatabase = {
        1: [ // Niveau 1: Unités de base, comparaisons directes
            {
                grandeur: "Longueur",
                questionText: "Quel est le plus long : une gomme (environ 5 cm) ou un cahier (environ 30 cm) ?",
                options: ["La gomme", "Le cahier", "Ils sont pareils"],
                correctAnswer: "Le cahier",
                image: "images/gomme_cahier.png" // Optionnel: image illustrant gomme et cahier
            },
            {
                grandeur: "Masse",
                questionText: "Qu'est-ce qui est le plus léger : une plume ou une pomme ?",
                options: ["La plume", "La pomme", "C'est pareil"],
                correctAnswer: "La plume",
                image: "images/plume_pomme.png" // Optionnel
            },
            {
                grandeur: "Contenance",
                questionText: "Un verre d'eau contient MOINS qu'une baignoire pleine ?",
                options: ["Vrai", "Faux"],
                correctAnswer: "Vrai",
                explanation: "Une baignoire contient beaucoup plus d'eau qu'un simple verre !"
            },
            {
                grandeur: "Durée",
                questionText: "Qu'est-ce qui dure le plus longtemps : une récréation ou une journée d'école ?",
                options: ["La récréation", "La journée d'école", "C'est pareil"],
                correctAnswer: "La journée d'école"
            },
            {
                grandeur: "Prix",
                questionText: "Si un jouet coûte 5 euros et un autre 10 euros, lequel coûte plus cher ?",
                options: ["Celui à 5 euros", "Celui à 10 euros", "Ils coûtent pareil"],
                correctAnswer: "Celui à 10 euros"
            }
        ],
        2: [ // Niveau 2: Introduction d'unités spécifiques, conversions simples implicites
            {
                grandeur: "Longueur",
                questionText: "Pour mesurer la taille d'une fourmi, on utilise plutôt des...",
                options: ["Kilomètres (km)", "Mètres (m)", "Centimètres (cm) ou Millimètres (mm)"],
                correctAnswer: "Centimètres (cm) ou Millimètres (mm)"
            },
            {
                grandeur: "Masse",
                questionText: "Un paquet de sucre pèse souvent 1...",
                options: ["Gramme (g)", "Kilogramme (kg)", "Litre (L)"],
                correctAnswer: "Kilogramme (kg)",
                image: "images/paquet_sucre.png" // Optionnel
            },
            {
                grandeur: "Contenance",
                questionText: "L'unité principale pour mesurer le lait dans une brique est le...",
                options: ["Mètre (m)", "Litre (L)", "Gramme (g)"],
                correctAnswer: "Litre (L)"
            },
            {
                grandeur: "Durée",
                questionText: "Dans une heure, il y a 60...",
                options: ["Secondes", "Minutes", "Heures"],
                correctAnswer: "Minutes"
            },
            {
                grandeur: "Prix",
                questionText: "1 euro est égal à combien de centimes ?",
                options: ["10 centimes", "50 centimes", "100 centimes"],
                correctAnswer: "100 centimes"
            }
        ],
        3: [ // Niveau 3: Problèmes simples, estimations plus fines
            {
                grandeur: "Longueur",
                questionText: "Si je fais 3 pas d'environ 1 mètre chacun, j'ai parcouru environ...",
                options: ["3 centimètres", "3 mètres", "3 kilomètres"],
                correctAnswer: "3 mètres"
            },
            {
                grandeur: "Masse",
                questionText: "Un chat adulte pèse environ...",
                options: ["50 grammes", "4 kilogrammes", "200 kilogrammes"],
                correctAnswer: "4 kilogrammes",
                image: "images/chat_adulte.png" // Optionnel
            },
            {
                grandeur: "Contenance",
                questionText: "Si je bois 2 verres d'eau de 25 centilitres (cL) chacun, j'ai bu...",
                options: ["50 Litres", "50 centilitres", "25 Litres"],
                correctAnswer: "50 centilitres",
                explanation: "25 cL + 25 cL = 50 cL. 50 cL c'est un demi-litre."
            },
            {
                grandeur: "Durée",
                questionText: "Un film pour enfant dure souvent environ 1 ___ et 30 ___.",
                options: ["Mètre, Grammes", "Heure, Minutes", "Kilogramme, Secondes"],
                correctAnswer: "Heure, Minutes"
            },
            {
                grandeur: "Prix",
                questionText: "J'ai 2 euros. Un livre coûte 1 euro et 50 centimes. Puis-je l'acheter ?",
                options: ["Oui", "Non"],
                correctAnswer: "Oui",
                explanation: "1 euro et 50 centimes, c'est moins que 2 euros."
            }
        ]
    };

    const safariAnimals = [
        { name: "Panda Penseur", image: "images/panda.png", factTemplate: "Les pandas aiment mesurer les bambous avant de les manger !" },
        { name: "Guépard Rapide", image: "images/cheetah.png", factTemplate: "Le guépard mesure sa vitesse pour attraper ses proies !" },
        { name: "Hibou Savant", image: "images/owl.png", factTemplate: "Le hibou estime la distance pour chasser la nuit !" },
        { name: "Baleine Gigantesque", image: "images/whale.png", factTemplate: "La baleine est l'un des plus grands animaux, sa taille se mesure en mètres !" },
        { name: "Colibri Précis", image: "images/hummingbird.png", factTemplate: "Le colibri mesure la quantité de nectar dans chaque fleur !" }
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
        if (isWaitingForNext) return;
        isWaitingForNext = true;

        const currentLevelSet = measurementDatabase[level] || measurementDatabase[Object.keys(measurementDatabase).pop()];
        currentQuestionData = getRandomElement(currentLevelSet);

        questionTextElement.textContent = currentQuestionData.questionText;

        // Gérer l'image de la question
        if (currentQuestionData.image) {
            questionImageElement.src = currentQuestionData.image;
            questionImageElement.style.display = 'block';
            questionImageElement.alt = `Illustration pour ${currentQuestionData.grandeur}`;
        } else {
            questionImageElement.style.display = 'none';
            questionImageElement.src = ""; // Vider la source pour éviter d'afficher l'ancienne image
        }

        const options = shuffleArray([...currentQuestionData.options]); // Mélanger une copie des options

        optionsAreaElement.innerHTML = '';
        options.forEach(optText => {
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
        updateAnimalFact(); // Mettre à jour le fait animal avec la grandeur
        isWaitingForNext = false;
    }

    function updateAnimalDisplay() {
        const animalIndex = Math.floor(score / 20) % safariAnimals.length; // Change d'animal tous les 20 points
        const currentAnimal = safariAnimals[animalIndex];
        animalImageElement.src = currentAnimal.image;
        animalImageElement.alt = currentAnimal.name;
        // Le fait sera mis à jour par updateAnimalFact() lié à la question
    }

    function updateAnimalFact() {
        const animalIndex = Math.floor(score / 20) % safariAnimals.length;
        const currentAnimal = safariAnimals[animalIndex];
        let fact = currentAnimal.factTemplate;
        // Personnaliser le fait si possible avec la grandeur
        if (currentQuestionData.grandeur) {
            fact = `${currentAnimal.name} explore la grandeur : ${currentQuestionData.grandeur.toLowerCase()} ! ` + fact;
        } else {
            fact = currentAnimal.name + " t'encourage ! " + fact;
        }
        animalFactElement.textContent = fact;
    }


    function checkAnswer(selectedOption) {
        if (isWaitingForNext) return;
        isWaitingForNext = true;

        document.querySelectorAll('.option-button').forEach(btn => btn.disabled = true);

        let feedbackDelay = 1800;

        if (selectedOption === currentQuestionData.correctAnswer) {
            feedbackTextElement.textContent = "Excellent ! C'est la bonne réponse !";
            feedbackTextElement.className = 'correct';
            score += 10;
            questionsAnsweredInLevel++;

            if (questionsAnsweredInLevel >= questionsPerLevel) {
                level++;
                questionsAnsweredInLevel = 0;
                feedbackTextElement.textContent = `Super ! Tu passes au Niveau ${level} !`;

                if (level > Object.keys(measurementDatabase).length) {
                    feedbackTextElement.textContent = "Félicitations, tu as exploré toutes les mesures ! Recommence pour devenir un expert.";
                    level = Object.keys(measurementDatabase).length;
                    feedbackDelay = 4000;
                }
                if (level % 2 === 0 && questionsPerLevel < 7) { // Augmente le nombre de questions
                    questionsPerLevel++;
                }
            }
        } else {
            let incorrectMsg = `Dommage ! Ce n'est pas tout à fait ça. La bonne réponse était "${currentQuestionData.correctAnswer}".`;
            if (currentQuestionData.explanation) {
                incorrectMsg += `\nPourquoi ? ${currentQuestionData.explanation}`;
            }
            feedbackTextElement.textContent = incorrectMsg;
            feedbackTextElement.className = 'incorrect';
            score = Math.max(0, score - 2); // Pénalité plus légère
            feedbackDelay = 3500;
        }

        scoreElement.textContent = score;
        levelElement.textContent = level;
        updateProgressBar();
        updateAnimalDisplay(); // Mettre à jour l'image de l'animal (peut changer avec le score)

        setTimeout(() => {
            isWaitingForNext = false;
            generateProblem();
        }, feedbackDelay);
    }

    function updateProgressBar() {
        const progressPercentage = (questionsAnsweredInLevel / questionsPerLevel) * 100;
        progressBarFillElement.style.width = `${progressPercentage}%`;
        progressBarFillElement.style.borderRadius = progressPercentage >= 99 ? '10px' : '10px 0 0 10px';
    }

    // Initialisation
    updateAnimalDisplay();
    generateProblem();
    updateProgressBar();
});