import random
# pygame.org
# pygame works as an old movie that never ends and repeats itself forever (until you die)
import pygame

from car import *
from messages import *


def gameMP(SCREEN_WIDTH, SCREEN_HEIGHT):

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Amount of pixels that compose size of the window
    pygame.display.set_caption("Car Racing Game")


    # GAME SETTINGS:
    # colors
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    RED = (249, 65, 68)
    BLUE = (0, 180, 216)

    # Font
    arialfont_timer = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    messages_group = pygame.sprite.Group()

    # RIBBON - PAUSE, TIMER AND LIFE COUNTER:
    # Pause button
    pause_img = pygame.image.load("Images/pause.png").convert()
    pause_img = pygame.transform.scale(pause_img, (20, 20))
    # Timer
    start_timer = pygame.time.get_ticks()
    # Lives
    heart_img = pygame.image.load("Images/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))
    lives_player1, lives_player2 = 3, 3

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
    playerCar1 = PlayerCar("Images/00C.png", 50)
    playerCar1.rect.x = (SCREEN_WIDTH - playerCar1.rect.width) // 2 - 50  # which column the car starts
    playerCar1.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Player 2 car
    playerCar2 = PlayerCar("Images/01C.png", 50)
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

    all_sprites_list.add(playerCar1, playerCar2, car1, car2, car3, car4)  # To show the cars on the screen
    incoming_cars_list.add(car1, car2, car3, car4)
    player_car1_list.add(playerCar1)
    player_car2_list.add(playerCar2)

    carryOn = True

    # Controls whether the player's input should or not be considered
    movement_enabled = True

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # pygame.quit() checks if we pressed the red X (to leave the app)
                carryOn = False

        if movement_enabled:
            # Move player 1 car (with input from the user):
            if keys[pygame.K_LEFT]:
                playerCar1.moveLeft(5)
                # Ensure the player's car stays within the left boundary of the road
                playerCar1.rect.x = max(road_x, playerCar1.rect.x)
            if keys[pygame.K_RIGHT]:
                playerCar1.moveRight(5)
                # Ensure the player's car stays within the right boundary of the road
                playerCar1.rect.x = min(road_x + road_width - playerCar1.rect.width, playerCar1.rect.x)
            if keys[pygame.K_UP]:
                playerCar1.moveUp(5)
                # Ensure the player's car stays within the top boundary of the road
                playerCar1.rect.y = max(0, playerCar1.rect.y)
            if keys[pygame.K_DOWN]:
                playerCar1.moveDown(5)
                # Ensure the player's car stays within the bottom boundary of the road
                playerCar1.rect.y = min(SCREEN_HEIGHT - playerCar1.rect.height, playerCar1.rect.y)

            # Movement for player 2
            if keys[pygame.K_a]:  # Left
                playerCar2.moveLeft(5)
                playerCar2.rect.x = max(road_x, playerCar2.rect.x)
            if keys[pygame.K_d]:  # Right
                playerCar2.moveRight(5)
                playerCar2.rect.x = min(road_x + road_width - playerCar2.rect.width, playerCar2.rect.x)
            if keys[pygame.K_w]:  # Up
                playerCar2.moveUp(5)
                playerCar2.rect.y = max(0, playerCar2.rect.y)
            if keys[pygame.K_s]:  # Down
                playerCar2.moveDown(5)
                playerCar2.rect.y = min(SCREEN_HEIGHT - playerCar2.rect.height, playerCar2.rect.y)

        # screen.fill(GREEN)
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
                pygame.draw.line(screen, WHITE, [line_x, line_y], [line_x, line_y + 20], 1)

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
            if not playerCar1.invincible and pygame.sprite.collide_mask(playerCar1, car) is not None:
                # Collision detected
                lives_player1 -= 1
                show_message(messages_group, "-1", message_font, (playerCar1.rect.x, playerCar1.rect.y), BLUE)
                # Activate invincibility for 5 seconds after collision
                playerCar1.invincible = True
                invincibility_start_time = pygame.time.get_ticks()
                invincibility_duration = 2000
                # Reset player's car position
                playerCar1.rect.x = (SCREEN_WIDTH - playerCar1.rect.width) // 2 - 50
                playerCar1.rect.y = SCREEN_HEIGHT - 150
                # If no lives left --> end the game
                if lives_player1 == 0:
                    carryOn = False

        # Handle collisions with PlayerCar1
        for car in incoming_cars_list:
            if not playerCar2.invincible and pygame.sprite.collide_mask(playerCar2, car) is not None:
                # Collision detected for player 2
                lives_player2 -= 1
                show_message(messages_group, "-1", message_font, (playerCar2.rect.x, playerCar2.rect.y), RED)
                # Activate invincibility for 5 seconds after collision for player 2
                playerCar2.invincible = True
                invincibility_start_time_player2 = pygame.time.get_ticks()
                invincibility_duration_player2 = 2000
                # Reset player 2's car position
                playerCar2.rect.x = (SCREEN_WIDTH - playerCar2.rect.width) // 2 + 50
                playerCar2.rect.y = SCREEN_HEIGHT - 150
                # If no lives left for player 2 --> end the game
                if lives_player2 == 0:
                    carryOn = False

        # Update invincibility status based on elapsed time
        #Player car 1
        if playerCar1.invincible:
            elapsed_time = pygame.time.get_ticks() - invincibility_start_time
            toggle_interval = 200
            if elapsed_time >= invincibility_duration:
                playerCar1.invincible = False
                playerCar1.visible = True
            else:
                playerCar1.visible = (elapsed_time // toggle_interval) % 2 == 0

        #Player car 2
        if playerCar2.invincible:
            elapsed_time = pygame.time.get_ticks() - invincibility_start_time_player2
            toggle_interval = 200
            if elapsed_time >= invincibility_duration_player2:
                playerCar2.invincible = False
                playerCar2.visible = True
            else:
                playerCar2.visible = (elapsed_time // toggle_interval) % 2 == 0

        all_sprites_list.update()

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, 30])

        # Update timer
        elapsed_time = pygame.time.get_ticks() // 1000
        minutes, seconds = divmod(elapsed_time, 60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
                                                    #The quotient --> minutes, and the remainder --> seconds
                                                    # The result is unpacked into the minutes and seconds variables
        timer_text = arialfont_timer.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate to center the text
        timer_x = (SCREEN_WIDTH - timer_text.get_width()) // 2
        screen.blit(timer_text, (timer_x, 0))

        # Update lives

        #Player 1 lives
        for i in range(lives_player1):
            screen.blit(heart_img, (SCREEN_WIDTH - 40 - i * 35, 5))
        #Player 2 lives
        for i in range(lives_player2):
            screen.blit(heart_img, (10 + i * 35, 5))

        # Draw and update messages
        messages_group.draw(screen)
        messages_group.update()

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame
