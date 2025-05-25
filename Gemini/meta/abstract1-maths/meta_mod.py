# Filename: generate_metamodel_diagram.py
import graphviz

def clean_text_for_label(text):
    """Cleans text for Graphviz HTML-like labels."""
    text = text.replace("List~", "List[")
    text = text.replace("Map~", "Map[")
    text = text.replace("~", "]")
    # HTML escape special characters
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()

def create_metaclass_node_label(class_name, attributes, methods, color='lightblue'):
    """Creates an HTML-like label for a metaclass node."""
    label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="{color}">\n'
    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2" BGCOLOR="powderblue"><B>{class_name}</B></TD></TR>\n'

    # Attributes
    if attributes:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        label += '    <B>Attributes:</B><BR ALIGN="LEFT"/>\n'
        for attr in attributes:
            attr_cleaned = clean_text_for_label(attr)
            label += f'    {attr_cleaned}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    else:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"><B>Attributes:</B><BR ALIGN="LEFT"/> </TD></TR>\n'

    # Methods / Responsibilities
    if methods:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT">\n'
        label += '    <B>Responsibilities/Methods:</B><BR ALIGN="LEFT"/>\n'
        for method in methods:
            method_cleaned = clean_text_for_label(method)
            if '()' not in method_cleaned: # Add () for clarity if missing
                method_cleaned += "()"
            label += f'    {method_cleaned}<BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    else:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2"><B>Responsibilities/Methods:</B><BR ALIGN="LEFT"/> </TD></TR>\n'

    label += '</TABLE>>'
    return label

# Initialize the Digraph
dot_meta = graphviz.Digraph('EducationalGameMetamodel', comment='Metamodel for Educational Math Games', format='jpg')
dot_meta.attr(rankdir='TB', splines='spline', nodesep='0.6', ranksep='1.2', overlap='false')
dot_meta.node_attr.update(shape='plain', fontname='Helvetica', fontsize='10')
dot_meta.edge_attr.update(fontname='Helvetica', fontsize='9', len='1.8')

# --- Define Meta-Model Components ---

# Core Game Structure
dot_meta.node('EducationalGame', label=create_metaclass_node_label('EducationalGame',
                                                                   ["targetAudience: String", "overallGoals: List<String>", "theme: GameTheme (Optional)"],
                                                                   ["initialize()", "runGameLoop()"], color='khaki'))
dot_meta.node('GameActivity', label=create_metaclass_node_label('GameActivity',
                                                                ["activityId: String", "associatedObjectives: List<LearningObjective>"],
                                                                ["startActivity()", "endActivity()"], color='lightcoral'))
dot_meta.node('GameTheme', label=create_metaclass_node_label('GameTheme',
                                                             ["name: String", "visualStyle: String", "narrativeElements: List<String>"], [], color='lightgrey'))

# Learning Content Structure
dot_meta.node('LearningDomain', label=create_metaclass_node_label('LearningDomain', ["name: String"], [], color='palegreen'))
dot_meta.node('LearningObjective', label=create_metaclass_node_label('LearningObjective',
                                                                     ["objectiveId: String", "description: String", "requiredSkills: List<Skill>"], [], color='palegreen'))
dot_meta.node('Skill', label=create_metaclass_node_label('Skill', ["skillId: String", "description: String"], [], color='palegreen'))

# Exercise Structure
dot_meta.node('ExerciseTemplate', label=create_metaclass_node_label('ExerciseTemplate',
                                                                    ["templateId: String", "interactionType: String", # e.g., 'MCQ', 'NumericInput', 'DragDrop'
                                                                     "targetObjective: LearningObjective"],
                                                                    ["definePresentationFormat()", "defineSolutionFormat()"], color='lightgoldenrodyellow'))
dot_meta.node('ExerciseInstance', label=create_metaclass_node_label('ExerciseInstance',
                                                                    ["instanceId: String", "presentationData: PresentationData", "solutionData: SolutionData"],
                                                                    ["presentToUser()", "evaluateAnswer(userAnswer)"], color='lightgoldenrodyellow'))
dot_meta.node('PresentationData', label=create_metaclass_node_label('PresentationData', ["content: Any"], [], color='lightyellow'))
dot_meta.node('SolutionData', label=create_metaclass_node_label('SolutionData', ["expectedAnswer: Any", "tolerance: Float (Optional)"], [], color='lightyellow'))
dot_meta.node('ExerciseGenerator', label=create_metaclass_node_label('ExerciseGenerator', [],
                                                                     ["generateInstance(template: ExerciseTemplate, difficulty: DifficultyProfile): ExerciseInstance"], color='moccasin'))

# Difficulty and Progression
dot_meta.node('DifficultyProfile', label=create_metaclass_node_label('DifficultyProfile',
                                                                     ["levelId: String", "parameters: Map<String, Any>"], # e.g., {'range': [1,10], 'num_distractors': 3}
                                                                     [], color='lightblue'))
dot_meta.node('ProgressionController', label=create_metaclass_node_label('ProgressionController',
                                                                         ["strategy: String"], # e.g., 'Linear', 'Adaptive', 'MasteryBased'
                                                                         ["getNextActivityOrExercise(performance: UserPerformanceData): GameActivity/ExerciseInstance",
                                                                          "updateDifficulty(performance: UserPerformanceData): DifficultyProfile"], color='lightblue'))

# User and Performance
dot_meta.node('UserProfile', label=create_metaclass_node_label('UserProfile',
                                                               ["userId: String", "preferences: Map<String, Any>", "performanceData: UserPerformanceData"],
                                                               ["loadProfile()", "saveProfile()"], color='lightpink'))
dot_meta.node('UserPerformanceData', label=create_metaclass_node_label('UserPerformanceData',
                                                                       ["metrics: Map<EvaluationMetric, List<Result>>", "masteryLevels: Map<LearningObjective, Float>"],
                                                                       ["recordResult(metric, result)", "calculateMastery()"], color='lightpink'))
dot_meta.node('EvaluationMetric', label=create_metaclass_node_label('EvaluationMetric', ["metricId: String", "description: String"], [], color='lightsalmon'))
dot_meta.node('FeedbackPolicy', label=create_metaclass_node_label('FeedbackPolicy',
                                                                  ["timing: String", # e.g., 'Immediate', 'Delayed'
                                                                   "contentFormat: String"], # e.g., 'CorrectIncorrect', 'Hint', 'Explanation'
                                                                  ["generateFeedback(isCorrect, context): Feedback"], color='lightsalmon'))
dot_meta.node('Feedback', label=create_metaclass_node_label('Feedback', ["message: String", "type: String"], [], color='lightsalmon'))


# --- Define Meta-Model Relationships ---

# Composition / Aggregation (Whole -> Part)
dot_meta.edge('EducationalGame', 'GameActivity', label='"1..*" contains', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('EducationalGame', 'LearningDomain', label='"1..*" covers', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('EducationalGame', 'ProgressionController', label='"1" uses', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('EducationalGame', 'FeedbackPolicy', label='"1" defines', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('EducationalGame', 'EvaluationMetric', label='"1..*" defines', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('EducationalGame', 'GameTheme', label='"0..1" has', arrowtail='odiamond', dir='forward', arrowhead='none')
dot_meta.edge('EducationalGame', 'UserProfile', label='"1..*" for', arrowtail='odiamond', dir='forward', arrowhead='none') # Game has users

dot_meta.edge('LearningDomain', 'LearningObjective', label='"1..*" contains', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('LearningObjective', 'Skill', label='"0..*" requires', arrowtail='odiamond', dir='forward', arrowhead='none')

dot_meta.edge('GameActivity', 'LearningObjective', label='"1..*" targets', arrowhead='vee') # Association
dot_meta.edge('GameActivity', 'ExerciseTemplate', label='"1..*" uses', arrowhead='vee') # Association

dot_meta.edge('ExerciseTemplate', 'LearningObjective', label='"1" targets', arrowhead='vee') # Association

dot_meta.edge('ExerciseInstance', 'PresentationData', label='"1" has', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('ExerciseInstance', 'SolutionData', label='"1" has', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('ExerciseInstance', 'ExerciseTemplate', label='"1" instantiates', style='dashed', arrowhead='open') # Instantiation/Realization

# Dependencies / Associations
dot_meta.edge('ExerciseGenerator', 'ExerciseTemplate', style='dashed', arrowhead='vee', label='"uses"')
dot_meta.edge('ExerciseGenerator', 'DifficultyProfile', style='dashed', arrowhead='vee', label='"uses"')
dot_meta.edge('ExerciseGenerator', 'ExerciseInstance', style='dashed', arrowhead='vee', label='"creates"')

dot_meta.edge('ProgressionController', 'GameActivity', style='dashed', arrowhead='vee', label='"selects"')
dot_meta.edge('ProgressionController', 'ExerciseInstance', style='dashed', arrowhead='vee', label='"selects"')
dot_meta.edge('ProgressionController', 'DifficultyProfile', style='dashed', arrowhead='vee', label='"manages/updates"')
dot_meta.edge('ProgressionController', 'UserPerformanceData', style='dashed', arrowhead='vee', label='"uses"')

dot_meta.edge('UserProfile', 'UserPerformanceData', label='"1" contains', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta.edge('UserPerformanceData', 'EvaluationMetric', style='dashed', arrowhead='vee', label='"records for"')
dot_meta.edge('UserPerformanceData', 'LearningObjective', style='dashed', arrowhead='vee', label='"tracks mastery of"')

dot_meta.edge('FeedbackPolicy', 'Feedback', style='dashed', arrowhead='vee', label='"generates"')
dot_meta.edge('FeedbackPolicy', 'ExerciseInstance', style='dashed', arrowhead='vee', label='"uses context from"') # Feedback depends on evaluation context

dot_meta.edge('EducationalGame', 'ExerciseGenerator', label='"1" uses', arrowtail='odiamond', dir='forward', arrowhead='none') # Game needs a generator


# Render the metamodel diagram
metamodel_filename = 'educational_game_metamodel'
try:
    dot_meta.render(metamodel_filename, view=False)
    print(f"Metamodel diagram saved as {metamodel_filename}.jpg and {metamodel_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print(f"Graphviz executable not found. DOT source saved as {metamodel_filename}")

