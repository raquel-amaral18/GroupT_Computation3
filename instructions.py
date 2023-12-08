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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # colors
    MAASTRICHT_BLUE = (3, 23, 48)
    LIGHT_BLUE = (65, 163, 187)

    # Background
    background = pygame.image.load("Images/Design/instructions_pause.png")
    original_width, original_height = background.get_size()

    target_width = SCREEN_WIDTH
    target_height = int(original_height * (target_width / original_width))
    # Scale the image with the fixed aspect ratio
    background = pygame.transform.scale(background, (target_width, target_height))

    # Create an X button to return to the pause menu
    return_button = Button("X", SCREEN_WIDTH // 2, 630, 50, 50, 50, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=100)

    carry_on_instructions = True
    while carry_on_instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.is_clicked(event.pos):
                    carry_on_instructions = False

        screen.blit(background, (0, 0))

        return_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
