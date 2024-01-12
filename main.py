# Import necessary libraries
# Importieren Sie die erforderlichen Bibliotheken.
import pygame
import random

# Initialize PyGame
# PyGame initialisieren
pygame.init()

# Setup screen
# Setup-Bildschirm
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Welcome to 2048!")

# Set timer, fps and font
# Timer, fps und Schriftart einstellen
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 18)

# Set colors for text and background
# Farben für Text und Hintergrund festlegen
TEXT = (255, 246, 230)
BACKGROUND = (187, 173, 160)

# Define function for displaying rules
# Funktion zur Anzeige von Regeln definieren
def display_rules():
    rules_text = [
        "Welcome to 2048!",
        "Rules:",
        "1. Use arrow keys to move tiles.",
        "2. Tiles with the same number merge",
        " when they collide.",
        "3. The goal is to reach the tile",
        " with the number 2048.",
        "",
        "Press Space"
    ]

    y_position = 100

    for line in rules_text:
        text = font.render(line, True, TEXT)
        text_rect = text.get_rect(center=(WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        y_position += 40

# Setup rules screen
# Bildschirm "Regeln einrichten
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False  

    
    screen.fill(BACKGROUND)
    display_rules()
    pygame.display.flip()


# Set colors for the game
# Farben für das Spiel festlegen
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          4096: (255, 80, 75),
          8192: (255, 34, 75),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# Initialize some of the used variables
# Initialisieren Sie einige der verwendeten Variablen
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0

# Get highscore from log file
# Highscore aus Protokolldatei abrufen
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high

# Setup Game Over screen
# Bildschirm "Game Over" einrichten
def draw_over():
    pygame.draw.rect(screen, 'dark grey', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'red')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# Setup function for pressing UP key
# Setup-Funktion für das Drücken der UP-Taste
def up (board):
        # Initialize variable score from outside the scope
        # Initialisierung der Variable score von außerhalb des Bereichs
        global score
        # Matrix to track merged tiles
        # Matrix zur Verfolgung der zusammengefügten Kacheln
        merged = [[False for _ in range(4)] for _ in range(4)]
        # Iterate over the rows and columns
        # Iterieren Sie über die Zeilen und Spalten.
        for i in range(4):
            for j in range(4):
                # Initialize shift and iterate over rows
                # Verschiebung initialisieren und über Zeilen iterieren
                shift = 0
                if i > 0:
                    for q in range(i):
                        # Check for empty spaces
                        # Auf Leerzeichen prüfen
                        if board[q][j] == 0:
                            shift += 1
                    # Shift the tile if there are empty spaces
                    # Verschieben Sie die Kachel, wenn es leere Stellen gibt.
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    # Check if merging is possible
                    # Prüfen Sie, ob eine Zusammenführung möglich ist.
                    if (
                        board[i - shift - 1][j] == board[i - shift][j]
                        and not merged[i - shift][j]
                        and not merged[i - shift - 1][j]
                    ):
                        # Merge tiles, double the value, update score, and mark as merged
                        # Kacheln zusammenführen, den Wert verdoppeln, die Punktzahl aktualisieren und als zusammengeführt markieren
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

# Setup function for pressing DOWN key
# Setup-Funktion für das Drücken der DOWN-Taste
def down (board):
        # Initialize variable score from outside the scope
        # Initialisierung der Variable score von außerhalb des Bereichs
        global score
        # Matrix to track merged tiles
        # Matrix zur Verfolgung der zusammengefügten Kacheln
        merged = [[False for _ in range(4)] for _ in range(4)]
        # Iterate over the rows and columns
        # Iterieren Sie über die Zeilen und Spalten.
        for i in range(3):
            for j in range(4):
                # Initialize shift and iterate over rows
                # Verschiebung initialisieren und über Zeilen iterieren
                shift = 0
                for q in range(i + 1):
                    # Check for empty spaces
                    # Auf Leerzeichen prüfen
                    if board[3 - q][j] == 0:
                        shift += 1
                # Shift the tile if there are empty spaces
                # Verschieben Sie die Kachel, wenn es leere Stellen gibt.
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                # Check if merging is possible
                # Prüfen Sie, ob eine Zusammenführung möglich ist.
                if 3 - i + shift <= 3:
                    if (
                        board[2 - i + shift][j] == board[3 - i + shift][j]
                        and not merged[3 - i + shift][j]
                        and not merged[2 - i + shift][j]
                    ):
                        # Merge tiles, double the value, update score, and mark as merged
                        # Kacheln zusammenführen, den Wert verdoppeln, die Punktzahl aktualisieren und als zusammengeführt markieren
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

# Setup function for pressing LEFT key
# Setup-Funktion für das Drücken der LINKEN Taste
def left (board):
        # Initialize variable score from outside the scope
        # Initialisierung der Variable score von außerhalb des Bereichs
        global score
        # Matrix to track merged tiles
        # Matrix zur Verfolgung der zusammengefügten Kacheln
        merged = [[False for _ in range(4)] for _ in range(4)]
        # Iterate over the rows and columns
        # Iterieren Sie über die Zeilen und Spalten.
        for i in range(4):
            for j in range(4):
                # Initialize shift and iterate over rows
                # Verschiebung initialisieren und über Zeilen iterieren
                shift = 0
                for q in range(j):
                    # Check for empty spaces
                    # Auf Leerzeichen prüfen
                    if board[i][q] == 0:
                        shift += 1
                # Shift the tile if there are empty spaces
                # Verschieben Sie die Kachel, wenn es leere Stellen gibt.
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                # Check if merging is possible
                # Prüfen Sie, ob eine Zusammenführung möglich ist.
                if (
                    board[i][j - shift] == board[i][j - shift - 1]
                    and not merged[i][j - shift - 1]
                    and not merged[i][j - shift]
                ):
                    # Merge tiles, double the value, update score, and mark as merged
                    # Kacheln zusammenführen, den Wert verdoppeln, die Punktzahl aktualisieren und als zusammengeführt markieren
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

# Setup function for pressing RIGHT key
# Setup-Funktion für das Drücken der RECHTS-Taste
def right (board):
        # Initialize variable score from outside the scope
        # Initialization of the variable score from outside the range
        global score
        # Matrix to track merged tiles
        # Matrix zur Verfolgung der zusammengefügten Kacheln
        merged = [[False for _ in range(4)] for _ in range(4)]
        # Iterate over the rows and columns
        # Iterieren Sie über die Zeilen und Spalten.
        for i in range(4):
            for j in range(4):
                # Initialize shift and iterate over rows
                # Verschiebung initialisieren und über Zeilen iterieren
                shift = 0
                for q in range(j):
                    # Check for empty spaces
                    # Auf Leerzeichen prüfen
                    if board[i][3 - q] == 0:
                        shift += 1
                # Shift the tile if there are empty spaces
                # Verschieben Sie die Kachel, wenn es leere Stellen gibt.
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                # Check if merging is possible
                 # Prüfen Sie, ob eine Zusammenführung möglich ist.
                if 4 - j + shift <= 3:
                    if (
                        board[i][4 - j + shift] == board[i][3 - j + shift]
                        and not merged[i][4 - j + shift]
                        and not merged[i][3 - j + shift]
                    ):
                        # Merge tiles, double the value, update score, and mark as merged
                        # Kacheln zusammenführen, den Wert verdoppeln, die Punktzahl aktualisieren und als zusammengeführt markieren
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True

# Setup function for choosing function based on the pressed key
# Setup-Funktion für die Auswahl der Funktion basierend auf der gedrückten Taste

def take_turn(direc, board):
    global score
   
    if direc == "UP":
     up (board)

    elif direc == "DOWN":
        down (board)

    elif direc == "LEFT":
        left (board)

    elif direc == "RIGHT":
        right (board)

    return board


# Setup function for spawning new pieces
# Funktion zum Erzeugen neuer Stücke einrichten
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# Setup function for drawing a game board
# Setup-Funktion zum Zeichnen eines Spielbretts
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass

# Setup function for drawing game pieces
# Funktion zum Zeichnen von Spielfiguren einrichten
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'dark grey', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# Main game loop
# Hauptspielschleife
run = True
while run:
    # Activate functions
    # Funktionen aktivieren
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    # Spawn new pieces
    # Neue Stücke hervorbringen
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    # Setup new turn
     # Neue Runde einrichten
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        # Set high score
        # Highscore setzen
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score
    # Handle events (pressed keys) in game
            # Handle Events (gedrückte Tasten) im Spiel
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            # Restarting the game after game is over
                # Neustart des Spiels nach Beendigung des Spiels
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False
    # Setup high score
     # Highscore einrichten
    if score > high_score:
        high_score = score

    pygame.display.flip()
# Quit game
    # Spiel beenden
pygame.quit()
