import pygame
from button import Button

import config


def car_0_select():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        updated_selected_car = 0

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), inventory_cars, updated_selected_car)

        config.chosen_car = 0

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))


def car_1_select():
    try:
        with open('hscore.txt', 'r') as f:
            high_scores = eval(f.read())
    except (FileNotFoundError, SyntaxError):
        high_scores = {}

    if config.username in high_scores:
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        updated_selected_car = 1

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), inventory_cars, updated_selected_car)

        config.chosen_car = 1

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
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        updated_selected_car = 2

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), inventory_cars, updated_selected_car)

        config.chosen_car = 2

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
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        updated_selected_car = 3

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), inventory_cars, updated_selected_car)

        config.chosen_car = 3

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
        score_coins, inventory_cars, selected_car = high_scores[config.username]
        score, coins = score_coins

        updated_selected_car = 4

        # Update the dictionary entry
        high_scores[config.username] = ((score, coins), inventory_cars, updated_selected_car)

        config.chosen_car = 4

        # Write the updated dictionary back to the file
        with open('hscore.txt', 'w') as f:
            f.write(repr(high_scores))


def inventory(SCREEN_WIDTH, SCREEN_HEIGHT):
    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    MAASTRICHT_BLUE = (3, 23, 48)
    LIGHT_BLUE = (65, 163, 187)
    RED = (249, 65, 68)

    # Load the existing high scores from hscore.txt
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


    # BACKGROUND:
    background = pygame.image.load('Images/Design/stars&planets.png')

    # CAR IMAGES:
    car_width = 100
    car_images = []
    distance_between_cars = 70
    start_x = 50

    for image_path in ['Images/Vehicles/PlayerCar/00C.png', 'Images/Vehicles/PlayerCar/02C.png',
                       'Images/Vehicles/PlayerCar/04C.png', 'Images/Vehicles/PlayerCar/05C.png',
                       'Images/Vehicles/PlayerCar/06C.png']:
        original_image = pygame.image.load(image_path)
        aspect_ratio = original_image.get_width() / original_image.get_height()
        scaled_image = pygame.transform.scale(original_image, (car_width, int(car_width / aspect_ratio)))
        car_images.append(scaled_image)


    # Create a return button in the top right corner
    return_button = Button("X", SCREEN_WIDTH - 100, 100, 50, 50, 50, MAASTRICHT_BLUE, LIGHT_BLUE, border_radius=100)

    # SELECTION BUTTONS:
    # Map between button index (dynamic) and car selection function
    car_button_mapping = {
        0: car_0_select,
        1: car_1_select,
        2: car_2_select,
        3: car_3_select,
        4: car_4_select,
    }
    # Create buttons only for purchased cars, excluding choosen car (0 by default)
    # Map between button index (dynamic) and car buttons
    car_buttons_mapping = {
        i: Button("Select", start_x + i * (car_width + 70), 500, 100, 50, 30, MAASTRICHT_BLUE, LIGHT_BLUE,
                  border_radius=12)
        if (i in inventory_cars and i != config.chosen_car) else None
        for i in range(len(car_images))
    }

    # Main loop for the inventory
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the return button is clicked
                if return_button.is_clicked(event.pos):
                    from interface import interface
                    interface()

                # Check if any car button is clicked
                for i, car_button in car_buttons_mapping.items():
                    if car_button is not None and car_button.is_clicked(event.pos):
                        selected_car_number = i
                        # Call the corresponding car selection function
                        car_button_mapping[selected_car_number]()

        screen.blit(background, (0, 0))  # Background

        # Clear the existing buttons
        car_buttons_mapping.clear()

        for i, car_image in enumerate(car_images):
            x = start_x + i * (car_width + distance_between_cars)
            y = (screen.get_height() - car_image.get_height()) // 2

            # Check if the car is selectable (purchased or free)
            if i in inventory_cars:
                # Draw a rectangle around the selected car (based on config.chosen_car)
                if config.chosen_car == i:
                    pygame.draw.rect(screen, LIGHT_BLUE, (x - 10, y - 10, car_width + 20, car_image.get_height() + 20),
                                     0, border_radius=24)
                    pygame.draw.rect(screen, MAASTRICHT_BLUE, (x - 8, y - 8, car_width + 16, car_image.get_height() + 16),
                                     0, border_radius=24)
                # Draw the cars
                screen.blit(car_image, (x, y))
                # Create a new button for the car, excluding the selected car
                if config.chosen_car != i:
                    car_buttons_mapping[i] = Button("Select", x, 500, 100, 50, 30, MAASTRICHT_BLUE,
                                                    LIGHT_BLUE, border_radius=12)
            else:
                # Darken the appearance of the car (maintaining shape)
                darkened_surface = car_image.convert_alpha()
                darkened_surface.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
                screen.blit(darkened_surface, (x, y))

        # DRAW BUTTONS
        return_button.draw(screen)
        for car_button in car_buttons_mapping.values():
            if car_button is not None:
                car_button.draw(screen)


        # Update the display
        pygame.display.flip()

    pygame.quit()
