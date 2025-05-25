import graphviz
import re

def clean_text(text):
    """Cleans mermaid specific syntax for simpler display or processing."""
    text = text.replace("List~", "List[")
    text = text.replace("Map~", "Map[")
    text = text.replace("~", "]")
    # Remove visibility markers like +,-,# for simple display in label
    # text = text.lstrip('+-# ') # Not removing, will include in label
    return text.strip()

def create_class_node_label(class_name, stereotype, attributes, methods):
    """Creates an HTML-like label for a class node in Graphviz."""
    label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">\n'

    # Class Name and Stereotype
    if stereotype:
        label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2"><FONT POINT-SIZE="10">&lt;&lt;{stereotype}&gt;&gt;</FONT><BR/><B>{class_name}</B></TD></TR>\n'
    else:
        label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2"><B>{class_name}</B></TD></TR>\n'

    # Attributes
    if attributes:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        for attr in attributes:
            # HTML escape special characters like < > &
            attr_cleaned = clean_text(attr).replace("<", "&lt;").replace(">", "&gt;")
            label += f'    {attr_cleaned}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    else:
        # Add an empty attributes row if no attributes to maintain structure for separator
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"> </TD></TR>\n'


    # Methods
    if methods:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        for method in methods:
            method_cleaned = clean_text(method).replace("<", "&lt;").replace(">", "&gt;")
            label += f'    {method_cleaned}()<BR ALIGN="LEFT"/>\n' # Assuming all methods end with () for simplicity
        label += '  </TD></TR>\n'
    else:
        # Add an empty methods row if no methods
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"> </TD></TR>\n'

    label += '</TABLE>>'
    return label

def create_enum_node_label(enum_name, values):
    """Creates an HTML-like label for an enum node in Graphviz."""
    label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">\n'
    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2"><FONT POINT-SIZE="10">&lt;&lt;enumeration&gt;&gt;</FONT><BR/><B>{enum_name}</B></TD></TR>\n'
    if values:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        for val in values:
            label += f'    {val.strip()}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    label += '</TABLE>>'
    return label

# Initialize the Digraph
dot = graphviz.Digraph('MathSafariConceptualModel', comment='Conceptual Model for Math Safari Game', format='png')
dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='0.8') # TB or LR
dot.node_attr.update(shape='plain', fontname='Helvetica', fontsize='10')
dot.edge_attr.update(fontname='Helvetica', fontsize='9')

# --- Define Classes and Enums ---

# GameEngine
attributes_ge = [
    "+User currentUser",
    "+Level currentLevel",
    "+GameSettings settings",
    "+ScoreKeeper scoreKeeper",
    "+ProgressTracker progressTracker",
    "+ProblemFactory problemFactory",
    "+FeedbackController feedbackController",
    "+RewardController rewardController",
    "+UIController uiController",
    "+List~MathOperation~ activeOperations"
]
methods_ge = [
    "+startGame",
    "+requestNextProblem",
    "+submitUserAnswer(answer: string)",
    "+advanceLevel",
    "+setOperations(operations: List~OperationType~)",
    "+getCurrentDifficulty() : DifficultyProfile"
]
dot.node('GameEngine', label=create_class_node_label('GameEngine', None, attributes_ge, methods_ge))

# User
attributes_user = [
    "+string userId",
    "+string userName",
    "+UserPreferences preferences",
    "+UserProfile profile"
]
dot.node('User', label=create_class_node_label('User', None, attributes_user, []))

# UserPreferences
attributes_upref = [
    "+string visualTheme (e.g., \"safari\", \"space\")",
    "+boolean soundEffectsEnabled"
]
dot.node('UserPreferences', label=create_class_node_label('UserPreferences', None, attributes_upref, []))

# UserProfile
attributes_uprof = [
    "+int currentLevelId",
    "+int totalScore",
    "+Map~OperationType, OperationMetrics~ operationMetrics",
    "+Map~int, LevelAttempt~ levelAttemptsLog"
]
dot.node('UserProfile', label=create_class_node_label('UserProfile', None, attributes_uprof, []))

# OperationMetrics
attributes_om = [
    "+int problemsAttempted",
    "+int correctAnswers",
    "+float averageTimeSeconds",
    "+List~float~ accuracyHistory (e.g., last 10 attempts)"
]
dot.node('OperationMetrics', label=create_class_node_label('OperationMetrics', None, attributes_om, []))

# LevelAttempt
attributes_la = [
    "+int levelId",
    "+int scoreAchieved",
    "+boolean isCompleted",
    "+DateTime attemptTimestamp",
    "+List~ProblemRecord~ problemRecords"
]
dot.node('LevelAttempt', label=create_class_node_label('LevelAttempt', None, attributes_la, []))

# ProblemRecord
attributes_pr = [
    "+string problemStatement",
    "+string userAnswer",
    "+string correctAnswer",
    "+boolean wasCorrect",
    "+int timeTakenSeconds"
]
dot.node('ProblemRecord', label=create_class_node_label('ProblemRecord', None, attributes_pr, []))

# Level
attributes_level = [
    "+int levelId",
    "+string levelName",
    "+int targetCorrectAnswersToPass",
    "+int questionsCompletedInLevel",
    "+DifficultyProfile difficultyProfile",
    "+List~OperationType~ allowedOperations",
    "+Reward rewardForCompletion"
]
dot.node('Level', label=create_class_node_label('Level', None, attributes_level, []))

# DifficultyProfile
attributes_dp = [
    "+int minOperandValue",
    "+int maxOperandValue",
    "+int numberOfOperands",
    "+boolean allowNegativeResults",
    "+Map~string, any~ operationSpecificConfigs"
]
dot.node('DifficultyProfile', label=create_class_node_label('DifficultyProfile', None, attributes_dp, []))

# Problem
attributes_problem = [
    "+List~number~ operands",
    "+MathOperation operation",
    "+number correctAnswer",
    "+string questionAsString",
    "+float assignedDifficultyScore"
]
dot.node('Problem', label=create_class_node_label('Problem', None, attributes_problem, []))

# MathOperation (Interface)
attributes_mo = [
    "+OperationType type",
    "+string displaySymbol"
]
methods_mo = [
    "+calculateResult(operands: List~number~) : number",
    "+generateOperandsForDifficulty(profile: DifficultyProfile) : List~number~",
    "+formatQuestionText(operands: List~number~) : string"
]
dot.node('MathOperation', label=create_class_node_label('MathOperation', 'Interface', attributes_mo, methods_mo))

# Addition
attributes_add = [
    "+OperationType type = OperationType.ADDITION",
    "+string displaySymbol = \"+\""
]
methods_add = [
    "+calculateResult(operands)",
    "+generateOperandsForDifficulty(profile)",
    "+formatQuestionText(operands)"
]
dot.node('Addition', label=create_class_node_label('Addition', None, attributes_add, methods_add))

# Subtraction
attributes_sub = [
    "+OperationType type = OperationType.SUBTRACTION",
    "+string displaySymbol = \"-\""
]
methods_sub = [
    "+calculateResult(operands)",
    "+generateOperandsForDifficulty(profile)",
    "+formatQuestionText(operands)"
]
dot.node('Subtraction', label=create_class_node_label('Subtraction', None, attributes_sub, methods_sub))

# Multiplication
attributes_mul = [
    "+OperationType type = OperationType.MULTIPLICATION",
    "+string displaySymbol = \"×\""
]
methods_mul = [
    "+calculateResult(operands)",
    "+generateOperandsForDifficulty(profile)",
    "+formatQuestionText(operands)"
]
dot.node('Multiplication', label=create_class_node_label('Multiplication', None, attributes_mul, methods_mul))

# OperationType (Enum)
values_ot = [
    "ADDITION",
    "SUBTRACTION",
    "MULTIPLICATION",
    "DIVISION"
]
dot.node('OperationType', label=create_enum_node_label('OperationType', values_ot))

# ProblemFactory
attributes_pf = [
    "+DifficultyAdaptationEngine adaptationEngine"
]
methods_pf = [
    "+generateNewProblem(level: Level, activeOps: List~MathOperation~) : Problem"
]
dot.node('ProblemFactory', label=create_class_node_label('ProblemFactory', None, attributes_pf, methods_pf))

# DifficultyAdaptationEngine
methods_dae = [
    "+adaptProfileBasedOnPerformance(currentProfile: DifficultyProfile, userProfile: UserProfile) : DifficultyProfile"
]
dot.node('DifficultyAdaptationEngine', label=create_class_node_label('DifficultyAdaptationEngine', None, [], methods_dae))

# ScoreKeeper
attributes_sk = [
    "+int currentSessionScore",
    "+int pointsPerCorrect"
]
methods_sk = [
    "+recordCorrectAnswer",
    "+recordIncorrectAnswer",
    "+resetSessionScore"
]
dot.node('ScoreKeeper', label=create_class_node_label('ScoreKeeper', None, attributes_sk, methods_sk))

# FeedbackController
methods_fc = [
    "+generateUserFeedback(isCorrect: boolean, correctAnswer?: number, problemContext?: Problem) : Feedback"
]
dot.node('FeedbackController', label=create_class_node_label('FeedbackController', None, [], methods_fc))

# Feedback
attributes_fb = [
    "+string messageText",
    "+FeedbackType type", # (e.g. ENCOURAGEMENT_CORRECT, HINT_INCORRECT, SHOW_SOLUTION)
    "+string visualIndicator" # (e.g. "happy_animal.png", "thinking_face.gif")
]
dot.node('Feedback', label=create_class_node_label('Feedback', None, attributes_fb, []))
# Note: FeedbackType would be another enum or a set of constants
dot.node('FeedbackType', label=create_enum_node_label('FeedbackType', ['ENCOURAGEMENT_CORRECT', 'HINT_INCORRECT', 'SHOW_SOLUTION']))


# RewardController
attributes_rc = [
    "+List~Reward~ allPossibleRewards"
]
methods_rc = [
    "+assignRewardForLevel(level: Level) : Reward",
    "+unlockRewardForUser(user: User, reward: Reward)"
]
dot.node('RewardController', label=create_class_node_label('RewardController', None, attributes_rc, methods_rc))

# Reward
attributes_reward = [
    "+string rewardId",
    "+string rewardName",
    "+string visualAssetPath",
    "+string descriptiveText"
]
dot.node('Reward', label=create_class_node_label('Reward', None, attributes_reward, []))

# ProgressTracker
methods_pt = [
    "+loadUserProfile(userId: string) : UserProfile",
    "+saveUserProfile(user: User)",
    "+logProblemAttempt(user: User, levelId: int, problem: Problem, userAnswer: string, isCorrect: boolean, timeTaken: int)",
    "+getOverallUserStats(userProfile: UserProfile) : object",
    "+getStatsForOperation(userProfile: UserProfile, opType: OperationType) : OperationMetrics"
]
dot.node('ProgressTracker', label=create_class_node_label('ProgressTracker', None, [], methods_pt))

# UIController
methods_uic = [
    "+renderProblem(problem: Problem)",
    "+renderFeedback(feedback: Feedback)",
    "+updateScoreDisplay(score: int)",
    "+updateLevelDisplay(levelName: string)",
    "+renderReward(reward: Reward)",
    "+renderProgressReport(stats: object)",
    "+captureUserInput() : string",
    "+showLevelProgressBar(completed: int, total: int)"
]
dot.node('UIController', label=create_class_node_label('UIController', None, [], methods_uic))

# GameSettings
attributes_gs = [
    "+int startingLevelId",
    "+List~OperationType~ defaultEnabledOperations",
    "+Map~int, Level~ levelDefinitions"
]
dot.node('GameSettings', label=create_class_node_label('GameSettings', None, attributes_gs, []))


# --- Define Relationships ---
# For UML: arrow pointing from part to whole (or subclass to superclass)
# dir='back' means the arrow head is at the source of the edge definition.
# arrowtail is at the source, arrowhead is at the target.
# UML composition: diamond at composite (whole). Arrow from composite to part.
# Graphviz: if dir='forward' (default), tail is source, head is target.

# GameEngine Compositions (GameEngine is the whole)
dot.edge('GameEngine', 'User', label='"1"', arrowtail='diamond', dir='forward', arrowhead='none', constraint='true')
dot.edge('GameEngine', 'Level', label='"manages current"', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('GameEngine', 'GameSettings', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('GameEngine', 'ScoreKeeper', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('GameEngine', 'ProgressTracker', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('GameEngine', 'ProblemFactory', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('GameEngine', 'FeedbackController', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('GameEngine', 'RewardController', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('GameEngine', 'UIController', arrowtail='diamond', dir='forward', arrowhead='none')

# GameEngine Aggregation (GameEngine is the whole)
dot.edge('GameEngine', 'MathOperation', label='"* uses active"', arrowtail='odiamond', dir='forward', arrowhead='none')

# User Compositions
dot.edge('User', 'UserPreferences', label='"1"', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('User', 'UserProfile', label='"1"', arrowtail='diamond', dir='forward', arrowhead='none')

# UserProfile Compositions
dot.edge('UserProfile', 'OperationMetrics', label='"* Map"', arrowtail='diamond', dir='forward', arrowhead='none') # Simplified Map notation
dot.edge('UserProfile', 'LevelAttempt', label='"* Map"', arrowtail='diamond', dir='forward', arrowhead='none') # Simplified Map notation

# LevelAttempt Compositions
dot.edge('LevelAttempt', 'ProblemRecord', label='"* List"', arrowtail='diamond', dir='forward', arrowhead='none')


# Level Compositions
dot.edge('Level', 'DifficultyProfile', label='"1"', arrowtail='diamond', dir='forward', arrowhead='none')
dot.edge('Level', 'Reward', label='"0..1 offers"', arrowtail='diamond', dir='forward', arrowhead='none') # More like association or aggregation for reward

# Problem Composition
dot.edge('Problem', 'MathOperation', label='"1"', arrowtail='diamond', dir='forward', arrowhead='none') # Problem has one MathOperation instance

# Inheritances (Subclass -> Superclass, arrowhead='empty' at Superclass)
dot.edge('Addition', 'MathOperation', arrowhead='empty', dir='forward')
dot.edge('Subtraction', 'MathOperation', arrowhead='empty', dir='forward')
dot.edge('Multiplication', 'MathOperation', arrowhead='empty', dir='forward')

# ProblemFactory Composition
dot.edge('ProblemFactory', 'DifficultyAdaptationEngine', label='"1"', arrowtail='diamond', dir='forward', arrowhead='none')

# Associations / Dependencies (source -> target, arrowhead='vee' or 'open', style='dashed' for dependency)
dot.edge('ProblemFactory', 'Level', style='dashed', arrowhead='vee', label='"uses"')
dot.edge('ProblemFactory', 'MathOperation', style='dashed', arrowhead='vee', label='"uses"')
dot.edge('ProblemFactory', 'DifficultyProfile', style='dashed', arrowhead='vee', label='"uses"') # Added this based on diagram logic

dot.edge('DifficultyAdaptationEngine', 'UserProfile', style='dashed', arrowhead='vee', label='"analyzes"')
dot.edge('DifficultyAdaptationEngine', 'DifficultyProfile', style='dashed', arrowhead='vee', label='"uses/returns"') # Added

dot.edge('ProgressTracker', 'UserProfile', style='dashed', arrowhead='vee', label='"manages"')
dot.edge('ProgressTracker', 'ProblemRecord', style='dashed', arrowhead='vee', label='"logs"') # More a "creates" or "handles" relationship
dot.edge('ProgressTracker', 'User', style='dashed', arrowhead='vee', label='"uses"')
dot.edge('ProgressTracker', 'Problem', style='dashed', arrowhead='vee', label='"uses for logging"')
dot.edge('ProgressTracker', 'OperationMetrics', style='dashed', arrowhead='vee', label='"updates"')


dot.edge('GameSettings', 'Level', arrowhead='vee', label='"defines structure of (Map)"') # Association

# Other associations based on attributes implying usage
dot.edge('MathOperation', 'OperationType', style='dashed', arrowhead='vee', label='"has a type"')
dot.edge('Level', 'OperationType', style='dashed', arrowhead='vee', label='"uses (List)"')
dot.edge('GameSettings', 'OperationType', style='dashed', arrowhead='vee', label='"uses (List)"')
dot.edge('GameEngine', 'OperationType', style='dashed', arrowhead='vee', label='"uses (List)"')
dot.edge('GameEngine', 'DifficultyProfile', style='dashed', arrowhead='vee', label='"uses for return"')


dot.edge('FeedbackController', 'Feedback', style='dashed', arrowhead='vee', label='"generates"')
dot.edge('FeedbackController', 'Problem', style='dashed', arrowhead='vee', label='"uses context"')
dot.edge('Feedback', 'FeedbackType', style='dashed', arrowhead='vee', label='"has a type"')

dot.edge('UIController', 'Problem', style='dashed', arrowhead='vee', label='"renders"')
dot.edge('UIController', 'Feedback', style='dashed', arrowhead='vee', label='"renders"')
dot.edge('UIController', 'Reward', style='dashed', arrowhead='vee', label='"renders"')
dot.edge('UIController', 'Level', style='dashed', arrowhead='vee', label='"uses for display"')


dot.edge('RewardController', 'Reward', style='dashed', arrowhead='vee', label='"manages (List)"') # Manages list
dot.edge('RewardController', 'Level', style='dashed', arrowhead='vee', label='"uses"')
dot.edge('RewardController', 'User', style='dashed', arrowhead='vee', label='"uses"')


# Render the graph
output_filename = 'math_safari_conceptual_model'
try:
    dot.render(output_filename, view=False) # Set view=True to auto-open
    print(f"Class diagram saved as {output_filename}.png and {output_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print("Graphviz executable not found. Please ensure Graphviz is installed and in your PATH.")
    print("You can typically install it with: sudo apt-get install graphviz (Linux) or brew install graphviz (macOS)")
    print(f"Source DOT file saved as {output_filename}")