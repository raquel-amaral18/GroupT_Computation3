import pygame

from game import game
from multiplayer import *
from button import Button
import config



def interface():

    pygame.init()  # Initialize the pygame
    trigger = 0    # Trigger for the car model

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

    #Buttons
    login_button = Button("Login", 90, 400, 200, 60)
    inventory_button = Button("Inventory", 610, 400, 200, 60)


    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            login_button.draw(screen)

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 310 <= mouse[0] <= 580 and 470 <= mouse[1] <= 550:
                    game(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 345 <= mouse[0] <= 545 and 570 <= mouse[1] <= 650:
                    multiplayermenu(SCREEN_WIDTH, SCREEN_HEIGHT)
                    # gameMP2roads(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 90 <= mouse[0] <= 290 and 500 <= mouse[1] <= 560:
                    from Store import store
                    store(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 90 <= mouse[0] <= 290 and 600 <= mouse[1] <= 660:
                    from instructions import instructions1_
                    instructions1_(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 610 <= mouse[0] <= 810 and 500 <= mouse[1] <= 560:
                    credits_(SCREEN_WIDTH, SCREEN_HEIGHT)
                if 610 <= mouse[0] <= 810 and 600 <= mouse[1] <= 660:
                    pygame.quit()
                if login_button.is_clicked(event.pos):
                    from users import prompt_player_name, user, chosen_car
                    player_name = prompt_player_name()
                    username = user(player_name)
                    config.username = username
                    config.chosen_car = 0



                if inventory_button.is_clicked(event.pos):
                    from Inventory import inventory
                    inventory(SCREEN_WIDTH, SCREEN_HEIGHT)




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

def multiplayermenu(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame
    from button import Button
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
    background = pygame.image.load("Images/BackgroundMP.png")
    original_width, original_height = background.get_size()

    # Draw Pause Menu Text
    font = pygame.font.SysFont('monospace', 50, bold=True)
    text = font.render('Paused', True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)


    # Button dimensions and positioning
    button_width, button_height = 150, 60  # Increase width and height
    horizontal_spacing, vertical_spacing = 30, 20  # Increase spacing
    total_width = 2 * button_width + horizontal_spacing
    # Adjusted button positions
    start_x = (screen.get_width() - total_width) / 2
    start_y = text_rect.bottom + 60  # Increase the starting y-position
    center_x = (SCREEN_WIDTH - button_width) // 2
    bottom_y = SCREEN_HEIGHT - button_height - 20

    # Create buttons
    Single_road_button = Button("Single Road Fun", start_x, start_y, button_width, button_height)
    Two_Player_button = Button("2 Players, 2 Roads", start_x + button_width + horizontal_spacing, start_y, button_width, button_height)
    credits_button = Button("Credits", start_x, start_y + button_height + vertical_spacing, button_width, button_height)
    quit_button = Button("Quit", start_x + button_width + horizontal_spacing, start_y + button_height + vertical_spacing, button_width, button_height)
    back_button = Button("Back", center_x, bottom_y, button_width, button_height)

    # Draw buttons
    Single_road_button.draw(screen)
    Two_Player_button.draw(screen)
    credits_button.draw(screen)
    quit_button.draw(screen)
    back_button.draw(screen)

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
                if Single_road_button.is_clicked(event.pos):
                    gameMP(SCREEN_WIDTH, SCREEN_HEIGHT)
                elif Two_Player_button.is_clicked(event.pos):
                    gameMP2roads(SCREEN_WIDTH, SCREEN_HEIGHT)
                elif credits_button.is_clicked(event.pos):
                    paused = False  # Resume game
                elif quit_button.is_clicked(event.pos):
                    pygame.quit()
                elif back_button.is_clicked(event.pos):
                    interface()

        screen.blit(background, (0, 0))

        Single_road_button.draw(screen)
        Two_Player_button.draw(screen)
        credits_button.draw(screen)
        quit_button.draw(screen)
        back_button.draw(screen)


        pygame.display.update()