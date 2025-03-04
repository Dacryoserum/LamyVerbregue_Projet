import pygame
import random
import sys
from sound_manager import SoundManager

print("Démarrage du programme...")
import pygame
print("Pygame importé avec succès")


# etc...
# =============================================================================
# Configuration générale du jeu
# =============================================================================

# Dimensions de la fenêtre (zone de jeu + panneau latéral)
LARGEUR_FENETRE = 500      # Largeur totale de la fenêtre en pixels
HAUTEUR_FENETRE = 600      # Hauteur totale de la fenêtre en pixels

# Dimensions de la grille de jeu
TAILLE_CASE = 30           # Taille d'une case en pixels
LARGEUR_JEU = 300          # Largeur de la zone de jeu (partie de la fenêtre dédiée au jeu)
NB_COLONNES = LARGEUR_JEU // TAILLE_CASE   # Nombre de colonnes de la grille
NB_LIGNES = HAUTEUR_FENETRE // TAILLE_CASE    # Nombre de lignes de la grille

# =============================================================================
# Définition des couleurs (format RGB)
# =============================================================================
GRIS = (30, 30, 30)        # Couleur de fond principale
GRIS_CLAIR = (60, 60, 60)   # Couleur utilisée pour dessiner les lignes de la grille et les encadrements
BLANC = (255, 255, 255)     # Couleur blanche (utilisée pour l'animation flash)
NOIR = (0, 0, 0)           # Couleur noire (utilisée pour les contours)

# =============================================================================
# Définition des couleurs associées à chaque type de pièce
# =============================================================================
CARTE_COULEURS = {
    "I": (0, 255, 255),    # Cyan
    "J": (0, 0, 255),      # Bleu
    "L": (255, 165, 0),    # Orange
    "O": (255, 255, 0),    # Jaune
    "S": (0, 255, 0),      # Vert
    "T": (128, 0, 128),    # Violet
    "Z": (255, 0, 0)       # Rouge
}

# =============================================================================
# Définition des formes et de leurs rotations
#
# Chaque pièce est définie par une liste de rotations.
# Chaque rotation est une liste de tuples (dx, dy) exprimés en nombre de cases.
# =============================================================================
FORMES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)]
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)]
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)]
    ],
    "O": [
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)]
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)]
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)]
    ]
}

# =============================================================================
# Configuration du rythme de chute et de l'animation d'effacement
# =============================================================================
VITESSE_CHUTE_INIT = 500      # Temps en millisecondes avant que la pièce ne descende d'une case
DUREE_ANIMATION_LIGNE = 500   # Durée de l'animation (flash) lors de l'effacement d'une ligne

# =============================================================================
# Classe Tetris (représente une pièce)
# =============================================================================
class Tetris:
    def __init__(self, x, y, forme, taille_case):
        """
        Initialise une pièce de Tetris.

        :param x: Position x (en pixels) du coin supérieur gauche de la pièce.
        :param y: Position y (en pixels) du coin supérieur gauche de la pièce.
        :param forme: Identifiant de la forme ("I", "J", "L", "O", "S", "T", "Z").
        :param taille_case: Taille d'une case en pixels.
        """
        self.x = x
        self.y = y
        self.forme = forme
        self.couleur = CARTE_COULEURS[forme]
        self.taille_case = taille_case
        self.rotation = 0

    def get_blocs(self):
        """
        Calcule et retourne la liste des positions (en pixels) de chaque bloc constituant la pièce.
        Chaque position est calculée en fonction de la rotation actuelle.
        """
        blocs = []
        for dx, dy in FORMES[self.forme][self.rotation]:
            blocs.append((self.x + dx * self.taille_case, self.y + dy * self.taille_case))
        return blocs

    def move_down(self):
        """Déplace la pièce d'une case vers le bas."""
        self.y += self.taille_case

    def move_side(self, dx):
        """
        Déplace la pièce horizontalement.

        :param dx: Décalage en pixels (positif vers la droite, négatif vers la gauche).
        """
        self.x += dx

    def rotate(self):
        """
        Effectue une rotation de la pièce dans le sens horaire.
        Retourne la rotation précédente pour permettre une annulation si nécessaire.
        """
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(FORMES[self.forme])
        return old_rotation

    def rotate_back(self, old_rotation):
        """
        Annule la rotation en rétablissant l'ancienne valeur de rotation.
        
        :param old_rotation: La valeur de rotation à restaurer.
        """
        self.rotation = old_rotation

    def draw(self, surface):
        """
        Dessine la pièce sur la surface donnée.

        :param surface: Surface Pygame sur laquelle dessiner la pièce.
        """
        for x_bloc, y_bloc in self.get_blocs():
            rect = pygame.Rect(x_bloc, y_bloc, self.taille_case, self.taille_case)
            pygame.draw.rect(surface, self.couleur, rect)
            # Dessine un contour pour mieux visualiser les blocs
            pygame.draw.rect(surface, NOIR, rect, 1)

# =============================================================================
# Classe PlateauDeJeu (représente la grille de jeu)
# =============================================================================
class PlateauDeJeu:
    def __init__(self, largeur, hauteur):
        """
        Initialise le plateau de jeu avec une grille vide.

        :param largeur: Nombre de colonnes de la grille.
        :param hauteur: Nombre de lignes de la grille.
        """
        self.largeur = largeur
        self.hauteur = hauteur
        # La grille est une liste de listes contenant None (case vide) ou une couleur (case occupée)
        self.grille = [[None for _ in range(largeur)] for _ in range(hauteur)]

    def is_valid_move(self, tetris, dx=0, dy=0):
        """
        Vérifie si le déplacement de la pièce (définie par dx et dy) est valide.
        Le déplacement est invalide si la pièce sort de la grille ou entre en collision avec une case déjà occupée.

        :param tetris: Instance de Tetris représentant la pièce à déplacer.
        :param dx: Décalage horizontal (en pixels).
        :param dy: Décalage vertical (en pixels).
        :return: True si le mouvement est valide, False sinon.
        """
        for x, y in tetris.get_blocs():
            new_x = x + dx
            new_y = y + dy
            col = new_x // TAILLE_CASE
            lig = new_y // TAILLE_CASE
            if col < 0 or col >= self.largeur or lig >= self.hauteur:
                return False
            if lig >= 0 and self.grille[lig][col] is not None:
                return False
        return True

    def lock_piece(self, tetris):
        """
        Verrouille la pièce en ajoutant ses blocs à la grille.
        Cette opération est effectuée lorsque la pièce ne peut plus descendre.

        :param tetris: Instance de Tetris à verrouiller.
        """
        for x, y in tetris.get_blocs():
            col = x // TAILLE_CASE
            lig = y // TAILLE_CASE
            if lig >= 0:
                self.grille[lig][col] = tetris.couleur

    def get_lignes_completes(self):
        """
        Identifie et retourne une liste des indices de lignes entièrement remplies.

        :return: Liste d'indices de lignes complètes.
        """
        lignes = []
        for i, ligne in enumerate(self.grille):
            if all(cell is not None for cell in ligne):
                lignes.append(i)
        return lignes

    def effacer_lignes(self, indices_lignes):
        """
        Supprime les lignes spécifiées par leurs indices, puis ajoute en haut des lignes vides
        afin de maintenir la taille de la grille.

        :param indices_lignes: Liste d'indices des lignes à effacer.
        """
        for lig in sorted(indices_lignes):
            # Supprime la ligne complète
            del self.grille[lig]
            # Insère une nouvelle ligne vide en haut de la grille
            self.grille.insert(0, [None for _ in range(self.largeur)])

    def clear_lines(self):
        """
        Alternative d'effacement des lignes complètes en réassemblant la grille.
        Retourne le nombre de lignes effacées.

        :return: Nombre de lignes effacées.
        """
        lignes_cleared = 0
        nouvelle_grille = [ligne for ligne in self.grille if any(cell is None for cell in ligne)]
        lignes_cleared = self.hauteur - len(nouvelle_grille)
        for _ in range(lignes_cleared):
            nouvelle_grille.insert(0, [None for _ in range(self.largeur)])
        self.grille = nouvelle_grille
        return lignes_cleared

    def draw(self, surface, lignes_animation=None):
        """
        Dessine la grille (les blocs déjà placés) sur la surface donnée.
        Si des lignes sont en cours d'animation d'effacement, celles-ci sont dessinées avec un effet flash.

        :param surface: Surface Pygame sur laquelle dessiner la grille.
        :param lignes_animation: Liste d'indices de lignes à animer (optionnel).
        """
        temps = pygame.time.get_ticks()
        for lig in range(self.hauteur):
            for col in range(self.largeur):
                couleur = self.grille[lig][col]
                if couleur is not None:
                    # Si la ligne fait partie de l'animation, on alterne entre BLANC et la couleur d'origine
                    if lignes_animation is not None and lig in lignes_animation:
                        if (temps // 150) % 2 == 0:
                            couleur_affiche = BLANC
                        else:
                            couleur_affiche = couleur
                    else:
                        couleur_affiche = couleur
                    rect = pygame.Rect(col * TAILLE_CASE, lig * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                    pygame.draw.rect(surface, couleur_affiche, rect)
                    pygame.draw.rect(surface, NOIR, rect, 1)

# =============================================================================
# Fonctions de dessin et d'affichage du panneau latéral
# =============================================================================
def draw_grid(surface):
    """
    Dessine les lignes de la grille de la zone de jeu.
    
    :param surface: Surface Pygame sur laquelle dessiner la grille.
    """
    for y in range(NB_LIGNES):
        pygame.draw.line(surface, GRIS_CLAIR, (0, y * TAILLE_CASE), (LARGEUR_JEU, y * TAILLE_CASE))
    for x in range(NB_COLONNES):
        pygame.draw.line(surface, GRIS_CLAIR, (x * TAILLE_CASE, 0), (x * TAILLE_CASE, HAUTEUR_FENETRE))

def new_piece():
    """
    Crée et retourne une nouvelle pièce placée en haut de la zone de jeu et centrée horizontalement.
    
    :return: Instance de Tetris représentant la nouvelle pièce.
    """
    forme = random.choice(list(FORMES.keys()))
    x = LARGEUR_JEU // 2 - 2 * TAILLE_CASE  # Centrage approximatif de la pièce
    y = 0
    return Tetris(x, y, forme, TAILLE_CASE)

def draw_next_piece(surface, piece):
    """
    Affiche un encadré de prévisualisation de la prochaine pièce dans le panneau latéral.
    
    :param surface: Surface Pygame sur laquelle dessiner la prévisualisation.
    :param piece: Instance de Tetris représentant la prochaine pièce.
    """
    preview_x = LARGEUR_JEU + 50
    preview_y = 50
    # Dessine l'encadré de prévisualisation
    pygame.draw.rect(surface, GRIS_CLAIR, (preview_x - 10, preview_y - 10, 120, 120), 2)
    # Calcul pour centrer la pièce dans l'encadré :
    blocs = FORMES[piece.forme][piece.rotation]
    min_x = min(dx for dx, _ in blocs)
    min_y = min(dy for _, dy in blocs)
    max_x = max(dx for dx, _ in blocs)
    max_y = max(dy for _, dy in blocs)
    largeur_piece = (max_x - min_x + 1) * TAILLE_CASE
    hauteur_piece = (max_y - min_y + 1) * TAILLE_CASE
    offset_x = preview_x + (120 - largeur_piece) // 2 - min_x * TAILLE_CASE
    offset_y = preview_y + (120 - hauteur_piece) // 2 - min_y * TAILLE_CASE
    # Dessine chaque bloc de la pièce dans l'encadré
    for dx, dy in blocs:
        rect = pygame.Rect(offset_x + dx * TAILLE_CASE, offset_y + dy * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
        pygame.draw.rect(surface, piece.couleur, rect)
        pygame.draw.rect(surface, NOIR, rect, 1)

def draw_score(surface, score):
    """
    Affiche le score dans le panneau latéral.

    :param surface: Surface Pygame sur laquelle dessiner le score.
    :param score: Score actuel (entier).
    """
    font = pygame.font.SysFont('Arial', 24)
    texte_score = font.render("Score :", True, BLANC)
    valeur_score = font.render(str(score), True, BLANC)
    x = LARGEUR_JEU + 10
    surface.blit(texte_score, (x, 10))
    surface.blit(valeur_score, (x, 40))

def draw_controls(surface):
    """
    Affiche la liste des contrôles dans le panneau latéral, placée sous l'aperçu de la pièce suivante.

    :param surface: Surface Pygame sur laquelle dessiner les contrôles.
    """
    font = pygame.font.SysFont('Arial', 14)
    controles = [
        "Contrôles :",
        "Flèche gauche : Gauche",
        "Flèche droite : Droite",
        "Flèche haut : Rotation",
        "Flèche bas : Descente douce",
        "Espace : Descente rapide",
        "P : Pause",
        "Echap : Retour au menu",
        "R : Redémarrer (Game Over)"
    ]
    x = LARGEUR_JEU + 10
    y = 200  # Position verticale dans le panneau latéral
    for ligne in controles:
        texte = font.render(ligne, True, BLANC)
        surface.blit(texte, (x, y))
        y += 25

def draw_game_over(surface):
    """
    Affiche le message 'GAME OVER' au centre de la zone de jeu.

    :param surface: Surface Pygame sur laquelle dessiner le message.
    """
    font = pygame.font.SysFont('Arial', 36)
    texte = font.render("GAME OVER", True, BLANC)
    surface.blit(texte, (LARGEUR_JEU // 2 - texte.get_width() // 2,
                         HAUTEUR_FENETRE // 2 - texte.get_height() // 2))

def draw_pause(surface):
    """
    Affiche le message 'PAUSE' au centre de la zone de jeu.

    :param surface: Surface Pygame sur laquelle dessiner le message.
    """
    font = pygame.font.SysFont('Arial', 36)
    texte = font.render("PAUSE", True, BLANC)
    surface.blit(texte, (LARGEUR_JEU // 2 - texte.get_width() // 2,
                         HAUTEUR_FENETRE // 2 - texte.get_height() // 2))

# =============================================================================
# Boucle principale du jeu
# =============================================================================
def main():
    """
    Point d'entrée du jeu Tetris.
    
    Gère la boucle principale, le traitement des événements, la logique de jeu,
    l'affichage de la grille, des pièces, du score, des animations et du panneau latéral.
    """
    pygame.init()
    SoundManager().play_music()
    screen = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Initialisation du plateau et des pièces
    plateau = PlateauDeJeu(NB_COLONNES, NB_LIGNES)
    piece_actuelle = new_piece()
    piece_suivante = new_piece()
    fall_speed = VITESSE_CHUTE_INIT   # Vitesse de chute initiale (en millisecondes)
    fall_time = 0                     # Temps accumulé depuis la dernière descente
    score = 0                         # Score du joueur
    game_over = False                 # Indique si le jeu est terminé
    pause = False                     # Indique si le jeu est en pause

    # Variables pour gérer l'animation d'effacement des lignes
    en_animation = False              # Indique si l'animation est en cours
    lignes_animation = []             # Liste des indices de lignes à animer
    timer_animation = 0               # Timer pour l'animation d'effacement
    

    running = True
    while running:
        # dt correspond au temps écoulé en millisecondes depuis la dernière itération de la boucle
        dt = clock.tick(60)  # Limite le jeu à 60 FPS

        # Incrémente le temps de chute seulement si le jeu n'est pas en pause et qu'aucune animation n'est en cours
        if not pause and not en_animation:
            fall_time += dt

        # =============================================================================
        # Traitement des événements
        # =============================================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SoundManager().stop_music()
                running = False

            # Gestion des événements clavier
            if event.type == pygame.KEYDOWN:
                # Si la touche R est pressée après un Game Over, redémarre le jeu
                if event.key == pygame.K_r and game_over:
                    plateau = PlateauDeJeu(NB_COLONNES, NB_LIGNES)
                    piece_actuelle = new_piece()
                    piece_suivante = new_piece()
                    score = 0
                    fall_speed = VITESSE_CHUTE_INIT
                    game_over = False
                    fall_time = 0
                    pause = False
                    en_animation = False
                # Si la touche Echap est pressée après un Game Over, renvoie sur le home_screen
                if event.key == pygame.K_ESCAPE:
                        SoundManager().stop_music()
                        pygame.quit()
                        import home_screen
                        menu = home_screen.TetrisMenu()
                        menu.run()
                        sys.exit()
                # Bascule le mode pause avec la touche P (si le jeu n'est pas en animation)
                if event.key == pygame.K_p and not game_over and not en_animation:
                    pause = not pause
                # Si le jeu n'est pas en pause, en animation ou terminé, on gère les déplacements et la rotation
                if not pause and not en_animation and not game_over:
                    if event.key == pygame.K_LEFT:
                        if plateau.is_valid_move(piece_actuelle, dx=-TAILLE_CASE):
                            piece_actuelle.move_side(-TAILLE_CASE)
                    elif event.key == pygame.K_RIGHT:
                        if plateau.is_valid_move(piece_actuelle, dx=TAILLE_CASE):
                            piece_actuelle.move_side(TAILLE_CASE)
                    elif event.key == pygame.K_DOWN:
                        if plateau.is_valid_move(piece_actuelle, dy=TAILLE_CASE):
                            piece_actuelle.move_down()
                    elif event.key == pygame.K_UP:
                        # Effectue la rotation ; en cas d'invalidité, annule la rotation
                        old_rot = piece_actuelle.rotate()
                        if not plateau.is_valid_move(piece_actuelle):
                            piece_actuelle.rotate_back(old_rot)
                    elif event.key == pygame.K_SPACE:
                        # Descente rapide (hard drop) : la pièce descend jusqu'à ce qu'elle ne puisse plus se déplacer
                        while plateau.is_valid_move(piece_actuelle, dy=TAILLE_CASE):
                            piece_actuelle.move_down()
                        # Force le verrouillage immédiat en réinitialisant le timer de chute
                        fall_time = fall_speed

        # =============================================================================
        # Logique de mise à jour du jeu
        # =============================================================================
        if not pause and not game_over:
            if not en_animation:
                # Vérifie si le temps écoulé est suffisant pour faire descendre la pièce d'une case
                if fall_time >= fall_speed:
                    if plateau.is_valid_move(piece_actuelle, dy=TAILLE_CASE):
                        # La pièce descend normalement
                        piece_actuelle.move_down()
                    else:
                        # La pièce ne peut plus descendre et est verrouillée sur le plateau
                        plateau.lock_piece(piece_actuelle)
                        # Vérifie la présence de lignes complètes
                        lignes_completes = plateau.get_lignes_completes()
                        if lignes_completes:
                            # Lance l'animation d'effacement des lignes
                            en_animation = True
                            lignes_animation = lignes_completes
                            timer_animation = DUREE_ANIMATION_LIGNE
                        else:
                            # Passe à la pièce suivante
                            piece_actuelle = piece_suivante
                            piece_suivante = new_piece()
                            # Si la nouvelle pièce ne peut pas être placée, le jeu est terminé
                            if not plateau.is_valid_move(piece_actuelle):
                                game_over = True
                    # Réinitialise le compteur de temps de chute
                    fall_time = 0
            else:
                # Si une animation d'effacement est en cours, on décrémente le timer d'animation
                timer_animation -= dt
                if timer_animation <= 0:
                    # Une fois l'animation terminée, efface les lignes et met à jour le score
                    nb_lignes = len(lignes_animation)
                    plateau.effacer_lignes(lignes_animation)
                    score += nb_lignes * 100
                    # Ajuste la vitesse de chute en fonction du score (plancher à 100 ms)
                    fall_speed = max(100, VITESSE_CHUTE_INIT - (score // 500) * 20)
                    en_animation = False
                    lignes_animation = []
                    # Passe à la pièce suivante
                    piece_actuelle = piece_suivante
                    piece_suivante = new_piece()
                    # Si la nouvelle pièce ne peut pas être placée, le jeu est terminé
                    if not plateau.is_valid_move(piece_actuelle):
                        game_over = True
                    fall_time = 0

        # =============================================================================
        # Phase de dessin / affichage
        # =============================================================================
        screen.fill(GRIS)  # Efface l'écran avec la couleur de fond

        # Dessine la zone de jeu (le plateau)
        pygame.draw.rect(screen, NOIR, (0, 0, LARGEUR_JEU, HAUTEUR_FENETRE))
        plateau.draw(screen, lignes_animation if en_animation else None)
        draw_grid(screen)

        # Affiche la pièce active ou le message Game Over
        if not game_over:
            if not en_animation:
                piece_actuelle.draw(screen)
            draw_next_piece(screen, piece_suivante)
        else:
            draw_game_over(screen)

        # Dessine le score et les contrôles dans le panneau latéral
        draw_score(screen, score)
        draw_controls(screen)

        # Si le jeu est en pause, affiche le message "PAUSE"
        if pause and not game_over:
            draw_pause(screen)

        pygame.display.flip()  # Met à jour l'affichage

    pygame.quit()

# =============================================================================
# Point d'entrée du programme
# =============================================================================
if __name__ == "__main__":
    main()
