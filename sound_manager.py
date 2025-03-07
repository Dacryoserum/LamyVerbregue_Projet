import pygame
import os

# =============================================================================
# Classe SoundManager (gestionnaire de son pour le jeu Tetris)
# =============================================================================
class SoundManager:
    """Gestionnaire de son pour le jeu Tetris"""
    
    # Instance unique pour le pattern Singleton
    _instance = None
    
    def __new__(cls):
        """
        Implémentation du pattern Singleton pour s'assurer qu'une seule instance existe.
        Cela permet de maintenir un état cohérent du son dans toute l'application.
        
        :return: L'instance unique de SoundManager.
        """
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """
        Initialise le gestionnaire de son (une seule fois).
        Cette méthode ne s'exécute qu'une seule fois grâce au pattern Singleton,
        même si plusieurs instances sont créées.
        """
        # Si déjà initialisé, ne rien faire
        if self._initialized:
            return
            
        # Initialisation du mixer audio de Pygame si pas déjà fait
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Définition des chemins vers les fichiers audio
        sounds_dir = 'sound'
        self.music_path = os.path.join(sounds_dir, 'tetris_theme.mp3')
        
        # Dictionnaire pour stocker les effets sonores (son → objet Sound)
        self.sound_effects = {}
        
        # Chargement des effets sonores
        self._load_sound_effects()
        
        # État initial du son
        self.music_playing = False  # Indique si la musique est en cours de lecture
        self.sound_enabled = True   # Indique si les effets sonores sont activés
        
        # Marquer comme initialisé
        self._initialized = True
    
    def _load_sound_effects(self):
        """
        Charge les effets sonores dans le dictionnaire.
        Cette méthode privée est appelée lors de l'initialisation
        et recherche les fichiers audio dans le dossier 'sound'.
        """
        try:
            # Définir les chemins des effets sonores
            sounds_dir = 'sound'
            sound_files = {
                'line_clear': os.path.join(sounds_dir, 'line_complete.mp3'),
                'piece_drop': os.path.join(sounds_dir, 'piece.mp3')
            }
            
            # Charger chaque effet sonore s'il existe
            for name, path in sound_files.items():
                if os.path.exists(path):
                    self.sound_effects[name] = pygame.mixer.Sound(path)
                else:
                    print(f"Attention: Le fichier son '{path}' n'existe pas.")
        except Exception as e:
            print(f"Erreur lors du chargement des effets sonores: {e}")
    
    def play_music(self):
        """
        Démarre la musique en boucle.
        Charge le fichier de musique de fond et le joue en boucle infinie.
        Met à jour l'état de lecture de la musique.
        """
        if not self.music_playing:
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(loops=-1)  # Joue la musique en boucle infinie
                self.music_playing = True
            except Exception as e:
                print(f"Erreur lors du chargement de la musique: {e}")
    
    def stop_music(self):
        """
        Arrête la musique.
        Arrête complètement la lecture de la musique de fond
        et met à jour l'état de lecture.
        """
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def pause_music(self):
        """
        Met la musique en pause.
        Suspend temporairement la lecture de la musique
        sans changer le point de lecture.
        """
        if self.music_playing:
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """
        Reprend la musique après une pause.
        Reprend la lecture de la musique à partir du point
        où elle a été mise en pause.
        """
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        """
        Règle le volume de la musique (entre 0.0 et 1.0).
        
        :param volume: Niveau de volume entre 0.0 (silencieux) et 1.0 (maximum).
        """
        pygame.mixer.music.set_volume(volume)
    
    def play_sound(self, sound_name):
        """
        Joue un effet sonore par son nom.
        
        :param sound_name: Nom de l'effet sonore à jouer (clé dans le dictionnaire sound_effects).
        """
        if self.sound_enabled and sound_name in self.sound_effects:
            try:
                self.sound_effects[sound_name].play()
            except Exception as e:
                print(f"Erreur lors de la lecture de l'effet sonore '{sound_name}': {e}")
    
    def set_sound_volume(self, sound_name, volume):
        """
        Règle le volume d'un effet sonore spécifique (entre 0.0 et 1.0).
        
        :param sound_name: Nom de l'effet sonore à modifier.
        :param volume: Niveau de volume entre 0.0 (silencieux) et 1.0 (maximum).
        """
        if sound_name in self.sound_effects:
            self.sound_effects[sound_name].set_volume(volume)
    
    def enable_sounds(self, enabled=True):
        """
        Active ou désactive les effets sonores.
        
        :param enabled: True pour activer les sons, False pour les désactiver.
        """
        self.sound_enabled = enabled