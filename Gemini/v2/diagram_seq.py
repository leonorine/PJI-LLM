# Filename: diagram_seq.py
import graphviz

dot_seq = graphviz.Digraph('SafariMathsSequenceDiagram', comment='Safari Maths - User Interaction Sequence', format='pdf')
dot_seq.attr(rankdir='TB', splines='ortho', nodesep='0.5') # TB for Top-to-Bottom sequence
dot_seq.node_attr.update(shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Helvetica', fontsize='10')
dot_seq.edge_attr.update(fontname='Helvetica', fontsize='9')

# Participants / Components as nodes (can also use subgraphs for lifelines if desired)
dot_seq.node('User', shape='actor', fillcolor='khaki')
dot_seq.node('UIController', fillcolor='lightgreen')
dot_seq.node('GameEngine', fillcolor='lightcoral')
dot_seq.node('ProblemFactory')
dot_seq.node('SelectedMathOperation', label='MathOperation\n(Addition/Subtraction)', fillcolor='lightgoldenrodyellow') # Placeholder for the chosen operation strategy
dot_seq.node('FeedbackController')
dot_seq.node('ScoreKeeper')
dot_seq.node('ProgressTracker')


# Sequence of Interactions
# Using invisible nodes and edges for ordering if needed, or rely on top-to-bottom rendering.
# The edge labels will primarily define the sequence messages.

dot_seq.edge('User', 'UIController', label='1. Choisit le mode d\'opération\n(Addition, Soustraction, Mixte)')
dot_seq.edge('UIController', 'GameEngine', label='2. informeModeChoisi(mode)')
dot_seq.edge('GameEngine', 'GameEngine', label='3. setOperationMode(mode)\n   configure activeOperations') # Self-loop for internal state change

dot_seq.edge('GameEngine', 'ProblemFactory', label='4. demandeNouveauProblème(niveau, modeOp)')
dot_seq.edge('ProblemFactory', 'SelectedMathOperation', label='5. génèreOpérandesPourDifficulté()')
dot_seq.edge('SelectedMathOperation', 'ProblemFactory', label='6. retourneOpérandes()')
dot_seq.edge('ProblemFactory', 'SelectedMathOperation', label='7. calculeRésultat()')
dot_seq.edge('SelectedMathOperation', 'ProblemFactory', label='8. retourneRéponseCorrecte()')
dot_seq.edge('ProblemFactory', 'GameEngine', label='9. retourneProblème(Problème)')

dot_seq.edge('GameEngine', 'UIController', label='10. afficheProblème(Problème)')
dot_seq.edge('User', 'UIController', label='11. Entre sa réponse')
dot_seq.edge('UIController', 'GameEngine', label='12. soumetRéponseUtilisateur(réponse)')

dot_seq.edge('GameEngine', 'GameEngine', label='13. évalueRéponse()') # Internal evaluation

dot_seq.edge('GameEngine', 'FeedbackController', label='14. demandeFeedback(estCorrect, réponseCorrecte)')
dot_seq.edge('FeedbackController', 'GameEngine', label='15. retourneFeedback(Feedback)')

dot_seq.edge('GameEngine', 'ScoreKeeper', label='16. metÀJourScore(estCorrect)')
dot_seq.edge('GameEngine', 'ProgressTracker', label='17. enregistreTentative(Problème, réponseUtilisateur, estCorrect)')

dot_seq.edge('GameEngine', 'UIController', label='18. metÀJourAffichage(Feedback, score, niveau)')
dot_seq.edge('UIController', 'User', label='19. Affiche feedback & état du jeu')

dot_seq.edge('GameEngine', 'GameEngine', label='20. Vérifie si niveau complété\n   (Si oui, advanceLevel())')
dot_seq.edge('GameEngine', 'GameEngine', label='21. Prépare le prochain cycle (retour à l\'étape 4 ou 1)')


# Render the sequence diagram
sequence_diagram_filename = 'safari_maths_sequence_diagram_evolved'
try:
    dot_seq.render(sequence_diagram_filename, view=False)
    print(f"Sequence diagram saved as {sequence_diagram_filename}.pdf and {sequence_diagram_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print(f"Graphviz executable not found. DOT source saved as {sequence_diagram_filename}")