import pygame
from button import Button
from game import accessed_from_pause


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
                    from interface import interface
                    interface()

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, DARK_BLUE, [750, 600, 80, 80], border_radius=100)

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
                    from game import game
                    return

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, DARK_BLUE, [750, 600, 80, 80], border_radius=100)

        pygame.display.update()