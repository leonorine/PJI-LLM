from graphviz import Digraph

# Création d'un diagramme UML simplifié pour le jeu éducatif d'addition
# Composants: Jeu, Question, Utilisateur, Système de progression
# Relations: Jeu génère Question, Utilisateur répond à Question, Jeu suit la progression

g = Digraph('G', filename='jeu_educatif_addition', format='pdf')

g.attr(rankdir='LR', size='8,5')

g.node('Jeu', 'Jeu Educatif Addition', shape='box', style='filled', color='lightblue')
g.node('Question', 'Question d\'addition', shape='ellipse', style='filled', color='lightyellow')
g.node('Utilisateur', 'Utilisateur (Enfant)', shape='box', style='filled', color='lightgreen')
g.node('Progression', 'Système de progression', shape='diamond', style='filled', color='lightpink')

g.edge('Jeu', 'Question', label='génère')
g.edge('Utilisateur', 'Question', label='répond à')
g.edge('Jeu', 'Progression', label='met à jour')
g.edge('Progression', 'Utilisateur', label='affiche progrès')

# Ajouter des notes pour les règles et interactions

g.node('Règles', 'Règles du jeu:\n- 10 questions\n- Feedback immédiat\n- Pas de pénalité', shape='note', color='orange')
g.edge('Règles', 'Jeu', style='dashed')

# Sauvegarder le diagramme dans un fichier PNG
path = g.render()
path