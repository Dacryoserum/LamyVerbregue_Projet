import pygame
import sys

class TetrisMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption('Tetris Menu')
        self.font = pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()

    def draw_button(self, text, y_pos, is_hover):
        color = (100, 200, 100) if is_hover else (50, 150, 50)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(200, y_pos))
        button_rect = pygame.Rect(100, y_pos - 25, 200, 50)
        
        pygame.draw.rect(self.screen, color, button_rect, border_radius=10)
        self.screen.blit(text_surface, text_rect)
        return button_rect

    def run(self):
        running = True
        start_hover = False
        quit_hover = False

        # Initial button creation before the event loop
        start_button = self.draw_button('Start', 300, start_hover)
        quit_button = self.draw_button('Quit', 400, quit_hover)

        while running:
            self.screen.fill((0, 0, 0))
            
            # Title
            title = self.font.render('TETRIS', True, (255, 255, 255))
            title_rect = title.get_rect(center=(200, 100))
            self.screen.blit(title, title_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEMOTION:
                    start_hover = start_button.collidepoint(event.pos)
                    quit_hover = quit_button.collidepoint(event.pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        pygame.display.quit()
                        # Direct import and execution of main game
                        import main
                        main.main()
                        sys.exit()
                    
                    if quit_button.collidepoint(event.pos):
                        running = False

            # Redraw buttons with current hover state
            start_button = self.draw_button('Start', 300, start_hover)
            quit_button = self.draw_button('Quit', 400, quit_hover)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

def main():
    menu = TetrisMenu()
    menu.run()

if __name__ == "__main__":
    main()