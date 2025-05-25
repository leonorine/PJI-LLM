import graphviz

def clean_text_for_label(text):
    """Cleans text for Graphviz HTML-like labels."""
    text = text.replace("List~", "List[")
    text = text.replace("Map~", "Map[")
    text = text.replace("~", "]")
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()

def create_class_node_label(class_name, stereotype, attributes, methods, color='lightyellow'):
    """Creates an HTML-like label for a class node in Graphviz."""
    label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="{color}">\n'
    stereotype_html = ""
    if stereotype:
        stereotype_text = clean_text_for_label(stereotype)
        stereotype_html = f'<FONT POINT-SIZE="10">&lt;&lt;{stereotype_text}&gt;&gt;</FONT><BR ALIGN="CENTER"/>'
    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2" BGCOLOR="lightblue">{stereotype_html}<B>{class_name}</B></TD></TR>\n'

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
dot_measure = graphviz.Digraph('SafariDesMesures_Model', comment='Model for Safari des Mesures Game', format='png')
dot_measure.attr(rankdir='TB', splines='spline', nodesep='0.7', ranksep='1.0', newrank='true')
dot_measure.node_attr.update(shape='plain', fontname='Helvetica', fontsize='10')
dot_measure.edge_attr.update(fontname='Helvetica', fontsize='9', len='1.5')

# --- Core Game Engine (Largely Reused) ---
attributes_ge = [ "+UserProfile currentUserProfile", "+GameLevel currentLevel", "+GameConfiguration settings", "+ScoreManager scoreManager", "+UserProgressTracker progressTracker", "+ExerciseGenerator exerciseGenerator", "+FeedbackSystem feedbackSystem", "+RewardSystem rewardSystem", "+UIManager uiManager" ]
methods_ge = [ "+startGame()", "+requestNextExercise()", "+submitUserAnswer(answer: string)", "+advanceLevel()", ]
dot_measure.node('GameEngine', label=create_class_node_label('GameEngine', 'Core', attributes_ge, methods_ge, color='lightcoral'))

# --- User and Progress (Largely Reused) ---
dot_measure.node('UserProfile', label=create_class_node_label('UserProfile', None, ["userId: string", "currentLevelId: int", "totalScore: int", "preferences: UserPreferences"], [], color='lightblue'))
dot_measure.node('UserProgressTracker', label=create_class_node_label('UserProgressTracker', None, [], ["loadProfile()", "saveProfile()", "logAttempt(isCorrect: boolean)"], color='lightblue'))

# --- Game Structure (Adapted for Measurements) ---
dot_measure.node('GameLevel', label=create_class_node_label('GameLevel', None, ["levelId: int", "levelName: string", "targetCorrectExercises: int", "difficultyParams: MeasurementDifficultyParams"], [], color='palegreen'))
dot_measure.node('MeasurementDifficultyParams', label=create_class_node_label('MeasurementDifficultyParams', 'Specific', ["grandeursCovered: List<string>", "unitsInvolved: List<string>", "maxNumericValue: int", "conversionComplexity: int (0-2)", "problemTypes: List<string>"], [], color='lightgreen'))
dot_measure.node('GameConfiguration', label=create_class_node_label('GameConfiguration', None, ["levels: Map<int, GameLevel>", "measurementDatabase: Map<int, List<MeasurementExerciseData>>"], [], color='palegreen'))

# --- Exercise Content (Specific to Measurements) ---
dot_measure.node('MeasurementExercise', label=create_class_node_label('MeasurementExercise', 'Specific', ["grandeur: string (Longueur, Masse, etc.)", "questionText: string", "imagePath: string (optional)", "options: List<string>", "correctAnswer: string", "explanation: string (optional)"], [], color='lightgoldenrodyellow'))
# MeasurementExerciseData is used by GameConfiguration and ExerciseGenerator
dot_measure.node('MeasurementExerciseData', label=create_class_node_label('MeasurementExerciseData', 'Data Transfer Object', ["grandeur: string", "questionText: string", "options: List<string>", "correctAnswer: string", "imagePath?: string", "explanation?: string"], [], color='cornsilk'))


dot_measure.node('ExerciseGenerator', label=create_class_node_label('ExerciseGenerator', 'Specific', [], ["generateExercise(levelId: int, db: Map, params: MeasurementDifficultyParams): MeasurementExercise"], color='moccasin'))

# --- Supporting Systems (Largely Reused) ---
dot_measure.node('ScoreManager', label=create_class_node_label('ScoreManager', None, ["currentScore: int"], ["updateScore(isCorrect: boolean)"], color='lightpink'))
dot_measure.node('FeedbackSystem', label=create_class_node_label('FeedbackSystem', None, [], ["generateFeedback(isCorrect: boolean, correctAnswer: string, explanation?: string): FeedbackMessage"], color='lightpink'))
dot_measure.node('FeedbackMessage', label=create_class_node_label('FeedbackMessage', None, ["text: string", "type: string"], [], color='lightpink'))
dot_measure.node('RewardSystem', label=create_class_node_label('RewardSystem', None, ["availableRewards: List<Reward>"], ["getRewardForMilestone(): Reward"], color='lightpink'))
dot_measure.node('Reward', label=create_class_node_label('Reward', None, ["name: string", "imagePath: string", "fact: string"], [], color='lightpink'))
dot_measure.node('UIManager', label=create_class_node_label('UIManager', None, [], ["displayExercise(exercise: MeasurementExercise)", "displayFeedback(feedback: FeedbackMessage)", "updateProgressDisplay(score, level, progressPercent)"], color='lightcyan'))

# --- Relationships ---
dot_measure.edge('GameEngine', 'UserProfile', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 manages"')
dot_measure.edge('GameEngine', 'GameLevel', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 current"')
dot_measure.edge('GameEngine', 'GameConfiguration', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
dot_measure.edge('GameEngine', 'ExerciseGenerator', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 uses"')
# ... other core connections for GameEngine ...
dot_measure.edge('GameEngine', 'ScoreManager', arrowtail='diamond', dir='forward', arrowhead='none')
dot_measure.edge('GameEngine', 'FeedbackSystem', arrowtail='diamond', dir='forward', arrowhead='none')
dot_measure.edge('GameEngine', 'RewardSystem', arrowtail='diamond', dir='forward', arrowhead='none')
dot_measure.edge('GameEngine', 'UIManager', arrowtail='diamond', dir='forward', arrowhead='none')
dot_measure.edge('GameEngine', 'UserProgressTracker', arrowtail='diamond', dir='forward', arrowhead='none')


dot_measure.edge('GameLevel', 'MeasurementDifficultyParams', arrowtail='diamond', dir='forward', arrowhead='none', label='"1 defines"')
dot_measure.edge('GameConfiguration', 'MeasurementExerciseData', style='dashed', arrowhead='vee', label='"contains (DB)"')

dot_measure.edge('ExerciseGenerator', 'GameConfiguration', style='dashed', arrowhead='vee', label='"uses (DB from)"')
dot_measure.edge('ExerciseGenerator', 'MeasurementDifficultyParams', style='dashed', arrowhead='vee', label='"uses for generation"')
dot_measure.edge('ExerciseGenerator', 'MeasurementExercise', style='dashed', arrowhead='vee', label='"creates"')
dot_measure.edge('MeasurementExercise', 'MeasurementExerciseData', style='dashed', arrowhead='open', label='"instantiates from"') # Realization


dot_measure.edge('UIManager', 'MeasurementExercise', style='dashed', arrowhead='vee', label='"displays"')

# Render the diagram
diagram_filename = 'safari_des_mesures_model'
try:
    dot_measure.render(diagram_filename, view=False)
    print(f"Measurement game model diagram saved as {diagram_filename}.png and {diagram_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print(f"Graphviz executable not found. DOT source saved as {diagram_filename}")
except Exception as e:
    print(f"An error occurred during rendering: {e}")
