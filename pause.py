import pygame


def pause_menu(SCREEN_WIDTH, SCREEN_HEIGHT, elapsed_time, lives, coin_counter):

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # COLORS
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    MAASTRICHT_BLUE = (3, 23, 48)
    LIGHT_BLUE = (65, 163, 187)
    DARK_BLUE = (27, 148, 153)


    # TEXT
    # buttons information
    game_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("RESUME", True, BLACK)
    instructions_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("HOW TO PLAY?", True, BLACK)
    quit_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render("QUIT", True, BLACK)


    # BACKGROUND
    # Background
    background = pygame.image.load("Images/Pause/pause_background.png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))


    # LOGO
    logo = pygame.image.load("Images/Pause/logo.png")
    aspect_ratio = logo.get_width() / logo.get_height()
    scaled_height = int(200 / aspect_ratio)
    logo = pygame.transform.scale(logo, (200, scaled_height))


    # BUTTONS
    BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

    while True:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0]
                        <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH
                        and 350 <= mouse[1] <= 350 + BUTTON_HEIGHT):
                    from game import game
                    game(SCREEN_WIDTH, SCREEN_HEIGHT, elapsed_time, lives, coin_counter)

                elif SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0] \
                        <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH \
                        and 420 <= mouse[1] <= 420 + BUTTON_HEIGHT:
                    from interface import instructions1_
                    instructions1_(SCREEN_WIDTH, SCREEN_HEIGHT)
                    pass

                elif SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0]\
                        <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH \
                        and 490 <= mouse[1] <= 490 + BUTTON_HEIGHT:
                    from interface import interface
                    interface()
                    pass

        # Draw background
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, MAASTRICHT_BLUE, [SCREEN_WIDTH // 2 - 450 // 2, 50, 450, 550], border_radius=24)
        pygame.draw.rect(screen, LIGHT_BLUE, [SCREEN_WIDTH // 2 - 450 // 2, 50, 450, 550], border_radius=24, width=4)

        # Draw logo
        screen.blit(logo, (SCREEN_WIDTH // 2 - 200 // 2, 0))


        # DRAW BUTTONS
        # Return to the game
        pygame.draw.rect(screen, DARK_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 355, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        pygame.draw.rect(screen,
                         DARK_BLUE if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0]
                                       <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH
                                       and 350 <= mouse[1] <= 350 + BUTTON_HEIGHT)
                         else LIGHT_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        text_x = (SCREEN_WIDTH // 2 - game_text.get_width() // 2)
        text_y = (350 + BUTTON_HEIGHT // 2 - game_text.get_height() // 2)
        screen.blit(game_text, (text_x, text_y))

        # Instructions panel
        pygame.draw.rect(screen, DARK_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 425, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        pygame.draw.rect(screen,
                         DARK_BLUE if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0]
                                       <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH
                                       and 420 <= mouse[1] <= 420 + BUTTON_HEIGHT)
                         else LIGHT_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 420, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        text_x = (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2)
        text_y = (420 + BUTTON_HEIGHT // 2 - instructions_text.get_height() // 2)
        screen.blit(instructions_text, (text_x, text_y))

        # Back to interface
        pygame.draw.rect(screen, DARK_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 495, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        pygame.draw.rect(screen,
                         DARK_BLUE if (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 <= mouse[0]
                                       <= SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2 + BUTTON_WIDTH
                                       and 490 <= mouse[1] <= 490 + BUTTON_HEIGHT)
                         else LIGHT_BLUE,
                         [SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 490, BUTTON_WIDTH, BUTTON_HEIGHT], border_radius=24)
        text_x = (SCREEN_WIDTH // 2 - quit_text.get_width() // 2)
        text_y = (490 + BUTTON_HEIGHT // 2 - quit_text.get_height() // 2)
        screen.blit(quit_text, (text_x, text_y))

        pygame.display.flip()
