import random
# pygame.org
# pygame works as an old movie that never ends and repeats itself forever (until you die)
import pygame

from car import *
from coins import Coin
from messages import *


def gameMP(SCREEN_WIDTH, SCREEN_HEIGHT):

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOWdd:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Amount of pixels that compose size of the window
    pygame.display.set_caption("Car Racing Game")


    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    RED = (249, 65, 68)
    BLUE = (0, 180, 216)

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
    forest_background = pygame.image.load("Images/forest.jpg").convert()
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
    # Player 1 car
    playerCar1 = PlayerCar("Images/00C.png", 50, 2)
    playerCar1.rect.x = (SCREEN_WIDTH - playerCar1.rect.width) // 2 - 50  # which column the car starts
    playerCar1.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Player 2 car
    playerCar2 = PlayerCar("Images/01C.png", 50, 2)
    playerCar2.rect.x = (SCREEN_WIDTH - playerCar2.rect.width) // 2 + 50  # which column the car starts
    playerCar2.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Opponent cars
    car1 = IncomingCars("Images/03C.png", 50, 2, road_x + (lane_width - 50) // 2)
    car2 = IncomingCars("Images/02C.png", 50, 4, road_x + lane_width + (lane_width - 50) // 2)
    car3 = IncomingCars("Images/05C.png", 50, 3, road_x + (2 * lane_width) + (lane_width - 50) // 2)
    car4 = IncomingCars("Images/07C.png", 50, 1, road_x + (3 * lane_width) + (lane_width - 50) // 2)

    all_sprites_list = pygame.sprite.Group()
    incoming_cars_list = pygame.sprite.Group()
    player_car1_list = pygame.sprite.Group()
    player_car2_list = pygame.sprite.Group()

    # Coins
    coin_list = pygame.sprite.Group()

    all_sprites_list.add(playerCar1, playerCar2, car1, car2, car3, car4)  # To show the cars on the screen
    incoming_cars_list.add(car1, car2, car3, car4)
    player_car1_list.add(playerCar1)
    player_car2_list.add(playerCar2)

    carryOn = True

    # Controls whether the player 1 input should or not be considered
    movement_enabled1 = True
    # Controls whether the player 2 input should or not be considered
    movement_enabled2 = True

    # Game level
    level = 1
    last_minute = 0

    # Nr of coins
    coin_counter1 = 0
    coin_counter2 = 0

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # pygame.quit() checks if we pressed the red X (to leave the app)
                carryOn = False

        if movement_enabled1:
            # Move player 1 car (with input from the user):
            if keys[pygame.K_LEFT]:
                # Ensure the player's car stays within the left boundary of the road and doesn't collide with playerCar2
                if playerCar1.rect.x - playerCar1.speed > road_x \
                        and not playerCar1.rect.colliderect(playerCar2.rect.move(playerCar1.speed, 0)):
                    playerCar1.moveLeft(5)
            if keys[pygame.K_RIGHT]:
                # Ensure the player's car stays within the right boundary of the road and doesn't collide with playerCar2
                if playerCar1.rect.x + playerCar1.speed < road_x + road_width - playerCar1.rect.width \
                        and not playerCar1.rect.colliderect(playerCar2.rect.move(-playerCar1.speed, 0)):
                    playerCar1.moveRight(5)
            if keys[pygame.K_UP]:
                # Ensure the player's car stays within the top boundary of the road
                if playerCar1.rect.y - playerCar1.speed > 0 \
                        and not playerCar1.rect.colliderect(playerCar2.rect.move(0, playerCar1.speed)):
                    playerCar1.moveUp(5)
            if keys[pygame.K_DOWN]:
                # Ensure the player's car stays within the bottom boundary of the road
                if playerCar1.rect.y + playerCar1.speed < SCREEN_HEIGHT - playerCar1.rect.height \
                        and not playerCar1.rect.colliderect(playerCar2.rect.move(0, -playerCar1.speed)):
                    playerCar1.moveDown(5)

        if movement_enabled2:
            if keys[pygame.K_a]:
                # Ensure the player's car stays within the left boundary of the road and doesn't collide with playerCar1
                if playerCar2.rect.x - playerCar2.speed > road_x \
                        and not playerCar2.rect.colliderect(playerCar1.rect.move(playerCar2.speed, 0)):
                    playerCar2.moveLeft(5)
            if keys[pygame.K_d]:
                # Ensure the player's car stays within the right boundary of the road and doesn't collide with playerCar1
                if playerCar2.rect.x + playerCar2.speed < road_x + road_width - playerCar2.rect.width \
                        and not playerCar2.rect.colliderect(playerCar1.rect.move(-playerCar2.speed, 0)):
                    playerCar2.moveRight(5)
            if keys[pygame.K_w]:
                # Ensure the player's car stays within the top boundary of the road
                if playerCar2.rect.y - playerCar2.speed > 0 \
                        and not playerCar2.rect.colliderect(playerCar1.rect.move(0, playerCar2.speed)):
                    playerCar2.moveUp(5)
            if keys[pygame.K_s]:
                # Ensure the player's car stays within the bottom boundary of the road
                if playerCar2.rect.y + playerCar2.speed < SCREEN_HEIGHT - playerCar2.rect.height \
                        and not playerCar2.rect.colliderect(playerCar1.rect.move(0, -playerCar2.speed)):
                    playerCar2.moveDown(5)

        # Draw background
        screen.blit(forest_background, (0, 0))

        pygame.draw.rect(screen, GREY, [road_x, 0, road_width, SCREEN_HEIGHT])

        # Draw road markings
        middle_line_x = road_x + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x, 0], [middle_line_x, SCREEN_HEIGHT], 6)  # Central line

        dashed_lines_x = [road_x + (i * lane_width) for i in range(1, num_lanes)]

        # Calculate the offset based on the player's car speed
        offset_y = (pygame.time.get_ticks() // 10) % 40
        for line_x in dashed_lines_x:
            for line_y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y + offset_y], [line_x, line_y + 20 + offset_y], 1)

        # Draw the cars
        incoming_cars_list.draw(screen)
        if playerCar1.visible:
            player_car1_list.draw(screen)
        if playerCar2.visible:
            player_car2_list.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar1.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()

        # Handle collisions with PlayerCar1
        for car in incoming_cars_list:
            if not playerCar1.ghost and pygame.sprite.collide_mask(playerCar1, car) is not None:
                # Collision detected
                playerCar1.lives -= 1
                show_message(messages_group, "-1", message_font, (playerCar1.rect.x, playerCar1.rect.y), BLUE)
                # Activate invincibility for 5 seconds after collision
                playerCar1.ghost = True
                ghost_start_time = pygame.time.get_ticks()
                ghost_duration = 2000
                # Reset player's car position
                playerCar1.rect.x = (SCREEN_WIDTH - playerCar1.rect.width) // 2 - 50
                playerCar1.rect.y = SCREEN_HEIGHT - 150
                # If no lives left --> end the game
                if playerCar1.lives == 0:
                    carryOn = False

        # Handle collisions with PlayerCar1
        for car in incoming_cars_list:
            if not playerCar2.ghost and pygame.sprite.collide_mask(playerCar2, car) is not None:
                # Collision detected for player 2
                playerCar2.lives -= 1
                show_message(messages_group, "-1", message_font, (playerCar2.rect.x, playerCar2.rect.y), RED)
                # Activate invincibility for 5 seconds after collision for player 2
                playerCar2.ghost = True
                ghost_start_time_player2 = pygame.time.get_ticks()
                ghost_duration_player2 = 2000
                # Reset player 2's car position
                playerCar2.rect.x = (SCREEN_WIDTH - playerCar2.rect.width) // 2 + 50
                playerCar2.rect.y = SCREEN_HEIGHT - 150
                # If no lives left for player 2 --> end the game
                if playerCar2.lives == 0:
                    carryOn = False

        # Update invincibility status based on elapsed time
        #Player car 1
        if playerCar1.ghost:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar1.ghost = False
                playerCar1.visible = True
            else:
                playerCar1.visible = (elapsed_time // toggle_interval) % 2 == 0

        #Player car 2
        if playerCar2.ghost:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time_player2
            toggle_interval = 200
            if elapsed_time >= ghost_duration_player2:
                playerCar2.ghost = False
                playerCar2.visible = True
            else:
                playerCar2.visible = (elapsed_time // toggle_interval) % 2 == 0

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

        # Check collisions with the players
        coin_collision_list1 = pygame.sprite.spritecollide(playerCar1, coin_list, True)
        coin_collision_list2 = pygame.sprite.spritecollide(playerCar2, coin_list, True)
        # Update coin counter
        coin_counter1 += len(coin_collision_list1)
        coin_counter2 += len(coin_collision_list2)

        if coin_counter1 % 10 == 0 and coin_counter1 > 0:
            playerCar1.lives += 1

        if coin_counter2 % 10 == 0 and coin_counter2 > 0:
            playerCar2.lives += 1

        # Display coin counters
        pygame.draw.rect(screen, BLACK, [50, 640, 110, 80], border_radius=24)
        pygame.draw.rect(screen, BLACK, [740, 640, 110, 80], border_radius=24)

        coin_image = pygame.image.load("Images/coin.png")
        coin_image = pygame.transform.scale(coin_image, (30, 30))
        coin_counter_rect1 = coin_image.get_rect()
        coin_counter_rect2 = coin_image.get_rect()
        coin_counter_rect1.topleft = (70, 657)
        coin_counter_rect2.topleft = (760, 657)
        screen.blit(coin_image, coin_counter_rect1)
        screen.blit(coin_image, coin_counter_rect2)

        coin_counter_text = coins_font.render(f": {coin_counter1}", True, WHITE)
        screen.blit(coin_counter_text, (110, 650))
        coin_counter_text = coins_font.render(f": {coin_counter2}", True, WHITE)
        screen.blit(coin_counter_text, (800, 650))

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, 30])

        # Draw button
        screen.blit(pause_img, (380, 5))

        # Update timer
        elapsed_time = pygame.time.get_ticks() // 1000
        minutes, seconds = divmod(elapsed_time, 60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
                                                    #The quotient --> minutes, and the remainder --> seconds
                                                    # The result is unpacked into the minutes and seconds variables
        timer_text = timer_font.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate and center the text
        timer_x = (SCREEN_WIDTH - timer_text.get_width()) // 2
        screen.blit(timer_text, (timer_x, 0))

        # Level upgrade
        if minutes > last_minute:
            # Increase the level every minute
            level += 1
            last_minute = minutes

            # Increase players speed
            playerCar1.speed += 1
            playerCar2.speed += 1

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
        #Player 1 lives
        for i in range(playerCar1.lives):
            screen.blit(heart_img, (SCREEN_WIDTH - 40 - i * 35, 5))
        #Player 2 lives
        for i in range(playerCar2.lives):
            screen.blit(heart_img, (10 + i * 35, 5))

        # Draw and update messages
        messages_group.draw(screen)
        messages_group.update()

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame


def gameMP2roads(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Car Racing Game")

    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    RED = (249, 65, 68)
    BLUE = (0, 180, 216)

    # Font
    timer_font = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    level_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    coins_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30)

    messages_group = pygame.sprite.Group()

    # RIBBON - TIMER AND LIFE COUNTER:
    # Pause button
    pause_img = pygame.image.load("Images/pause.png").convert()
    pause_img = pygame.transform.scale(pause_img, (20, 20))

    # Lives
    heart_img = pygame.image.load("Images/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))

    # ENVIRONMENTS:
    # Forest
    forest_background = pygame.image.load("Images/forest.jpg").convert()
    forest_background = pygame.transform.scale(forest_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Underwater
    underwater_background = pygame.image.load("Images/underwater.jpg").convert()
    underwater_background = pygame.transform.scale(underwater_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Space
    space_background = pygame.image.load("Images/space.jpeg").convert()
    space_background = pygame.transform.scale(space_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    # ROADS:
    num_lanes = 4  # Number of lanes
    road_width = 350  # Width of the road
    lane_width = road_width / num_lanes

    # ROAD Player 1 (Right Side):
    # Center of the right half of the screen
    right_road_center = 3 * SCREEN_WIDTH / 4
    # Positioning the road in the middle of the right half
    road_x_right = right_road_center - (road_width / 2)

    # ROAD Player 2 (Left Side):
    # Center of the left half of the screen
    left_road_center = SCREEN_WIDTH / 4
    # Positioning the road in the middle of the left half
    road_x_left = left_road_center - (road_width / 2)


    # VEHICLES:
    # Player 1 car
    playerCar1 = PlayerCar("Images/00C.png", 50, 3)
    playerCar1.rect.x = right_road_center - (playerCar1.rect.width // 2)  # Center on the left road
    playerCar1.rect.y = SCREEN_HEIGHT - 150

    # Player 2 car
    playerCar2 = PlayerCar("Images/01C.png", 50, 3)
    playerCar2.rect.x = left_road_center - (playerCar2.rect.width // 2)  # Center on the right road
    playerCar2.rect.y = SCREEN_HEIGHT - 150

    # Opponent cars
    car1 = IncomingCars("Images/03C.png", 50, 2, road_x_left + (lane_width - 50) // 2)
    car2 = IncomingCars("Images/02C.png", 50, 4, road_x_left + lane_width + (lane_width - 50) // 2)
    car3 = IncomingCars("Images/05C.png", 50, 3, road_x_left + (2 * lane_width) + (lane_width - 50) // 2)
    car4 = IncomingCars("Images/07C.png", 50, 1, road_x_left + (3 * lane_width) + (lane_width - 50) // 2)

    car5 = IncomingCars("Images/03C.png", 50, 2, road_x_right + (lane_width - 50) // 2)
    car6 = IncomingCars("Images/02C.png", 50, 4, road_x_right + lane_width + (lane_width - 50) // 2)
    car7 = IncomingCars("Images/05C.png", 50, 3, road_x_right + (2 * lane_width) + (lane_width - 50) // 2)
    car8 = IncomingCars("Images/07C.png", 50, 1, road_x_right + (3 * lane_width) + (lane_width - 50) // 2)


    all_sprites_list = pygame.sprite.Group()
    incoming_cars_list = pygame.sprite.Group()
    player_car_list1 = pygame.sprite.Group()
    player_car_list2 = pygame.sprite.Group()

    all_sprites_list.add(playerCar1, playerCar2, car1, car2, car3, car4, car5, car7, car8)
    incoming_cars_list.add(car1, car2, car3, car4, car5, car6, car7, car8)
    player_car_list1.add(playerCar1)
    player_car_list2.add(playerCar2)

    carryOn = True

    # Controls whether the player 1 input should or not be considered
    movement_enabled1 = True
    # Controls whether the player 2 input should or not be considered
    movement_enabled2 = True

    # Game level
    level = 1
    last_minute = 0

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT:  # pygame.quit() checks if we pressed the red X (to leave the app)
                carryOn = False

        if movement_enabled1:
            # Move player 1 car (with input from the user):
            if keys[pygame.K_LEFT]:
                playerCar1.moveLeft(5)
                # Ensure the player's car stays within the left boundary of the right road
                playerCar1.rect.x = max(road_x_right, playerCar1.rect.x)
            if keys[pygame.K_RIGHT]:
                playerCar1.moveRight(5)
                # Ensure the player's car stays within the right boundary of the right road
                playerCar1.rect.x = min(road_x_right + road_width - playerCar1.rect.width, playerCar1.rect.x)
            if keys[pygame.K_UP]:
                playerCar1.moveUp(5)
                # Ensure the player's car stays within the top boundary of the road
                playerCar1.rect.y = max(0, playerCar1.rect.y)
            if keys[pygame.K_DOWN]:
                playerCar1.moveDown(5)
                # Ensure the player's car stays within the bottom boundary of the road
                playerCar1.rect.y = min(SCREEN_HEIGHT - playerCar1.rect.height, playerCar1.rect.y)

        if movement_enabled2:
            # Movement for player 2
            if keys[pygame.K_a]:  # Left
                playerCar2.moveLeft(5)
                # Ensure the player's car stays within the left boundary of the left road
                playerCar2.rect.x = max(road_x_left, playerCar2.rect.x)
            if keys[pygame.K_d]:  # Right
                playerCar2.moveRight(5)
                # Ensure the player's car stays within the right boundary of the left road
                playerCar2.rect.x = min(road_x_left + road_width - playerCar2.rect.width, playerCar2.rect.x)
            if keys[pygame.K_w]:  # Up
                playerCar2.moveUp(5)
                playerCar2.rect.y = max(0, playerCar2.rect.y)
            if keys[pygame.K_s]:  # Down
                playerCar2.moveDown(5)
                playerCar2.rect.y = min(SCREEN_HEIGHT - playerCar2.rect.height, playerCar2.rect.y)

        # Draw background
        screen.blit(forest_background, (0, 0))

        pygame.draw.rect(screen, GREY, [road_x_left, 0, road_width, SCREEN_HEIGHT])  # Left Road
        pygame.draw.rect(screen, GREY, [road_x_right, 0, road_width, SCREEN_HEIGHT])  # Right Road

        # DRAW ROAD MARKINGS FOR THE LEFT ROAD
        middle_line_x_left = road_x_left + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x_left, 0], [middle_line_x_left, SCREEN_HEIGHT], 6)

        dashed_lines_x_left = [road_x_left + (i * lane_width) for i in range(1, num_lanes)]

        offset_y = (pygame.time.get_ticks() // 10) % 40
        for line_x in dashed_lines_x_left:
            for line_y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y + offset_y], [line_x, line_y + 20 + offset_y], 1)

        # DRAW ROAD MARKINGS FOR THE RIGHT ROAD
        middle_line_x_right = road_x_right + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x_right, 0], [middle_line_x_right, SCREEN_HEIGHT], 6)

        dashed_lines_x_right = [road_x_right + (i * lane_width) for i in range(1, num_lanes)]

        offset_y = (pygame.time.get_ticks() // 10) % 40
        for line_x in dashed_lines_x_right:
            for line_y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y + offset_y], [line_x, line_y + 20 + offset_y], 1)

        # Draw the cars
        incoming_cars_list.draw(screen)
        if playerCar1.visible:
            player_car_list1.draw(screen)
        if playerCar2.visible:
            player_car_list2.draw(screen)


        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar1.speed)
            # Reset cars position when they go off-screen
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()

        # Handle collisions with PlayerCar1
        for car in incoming_cars_list:
            if not playerCar1.ghost and pygame.sprite.collide_mask(playerCar1, car) is not None:
                # Collision detected
                playerCar1.lives -= 1
                show_message(messages_group, "-1", message_font, (playerCar1.rect.x, playerCar1.rect.y), BLUE)
                # Activate invincibility for 5 seconds after collision
                playerCar1.ghost = True
                ghost_start_time = pygame.time.get_ticks()
                ghost_duration = 2000
                # Reset player's car position
                playerCar1.rect.x = right_road_center - (playerCar1.rect.width // 2)
                playerCar1.rect.y = SCREEN_HEIGHT - 150
                # If no lives left --> end the game
                if playerCar1.lives == 0:
                    carryOn = False

            # Handle collisions with PlayerCar1
            for car_ in incoming_cars_list:
                if not playerCar2.ghost and pygame.sprite.collide_mask(playerCar2, car_) is not None:
                    # Collision detected for player 2
                    playerCar2.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar2.rect.x, playerCar2.rect.y), RED)
                    # Activate invincibility for 5 seconds after collision for player 2
                    playerCar2.ghost = True
                    ghost_start_time_player2 = pygame.time.get_ticks()
                    ghost_duration_player2 = 2000
                    # Reset player 2's car position
                    playerCar2.rect.x = left_road_center - (playerCar2.rect.width // 2)
                    playerCar2.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left for player 2 --> end the game
                    if playerCar2.lives == 0:
                        carryOn = False

            # Update invincibility status based on elapsed time
            # Player car 1
            if playerCar1.ghost:
                elapsed_time = pygame.time.get_ticks() - ghost_start_time
                toggle_interval = 200
                if elapsed_time >= ghost_duration:
                    playerCar1.ghost = False
                    playerCar1.visible = True
                else:
                    playerCar1.visible = (elapsed_time // toggle_interval) % 2 == 0

            # Player car 2
            if playerCar2.ghost:
                elapsed_time = pygame.time.get_ticks() - ghost_start_time_player2
                toggle_interval = 200
                if elapsed_time >= ghost_duration_player2:
                    playerCar2.ghost = False
                    playerCar2.visible = True
                else:
                    playerCar2.visible = (elapsed_time // toggle_interval) % 2 == 0

        all_sprites_list.update()

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, 30])

        # Draw button
        screen.blit(pause_img, (380, 5))

        # Update timer
        elapsed_time = pygame.time.get_ticks() // 1000
        minutes, seconds = divmod(elapsed_time,
                                  60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
                                        # The quotient --> minutes, and the remainder --> seconds
                                        # The result is unpacked into the minutes and seconds variables
        timer_text = timer_font.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate to center the text
        timer_x = (SCREEN_WIDTH - timer_text.get_width()) // 2
        screen.blit(timer_text, (timer_x, 0))

        # Level upgrade
        if minutes > last_minute:
            # Increase the level every minute
            level += 1
            last_minute = minutes

            # Increase players speed
            playerCar1.speed += 1
            playerCar2.speed += 1

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
        # Player 1 lives
        for i in range(playerCar1.lives):
            screen.blit(heart_img, (SCREEN_WIDTH - 40 - i * 35, 5))
        # Player 2 lives
        for i in range(playerCar2.lives):
            screen.blit(heart_img, (10 + i * 35, 5))

        # Draw and update messages
        messages_group.draw(screen)
        messages_group.update()

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame
