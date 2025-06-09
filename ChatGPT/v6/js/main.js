
const allGames = {
    math: [
        { question: "Combien font 5 + 3 ?", choices: ["6", "8", "9"], answer: "8" },
        { question: "9 - 4 ?", choices: ["5", "6", "4"], answer: "5" },
        { question: "2 + 7 ?", choices: ["10", "9", "8"], answer: "9" },
        { question: "6 + 6 ?", choices: ["12", "11", "13"], answer: "12" },
        { question: "8 - 3 ?", choices: ["6", "5", "4"], answer: "5" }
    ],
    grammaire: [
        { question: "Quel mot est bien orthographié ?", choices: ["chatt", "chat", "cha"], answer: "chat" },
        { question: "Quel mot est correct ?", choices: ["maisson", "maison", "meison"], answer: "maison" },
        { question: "Lequel est bien écrit ?", choices: ["soleill", "soleil", "solail"], answer: "soleil" },
        { question: "Choisis le bon mot :", choices: ["journé", "journée", "journai"], answer: "journée" },
        { question: "Quel mot est juste ?", choices: ["enfant", "enfan", "enfants"], answer: "enfant" }
    ],
    grandeurs: [
        { question: "Combien de cm dans 1 m ?", choices: ["10", "100", "1000"], answer: "100" },
        { question: "Quelle unité mesure une masse ?", choices: ["Litre", "Kilogramme", "Mètre"], answer: "Kilogramme" },
        { question: "Quelle unité mesure une durée ?", choices: ["Litre", "Minute", "Grammes"], answer: "Minute" },
        { question: "Quel est le plus petit ?", choices: ["km", "m", "cm"], answer: "cm" },
        { question: "Quelle unité pour la contenance ?", choices: ["L", "g", "cm"], answer: "L" }
    ],
    sciences: [
        { question: "Quel organe permet de respirer ?", choices: ["Cœur", "Foie", "Poumons"], answer: "Poumons" },
        { question: "Planète la plus proche du Soleil ?", choices: ["Mars", "Mercure", "Terre"], answer: "Mercure" },
        { question: "Combien de pattes a une araignée ?", choices: ["6", "8", "10"], answer: "8" },
        { question: "Que produit une plante ?", choices: ["Lumière", "Oxygène", "Fer"], answer: "Oxygène" },
        { question: "Quel est un état de l'eau ?", choices: ["Feu", "Solide", "Cendre"], answer: "Solide" }
    ]
};

let engine = null;

function startGame(gameKey) {
    engine = new RuleEngine(allGames[gameKey]);
    engine.reset();
    renderQuestion();
}

function renderQuestion() {
    const container = document.getElementById("game-container");
    container.innerHTML = "";

    if (engine.isFinished()) {
        container.innerHTML = `<h2>Félicitations ! Score : ${engine.score}/${engine.questions.length}</h2>`;
        const retry = document.createElement("button");
        retry.textContent = "Recommencer";
        retry.onclick = () => engine.reset() || renderQuestion();
        container.appendChild(retry);
        return;
    }

    const q = engine.getCurrentQuestion();
    const title = document.createElement("h2");
    title.textContent = q.question;
    container.appendChild(title);

    q.choices.forEach(choice => {
        const btn = document.createElement("button");
        btn.className = "choice";
        btn.textContent = choice;
        btn.onclick = () => {
            const correct = engine.submitAnswer(choice);
            showFeedback(correct);
        };
        container.appendChild(btn);
    });
}

function showFeedback(correct) {
    const container = document.getElementById("game-container");
    const feedback = document.createElement("div");
    feedback.className = "feedback";
    feedback.textContent = correct ? "Bonne réponse !" : "Mauvaise réponse !";
    container.appendChild(feedback);
    setTimeout(renderQuestion, 1000);
}
