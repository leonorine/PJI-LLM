import graphviz

# Création du diagramme de classes UML pour le jeu éducatif d'addition et soustraction
def generer_diagramme_classes():
    # Initialisation du diagramme
    dot = graphviz.Digraph('UML_Classe_Jeu_Maths')

    # Configuration générale du diagramme
    dot.attr(rankdir='LR', size='10,6')
    dot.attr('node', shape='record', fontname='Helvetica')

    # Définition des classes avec leurs attributs et méthodes

    # Classe Jeu - Classe principale qui gère la logique du jeu
    jeu_label = "{Jeu|+ currentQuestion: Question\l+ currentQuestionNumber: int\l+ totalQuestions: int\l+ operationType: string\l+ stats: dict\l|+ generateQuestion()\l+ checkAnswer()\l+ updateUI()\l+ resetGame()\l+ setOperationType()\l}"
    dot.node('Jeu', jeu_label)

    # Classe Question - Représente une question mathématique
    question_label = "{Question|+ num1: int\l+ num2: int\l+ operation: string\l+ answer: int\l+ type: string\l|+ generateAddition()\l+ generateSubtraction()\l}"
    dot.node('Question', question_label)

    # Classe Utilisateur - Représente l'enfant qui utilise le jeu
    utilisateur_label = "{Utilisateur|+ niveau: int\l+ historiqueProgres: dict\l|+ getNiveau()\l+ updateProgres()\l}"
    dot.node('Utilisateur', utilisateur_label)

    # Classe Progression - Suit le score et les performances
    progression_label = "{Progression|+ score: int\l+ questionsReussies: int\l+ questionsTotales: int\l+ historiqueDetaille: dict\l|+ adapterDifficulte()\l}"
    dot.node('Progression', progression_label)

    # Relations entre classes

    # Jeu génère des Questions
    dot.edge('Jeu', 'Question', label='génère')

    # Jeu interagit avec l'Utilisateur
    dot.edge('Jeu', 'Utilisateur', label='interagit avec')

    # Jeu met à jour la Progression
    dot.edge('Jeu', 'Progression', label='met à jour')

    # Progression influence la difficulté des Questions
    dot.edge('Progression', 'Question', label='adapte difficulté')

    # Note pour l'extension soustraction - Mise en évidence des modifications
    dot.node('Note', 'Extension pour soustraction\n- Génération de questions de soustraction\n- Statistiques distinctes par opération\n- Sélecteur de type d\'opération', shape='note')
    dot.edge('Note', 'Jeu', style='dashed')
    dot.edge('Note', 'Question', style='dashed')

    return dot

# Diagramme de séquence montrant l'interaction utilisateur
def generer_diagramme_sequence():
    # Initialisation du diagramme
    seq = graphviz.Digraph('Sequence_Interaction_Jeu')

    # Configuration générale du diagramme
    seq.attr(rankdir='TB', size='8,10')
    seq.attr('node', shape='rectangle', fontname='Helvetica')

    # Participants du diagramme de séquence
    seq.node('User', 'Utilisateur')
    seq.node('Game', 'Jeu')
    seq.node('Question', 'Question')
    seq.node('Progression', 'Progression')

    # Messages échangés entre les participants
    # L'utilisateur choisit d'abord le type d'opération
    seq.edge('User', 'Game', label='1. choisit type opération (addition/soustraction/mixte)')

    # Le jeu génère une question appropriée
    seq.edge('Game', 'Question', label='2. génère question selon type choisi')

    # Le jeu affiche la question à l'utilisateur
    seq.edge('Game', 'User', label='3. affiche question')

    # L'utilisateur répond à la question
    seq.edge('User', 'Game', label='4. répond à la question')

    # Le jeu vérifie la réponse
    seq.edge('Game', 'Question', label='5. vérifie réponse')

    # Le jeu met à jour la progression
    seq.edge('Game', 'Progression', label='6. met à jour progression')

    # Le jeu fournit un feedback à l'utilisateur
    seq.edge('Game', 'User', label='7. affiche feedback')

    # Le jeu affiche la progression mise à jour
    seq.edge('Game', 'User', label='8. affiche progression')

    # Note pour l'extension soustraction - Mise en évidence des modifications
    seq.node('Note', 'Extension pour soustraction\n- Choix du type d\'opération\n- Questions d\'addition et soustraction\n- Statistiques distinctes par opération', shape='note')
    seq.edge('Note', 'Game', style='dashed')

    return seq

# Génération et sauvegarde des diagrammes
if __name__ == "__main__":
    # Génération du diagramme de classes
    diagramme_classes = generer_diagramme_classes()

    # Affichage du code source du diagramme de classes
    print("Code source du diagramme de classes:")
    print(diagramme_classes.source)
    print("\n")

    # Tentative de sauvegarde du diagramme de classes
    try:
        diagramme_classes.render('diagramme_classes', format='pdf', cleanup=True)
        print("Diagramme de classes généré avec succès: diagramme_classes.pdf")
    except Exception as e:
        print(f"Impossible de générer le diagramme de classes: {e}")
        print("Assurez-vous que Graphviz est correctement installé sur votre système.")

    # Génération du diagramme de séquence
    diagramme_sequence = generer_diagramme_sequence()

    # Affichage du code source du diagramme de séquence
    print("Code source du diagramme de séquence:")
    print(diagramme_sequence.source)
    print("\n")

    # Tentative de sauvegarde du diagramme de séquence
    try:
        diagramme_sequence.render('diagramme_sequence', format='pdf', cleanup=True)
        print("Diagramme de séquence généré avec succès: diagramme_sequence.pdf")
    except Exception as e:
        print(f"Impossible de générer le diagramme de séquence: {e}")
        print("Assurez-vous que Graphviz est correctement installé sur votre système.")
