import pygame
import sys

# =============================================================================
# Classe TetrisMenu (représente l'écran d'accueil du jeu)
# =============================================================================
class TetrisMenu:
    def __init__(self):
        """
        Initialise l'écran d'accueil du jeu Tetris.
        Configure la fenêtre, les polices et l'horloge pour limiter le taux de rafraîchissement.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))  # Fenêtre de 400x600 pixels
        pygame.display.set_caption('Tetris Menu')          # Titre de la fenêtre
        self.font = pygame.font.Font(None, 50)             # Police par défaut, taille 50
        self.clock = pygame.time.Clock()                   # Horloge pour limiter les FPS

    def draw_button(self, text, y_pos, is_hover):
        """
        Dessine un bouton avec effet de survol sur l'écran.
        
        :param text: Texte à afficher sur le bouton.
        :param y_pos: Position verticale du centre du bouton.
        :param is_hover: Indique si la souris survole le bouton (change la couleur).
        :return: Objet Rect représentant le bouton (utilisé pour les interactions).
        """
        # Couleur verte plus claire si survol, plus foncée sinon
        color = (100, 200, 100) if is_hover else (50, 150, 50)
        
        # Création du texte rendu avec la police définie
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(200, y_pos))
        
        # Création du rectangle du bouton (largeur 200, hauteur 50)
        button_rect = pygame.Rect(100, y_pos - 25, 200, 50)
        
        # Dessin du bouton avec des coins arrondis
        pygame.draw.rect(self.screen, color, button_rect, border_radius=10)
        
        # Affichage du texte centré sur le bouton
        self.screen.blit(text_surface, text_rect)
        
        return button_rect

    def run(self):
        """
        Boucle principale de l'écran d'accueil.
        Gère l'affichage, les événements et les interactions avec les boutons.
        Permet de lancer le jeu ou de quitter l'application.
        """
        running = True          # Contrôle de la boucle principale
        start_hover = False     # État de survol du bouton Start
        quit_hover = False      # État de survol du bouton Quit
        
        # Création initiale des boutons avant la boucle d'événements
        start_button = self.draw_button('Start', 300, start_hover)
        quit_button = self.draw_button('Quit', 400, quit_hover)
        
        # Boucle principale
        while running:
            self.screen.fill((0, 0, 0))  # Remplissage de l'écran avec la couleur noire
            
            # Affichage du titre "TETRIS"
            title = self.font.render('TETRIS', True, (255, 255, 255))
            title_rect = title.get_rect(center=(200, 100))
            self.screen.blit(title, title_rect)
            
            # =============================================================================
            # Traitement des événements
            # =============================================================================
            for event in pygame.event.get():
                # Gestion de la fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    running = False
                
                # Gestion du mouvement de la souris (pour effet de survol)
                if event.type == pygame.MOUSEMOTION:
                    start_hover = start_button.collidepoint(event.pos)
                    quit_hover = quit_button.collidepoint(event.pos)
                
                # Gestion des clics de souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Clic sur le bouton Start
                    if start_button.collidepoint(event.pos):
                        pygame.display.quit()  # Ferme la fenêtre du menu
                        # Import et exécution directs du jeu principal
                        import main
                        main.main()  # Lance le jeu
                        sys.exit()   # Quitte le programme après la partie
                    
                    # Clic sur le bouton Quit
                    if quit_button.collidepoint(event.pos):
                        running = False
            
            # Redessine les boutons avec l'état de survol actuel
            start_button = self.draw_button('Start', 300, start_hover)
            quit_button = self.draw_button('Quit', 400, quit_hover)
            
            # Mise à jour de l'affichage
            pygame.display.flip()
            
            # Limitation à 60 images par seconde
            self.clock.tick(60)
        
        # Nettoyage et sortie
        pygame.quit()
        sys.exit()

# =============================================================================
# Point d'entrée du programme
# =============================================================================
def main():
    """
    Fonction principale qui initialise et exécute le menu du jeu Tetris.
    """
    menu = TetrisMenu()
    menu.run()

if __name__ == "__main__":
    main()