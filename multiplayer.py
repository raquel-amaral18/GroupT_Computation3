import random
# pygame.org
# pygame works as an old movie that never ends and repeats itself forever (until you die)
import pygame

from car import *
from coins import Coin
from messages import *
from pause import display_pause_menu
from powerups import *
from button import Button


def gameMP(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    paused = False

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
    ORANGE = (255, 159, 28)
    BLACK = (0, 0, 0)

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
    pause_button = Button("", 380, 5, 20, 20)

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
    player_car_list = pygame.sprite.Group()

    # Coins
    coin_list = pygame.sprite.Group()

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

    all_sprites_list.add(playerCar1, playerCar2, car1, car2, car3, car4, power_up_invincibility, power_up_slowing,
                         power_up_jet_bomb,
                         power_up_extra_life, power_up_size_change)  # To show the moving objects on the screen
    incoming_cars_list.add(car1, car2, car3, car4)
    incoming_powerups_list.add(power_up_invincibility, power_up_slowing, power_up_jet_bomb, power_up_extra_life,
                               power_up_size_change)
    player_car_list.add(playerCar1, playerCar2)

    # Powerup Bar
    max_powerup_bar_width = 170
    powerup_bar_x = 685
    powerup_bar_Y = 50
    powerup_bar_width = 162

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
            if event.type == pygame.QUIT or keys[
                pygame.K_ESCAPE]:  # pygame.quit() checks if we pressed the red X (to leave the app)
                carryOn = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
                elif event.key == pygame.K_p:
                    paused = not paused  # Toggle pause state

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event.pos):
                    paused = not paused  # Resume game

        if paused:
            resume_button, how_to_play_button, credits_button, quit_button = display_pause_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif how_to_play_button.is_clicked(event.pos):
                        from instructions import instructions3_
                        instructions3_(SCREEN_WIDTH, SCREEN_HEIGHT)
                    elif credits_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif quit_button.is_clicked(event.pos):
                        carryOn = False  # Quit game
            continue  # Skip the rest of the game loop when paused

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
        for player in player_car_list:
            if player.visible:
                player_car_list.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar1.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()

        # Draw the power-ups
        incoming_powerups_list.draw(screen)

        # Handle collisions with PlayerCar1
        for car in incoming_cars_list:
            if not playerCar1.ghost and pygame.sprite.collide_mask(playerCar1, car) is not None:
                if playerCar1.pac_man:
                    # car stays invisible
                    car.visible = False
                    # car gets out of the way
                    car.speed = car.speed * 10
                    if car.rect.y >= SCREEN_HEIGHT:
                        car.visible = True

                else:
                    # Collision detected
                    playerCar1.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar1.rect.x, playerCar1.rect.y), RED)
                    # Activate invincibility for 5 seconds after collision
                    playerCar1.ghost = True
                    # playerCar.invincible is a check to not enter playerCar.ghost timer when we activate invincibility powerup
                    playerCar1.invincible = False
                    ghost_start_time = pygame.time.get_ticks()
                    ghost_duration = 2000
                    # Reset player's car position
                    playerCar1.rect.x = (SCREEN_WIDTH - playerCar1.rect.width) // 2 - 50
                    playerCar1.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left --> end the game
                    if playerCar1.lives == 0:
                        carryOn = False

        # Handle collisions with PlayerCar2
        for car in incoming_cars_list:
            if not playerCar2.ghost and pygame.sprite.collide_mask(playerCar2, car) is not None:
                if playerCar2.pac_man:
                    # car stays invisible
                    car.visible = False
                    # car gets out of the way
                    car.speed = car.speed * 10
                    if car.rect.y >= SCREEN_HEIGHT:
                        car.visible = True

                else:
                    # Collision detected
                    playerCar2.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar2.rect.x, playerCar2.rect.y), RED)
                    # Activate invincibility for 5 seconds after collision
                    playerCar2.ghost = True
                    # playerCar.invincible is a check to not enter playerCar.ghost timer when we activate invincibility powerup
                    playerCar2.invincible = False
                    ghost_start_time = pygame.time.get_ticks()
                    ghost_duration = 2000
                    # Reset player's car position
                    playerCar2.rect.x = (SCREEN_WIDTH - playerCar2.rect.width) // 2 + 50
                    playerCar2.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left --> end the game
                    if playerCar2.lives == 0:
                        carryOn = False

        # Update invincibility status based on elapsed time
        # Player car 1
        if playerCar1.ghost and not playerCar1.invincible:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar1.ghost = False
                playerCar1.visible = True
                movement_enabled = True
            else:
                playerCar1.visible = (elapsed_time // toggle_interval) % 2 == 0

        # Player car 2
        if playerCar2.ghost and not playerCar2.invincible:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar2.ghost = False
                playerCar2.visible = True
                movement_enabled = True
            else:
                playerCar2.visible = (elapsed_time // toggle_interval) % 2 == 0

        # Power up picker --> probability:
        if all(not powerup.active for powerup in incoming_powerups_list):

            spawn_prob = random.randint(0, 100)

            # hearts only spawn when player needs them
            # 30% --> when activated
            if 0 <= spawn_prob < 20 and playerCar1.lives < 3:
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

                if pygame.sprite.collide_mask(playerCar1, powerup) is not None:

                    powerup.powered_up = True

                    if powerup.powered_up:
                        powerup.active_time = pygame.time.get_ticks()
                        powerup.affect_player(playerCar1, screen, messages_group)
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
                    if playerCar1.ghost and playerCar1.invincible:
                        playerCar1.visible = (elapsed_time // 200) % 2 == 0
                # Powerup effect time is over
                else:
                    powerup.effect_over(playerCar1, incoming_cars_list, screen)
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
        minutes, seconds = divmod(elapsed_time,
                                  60)  # divmod calculates the quotient and remainder when elapsed_time is divided by 60.
        # The quotient --> minutes, and the remainder --> seconds
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


def gameMP2roads(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    paused = False

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
    ORANGE = (255, 159, 28)
    BLACK = (0, 0, 0)

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
    pause_button = Button("", 380, 5, 20, 20)

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
    player_car_list = pygame.sprite.Group()

    # POWER UPS:

    # Left Road
    initial_left_x_pow = [
        (road_x_left + (lane_width - 40) // 2),  # lane 1
        (road_x_left + lane_width + (lane_width - 40) // 2),  # lane 2
        (road_x_left + (2 * lane_width) + (lane_width - 40) // 2),  # lane 3
        (road_x_left + (3 * lane_width) + (lane_width - 40) // 2)  # lane 4
    ]

    selected_initial_left_x_pow = random.choice(initial_left_x_pow)

    power_up_invincibility = Invincibility("Images/invincibility.png", 40, selected_initial_left_x_pow)
    power_up_slowing = SlowDown("Images/slow_down.png", 40, selected_initial_left_x_pow)
    power_up_jet_bomb = JetBomb("Images/jet_bomb.png", 40, selected_initial_left_x_pow)
    power_up_extra_life = RestoreLives("Images/heart.png", 40, selected_initial_left_x_pow)
    power_up_size_change = SizeChange("Images/change_size.png", 40, selected_initial_left_x_pow)

    incoming_powerups_list_left_road = pygame.sprite.Group()

    # Right Road
    initial_right_x_pow = [
        (road_x_right + (lane_width - 50) // 2),  # lane 1
        (road_x_right + lane_width + (lane_width - 50) // 2),  # lane 2
        (road_x_right + (2 * lane_width) + (lane_width - 50) // 2),  # lane 3
        (road_x_right + (3 * lane_width) + (lane_width - 50) // 2)  # lane 4
    ]

    selected_initial_right_x_pow = random.choice(initial_right_x_pow)

    power_up_invincibility_right = Invincibility("Images/invincibility.png", 40, selected_initial_right_x_pow)
    power_up_slowing_right = SlowDown("Images/slow_down.png", 40, selected_initial_right_x_pow)
    power_up_jet_bomb_right = JetBomb("Images/jet_bomb.png", 40, selected_initial_right_x_pow)
    power_up_extra_life_right = RestoreLives("Images/heart.png", 40, selected_initial_right_x_pow)
    power_up_size_change_right = SizeChange("Images/change_size.png", 40, selected_initial_right_x_pow)

    incoming_powerups_list_right_road = pygame.sprite.Group()

    # Add Objects to Lists
    all_sprites_list.add(playerCar1, playerCar2, car1, car2, car3, car4, car5, car6, car7, car8, power_up_invincibility,
                         power_up_slowing, power_up_jet_bomb,
                         power_up_extra_life, power_up_size_change)  # To show the moving objects on the screen
    incoming_cars_list.add(car1, car2, car3, car4, car5, car6, car7, car8)
    incoming_powerups_list_left_road.add(power_up_invincibility, power_up_slowing, power_up_jet_bomb,
                                         power_up_extra_life, power_up_size_change)
    incoming_powerups_list_right_road.add(power_up_invincibility_right, power_up_slowing_right, power_up_jet_bomb_right,
                                          power_up_extra_life_right, power_up_size_change_right)
    player_car_list.add(playerCar1, playerCar2)

    # Powerup Bar
    max_powerup_bar_width = 170
    powerup_bar_x = 685
    powerup_bar_Y = 50
    powerup_bar_width = 162

    carryOn = True

    # Controls whether the player 1 input should or not be considered
    movement_enabled1 = True
    # Controls whether the player 2 input should or not be considered
    movement_enabled2 = True

    # Add a variable to track the active power-up
    active_powerup = None

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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
                elif event.key == pygame.K_p:
                    paused = not paused  # Toggle pause state

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event.pos):
                    paused = not paused  # Resume game

        if paused:
            resume_button, how_to_play_button, credits_button, quit_button = display_pause_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif how_to_play_button.is_clicked(event.pos):
                        from instructions import instructions3_
                        instructions3_(SCREEN_WIDTH, SCREEN_HEIGHT)
                    elif credits_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif quit_button.is_clicked(event.pos):
                        carryOn = False  # Quit game
            continue  # Skip the rest of the game loop when paused

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
        for player in player_car_list:
            if player.visible:
                player_car_list.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar1.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar1.speed)
            # Reset cars position when they go off-screen
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()

        incoming_powerups_list_left_road.draw(screen)
        incoming_powerups_list_right_road.draw(screen)

        # Handle collisions with PlayerCar1
        for car in incoming_cars_list:
            if not playerCar1.ghost and pygame.sprite.collide_mask(playerCar1, car) is not None:
                if playerCar1.pac_man:
                    # car stays invisible
                    car.visible = False
                    # car gets out of the way
                    car.speed = car.speed * 10
                    if car.rect.y >= SCREEN_HEIGHT:
                        car.visible = True

                else:
                    # Collision detected
                    playerCar1.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar1.rect.x, playerCar1.rect.y), RED)
                    # Activate invincibility for 5 seconds after collision
                    playerCar1.ghost = True
                    # playerCar.invincible is a check to not enter playerCar.ghost timer when we activate invincibility powerup
                    playerCar1.invincible = False
                    ghost_start_time = pygame.time.get_ticks()
                    ghost_duration = 2000
                    # Reset player's car position
                    playerCar1.rect.x = right_road_center - (playerCar1.rect.width // 2)
                    playerCar1.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left --> end the game
                    if playerCar1.lives == 0:
                        carryOn = True

        # Handle collisions with PlayerCar2
        for car in incoming_cars_list:
            if not playerCar2.ghost and pygame.sprite.collide_mask(playerCar2, car) is not None:
                if playerCar2.pac_man:
                    # car stays invisible
                    car.visible = False
                    # car gets out of the way
                    car.speed = car.speed * 10
                    if car.rect.y >= SCREEN_HEIGHT:
                        car.visible = True

                else:
                    # Collision detected
                    playerCar2.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar2.rect.x, playerCar2.rect.y), RED)
                    # Activate invincibility for 5 seconds after collision
                    playerCar2.ghost = True
                    # playerCar.invincible is a check to not enter playerCar.ghost timer when we activate invincibility powerup
                    playerCar2.invincible = False
                    ghost_start_time = pygame.time.get_ticks()
                    ghost_duration = 2000
                    # Reset player's car position
                    playerCar2.rect.x = left_road_center - (playerCar2.rect.width // 2)
                    playerCar2.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left --> end the game
                    if playerCar2.lives == 0:
                        carryOn = True

        # Update invincibility status based on elapsed time
        # Player car 1
        if playerCar1.ghost and not playerCar1.invincible:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar1.ghost = False
                playerCar1.visible = True
                movement_enabled = True
            else:
                playerCar1.visible = (elapsed_time // toggle_interval) % 2 == 0

        # Player car 2
        if playerCar2.ghost and not playerCar2.invincible:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar2.ghost = False
                playerCar2.visible = True
                movement_enabled = True
            else:
                playerCar2.visible = (elapsed_time // toggle_interval) % 2 == 0

        # Power up picker --> probability for Left Road:
        if all(not powerup.active for powerup in incoming_powerups_list_left_road):

            spawn_prob = random.randint(0, 100)

            # hearts only spawn when player needs them
            # 30% --> when activated
            if 0 <= spawn_prob < 20 and playerCar2.lives < 3:
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

        # Power up cycle for left road
        for powerup in incoming_powerups_list_left_road:

            # POWERUP contact with playerCar + respawn
            if powerup.active:
                powerup.moveDown(powerup.speed)

                if pygame.sprite.collide_mask(playerCar2, powerup) is not None:

                    powerup.powered_up = True

                    if powerup.powered_up:
                        powerup.active_time = pygame.time.get_ticks()
                        powerup.affect_player(playerCar2, screen, messages_group)
                        powerup.affect_traffic(incoming_cars_list)
                        powerup.reshape(road_x_left, lane_width)

                # Powerup isn't caught
                elif powerup.rect.y >= SCREEN_HEIGHT:
                    powerup.reshape(road_x_left, lane_width)

        # Power up Timer --> when powerup ends, effect stops
        current_time = pygame.time.get_ticks()
        for powerup in incoming_powerups_list_left_road:
            if powerup.powered_up:
                elapsed_time = current_time - powerup.active_time
                # Checks if we are still within powerup effect time
                if elapsed_time < powerup.duration:
                    # Calculate remaining time ratio
                    remaining_ratio = (powerup.duration - elapsed_time) / powerup.duration
                    # Scale bar width based on remaining time (orange bar decreases)
                    powerup_bar_width = max_powerup_bar_width * remaining_ratio
                    # Effect to make car blink while invincibility powerup is active
                    if playerCar2.ghost and playerCar2.invincible:
                        playerCar2.visible = (elapsed_time // 200) % 2 == 0
                # Powerup effect time is over
                else:
                    powerup.effect_over(playerCar2, incoming_cars_list, screen)
                    powerup.powered_up = False
                    # self.cooldown = current_time

        # Power up countdown Bar
        for powerup in incoming_powerups_list_left_road:
            if powerup.powered_up:
                pygame.draw.rect(screen, WHITE,
                                 [powerup_bar_x - 5, powerup_bar_Y - 5, max_powerup_bar_width + 6, 34])  # border
                pygame.draw.rect(screen, BLACK,
                                 [powerup_bar_x - 4, powerup_bar_Y - 4, max_powerup_bar_width + 4, 32])  # background
                pygame.draw.rect(screen, ORANGE, [powerup_bar_x, powerup_bar_Y, powerup_bar_width, 24])  # timer bar

        # Power up contact with incoming cars
        """
        Quando nível sobe muito , carros vão demasiado rápido...levao os powerups atrás pq velocidade de aceleração do
        powerup é mais pequena q a do carro...arrnajar maneira de aumentar velocidade dos powerups para ficar proporcional
        com a dos carros, à medida q o nível sobe. 

        aumentar velocidadde de impacto com o nivel... if level == 3: powerup.speed = ....
        """
        for powerup in incoming_powerups_list_left_road:
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

        # Power up picker --> probability for Right Road:
        if all(not powerup.active for powerup in incoming_powerups_list_right_road):

            spawn_prob = random.randint(0, 100)

            # hearts only spawn when player needs them
            # 30% --> when activated
            if 0 <= spawn_prob < 20 and playerCar1.lives < 3:
                power_up_extra_life_right.active = True
            # 30%
            elif 20 <= spawn_prob <= 80:
                power_up_jet_bomb_right.active = True
            # 15%
            elif 80 <= spawn_prob < 85:
                # if not power_up_slowing.powered_up: #and (pygame.time.get_ticks() - power_up_slowing.cooldown > cooldown_duration):
                power_up_slowing_right.active = True
            # 15%
            elif 85 <= spawn_prob < 90:
                power_up_size_change_right.active = True
            # 10%
            elif 90 <= spawn_prob <= 100:
                power_up_invincibility_right.active = True

        # Power up cycle for Right road
        for powerup in incoming_powerups_list_right_road:

            # POWERUP contact with playerCar + respawn
            if powerup.active:
                powerup.moveDown(powerup.speed)

                if pygame.sprite.collide_mask(playerCar1, powerup) is not None:

                    powerup.powered_up = True

                    if powerup.powered_up:
                        powerup.active_time = pygame.time.get_ticks()
                        powerup.affect_player(playerCar1, screen, messages_group)
                        powerup.affect_traffic(incoming_cars_list)
                        powerup.reshape(road_x_right, lane_width)

                # Powerup isn't caught
                elif powerup.rect.y >= SCREEN_HEIGHT:
                    powerup.reshape(road_x_right, lane_width)

        # Power up Timer --> when powerup ends, effect stops
        current_time = pygame.time.get_ticks()
        for powerup in incoming_powerups_list_right_road:
            if powerup.powered_up:
                elapsed_time = current_time - powerup.active_time
                # Checks if we are still within powerup effect time
                if elapsed_time < powerup.duration:
                    # Calculate remaining time ratio
                    remaining_ratio = (powerup.duration - elapsed_time) / powerup.duration
                    # Scale bar width based on remaining time (orange bar decreases)
                    powerup_bar_width = max_powerup_bar_width * remaining_ratio
                    # Effect to make car blink while invincibility powerup is active
                    if playerCar1.ghost and playerCar1.invincible:
                        playerCar1.visible = (elapsed_time // 200) % 2 == 0
                # Powerup effect time is over
                else:
                    powerup.effect_over(playerCar1, incoming_cars_list, screen)
                    powerup.powered_up = False
                    # self.cooldown = current_time

        # Power up countdown Bar
        for powerup in incoming_powerups_list_right_road:
            if powerup.powered_up:
                pygame.draw.rect(screen, WHITE,
                                 [powerup_bar_x - 5, powerup_bar_Y - 5, max_powerup_bar_width + 6, 34])  # border
                pygame.draw.rect(screen, BLACK,
                                 [powerup_bar_x - 4, powerup_bar_Y - 4, max_powerup_bar_width + 4, 32])  # background
                pygame.draw.rect(screen, ORANGE, [powerup_bar_x, powerup_bar_Y, powerup_bar_width, 24])  # timer bar

        # Power up contact with incoming cars
        """
        Quando nível sobe muito , carros vão demasiado rápido...levao os powerups atrás pq velocidade de aceleração do
        powerup é mais pequena q a do carro...arrnajar maneira de aumentar velocidade dos powerups para ficar proporcional
        com a dos carros, à medida q o nível sobe. 

        aumentar velocidadde de impacto com o nivel... if level == 3: powerup.speed = ....
        """
        for powerup in incoming_powerups_list_right_road:
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
