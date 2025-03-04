import pygame

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
            pygame.mixer.init()
        
        # Chemin vers les fichiers audio
        self.music_path = 'LamyVerbregue_Projet/tetris_theme.mp3'
        
        # État du son
        self.music_playing = False
        
        self._initialized = True
    
    def play_music(self):
        """Démarre la musique en boucle"""
        if not self.music_playing:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(loops=-1)  # Joue la musique en boucle infinie
            self.music_playing = True
    
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