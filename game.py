import random
# pygame.org
# pygame works as an old movie that never ends and repeats itself forever (until you die)
import pygame

from car import *
from coins import Coin
from messages import *


def game(SCREEN_WIDTH, SCREEN_HEIGHT):

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Amount of pixels that compose size of the window
    pygame.display.set_caption("Car Racing Game")


    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    RED = (249, 65, 68)

    # Font
    timer_font = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    level_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    coins_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30)

    messages_group = pygame.sprite.Group()

    # RIBBON - PAUSE, TIMER AND LIFE COUNTER:
    # Pause button
    pause_img = pygame.image.load("Images/pause.png").convert()
    pause_img = pygame.transform.scale(pause_img, (20, 20))

    # Lives
    heart_img = pygame.image.load("Images/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))

    # ENVIRONMENTS:
    # Forest
    forest_background = pygame.image.load("Images/forest.jpg")
    forest_background = pygame.transform.scale(forest_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Underwater
    underwater_background = pygame.image.load("Images/underwater.jpg").convert()
    underwater_background = pygame.transform.scale(underwater_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Space
    space_background = pygame.image.load("Images/space.jpeg").convert()
    space_background = pygame.transform.scale(space_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    # ROAD:
    num_lanes = 4  # Number of lanes
    road_width = 350  # Width of the road
    lane_width = road_width / num_lanes
    road_x = (SCREEN_WIDTH - road_width) // 2  # Distance from the road to the left of the screen


    # VEHICLES:
    # Player's car
    playerCar = PlayerCar("Images/00C.png", 50, 3)
    playerCar.rect.x = (SCREEN_WIDTH - playerCar.rect.width) // 2  # which column the car starts
    playerCar.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Opponent cars
    car1 = IncomingCars("Images/04C.png", 50, 2, road_x + (lane_width - 50) // 2)
    car2 = IncomingCars("Images/02C.png", 50, 4, road_x + lane_width + (lane_width - 50) // 2)
    car3 = IncomingCars("Images/05C.png", 50, 3, road_x + (2 * lane_width) + (lane_width - 50) // 2)
    car4 = IncomingCars("Images/07C.png", 50, 1, road_x + (3 * lane_width) + (lane_width - 50) // 2)

    all_sprites_list = pygame.sprite.Group()
    incoming_cars_list = pygame.sprite.Group()
    player_car_list = pygame.sprite.Group()

    # Coins
    coin_list = pygame.sprite.Group()

    all_sprites_list.add(playerCar, car1, car2, car3, car4)  # To show the cars on the screen
    incoming_cars_list.add(car1, car2, car3, car4)
    player_car_list.add(playerCar)

    carryOn = True

    # Controls whether the player's input should or not be considered
    movement_enabled = True

    # Game level
    level = 1
    last_minute = 0

    # Nr of coins
    coin_counter = 0

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # pygame.quit() checks if we pressed the red X (to leave the app)
                carryOn = False

        if movement_enabled:
            # Move player's car (with input from the user):
            if keys[pygame.K_LEFT]:
                playerCar.moveLeft(5)
                # Ensure the player's car stays within the left boundary of the road
                playerCar.rect.x = max(road_x, playerCar.rect.x)
            if keys[pygame.K_RIGHT]:
                playerCar.moveRight(5)
                # Ensure the player's car stays within the right boundary of the road
                playerCar.rect.x = min(road_x + road_width - playerCar.rect.width, playerCar.rect.x)
            if keys[pygame.K_UP]:
                playerCar.moveUp(5)
                # Ensure the player's car stays within the top boundary of the road
                playerCar.rect.y = max(0, playerCar.rect.y)
            if keys[pygame.K_DOWN]:
                playerCar.moveDown(5)
                # Ensure the player's car stays within the bottom boundary of the road
                playerCar.rect.y = min(SCREEN_HEIGHT - playerCar.rect.height, playerCar.rect.y)

        # Draw background
        screen.blit(forest_background, (0, 0))

        pygame.draw.rect(screen, GREY, [road_x, 0, road_width, SCREEN_HEIGHT])

        # Draw road markings
        middle_line_x = road_x + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x, 0], [middle_line_x, SCREEN_HEIGHT], 6)  # Central double line

        dashed_lines_x = [road_x + (i * lane_width) for i in range(1, num_lanes)]

        # Calculate the offset based on the player's car speed
        offset_y = (pygame.time.get_ticks() // 10) % 40  # A smaller divisor results in a faster movement
        for line_x in dashed_lines_x:
            for line_y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y + offset_y], [line_x, line_y + 20 + offset_y], 1)

        # Draw the cars
        incoming_cars_list.draw(screen)
        if playerCar.visible:
            player_car_list.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()


        #  car_collision_list = pygame.sprite.spritecollide(playerCar, incoming_cars_list, False)  # If True --> Pacman
        # if len(car_collision_list) > 0:
            # carryOn = False
        for car in incoming_cars_list:
            if not playerCar.ghost and pygame.sprite.collide_mask(playerCar, car) is not None:
                # Collision detected
                playerCar.lives -= 1
                show_message(messages_group, "-1", message_font, (playerCar.rect.x, playerCar.rect.y), RED)
                # Activate invincibility for 5 seconds after collision
                playerCar.ghost = True
                ghost_start_time = pygame.time.get_ticks()
                ghost_duration = 2000
                # Reset player's car position
                playerCar.rect.x = (SCREEN_WIDTH - playerCar.rect.width) // 2
                playerCar.rect.y = SCREEN_HEIGHT - 150
                # If no lives left --> end the game
                if playerCar.lives == 0:
                    carryOn = False

        # Update invincibility status based on elapsed time
        if playerCar.ghost:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar.ghost = False
                playerCar.visible = True
                movement_enabled = True
            else:
                playerCar.visible = (elapsed_time // toggle_interval) % 2 == 0

        all_sprites_list.update()

        # Draw the coins
        for line_x in dashed_lines_x:
            if line_x % 2 != 0 and random.random() < 0.005:  # Adjust the probability
                coin = Coin("Images/coin.png", 40, line_x - 20, -50)
                coin_list.add(coin)

        coin_list.update()
        coin_list.draw(screen)

        for coin in coin_list:
            coin.moveDown()

        # Check collisions with the player
        coin_collision_list = pygame.sprite.spritecollide(playerCar, coin_list, True)  # works like packman

        # Play coin sound for each collision
        # for coin_collision in coin_collision_list:
            # Add sound

        # Update coin counter
        coin_counter += len(coin_collision_list)

        # Display coin counter
        pygame.draw.rect(screen, BLACK, [740, 640, 110, 80], border_radius=24)

        coin_image = pygame.image.load("Images/coin.png")
        coin_image = pygame.transform.scale(coin_image, (30, 30))
        coin_counter_rect = coin_image.get_rect()
        coin_counter_rect.topleft = (760, 657)  # Adjust the coordinates based on your layout
        screen.blit(coin_image, coin_counter_rect)

        coin_counter_text = coins_font.render(f": {coin_counter}", True, WHITE)
        screen.blit(coin_counter_text, (800, 650))

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, 30])

        # Draw button
        screen.blit(pause_img, (15, 5))

        # Update timer
        elapsed_time = pygame.time.get_ticks() // 1000
        minutes, seconds = divmod(elapsed_time, 60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
                                                    #The quotient --> minutes, and the remainder --> seconds
                                                    # The result is unpacked into the minutes and seconds variables
        timer_text = timer_font.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate to center the text
        timer_x = (SCREEN_WIDTH - timer_text.get_width()) // 2
        screen.blit(timer_text, (timer_x, 5))

        # Level upgrade
        if minutes > last_minute:
            # Increase the level every minute
            level += 1
            last_minute = minutes

            # Increase playerCar speed
            playerCar.speed += 1

            # DISPLAY LEVEL CHANGE FOR 2 SECONDS
            # Draw a semi-transparent rectangle over the entire screen
            transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(transparent_surface, (0, 0, 0, 128), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(transparent_surface, (0, 0))
            # Display the level
            level_text = level_font.render(f"Level {level}", True, WHITE)
            level_x = (SCREEN_WIDTH - level_text.get_width()) // 2
            level_y = (SCREEN_HEIGHT - level_text.get_height()) // 2
            screen.blit(level_text, (level_x, level_y))

            pygame.display.flip()  # Update the full display Surface to the screen

            # Pause for 1 seconds
            pygame.time.wait(1000)
            # Clear the screen
            screen.blit(forest_background, (0, 0))
            pygame.display.flip()

        # Update lives
        for i in range(playerCar.lives):
            screen.blit(heart_img, (SCREEN_WIDTH - 40 - i * 35, 5))

        # Draw and update messages
        messages_group.draw(screen)
        messages_group.update()

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame
