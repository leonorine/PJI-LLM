import graphviz

def clean_text_for_label(text):
    """Nettoie le texte pour les étiquettes HTML de Graphviz."""
    text = text.replace("List~", "List[")
    text = text.replace("Map~", "Map[")
    text = text.replace("~", "]")
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()

def create_simplified_node_label(class_name, stereotype, key_attributes, key_responsibilities, color='lightyellow'):
    """Crée une étiquette HTML simplifiée pour un nœud de classe."""
    label = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" BGCOLOR="{color}">\n'
    stereotype_html = ""
    if stereotype:
        stereotype_text = clean_text_for_label(stereotype)
        stereotype_html = f'<FONT POINT-SIZE="9" COLOR="dimgray">&lt;&lt;{stereotype_text}&gt;&gt;</FONT><BR ALIGN="CENTER"/>'

    label += f'  <TR><TD ALIGN="CENTER" COLSPAN="2" BGCOLOR="lightblue">{stereotype_html}<B>{class_name}</B></TD></TR>\n'

    # Attributs Clés (simplifiés)
    if key_attributes:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT" BGCOLOR="white">\n'
        for attr in key_attributes:
            attr_cleaned = clean_text_for_label(attr)
            label += f'    <FONT POINT-SIZE="9">{attr_cleaned}</FONT><BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'

    # Responsabilités Clés (simplifiées)
    if key_responsibilities:
        label += '  <TR><TD ALIGN="LEFT" COLSPAN="2" BALIGN="LEFT" BGCOLOR="white">\n'
        for resp in key_responsibilities:
            resp_cleaned = clean_text_for_label(resp)
            label += f'    <FONT POINT-SIZE="9">{resp_cleaned}</FONT><BR ALIGN="LEFT"/>\n'
        label += '  </TD></TR>\n'
    label += '</TABLE>>'
    return label

# Initialisation du Digraph
dot_meta_simple = graphviz.Digraph('SimplifiedEducationalGameMetamodel', comment='Simplified Metamodel for Educational Games', format='png')
dot_meta_simple.attr(rankdir='TB', splines='spline', nodesep='0.8', ranksep='1.2', overlap='false', concentrate='true', compound='true', fontname='Helvetica', fontsize='10')
dot_meta_simple.node_attr.update(shape='plain')
dot_meta_simple.edge_attr.update(fontname='Helvetica', fontsize='8', len='1.8', minlen='1.5')

# --- Méta-Concepts Fondamentaux Simplifiés ---

# 1. Coquille et Contexte du Jeu
dot_meta_simple.node('EducationalGameShell', label=create_simplified_node_label('EducationalGameShell', 'Cadre du Jeu',
                                                                                ["- publicCible", "- objectifsGlobaux", "- thème (optionnel)"],
                                                                                ["+ initialiserJeu()", "+ gérerCycleDeJeu()"], color='khaki'))

# 2. Contenu Pédagogique
with dot_meta_simple.subgraph(name='cluster_learning_content') as c:
    c.attr(label='Contenu Pédagogique', style='filled', color='lightgrey', fontcolor='black')
    c.node('LearningObjective', label=create_simplified_node_label('LearningObjective', 'Ce Qui Est Appris',
                                                                   ["- descriptionObjectif", "- critèresMesurables"],
                                                                   [], color='palegreen'))
    c.node('DomainSpecificContent', label=create_simplified_node_label('DomainSpecificContent', 'Données Brutes du Domaine',
                                                                       ["- typeContenu (ex: mots, équations, faits)", "- structureDonnées"],
                                                                       ["+ fournirDonnéesExercice()"], color='palegreen'))

# 3. Structure de l'Exercice et Difficulté
with dot_meta_simple.subgraph(name='cluster_exercise_engine') as c:
    c.attr(label='Moteur d\'Exercice', style='filled', color='lightgrey', fontcolor='black')
    c.node('ExerciseType', label=create_simplified_node_label('ExerciseType', 'Modèle d\'Interaction',
                                                              ["- typeInteraction (QCM, Saisie, etc.)", "- formatPrésentation", "- formatSolution"],
                                                              [], color='lightgoldenrodyellow'))
    c.node('DifficultyController', label=create_simplified_node_label('DifficultyController', 'Gestion Difficulté',
                                                                      ["- paramètresDifficulté (ex: plage, complexité)", "- niveauActuel"],
                                                                      ["+ adapterDifficulté()"], color='powderblue'))
    c.node('ExerciseGenerator', label=create_simplified_node_label('ExerciseGenerator', 'Créateur d\'Exercices',
                                                                   [],
                                                                   ["+ générerExerciceConcret()"], color='moccasin'))
    c.node('PlayableExercise', label=create_simplified_node_label('PlayableExercise', 'Défi Concret',
                                                                  ["- donnéesPrésentées", "- solutionAttendue"],
                                                                  ["+ présenterÀUtilisateur()", "+ évaluerRéponse()"], color='lightgoldenrodyellow'))

# 4. Interaction Utilisateur, Progression et Feedback
with dot_meta_simple.subgraph(name='cluster_learner_interaction') as c:
    c.attr(label='Interaction & Progression', style='filled', color='lightgrey', fontcolor='black')
    c.node('ProgressionManager', label=create_simplified_node_label('ProgressionManager', 'Logique de Progression',
                                                                    ["- stratégieProgression (linéaire, adaptative)", "- étatProgressionUtilisateur"],
                                                                    ["+ déterminerProchaineÉtape()"], color='lightskyblue'))
    c.node('FeedbackEngine', label=create_simplified_node_label('FeedbackEngine', 'Moteur de Feedback',
                                                                ["- typeFeedback (immédiat, explicatif)"],
                                                                ["+ fournirFeedback()"], color='lightsalmon'))
    c.node('UserProfile', label=create_simplified_node_label('UserProfile', 'Données Apprenant',
                                                             ["- idUtilisateur", "- préférences", "- historiquePerformance"],
                                                             ["+ enregistrerPerformance()"], color='lightpink'))

# --- Relations Clés Simplifiées ---

# EducationalGameShell est le conteneur principal
dot_meta_simple.edge('EducationalGameShell', 'LearningObjective', label='"définit les buts de"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('EducationalGameShell', 'ProgressionManager', label='"utilise"', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta_simple.edge('EducationalGameShell', 'ExerciseGenerator', label='"emploie"', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta_simple.edge('EducationalGameShell', 'FeedbackEngine', label='"utilise"', arrowtail='diamond', dir='forward', arrowhead='none')
dot_meta_simple.edge('EducationalGameShell', 'UserProfile', label='"gère pour"', arrowtail='odiamond', dir='forward', arrowhead='none')


# Liens vers le Contenu Pédagogique
dot_meta_simple.edge('LearningObjective', 'DomainSpecificContent', label='"se base sur"', style='dashed', arrowhead='vee', constraint='false') # Un objectif nécessite du contenu pour être enseigné

# Moteur d'Exercice
dot_meta_simple.edge('ExerciseGenerator', 'LearningObjective', label='"cible"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('ExerciseGenerator', 'DomainSpecificContent', label='"utilise"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('ExerciseGenerator', 'ExerciseType', label='"selon"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('ExerciseGenerator', 'DifficultyController', label='"ajusté par"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('ExerciseGenerator', 'PlayableExercise', label='"crée"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('PlayableExercise', 'ExerciseType', label='"est un type de"', style='dashed', arrowhead='empty', dir='back')

# Interaction et Progression
dot_meta_simple.edge('ProgressionManager', 'LearningObjective', label='"guide vers"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('ProgressionManager', 'UserProfile', label='"utilise données de"', style='dashed', arrowhead='vee')
dot_meta_simple.edge('ProgressionManager', 'DifficultyController', label='"influence"', style='dashed', arrowhead='vee') # La progression peut changer la difficulté

dot_meta_simple.edge('PlayableExercise', 'FeedbackEngine', label='"déclenche"', style='dashed', arrowhead='vee', lhead='cluster_learner_interaction') # Le résultat d'un exercice déclenche le feedback
dot_meta_simple.edge('FeedbackEngine', 'UserProfile', label='"informe (implicitement)"', style='dashed', arrowhead='vee', constraint='false') # Le feedback aide l'utilisateur à apprendre

dot_meta_simple.edge('UserProfile', 'PlayableExercise', label='"interagit avec (via UI)"', style='dotted', arrowhead='none', constraint='false') # Relation indirecte

# Placement des clusters pour un meilleur agencement (peut nécessiter des ajustements)
# On peut essayer de forcer un ordre ou un groupement si Graphviz ne le fait pas bien automatiquement.
# Par exemple, en s'assurant que les arêtes entre clusters sont bien définies.
# L'attribut 'compound=true' sur le graphe principal est important pour que les arêtes vers/depuis les clusters (lhead, ltail) fonctionnent.

# Render the simplified metamodel diagram
simplified_metamodel_filename = 'simplified_educational_game_metamodel'
try:
    dot_meta_simple.render(simplified_metamodel_filename, view=False)
    print(f"Simplified metamodel diagram saved as {simplified_metamodel_filename}.png and {simplified_metamodel_filename}")
except graphviz.backend.execute.ExecutableNotFound:
    print(f"Graphviz executable not found. Please ensure Graphviz is installed and in your PATH.")
    print(f"Source DOT file saved as {simplified_metamodel_filename}")
except Exception as e:
    print(f"An error occurred during rendering: {e}")

