#!/usr/bin/env python3
"""
Script de lancement pour le Tetris
Ce script installe les dépendances, exécute les tests et lance le jeu.
"""

import os
import platform
import subprocess
import sys
import time

# =============================================================================
# Fonctions utilitaires pour l'affichage et l'exécution de commandes
# =============================================================================
def print_colored(text, color):
    """
    Affiche du texte coloré dans le terminal.
    
    :param text: Le texte à afficher.
    :param color: La couleur à utiliser ('green', 'yellow', 'red', 'blue', 'purple').
    """
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'end': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['end']}")

def run_command(command, message, error_message=None):
    """
    Exécute une commande système et affiche un message.
    
    :param command: La commande à exécuter.
    :param message: Le message à afficher avant l'exécution.
    :param error_message: Le message d'erreur à afficher en cas d'échec (optionnel).
    :return: True si la commande s'est exécutée avec succès, False sinon.
    """
    print_colored(message, "blue")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(error_message or f"Erreur: {e}", "red")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

# =============================================================================
# Configuration de l'environnement de test
# =============================================================================
def check_pytest_ini():
    """
    Vérifie si le fichier pytest.ini existe, sinon le crée.
    Ce fichier est nécessaire pour définir les marqueurs personnalisés utilisés dans les tests.
    """
    if not os.path.exists("pytest.ini"):
        print_colored("Création du fichier pytest.ini...", "yellow")
        with open("pytest.ini", "w") as f:
            f.write("[pytest]\nmarkers =\n    integration: marks tests as integration tests\n")

def setup_environment():
    """
    Configure l'environnement virtuel et installe les dépendances.
    
    Cette fonction:
    1. Détecte si nous sommes dans un environnement virtuel
    2. Crée un environnement virtuel si nécessaire
    3. Réexécute ce script dans l'environnement virtuel si nous n'y sommes pas déjà
    4. Installe les dépendances requises
    
    :return: True si la configuration a réussi, False sinon.
    """
    # Déterminer le système d'exploitation
    system = platform.system()
    
    # Vérifier si nous sommes dans un environnement virtuel
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print_colored("Création de l'environnement virtuel...", "yellow")
        venv_name = "tetris_env"
        
        # Créer l'environnement virtuel
        if not os.path.exists(venv_name):
            if not run_command(f"python -m venv {venv_name}", "Création de l'environnement virtuel..."):
                return False
        
        # Activer l'environnement virtuel et exécuter ce script à nouveau
        print_colored("Activation de l'environnement virtuel...", "yellow")
        
        if system == "Windows":
            activate_script = os.path.join(venv_name, "Scripts", "activate")
            python_path = os.path.join(venv_name, "Scripts", "python")
        else:  # macOS ou Linux
            activate_script = os.path.join(venv_name, "bin", "activate")
            python_path = os.path.join(venv_name, "bin", "python")
        
        # Réexécuter ce script dans l'environnement virtuel
        if system == "Windows":
            cmd = f"{venv_name}\\Scripts\\activate && {python_path} {__file__}"
        else:
            cmd = f"source {activate_script} && {python_path} {__file__}"
        
        os.system(cmd)
        return False  # Le script est réexécuté dans l'environnement virtuel
    
    # Installer les dépendances
    if not run_command("pip install -r requirements.txt", "Installation des dépendances..."):
        return False
    
    return True

# =============================================================================
# Exécution des tests et lancement du jeu
# =============================================================================
def run_tests():
    """
    Exécute les tests pour vérifier le bon fonctionnement du jeu.
    
    Cette fonction:
    1. S'assure que le fichier pytest.ini existe
    2. Lance les tests avec pytest et affiche les résultats détaillés
    
    :return: True si tous les tests passent, False sinon.
    """
    check_pytest_ini()
    print_colored("\n=== EXÉCUTION DES TESTS ===", "purple")
    return run_command("pytest test_tetris.py -v", "Exécution des tests...", "Certains tests ont échoué.")

def launch_game():
    """
    Lance le jeu Tetris.
    
    Cette fonction:
    1. Vérifie si le fichier home_screen.py existe
    2. Lance soit home_screen.py (pour l'écran d'accueil) soit main.py
    3. Utilise la bonne commande selon le système d'exploitation
    
    :return: True si le jeu a été lancé avec succès, False sinon.
    """
    print_colored("\n=== LANCEMENT DU JEU ===", "green")
    time.sleep(1)  # Petit délai pour que l'utilisateur puisse voir le message
    
    # Lancer le jeu
    try:
        # Vérifier si home_screen.py existe, sinon lancer main.py
        if os.path.exists("home_screen.py"):
            if platform.system() == "Windows":
                os.system("python home_screen.py")
            else:
                os.system("python3 home_screen.py")
        else:
            if platform.system() == "Windows":
                os.system("python main.py")
            else:
                os.system("python3 main.py")
        return True
    except Exception as e:
        print_colored(f"Erreur lors du lancement du jeu: {e}", "red")
        return False

# =============================================================================
# Point d'entrée du script
# =============================================================================
def main():
    """
    Point d'entrée du script.
    
    Cette fonction coordonne tout le processus:
    1. Configuration de l'environnement
    2. Exécution des tests
    3. Lancement du jeu si les tests passent ou si l'utilisateur le souhaite malgré des échecs
    """
    print_colored("=== INSTALLATION ET LANCEMENT DU TETRIS ===", "green")
    
    # Configuration de l'environnement
    if not setup_environment():
        print_colored("La configuration de l'environnement a échoué.", "red")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    # Exécution des tests
    tests_passed = run_tests()
    
    # Lancement du jeu si les tests sont passés
    if tests_passed:
        launch_game()
    else:
        print_colored("\nCertains tests ont échoué. Voulez-vous quand même lancer le jeu? (o/n)", "yellow")
        choice = input().lower()
        if choice == 'o' or choice == 'oui' or choice == 'y' or choice == 'yes':
            launch_game()
        else:
            print_colored("Lancement du jeu annulé.", "red")
    
    # Afficher un message sur la désactivation de l'environnement virtuel
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_colored("\nPour désactiver l'environnement virtuel, utilisez la commande 'deactivate'", "blue")

if __name__ == "__main__":
    main()