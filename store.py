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

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    MAASTRICHT_BLUE = (3, 23, 48)
    LIGHT_BLUE = (65, 163, 187)
    RED = (249, 65, 68)


    # BACKGROUND:
    # Load background image (replace 'BackgroundStore.png' with your actual image path)
    background = pygame.image.load('Images/Design/stars&planets.png')

    # CURRENT USER INFORMATION:
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
        user_score = user_coins = user_additional_value = 0  # Default values if the user is not found

    # USER COINS
    # Function to display the user's coin count
    def display_coins(scree, coins, position, color=(255, 255, 255)):
        # Coins
        coin_image = pygame.image.load("Images/Extras/coin.png")
        coin_image = pygame.transform.scale(coin_image, (30, 30))
        coin_counter_rect = coin_image.get_rect()
        coin_counter_rect.topleft = (20, 10)

        pygame.draw.rect(screen, MAASTRICHT_BLUE, [10, 0, 200, 50], border_radius=12)
        screen.blit(coin_image, coin_counter_rect)

        coin_counter_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).render(f": {coins}", True, color)
        screen.blit(coin_counter_text, (60, 5))


    # Load car images
    car_width = 100
    car_images = []

    for image_path in ['Images/Vehicles/PlayerCar/02C.png', 'Images/Vehicles/PlayerCar/04C.png',
                       'Images/Vehicles/PlayerCar/05C.png', 'Images/Vehicles/PlayerCar/06C.png']:
        original_image = pygame.image.load(image_path)
        aspect_ratio = original_image.get_width() / original_image.get_height()
        scaled_image = pygame.transform.scale(original_image, (car_width, int(car_width / aspect_ratio)))
        car_images.append(scaled_image)


    # Create a return button in the top right corner
    return_button = Button("X", SCREEN_WIDTH - 200, 100, 50, 50, 50, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=100)
    car1_button = Button("5 Coins", 145, 500, 100, 50, 30, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=12)
    car2_button = Button("10 Coins", 315, 500, 100, 50, 30, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=12)
    car3_button = Button("15 coins", 485, 500, 100, 50, 30, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=12)
    car4_button = Button("20 coins", 650, 500, 100, 50, 30, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=12)

    # Main loop for the store
    running = True
    show_message_flag = False
    message_start_time = 0
    message = ""

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
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
                        show_message_flag = True
                        message_start_time = pygame.time.get_ticks()
                elif car2_button.is_clicked(event.pos):
                    if user_coins >= 10 and (3 not in cars):
                        from interface import interface
                        car_3_purchase()
                        interface()
                    else:
                        show_message_flag = True
                        message_start_time = pygame.time.get_ticks()
                elif car3_button.is_clicked(event.pos):
                    if user_coins >= 15 and (4 not in cars):
                        from interface import interface
                        car_4_purchase()
                        interface()
                    else:
                        show_message_flag = True
                        message_start_time = pygame.time.get_ticks()
                elif car4_button.is_clicked(event.pos):
                    if user_coins >= 20 and (5 not in cars):
                        from interface import interface
                        car_5_purchase()
                        interface()
                    else:
                        show_message_flag = True
                        message_start_time = pygame.time.get_ticks()

        # Drawing
        screen.blit(background, (0, 0))  # Draw background

        distance_between_cars = 70
        total_width = (car_width + distance_between_cars) * len(car_images) - distance_between_cars
        start_x = (screen.get_width() - total_width) // 2


        for i, car_image in enumerate(car_images):
            x = start_x + i * (car_width + distance_between_cars)
            y = (screen.get_height() - car_image.get_height()) // 2
            screen.blit(car_image, (x, y))

        return_button.draw(screen)  # Draw the return button
        car1_button.draw(screen)  # Draw the return button
        car2_button.draw(screen)  # Draw the return button
        car3_button.draw(screen)  # Draw the return button
        car4_button.draw(screen)  # Draw the return button


        # Display coin count
        display_coins(screen, user_coins, (10, 10))

        #You Need more Coins message
        if show_message_flag:
            message_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 50).\
                render("You need more coins!", True, RED)
            message_x = (SCREEN_WIDTH - message_text.get_width()) // 2
            message_y = (SCREEN_HEIGHT - message_text.get_height()) // 2

            # Draw a black ribbon under the message text
            ribbon_rect = pygame.Rect(0, 300, SCREEN_WIDTH, 100)
            pygame.draw.rect(screen, MAASTRICHT_BLUE, ribbon_rect)

            screen.blit(message_text, (message_x, message_y))

            pygame.display.flip()

            # Check if the duration has passed
            current_time = pygame.time.get_ticks()
            if current_time - message_start_time >= 3000:
                show_message_flag = False  # Hide the message after waiting

        # Update the display
        pygame.display.flip()

    pygame.quit()
