import graphviz

def clean_text_for_label(text):
    """Nettoie le texte pour les étiquettes HTML de Graphviz."""
    text = text.replace("List~", "List[")
    text = text.replace("Map~", "Map[")
    text = text.replace("~", "]")
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()

def create_instance_node_label(class_name, meta_concept, key_attributes, key_responsibilities, color='lightyellow'):
    """Crée une étiquette HTML pour un nœud d'instance de jeu, en référençant son méta-concept."""
    label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="{color}">\n'
    stereotype_html = f'<FONT POINT-SIZE="9" COLOR="dimgray">&lt;&lt;Instance de: {clean_text_for_label(meta_concept)}&gt;&gt;</FONT><BR ALIGN="CENTER"/>'

    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2" BGCOLOR="lightblue">{stereotype_html}<B>{class_name}</B></TD></TR>\n'

    if key_attributes:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT" BGCOLOR="white">\n'
        label += '    <B>Attributs Spécifiques:</B><BR ALIGN="LEFT"/>\n'
        for attr in key_attributes:
            attr_cleaned = clean_text_for_label(attr)
            label += f'    <FONT POINT-SIZE="9">{attr_cleaned}</FONT><BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'

    if key_responsibilities:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT" BGCOLOR="white">\n'
        label += '    <B>Rôles Spécifiques:</B><BR ALIGN="LEFT"/>\n'
        for resp in key_responsibilities:
            resp_cleaned = clean_text_for_label(resp)
            label += f'    <FONT POINT-SIZE="9">{resp_cleaned}</FONT><BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    label += '</TABLE>>'
    return label

# Initialisation du Digraph
dot_atomes = graphviz.Digraph('SafariDesAtomes_GameModel', comment='Modèle du Jeu Safari des Atomes', format='png')
dot_atomes.attr(rankdir='TB', splines='spline', nodesep='0.8', ranksep='1.2', overlap='false', concentrate='true', compound='true', fontname='Helvetica', fontsize='10')
dot_atomes.node_attr.update(shape='plain')
dot_atomes.edge_attr.update(fontname='Helvetica', fontsize='8', len='1.8', minlen='1.5')

# --- Instanciation des Méta-Concepts pour "Safari des Atomes" ---

# 1. Coquille et Contexte du Jeu
dot_atomes.node('SafariAtomesShell', label=create_instance_node_label('SafariAtomesShell', 'EducationalGameShell',
                                                                      ["- publicCible: 8-10 ans", "- objectifs: Identifier éléments (nom, symbole, utilité)", "- thème: Laboratoire Scientifique"],
                                                                      ["+ démarrerExploration()", "+ gérerSession()"], color='khaki'))

# 2. Contenu Pédagogique
with dot_atomes.subgraph(name='cluster_atomes_learning_content') as c:
    c.attr(label='Contenu: Éléments Chimiques', style='filled', color='lightgrey', fontcolor='black')
    c.node('ElementIdentificationObjective', label=create_instance_node_label('ElementIdentificationObjective', 'LearningObjective',
                                                                              ["- description: Associer Symbole-Nom-Utilité pour N éléments", "- critères: 80% de réussite par élément"],
                                                                              [], color='palegreen'))
    c.node('ElementDatabase', label=create_instance_node_label('ElementDatabase', 'DomainSpecificContent',
                                                               ["- typeContenu: Données sur les éléments", "- structure: {nom, symbole, utilité, image, distracteurs}"],
                                                               ["+ getElementData(niveau): ElementInfo"], color='palegreen'))

# 3. Structure de l'Exercice et Difficulté
with dot_atomes.subgraph(name='cluster_atomes_exercise_engine') as c:
    c.attr(label='Moteur d\'Exercice: Atomes', style='filled', color='lightgrey', fontcolor='black')
    c.node('QCMElementType', label=create_instance_node_label('QCMElementType', 'ExerciseType',
                                                              ["- typeInteraction: QCM (Choix Multiple)", "- formatPrésentation: Question textuelle + options", "- formatSolution: Option correcte (String)"],
                                                              [], color='lightgoldenrodyellow'))
    c.node('AtomDifficultyManager', label=create_instance_node_label('AtomDifficultyManager', 'DifficultyController',
                                                                     ["- paramètres: nbÉlémentsParNiveau, complexitéDistracteurs", "- niveauActuel: int"],
                                                                     ["+ ajusterSelonNiveau()"], color='powderblue'))
    c.node('AtomExerciseFactory', label=create_instance_node_label('AtomExerciseFactory', 'ExerciseGenerator',
                                                                   ["- typesExercicesSupportés: [Symbole->Nom, Nom->Symbole, Élément->Utilité]"],
                                                                   ["+ générerDéfiAtomique(typeDéfi, niveau): AtomicChallenge"], color='moccasin'))
    c.node('AtomicChallenge', label=create_instance_node_label('AtomicChallenge', 'PlayableExercise',
                                                               ["- questionAffichée: String", "- optionsProposées: List<String>", "- réponseCorrecte: String", "- imageÉlément?: String"],
                                                               ["+ afficherDéfi()", "+ vérifierRéponse(réponseUtilisateur)"], color='lightgoldenrodyellow'))

# 4. Interaction Utilisateur, Progression et Feedback
with dot_atomes.subgraph(name='cluster_atomes_learner_interaction') as c:
    c.attr(label='Interaction & Progression: Atomes', style='filled', color='lightgrey', fontcolor='black')
    c.node('AtomProgressionSystem', label=create_instance_node_label('AtomProgressionSystem', 'ProgressionManager',
                                                                     ["- stratégie: Linéaire par lot d'éléments", "- scorePourNiveauSup: int"],
                                                                     ["+ déterminerProchainÉlémentOuNiveau()"], color='lightskyblue'))
    c.node('AtomFeedbackUnit', label=create_instance_node_label('AtomFeedbackUnit', 'FeedbackEngine',
                                                                ["- typeFeedback: Immédiat, Correctif (donne la bonne réponse)"],
                                                                ["+ donnerRetourScientifique()"], color='lightsalmon'))
    c.node('ScientistProfile', label=create_instance_node_label('ScientistProfile', 'UserProfile',
                                                                ["- nomScientifiqueEnHerbe: String", "- élémentsDécouverts: List<String>", "- scoreTotal: int", "- niveauActuel: int"],
                                                                ["+ enregistrerDécouverte()"], color='lightpink'))

# --- Relations Clés pour "Safari des Atomes" ---

dot_atomes.edge('SafariAtomesShell', 'ElementIdentificationObjective', label='"vise à atteindre"', style='dashed', arrowhead='vee')
dot_atomes.edge('SafariAtomesShell', 'AtomProgressionSystem', label='"utilise"', arrowtail='diamond', dir='forward', arrowhead='none')
dot_atomes.edge('SafariAtomesShell', 'AtomExerciseFactory', label='"emploie"', arrowtail='diamond', dir='forward', arrowhead='none')
dot_atomes.edge('SafariAtomesShell', 'AtomFeedbackUnit', label='"utilise"', arrowtail='diamond', dir='forward', arrowhead='none')
dot_atomes.edge('SafariAtomesShell', 'ScientistProfile', label='"gère pour"', arrowtail='odiamond', dir='forward', arrowhead='none')

dot_atomes.edge('ElementIdentificationObjective', 'ElementDatabase', label='"se base sur contenu de"', style='dashed', arrowhead='vee', constraint='false')

dot_atomes.edge('AtomExerciseFactory', 'ElementIdentificationObjective', label='"cible"', style='dashed', arrowhead='vee')
dot_atomes.edge('AtomExerciseFactory', 'ElementDatabase', label='"puise dans"', style='dashed', arrowhead='vee')
dot_atomes.edge('AtomExerciseFactory', 'QCMElementType', label='"selon type"', style='dashed', arrowhead='vee')
dot_atomes.edge('AtomExerciseFactory', 'AtomDifficultyManager', label='"configuré par"', style='dashed', arrowhead='vee')
dot_atomes.edge('AtomExerciseFactory', 'AtomicChallenge', label='"crée"', style='dashed', arrowhead='vee')
dot_atomes.edge('AtomicChallenge', 'QCMElementType', label='"est un type de"', style='dashed', arrowhead='empty', dir='back')

dot_atomes.edge('AtomProgressionSystem', 'ElementIdentificationObjective', label='"guide vers maîtrise de"', style='dashed', arrowhead='vee')
dot_atomes.edge('AtomProgressionSystem', 'ScientistProfile', label='"utilise performance de"', style='dashed', arrowhead='vee')
dot_atomes.edge('AtomProgressionSystem', 'AtomDifficultyManager', label='"peut influencer"', style='dashed', arrowhead='vee')

dot_atomes.edge('AtomicChallenge', 'AtomFeedbackUnit', label='"déclenche feedback de"', style='dashed', arrowhead='vee', lhead='cluster_atomes_learner_interaction')
dot_atomes.edge('ScientistProfile', 'AtomicChallenge', label='"interagit avec"', style='dotted', arrowhead='none', constraint='false')


# Render the "Safari des Atomes" model diagram
atomes_model_filename = 'safari_des_atomes_game_model'
try:
    dot_atomes.render(atomes_model_filename, view=False)
    print(f"\"Safari des Atomes\" model diagram saved as {atomes_model_filename}.png and {atomes_model_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print(f"Graphviz executable not found. Please ensure Graphviz is installed and in your PATH.")
    print(f"Source DOT file saved as {atomes_model_filename}")
except Exception as e:
    print(f"An error occurred during rendering: {e}")