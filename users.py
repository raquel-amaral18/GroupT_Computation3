import pygame
import sys


def prompt_player_name():
    """
    Function for the player to input his/her name


    Returns:
        str: The player's name
    """
    # Function to prompt for player's name
    pygame.font.init()

    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    font = pygame.font.SysFont('Arial', 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text  # Return the text when Enter is pressed
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def user(name):
    """
    Loads the player's information if he already exists in the file 'hscore.txt' or adds a new player with default
    values if the name doesn't exist yet.


    Parameters:
        name (str): The name of the player.

    Returns:
        str: The name of the player. this name can already exist or be created in the function.
    """
    users = []

    # Loads the file
    try:
        with open('hscore.txt', 'r') as f:
            highscores = eval(f.read())
            users = list(highscores.keys())
    except (FileNotFoundError, SyntaxError):
        highscores = {}

    # Check if the user already exists
    if name in users:
        return name
    else:
        # Add the new user with all his stats at zero except the first car
        from database import highscore
        highscore(name, score=0, coins=0)
        return name


def chosen_car(name):
    """
    Retrieves the selected car for the player from the file.

    Parameters:
        name (str): The name of the player.

    Returns:
        int or None: The index of the selected car if the player is found, if there is not no player found return none.
    """
    # Load the existing high scores from the file
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        return None  # Return None if file doesn't exist or there's an error in reading

    # Check if the user exists in the high scores
    if name in high_scores:
        # Extract the selected car value at index 2
        existing_selected_car = high_scores[name][2]
        return existing_selected_car
    else:
        return None  # Return None if the user is not found
