document.addEventListener('DOMContentLoaded', () => {
    const num1Element = document.getElementById('num1');
    const num2Element = document.getElementById('num2');
    const answerInputElement = document.getElementById('answer-input');
    const submitButton = document.getElementById('submit-button');
    const feedbackTextElement = document.getElementById('feedback-text');
    const scoreElement = document.getElementById('score');
    const levelElement = document.getElementById('level');
    const animalImageElement = document.getElementById('animal-image');
    const animalFactElement = document.getElementById('animal-fact');
    const progressBarFillElement = document.getElementById('progress-bar-fill');

    let currentNum1;
    let currentNum2;
    let correctAnswer;
    let score = 0;
    let level = 1;
    let questionsPerLevel = 5; // Nombre de questions pour passer au niveau suivant
    let questionsAnsweredInLevel = 0;

    const safariAnimals = [
        { name: "Lion", image: "images/lion.png", fact: "Le lion est souvent appelé le 'roi de la jungle' !" },
        { name: "Éléphant", image: "images/elephant.png", fact: "L'éléphant d'Afrique est le plus grand animal terrestre !" },
        { name: "Girafe", image: "images/giraffe.png", fact: "La girafe a le plus long cou de tous les mammifères !" },
        { name: "Zèbre", image: "images/zebra.png", fact: "Chaque zèbre a un motif de rayures unique, comme une empreinte digitale !" },
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
        let maxNumber = level * 5; // La difficulté augmente avec le niveau
        if (level >= 3) { // Augmente un peu plus pour les niveaux supérieurs
            maxNumber = level * 6;
        }
        if (level >= 5) {
            maxNumber = level * 7;
        }

        currentNum1 = getRandomInt(1, maxNumber);
        currentNum2 = getRandomInt(1, maxNumber);

        // Pour s'assurer que les problèmes ne deviennent pas trop simples à haut niveau
        if (level > 2 && currentNum1 < level) currentNum1 += level;
        if (level > 2 && currentNum2 < level) currentNum2 += level;


        correctAnswer = currentNum1 + currentNum2;

        num1Element.textContent = currentNum1;
        num2Element.textContent = currentNum2;
        answerInputElement.value = '';
        feedbackTextElement.textContent = '';
        feedbackTextElement.className = ''; // Réinitialiser la classe de couleur
        answerInputElement.focus();
    }

    function updateAnimalDisplay() {
        const animalIndex = (level - 1) % safariAnimals.length; // Boucle sur les animaux
        const currentAnimal = safariAnimals[animalIndex];
        animalImageElement.src = currentAnimal.image;
        animalImageElement.alt = currentAnimal.name;
        animalFactElement.textContent = currentAnimal.fact;
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
                // Augmenter le nombre de questions nécessaires pour les niveaux plus élevés si souhaité
                if (level > 3) questionsPerLevel = 7;
                if (level > 6) questionsPerLevel = 10;
            }
            updateAnimalDisplay(); // Mettre à jour l'animal même si le niveau ne change pas immédiatement (ou le faire seulement au changement de niveau)
        } else {
            feedbackTextElement.textContent = `Oups ! Essaye encore. La bonne réponse était ${correctAnswer}.`;
            feedbackTextElement.className = 'incorrect';
            // Optionnel: déduire des points pour une mauvaise réponse
            // score = Math.max(0, score - 2);
        }
        scoreElement.textContent = score;
        levelElement.textContent = level;
        updateProgressBar();
        setTimeout(generateProblem, feedbackTextElement.className === 'correct' ? 1500 : 3000); // Nouveau problème après un délai
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
    updateAnimalDisplay(); // Afficher le premier animal
    updateProgressBar();
});