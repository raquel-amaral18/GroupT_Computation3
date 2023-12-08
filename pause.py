import pygame
from button import Button


def display_pause_menu(screen):
    """
    Displays a pause menu overlay on the game screen.


    Parameters:
        screen (pygame.Surface): The pygame screen surface where the pause menu will be displayed.

    Returns:
        tuple: A tuple containing the Button objects for 'RESUME', 'HOW TO PLAY', and 'QUIT'.

    """
    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700

    # COLORS:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_BLUE = (65, 163, 187)

    # PAUSE MENU:
    # Draw a semi-transparent rectangle over the entire screen
    pause_overlay = pygame.Surface(screen.get_size()).convert_alpha()
    pygame.draw.rect(pause_overlay, (0, 0, 0, 128), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(pause_overlay, (0, 0))

    # Draw Pause Menu Text
    pause_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 50).render('PAUSED', True, WHITE)
    pause_rect = pause_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(pause_overlay, pause_rect)


    # Button dimensions and positioning
    BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
    vertical_spacing = 15
    start_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    start_y = pause_rect.bottom + 50  # Below 'Paused' text

    # Create buttons
    resume_button = Button("RESUME", start_x, start_y,
                           BUTTON_WIDTH, BUTTON_HEIGHT, font_size=30, text_color=BLACK, button_color=LIGHT_BLUE,
                           border_radius=0)
    how_to_play_button = Button("HOW TO PLAY", start_x, start_y + BUTTON_HEIGHT + vertical_spacing,
                                BUTTON_WIDTH, BUTTON_HEIGHT, font_size=30, text_color=BLACK, button_color=LIGHT_BLUE,
                                border_radius=0)
    quit_button = Button("QUIT", start_x, start_y + 2 * (BUTTON_HEIGHT + vertical_spacing),
                         BUTTON_WIDTH, BUTTON_HEIGHT, font_size=30, text_color=BLACK, button_color=LIGHT_BLUE,
                         border_radius=0)

    # Draw buttons
    resume_button.draw(screen)
    how_to_play_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.flip()

    return resume_button, how_to_play_button, quit_button
