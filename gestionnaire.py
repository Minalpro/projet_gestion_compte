import json # Permet de travailler avec des fichier et des données JSON
import logging # Utilisé pour créer des journaux dans une application
import uuid # Utiliser pour générer des mot de passe unique

# Configuration de la journalisation
logging.basicConfig(filename="transaction.log", level=logging.INFO, format="%(asctime)s-%(message)s")

# Création de la classe compte
class Compte:
    # Les attributs de la classe compte
    def __init__(self, titulaire, solde_initial):
        self.id = str(uuid.uuid4()) # Création d'un identifiant unique
        self.titulaire = titulaire
        self.solde = solde_initial
    logging.basicConfig(filename="transaction.log", level=logging.INFO, format="%(asctime)s-%(message)s")

# Déclaration des méthodes de la classe compte
    def deposer(self, montant):
        if montant <=0:
            raise ValueError("Le montant du dépôt doit être positif.")
        self.solde +=montant
        logging.info(f"Dépôt de {montant} sur le compte {self.id} ({self.titulaire}). Nouveau solde :v{self.solde}")

    def retirer(self, montant):
        if montant <= 0:
            raise ValueError("Le montant du retrait est doit être positif.")
        if montant > self.solde:
            raise ValueError("Fonds insuffissants pour éffectuer ce retrait.")
        self.solde -=montant
        logging.info(f"Retrait de {montant} sur compte {self.id} ({self.titulaire}). Nouveau solde : {self.solde}")
        
    def afficher_solde(self):
        return f"Titulaire : {self.titulaire}, Solde : {self.solde:.2f}"

# Création de la classe gestionnaire de compte
class GestionnaireDeComptes:
    # Cr&ation de l'attribut liste de compte
    def __init__(self):
        self.comptes = []
    
    # Déclaration des méthodes de la classe gestionnaire de compte
    def creer_compte(self, titulaire, solde_initial):
        compte = compte(titulaire, solde_initial)
        self.comptes.append(compte)
        return compte

    def supprimer_compte(self, id_compte):
        compte = self.trouver_compte(id_compte)
        self.comptes.remove(compte)
        logging.info(f"Compte supprimé : {id_compte} ({compte.titulaire})")

    def afficher_comptes(self):
        if not self.comptes:
            return "Aucun compte trouvé"
        return "\n".joint([f"ID : {compte.id}, {compte.afficher_solde()}" for compte in self.comptes])
    
    def trouver_compte(self, id_compte):
        for compte in self.comptes:
            if compte.id==id_compte:
                return compte
            raise ValueError("Compte non trouvé.")

    def sauvegarder_comptes(self, fichier="comptes.json"):
        with open (fichier, "w") as f:
            json.dump([compte.__dict__ for compte in self.comptes], f)
    
    def charger_comptes(self, fichier="comptes.json"):
        try:
            with open(fichier, "r") as f:
                comptes_data = json.load(f)
                self.comptes = [compte(**compte) for compte in comptes_data]
        except FileNotFoundError:
            pass


# Création du menu principal du projet
def menu():
    gestionnaire = GestionnaireDeComptes()
    gestionnaire.charger_comptes()

    while True:
        print("\nMenu :")
        print("1. Créer un compte")
        print("2. Supprimer un compte")
        print("3. Consulter un compte")
        print("4. Déposer de l'argent")
        print("5. Retirer de l'argent")
        print("6. Afficher tous les comptes")
        print("7. Quitter")

        choix = input("Votre choix : ")

        if choix=="1":
            titulaire = input("Nom du titulaire: ")
            solde_initial = float(input("Solde initial: "))
            compte = gestionnaire.creer_compte(titulaire, solde_initial)
            print(f"Compte créé avec succès. ID : {compte.id}")

        elif choix=="2":
            id_compte = input("ID du compte à supprimer : ")
            try:
                compte = gestionnaire.supprimer_compte(id_compte)
                print("Compte supprimer avec succès.")
            except ValueError as e:
                print(e)

        elif choix == "3":
            id_compte = input("ID du compte à consulter : ")
            try:
                compte = gestionnaire.trouver_compte(id_compte)
                print(compte.afficher_solde())
            except ValueError as e:
                print(e)
        
        elif choix == "4":
            id_compte = input("ID du compte : ")
            montant = float(input("Montant à déposer : "))
            try:
                compte = gestionnaire.trouver_compte(id_compte)
                compte.deposer(montant)
                print("Dépôt effectué avec succès.")
            except ValueError as e:
                print(e)
        
        elif choix == "5":
            id_compte = input("ID du compte : ")
            montant = float(input("Montant à retirer : "))
            try:
                compte = gestionnaire.trouver_compte(id_compte)
                compte.retirer(montant)
                print("Retrait effectué avec succès.")
            except ValueError as e:
                print(e)
        elif choix == "6":
            print(gestionnaire.afficher_comptes())

        elif choix == "7":
            gestionnaire.sauvegarder_comptes()
            print("Comptes sauvegardés. Au revoir!")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__== "__main__":
    menu()


                




            
    
