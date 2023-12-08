import pygame
from button import Button


def instructions_(SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Display game instructions.

    Parameters
    ----------
        SCREEN_WIDTH : int
            the width of the game screen
        SCREEN_HEIGHT : int
            the height of the game screen
    """
    instructions_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Instructions")

    instructions_background = pygame.image.load("path_to_instructions_background_image.jpg").convert()
    instructions_background = pygame.transform.scale(instructions_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create an X button to return to the pause menu
    x_button = Button("X", SCREEN_WIDTH - 30, 10, 20, 20, font_size=20, text_color=(255, 255, 255), button_color=(0, 0, 0, 0))

    carry_on_instructions = True
    while carry_on_instructions:
        instructions_screen.blit(instructions_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carry_on_instructions = False
                carryOn = False  # To exit the entire game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carry_on_instructions = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x_button.is_clicked(event.pos):
                    carry_on_instructions = False

        pygame.display.flip()

    pygame.quit()
