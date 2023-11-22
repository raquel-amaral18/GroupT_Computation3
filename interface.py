import pygame

from game import game


def interface():

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))

    # GAME SETTINGS:
    # colors
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (48, 168, 99)
    PALE_VIOLET_PINK = (240, 98, 146)
    RED = (249, 65, 68)
    VIOLET = (199, 125, 255)
    YELLOW = (255, 209, 102)
    ORANGE = (251, 133, 0)
    BLUE = (0, 180, 216)

    # font
    corbelfont = pygame.font.SysFont('Corbel', 50)
    arialfont = pygame.font.SysFont('arial', 40)

    # text
    title = arialfont.render("Car Racing Game", True, WHITE)
    car_racing_text = arialfont.render("Car Racing", True, WHITE)
    credits_text = arialfont.render("Credits", True, WHITE)
    multi_player_text = arialfont.render("Multi Player", True, WHITE)
    quit_text = arialfont.render("Quit", True, WHITE)

    # Boxes dimensions
    box_width = 200
    box_height = 75
    box_margin = 50


    # Drawing the screen
    while True:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin \
                        and 300 <= mouse[1] <= 300 + box_height:
                    game()
                if screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin \
                        and 400 <= mouse[1] <= 400 + box_height:
                    # Add multiplayer function here
                    pass
                if screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin \
                        and 500 <= mouse[1] <= 500 + box_height:
                    credits_()
                if screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin \
                        and 600 <= mouse[1] <= 600 + box_height:
                    pygame.quit()

            screen.fill(BLACK)
            screen.blit(title, (screen_width - title.get_width() - 20, 20))

            # Draw boxes and text in the same column
            # Define box positions
            pygame.draw.rect(screen,
                             GREEN if (screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin
                                       and 300 <= mouse[1] <= 300 + box_height) else GREY,
                             [screen_width - box_width - box_margin, 300, box_width, box_height])
            screen.blit(car_racing_text, (screen_width - box_width - box_margin + (box_width - car_racing_text.get_width()) // 2,
                               300 + (box_height - car_racing_text.get_height()) // 2))

            pygame.draw.rect(screen,
                             BLUE if (screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin
                                      and 400 <= mouse[1] <= 400 + box_height) else GREY,
                             [screen_width - box_width - box_margin, 400, box_width, box_height])
            screen.blit(multi_player_text, (screen_width - box_width - box_margin + (box_width - multi_player_text.get_width()) // 2,
                                 400 + (box_height - multi_player_text.get_height()) // 2))

            pygame.draw.rect(screen,
                             ORANGE if (screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin
                                      and 500 <= mouse[1] <= 500 + box_height) else GREY,
                             [screen_width - box_width - box_margin, 500, box_width, box_height])
            screen.blit(credits_text, (screen_width - box_width - box_margin + (box_width - credits_text.get_width()) // 2,
                            500 + (box_height - credits_text.get_height()) // 2))

            pygame.draw.rect(screen,
                             VIOLET if (screen_width - box_width - box_margin <= mouse[0] <= screen_width - box_margin
                                      and 600 <= mouse[1] <= 600 + box_height) else GREY,
                             [screen_width - box_width - box_margin, 600, box_width, box_height])
            screen.blit(quit_text, (screen_width - box_width - box_margin + (box_width - quit_text.get_width()) // 2,
                         600 + (box_height - quit_text.get_height()) // 2))



        pygame.display.update()


def credits_():
    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen_width = 800
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    # GAME SETTINGS:
    # colors
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (48, 168, 99)
    PALE_VIOLET_PINK = (240, 98, 146)
    RED = (249, 65, 68)
    VIOLET = (199, 125, 255)
    YELLOW = (255, 209, 102)
    ORANGE = (251, 133, 0)
    BLUE = (0, 180, 216)

    # font
    corbelfont = pygame.font.SysFont('Corbel', 50)
    comicsansfont = pygame.font.SysFont('Comic Sans MS', 25)

    # text
    title = corbelfont.render("Credits", True, WHITE)
    credits_1 = comicsansfont.render("Raquel Amaral", True, YELLOW)

    carryOn = True
    # Drawing the screen
    while carryOn:
        mouse = pygame.mouse.get_pos()  # Stores in a tuple all the positions of the mouse

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT:
                carryOn = False

        screen.fill(BLACK)

        screen.blit(title, (100, 100))
        screen.blit(credits_1, (100, 200))


        pygame.display.update()