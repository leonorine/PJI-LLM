document.addEventListener('DOMContentLoaded', () => {
    const problemAreaElement = document.getElementById('problem-area'); // Changé pour manipuler le contenu
    const answerInputElement = document.getElementById('answer-input');
    const submitButton = document.getElementById('submit-button');
    const feedbackTextElement = document.getElementById('feedback-text');
    const scoreElement = document.getElementById('score');
    const levelElement = document.getElementById('level');
    const animalImageElement = document.getElementById('animal-image');
    const animalFactElement = document.getElementById('animal-fact');
    const progressBarFillElement = document.getElementById('progress-bar-fill');

    // Sélection du mode d'opération
    const operationRadios = document.querySelectorAll('input[name="operation"]');
    let currentOperationMode = 'addition'; // Mode par défaut

    operationRadios.forEach(radio => {
        radio.addEventListener('change', (event) => {
            currentOperationMode = event.target.value;
            generateProblem(); // Génère un nouveau problème avec le mode sélectionné
            feedbackTextElement.textContent = ''; // Efface le feedback précédent
            feedbackTextElement.className = '';
        });
    });

    let num1, num2, correctAnswer, currentOperatorSymbol;
    let score = 0;
    let level = 1;
    let questionsPerLevel = 5;
    let questionsAnsweredInLevel = 0;

    const safariAnimals = [
        { name: "Lion", image: "images/lion.png", fact: "Le lion est souvent appelé le 'roi de la jungle' !" },
        { name: "Éléphant", image: "images/elephant.png", fact: "L'éléphant d'Afrique est le plus grand animal terrestre !" },
        { name: "Girafe", image: "images/giraffe.png", fact: "La girafe a le plus long cou de tous les mammifères !" },
        { name: "Zèbre", image: "images/zebra.png", fact: "Chaque zèbre a un motif de rayures unique !" },
        { name: "Singe", image: "images/monkey.png", fact: "Les singes sont très intelligents et sociaux !" },
        { name: "Tigre", image: "images/tiger.png", fact: "Le tigre est le plus grand félin sauvage du monde."},
        { name: "Panda", image: "images/panda.png", fact: "Le panda géant mange principalement du bambou."},
        { name: "Rhinocéros", image: "images/rhino.png", fact: "Les rhinocéros ont une peau très épaisse."},
        { name: "Hippopotame", image: "images/hippo.png", fact: "L'hippopotame passe beaucoup de temps dans l'eau."},
        { name: "Crocodile", image: "images/crocodile.png", fact: "Les crocodiles sont d'excellents nageurs."}
    ];

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function generateProblem() {
        let maxNumberBase = level * 4 + 5; // Augmente la base max pour les nombres
        let minNumberBase = level > 2 ? level - 1 : 1;

        let operationToUse = currentOperationMode;

        if (currentOperationMode === 'mixed') {
            operationToUse = Math.random() < 0.5 ? 'addition' : 'subtraction';
        }

        if (operationToUse === 'addition') {
            currentOperatorSymbol = '+';
            num1 = getRandomInt(minNumberBase, maxNumberBase);
            num2 = getRandomInt(minNumberBase, maxNumberBase);
            correctAnswer = num1 + num2;
        } else { // Soustraction
            currentOperatorSymbol = '-';
            // Assurer que num1 >= num2 pour éviter les résultats négatifs
            // et que le résultat ne soit pas trop trivial (ex: 5-5 trop souvent)
            let tempNum1 = getRandomInt(minNumberBase, maxNumberBase);
            let tempNum2 = getRandomInt(minNumberBase, tempNum1); // num2 est <= num1

            // Pour éviter trop de X - 0 ou X - X si minNumberBase est 1
            if (tempNum1 === tempNum2 && tempNum1 > minNumberBase +1 ) { // Si X-X et X n'est pas le plus petit nombre possible
                // essayer de rendre num2 un peu plus petit, si possible.
                tempNum2 = getRandomInt(minNumberBase, Math.max(minNumberBase, tempNum1 -1));
            } else if (tempNum1 === tempNum2 && tempNum1 <= minNumberBase + 1) { // Si X-X et X est petit
                // on augmente num1 pour avoir une chance de faire autre chose que X-X = 0
                tempNum1 = getRandomInt(minNumberBase+1, maxNumberBase);
                tempNum2 = getRandomInt(minNumberBase, tempNum1);
            }

            num1 = tempNum1;
            num2 = tempNum2;
            correctAnswer = num1 - num2;
        }

        problemAreaElement.innerHTML = `<span id="num1">${num1}</span> ${currentOperatorSymbol} <span id="num2">${num2}</span> = ?`;
        answerInputElement.value = '';
        // feedbackTextElement.textContent = ''; // Effacé lors du changement d'opération ou après checkAnswer
        // feedbackTextElement.className = '';
        answerInputElement.focus();
    }

    function updateAnimalDisplay() {
        const animalIndex = (level - 1) % safariAnimals.length; // Change d'animal tous les 20 points
        const currentAnimal = safariAnimals[animalIndex];
        animalImageElement.src = currentAnimal.image;
        animalImageElement.alt = currentAnimal.name;
        animalFactElement.textContent = `Niveau ${level}: ${currentAnimal.fact}`;
    }

    function checkAnswer() {
        const userAnswer = parseInt(answerInputElement.value);

        if (isNaN(userAnswer)) {
            feedbackTextElement.textContent = "Entre un nombre !";
            feedbackTextElement.className = 'incorrect';
            return;
        }

        if (userAnswer === correctAnswer) {
            feedbackTextElement.textContent = "Bravo ! C'est correct !";
            feedbackTextElement.className = 'correct';
            score += 10;
            questionsAnsweredInLevel++;
            if (questionsAnsweredInLevel >= questionsPerLevel) {
                level++;
                questionsAnsweredInLevel = 0;
                feedbackTextElement.textContent = `Super ! Tu passes au Niveau ${level} !`;
                if (level % 3 === 0 && questionsPerLevel < 10) { // Augmente la difficulté tous les 3 niveaux
                    questionsPerLevel++;
                }
            }
            updateAnimalDisplay();
        } else {
            feedbackTextElement.textContent = `Oups ! Essaye encore. La bonne réponse était ${correctAnswer}.`;
            feedbackTextElement.className = 'incorrect';
            score = Math.max(0, score - 2); // Pénalité légère
        }
        scoreElement.textContent = score;
        levelElement.textContent = level;
        updateProgressBar();
        // Génère un nouveau problème après un délai, plus long si incorrect
        setTimeout(generateProblem, feedbackTextElement.className === 'correct' ? 1500 : 3000);
    }

    function updateProgressBar() {
        const progressPercentage = (questionsAnsweredInLevel / questionsPerLevel) * 100;
        progressBarFillElement.style.width = `${progressPercentage}%`;
    }

    submitButton.addEventListener('click', checkAnswer);
    answerInputElement.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            checkAnswer();
        }
    });

    // Initialisation
    generateProblem();
    updateAnimalDisplay();
    updateProgressBar();
});