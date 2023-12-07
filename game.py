import random
import pygame
from car import *
from coins import Coin
from messages import *
from pause import display_pause_menu
from button import Button
from powerups import *
import config
from users import chosen_car


is_game_paused = False
accessed_from_pause = False


def game(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    # Pause Menu State
    paused = False

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
    ORANGE = (255, 159, 28)
    BLACK = (0, 0, 0)

    # Font
    timer_font = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    level_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    coins_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30)
    game_over_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)

    messages_group = pygame.sprite.Group()

    #CURRENT USER
    username = config.username

    #SELECTED CAR
    picked_car = config.chosen_car

    possible_car = ["Images/00C.png", "Images/04C.png", "Images/02C.png", "Images/05C.png", "Images/07C.png"]

    # GAME OVER
    # Background
    game_over_background = pygame.image.load("Images/stars&planets.png")
    game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # RIBBON - PAUSE, TIMER AND LIFE COUNTER:
    # Pause button
    pause_img = pygame.image.load("Images/pause.png").convert()
    pause_img = pygame.transform.scale(pause_img, (20, 20))
    pause_button = Button("", 19, 10, 20, 20)

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
    playerCar = PlayerCar(possible_car[picked_car], 50, 3)
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

    # POWER UPS:
    initial_x_pow = [
        (road_x + (lane_width - 40) // 2),  # lane 1
        (road_x + lane_width + (lane_width - 40) // 2),  # lane 2
        (road_x + (2 * lane_width) + (lane_width - 40) // 2),  # lane 3
        (road_x + (3 * lane_width) + (lane_width - 40) // 2)  # lane 4
    ]

    selected_initial_x_pow = random.choice(initial_x_pow)

    power_up_invincibility = Invincibility("Images/invincibility.png", 40, selected_initial_x_pow)
    power_up_slowing = SlowDown("Images/slow_down.png", 40, selected_initial_x_pow)
    power_up_jet_bomb = JetBomb("Images/jet_bomb.png", 40, selected_initial_x_pow)
    power_up_extra_life = RestoreLives("Images/heart.png", 40, selected_initial_x_pow)
    power_up_size_change = SizeChange("Images/change_size.png", 40, selected_initial_x_pow)

    incoming_powerups_list = pygame.sprite.Group()

    all_sprites_list.add(playerCar, car1, car2, car3, car4, power_up_invincibility, power_up_slowing, power_up_jet_bomb,
                         power_up_extra_life, power_up_size_change)  # To show the moving objects on the screen
    incoming_cars_list.add(car1, car2, car3, car4)
    player_car_list.add(playerCar)
    incoming_powerups_list.add(power_up_invincibility, power_up_slowing, power_up_jet_bomb, power_up_extra_life,
                               power_up_size_change)

    # Powerup Bar
    max_powerup_bar_width = 170
    powerup_bar_x = 685
    powerup_bar_Y = 50
    powerup_bar_width = 162

    carryOn = True
    game_over = False

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event.pos):
                    paused = not paused  # Resume game




            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
                elif event.key == pygame.K_p:
                    paused = not paused  # Toggle pause state

        if paused:
            resume_button, how_to_play_button, credits_button, quit_button = display_pause_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[
                    pygame.K_ESCAPE]:  # pygame.quit() checks if we pressed the red X (to leave the app)
                    carryOn = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif how_to_play_button.is_clicked(event.pos):
                        from instructions import instructions3_
                        instructions3_(SCREEN_WIDTH, SCREEN_HEIGHT)
                        pause = False
                    elif credits_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif quit_button.is_clicked(event.pos):
                        from interface import interface
                        interface()  # Quit game
            continue  # Skip the rest of the game loop when paused

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

        # Draw pause Button
        pause_button.draw(screen)

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

        # Draw the playerCar
        if playerCar.visible:
            player_car_list.draw(screen)

        # Draw the power-ups
        incoming_powerups_list.draw(screen)

        # Draw + Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()
            if car.visible:
                screen.blit(car.image, car.rect)

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
                if playerCar.pac_man:
                    # car stays invisible
                    car.visible = False
                    # car gets out of the way
                    car.speed = car.speed * 10
                    if car.rect.y >= SCREEN_HEIGHT:
                        car.visible = True

                else:
                    # Collision detected
                    playerCar.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar.rect.x, playerCar.rect.y), RED)
                    # Activate invincibility for 5 seconds after collision
                    playerCar.ghost = True
                    # playerCar.invincible is a check to not enter playerCar.ghost timer when we activate invincibility powerup
                    playerCar.invincible = False
                    ghost_start_time = pygame.time.get_ticks()
                    ghost_duration = 2000
                    # Reset player's car position
                    playerCar.rect.x = (SCREEN_WIDTH - playerCar.rect.width) // 2
                    playerCar.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left --> end the game
                    if playerCar.lives == 0 and not game_over:
                        game_over = True

        if game_over:
            # Display the game-over screen
            screen.blit(game_over_background, (0, 0))
            game_over_text = game_over_font.render("GAME OVER", True, WHITE)
            level_x = (SCREEN_WIDTH - game_over_text.get_width()) // 2
            level_y = (SCREEN_HEIGHT - game_over_text.get_height()) // 2
            screen.blit(game_over_text, (level_x, level_y))

            # Load the existing high scores from the file
            try:
                with open('hscore.txt', 'r') as f:
                    highscores = eval(f.read())
                    users = list(highscores.keys())

            except (FileNotFoundError, SyntaxError):
                highscores = {}

            # Check if the user already exists
            if username in users:
                from database import highscore
                highscore(username, elapsed_time, coin_counter )


            pygame.display.flip()  # Update the display

            # Short delay before interface() display
            pygame.time.delay(2000)

            # The game is over, set the flag and exit the game loop
            from interface import interface
            interface()

        # Update invincibility status based on elapsed time
        if playerCar.ghost and not playerCar.invincible:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar.ghost = False
                playerCar.visible = True
                movement_enabled = True
            else:
                playerCar.visible = (elapsed_time // toggle_interval) % 2 == 0

        all_sprites_list.update()

        # Power up picker --> probability:
        if all(not powerup.active for powerup in incoming_powerups_list):

            spawn_prob = random.randint(0, 100)

            # hearts only spawn when player needs them
            # 30% --> when activated
            if 0 <= spawn_prob < 20 and playerCar.lives < 3:
                power_up_extra_life.active = True
            # 30%
            elif 20 <= spawn_prob <= 80:
                power_up_jet_bomb.active = True
            # 15%
            elif 80 <= spawn_prob < 85:
                # if not power_up_slowing.powered_up: #and (pygame.time.get_ticks() - power_up_slowing.cooldown > cooldown_duration):
                power_up_slowing.active = True
            # 15%
            elif 85 <= spawn_prob < 90:
                power_up_size_change.active = True
            # 10%
            elif 90 <= spawn_prob <= 100:
                power_up_invincibility.active = True

        # Power up cicle
        for powerup in incoming_powerups_list:

            # POWERUP contact with playerCar + respawn
            if powerup.active:
                powerup.moveDown(powerup.speed)

                if pygame.sprite.collide_mask(playerCar, powerup) is not None:

                    powerup.powered_up = True

                    if powerup.powered_up:
                        powerup.active_time = pygame.time.get_ticks()
                        powerup.affect_player(playerCar, screen, messages_group)
                        powerup.affect_traffic(incoming_cars_list)
                        powerup.reshape(road_x, lane_width)

                # Powerup isn't caught
                elif powerup.rect.y >= SCREEN_HEIGHT:
                    powerup.reshape(road_x, lane_width)

        # Power up Timer --> when powerup ends, effect stops
        current_time = pygame.time.get_ticks()
        for powerup in incoming_powerups_list:
            if powerup.powered_up:
                elapsed_time = current_time - powerup.active_time
                # Checks if we are still within powerup effect time
                if elapsed_time < powerup.duration:
                    # Calculate remaining time ratio
                    remaining_ratio = (powerup.duration - elapsed_time) / powerup.duration
                    # Scale bar width based on remaining time (orange bar decreases)
                    powerup_bar_width = max_powerup_bar_width * remaining_ratio
                    # Effect to make car blink while invincibility powerup is active
                    if playerCar.ghost and playerCar.invincible:
                        playerCar.visible = (elapsed_time // 200) % 2 == 0
                # Powerup effect time is over
                else:
                    powerup.effect_over(playerCar, incoming_cars_list, screen)
                    powerup.powered_up = False
                    # self.cooldown = current_time

        # Power up countdown Bar
        for powerup in incoming_powerups_list:
            if powerup.powered_up:
                pygame.draw.rect(screen, WHITE,
                                 [powerup_bar_x - 5, powerup_bar_Y - 5, max_powerup_bar_width + 6, 34])  # border
                pygame.draw.rect(screen, BLACK,
                                 [powerup_bar_x - 4, powerup_bar_Y - 4, max_powerup_bar_width + 4, 32])  # background
                pygame.draw.rect(screen, ORANGE, [powerup_bar_x, powerup_bar_Y, powerup_bar_width, 24])  # timer bar

        # Pac_man
        # for car in incoming_cars_list:
        # if not playerCar.ghost and pygame.sprite.collide_mask(playerCar, car) is not None:

        # Power up contact with incoming cars
        """
        Quando nível sobe muito , carros vão demasiado rápido...levao os powerups atrás pq velocidade de aceleração do
        powerup é mais pequena q a do carro...arrnajar maneira de aumentar velocidade dos powerups para ficar proporcional
        com a dos carros, à medida q o nível sobe. 

        aumentar velocidadde de impacto com o nivel... if level == 3: powerup.speed = ....
        """
        for powerup in incoming_powerups_list:
            for car in incoming_cars_list:
                # Condition to only run this code on the screen player can see
                # ... otherwise powerup appear to fast in the screen ... and to reduce collisions we can´t see
                if (0 <= powerup.rect.x <= SCREEN_WIDTH - powerup.rect.width and
                        -5 <= powerup.rect.y <= SCREEN_HEIGHT - powerup.rect.height and
                        0 <= car.rect.x <= SCREEN_WIDTH - car.rect.width and
                        -5 <= car.rect.y <= SCREEN_HEIGHT - car.rect.height):
                    if pygame.sprite.collide_mask(powerup, car) is not None:
                        # velocidade aumenta à medida que os níveis sobem
                        powerup.speed = 10 + (level - 1) * 3
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
        minutes, seconds = divmod(elapsed_time,
                                  60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
        # The quotient --> minutes, and the remainder --> seconds
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
