import graphviz

def clean_text_for_label(text):
    """Cleans text for Graphviz HTML-like labels."""
    text = text.replace("List~", "List[")
    text = text.replace("Map~", "Map[")
    text = text.replace("~", "]")
    # HTML escape special characters
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()

def create_class_node_label(class_name, stereotype, attributes, methods, color='lightyellow'):
    """Creates an HTML-like label for a class node in Graphviz."""
    label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="{color}">\n'

    stereotype_html = ""
    if stereotype:
        # CORRECTION: On ajoute &lt;&lt; et &gt;&gt; ici, mais on s'assure qu'ils ne sont pas déjà présents
        stereotype_text = clean_text_for_label(stereotype)
        stereotype_html = f'<FONT POINT-SIZE="10">&lt;&lt;{stereotype_text}&gt;&gt;</FONT><BR ALIGN="CENTER"/>'

    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2" BGCOLOR="moccasin">{stereotype_html}<B>{class_name}</B></TD></TR>\n'

    # ... (Le reste de la fonction reste identique) ...
    if attributes:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        label += '    <B>Attributes:</B><BR ALIGN="LEFT"/>\n'
        for attr in attributes:
            attr_cleaned = clean_text_for_label(attr)
            label += f'    {attr_cleaned}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    else:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"><B>Attributes:</B><BR ALIGN="LEFT"/> </TD></TR>\n'

    if methods:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        label += '    <B>Methods:</B><BR ALIGN="LEFT"/>\n'
        for method in methods:
            method_cleaned = clean_text_for_label(method)
            if '()' not in method_cleaned:
                method_cleaned += "()"
            label += f'    {method_cleaned}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    else:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"><B>Methods:</B><BR ALIGN="LEFT"/> </TD></TR>\n'

    label += '</TABLE>>'
    return label

# Initialize the Digraph
dot_grammar = graphviz.Digraph('SafariDesMots_Model', comment='Model for Safari des Mots Grammar Game', format='png')
# CORRECTION: Changement de splines='ortho' à splines='spline'
dot_grammar.attr(rankdir='TB', splines='spline', nodesep='0.7', ranksep='0.9', newrank='true')
dot_grammar.node_attr.update(shape='plain', fontname='Helvetica', fontsize='10')
dot_grammar.edge_attr.update(fontname='Helvetica', fontsize='9', len='1.5')

# --- Définition des Nœuds (avec stéréotypes corrigés) ---
# CORRECTION: On passe 'Core', 'Specific', 'Data' sans les chevrons
attributes_ge = [ "+UserProfile currentUserProfile", "+GameLevel currentLevel", "+GameConfiguration settings", "+ScoreManager scoreManager", "+UserProgressTracker progressTracker", "+ExerciseGenerator exerciseGenerator", "+FeedbackSystem feedbackSystem", "+RewardSystem rewardSystem", "+UIManager uiManager" ]
methods_ge = [ "+startGame()", "+requestNextExercise()", "+submitUserSelection(selection: string)", "+advanceLevel()", ]
dot_grammar.node('GameEngine', label=create_class_node_label('GameEngine', 'Core', attributes_ge, methods_ge, color='lightcoral'))

dot_grammar.node('GrammarDifficultyParams', label=create_class_node_label('GrammarDifficultyParams', 'Specific', ["wordLengthRange: List~int~", "distractorSimilarity: float", "phoneticComplexity: int", "numberOfOptions: int"], [], color='lightgreen'))
dot_grammar.node('GrammarExercise', label=create_class_node_label('GrammarExercise', 'Specific', ["instructionText: string", "correctWord: string", "distractorWords: List~string~", "allOptions: List~string~ (shuffled)"], [], color='lightgoldenrodyellow'))
dot_grammar.node('ExerciseGenerator', label=create_class_node_label('ExerciseGenerator', 'Specific', ["wordDatabase: Map<int, List<WordEntry>>"], ["generateExercise(levelId: int, params: GrammarDifficultyParams): GrammarExercise"], color='moccasin'))
dot_grammar.node('WordEntry', label=create_class_node_label('WordEntry', 'Data', ["correctForm: string", "commonMisspellings: List~string~", "relatedConcepts: List~string~"], [], color='lightyellow'))

# --- Définition des autres Nœuds (sans stéréotypes ou avec des stéréotypes simples) ---
dot_grammar.node('UserProfile', label=create_class_node_label('UserProfile', None, ["userId: string", "currentLevelId: int", "totalScore: int", "preferences: UserPreferences", "performanceLog: Map<int, LevelPerformance>"], [], color='lightblue'))
dot_grammar.node('UserPreferences', label=create_class_node_label('UserPreferences', None, ["theme: string", "soundEnabled: boolean"], [], color='aliceblue'))
dot_grammar.node('LevelPerformance', label=create_class_node_label('LevelPerformance', None, ["correctAnswers: int", "attempted: int"], [], color='aliceblue'))
dot_grammar.node('UserProgressTracker', label=create_class_node_label('UserProgressTracker', None, [], ["loadProfile()", "saveProfile()", "logAttempt(isCorrect: boolean)"], color='lightblue'))
dot_grammar.node('GameLevel', label=create_class_node_label('GameLevel', None, ["levelId: int", "levelName: string", "targetCorrectExercises: int", "exercisesCompletedThisLevel: int", "difficultyParams: GrammarDifficultyParams"], [], color='palegreen'))
dot_grammar.node('GameConfiguration', label=create_class_node_label('GameConfiguration', None, ["levels: Map<int, GameLevel>", "rewards: List<Reward>"], [], color='palegreen'))
dot_grammar.node('ScoreManager', label=create_class_node_label('ScoreManager', None, ["currentScore: int", "pointsPerCorrect: int"], ["updateScore(isCorrect: boolean)"], color='lightpink'))
dot_grammar.node('FeedbackSystem', label=create_class_node_label('FeedbackSystem', None, [], ["generateFeedback(isCorrect: boolean, correctAnswer?: string): FeedbackMessage"], color='lightpink'))
dot_grammar.node('FeedbackMessage', label=create_class_node_label('FeedbackMessage', None, ["text: string", "type: string (CORRECT/INCORRECT)"], [], color='lightpink'))
dot_grammar.node('RewardSystem', label=create_class_node_label('RewardSystem', None, ["availableRewards: List<Reward>"], ["getRewardForMilestone() : Reward"], color='lightpink'))
dot_grammar.node('Reward', label=create_class_node_label('Reward', None, ["name: string", "imagePath: string", "unlockFact: string"], [], color='lightpink'))
dot_grammar.node('UIManager', label=create_class_node_label('UIManager', None, [], ["displayExercise(exercise: GrammarExercise)", "displayFeedback(feedback: FeedbackMessage)", "updateProgressDisplay(score: int, level: int, progressPercent: float)"], color='lightcyan'))

# --- Définition des Relations (inchangées, mais devraient mieux fonctionner avec splines='spline') ---
dot_grammar.edge('GameEngine', 'UserProfile', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 manages"')
dot_grammar.edge('GameEngine', 'GameLevel', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 current"')
dot_grammar.edge('GameEngine', 'GameConfiguration', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
dot_grammar.edge('GameEngine', 'ScoreManager', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
dot_grammar.edge('GameEngine', 'UserProgressTracker', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
dot_grammar.edge('GameEngine', 'ExerciseGenerator', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
dot_grammar.edge('GameEngine', 'FeedbackSystem', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
dot_grammar.edge('GameEngine', 'RewardSystem', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
dot_grammar.edge('GameEngine', 'UIManager', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 interacts_with"')
dot_grammar.edge('UserProfile', 'UserPreferences', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 has"')
dot_grammar.edge('UserProfile', 'LevelPerformance', arrowtail='diamond', dir='forward', arrowhead='none', label='"* logs"')
dot_grammar.edge('GameLevel', 'GrammarDifficultyParams', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 defines"')
dot_grammar.edge('ExerciseGenerator', 'WordEntry', style='dashed', arrowhead='vee', label='"uses data from (DB)"')
dot_grammar.edge('ExerciseGenerator', 'GrammarExercise', style='dashed', arrowhead='vee', label='"creates"')
dot_grammar.edge('ExerciseGenerator', 'GrammarDifficultyParams', style='dashed', arrowhead='vee', label='"uses for generation"')
dot_grammar.edge('UIManager', 'GrammarExercise', style='dashed', arrowhead='vee', label='"displays"')
dot_grammar.edge('UIManager', 'FeedbackMessage', style='dashed', arrowhead='vee', label='"displays"')
dot_grammar.edge('UIManager', 'Reward', style='dashed', arrowhead='vee', label='"displays"')

# Render the diagram
diagram_filename = 'safari_des_mots_model_fixed'
try:
    dot_grammar.render(diagram_filename, view=False)
    print(f"Grammar game model diagram saved as {diagram_filename}.png and {diagram_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print(f"Graphviz executable not found. Please ensure Graphviz is installed and in your PATH.")
    print(f"Source DOT file saved as {diagram_filename}")
except Exception as e:
    print(f"An error occurred during rendering: {e}")

