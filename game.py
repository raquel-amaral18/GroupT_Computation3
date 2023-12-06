import random

import pygame

from car import PlayerCar, IncomingCars
from powerups import Invincibility, SlowDown, RestoreLives, Rocket, SizeChange
from pause import display_pause_menu

from button import Button

from coins import Coin
from messages import show_message


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
    ORANGE = (255, 159, 28)

    # Font
    timer_font = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    level_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    coins_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30)
    game_over_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)

    messages_group = pygame.sprite.Group()


    # MUSIC AND SOUNDS
    # Load background music
    pygame.mixer.music.load("Music&Sounds/background_music.mp3")
    pygame.mixer.music.set_volume(0.2)  # Set the volume
    pygame.mixer.music.play(-1)  # Play the background music on loop

    # Load sounds
    catch_coin = pygame.mixer.Sound("Music&Sounds/catch_coin.wav")
    car_collision = pygame.mixer.Sound("Music&Sounds/car_collision.flac")
    level_up = pygame.mixer.Sound("Music&Sounds/level_up.wav")
    catch_powerup = pygame.mixer.Sound("Music&Sounds/catch_powerup.wav")

    # GAME OVER
    # Background
    game_over_background = pygame.image.load("Images/Design/stars&planets.png")
    game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    # RIBBON - PAUSE AND LIFE COUNTER:
    # Pause button
    pause_img = pygame.image.load("Images/Extras/pause.png").convert()
    pause_img = pygame.transform.scale(pause_img, (20, 20))
    pause_button = Button("", 15, 5, 20, 20, font_size=0, text_color=0, button_color=(0, 0, 0, 255))  # Transparent

    # Lives
    heart_img = pygame.image.load("Images/Extras/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))


    # FOOTER - COIN COUNTER:
    # Coins
    coin_image = pygame.image.load("Images/Extras/coin.png")
    coin_image = pygame.transform.scale(coin_image, (30, 30))
    coin_counter_rect = coin_image.get_rect()
    coin_counter_rect.topleft = (760, 657)

    # Nr of coins
    coin_counter = 0

    coin_list = pygame.sprite.Group()  # Coins will only be added in the game loop


    # ENVIRONMENTS (aka background):
    backgrounds = [
        pygame.image.load("Images/Design/background6.png"),
        pygame.image.load("Images/Design/background2.png"),
        pygame.image.load("Images/Design/background3.png"),
        pygame.image.load("Images/Design/background4.png"),
        pygame.image.load("Images/Design/background5.png"),
        pygame.image.load("Images/Design/background6.png")
    ]
    num_backgrounds = len(backgrounds)
    resized_backgrounds = [pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT)) for bg in backgrounds]


    # ROAD:
    num_lanes = 4  # Number of lanes
    road_width = 450  # Width of the road
    lane_width = road_width / num_lanes
    road_x = (SCREEN_WIDTH - road_width) // 2  # Distance from the road to the left of the screen


    # VEHICLES:
    # Player's car
    playerCar = PlayerCar("Images/Vehicles/00C.png", 60, 3)
    playerCar.rect.x = (SCREEN_WIDTH - playerCar.rect.width) // 2  # which column the car starts
    playerCar.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Opponent cars
    car1 = IncomingCars("Images/Vehicles/04C.png", 60, 2, road_x + (lane_width - 50) // 2)
    car2 = IncomingCars("Images/Vehicles/02C.png", 60, 4, road_x + lane_width + (lane_width - 50) // 2)
    car3 = IncomingCars("Images/Vehicles/05C.png", 60, 3, road_x + (2 * lane_width) + (lane_width - 50) // 2)
    car4 = IncomingCars("Images/Vehicles/07C.png", 60, 1, road_x + (3 * lane_width) + (lane_width - 50) // 2)

    all_sprites_list = pygame.sprite.Group()  # All moving objects group
    incoming_cars_list = pygame.sprite.Group()
    player_car_list = pygame.sprite.Group()


    # POWER UPS:
    initial_x_pow = [
        (road_x + (lane_width - 40) // 2),  # lane 1
        (road_x + lane_width + (lane_width - 40) // 2),  # lane 2
        (road_x + (2 * lane_width) + (lane_width - 40) // 2),  # lane 3
        (road_x + (3 * lane_width) + (lane_width - 40) // 2)  # lane 4
    ]

    selected_initial_x_pow = random.choice(initial_x_pow)

    power_up_invincibility = Invincibility("Images/PowerUps/invincibility.png", 50, selected_initial_x_pow)
    power_up_slowing = SlowDown("Images/PowerUps/slow_down.png", 50, selected_initial_x_pow)
    power_up_rocket = Rocket("Images/PowerUps/rocket.png", 50, selected_initial_x_pow)
    power_up_extra_life = RestoreLives("Images/PowerUps/heart.png", 50, selected_initial_x_pow)
    power_up_size_change = SizeChange("Images/PowerUps/change_size.png", 50, selected_initial_x_pow)

    incoming_powerups_list = pygame.sprite.Group()

    # To show the moving objects on the screen
    all_sprites_list.add(playerCar,
                         car1, car2, car3, car4,
                         power_up_invincibility, power_up_slowing, power_up_rocket, power_up_extra_life,
                         power_up_size_change)
    incoming_cars_list.add(car1, car2, car3, car4)
    player_car_list.add(playerCar)
    incoming_powerups_list.add(power_up_invincibility, power_up_slowing, power_up_rocket, power_up_extra_life,
                               power_up_size_change)


    # GAME EXTRAS:
    # Powerup Bar
    max_powerup_bar_width = 170
    powerup_bar_x = 685
    powerup_bar_Y = 50
    powerup_bar_width = 162

    # Controls whether the player's input should or not be considered
    movement_enabled = True

    # Game level
    level = 1
    last_minute = 0


    # Pause Menu State
    paused = False

    # Game State
    carryOn = True
    game_over = False

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # pygame.QUIT checks if we pressed the red X
                carryOn = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event.pos):
                    paused = not paused  # Resume game

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
                elif event.key == pygame.K_p:
                    paused = not paused  # Toggle pause state

        # PAUSE MENU:
        if paused:
            resume_button, how_to_play_button, quit_button = display_pause_menu(SCREEN_WIDTH, SCREEN_HEIGHT)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif how_to_play_button.is_clicked(event.pos):
                        from instructions import instructions3_
                        instructions3_(SCREEN_WIDTH, SCREEN_HEIGHT)
                        pause = False
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
        screen.blit(resized_backgrounds[(level - 1) % num_backgrounds], (0, 0))

        pygame.draw.rect(screen, GREY, [road_x, 0, road_width, SCREEN_HEIGHT])  # Road

        # Draw road markings
        middle_line_x = road_x + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x, 0], [middle_line_x, SCREEN_HEIGHT], 6)  # Central double line

        dashed_lines_x = [road_x + (i * lane_width) for i in range(1, num_lanes)]

        # Calculate the offset based on the player's car speed
        offset_y = (pygame.time.get_ticks() // 10) % 40  # A smaller divisor results in a faster movement
        for line_x in dashed_lines_x:
            for line_y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y + offset_y], [line_x, line_y + 20 + offset_y], 1)

        incoming_cars_list.draw(screen)
        if playerCar.visible:
            player_car_list.draw(screen)

        # Draw the power-ups
        incoming_powerups_list.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list:
            # Velocity
            car.moveDown(playerCar.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()

        for car in incoming_cars_list:
            if not playerCar.ghost and pygame.sprite.collide_mask(playerCar, car) is not None:
                if playerCar.pac_man:
                    car.reshape()
                if not playerCar.invincible and not playerCar.pac_man:
                    # Collision detected
                    car_collision.play()
                    playerCar.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar.rect.x, playerCar.rect.y), RED)
                    # Activate invincibility for 2 seconds after collision
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

            pygame.display.flip()  # Update the display

            # Short delay before interface() display
            pygame.time.delay(2000)

            # The game is over, set the flag and exit the game loop
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

        """ 
            2º - Permitir usar só 2 power ups ao mm tempo --> criar variável que conta os powerups apanhados --> 
                 Quando essa variável chega a 2 ... n permitir ativar mais powerups ... smp que um power up acaba, 
                 subtrair 1 dessa variável, para dar espaço ao próximo ... quando player tentar apanhar terceiro powerup
                 ao mm tempo, display mensagem "FULL"

            3ª -  Não deixar apanhar invincibility quando tamos usar um powerup ... n deixar apanhar jet_bomb quando 
                  tamos a usar invincibility (vice-versa)

            4º - if playerCar collides with car ... any powerup activated ends

            6º - Tratar Jet_bom --> pacman type shit...collide with car = boom (tempo)

            8º - Perceber coins, e ver como implementar Magnet (tempo)

            9º - Ver se resolvo powerup collision com cars não funcionar 100% das vezes


            Extras: 

            - In line powerups...have 1, 2 pr 3 slotes...when player picks ups power_up while using anotehr powerup...
            icon stored in box, whe need to click button to activate item (Mario Kart)
        """
        # Power up picker --> probability:
        if all(not powerup.active for powerup in incoming_powerups_list):

            spawn_prob = random.uniform(0, 100)

            # 1% --> when activated
            if 0 <= spawn_prob < 1 and playerCar.lives < 2:  # hearts only spawn when player needs them
                power_up_extra_life.active = True
            # 5%
            elif 2 <= spawn_prob <= 6:
                power_up_rocket.active = True
            # 3%
            elif 7 <= spawn_prob < 10:
                power_up_slowing.active = True
            # 6%
            elif 10 <= spawn_prob < 16:
                power_up_size_change.active = True
            # 0.5%
            elif 16.5 <= spawn_prob <= 17:
                power_up_invincibility.active = True

        # Power up cicle
        for powerup in incoming_powerups_list:
            # POWERUP contact with playerCar + respawn
            if powerup.active:
                powerup.moveDown(powerup.speed)

                if pygame.sprite.collide_mask(playerCar, powerup) is not None:
                    catch_powerup.play()
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
                    if playerCar.invincible:
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


        # Draw the coins
        for i, line_x in enumerate(dashed_lines_x):
            if i == 0 or i == 2:  # Select the 1st and 3rd lines
                if random.random() < 0.002:  # Fixed probability for coin generation
                    coin = Coin("Images/Extras/coin.png", 40, line_x - 20, -50)
                    coin_list.add(coin)

        coin_list.update()
        coin_list.draw(screen)

        for coin in coin_list:
            coin.moveDown()

        # Check collisions with the player
        coin_collision_list = pygame.sprite.spritecollide(playerCar, coin_list, True)  # works like packman

        if coin_collision_list:
            catch_coin.play()

        # Update coin counter
        coin_counter += len(coin_collision_list)

        # Display coin counter
        pygame.draw.rect(screen, BLACK, [740, 640, 110, 80], border_radius=24)

        screen.blit(coin_image, coin_counter_rect)

        coin_counter_text = coins_font.render(f": {coin_counter}", True, WHITE)
        screen.blit(coin_counter_text, (800, 650))

        # RIBBON:
        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, 30])

        # Draw pause Button
        pause_button.draw(screen)
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

            # Play level-up sound
            level_up.play()

            pygame.display.flip()  # Update the full display Surface to the screen

            # Pause for 1 seconds
            pygame.time.wait(1000)
            # Clear the screen
            screen.blit(resized_backgrounds[(level - 1) % num_backgrounds], (0, 0))
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


    if not carryOn:
        # Transition to the interface
        from interface import interface
        interface()
