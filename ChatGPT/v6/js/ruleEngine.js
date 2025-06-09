
class RuleEngine {
    constructor(questions) {
        this.questions = questions;
        this.current = 0;
        this.score = 0;
    }

    getCurrentQuestion() {
        return this.questions[this.current];
    }

    submitAnswer(choice) {
        const correct = choice === this.questions[this.current].answer;
        if (correct) this.score++;
        this.current++;
        return correct;
    }

    isFinished() {
        return this.current >= this.questions.length;
    }

    reset() {
        this.current = 0;
        this.score = 0;
    }
}
