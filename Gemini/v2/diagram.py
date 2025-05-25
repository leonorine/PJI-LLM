# Filename: diagram.py
import graphviz

def clean_text_for_label(text):
    """Cleans text for Graphviz HTML-like labels."""
    text = text.replace("List~", "List[")
    text = text.replace("Map~", "Map[")
    text = text.replace("~", "]")
    # HTML escape special characters
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()

def create_class_node_label(class_name, stereotype, attributes, methods):
    """Creates an HTML-like label for a class node in Graphviz."""
    label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="lightyellow">\n'

    # Class Name and Stereotype
    stereotype_html = ""
    if stereotype:
        stereotype_html = f'<FONT POINT-SIZE="10">&lt;&lt;{stereotype}&gt;&gt;</FONT><BR ALIGN="CENTER"/>'

    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2" BGCOLOR="moccasin">{stereotype_html}<B>{class_name}</B></TD></TR>\n'

    # Attributes
    if attributes:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        label += '    <B>Attributes:</B><BR ALIGN="LEFT"/>\n'
        for attr in attributes:
            attr_cleaned = clean_text_for_label(attr)
            label += f'    {attr_cleaned}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    else:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"><B>Attributes:</B><BR ALIGN="LEFT"/> </TD></TR>\n' # Empty attributes section

    # Methods
    if methods:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        label += '    <B>Methods:</B><BR ALIGN="LEFT"/>\n'
        for method in methods:
            method_cleaned = clean_text_for_label(method)
            # Basic check if it's a method by looking for ()
            if '()' not in method_cleaned: # ensure methods are marked as such for clarity
                method_cleaned += "()"
            label += f'    {method_cleaned}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    else:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"><B>Methods:</B><BR ALIGN="LEFT"/> </TD></TR>\n' # Empty methods section

    label += '</TABLE>>'
    return label

def create_enum_node_label(enum_name, values):
    """Creates an HTML-like label for an enum node in Graphviz."""
    label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="lightcyan">\n'
    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2" BGCOLOR="paleturquoise"><FONT POINT-SIZE="10">&lt;&lt;enumeration&gt;&gt;</FONT><BR ALIGN="CENTER"/><B>{enum_name}</B></TD></TR>\n'
    if values:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        for val in values:
            label += f'    {clean_text_for_label(val)}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    label += '</TABLE>>'
    return label

# Initialize the Digraph
dot_class = graphviz.Digraph('SafariMathsClassDiagram', comment='Safari Maths - Class Diagram', format='pdf')
dot_class.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.0', newrank='true')
dot_class.node_attr.update(shape='plain', fontname='Helvetica', fontsize='10')
dot_class.edge_attr.update(fontname='Helvetica', fontsize='9', len='1.5')

# --- Define Classes and Enums (relevant to the evolution) ---

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
    "+List~MathOperation~ activeOperations",
    "+string currentOperationMode" # Added for user selection
]
methods_ge = [
    "+startGame()",
    "+requestNextProblem()",
    "+submitUserAnswer(answer: string)",
    "+advanceLevel()",
    "+setOperationMode(mode: string)", # Highlighted change
    "+getCurrentDifficulty() : DifficultyProfile"
]
dot_class.node('GameEngine', label=create_class_node_label('GameEngine', None, attributes_ge, methods_ge))

# UIController
methods_uic = [
    # ... other methods from previous model ...
    "+renderProblem(problem: Problem)",
    "+renderFeedback(feedback: Feedback)",
    "+updateScoreDisplay(score: int)",
    "+displayOperationSelection()", # Highlighted change
    "+getSelectedOperationMode() : string", # Highlighted change
    "+captureUserInput() : string"
]
dot_class.node('UIController', label=create_class_node_label('UIController', None, ["... attributes ..."], methods_uic))


# MathOperation (Interface) - Central to the extensibility
attributes_mo = [
    "+OperationType type",
    "+string displaySymbol"
]
methods_mo = [
    "+calculateResult(operands: List~number~) : number",
    "+generateOperandsForDifficulty(profile: DifficultyProfile) : List~number~",
    "+formatQuestionText(operands: List~number~) : string"
]
dot_class.node('MathOperation', label=create_class_node_label('MathOperation', 'Interface', attributes_mo, methods_mo))

# Addition (Concrete Implementation)
attributes_add = [
    "+OperationType type = OperationType.ADDITION",
    "+string displaySymbol = \"+\""
]
methods_add = [
    "+calculateResult(operands)",
    "+generateOperandsForDifficulty(profile)",
    "+formatQuestionText(operands)"
]
dot_class.node('Addition', label=create_class_node_label('Addition', None, attributes_add, methods_add))

# Subtraction (Concrete Implementation - HIGHLIGHT OF THIS EVOLUTION)
attributes_sub = [
    "+OperationType type = OperationType.SUBTRACTION",
    "+string displaySymbol = \"-\""
]
methods_sub = [
    "+calculateResult(operands)",
    "+generateOperandsForDifficulty(profile) : List~number~", # Ensures num1 >= num2
    "+formatQuestionText(operands)"
]
dot_class.node('Subtraction', label=create_class_node_label('Subtraction', 'IMPLEMENTED', attributes_sub, methods_sub)) # Added stereotype for emphasis

# ProblemFactory
attributes_pf = [
    "+DifficultyAdaptationEngine adaptationEngine"
]
methods_pf = [
    "+generateNewProblem(level: Level, activeOps: List~MathOperation~, currentMode: string) : Problem" # currentMode can influence which op from activeOps
]
dot_class.node('ProblemFactory', label=create_class_node_label('ProblemFactory', None, attributes_pf, methods_pf))


# DifficultyProfile
attributes_dp = [
    "+int minOperandValue",
    "+int maxOperandValue",
    "+int numberOfOperands",
    "+boolean allowNegativeResults (default: false)", # Important for Subtraction
    "+Map~string, any~ operationSpecificConfigs"
]
dot_class.node('DifficultyProfile', label=create_class_node_label('DifficultyProfile', None, attributes_dp, []))

# OperationType (Enum)
values_ot = [ "ADDITION", "SUBTRACTION", "MULTIPLICATION (Future)", "DIVISION (Future)", "MIXED (UI concept)" ]
dot_class.node('OperationType', label=create_enum_node_label('OperationType', values_ot))

# Other classes (simplified for brevity, assume they exist as per previous model)
for name in ['User', 'Level', 'GameSettings', 'ScoreKeeper', 'ProgressTracker',
             'FeedbackController', 'RewardController', 'Problem', 'Reward', 'Feedback',
             'DifficultyAdaptationEngine', 'UserProfile', 'OperationMetrics', 'LevelAttempt', 'ProblemRecord', 'UserPreferences']:
    dot_class.node(name, label=create_class_node_label(name, None, ["...attributes..."], ["...methods..."]))


# --- Define Relationships (Focus on those relevant to the evolution) ---
# GameEngine uses MathOperations
dot_class.edge('GameEngine', 'MathOperation', label='"* uses active"', arrowtail='odiamond', dir='forward', arrowhead='none')
dot_class.edge('GameEngine', 'UIController', arrowtail='diamond', dir='forward', arrowhead='none') # Composition

# Inheritances for MathOperation
dot_class.edge('Addition', 'MathOperation', arrowhead='empty', dir='forward', style='bold', color='blue')
dot_class.edge('Subtraction', 'MathOperation', arrowhead='empty', dir='forward', style='bold', color='red', label="<<Newly Active>>") # Highlight

# ProblemFactory uses MathOperations and DifficultyProfile
dot_class.edge('ProblemFactory', 'MathOperation', style='dashed', arrowhead='vee', label='"selects/uses"')
dot_class.edge('ProblemFactory', 'DifficultyProfile', style='dashed', arrowhead='vee', label='"uses"')
dot_class.edge('GameEngine', 'ProblemFactory', arrowtail='diamond', dir='forward', arrowhead='none')


# UIController interacts with GameEngine for operation mode
dot_class.edge('UIController', 'GameEngine', style='dashed', arrowhead='vee', label='"signals op mode change"')

# Associations with OperationType (Enum)
dot_class.edge('MathOperation', 'OperationType', style='dashed', arrowhead='vee', label='"has a type"')
dot_class.edge('GameEngine', 'OperationType', style='dashed', arrowhead='vee', label='"manages based on mode"')


# Render the class diagram
class_diagram_filename = 'safari_maths_class_diagram_evolved'
try:
    dot_class.render(class_diagram_filename, view=False)
    print(f"Class diagram saved as {class_diagram_filename}.pdf and {class_diagram_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print(f"Graphviz executable not found. DOT source saved as {class_diagram_filename}")