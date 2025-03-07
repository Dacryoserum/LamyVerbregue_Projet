#!/usr/bin/env python3
"""
Script de lancement pour le Tetris
Ce script installe les dépendances, exécute les tests et lance le jeu.
Compatible avec Windows, macOS et Linux.
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
    Compatible avec Windows en détectant si colorama est disponible.
    
    :param text: Le texte à afficher.
    :param color: La couleur à utiliser ('green', 'yellow', 'red', 'blue', 'purple').
    """
    # Pour Windows, essayer d'utiliser colorama si disponible
    if platform.system() == "Windows":
        try:
            import colorama
            colorama.init()
            has_colorama = True
        except ImportError:
            has_colorama = False
    else:
        has_colorama = True
    
    if has_colorama:
        colors = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'end': '\033[0m'
        }
        print(f"{colors.get(color, '')}{text}{colors['end']}")
    else:
        # Fallback si colorama n'est pas disponible sur Windows
        print(text)

def run_command(command, message, error_message=None, shell=True):
    """
    Exécute une commande système et affiche un message.
    
    :param command: La commande à exécuter.
    :param message: Le message à afficher avant l'exécution.
    :param error_message: Le message d'erreur à afficher en cas d'échec (optionnel).
    :param shell: Si True, exécute via shell, sinon comme liste d'arguments.
    :return: True si la commande s'est exécutée avec succès, False sinon.
    """
    print_colored(message, "blue")
    try:
        # Utiliser une approche différente pour Windows
        if platform.system() == "Windows" and isinstance(command, str) and shell:
            # Les commandes complexes sur Windows peuvent nécessiter cmd.exe
            process = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            process = subprocess.run(
                command, 
                shell=shell, 
                check=True, 
                capture_output=True, 
                text=True
            )
            
        if process.stdout:
            print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(error_message or f"Erreur: {e}", "red")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False
    except Exception as e:
        print_colored(f"Exception inattendue: {str(e)}", "red")
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

def check_venv_exists(venv_name):
    """
    Vérifie si un environnement virtuel existe.
    
    :param venv_name: Nom de l'environnement virtuel.
    :return: True si l'environnement existe, False sinon.
    """
    if platform.system() == "Windows":
        return os.path.exists(os.path.join(venv_name, "Scripts", "python.exe"))
    else:  # macOS ou Linux
        return os.path.exists(os.path.join(venv_name, "bin", "python"))

def create_venv(venv_name):
    """
    Crée un environnement virtuel Python.
    
    :param venv_name: Nom de l'environnement virtuel à créer.
    :return: True si création réussie, False sinon.
    """
    # Vérifier si Python est accessible
    try:
        # Essayer différentes commandes Python selon la plateforme
        if platform.system() == "Windows":
            python_cmds = ["python", "py", "python3"]
        else:
            python_cmds = ["python3", "python"]
            
        python_cmd = None
        for cmd in python_cmds:
            try:
                subprocess.run([cmd, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                python_cmd = cmd
                break
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
                
        if not python_cmd:
            print_colored("Impossible de trouver Python. Veuillez l'installer.", "red")
            return False
            
        # Créer l'environnement virtuel
        result = run_command(
            [python_cmd, "-m", "venv", venv_name],
            f"Création de l'environnement virtuel '{venv_name}'...",
            shell=False
        )
        return result
    except Exception as e:
        print_colored(f"Erreur lors de la création de l'environnement virtuel: {e}", "red")
        return False

def run_in_venv(venv_name, script_path):
    """
    Exécute un script dans l'environnement virtuel.
    
    :param venv_name: Nom de l'environnement virtuel.
    :param script_path: Chemin du script à exécuter.
    :return: Code de retour de la commande.
    """
    system = platform.system()
    
    if system == "Windows":
        python_path = os.path.join(venv_name, "Scripts", "python.exe")
        # Sur Windows, directement appeler l'exécutable python du venv
        cmd = f'"{python_path}" "{script_path}"'
    else:  # macOS ou Linux
        activate_path = os.path.join(venv_name, "bin", "activate")
        python_path = os.path.join(venv_name, "bin", "python")
        # Sur Unix, source l'activation puis exécute
        cmd = f'source "{activate_path}" && "{python_path}" "{script_path}"'
    
    print_colored(f"Exécution du script dans l'environnement '{venv_name}'...", "blue")
    
    if system == "Windows":
        # Sur Windows, utiliser une approche différente
        return subprocess.call(cmd, shell=True)
    else:
        # Sur Unix, utiliser une approche standard
        return os.system(cmd)

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
    print_colored(f"Système d'exploitation détecté: {system}", "blue")
    
    # Nom de l'environnement virtuel
    venv_name = "tetris_env"
    
    # Vérifier si nous sommes dans un environnement virtuel
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print_colored("Pas dans un environnement virtuel.", "yellow")
        
        # Vérifier si l'environnement virtuel existe déjà
        if not check_venv_exists(venv_name):
            print_colored(f"L'environnement '{venv_name}' n'existe pas, création...", "yellow")
            if not create_venv(venv_name):
                print_colored("Échec de la création de l'environnement virtuel.", "red")
                return False
        
        # Exécuter ce script dans l'environnement virtuel
        print_colored(f"Exécution du script dans l'environnement '{venv_name}'...", "yellow")
        exit_code = run_in_venv(venv_name, __file__)
        
        # Le script a été réexécuté dans l'environnement virtuel, donc sortir
        sys.exit(exit_code)
    
    print_colored("Dans un environnement virtuel.", "green")
    
    # Installer les dépendances
    # Sur Windows, pip est généralement dans le dossier Scripts
    if system == "Windows":
        pip_cmd = os.path.join(sys.prefix, "Scripts", "pip")
        if not os.path.exists(pip_cmd + ".exe"):
            pip_cmd = "pip"  # Fallback au pip du PATH
    else:
        pip_cmd = os.path.join(sys.prefix, "bin", "pip")
        if not os.path.exists(pip_cmd):
            pip_cmd = "pip"  # Fallback au pip du PATH
            
    # Installer les dépendances
    install_cmd = f'"{pip_cmd}" install -r requirements.txt'
    if not run_command(install_cmd, "Installation des dépendances..."):
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
    
    # Déterminer la commande pytest selon la plateforme
    if platform.system() == "Windows":
        pytest_cmd = os.path.join(sys.prefix, "Scripts", "pytest.exe")
        if not os.path.exists(pytest_cmd):
            pytest_cmd = "pytest"  # Fallback
    else:
        pytest_cmd = os.path.join(sys.prefix, "bin", "pytest")
        if not os.path.exists(pytest_cmd):
            pytest_cmd = "pytest"  # Fallback
    
    return run_command(f'"{pytest_cmd}" test_tetris.py -v', "Exécution des tests...", "Certains tests ont échoué.")

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
    
    # Déterminer la commande Python selon la plateforme
    system = platform.system()
    if system == "Windows":
        python_cmd = os.path.join(sys.prefix, "python.exe")
        if not os.path.exists(python_cmd):
            python_cmd = "python"  # Fallback
    else:
        python_cmd = os.path.join(sys.prefix, "bin", "python")
        if not os.path.exists(python_cmd):
            python_cmd = "python3"  # Fallback
    
    # Lancer le jeu
    try:
        # Vérifier si home_screen.py existe, sinon lancer main.py
        if os.path.exists("home_screen.py"):
            script = "home_screen.py"
        else:
            script = "main.py"
            
        cmd = f'"{python_cmd}" {script}'
        print_colored(f"Lancement de {script}...", "green")
        
        if system == "Windows":
            # Sur Windows, utiliser subprocess pour mieux gérer les fenêtres Pygame
            return subprocess.call(cmd, shell=True) == 0
        else:
            # Sur Unix, utiliser os.system
            return os.system(cmd) == 0
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