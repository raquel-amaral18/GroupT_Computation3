import pygame
from button import Button
import config


def show_message(screen, message, position, font_size=30, color=(255, 0, 0)):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def car_2_purchase():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_number_tuple = number_tuple + (2,)

        # Removing 5 coins
        updated_coins = coins - 5

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_number_tuple, additional_value)

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))

def car_3_purchase():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_number_tuple = number_tuple + (3,)

        # Removing 5 coins
        updated_coins = coins - 10

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_number_tuple, additional_value)

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))

def car_4_purchase():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_number_tuple = number_tuple + (4,)

        # Removing 5 coins
        updated_coins = coins - 15

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_number_tuple, additional_value)

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))

def car_5_purchase():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, number_tuple, additional_value = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_number_tuple = number_tuple + (5,)

        # Removing 5 coins
        updated_coins = coins - 20

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_number_tuple, additional_value)

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))


def store(SCREEN_WIDTH, SCREEN_HEIGHT):
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

    # Function to display the user's coin count
    def display_coins(screen, coins, position, font_size=30, color=(255, 255, 255)):
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(f"Coins: {coins}", True, color)
        screen.blit(text_surface, position)
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
    car1_button = Button("5 Coins", 200, 220, 50, 50)
    car2_button = Button("10 Coins", 650, 220, 50, 50)
    car3_button = Button("15 coins", 200, 570, 50, 50)
    car4_button = Button("20 coins", 650, 570, 50, 50)

    # Main loop for the store
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
                elif car1_button.is_clicked(event.pos):
                    if user_coins >= 5 and (2 not in cars):
                        from interface import interface
                        car_2_purchase()
                        interface()
                    else:
                        message = "You need more coins"
                        show_message_flag = True
                elif car2_button.is_clicked(event.pos):
                    if user_coins >= 10 and (3 not in cars):
                        from interface import interface
                        car_3_purchase()
                        interface()
                    else:
                        message = "You need more coins"
                        show_message_flag = True
                elif car3_button.is_clicked(event.pos):
                    if user_coins >= 15 and (4 not in cars):
                        from interface import interface
                        car_4_purchase()
                        interface()
                    else:
                        message = "You need more coins"
                        show_message_flag = True
                elif car4_button.is_clicked(event.pos):
                    if user_coins >= 20 and (5 not in cars):
                        from interface import interface
                        car_5_purchase()
                        interface()
                    else:
                        message = "You need more coins"
                        show_message_flag = True

        # Drawing
        screen.blit(background, (0, 0))  # Draw background
        draw_cars()
        return_button.draw(screen)  # Draw the return button
        car1_button.draw(screen)  # Draw the return button
        car2_button.draw(screen)  # Draw the return button
        car3_button.draw(screen)  # Draw the return button
        car4_button.draw(screen)  # Draw the return button


        # Display coin count
        display_coins(screen, user_coins, (10, 10))

        #You Need more Coins message
        if show_message_flag:
            show_message(screen, message, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Update the display
        pygame.display.flip()

    pygame.quit()