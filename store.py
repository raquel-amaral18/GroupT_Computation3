import pygame
from button import Button
import config


def car_1_purchase():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        # Adding car number 1 to the tuple
        updated_inventory_cars = inventory_cars + (1,)

        # Removing 50 coins
        updated_coins = coins - 50

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_inventory_cars, selected_car)

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))


def car_2_purchase():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        # Adding number 2 to the tuple
        updated_inventory_cars = inventory_cars + (2,)

        # Removing 100 coins
        updated_coins = coins - 100

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_inventory_cars, selected_car)

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
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        # Adding number 3 to the tuple
        updated_inventory_cars = inventory_cars + (3,)

        # Removing 150 coins
        updated_coins = coins - 150

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_inventory_cars, selected_car)

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
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        # Adding number 4 to the tuple
        updated_inventory_cars = inventory_cars + (4,)

        # Removing 200 coins
        updated_coins = coins - 200

        # Update the dictionary entry
        high_scores[config.username] = ((score, updated_coins), updated_inventory_cars, selected_car)

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
    background = pygame.image.load('Images/Design/stars&planets.png')

    # CURRENT USER INFORMATION:
    # Load the existing high scores from the file
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}  # Initialize an empty dictionary if file empty/not working

    #CURRENT USER
    # Extract the high score data for the current user
    if config.username in high_scores:
        user_data = high_scores[config.username]
        user_score, user_coins, inventory_cars, user_selected_car = user_data[0][0], user_data[0][1], user_data[1], user_data[2]
    else:
        user_score = user_coins = user_selected_car = 0  # Default values if the user is not found
        inventory_cars = (0,)  # Default value for inventory_cars when user is not found

    # USER COINS
    # Function to display the user's coin count
    def display_coins(screen, coins):
        # Coins
        coin_image = pygame.image.load("Images/Extras/coin.png")
        coin_image = pygame.transform.scale(coin_image, (30, 30))
        coin_counter_rect = coin_image.get_rect()
        coin_counter_rect.topleft = (20, 10)

        pygame.draw.rect(screen, MAASTRICHT_BLUE, [10, 0, 200, 50], border_radius=12)
        screen.blit(coin_image, coin_counter_rect)

        coin_counter_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30).\
            render(f": {coins}", True, (255, 255, 255))
        screen.blit(coin_counter_text, (60, 5))


    # CARS:
    car_width = 100
    car_images = []
    distance_between_cars = 70
    total_width = (car_width + distance_between_cars) * len(car_images) - distance_between_cars
    start_x = (screen.get_width() - total_width) // 2

    for image_path in ['Images/Vehicles/PlayerCar/02C.png', 'Images/Vehicles/PlayerCar/04C.png',
                       'Images/Vehicles/PlayerCar/05C.png', 'Images/Vehicles/PlayerCar/06C.png']:
        original_image = pygame.image.load(image_path)
        aspect_ratio = original_image.get_width() / original_image.get_height()
        scaled_image = pygame.transform.scale(original_image, (car_width, int(car_width / aspect_ratio)))
        car_images.append(scaled_image)

    return_button = Button("X", SCREEN_WIDTH - 200, 100, 50, 50, 50, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=100)

    # SELECTION BUTTONS:
    # Map between button index (dynamic) and car selection function
    purchase_button_mapping = {
        1: car_1_purchase,
        2: car_2_purchase,
        3: car_3_purchase,
        4: car_4_purchase
    }

    # Map between button index (dynamic) and price tag buttons
    price_tags_button_mapping = {
        i: Button(f"{i * 50} Coins", start_x + i * (car_width + distance_between_cars), 500, 120, 50, 30,
                  MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=12)
        if i not in inventory_cars else None
        for i in range(1, len(car_images) + 1)
    }

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

                for i, price_tag_button in price_tags_button_mapping.items():
                    if price_tag_button is not None and price_tag_button.is_clicked(event.pos):
                        selected_car_number = i
                        # Call the corresponding car purchase function
                        purchase_button_mapping[selected_car_number]()

        # Drawing
        screen.blit(background, (0, 0))  # Draw background

        distance_between_cars = 70
        total_width = (car_width + distance_between_cars) * len(car_images) - distance_between_cars
        start_x = (screen.get_width() - total_width) // 2


        for i, car_image in enumerate(car_images):
            x = start_x + i * (car_width + distance_between_cars)
            y = (screen.get_height() - car_image.get_height()) // 2
            screen.blit(car_image, (x, y))

            # Check if the car is in the inventory and display message
            if i + 1 in inventory_cars:  # Have in mind that 0 is not displayed in store, but exists
                message_text = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 20). \
                    render("Already Purchased", True, (255, 255, 255))
                message_x = x + (car_width - message_text.get_width()) // 2
                message_y = y + car_image.get_height() + 10
                screen.blit(message_text, (message_x, message_y))

            elif i+1 not in inventory_cars and user_coins < ((i + 1) * 50):
                # Darken the appearance of the car (maintaining shape)
                darkened_surface = car_image.convert_alpha()
                darkened_surface.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
                screen.blit(darkened_surface, (x, y))

        # DRAW BUTTONS
        return_button.draw(screen)
        for car_button in price_tags_button_mapping.values():
            if car_button is not None:
                car_button.draw(screen)


        # Display coin count
        display_coins(screen, user_coins)

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
