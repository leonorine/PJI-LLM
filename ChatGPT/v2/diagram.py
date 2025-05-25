from graphviz import Digraph

# Diagramme de classes
class_diagram = Digraph("Jeu_Mathematique_Classes", format='pdf')
class_diagram.attr(rankdir='LR', size='10')

# --- Classes principales ---
class_diagram.node('Game', '''{Game|
- questions: List<Question>\\l
- currentQuestionIndex: int\\l
- score: int\\l
- totalQuestions: int\\l
- difficulty: DifficultyLevel\\l
- operationType: OperationType\\l
- player: PlayerProfile\\l
|
+ startGame()\\l
+ generateQuestion(): Question\\l
+ submitAnswer(choice: int): bool\\l
+ restartGame()\\l
}''')

class_diagram.node('Question', '''{Question|
- operand1: int\\l
- operand2: int\\l
- correctAnswer: int\\l
- choices: List<int>\\l
- operation: OperationType\\l
|
+ isCorrect(choice: int): bool\\l
}''')

class_diagram.node('PlayerProfile', '''{PlayerProfile|
- name: string\\l
- progressData: ProgressData\\l
|
+ updateProgress()\\l
+ getLevel(): DifficultyLevel\\l
}''')

class_diagram.node('ProgressData', '''{ProgressData|
- history: List<ScoreRecord>\\l
- averageScore: float\\l
- preferredOperation: OperationType\\l
}''')

class_diagram.node('ScoreRecord', '''{ScoreRecord|
- date: Date\\l
- score: int\\l
- difficulty: DifficultyLevel\\l
- operation: OperationType\\l
}''')

# --- Enumérations ---
class_diagram.node('OperationType', '''{OperationType|
ADDITION\\l
SOUSTRACTION\\l
MULTIPLICATION\\l
}''', shape='record')

class_diagram.node('DifficultyLevel', '''{DifficultyLevel|
EASY\\l
MEDIUM\\l
HARD\\l
}''', shape='record')

# --- Relations ---
class_diagram.edge('Game', 'Question', label='1..*')
class_diagram.edge('Game', 'PlayerProfile', label='1')
class_diagram.edge('PlayerProfile', 'ProgressData', label='1')
class_diagram.edge('ProgressData', 'ScoreRecord', label='1..*')
class_diagram.edge('Game', 'OperationType', label='uses')
class_diagram.edge('Question', 'OperationType', label='uses')
class_diagram.edge('ProgressData', 'OperationType', label='prefers')

# --- Diagramme de séquence ---
sequence_diagram = Digraph("Jeu_Mathematique_Sequence", format='pdf')
sequence_diagram.attr(rankdir='TB', size='10')

sequence_diagram.node('User', 'Joueur', shape='actor')
sequence_diagram.node('UI', 'UI', shape='rectangle')
sequence_diagram.node('GameObj', 'Game', shape='rectangle')
sequence_diagram.node('QuestionObj', 'Question', shape='rectangle')
sequence_diagram.node('ProfileObj', 'PlayerProfile', shape='rectangle')

sequence_diagram.edge('User', 'UI', 'Choisit mode / répond')
sequence_diagram.edge('UI', 'GameObj', 'submitAnswer(choice)')
sequence_diagram.edge('GameObj', 'QuestionObj', 'isCorrect()')
sequence_diagram.edge('GameObj', 'ProfileObj', 'updateProgress()')
sequence_diagram.edge('GameObj', 'UI', 'Afficher score/question')

# Exporter les images
class_diagram_path = class_diagram.render('diagramme_classes')
sequence_diagram_path = sequence_diagram.render('diagramme_sequence')

class_diagram_path, sequence_diagram_path
