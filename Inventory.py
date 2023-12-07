import pygame
from button import Button
import config


def show_message(screen, message, position, font_size=30, color=(255, 0, 0)):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)


def car_1_select():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_additional_value = 1

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), number_tuple, updated_additional_value)

        config.chosen_car = 0

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))

def car_2_select():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_additional_value = 2

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), number_tuple, updated_additional_value)

        config.chosen_car = 1

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))
def car_3_select():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_additional_value = 3

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), number_tuple, updated_additional_value)

        config.chosen_car = 2

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))

def car_4_select():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_additional_value = 4

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), number_tuple, updated_additional_value)

        config.chosen_car = 3

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))

def car_5_select():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_additional_value = 5

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), number_tuple, updated_additional_value)

        config.chosen_car = 4

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))


def inventory(SCREEN_WIDTH, SCREEN_HEIGHT):
    # Initialize Pygame
    pygame.init()

    # Load the existing high scores from the file
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}  # Initialize an empty dictionary if file

    #CURRENT USER
    # Extract the high score data for the current user
    if config.username in high_scores:
        user_data = high_scores[config.username]
        user_score, user_coins, cars, user_additional_value = user_data[0][0], user_data[0][1], user_data[1], user_data[2]
    else:
        user_score = user_coins = user_additional_value = None  # Default values if the user is not found


    # Set the screen dimensions (adjust as needed)
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load background image (replace 'BackgroundStore.png' with your actual image path)
    background = pygame.image.load('Images/stars&planets.png')

    # Load car images and scale them (replace 'car_image_x.png' with your actual image paths)
    car_images = [pygame.transform.scale(pygame.image.load('Images/04C.png'), (50, 70)),
                  pygame.transform.scale(pygame.image.load('Images/02C.png'), (50, 70)),
                  pygame.transform.scale(pygame.image.load('Images/05C.png'), (50, 70)),
                  pygame.transform.scale(pygame.image.load('Images/07C.png'), (50, 70))]

    car0 = pygame.transform.scale(pygame.image.load('Images/00C.png'), (50, 70))


    # Function to draw the begginer car in the middle of the screen
    def draw_car0_center():
        car_width, car_height = 50, 70  # Width and height of the car image
        center_x = SCREEN_WIDTH // 2 - car_width // 2
        center_y = SCREEN_HEIGHT // 2 - car_height // 2
        screen.blit(car0, (center_x, center_y))


    # Function to draw cars on the screen
    def draw_cars():
        num_columns = 2
        num_rows = 2
        car_width, car_height = 50, 70  # Width and height of the car images

        # Calculate spacing and starting positions
        column_spacing = SCREEN_WIDTH // num_columns
        row_spacing = SCREEN_HEIGHT // num_rows
        start_x = (column_spacing - car_width) // 2
        start_y = (row_spacing - car_height) // 2

        for i, img in enumerate(car_images):
            x = start_x + (i % num_columns) * column_spacing
            y = start_y + (i // num_columns) * row_spacing
            screen.blit(img, (x, y))

    # Create a return button in the top right corner
    return_button = Button("Return", SCREEN_WIDTH - 110, 10, 100, 50)
    car0_button = Button("Select", SCREEN_WIDTH // 2 - 22, SCREEN_HEIGHT // 2 + 40 , 50, 50)
    car1_button = Button("Select", 200, 220, 50, 50)
    car2_button = Button("Select", 650, 220, 50, 50)
    car3_button = Button("Select", 200, 570, 50, 50)
    car4_button = Button("Select", 650, 570, 50, 50)

    # Main loop for the inventory
    running = True
    show_message_flag = False
    message = ""
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_message_flag = False  # Reset message flag
                # Check if the return button is clicked
                if return_button.is_clicked(event.pos):
                    from interface import interface
                    interface()
                elif car0_button.is_clicked(event.pos):
                    if 1 in cars:
                        from interface import interface
                        car_1_select()
                        interface()
                elif car1_button.is_clicked(event.pos):
                    if 2 in cars:
                        from interface import interface
                        car_2_select()
                        interface()
                    else:
                        message = "Car not purchased"
                        show_message_flag = True
                elif car2_button.is_clicked(event.pos):
                    if 3 in cars:
                        from interface import interface
                        car_3_select()
                        interface()
                    else:
                        message = "Car not purchased"
                        show_message_flag = True
                elif car3_button.is_clicked(event.pos):
                    if 4 in cars:
                        from interface import interface
                        car_4_select()
                        interface()
                    else:
                        message = "Car not purchased"
                        show_message_flag = True
                elif car4_button.is_clicked(event.pos):
                    if 5 in cars:
                        from interface import interface
                        car_5_select()
                        interface()
                    else:
                        message = "Car not purchased"
                        show_message_flag = True

        # Drawing
        screen.blit(background, (0, 0))  # Draw background
        draw_cars()
        draw_car0_center()  # Draw beginner car in the center

        # DRAW BUTTONS
        return_button.draw(screen)
        car0_button.draw(screen)
        car1_button.draw(screen)
        car2_button.draw(screen)
        car3_button.draw(screen)
        car4_button.draw(screen)

        #Purchase Message
        if show_message_flag:
            show_message(screen, message, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Update the display
        pygame.display.flip()

    pygame.quit()