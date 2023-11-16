import random
# pygame.org
# pygame works as an old movie that never ends and repeats itself forever (until you die)
import pygame

from car import *

from powerups import *


def game():

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen_width = 700
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))  # Amount of pixels that compose size of the window
    pygame.display.set_caption("Car Racing Game")


    # GAME SETTINGS:
    # colors
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    GREEN = (48, 168, 99)
    PALE_VIOLET_PINK = (240, 98, 146)
    RED = (249, 65, 68)
    VIOLET = (199, 125, 255)
    YELLOW = (255, 209, 102)
    ORANGE = (251, 133, 0)
    BLUE = (0, 180, 216)

    cars_color = [RED, VIOLET, YELLOW, ORANGE, BLUE]

    # Font
    arialfont_timer = pygame.font.SysFont('arial', 25)
    arialfont_score = pygame.font.SysFont('arial', 25)

    # RIBBON - TIMER AND LIFE COUNTER:
    # Timer
    start_timer = pygame.time.get_ticks()
    # Lives
    heart_img = pygame.image.load("Images/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))
    lives = 3
    # Score
    score = 0
    points_per_pass = 10

    # ENVIRONMENTS:
    # Forest
    forest_background = pygame.image.load("Images/forest.jpg")
    forest_background = pygame.transform.scale(forest_background, (screen_width, screen_height))
    # Underwater
    underwater_background = pygame.image.load("Images/underwater.jpg").convert()
    underwater_background = pygame.transform.scale(underwater_background, (screen_width, screen_height))
    # Space
    space_background = pygame.image.load("Images/space.jpeg").convert()
    space_background = pygame.transform.scale(space_background, (screen_width, screen_height))


    # ROAD:
    num_lanes = 4  # Number of lanes
    road_width = 350  # Width of the road
    lane_width = road_width / num_lanes
    road_x = (screen_width - road_width) // 2  # Distance from the road to the left of the screen


    # VEHICLES:
    # Player's car
    playerCar = PlayerCar("Images/00C.png", 50)
    playerCar.rect.x = (screen_width - playerCar.rect.width) // 2  # which column the car starts
    playerCar.rect.y = 450  # which row the car starts

    # Opponent cars
    # Opponent cars
    car1 = IncomingCars("Images/01C.png", 50, 2, road_x + (lane_width - 40) // 2)
    car2 = IncomingCars("Images/02C.png", 50, 4, road_x + lane_width + (lane_width - 40) // 2)
    car3 = IncomingCars("Images/03C.png", 50, 3, road_x + (2 * lane_width) + (lane_width - 40) // 2)
    car4 = IncomingCars("Images/02C.png", 50, 1, road_x + (3 * lane_width) + (lane_width - 40) // 2)

    all_sprites_list = pygame.sprite.Group()
    incoming_cars_list = pygame.sprite.Group()
    player_car_list = pygame.sprite.Group()

    all_sprites_list.add(playerCar, car1, car2, car3, car4)  # To show the cars on the screen
    incoming_cars_list.add(car1, car2, car3, car4)
    player_car_list.add(playerCar)

    carryOn = True

    # Controls whether the player's input should or not be considered
    movement_enabled = True

    # playerCar_speed = 3  # When this value is increased, ALL the incoming cars come faster

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT:  # pygame.quit() checks if we pressed the red X (to leave the app)
                carryOn = False

        if movement_enabled:
            # Move player's car (with input from the user):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                playerCar.moveLeft(5)
                # Ensure the player's car stays within the left boundary of the road
                playerCar.rect.x = max(road_x, playerCar.rect.x)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                playerCar.moveRight(5)
                # Ensure the player's car stays within the right boundary of the road
                playerCar.rect.x = min(road_x + road_width - playerCar.rect.width, playerCar.rect.x)

            # Accelarate and desaccelerate the car
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and playerCar.speed <= 10:
                playerCar.speed += 0.1
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and playerCar.speed > 0:
                playerCar.speed -= 0.1

        # screen.fill(GREEN)
        # Draw background
        screen.blit(forest_background, (0, 0))

        pygame.draw.rect(screen, GREY, [road_x, 0, road_width, screen_height])

        # Draw road markings
        middle_line_x = road_x + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x, 0], [middle_line_x, screen_height], 6)  # Central double line

        dashed_lines_x = [road_x + (i * lane_width) for i in range(1, num_lanes)]
        for line_x in dashed_lines_x:
            for line_y in range(0, screen_height, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y], [line_x, line_y + 20], 1)

        # Draw the cars
        incoming_cars_list.draw(screen)
        if playerCar.visible:
            player_car_list.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= screen_height:
                car.reshape()
                # Increase the score
                score += points_per_pass

        #  car_collision_list = pygame.sprite.spritecollide(playerCar, incoming_cars_list, False)  # If True --> Pacman
        # if len(car_collision_list) > 0:
            # carryOn = False
        for car in incoming_cars_list:
            if not playerCar.invincible and pygame.sprite.collide_mask(playerCar, car) is not None:
                # Collision detected
                lives -= 1
                # Activate invincibility for 5 seconds after collision
                playerCar.invincible = True
                invincibility_start_time = pygame.time.get_ticks()
                invincibility_duration = 2000
                # Reset player's car position
                playerCar.rect.x = (screen_width - playerCar.rect.width) // 2
                playerCar.rect.y = 450
                # If no lives left --> end the game
                if lives == 0:
                    carryOn = False

        # Update invincibility status based on elapsed time
        if playerCar.invincible:
            elapsed_time = pygame.time.get_ticks() - invincibility_start_time
            toggle_interval = 200
            if elapsed_time >= invincibility_duration:
                playerCar.invincible = False
                playerCar.visible = True
                movement_enabled = True
            else:
                playerCar.visible = (elapsed_time // toggle_interval) % 2 == 0

        all_sprites_list.update()

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, screen_width, 30])
        # Update score
        score_text = arialfont_score.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 0))
        # Update timer
        elapsed_time = pygame.time.get_ticks() // 1000
        minutes, seconds = divmod(elapsed_time, 60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
                                                    #The quotient --> minutes, and the remainder --> seconds
                                                    # The result is unpacked into the minutes and seconds variables
        timer_text = arialfont_timer.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate to center the text
        timer_x = (screen_width - timer_text.get_width()) // 2
        screen.blit(timer_text, (timer_x, 0))

        # Update lives
        for i in range(lives):
            screen.blit(heart_img, (screen_width - 40 - i * 35, 5))


        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame
