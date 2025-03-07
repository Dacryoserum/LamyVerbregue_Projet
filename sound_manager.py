import pygame
import os

class SoundManager:
    """Gestionnaire de son pour le jeu Tetris"""
    
    _instance = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton pour s'assurer qu'une seule instance existe"""
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialise le gestionnaire de son (une seule fois)"""
        if self._initialized:
            return
            
        # Initialisation du mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Chemins vers les fichiers audio
        self.music_path = 'LamyVerbregue_Projet/sound/tetris_theme.mp3'
        
        # Dictionnaire pour stocker les effets sonores
        self.sound_effects = {}
        
        # Charger les effets sonores
        self._load_sound_effects()
        
        # État du son
        self.music_playing = False
        self.sound_enabled = True
        
        self._initialized = True
    
    def _load_sound_effects(self):
        """Charge les effets sonores dans le dictionnaire"""
        try:
            # Créer le dossier des sons s'il n'existe pas
            sounds_dir = 'LamyVerbregue_Projet/sound'
            if not os.path.exists(sounds_dir):
                os.makedirs(sounds_dir)
                
            # Définir les chemins des effets sonores
            sound_files = {
                'line_clear': os.path.join(sounds_dir, 'line_complete.mp3'),
                'piece_drop': os.path.join(sounds_dir, 'piece.mp3')
            }
            
            # Charger chaque effet sonore
            for name, path in sound_files.items():
                if os.path.exists(path):
                    self.sound_effects[name] = pygame.mixer.Sound(path)
                else:
                    print(f"Attention: Le fichier son '{path}' n'existe pas.")
        except Exception as e:
            print(f"Erreur lors du chargement des effets sonores: {e}")
    
    def play_music(self):
        """Démarre la musique en boucle"""
        if not self.music_playing:
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(loops=-1)  # Joue la musique en boucle infinie
                self.music_playing = True
            except Exception as e:
                print(f"Erreur lors du chargement de la musique: {e}")
    
    def stop_music(self):
        """Arrête la musique"""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def pause_music(self):
        """Met la musique en pause"""
        if self.music_playing:
            pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Reprend la musique après une pause"""
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        """Règle le volume de la musique (entre 0.0 et 1.0)"""
        pygame.mixer.music.set_volume(volume)
    
    def play_sound(self, sound_name):
        """Joue un effet sonore par son nom"""
        if self.sound_enabled and sound_name in self.sound_effects:
            try:
                self.sound_effects[sound_name].play()
            except Exception as e:
                print(f"Erreur lors de la lecture de l'effet sonore '{sound_name}': {e}")
    
    def set_sound_volume(self, sound_name, volume):
        """Règle le volume d'un effet sonore spécifique (entre 0.0 et 1.0)"""
        if sound_name in self.sound_effects:
            self.sound_effects[sound_name].set_volume(volume)
    
    def enable_sounds(self, enabled=True):
        """Active ou désactive les effets sonores"""
        self.sound_enabled = enabled