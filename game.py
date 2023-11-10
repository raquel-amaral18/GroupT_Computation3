import random
# pygame.org
import pygame
# pygame works as an old movie that never ends and repeats itself forever (until you die)
from car import Car


def game():

    pygame.init()  # Initialize the pygame

    # COLORS:
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

    # EXTERNAL WINDOW:
    # Set up the screen
    screen_width = 700
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))  # Amount of pixels that compose size of the window
    pygame.display.set_caption("Car Racing Game")

    # Road:
    num_lanes = 4  # Number of lanes
    road_width = 350  # Width of the road
    lane_width = road_width / num_lanes
    road_x = 25  # Distance from the road to the left of the screen

    playerCar = Car(PALE_VIOLET_PINK, 40, 70)  # Color, width, length
    playerCar.rect.x = 220  # which column the car starts
    playerCar.rect.y = 400  # which row the car starts

    # Opponent cars
    car1 = Car(RED, 40, 70, 2)
    car1.rect.x = 45
    car1.rect.y = -300

    car2 = Car(YELLOW, 40, 70, 4)
    car2.rect.x = 130
    car2.rect.y = -654

    car3 = Car(VIOLET, 40, 70, 3)
    car3.rect.x = 220
    car3.rect.y = -795

    car4 = Car(ORANGE, 40, 70, 1)
    car4.rect.x = 310
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
        if keys[pygame.K_LEFT]:
            playerCar.moveLeft(5)
        if keys[pygame.K_RIGHT]:
            playerCar.moveRight(5)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar_speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= screen_height:
                car.rect.y = random.randint(-1000, 0)
                car.repaint(random.choice(cars_color))
                car.reshape(random.randint(30, 60), random.randint(60, 90))
                car.change_speed(random.randint(3, 6))

        all_sprites_list.update()

        screen.fill(GREEN)

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
            if pygame.sprite.collide_mask(playerCar, car) != None:
                carryOn = False

        all_sprites_list.draw(screen)

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per second (or milliseconds don't really know)

    pygame.quit()  # Terminate the pygame
