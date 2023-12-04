import pygame

from game import game
from multiplayer import gameMP


def interface():

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    LIGHT_YELLOW = (252, 198, 54)
    DARK_YELLOW = (182, 144, 42)
    LIGHT_BLUE = (65, 163, 187)
    DARK_BLUE = (27, 148, 153)

    # text
    game_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 60).render("PLAY", True, BLACK)
    multi_player_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 35).render("MULTIPLAYER", True, BLACK)
    store_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("STORE", True, BLACK)
    instructions_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("HOW TO PLAY?", True, BLACK)
    credits_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("CREDITS", True, BLACK)
    quit_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("QUIT", True, BLACK)

    # Background
    background = pygame.image.load("Images/interface.png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))


    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 310 <= mouse[0] <= 580 and 390 <= mouse[1] <= 470:
                    game(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 345 <= mouse[0] <= 545 and 490 <= mouse[1] <= 570:
                    gameMP(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 90 <= mouse[0] <= 290 and 500 <= mouse[1] <= 560:
                    # Store
                    pass
                if 90 <= mouse[0] <= 290 and 600 <= mouse[1] <= 660:
                    instructions1_(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 610 <= mouse[0] <= 810 and 500 <= mouse[1] <= 560:
                    credits_(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 610 <= mouse[0] <= 810 and 600 <= mouse[1] <= 660:
                    pygame.quit()

            screen.blit(background, (0, 0))

            # Define box positions
            # Game button
            pygame.draw.rect(screen, DARK_YELLOW, [320, 395, 250, 80], border_radius=24)
            pygame.draw.rect(screen,
                             DARK_YELLOW if (310 <= mouse[0] <= 580 and 390 <= mouse[1] <= 470) else LIGHT_YELLOW,
                             [320, 390, 250, 80], border_radius=24)
            text_x = (320 + 570 - game_text.get_width()) // 2
            text_y = (395 + 475 - game_text.get_height()) // 2
            screen.blit(game_text, (text_x, text_y))

            # Multiplayer button
            pygame.draw.rect(screen, DARK_YELLOW, [345, 495, 200, 80], border_radius=24)
            pygame.draw.rect(screen,
                             DARK_YELLOW if (345 <= mouse[0] <= 545 and 490 <= mouse[1] <= 570) else LIGHT_YELLOW,
                             [345, 490, 200, 80], border_radius=24)
            text_x = (345 + 545 - multi_player_text.get_width()) // 2
            text_y = (495 + 575 - multi_player_text.get_height()) // 2
            screen.blit(multi_player_text, (text_x, text_y))

            # Store button
            pygame.draw.rect(screen, DARK_BLUE, [90, 505, 200, 60], border_radius=100)
            pygame.draw.rect(screen,
                             DARK_BLUE if (90 <= mouse[0] <= 290 and 500 <= mouse[1] <= 560) else LIGHT_BLUE,
                             [90, 500, 200, 60], border_radius=100)
            text_x = (90 + 290 - store_text.get_width()) // 2
            text_y = (505 + 565 - store_text.get_height()) // 2
            screen.blit(store_text, (text_x, text_y))

            # Instructions button
            pygame.draw.rect(screen, DARK_BLUE, [90, 605, 200, 60], border_radius=100)
            pygame.draw.rect(screen,
                             DARK_BLUE if (90 <= mouse[0] <= 290 and 600 <= mouse[1] <= 660) else LIGHT_BLUE,
                             [90, 600, 200, 60], border_radius=100)
            text_x = (90 + 290 - instructions_text.get_width()) // 2
            text_y = (605 + 665 - instructions_text.get_height()) // 2
            screen.blit(instructions_text, (text_x, text_y))

            # Credits button
            pygame.draw.rect(screen, DARK_BLUE, [610, 505, 200, 60], border_radius=100)
            pygame.draw.rect(screen,
                             DARK_BLUE if (610 <= mouse[0] <= 810 and 500 <= mouse[1] <= 560) else LIGHT_BLUE,
                             [610, 500, 200, 60], border_radius=100)
            text_x = (610 + 810 - credits_text.get_width()) // 2
            text_y = (505 + 565 - credits_text.get_height()) // 2
            screen.blit(credits_text, (text_x, text_y))

            # Quit button
            pygame.draw.rect(screen, DARK_BLUE, [610, 605, 200, 60], border_radius=100)
            pygame.draw.rect(screen,
                             DARK_BLUE if (610 <= mouse[0] <= 810 and 600 <= mouse[1] <= 660) else LIGHT_BLUE,
                             [610, 600, 200, 60], border_radius=100)
            text_x = (610 + 810 - quit_text.get_width()) // 2
            text_y = (605 + 665 - quit_text.get_height()) // 2
            screen.blit(quit_text, (text_x, text_y))




        pygame.display.update()


def credits_(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (65, 163, 187)
    DARK_BLUE = (27, 148, 153)

    back_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("BACK", True, BLACK)

    # Background
    background = pygame.image.load("Images/credits.png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 345 <= mouse[0] <= 545 and 600 <= mouse[1] <= 660:
                    interface()

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, DARK_BLUE, [345, 605, 200, 60], border_radius=100)
        pygame.draw.rect(screen,
                         DARK_BLUE if (345 <= mouse[0] <= 545 and 600 <= mouse[1] <= 660) else LIGHT_BLUE,
                         [345, 600, 200, 60], border_radius=100)
        text_x = (345 + 545 - back_text.get_width()) // 2
        text_y = (605 + 660 - back_text.get_height()) // 2
        screen.blit(back_text, (text_x, text_y))

        pygame.display.update()


def instructions1_(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (65, 163, 187)
    DARK_BLUE = (27, 148, 153)

    # Background
    background = pygame.image.load("Images/instructions (1).png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= mouse[0] <= 830 and 600 <= mouse[1] <= 680:
                    instructions2_(SCREEN_WIDTH, SCREEN_HEIGHT)

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, DARK_BLUE, [750, 600, 80, 80], border_radius=100)

        pygame.display.update()


def instructions2_(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (65, 163, 187)
    DARK_BLUE = (27, 148, 153)

    # Background
    background = pygame.image.load("Images/instructions (2).png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= mouse[0] <= 830 and 600 <= mouse[1] <= 680:
                    interface()

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, DARK_BLUE, [750, 600, 80, 80], border_radius=100)

        pygame.display.update()
