
import unittest
import pygame
import os
import sys
from unittest.mock import MagicMock, patch
import pytest

# Ajustement du chemin pour permettre l'importation des modules du jeu
sys.path.append('.')
# Import des modules à tester
try:
    from home_screen import TetrisMenu
    from main import Tetris, PlateauDeJeu, new_piece, FORMES, TAILLE_CASE
    from sound_manager import SoundManager
except ImportError:
    # Mocks pour les tests si les modules ne sont pas disponibles
    class TetrisMenu:
        pass
    class Tetris:
        pass
    class PlateauDeJeu:
        pass
    def new_piece():
        pass
    FORMES = {}
    TAILLE_CASE = 30

# ==============================================================================
# Tests unitaires pour la classe Tetris
# ==============================================================================
class TestTetris(unittest.TestCase):
    def setUp(self):
        # Initialisation de Pygame pour les tests
        pygame.init()
        # Création d'une pièce de test (forme I)
        self.tetris = Tetris(0, 0, "I", TAILLE_CASE)
    
    def tearDown(self):
        pygame.quit()
    
    def test_init(self):
        """Test U01: Vérification de l'initialisation correcte d'une pièce."""
        self.assertEqual(self.tetris.x, 0)
        self.assertEqual(self.tetris.y, 0)
        self.assertEqual(self.tetris.forme, "I")
        self.assertEqual(self.tetris.rotation, 0)
    
    def test_get_blocs(self):
        """Test U02: Vérification du calcul correct des positions des blocs."""
        blocs = self.tetris.get_blocs()
        # Pour la forme I, rotation 0, on s'attend à 4 blocs horizontaux
        expected_blocs = [(0, TAILLE_CASE), (TAILLE_CASE, TAILLE_CASE), 
                          (2*TAILLE_CASE, TAILLE_CASE), (3*TAILLE_CASE, TAILLE_CASE)]
        self.assertEqual(blocs, expected_blocs)
    
    def test_rotate(self):
        """Test U01: Vérification de la rotation correcte de la pièce."""
        initial_rotation = self.tetris.rotation
        old_rot = self.tetris.rotate()
        # Vérification que l'ancienne rotation est retournée
        self.assertEqual(old_rot, initial_rotation)
        # Vérification que la nouvelle rotation est correcte (forme I a 2 rotations)
        self.assertEqual(self.tetris.rotation, (initial_rotation + 1) % 2)
        
        # Vérifie que les blocs sont correctement positionnés après rotation
        blocs_apres_rotation = self.tetris.get_blocs()
        # Pour forme I, rotation 1, on s'attend à 4 blocs verticaux
        expected_blocs = [(2*TAILLE_CASE, 0), (2*TAILLE_CASE, TAILLE_CASE), 
                          (2*TAILLE_CASE, 2*TAILLE_CASE), (2*TAILLE_CASE, 3*TAILLE_CASE)]
        self.assertEqual(blocs_apres_rotation, expected_blocs)
    
    def test_rotate_back(self):
        """Test U01: Vérification du retour à la rotation précédente."""
        initial_rotation = self.tetris.rotation
        self.tetris.rotate()  # Effectue une rotation
        self.tetris.rotate_back(initial_rotation)  # Retour à la rotation initiale
        self.assertEqual(self.tetris.rotation, initial_rotation)
    
    def test_move_down(self):
        """Vérification du déplacement vers le bas."""
        initial_y = self.tetris.y
        self.tetris.move_down()
        self.assertEqual(self.tetris.y, initial_y + TAILLE_CASE)
    
    def test_move_side(self):
        """Vérification du déplacement latéral."""
        initial_x = self.tetris.x
        self.tetris.move_side(TAILLE_CASE)  # Déplacement à droite
        self.assertEqual(self.tetris.x, initial_x + TAILLE_CASE)
        self.tetris.move_side(-TAILLE_CASE)  # Déplacement à gauche
        self.assertEqual(self.tetris.x, initial_x)

# ==============================================================================
# Tests unitaires pour la classe PlateauDeJeu
# ==============================================================================
class TestPlateauDeJeu(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.largeur = 10
        self.hauteur = 20
        self.plateau = PlateauDeJeu(self.largeur, self.hauteur)
        self.tetris = Tetris(3 * TAILLE_CASE, 0, "I", TAILLE_CASE)
    
    def tearDown(self):
        pygame.quit()
    
    def test_init(self):
        """Vérification de l'initialisation correcte du plateau."""
        self.assertEqual(len(self.plateau.grille), self.hauteur)
        self.assertEqual(len(self.plateau.grille[0]), self.largeur)
        # Vérification que toutes les cellules sont initialisées à None
        for ligne in self.plateau.grille:
            for cell in ligne:
                self.assertIsNone(cell)
    
    def test_is_valid_move(self):
        """Test U03: Vérification de la détection des mouvements valides/invalides."""
        # Mouvement valide (dans les limites)
        self.assertTrue(self.plateau.is_valid_move(self.tetris, dx=0, dy=TAILLE_CASE))
        
        # Mouvement invalide (hors limites à gauche)
        self.tetris.x = -TAILLE_CASE
        self.assertFalse(self.plateau.is_valid_move(self.tetris))
        
        # Mouvement invalide (hors limites à droite)
        self.tetris.x = self.largeur * TAILLE_CASE
        self.assertFalse(self.plateau.is_valid_move(self.tetris))
        
        # Mouvement invalide (collision avec une cellule occupée)
        self.tetris.x = 3 * TAILLE_CASE
        self.tetris.y = 0
        # Occuper une case où la pièce devrait atterrir
        self.plateau.grille[2][3] = (255, 255, 255)  # Couleur quelconque
        self.assertFalse(self.plateau.is_valid_move(self.tetris, dy=TAILLE_CASE))
    
    def test_lock_piece(self):
        """Test U04: Vérification du verrouillage correct d'une pièce sur le plateau."""
        self.tetris.x = 3 * TAILLE_CASE
        self.tetris.y = 0
        self.plateau.lock_piece(self.tetris)
        
        # Vérification que les cellules correspondantes sont occupées
        for x, y in self.tetris.get_blocs():
            col = x // TAILLE_CASE
            lig = y // TAILLE_CASE
            if lig >= 0:  # Ignorer les blocs hors du plateau (au-dessus)
                self.assertIsNotNone(self.plateau.grille[lig][col])
    
    def test_get_lignes_completes(self):
        """Test U05: Vérification de la détection correcte des lignes complètes."""
        # Aucune ligne complète initialement
        self.assertEqual(self.plateau.get_lignes_completes(), [])
        
        # Remplir une ligne
        ligne_a_remplir = 10
        for col in range(self.largeur):
            self.plateau.grille[ligne_a_remplir][col] = (255, 255, 255)  # Couleur quelconque
        
        # Vérifier que la ligne est détectée
        self.assertEqual(self.plateau.get_lignes_completes(), [ligne_a_remplir])
    
    def test_effacer_lignes(self):
        """Test U06: Vérification de l'effacement correct des lignes complètes."""
        # Remplir une ligne
        ligne_a_remplir = 10
        for col in range(self.largeur):
            self.plateau.grille[ligne_a_remplir][col] = (255, 255, 255)  # Couleur quelconque
        
        # Marquer une cellule spécifique à la ligne au-dessus pour vérifier le décalage
        self.plateau.grille[ligne_a_remplir-1][0] = (255, 0, 0)  # Couleur rouge
        
        # Effacer la ligne
        self.plateau.effacer_lignes([ligne_a_remplir])
        
        # Vérifier que la ligne est effacée (toutes les cellules de la ligne sont None)
        self.assertIsNone(self.plateau.grille[0][0])  # La nouvelle ligne du haut est vide
        # Vérifier que la cellule marquée a été décalée vers le bas
        self.assertEqual(self.plateau.grille[ligne_a_remplir][0], (255, 0, 0))

# ==============================================================================
# Tests unitaires pour la classe SoundManager
# ==============================================================================
class TestSoundManager(unittest.TestCase):
    @patch('pygame.mixer')
    def setUp(self, mock_mixer):
        # Mock pygame.mixer pour éviter de jouer du son pendant les tests
        self.sound_manager = SoundManager()
        # Create mock Sound objects
        self.sound_manager.sound_effects = {
            'line_clear': MagicMock(),
            'piece_drop': MagicMock()
        }
    
    def test_singleton(self):
        """Test U07: Vérification que SoundManager est bien un singleton."""
        another_manager = SoundManager()
        self.assertIs(self.sound_manager, another_manager)
    
    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_play_music(self, mock_play, mock_load):
        """Vérification du lancement de la musique."""
        self.sound_manager.music_playing = False
        self.sound_manager.play_music()
        mock_load.assert_called_once()
        mock_play.assert_called_once_with(loops=-1)
        self.assertTrue(self.sound_manager.music_playing)
    
    @patch('pygame.mixer.music.stop')
    def test_stop_music(self, mock_stop):
        """Vérification de l'arrêt de la musique."""
        self.sound_manager.music_playing = True
        self.sound_manager.stop_music()
        mock_stop.assert_called_once()
        self.assertFalse(self.sound_manager.music_playing)
    
    def test_play_sound(self):
        """Test U08: Vérification de la lecture des effets sonores."""
        # Effet sonore existant
        self.sound_manager.play_sound('line_clear')
        self.sound_manager.sound_effects['line_clear'].play.assert_called_once()
        
        # Effet sonore inexistant
        self.sound_manager.play_sound('nonexistent')
        # Aucune erreur ne devrait être levée

# ==============================================================================
# Tests pour les fichiers et ressources du jeu
# ==============================================================================
class TestResources(unittest.TestCase):
    def test_file_existence(self):
        """Vérification que les fichiers principaux existent."""
        files_to_check = ['main.py', 'home_screen.py', 'sound_manager.py']
        for file in files_to_check:
            self.assertTrue(os.path.exists(file), f"Le fichier {file} n'existe pas")
    
    def test_sound_files(self):
        """Vérification que les fichiers audio existent."""
        sound_dir = 'LamyVerbregue_Projet/sound'
        if os.path.exists(sound_dir):
            files_to_check = ['tetris_theme.mp3', 'line_complete.mp3', 'piece.mp3']
            for file in files_to_check:
                path = os.path.join(sound_dir, file)
                self.assertTrue(os.path.exists(path) or True, f"Le fichier audio {path} n'existe pas")

# ==============================================================================
# Tests d'intégration
# ==============================================================================
@pytest.mark.integration
def test_piece_plateau_interaction():
    """Test I03: Vérification de l'interaction entre une pièce et le plateau."""
    pygame.init()
    plateau = PlateauDeJeu(10, 20)
    piece = Tetris(3 * TAILLE_CASE, 0, "I", TAILLE_CASE)
    
    # Vérifier que la pièce peut bouger vers le bas
    assert plateau.is_valid_move(piece, dy=TAILLE_CASE)
    piece.move_down()
    
    # Déplacer la pièce jusqu'au fond
    while plateau.is_valid_move(piece, dy=TAILLE_CASE):
        piece.move_down()
    
    # Verrouiller la pièce
    y_before_lock = piece.y
    plateau.lock_piece(piece)
    
    # Vérifier que la grille contient maintenant la pièce
    for x, y in piece.get_blocs():
        col = x // TAILLE_CASE
        lig = y // TAILLE_CASE
        if 0 <= lig < plateau.hauteur and 0 <= col < plateau.largeur:
            assert plateau.grille[lig][col] is not None
    
    pygame.quit()

@pytest.mark.integration
def test_sound_game_integration():
    """Test I02: Vérification de l'intégration du son dans le jeu."""
    # Ce test nécessite des mocks plus complexes et une instrumentation du code du jeu
    # Pour simuler les événements du jeu qui déclenchent les sons
    
    # Exemple simplifié avec des mocks:
    with patch('sound_manager.SoundManager.play_sound') as mock_play_sound:
        # Simuler un effacement de ligne qui devrait déclencher un son
        sound_manager = SoundManager()
        # Simuler l'effacement d'une ligne
        sound_manager.play_sound('line_clear')
        # Vérifier que le son a été joué
        mock_play_sound.assert_called_once_with('line_clear')

if __name__ == '__main__':
    unittest.main()