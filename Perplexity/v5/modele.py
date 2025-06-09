import graphviz

def generer_modele_jeu_astronomie():
    dot = graphviz.Digraph('Jeu_Astronomie')
    dot.attr(rankdir='TB', size='12,10')
    dot.attr('node', shape='record', fontname='Helvetica')

    # Jeu - orchestration
    jeu_label = ("{Jeu|+ currentQuestion: Question\\l"
                 "+ gameState: GameState\\l"
                 "+ totalQuestions: int\\l"
                 "+ sessionData: object\\l"
                 "|+ initializeGame()\\l"
                 "+ orchestrateSession()\\l"
                 "+ manageGameFlow()\\l"
                 "+ terminateSession()\\l}")
    dot.node('Jeu', jeu_label, fillcolor='lightblue', style='filled')

    # Question - unité d'apprentissage
    question_label = ("{Question|+ prompt: string\\l"
                      "+ options: list\\l"
                      "+ correctAnswer: any\\l"
                      "+ metadata: object\\l"
                      "+ domainContext: object\\l"
                      "|+ present()\\l"
                      "+ evaluate(response)\\l"
                      "+ generateHints()\\l"
                      "+ adaptDifficulty()\\l}")
    dot.node('Question', question_label, fillcolor='lightgreen', style='filled')

    # Apprenant - profil
    apprenant_label = ("{Apprenant|+ profile: LearnerProfile\\l"
                       "+ preferences: dict\\l"
                       "+ learningHistory: list\\l"
                       "+ currentLevel: int\\l"
                       "+ adaptiveParameters: object\\l"
                       "|+ updateProfile()\\l"
                       "+ getPreferences()\\l"
                       "+ recordPerformance()\\l"
                       "+ calculateMastery()\\l}")
    dot.node('Apprenant', apprenant_label, fillcolor='lightyellow', style='filled')

    # Domaine - point de variation
    domaine_label = ("{Domaine|+ name: string\\l"
                     "+ concepts: list\\l"
                     "+ rules: RuleSet\\l"
                     "+ assessmentCriteria: object\\l"
                     "+ contentLibrary: object\\l"
                     "|+ generateQuestion()\\l"
                     "+ evaluateAnswer()\\l"
                     "+ adaptContent()\\l"
                     "+ defineProgression()\\l}")
    dot.node('Domaine', domaine_label, fillcolor='lightsteelblue', style='filled')

    # Progression - analytique
    progression_label = ("{Progression|+ analytics: LearningAnalytics\\l"
                         "+ adaptiveEngine: object\\l"
                         "+ masteryModel: object\\l"
                         "+ difficultyScaling: object\\l"
                         "|+ analyzePerformance()\\l"
                         "+ recommendNextChallenge()\\l"
                         "+ adjustDifficulty()\\l"
                         "+ trackMastery()\\l}")
    dot.node('Progression', progression_label, fillcolor='lightcoral', style='filled')

    # Feedback - réponse éducative
    feedback_label = ("{Feedback|+ responseType: string\\l"
                      "+ pedagogicalMessage: string\\l"
                      "+ visualElements: object\\l"
                      "+ adaptiveHints: list\\l"
                      "|+ generateResponse()\\l"
                      "+ personalizeMessage()\\l"
                      "+ provideGuidance()\\l"
                      "+ reinforceLearning()\\l}")
    dot.node('Feedback', feedback_label, fillcolor='lightgoldenrodyellow', style='filled')

    # Relations principales
    dot.edge('Jeu', 'Question', label='orchestre')
    dot.edge('Jeu', 'Apprenant', label='adapte à')
    dot.edge('Jeu', 'Domaine', label='utilise')
    dot.edge('Jeu', 'Progression', label='consulte')
    dot.edge('Jeu', 'Feedback', label='déclenche')
    dot.edge('Domaine', 'Question', label='spécialise')
    dot.edge('Question', 'Feedback', label='génère')
    dot.edge('Feedback', 'Progression', label='informe')
    dot.edge('Progression', 'Apprenant', label='met à jour')
    dot.edge('Progression', 'Domaine', label='configure')
    dot.edge('Apprenant', 'Question', label='influence')

    # Spécialisation pour l'astronomie
    astro_label = ("{AstronomieDomain|+ name: \"Astronomie\"\\l"
                   "+ concepts: [\"constellations\", \"planètes\"]\\l"
                   "+ rules: IdentificationRules\\l"
                   "+ assessmentCriteria: object\\l"
                   "+ contentLibrary: StarDatabase\\l"
                   "|+ generateIdentificationQuestion()\\l"
                   "+ evaluateIdentification()\\l"
                   "+ adaptContent()\\l"
                   "+ defineProgression()\\l}")
    dot.node('AstronomieDomain', astro_label, fillcolor='lightseagreen', style='filled')
    dot.edge('Domaine', 'AstronomieDomain', label='spécialise')

    question_astro_label = ("{AstronomyQuestion|+ prompt: string\\l"
                            "+ options: list\\l"
                            "+ correctAnswer: any\\l"
                            "+ metadata: {imageUrl: string}\\l"
                            "+ domainContext: AstronomyDomain\\l"
                            "|+ present()\\l"
                            "+ evaluate(response)\\l"
                            "+ generateHints()\\l"
                            "+ adaptDifficulty()\\l}")
    dot.node('AstronomyQuestion', question_astro_label, fillcolor='mediumseagreen', style='filled')
    dot.edge('Question', 'AstronomyQuestion', label='spécialise')

    return dot

if __name__ == '__main__':
    modele = generer_modele_jeu_astronomie()
    print(modele.source)
    modele.render('jeu_astronomie_modele', format='png', cleanup=True)
