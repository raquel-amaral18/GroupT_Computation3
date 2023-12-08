import pygame

from button import Button


def prompt_player_name():
    """
        Function for the player to input their name.

        Returns:
        -------
            str:
                The player's name
    """
    # Function to prompt for player's name
    pygame.font.init()

    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    MAASTRICHT_BLUE = (3, 23, 48)
    LIGHT_BLUE = (65, 163, 187)


    font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = LIGHT_BLUE
    color = color_inactive
    active = False
    text = ''

    # Create a return button in the top right corner
    return_button = Button("X", SCREEN_WIDTH - 100, 100, 50, 50, 50, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=100)

    # Enter
    enter_size = (40, 40)
    enter = pygame.image.load("Images/Extras/enter.png")
    enter = pygame.transform.scale(enter, enter_size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.is_clicked(event.pos):
                    from interface import interface
                    interface()

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

        screen.fill(MAASTRICHT_BLUE)
        return_button.draw(screen)
        username_text = font.render("Username:", True, pygame.Color('lightskyblue3'))
        screen.blit(username_text, (395, 290))

        # Render the current text inside box
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        # Enter
        screen.blit(enter, (550, 380))

        pygame.display.flip()
        clock.tick(30)


def user(name):
    """
        Loads the player's information if they already exist on the file 'hscore.txt' or adds a new player with default
        values if the name is not found.

        Parameters:
        -----------
            name : str
                the name of the player

        Returns:
        --------
            str:
                the name of the player. This name can already exist or be created in the function
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
        Retrieves the selected car from the file.

        Parameters:
        -----------
            name : str
                the name of the player

        Returns:
        --------
            int or None:
                the index of the selected car if the player is found, if the player was not found return None.
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
