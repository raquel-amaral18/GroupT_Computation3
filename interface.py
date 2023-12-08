import pygame

import config

from game import game
from multiplayer import *


def find_user_with_highest_score():
    """
     This Function will access the database.py file and find the user with the highest score

    Return:
    -------
         max_score_user:
            name of user with the highest score,
         max_score:
            score from the user
    
    Imports:
    --------
        'read_highscores' function from 'database.py'
    """

    from database import read_highscores

    # Retrieving the high scores
    highscores = read_highscores()

    # Finding the user with the highest score
    if highscores:
        max_score_user = max(highscores, key=lambda user: highscores[user][0][0])
        max_score = highscores[max_score_user][0][0]
        return max_score_user, max_score
    else:
        return None, None


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
    MAASTRICHT_BLUE = (3, 23, 48)
    LIGHT_YELLOW = (252, 198, 54)
    DARK_YELLOW = (182, 144, 42)
    LIGHT_BLUE = (65, 163, 187)
    DARK_BLUE = (27, 148, 153)

    # text
    high_score_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 40)
    game_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 60).render("PLAY", True, BLACK)
    multi_player_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 35).render("MULTIPLAYER", True, BLACK)
    store_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("STORE", True, BLACK)
    instructions_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("HOW TO PLAY?", True,
                                                                                             BLACK)
    credits_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("CREDITS", True, BLACK)
    quit_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("QUIT", True, BLACK)

    # MUSIC AND SOUNDS
    # Load background music
    if config.is_music_enabled:
        pygame.mixer.music.load("Music&Sounds/background_music_menus.mp3")
        pygame.mixer.music.set_volume(0.2)  # Set the volume
        pygame.mixer.music.play(-1)  # Play the background music on loop

    # IMAGES:
    # Background
    background = pygame.image.load("Images/Design/interface.png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # Button images
    name_button_image = pygame.image.load("Images/Extras/user.png")
    inventory_image = pygame.image.load("Images/Extras/inventory.png")
    music_button_image = pygame.image.load("Images/Extras/music.png")
    sound_button_image = pygame.image.load("Images/Extras/sound.png")

    # Scale images to width=30 while maintaining aspect ratio
    name_button_image = pygame.transform.scale(name_button_image, (
        40, int(40 * name_button_image.get_height() / name_button_image.get_width())))
    inventory_image = pygame.transform.scale(inventory_image, (
        40, int(40 * inventory_image.get_height() / inventory_image.get_width())))
    music_button_image = pygame.transform.scale(music_button_image, (
        40, int(40 * music_button_image.get_height() / music_button_image.get_width())))
    sound_button_image = pygame.transform.scale(sound_button_image, (
        40, int(40 * sound_button_image.get_height() / sound_button_image.get_width())))

    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 740 <= mouse[0] <= 810 and 260 <= mouse[1] <= 310:  # User name button
                    from users import prompt_player_name, user, chosen_car
                    player_name = prompt_player_name()
                    username = user(player_name)
                    config.username = username
                    config.chosen_car = 0

                if 740 <= mouse[0] <= 810 and 330 <= mouse[1] <= 390:  # Inventory button
                    from inventory import inventory
                    inventory(SCREEN_WIDTH, SCREEN_HEIGHT)

                if 740 <= mouse[0] <= 810 and 400 <= mouse[1] <= 460:  # Sound button
                    config.is_sound_enabled = not config.is_sound_enabled

                if 670 <= mouse[0] <= 730 and 400 <= mouse[1] <= 460:  # Music button
                    config.is_music_enabled = not config.is_music_enabled
                    if not config.is_music_enabled:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                if 310 <= mouse[0] <= 580 and 470 <= mouse[1] <= 550:  # Game button
                    game(SCREEN_WIDTH, SCREEN_HEIGHT)

                elif 345 <= mouse[0] <= 545 and 570 <= mouse[1] <= 650:  # Multiplayer menu button
                    multiplayer_menu(SCREEN_WIDTH, SCREEN_HEIGHT)

                elif 90 <= mouse[0] <= 290 and 500 <= mouse[1] <= 560:  # Store button
                    from store import store
                    store(SCREEN_WIDTH, SCREEN_HEIGHT)

                elif 90 <= mouse[0] <= 290 and 600 <= mouse[1] <= 660:  # Instructions button
                    instructions1_(SCREEN_WIDTH, SCREEN_HEIGHT)

                elif 610 <= mouse[0] <= 810 and 500 <= mouse[1] <= 560:  # Credits button
                    credits_(SCREEN_WIDTH, SCREEN_HEIGHT)

                elif 610 <= mouse[0] <= 810 and 600 <= mouse[1] <= 660:  # Quit button
                    pygame.quit()

            screen.blit(background, (0, 0))

            # Define box positions
            # Game button
            pygame.draw.rect(screen, DARK_YELLOW, [320, 475, 250, 80], border_radius=24)
            pygame.draw.rect(screen,
                             DARK_YELLOW if (310 <= mouse[0] <= 580 and 470 <= mouse[1] <= 550) else LIGHT_YELLOW,
                             [320, 470, 250, 80], border_radius=24)
            text_x = (320 + 570 - game_text.get_width()) // 2
            text_y = (470 + 555 - game_text.get_height()) // 2
            screen.blit(game_text, (text_x, text_y))

            # Multiplayer button
            pygame.draw.rect(screen, DARK_YELLOW, [345, 575, 200, 80], border_radius=24)
            pygame.draw.rect(screen,
                             DARK_YELLOW if (345 <= mouse[0] <= 545 and 570 <= mouse[1] <= 650) else LIGHT_YELLOW,
                             [345, 570, 200, 80], border_radius=24)
            text_x = (345 + 545 - multi_player_text.get_width()) // 2
            text_y = (570 + 655 - multi_player_text.get_height()) // 2
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

            # User name button
            pygame.draw.rect(screen, DARK_YELLOW, [740, 265, 60, 60], border_radius=100)
            pygame.draw.rect(screen, LIGHT_YELLOW, [740, 260, 60, 60], border_radius=100)
            screen.blit(name_button_image, (750, 270))

            # Inventory button
            pygame.draw.rect(screen, DARK_YELLOW, [740, 335, 60, 60], border_radius=100)
            pygame.draw.rect(screen, LIGHT_YELLOW, [740, 330, 60, 60], border_radius=100)
            screen.blit(inventory_image, (750, 340))

            # Sound button
            pygame.draw.rect(screen, DARK_YELLOW, [740, 405, 60, 60], border_radius=100)
            pygame.draw.rect(screen, LIGHT_YELLOW, [740, 400, 60, 60], border_radius=100)
            screen.blit(sound_button_image, (750, 410))

            # Music button
            pygame.draw.rect(screen, DARK_YELLOW, [670, 405, 60, 60], border_radius=100)
            pygame.draw.rect(screen, LIGHT_YELLOW, [670, 400, 60, 60], border_radius=100)
            screen.blit(music_button_image, (680, 410))

            # Draw diagonal line when music is not playing
            if not config.is_music_enabled:
                pygame.draw.line(screen, MAASTRICHT_BLUE, (670, 400), (730, 460), 7)

            # Draw diagonal line when sound is not playing
            if not config.is_sound_enabled:
                pygame.draw.line(screen, MAASTRICHT_BLUE, (740, 400), (810, 460), 7)

            # Displays the user with the highest score in the menu
            max_score_user, max_score = find_user_with_highest_score()
            if max_score_user is not None:
                hs_text = high_score_font.render(f"{max_score}", True, LIGHT_BLUE)
                hs_person_text = high_score_font.render(f"{max_score_user}", True, LIGHT_BLUE)
                screen.blit(hs_text, (150, 300))
                screen.blit(hs_person_text, (130, 340))
                pygame.display.update()


        pygame.display.update()


def multiplayer_menu(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # COLORS
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    MAASTRICHT_BLUE = (3, 23, 48)
    LIGHT_BLUE = (65, 163, 187)
    DARK_BLUE = (27, 148, 153)

    # BACKGROUND
    # Background
    background = pygame.image.load("Images/Design/stars&planets.png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # TEXT
    road1_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30) \
        .render("SINGLE ROAD", True, BLACK)
    road2_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30) \
        .render("TWO-ROADS", True, BLACK)
    back_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 50).render("X", True, BLACK)

    # BUTTONS
    BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

    while True:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0] \
                        <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH \
                        and 350 <= mouse[1] <= 350 + BUTTON_HEIGHT:
                    gameMP(SCREEN_WIDTH, SCREEN_HEIGHT)
                elif SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0] \
                        <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH \
                        and 420 <= mouse[1] <= 420 + BUTTON_HEIGHT:
                    gameMP2roads(SCREEN_WIDTH, SCREEN_HEIGHT)
                elif 660 <= mouse[0] <= 710 and 220 <= mouse[1] <= 270:
                    interface()

        # Draw background
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, MAASTRICHT_BLUE, [SCREEN_WIDTH // 2 - 600 // 2, 200, 600, 300], border_radius=24)
        pygame.draw.rect(screen, LIGHT_BLUE, [SCREEN_WIDTH // 2 - 600 // 2, 200, 600, 300], border_radius=24, width=4)

        # DRAW BUTTONS
        # Single road
        pygame.draw.rect(screen, DARK_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 355, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        pygame.draw.rect(screen,
                         DARK_BLUE if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0]
                                       <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH
                                       and 350 <= mouse[1] <= 350 + BUTTON_HEIGHT)
                         else LIGHT_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        text_x = (SCREEN_WIDTH // 2 - road1_text.get_width() // 2)
        text_y = (350 + BUTTON_HEIGHT // 2 - road1_text.get_height() // 2)
        screen.blit(road1_text, (text_x, text_y))

        # Two roads
        pygame.draw.rect(screen, DARK_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 425, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        pygame.draw.rect(screen,
                         DARK_BLUE if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0]
                                       <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH
                                       and 420 <= mouse[1] <= 420 + BUTTON_HEIGHT)
                         else LIGHT_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        text_x = (SCREEN_WIDTH // 2 - road2_text.get_width() // 2)
        text_y = (420 + BUTTON_HEIGHT // 2 - road2_text.get_height() // 2)
        screen.blit(road2_text, (text_x, text_y))

        # back button
        pygame.draw.rect(screen, DARK_BLUE,
                         [660, 225, 50, 50], border_radius=24)
        pygame.draw.rect(screen, DARK_BLUE if (660 <= mouse[0] <= 710 and 220 <= mouse[1] <= 270) else LIGHT_BLUE,
                         [660, 220, 50, 50], border_radius=24)
        screen.blit(back_text, (673, 213))

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
    background = pygame.image.load("Images/Design/instructions (1).png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    arrow_size = (40, 40)

    arrow_right = pygame.image.load("Images/Design/arrow_right.png")
    arrow_right = pygame.transform.scale(arrow_right, arrow_size)
    arrow_right_rect = arrow_right.get_rect()

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

        # NEXT PAGE BUTTON
        next_page = pygame.draw.rect(screen,
                                     DARK_BLUE if (750 <= mouse[0] <= 830 and 600 <= mouse[1] <= 680) else LIGHT_BLUE,
                                     [750, 600, 80, 80], border_radius=40)

        next_arrow = (next_page.center[0] - arrow_right_rect.width // 2,
                      next_page.center[1] - arrow_right_rect.height // 2)

        screen.blit(arrow_right, next_arrow)

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
    background = pygame.image.load("Images/Design/instructions (2).png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # ARROWS
    arrow_size = (40, 40)

    arrow_right = pygame.image.load("Images/Design/arrow_right.png")
    arrow_right = pygame.transform.scale(arrow_right, arrow_size)
    arrow_right_rect = arrow_right.get_rect()

    arrow_left = pygame.image.load("Images/Design/arrow_left.png")
    arrow_left = pygame.transform.scale(arrow_left, arrow_size)
    arrow_left_rect = arrow_right.get_rect()

    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 650 <= mouse[0] <= 730 and 600 <= mouse[1] <= 680:
                    instructions1_(SCREEN_WIDTH, SCREEN_HEIGHT)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= mouse[0] <= 830 and 600 <= mouse[1] <= 680:
                    instructions3_(SCREEN_WIDTH, SCREEN_HEIGHT)

        screen.blit(background, (0, 0))

        # PREVIOUS PAGE BUTTON
        prev_page = pygame.draw.rect(screen,
                                     DARK_BLUE if (650 <= mouse[0] <= 730 and 600 <= mouse[1] <= 680) else LIGHT_BLUE,
                                     [650, 600, 80, 80], border_radius=40)

        prev_arrow = (prev_page.center[0] - arrow_left_rect.width // 2,
                      prev_page.center[1] - arrow_left_rect.height // 2)

        screen.blit(arrow_left, prev_arrow)

        # NEXT PAGE BUTTON
        next_page = pygame.draw.rect(screen,
                                     DARK_BLUE if (750 <= mouse[0] <= 830 and 600 <= mouse[1] <= 680) else LIGHT_BLUE,
                                     [750, 600, 80, 80], border_radius=40)

        next_arrow = (next_page.center[0] - arrow_right_rect.width // 2,
                      next_page.center[1] - arrow_right_rect.height // 2)

        screen.blit(arrow_right, next_arrow)

        pygame.display.update()


def instructions3_(SCREEN_WIDTH, SCREEN_HEIGHT):
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
    background = pygame.image.load("Images/Design/instructions (3).png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # ARROWS
    arrow_size = (40, 40)

    arrow_right = pygame.image.load("Images/Design/arrow_right.png")
    arrow_right = pygame.transform.scale(arrow_right, arrow_size)
    arrow_right_rect = arrow_right.get_rect()

    arrow_left = pygame.image.load("Images/Design/arrow_left.png")
    arrow_left = pygame.transform.scale(arrow_left, arrow_size)
    arrow_left_rect = arrow_right.get_rect()

    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 650 <= mouse[0] <= 730 and 600 <= mouse[1] <= 680:
                    instructions2_(SCREEN_WIDTH, SCREEN_HEIGHT)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 750 <= mouse[0] <= 830 and 600 <= mouse[1] <= 680:
                    interface()

        screen.blit(background, (0, 0))

        # PREVIOUS PAGE BUTTON
        prev_page = pygame.draw.rect(screen,
                                     DARK_BLUE if (650 <= mouse[0] <= 730 and 600 <= mouse[1] <= 680) else LIGHT_BLUE,
                                     [650, 600, 80, 80], border_radius=40)

        prev_arrow = (prev_page.center[0] - arrow_left_rect.width // 2,
                      prev_page.center[1] - arrow_left_rect.height // 2)

        screen.blit(arrow_left, prev_arrow)

        # NEXT PAGE BUTTON
        next_page = pygame.draw.rect(screen,
                                     DARK_BLUE if (750 <= mouse[0] <= 830 and 600 <= mouse[1] <= 680) else LIGHT_BLUE,
                                     [750, 600, 80, 80], border_radius=40)

        next_arrow = (next_page.center[0] - arrow_right_rect.width // 2,
                      next_page.center[1] - arrow_right_rect.height // 2)

        screen.blit(arrow_right, next_arrow)

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
    background = pygame.image.load("Images/Design/credits.png")
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
