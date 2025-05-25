def generer_meta_modele_plantuml():
    """Génère le méta-modèle en utilisant la syntaxe PlantUML"""

    plantuml_code = """
@startuml Meta_Modele_Jeux_Mathematiques

' Configuration générale
skinparam classAttributeIconSize 0
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle

' Définition des classes principales
class DomaineMathematique {
  + conceptCle: string
  + sousConceptsAssocies: list
  + ageRecommande: range
  + prerequis: list
  --
  + genererExercice(difficulte)
  + evaluerReponse(reponse)
}

class Apprenant {
  + age: int
  + niveau: int
  + historiquePerformance: dict
  + preferenceApprentissage: dict
  --
  + repondreExercice(exercice)
  + recevoirFeedback(feedback)
  + mettreAJourNiveau()
}

class Exercice {
  + type: string
  + difficulte: int
  + contenu: dict
  + reponseAttendue: any
  + tempsMaximum: int
  --
  + presenter()
  + verifierReponse(reponse)
  + genererIndice()
}

class Feedback {
  + type: string
  + contenu: string
  + impactMotivation: float
  + indiceAssocie: string
  --
  + presenter()
  + ajusterDifficulte()
  + suggererActiviteComplementaire()
}

class Progression {
  + niveauActuel: int
  + objectifsApprentissage: list
  + cheminParcours: list
  + adaptativite: float
  --
  + determinerProchainExercice()
  + evaluerMaitrise()
  + ajusterDifficulte()
  + genererRapportProgression()
}

class Jeu {
  + nom: string
  + interfaceGraphique: dict
  + mecaniquesJeu: list
  + recompenses: dict
  --
  + initialiser()
  + executerTour()
  + terminerSession()
  + sauvegarderProgression()
}

' Relations entre les classes
Jeu --> DomaineMathematique : utilise
Jeu --> Apprenant : interagit avec
Jeu --> Exercice : présente
Jeu --> Feedback : fournit
Jeu --> Progression : gère

DomaineMathematique --> Exercice : génère
Apprenant --> Exercice : répond à
Exercice --> Feedback : détermine
Feedback --> Progression : influence
Progression --> DomaineMathematique : adapte
Progression --> Apprenant : met à jour

@enduml
"""
    return plantuml_code

def generer_exemple_addition_soustraction_plantuml():
    """Génère l'exemple d'addition/soustraction en utilisant la syntaxe PlantUML"""

    plantuml_code = """
@startuml Instance_Addition_Soustraction

' Configuration générale
skinparam classAttributeIconSize 0
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle

' Définition des classes spécifiques
class OperationsArithmetiques {
  + conceptCle: "Opérations élémentaires"
  + sousConceptsAssocies: [addition, soustraction]
  + ageRecommande: 6-8 ans
  + prerequis: [comptage, numération]
  --
  + genererAddition(difficulte)
  + genererSoustraction(difficulte)
  + evaluerResultat(reponse)
}

class ExerciceOperation {
  + type: "opération"
  + difficulte: 1-3
  + contenu: {operande1, operateur, operande2}
  + reponseAttendue: resultat
  --
  + afficherOperation()
  + verifierResultat(reponse)
}

class FeedbackOperation {
  + type: "textuel et visuel"
  + contenu: message adapté
  + impactMotivation: positif/négatif
  --
  + afficherMessage()
  + montrerSolution()
}

class ProgressionOperation {
  + niveauActuel: 1-5
  + objectifs: maîtrise des opérations
  + adaptativite: moyenne
  --
  + augmenterDifficulte()
  + changerTypeOperation()
}

' Relations entre les classes
OperationsArithmetiques --> ExerciceOperation : génère
ExerciceOperation --> FeedbackOperation : produit
FeedbackOperation --> ProgressionOperation : informe
ProgressionOperation --> OperationsArithmetiques : ajuste

@enduml
"""
    return plantuml_code

def generer_exemple_multiplication_division_plantuml():
    """Génère l'exemple de multiplication/division en utilisant la syntaxe PlantUML"""

    plantuml_code = """
@startuml Instance_Multiplication_Division

' Configuration générale
skinparam classAttributeIconSize 0
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle

' Définition des classes spécifiques
class OperationsAvancees {
  + conceptCle: "Multiplication et division"
  + sousConceptsAssocies: [tables, groupements]
  + ageRecommande: 8-10 ans
  + prerequis: [addition, soustraction]
  --
  + genererMultiplication(difficulte)
  + genererDivision(difficulte)
  + evaluerResultat(reponse)
}

class ExerciceTablesMD {
  + type: "tables"
  + difficulte: 1-5
  + contenu: {facteur1, operateur, facteur2}
  + reponseAttendue: produit/quotient
  --
  + afficherOperation()
  + proposerChoixMultiples()
}

class FeedbackVisuel {
  + type: "graphique"
  + contenu: représentation visuelle
  + indiceAssocie: aide visuelle
  --
  + montrerGroupements()
  + expliquerErreur()
}

class ProgressionTables {
  + niveauActuel: 1-12
  + objectifs: mémorisation des tables
  + cheminParcours: séquentiel par table
  --
  + debloquerNouvelleTable()
  + reviserTablesProblematiques()
}

' Relations entre les classes
OperationsAvancees --> ExerciceTablesMD : génère
ExerciceTablesMD --> FeedbackVisuel : produit
FeedbackVisuel --> ProgressionTables : informe
ProgressionTables --> OperationsAvancees : ajuste

@enduml
"""
    return plantuml_code

def generer_exemple_formes_geometriques_plantuml():
    """Génère l'exemple de formes géométriques en utilisant la syntaxe PlantUML"""

    plantuml_code = """
@startuml Instance_Formes_Geometriques

' Configuration générale
skinparam classAttributeIconSize 0
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam packageStyle rectangle

' Définition des classes spécifiques
class GeometrieElementaire {
  + conceptCle: "Formes géométriques"
  + sousConceptsAssocies: [2D, 3D, propriétés]
  + ageRecommande: 5-9 ans
  + prerequis: [observation, comparaison]
  --
  + genererFormeAleatoire()
  + evaluerIdentification(reponse)
}

class ExerciceFormes {
  + type: "identification"
  + difficulte: 1-4
  + contenu: {image, propriétés}
  + reponseAttendue: nom de la forme
  --
  + afficherForme()
  + demanderProprietes()
}

class FeedbackInteractif {
  + type: "manipulatif"
  + contenu: forme interactive
  + impactMotivation: découverte
  --
  + permettreRotation()
  + soulignerCaracteristiques()
}

class ProgressionGeometrie {
  + niveauActuel: simple à complexe
  + objectifs: classification des formes
  + adaptativite: élevée
  --
  + introduireNouvellesFamilles()
  + complexifierFormes()
}

' Relations entre les classes
GeometrieElementaire --> ExerciceFormes : génère
ExerciceFormes --> FeedbackInteractif : produit
FeedbackInteractif --> ProgressionGeometrie : informe
ProgressionGeometrie --> GeometrieElementaire : ajuste

@enduml
"""
    return plantuml_code

def generer_diagramme_sequence_plantuml():
    """Génère un diagramme de séquence montrant l'interaction utilisateur"""

    plantuml_code = """
@startuml Sequence_Interaction_Jeu

' Configuration générale
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam sequenceArrowThickness 2

' Participants
actor Utilisateur as User
participant "Jeu" as Game
participant "DomaineMathematique" as Domain
participant "Exercice" as Exercise
participant "Feedback" as Feedback
participant "Progression" as Progress

' Séquence d'interactions
User -> Game: Choisit type d'opération\n(addition/soustraction/mixte)
activate Game

Game -> Domain: Demande génération d'exercice
activate Domain
Domain -> Exercise: Crée exercice adapté
activate Exercise
Domain <-- Exercise: Exercice créé
deactivate Exercise
Game <-- Domain: Exercice fourni
deactivate Domain

Game -> User: Affiche exercice
User -> Game: Répond à l'exercice

Game -> Exercise: Vérifie réponse
activate Exercise
Game <-- Exercise: Résultat de vérification
deactivate Exercise

Game -> Feedback: Génère feedback adapté
activate Feedback
Game <-- Feedback: Feedback fourni
deactivate Feedback

Game -> User: Affiche feedback

Game -> Progress: Met à jour progression
activate Progress
Progress -> Domain: Ajuste difficulté
activate Domain
Progress <-- Domain: Confirmation
deactivate Domain
Game <-- Progress: Progression mise à jour
deactivate Progress

Game -> User: Affiche progression
Game -> User: Propose exercice suivant

deactivate Game

@enduml
"""
    return plantuml_code

# Fonction pour sauvegarder les diagrammes PlantUML dans des fichiers
def sauvegarder_plantuml(nom_fichier, contenu):
    with open(f"{nom_fichier}.puml", "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"Diagramme PlantUML sauvegardé dans {nom_fichier}.puml")

# Sauvegarde des diagrammes PlantUML
if __name__ == "__main__":
    # Génération et sauvegarde des diagrammes PlantUML
    sauvegarder_plantuml("meta_modele_jeux_mathematiques", generer_meta_modele_plantuml())
    sauvegarder_plantuml("instance_addition_soustraction", generer_exemple_addition_soustraction_plantuml())
    sauvegarder_plantuml("instance_multiplication_division", generer_exemple_multiplication_division_plantuml())
    sauvegarder_plantuml("instance_formes_geometriques", generer_exemple_formes_geometriques_plantuml())
    sauvegarder_plantuml("sequence_interaction_jeu", generer_diagramme_sequence_plantuml())

    print("\nTous les diagrammes PlantUML ont été générés avec succès.")
    print("\nPour visualiser ces diagrammes, vous pouvez:")
    print("1. Utiliser l'extension PlantUML dans VS Code ou IntelliJ")
    print("2. Utiliser le service en ligne PlantUML (http://www.plantuml.com/plantuml/)")
    print("3. Installer l'outil PlantUML localement et exécuter: java -jar plantuml.jar *.puml")
