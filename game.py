import random
# pygame.org
import pygame
# pygame works as an old movie that never ends and repeats itself forever (until you die)
from car import Car


def game():

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOW:
    # Set up the screen
    screen_width = 700
    screen_height = 500
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
    font = pygame.font.Font(None, 30)


    # RIBBON - TIMER AND LIFE COUNTER:
    # Timer
    start_timer = pygame.time.get_ticks()
    # Lives
    heart_img = pygame.image.load("Images/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))
    lives = 3


    # ENVIRONMENTS:
    # Underwater
    underwater_background = pygame.image.load("Images/underwater.jpg").convert()
    underwater_background = pygame.transform.scale(underwater_background, (screen_width, screen_height))


    # ROAD:
    num_lanes = 4  # Number of lanes
    road_width = 350  # Width of the road
    lane_width = road_width / num_lanes
    road_x = (screen_width - road_width) // 2  # Distance from the road to the left of the screen


    # VEHICLES:
    # Player's car
    playerCar = Car(PALE_VIOLET_PINK, 40, 70)  # Color, width, length
    playerCar.rect.x = (screen_width - playerCar.rect.width) // 2  # which column the car starts
    playerCar.rect.y = 400  # which row the car starts

    # Opponent cars
    car1 = Car(RED, 40, 70, 2)
    car1.rect.x = road_x + (lane_width - car1.rect.width) // 2
    car1.rect.y = -300

    car2 = Car(YELLOW, 40, 70, 4)
    car2.rect.x = road_x + lane_width + (lane_width - car2.rect.width) // 2
    car2.rect.y = -654

    car3 = Car(VIOLET, 40, 70, 3)
    car3.rect.x = road_x + (2 * lane_width) + (lane_width - car3.rect.width) // 2
    car3.rect.y = -795

    car4 = Car(ORANGE, 40, 70, 1)
    car4.rect.x = road_x + (3 * lane_width) + (lane_width - car4.rect.width) // 2
    car4.rect.y = -476

    all_sprites_list = pygame.sprite.Group()
    incoming_cars_list = pygame.sprite.Group()

    all_sprites_list.add(playerCar, car1, car2, car3, car4)  # To show the cars on the screen
    incoming_cars_list.add(car1, car2, car3, car4)

    carryOn = True

    playerCar_speed = 3  # When this value is increased, ALL the incoming cars come faster

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT:  # pygame.quit() checks if we pressed the red X (to leave the app)
                carryOn = False

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

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar_speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= screen_height:
                car.rect.y = random.randint(-1000, 0)
                car.repaint(random.choice(cars_color))
                car.reshape(random.randint(30, 50), random.randint(60, 90))
                car.change_speed(random.randint(3, 5))

        all_sprites_list.update()

        # screen.fill(GREEN)
        # Draw underwater background
        screen.blit(underwater_background, (0, 0))

        pygame.draw.rect(screen, GREY, [road_x, 0, road_width, screen_height])

        # Draw road markings
        middle_line_x = road_x + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x, 0], [middle_line_x, screen_height], 6)  # Central double line

        dashed_lines_x = [road_x + (i * lane_width) for i in range(1, num_lanes)]
        for line_x in dashed_lines_x:
            for line_y in range(0, screen_height, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y], [line_x, line_y + 20], 1)

        #  car_collision_list = pygame.sprite.spritecollide(playerCar, incoming_cars_list, False)  # If True --> Pacman
        # if len(car_collision_list) > 0:
            # carryOn = False
        for car in incoming_cars_list:
            if pygame.sprite.collide_mask(playerCar, car) is not None:
                # Collision detected
                lives -= 1
                # Reset player's car position
                playerCar.rect.x = (screen_width - playerCar.rect.width) // 2
                playerCar.rect.y = 400
                # If no lives left --> end the game
                if lives == 0:
                    carryOn = False

        all_sprites_list.draw(screen)

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, screen_width, 25])
        # Update timer
        elapsed_time = pygame.time.get_ticks() // 1000
        minutes, seconds = divmod(elapsed_time, 60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
                                                    #The quotient --> minutes, and the remainder --> seconds
                                                    # The result is unpacked into the minutes and seconds variables
        timer_text = font.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate to center the text
        timer_x = (screen_width - timer_text.get_width()) // 2
        screen.blit(timer_text, (timer_x, 5))

        # Update lives
        lives_text = font.render("Lives: ", True, WHITE)
        for i in range(lives):
            screen.blit(heart_img, (screen_width - 40 - i * 35, 5))

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per second (or milliseconds don't really know)

    pygame.quit()  # Terminate the pygame
