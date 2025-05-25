import graphviz

def generer_modele_grandeurs_mesures():
    """Génère le modèle adapté pour le jeu de grandeurs et mesures"""

    dot = graphviz.Digraph('Modele_Jeu_Grandeurs_Mesures')
    dot.attr(rankdir='LR', size='12,8')
    dot.attr('node', shape='record', fontname='Helvetica')

    # Classes conservées du modèle de base
    jeu_label = "{Jeu|+ currentQuestion: Question\\l+ currentQuestionIndex: int\\l+ totalQuestions: int\\l+ score: int\\l+ level: int\\l|+ generateQuestion()\\l+ checkAnswer()\\l+ updateUI()\\l+ nextQuestion()\\l+ endGame()\\l}"
    dot.node('Jeu', jeu_label, fillcolor='lightblue', style='filled')

    question_label = "{Question|+ type: string\\l+ variant: string\\l+ config: object\\l+ correctAnswer: string\\l+ options: list\\l|+ generateComparisonQuestion()\\l+ generateEstimationQuestion()\\l+ generateConversionQuestion()\\l}"
    dot.node('Question', question_label, fillcolor='lightgreen', style='filled')

    utilisateur_label = "{Utilisateur|+ niveau: int\\l+ historiqueProgres: dict\\l|+ getNiveau()\\l+ updateProgres()\\l}"
    dot.node('Utilisateur', utilisateur_label, fillcolor='lightyellow', style='filled')

    progression_label = "{Progression|+ score: int\\l+ questionsReussies: int\\l+ questionsTotales: int\\l+ percentage: float\\l|+ updateLevel()\\l+ calculatePerformance()\\l}"
    dot.node('Progression', progression_label, fillcolor='lightcoral', style='filled')

    # Classes spécifiques aux grandeurs et mesures
    grandeur_label = "{GrandeurMesure|+ name: string\\l+ units: list\\l+ conversions: dict\\l+ examples: list\\l|+ convertUnit()\\l+ compareValues()\\l+ generateRealisticEstimation()\\l}"
    dot.node('GrandeurMesure', grandeur_label, fillcolor='lightpink', style='filled')

    exercice_mesure_label = "{ExerciceMesure|+ measurements: list\\l+ object: string\\l+ fromUnit: string\\l+ toUnit: string\\l|+ generateComparison()\\l+ generateEstimation()\\l+ generateConversion()\\l}"
    dot.node('ExerciceMesure', exercice_mesure_label, fillcolor='lightsteelblue', style='filled')

    # Relations conservées
    dot.edge('Jeu', 'Question', label='génère')
    dot.edge('Jeu', 'Utilisateur', label='interagit avec')
    dot.edge('Jeu', 'Progression', label='met à jour')
    dot.edge('Progression', 'Question', label='adapte difficulté')

    # Relations spécifiques aux mesures
    dot.edge('Question', 'ExerciceMesure', label='spécialise')
    dot.edge('ExerciceMesure', 'GrandeurMesure', label='utilise')
    dot.edge('GrandeurMesure', 'Question', label='configure')

    # Feedback conservé
    feedback_label = "{Feedback|+ message: string\\l+ type: string\\l+ visual: string\\l|+ displayCorrectAnswer()\\l+ showExplanation()\\l}"
    dot.node('Feedback', feedback_label, fillcolor='lightgoldenrodyellow', style='filled')
    dot.edge('Jeu', 'Feedback', label='fournit')

    # Note explicative
    note_label = "Adaptations pour grandeurs et mesures:\\l- 5 types de grandeurs\\l- 3 variants d exercices\\l- Conversions d unités\\l- Estimations réalistes\\l- Comparaisons visuelles"
    dot.node('Note', note_label, shape='note', fillcolor='wheat', style='filled')
    dot.edge('Note', 'GrandeurMesure', style='dashed')
    dot.edge('Note', 'ExerciceMesure', style='dashed')

    return dot

def generer_comparaison_trois_domaines():
    """Génère un diagramme comparatif des trois domaines"""

    dot = graphviz.Digraph('Comparaison_Trois_Domaines')
    dot.attr(rankdir='TB', size='10,12')
    dot.attr('node', shape='record', fontname='Helvetica')

    # Modèle générique
    modele_generique = "{ModeleGenerique|+ Jeu\\l+ Question\\l+ Utilisateur\\l+ Progression\\l+ Feedback\\l|Structure commune\\laux trois domaines}"
    dot.node('ModeleGenerique', modele_generique, fillcolor='lightgray', style='filled')

    # Spécialisations par domaine
    math_label = "{JeuMathematique|+ OperationQuestion\\l+ Addition/Soustraction\\l+ Calcul numérique\\l|Domaine: Arithmétique\\lAge: 6-8 ans}"
    dot.node('JeuMathematique', math_label, fillcolor='lightblue', style='filled')

    grammaire_label = "{JeuGrammaire|+ OrthographeQuestion\\l+ Choix multiples\\l+ Reconnaissance visuelle\\l|Domaine: Linguistique\\lAge: 6-8 ans}"
    dot.node('JeuGrammaire', grammaire_label, fillcolor='lightgreen', style='filled')

    mesures_label = "{JeuMesures|+ GrandeurMesure\\l+ ExerciceMesure\\l+ Comparaison/Estimation/Conversion\\l|Domaine: Grandeurs\\lAge: 6-8 ans}"
    dot.node('JeuMesures', mesures_label, fillcolor='lightcoral', style='filled')

    # Relations d'héritage
    dot.edge('ModeleGenerique', 'JeuMathematique', label='spécialise')
    dot.edge('ModeleGenerique', 'JeuGrammaire', label='spécialise')
    dot.edge('ModeleGenerique', 'JeuMesures', label='spécialise')

    return dot

# Génération des diagrammes
if __name__ == "__main__":
    # Modèle spécifique aux grandeurs et mesures
    modele_mesures = generer_modele_grandeurs_mesures()

    # Comparaison des trois domaines
    comparaison = generer_comparaison_trois_domaines()

    try:
        modele_mesures.render('modele_grandeurs_mesures', format='png', cleanup=True)
        comparaison.render('comparaison_trois_domaines', format='png', cleanup=True)
        print("Diagrammes générés avec succès:")
        print("- modele_grandeurs_mesures.png")
        print("- comparaison_trois_domaines.png")
    except Exception as e:
        print(f"Erreur lors de la génération: {e}")
