import pygame
from button import Button

def display_pause_menu(screen):
    """
    Function to display the pause menu
    """

    WHITE = (255, 255, 255)
    # Pause menu overlay
    pause_overlay = pygame.Surface(screen.get_size()).convert_alpha()
    pause_overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(pause_overlay, (0, 0))

    # Draw Pause Menu Text
    font = pygame.font.SysFont('monospace', 50, bold=True)
    text = font.render('Paused', True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)


    # Button dimensions and positioning
    button_width, button_height = 100, 50
    horizontal_spacing, vertical_spacing = 20, 15
    total_width = 2 * button_width + horizontal_spacing
    start_x = (screen.get_width() - total_width) / 2
    start_y = text_rect.bottom + 50  # Below 'Paused' text

    # Create buttons
    resume_button = Button("Resume", start_x, start_y, button_width, button_height)
    how_to_play_button = Button("How to Play", start_x + button_width + horizontal_spacing, start_y, button_width, button_height)
    credits_button = Button("Credits", start_x, start_y + button_height + vertical_spacing, button_width, button_height)
    quit_button = Button("Quit", start_x + button_width + horizontal_spacing, start_y + button_height + vertical_spacing, button_width, button_height)

    # Draw buttons
    resume_button.draw(screen)
    how_to_play_button.draw(screen)
    credits_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.flip()

    return resume_button, how_to_play_button, credits_button, quit_button