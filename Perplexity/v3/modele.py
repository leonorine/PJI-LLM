import graphviz

# Génération du modèle adapté pour le jeu de grammaire basé sur le modèle du jeu mathématique

def generer_modele_grammaire():
    dot = graphviz.Digraph('Modele_Jeu_Grammaire')
    dot.attr(rankdir='LR', size='10,6')
    dot.attr('node', shape='record', fontname='Helvetica')

    # Classes conservées du modèle mathématique
    jeu_label = "{Jeu|+ currentQuestion: Question\\l+ currentQuestionNumber: int\\l+ totalQuestions: int\\l+ score: int\\l|+ generateQuestion()\\l+ checkAnswer()\\l+ updateUI()\\l+ resetGame()\\l}"
    dot.node('Jeu', jeu_label)

    question_label = "{Question|+ prompt: string\\l+ options: list\\l+ correctAnswer: string\\l|+ generateOptions()\\l+ verifyAnswer()\\l}"
    dot.node('Question', question_label)

    utilisateur_label = "{Utilisateur|+ niveau: int\\l+ historiqueProgres: dict\\l|+ getNiveau()\\l+ updateProgres()\\l}"
    dot.node('Utilisateur', utilisateur_label)

    progression_label = "{Progression|+ score: int\\l+ questionsReussies: int\\l+ questionsTotales: int\\l+ historiqueDetaille: dict\\l|+ adapterDifficulte()\\l}"
    dot.node('Progression', progression_label)

    # Relations conservées
    dot.edge('Jeu', 'Question', label='génère')
    dot.edge('Jeu', 'Utilisateur', label='interagit avec')
    dot.edge('Jeu', 'Progression', label='met à jour')
    dot.edge('Progression', 'Question', label='adapte difficulté')

    # Modifications spécifiques pour la grammaire
    # Question adaptée pour orthographe avec options multiples
    dot.node('OrthographeQuestion', '{OrthographeQuestion|+ motsOptions: list\\l+ motCorrect: string\\l|+ genererOptions()\\l+ verifierOrthographe()}')
    dot.edge('Question', 'OrthographeQuestion', label='spécialise')

    # Feedback conservé mais adapté au domaine linguistique
    dot.node('Feedback', '{Feedback|+ message: string\\l+ type: string\\l|+ afficherMessage()}')
    dot.edge('Jeu', 'Feedback', label='fournit')

    return dot

modele_grammaire = generer_modele_grammaire()
modele_grammaire.render('modele_jeu_grammaire', format='pdf', cleanup=True)
print("Diagramme généré avec succès: modele_jeu_grammaire.pdf")
