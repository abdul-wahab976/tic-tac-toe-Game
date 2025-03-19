import pygame
import sys
import time
import gamelogic as ttt  # Ensure this module exists and is correct.

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
size = width, height = 600, 400
bg_color1 = (30, 144, 255)  # Dodger Blue
bg_color2 = (75, 0, 130)  # Indigo
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

# Font setup (use default Pygame font if the custom font is unavailable)
try:
    mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
    largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
    moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
except IOError:
    print("Font not found, using default font.")
    mediumFont = pygame.font.Font(None, 28)
    largeFont = pygame.font.Font(None, 40)
    moveFont = pygame.font.Font(None, 60)

# Initial game state and variables
user = None
board = ttt.initial_state()  # Initialize the Tic-Tac-Toe board
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw gradient background
    for y in range(height):
        r = bg_color1[0] + (bg_color2[0] - bg_color1[0]) * y // height
        g = bg_color1[1] + (bg_color2[1] - bg_color1[1]) * y // height
        b = bg_color1[2] + (bg_color2[2] - bg_color1[2]) * y // height
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

    # If user has not selected X or O yet
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = (width / 2, 50)
        screen.blit(title, titleRect)

        # Draw buttons for selecting X or O
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, bg_color1)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton, border_radius=10)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, bg_color1)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton, border_radius=10)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Draw the game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []

        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(tile_origin[0] + j * tile_size, tile_origin[1] + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, white, rect, 3, border_radius=5)

                # Display the moves
                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        # Check if the game is over
        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = "Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."

        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = (width / 2, 30)
        screen.blit(title, titleRect)

        # AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # User move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = ttt.result(board, (i, j))

        # Play again button after game is over
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, bg_color1)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton, border_radius=10)
            screen.blit(again, againRect)

            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()  # Reset the board
                    ai_turn = False

    pygame.display.flip()
