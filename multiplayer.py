import random
import pygame

import config

from car import PlayerCar, IncomingCars
from powerups import Invincibility, SlowDown, RestoreLives, JetBomb, SizeChange, NoPowerUp, KeyInversion, Invisible

from pause import display_pause_menu
from button import Button

from particles import *
from coins import Coin
from messages import show_message


def gameMP(SCREEN_WIDTH, SCREEN_HEIGHT):

    pygame.init()  # Initialize the pygame

    # EXTERNAL WINDOWdd:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    RED = (249, 65, 68)
    BLUE = (0, 180, 216)
    ORANGE = (255, 159, 28)
    
    # Font
    score_font = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    level_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    coins_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 30)
    game_over_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    winner_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 70)

    messages_group = pygame.sprite.Group()


    # MUSIC AND SOUNDS
    # Load background music
    if config.is_music_enabled:
        pygame.mixer.music.load("Music&Sounds/background_music.mp3")
        pygame.mixer.music.set_volume(0.2)  # Set the volume
        pygame.mixer.music.play(-1)  # Play the background music on loop

    # Load sounds
    if config.is_sound_enabled:
        catch_coin = pygame.mixer.Sound("Music&Sounds/catch_coin.wav")
        car_collision = pygame.mixer.Sound("Music&Sounds/car_collision.flac")
        level_up = pygame.mixer.Sound("Music&Sounds/level_up.wav")
        catch_powerup = pygame.mixer.Sound("Music&Sounds/catch_powerup.wav")
        jet_bomb = pygame.mixer.Sound("Music&Sounds/jet_bomb.mp3")

    # GAME OVER
    # Background
    game_over_background = pygame.image.load("Images/Design/stars&planets.png")
    game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    # RIBBON - PAUSE, SCORE AND LIFE COUNTER:
    # Pause button
    pause_img = pygame.image.load("Images/Extras/pause.png").convert()
    pause_img = pygame.transform.scale(pause_img, (20, 20))
    pause_button = Button("", 380, 5, 20, 20, font_size=0, text_color=0, button_color=(0, 0, 0, 255), border_radius=0)

    # Lives
    heart_img = pygame.image.load("Images/Extras/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))

    # Score
    score = 0
    updated_score = 0


    # FOOTER - COIN COUNTER:
    # Coins
    coin_image = pygame.image.load("Images/Extras/coin.png")
    coin_image = pygame.transform.scale(coin_image, (30, 30))
    coin_counter_rect1 = coin_image.get_rect()
    coin_counter_rect2 = coin_image.get_rect()
    coin_counter_rect1.topleft = (760, 657)
    coin_counter_rect2.topleft = (70, 657)

    # Nr of coins
    coin_counter1 = 0
    coin_counter2 = 0


    # ENVIRONMENTS (aka background):
    backgrounds = [
        pygame.image.load("Images/Design/background1.png"),
        pygame.image.load("Images/Design/background2.png"),
        pygame.image.load("Images/Design/background3.png"),
        pygame.image.load("Images/Design/background4.png"),
        pygame.image.load("Images/Design/background5.png"),
        pygame.image.load("Images/Design/background6.png"),
        pygame.image.load("Images/Design/background7.png"),
        pygame.image.load("Images/Design/background8.png")
    ]
    num_backgrounds = len(backgrounds)
    resized_backgrounds = [pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT)) for bg in backgrounds]


    # ROAD:
    num_lanes = 4  # Number of lanes
    road_width = 450  # Width of the road
    lane_width = road_width / num_lanes
    road_x = (SCREEN_WIDTH - road_width) // 2  # Distance from the road to the left of the screen


    # VEHICLES:
    # Player 1 car
    playerCar1 = PlayerCar("Images/Vehicles/PlayerCar/00C.png", 60, 2)
    playerCar1.rect.x = (SCREEN_WIDTH - playerCar1.rect.width) // 2 + 50  # which column the car starts
    playerCar1.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Player 2 car
    playerCar2 = PlayerCar("Images/Vehicles/PlayerCar/01C.png", 60, 2)
    playerCar2.rect.x = (SCREEN_WIDTH - playerCar2.rect.width) // 2 - 50  # which column the car starts
    playerCar2.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Opponent cars
    car1 = IncomingCars("Images/Vehicles/IncomingCars/03C.png", 60, 2, road_x + (lane_width - 50) // 2)
    car2 = IncomingCars("Images/Vehicles/IncomingCars/02C.png", 60, 4, road_x + lane_width + (lane_width - 50) // 2)
    car3 = IncomingCars("Images/Vehicles/IncomingCars/07C.png", 60, 3,
                        road_x + (2 * lane_width) + (lane_width - 50) // 2)
    car4 = IncomingCars("Images/Vehicles/IncomingCars/08C.png", 60, 1,
                        road_x + (3 * lane_width) + (lane_width - 50) // 2)

    all_sprites_list = pygame.sprite.Group()
    incoming_cars_list = pygame.sprite.Group()
    player_car1_list = pygame.sprite.Group()
    player_car2_list = pygame.sprite.Group()


    # Coins
    coin_list = pygame.sprite.Group()


    all_sprites_list.add(playerCar1, playerCar2, car1, car2, car3, car4)
    incoming_cars_list.add(car1, car2, car3, car4)
    player_car1_list.add(playerCar1)
    player_car2_list.add(playerCar2)

    # Controls whether the player 1 input should or not be considered
    movement_enabled1 = True
    # Controls whether the player 2 input should or not be considered
    movement_enabled2 = True

    # Game level
    level = 1
    first_lvl_up = 60

    # Pause Menu State
    paused = False

    # Winner
    winner = None

    # Game State
    carryOn = True
    game_over = False

    clock = pygame.time.Clock()  # How fast the screen resets (how many times you repeat the loop per second)

    # Game loop:
    while carryOn:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():  # It will return everything that the user inputs in a list (e.g.: mouse click)
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:  # pygame.quit() checks if we pressed the red X (to leave the app)
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
            resume_button, how_to_play_button, quit_button = display_pause_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif how_to_play_button.is_clicked(event.pos):
                        screen.blit(pygame.image.load("Images/Design/instructions_pause.png"), (0, 0))
                        pygame.display.flip()  # Update the screen to show changes

                        waiting_for_click = True
                        while waiting_for_click:
                            for event in pygame.event.get():  # Event handling loop
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    waiting_for_click = False
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
        screen.blit(resized_backgrounds[level - 1], (0, 0))

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
                if config.is_sound_enabled:
                    car_collision.play()
                playerCar1.lives -= 1
                show_message(messages_group, "-1", message_font, (playerCar1.rect.x, playerCar1.rect.y), BLUE)
                # Activate invincibility for 5 seconds after collision
                playerCar1.ghost = True
                ghost_start_time = pygame.time.get_ticks()
                ghost_duration = 2000
                # If no lives left --> end the game
                if playerCar1.lives == 0:
                    game_over = True

        # Handle collisions with PlayerCar2
        for car in incoming_cars_list:
            if not playerCar2.ghost and pygame.sprite.collide_mask(playerCar2, car) is not None:
                # Collision detected for player 2
                if config.is_sound_enabled:
                    car_collision.play()
                playerCar2.lives -= 1
                show_message(messages_group, "-1", message_font, (playerCar2.rect.x, playerCar2.rect.y), RED)
                # Activate invincibility for 5 seconds after collision for player 2
                playerCar2.ghost = True
                ghost_start_time_player2 = pygame.time.get_ticks()
                ghost_duration_player2 = 2000
                # If no lives left for player 2 --> end the game
                if playerCar2.lives == 0:
                    game_over = True

        if game_over:
            if playerCar1.lives > 0:
                winner = "Player 1 wins!"
            elif playerCar2.lives > 0:
                winner = "Player 2 wins!"

            # Display the game-over screen
            screen.blit(game_over_background, (0, 0))

            # Game over text
            game_over_text = game_over_font.render("GAME OVER", True, WHITE)
            game_over_x = (SCREEN_WIDTH - game_over_text.get_width()) // 2
            game_over_y = (SCREEN_HEIGHT - game_over_text.get_height()) // 2
            screen.blit(game_over_text, (game_over_x, game_over_y))

            # Winner text
            winner_text = winner_font.render(f"{winner}", True, WHITE)
            winner_x = (SCREEN_WIDTH - winner_text.get_width()) // 2
            winner_y = game_over_y + game_over_text.get_height() + 20
            screen.blit(winner_text, (winner_x, winner_y))

            pygame.display.flip()  # Update the display

            # Short delay before interface() display
            pygame.time.delay(2000)

            # The game is over, set the flag and exit the game loop
            carryOn = False

        # Update ghost status based on elapsed time
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
                coin = Coin("Images/Extras/coin.png", 40, line_x - 20, -50)
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

        # Check for extra lives
        if coin_counter1 >= 10:
            playerCar1.lives += coin_counter1 // 10
            coin_counter1 %= 10  # Reset the counter after gaining extra lives

        if coin_counter2 >= 10:
            playerCar2.lives += coin_counter2 // 10
            coin_counter2 %= 10  # Reset the counter after gaining extra lives

        if (coin_collision_list1 or coin_collision_list2) and config.is_sound_enabled:
            catch_coin.play()

        # Display coin counters
        pygame.draw.rect(screen, BLACK, [50, 640, 110, 80], border_radius=24)
        pygame.draw.rect(screen, BLACK, [740, 640, 110, 80], border_radius=24)

        screen.blit(coin_image, coin_counter_rect1)
        screen.blit(coin_image, coin_counter_rect2)

        coin_counter_text = coins_font.render(f": {coin_counter1}", True, WHITE)
        screen.blit(coin_counter_text, (800, 650))
        coin_counter_text = coins_font.render(f": {coin_counter2}", True, WHITE)
        screen.blit(coin_counter_text, (110, 650))

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, 30])

        # Draw button
        screen.blit(pause_img, (380, 5))

        # Update timer
        minutes, seconds = divmod(updated_score, 60)
        score_text = score_font.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate to center the text
        score_x = (SCREEN_WIDTH - score_text.get_width()) // 2
        screen.blit(score_text, (score_x, 5))

        # Level upgrade
        if updated_score == first_lvl_up:
            # Increase the level every minute
            level += 1
            first_lvl_up = first_lvl_up + 60

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

            # Play level-up sound
            if config.is_sound_enabled:
                level_up.play()

            pygame.display.flip()  # Update the full display Surface to the screen

            # Pause for 1 seconds
            pygame.time.wait(1000)
            # Clear the screen
            screen.blit(resized_backgrounds[(level - 1) % num_backgrounds], (0, 0))
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

        # Update score
        score += 1
        updated_score = score // 60

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame

    if not carryOn:
        from interface import interface
        interface()


def gameMP2roads(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()  # Initialize the pygame

    paused = False

    # EXTERNAL WINDOW:
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # GAME SETTINGS:
    # colors
    BLACK = (0, 0, 0)
    GREY = (80, 80, 80)
    WHITE = (255, 255, 255)
    RED = (249, 65, 68)
    BLUE = (0, 180, 216)
    BLACK = (0, 0, 0)

    # Font
    score_font = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    level_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    game_over_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 150)
    winner_font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", 70)

    messages_group = pygame.sprite.Group()


    # MUSIC AND SOUNDS
    # Load background music
    if config.is_music_enabled:
        pygame.mixer.music.load("Music&Sounds/background_music.mp3")
        pygame.mixer.music.set_volume(0.2)  # Set the volume
        pygame.mixer.music.play(-1)  # Play the background music on loop

    # Load sounds
    if config.is_sound_enabled:
        catch_coin = pygame.mixer.Sound("Music&Sounds/catch_coin.wav")
        car_collision = pygame.mixer.Sound("Music&Sounds/car_collision.flac")
        level_up = pygame.mixer.Sound("Music&Sounds/level_up.wav")
        catch_powerup = pygame.mixer.Sound("Music&Sounds/catch_powerup.wav")
        jet_bomb = pygame.mixer.Sound("Music&Sounds/jet_bomb.mp3")


    # GAME OVER
    # Background
    game_over_background = pygame.image.load("Images/Design/stars&planets.png")
    game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    # RIBBON - TIMER AND LIFE COUNTER:
    # Pause button
    pause_img = pygame.image.load("Images/Extras/pause.png").convert()
    pause_img = pygame.transform.scale(pause_img, (20, 20))
    pause_button = Button("", 15, 5, 20, 20, font_size=0, text_color=0, button_color=(0, 0, 0, 255), border_radius=0)

    # Lives
    heart_img = pygame.image.load("Images/Extras/heart.png").convert()
    heart_img = pygame.transform.scale(heart_img, (20, 20))

    # ENVIRONMENTS:
    background = pygame.image.load("Images/Design/2_roads_background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


    # ROADS:
    num_lanes = 4  # Number of lanes
    road_width = 400  # Width of the road
    lane_width = road_width / num_lanes
    road_speed1 = 10
    road_speed2 = 10

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
    playerCar1 = PlayerCar("Images/Vehicles/PlayerCar/00C.png", 60, 3)
    playerCar1.rect.x = right_road_center - (playerCar1.rect.width // 2)  # Center on the left road
    playerCar1.rect.y = SCREEN_HEIGHT - 150

    # Player 2 car
    playerCar2 = PlayerCar("Images/Vehicles/PlayerCar/01C.png", 60, 3)
    playerCar2.rect.x = left_road_center - (playerCar2.rect.width // 2)  # Center on the right road
    playerCar2.rect.y = SCREEN_HEIGHT - 150

    # Opponent cars
    car1 = IncomingCars("Images/Vehicles/IncomingCars/03C.png", 60, 2, road_x_left + (lane_width - 50) // 2)
    car2 = IncomingCars("Images/Vehicles/IncomingCars/02C.png", 60, 4, road_x_left + lane_width + (lane_width - 50) // 2)
    car3 = IncomingCars("Images/Vehicles/IncomingCars/05C.png", 60, 3, road_x_left + (2 * lane_width) + (lane_width - 50) // 2)
    car4 = IncomingCars("Images/Vehicles/IncomingCars/07C.png", 60, 1, road_x_left + (3 * lane_width) + (lane_width - 50) // 2)

    car5 = IncomingCars("Images/Vehicles/IncomingCars/03C.png", 60, 2, road_x_right + (lane_width - 50) // 2)
    car6 = IncomingCars("Images/Vehicles/IncomingCars/02C.png", 60, 4, road_x_right + lane_width + (lane_width - 50) // 2)
    car7 = IncomingCars("Images/Vehicles/IncomingCars/05C.png", 60, 3, road_x_right + (2 * lane_width) + (lane_width - 50) // 2)
    car8 = IncomingCars("Images/Vehicles/IncomingCars/07C.png", 60, 1, road_x_right + (3 * lane_width) + (lane_width - 50) // 2)

    all_sprites_list = pygame.sprite.Group()
    incoming_cars_list_right = pygame.sprite.Group()
    incoming_cars_list_left = pygame.sprite.Group()
    player_car_list1 = pygame.sprite.Group()
    player_car_list2 = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()

    # POWER UPS:
    # Left Road
    initial_left_x_pow = [
        (road_x_left + (lane_width - 40) // 2),  # lane 1
        (road_x_left + lane_width + (lane_width - 40) // 2),  # lane 2
        (road_x_left + (2 * lane_width) + (lane_width - 40) // 2),  # lane 3
        (road_x_left + (3 * lane_width) + (lane_width - 40) // 2)  # lane 4
    ]

    selected_initial_left_x_pow = random.choice(initial_left_x_pow)

    power_up_invincibility = Invincibility("Images/PowerUps/invincibility.png", 50, selected_initial_left_x_pow)
    power_up_slowing = SlowDown("Images/PowerUps/slow_down.png", 50, selected_initial_left_x_pow)
    power_up_jet_bomb = JetBomb("Images/PowerUps/jet_bomb.png", 50, selected_initial_left_x_pow)
    power_up_extra_life = RestoreLives("Images/PowerUps/heart.png", 50, selected_initial_left_x_pow)
    power_up_size_change = SizeChange("Images/PowerUps/change_size.png", 50, selected_initial_left_x_pow)
    power_up_no_power_up = NoPowerUp("Images/PowerUps/no_powerup.png", 50, selected_initial_left_x_pow)
    power_up_key_inversion = KeyInversion("Images/PowerUps/key_inversion.png", 50, selected_initial_left_x_pow)
    power_up_invisible = Invisible("Images/PowerUps/invisible.png", 50, selected_initial_left_x_pow)

    incoming_powerups_list_left_road = pygame.sprite.Group()

    # Right Road
    initial_right_x_pow = [
        (road_x_right + (lane_width - 50) // 2),  # lane 1
        (road_x_right + lane_width + (lane_width - 50) // 2),  # lane 2
        (road_x_right + (2 * lane_width) + (lane_width - 50) // 2),  # lane 3
        (road_x_right + (3 * lane_width) + (lane_width - 50) // 2)  # lane 4
    ]

    selected_initial_right_x_pow = random.choice(initial_right_x_pow)

    power_up_invincibility_right = Invincibility("Images/PowerUps/invincibility.png", 50, selected_initial_right_x_pow)
    power_up_slowing_right = SlowDown("Images/PowerUps/slow_down.png", 50, selected_initial_right_x_pow)
    power_up_jet_bomb_right = JetBomb("Images/PowerUps/jet_bomb.png", 50, selected_initial_right_x_pow)
    power_up_extra_life_right = RestoreLives("Images/PowerUps/heart.png", 50, selected_initial_right_x_pow)
    power_up_size_change_right = SizeChange("Images/PowerUps/change_size.png", 50, selected_initial_right_x_pow)
    power_up_no_power_up_right = NoPowerUp("Images/PowerUps/no_powerup.png", 50, selected_initial_right_x_pow)
    power_up_key_inversion_right = KeyInversion("Images/PowerUps/key_inversion.png", 50, selected_initial_right_x_pow)
    power_up_invisible_right = Invisible("Images/PowerUps/invisible.png", 50, selected_initial_right_x_pow)

    incoming_powerups_list_right_road = pygame.sprite.Group()

    # Add Objects to Lists
    all_sprites_list.add(playerCar1, playerCar2, car1, car2, car3, car4, car5, car6, car7, car8, power_up_invincibility,
                         power_up_slowing, power_up_jet_bomb, power_up_extra_life, power_up_size_change,
                         power_up_invisible, power_up_no_power_up, power_up_key_inversion, power_up_invincibility_right,
                         power_up_slowing_right, power_up_jet_bomb_right, power_up_extra_life_right,
                         power_up_size_change_right, power_up_invisible_right, power_up_no_power_up_right,
                         power_up_key_inversion_right)
    incoming_cars_list_left.add(car1, car2, car3, car4)
    incoming_cars_list_right.add(car5, car6, car7, car8)
    incoming_powerups_list_left_road.add(power_up_invincibility, power_up_slowing, power_up_jet_bomb,
                                         power_up_extra_life, power_up_size_change, power_up_invisible,
                                         power_up_no_power_up, power_up_key_inversion)
    incoming_powerups_list_right_road.add(power_up_invincibility_right, power_up_slowing_right, power_up_jet_bomb_right,
                                          power_up_extra_life_right, power_up_size_change_right,
                                          power_up_invisible_right, power_up_no_power_up_right,
                                          power_up_key_inversion_right)
    player_car_list1.add(playerCar1)
    player_car_list2.add(playerCar2)

    # GAME EXTRAS:

    # Stored Powerup
    stored_powerup_1 = None
    stored_powerup_2 = None
    activate_stored_powerup_1 = False
    activate_stored_powerup_2 = False

    # Stored Powerup Box
    square_size = (80, 80)
    rounded_square = pygame.Surface(square_size, pygame.SRCALPHA)
    border_radius = 15
    pygame.draw.rect(rounded_square, BLACK, rounded_square.get_rect(), border_radius=border_radius)
    square_position_1 = (485, 50)
    square_position_2 = (335, 50)

    # Powerup Bar
    max_powerup_bar_width = 170
    powerup_bar_x = 685
    powerup_bar_Y = 50
    powerup_bar_width = 162

    # PARTICLES:
    # Particle Event
    PARTICLE_EVENT = pygame.USEREVENT + 1
    # Time in miliseconds we want to pass between each call of the event
    pygame.time.set_timer(PARTICLE_EVENT, 5)

    particle1 = Particle(pygame.Color('red'))
    particle2 = Particle(pygame.Color('orange'))
    particle3 = Particle(pygame.Color('yellow'))

    particle4 = Particle(pygame.Color('red'))
    particle5 = Particle(pygame.Color('orange'))
    particle6 = Particle(pygame.Color('yellow'))

    # Controls whether the player's input should or not be considered
    movement_enabled1 = True
    movement_enabled2 = True

    # Variable to track the active power-up
    active_powerup = None

    # Score
    score = 0
    updated_score = 0

    # Game level
    level = 1
    first_lvl_up = 60

    # Winner
    winner = None

    # Game State
    carryOn = True
    game_over = False

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event.pos):
                    paused = not paused  # Resume game

            # activate particle event
            if event.type == PARTICLE_EVENT:
                particle1.add_particles(playerCar1.rect.x, playerCar1.rect.y)
                particle2.add_particles(playerCar1.rect.x, playerCar1.rect.y)
                particle3.add_particles(playerCar1.rect.x, playerCar1.rect.y)

                particle4.add_particles(playerCar2.rect.x, playerCar2.rect.y)
                particle5.add_particles(playerCar2.rect.x, playerCar2.rect.y)
                particle6.add_particles(playerCar2.rect.x, playerCar2.rect.y)

        if paused:
            resume_button, how_to_play_button, quit_button = display_pause_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_clicked(event.pos):
                        paused = False  # Resume game
                    elif how_to_play_button.is_clicked(event.pos):
                        screen.blit(pygame.image.load("Images/Design/instructions_pause.png"), (0, 0))
                        pygame.display.flip()  # Update the screen to show changes

                        waiting_for_click = True
                        while waiting_for_click:
                            for event in pygame.event.get():  # Event handling loop
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    waiting_for_click = False
                    elif quit_button.is_clicked(event.pos):
                        carryOn = False  # Quit game
            continue  # Skip the rest of the game loop when paused

        if movement_enabled1:
            # Move player 1 car (with input from the user):
            if not playerCar1.key_inverse:
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
                    # Ensure the player's car stays within the bottom boundary of the road
                    if playerCar1.rect.y + playerCar1.speed < SCREEN_HEIGHT - playerCar1.rect.height \
                            and not playerCar1.rect.colliderect(playerCar2.rect.move(0, -playerCar1.speed)):
                        playerCar1.moveDown(5)

                # Key Inverse powerup activared
            if playerCar1.key_inverse:
                if keys[pygame.K_RIGHT]:
                    playerCar1.moveLeft(5)
                    # Ensure the player's car stays within the left boundary of the right road
                    playerCar1.rect.x = max(road_x_right, playerCar1.rect.x)
                if keys[pygame.K_LEFT]:
                    playerCar1.moveRight(5)
                    # Ensure the player's car stays within the right boundary of the right road
                    playerCar1.rect.x = min(road_x_right + road_width - playerCar1.rect.width, playerCar1.rect.x)
                if keys[pygame.K_DOWN]:
                    playerCar1.moveUp(5)
                    # Ensure the player's car stays within the top boundary of the road
                    playerCar1.rect.y = max(0, playerCar1.rect.y)
                if keys[pygame.K_UP]:
                    playerCar1.moveDown(5)
                # Ensure the player's car stays within the bottom boundary of the road
                playerCar1.rect.y = min(SCREEN_HEIGHT - playerCar1.rect.height, playerCar1.rect.y)
            if keys[pygame.K_RSHIFT] and stored_powerup_1 is not None:
                # Activatrd powerup effect of stored powerup
                activate_stored_powerup_1 = True

        if movement_enabled2:
            # Movement for player 2
            if not playerCar2.key_inverse:
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
                # Key Inverse powerup activared
            if playerCar2.key_inverse:
                # Movement for player 2
                if keys[pygame.K_d]:  # Left
                    playerCar2.moveLeft(5)
                    # Ensure the player's car stays within the left boundary of the left road
                    playerCar2.rect.x = max(road_x_left, playerCar2.rect.x)
                if keys[pygame.K_a]:  # Right
                    playerCar2.moveRight(5)
                    # Ensure the player's car stays within the right boundary of the left road
                    playerCar2.rect.x = min(road_x_left + road_width - playerCar2.rect.width, playerCar2.rect.x)
                if keys[pygame.K_s]:  # Up
                    playerCar2.moveUp(5)
                    playerCar2.rect.y = max(0, playerCar2.rect.y)
                if keys[pygame.K_w]:  # Down
                    playerCar2.moveDown(5)
                    playerCar2.rect.y = min(SCREEN_HEIGHT - playerCar2.rect.height, playerCar2.rect.y)
            if keys[pygame.K_LSHIFT] and stored_powerup_2 is not None:
                # Activatrd powerup effect of stored powerup
                activate_stored_powerup_2 = True

        # Draw background
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, GREY, [road_x_left, 0, road_width, SCREEN_HEIGHT])  # Left Road
        pygame.draw.rect(screen, GREY, [road_x_right, 0, road_width, SCREEN_HEIGHT])  # Right Road

        # DRAW ROAD MARKINGS FOR THE RIGHT ROAD
        middle_line_x_right = road_x_right + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x_right, 0], [middle_line_x_right, SCREEN_HEIGHT], 6)

        dashed_lines_x_right = [road_x_right + (i * lane_width) for i in range(1, num_lanes)]

        offset_y = (pygame.time.get_ticks() // road_speed1) % 40
        for line_x in dashed_lines_x_right:
            for line_y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y + offset_y], [line_x, line_y + 20 + offset_y], 1)

        # DRAW ROAD MARKINGS FOR THE LEFT ROAD
        middle_line_x_left = road_x_left + road_width / 2
        pygame.draw.line(screen, WHITE, [middle_line_x_left, 0], [middle_line_x_left, SCREEN_HEIGHT], 6)

        dashed_lines_x_left = [road_x_left + (i * lane_width) for i in range(1, num_lanes)]

        offset_y = (pygame.time.get_ticks() // road_speed2) % 40
        for line_x in dashed_lines_x_left:
            for line_y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(screen, WHITE, [line_x, line_y + offset_y], [line_x, line_y + 20 + offset_y], 1)

        # Draw player's cars
        if playerCar1.visible:
            player_car_list1.draw(screen)
        if playerCar2.visible:
            player_car_list2.draw(screen)

        # Blit Stored Powerup Box
        if stored_powerup_1 is not None:  # boxes only appear if there are stored powerup
            screen.blit(rounded_square, square_position_1)
        if stored_powerup_2 is not None:
            screen.blit(rounded_square, square_position_2)

        # Draw Power ups
        incoming_powerups_list_right_road.draw(screen)
        incoming_powerups_list_left_road.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list_right:
            # Velocity
            car.moveDown(playerCar1.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()
            incoming_cars_list_right.draw(screen)

        # Move the opponent cars (automatically):
        for car in incoming_cars_list_left:
            # Velocity
            car.moveDown(playerCar2.speed)
            # When the cars go out of the screen, we move them up again
            if car.rect.y >= SCREEN_HEIGHT:
                car.reshape()
            incoming_cars_list_left.draw(screen)

        # Draw the explosion
        explosion_group.update()
        explosion_group.draw(screen)

        # Handle collisions with PlayerCar1
        for car in incoming_cars_list_right:
            if not playerCar1.ghost and pygame.sprite.collide_mask(playerCar1, car) is not None:
                if playerCar1.jet_bomb:
                    # saves incoming car posiion before it being reshaped
                    car_current_x = car.rect.x
                    car_current_y = car.rect.y + car.height / 2  # makes the explosion closer to the playerCar
                    # incoming car "vanishes"
                    car.reshape()
                    # explosion animation created and added to the sprite list
                    explosion = Explosion(car_current_x, car_current_y)
                    explosion_group.add(explosion)

                if not playerCar1.invincible and not playerCar1.jet_bomb:
                    if config.is_sound_enabled:
                        car_collision.play()
                    # Collision detected
                    playerCar1.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar1.rect.x, playerCar1.rect.y), RED)
                    # Car loses its powerup
                    for powerup in incoming_powerups_list_right_road:
                        powerup.effect_over(playerCar1, incoming_cars_list_right, screen, enemy_player=playerCar2)
                    # Activate invincibility for 5 seconds after collision
                    playerCar1.ghost = True
                    # playerCar.invincible is a check to not enter playerCar.ghost timer when we activate invincibility powerup
                    playerCar1.invincible = False
                    ghost_start_time_1 = pygame.time.get_ticks()
                    ghost_duration = 2000
                    # Reset player's car position
                    playerCar1.rect.x = right_road_center - 25
                    playerCar1.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left --> end the game
                    if playerCar1.lives == 0:
                        game_over = True

        # Handle collisions with PlayerCar2
        for car in incoming_cars_list_left:
            if not playerCar2.ghost and pygame.sprite.collide_mask(playerCar2, car) is not None:
                if playerCar2.jet_bomb:
                    # saves incoming car posiion before it being reshaped
                    car_current_x = car.rect.x
                    car_current_y = car.rect.y + car.height / 2  # makes the explosion closer to the playerCar
                    # incoming car "vanishes"
                    car.reshape()
                    # explosion animation created and added to the sprite list
                    explosion = Explosion(car_current_x, car_current_y)
                    explosion_group.add(explosion)

                if not playerCar2.invincible and not playerCar2.jet_bomb:
                    if config.is_sound_enabled:
                        car_collision.play()
                    # Collision detected
                    playerCar2.lives -= 1
                    show_message(messages_group, "-1", message_font, (playerCar2.rect.x, playerCar2.rect.y), RED)
                    # Car loses its powerup
                    for powerup in incoming_powerups_list_left_road:
                        powerup.effect_over(playerCar2, incoming_cars_list_left, screen, enemy_player=playerCar1)
                    # Activate invincibility for 5 seconds after collision
                    playerCar2.ghost = True
                    # playerCar.invincible is a check to not enter playerCar.ghost timer when we activate invincibility powerup
                    playerCar2.invincible = False
                    ghost_start_time_2 = pygame.time.get_ticks()
                    ghost_duration = 2000
                    # Reset player's car position
                    playerCar2.rect.x = left_road_center - 25
                    playerCar2.rect.y = SCREEN_HEIGHT - 150
                    # If no lives left --> end the game
                    if playerCar2.lives == 0:
                        game_over = True

            if game_over:
                if playerCar1.lives > 0:
                    winner = "Player 1 wins!"
                elif playerCar2.lives > 0:
                    winner = "Player 2 wins!"

                # Display the game-over screen
                screen.blit(game_over_background, (0, 0))

                # Game over text
                game_over_text = game_over_font.render("GAME OVER", True, WHITE)
                game_over_x = (SCREEN_WIDTH - game_over_text.get_width()) // 2
                game_over_y = (SCREEN_HEIGHT - game_over_text.get_height()) // 2
                screen.blit(game_over_text, (game_over_x, game_over_y))

                # Winner text
                winner_text = winner_font.render(f"{winner}", True, WHITE)
                winner_x = (SCREEN_WIDTH - winner_text.get_width()) // 2
                winner_y = game_over_y + game_over_text.get_height() + 20
                screen.blit(winner_text, (winner_x, winner_y))

                pygame.display.flip()  # Update the display

                # Short delay before interface() display
                pygame.time.delay(2000)

                # The game is over, set the flag and exit the game loop
                carryOn = False

        # Update invincibility status based on elapsed time
        # Player car 1
        if playerCar1.ghost:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time_1
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar1.ghost = False
                playerCar1.visible = True
            else:
                playerCar1.visible = (elapsed_time // toggle_interval) % 2 == 0

        # Player car 2
        if playerCar2.ghost:
            elapsed_time = pygame.time.get_ticks() - ghost_start_time_2
            toggle_interval = 200
            if elapsed_time >= ghost_duration:
                playerCar2.ghost = False
                playerCar2.visible = True
            else:
                playerCar2.visible = (elapsed_time // toggle_interval) % 2 == 0

        all_sprites_list.update()

        # Power up picker --> probability for Right Road:
        if all(not powerup.active for powerup in incoming_powerups_list_right_road) and stored_powerup_1 is None:

            spawn_prob = random.uniform(0, 100)

            # Hearts --> when activated (hearts only spawn when player needs them)
            if (0 <= spawn_prob < 20 and playerCar1.lives == 1) or (0 <= spawn_prob < 5 and playerCar1.lives == 2):
                power_up_extra_life_right.active = True
            # Size Change
            elif 20 <= spawn_prob < 35:
                power_up_size_change_right.active = True
            # Slow Down
            elif 35 <= spawn_prob < 45:
                power_up_slowing_right.active = True
            # Invincibility
            elif 45 <= spawn_prob <= 50:
                power_up_invincibility_right.active = True
            # Jet Bomb
            elif 50 <= spawn_prob <= 55:
                power_up_jet_bomb_right.active = True
            # Key Inversin
            elif 80 <= spawn_prob <= 90:
                power_up_key_inversion_right.active = True
            # No powerup
            elif 90 <= spawn_prob <= 95:
                power_up_no_power_up_right.active = True
            # Invisible
            elif 95 <= spawn_prob <= 100:
                power_up_invisible_right.active = True

        # Power up cycle for right road
        for powerup in incoming_powerups_list_right_road:
            # POWERUP contact with playerCar + respawn
            if powerup.active:
                powerup.moveDown(powerup.speed)
                if stored_powerup_1 is None:  # Make powerups stop when we have a stored one
                    powerup.moveDown(powerup.speed)

                if pygame.sprite.collide_mask(playerCar1, powerup) is not None and playerCar1.can_catch_powerup:
                    if config.is_sound_enabled:
                        catch_powerup.play()
                    powerup.powered_up = True

                    if any(p.powered_up for p in incoming_powerups_list_right_road if
                           p != powerup):  # Checks if any active power ups in list
                        powerup.active = False
                        powerup.powered_up = False
                        stored_powerup_1 = powerup
                        powerup.rect.x = square_position_1[0] + 15
                        powerup.rect.y = square_position_1[1] + 15
                        print('x')
                    else:
                        powerup.active_time = pygame.time.get_ticks()
                        powerup.affect_player(playerCar1, screen, messages_group, enemy_player=playerCar2)
                        powerup.affect_traffic(incoming_cars_list_right, messages_group)
                        powerup.reshape(road_x_right, lane_width)

                # Powerup isn't caught
                elif powerup.rect.y >= SCREEN_HEIGHT:
                    powerup.reshape(road_x_right, lane_width)

        # Activate Stored Powerup
        for powerup in incoming_powerups_list_right_road:
            if stored_powerup_1 and activate_stored_powerup_1:
                # Activate the stored power-up
                stored_powerup_1.powered_up = True
                # Determines storage powerup starting time
                stored_powerup_1.active_time = pygame.time.get_ticks()
                # If player activates storage powerup before current powerup effect finishes. Current powerup effect ends
                powerup.effect_over(playerCar1, incoming_cars_list_right, screen, enemy_player=playerCar2)
                # Ativates storage powerup effect
                stored_powerup_1.affect_player(playerCar1, screen, messages_group, enemy_player=playerCar2)
                stored_powerup_1.affect_traffic(incoming_cars_list_right, messages_group)
                # Makes storepowerup icon disappear
                stored_powerup_1.reshape(road_x_right, lane_width)
                # Clears the stored power-up after usage
                stored_powerup_1 = None
                # Deactivates Trigger
                activate_stored_powerup_1 = False

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
                # Powerup effect time is over
                else:
                    powerup.effect_over(playerCar1, incoming_cars_list_right, screen, enemy_player=playerCar2)
                    powerup.powered_up = False

                # Make visual effect of slowing last 1 milisecond (since power up picked)
                if elapsed_time < 100:
                    for car in incoming_cars_list_right:
                        if car.is_speed_reduced and car.slowing_mask is not None:
                            # Creates a blue mask on top of every incoming car (defined in car.reshape())
                            screen.blit(car.slowing_mask, (car.rect.x, car.rect.y))
                # Makes cars return to normal speed before jet_bomb ends, since due to their high speed, playerCar
                # was almost guaranteed to take a hit from cars that had already spawned before the powerup ended
                # Cant redefine speed in powerup feature jet_bomb else, since cars start to lose fps.
                if elapsed_time > powerup.duration - 100:
                    for car in incoming_cars_list_right:
                        if playerCar1.jet_bomb:
                            car.speed = random.randint(1, 4)

        # Power up countdown Bar
        for powerup in incoming_powerups_list_right_road:
            if powerup.powered_up:
                pygame.draw.rect(screen, WHITE,
                                 [powerup_bar_x - 5, powerup_bar_Y - 5, max_powerup_bar_width + 6, 34])  # border
                pygame.draw.rect(screen, BLACK,
                                 [powerup_bar_x - 4, powerup_bar_Y - 4, max_powerup_bar_width + 4, 32])  # background
                pygame.draw.rect(screen, BLUE, [powerup_bar_x, powerup_bar_Y, powerup_bar_width, 24])  # timer bar

        # Power up contact with incoming cars
        for powerup in incoming_powerups_list_right_road:
            for car in incoming_cars_list_right:
                # Condition to only run this code on the screen player can see
                # ... otherwise powerup appear to fast in the screen ... and to reduce collisions we can´t see
                if (0 <= powerup.rect.x <= SCREEN_WIDTH - powerup.rect.width and
                        -5 <= powerup.rect.y <= SCREEN_HEIGHT - powerup.rect.height and
                        0 <= car.rect.x <= SCREEN_WIDTH - car.rect.width and
                        -5 <= car.rect.y <= SCREEN_HEIGHT - car.rect.height):
                    if pygame.sprite.collide_mask(powerup, car) is not None:
                        # velocidade aumenta à medida que os níveis sobem
                        powerup.speed = 10 + (level - 1) * 3

        #  # NoPowerUp Effect
        if not playerCar2.can_catch_powerup:
            # Creates a red mask on top of player affected by NoPowerUp powerup
            screen.blit(playerCar2.nopowerup_mask, (playerCar2.rect.x, playerCar2.rect.y))

        # KeyInverse Effect
        if playerCar2.key_inverse:
            # Creates a yellow mask on top of player affected by KeyInverse powerup
            screen.blit(playerCar2.key_inverse_mask, (playerCar2.rect.x, playerCar2.rect.y))

        # Invincibility Effect
        if playerCar1.invincible:
            screen.blit(playerCar1.mask_surface, (playerCar1.rect.x, playerCar1.rect.y))

        # Jet_bomb features
        if playerCar1.jet_bomb:
            if config.is_sound_enabled:
                jet_bomb.play()
            # Display playerCar nitro particles
            particle1.emit(screen)
            particle2.emit(screen)
            particle3.emit(screen)
            # Car goes "pilot-mode"
            movement_enabled1 = False
            playerCar1.moveUp(1)
            # Doesn't let the car speed up to the top of the screen
            if playerCar1.rect.y < 150:
                playerCar1.moveDown(1)
            # Increase incoming car speed (high speed effect)
            for car in incoming_cars_list_right:
                car.speed += 0.5
            # Increase road velocity (high speed effect)
            road_speed1 = 2
        else:
            movement_enabled1 = True
            road_speed1 = 10

        # Power up picker --> probability for Left Road:
            if all(not powerup.active for powerup in incoming_powerups_list_left_road) and stored_powerup_2 is None:

                spawn_prob = random.uniform(0, 100)

                # Hearts --> when activated (hearts only spawn when player needs them)
                if (0 <= spawn_prob < 20 and playerCar2.lives == 1) or (0 <= spawn_prob < 5 and playerCar2.lives == 2):
                    power_up_extra_life.active = True
                # Size Change
                elif 20 <= spawn_prob < 35:
                    power_up_size_change.active = True
                # Slow Down
                elif 35 <= spawn_prob < 45:
                    power_up_slowing.active = True
                # Invincibility
                elif 45 <= spawn_prob <= 50:
                    power_up_invincibility.active = True
                # Jet Bomb
                elif 50 <= spawn_prob <= 55:
                    power_up_jet_bomb.active = True
                # Key Inversin
                elif 85 <= spawn_prob <= 90:
                    power_up_key_inversion.active = True
                # No powerup
                elif 90 <= spawn_prob <= 95:
                    power_up_no_power_up.active = True
                # Invisible
                elif 95 <= spawn_prob <= 100:
                    power_up_invisible.active = True

        # Power up cycle for Left road
        for powerup in incoming_powerups_list_left_road:

            # POWERUP contact with playerCar + respawn
            if powerup.active:
                powerup.moveDown(powerup.speed)
                if stored_powerup_2 is None:  # Make powerups stop when we have a stored one
                    powerup.moveDown(powerup.speed)

                if pygame.sprite.collide_mask(playerCar2, powerup) is not None and playerCar2.can_catch_powerup:
                    if config.is_sound_enabled:
                        catch_powerup.play()
                    powerup.powered_up = True

                    if any(p.powered_up for p in incoming_powerups_list_left_road if p != powerup):  # Checks if any active power ups in list
                        powerup.active = False
                        powerup.powered_up = False
                        stored_powerup_2 = powerup
                        powerup.rect.x = square_position_2[0] + 15
                        powerup.rect.y = square_position_2[1] + 15
                    else:
                        powerup.active_time = pygame.time.get_ticks()
                        powerup.affect_player(playerCar2, screen, messages_group, enemy_player=playerCar1)
                        powerup.affect_traffic(incoming_cars_list_left, messages_group)
                        powerup.reshape(road_x_left, lane_width)

                # Powerup isn't caught
                elif powerup.rect.y >= SCREEN_HEIGHT:
                    powerup.reshape(road_x_left, lane_width)

        # Activate Stored Powerup
        for powerup in incoming_powerups_list_left_road:
            if stored_powerup_2 and activate_stored_powerup_2:
                # Activate the stored power-up
                stored_powerup_2.powered_up = True
                # Determines storage powerup starting time
                stored_powerup_2.active_time = pygame.time.get_ticks()
                # If player activates storage powerup before current powerup effect finishes. Current powerup effect ends
                powerup.effect_over(playerCar2, incoming_cars_list_left, screen, enemy_player=playerCar1)
                # Ativates storage powerup effect
                stored_powerup_2.affect_player(playerCar2, screen, messages_group, enemy_player=playerCar1)
                stored_powerup_2.affect_traffic(incoming_cars_list_left, messages_group)
                # Makes storepowerup icon disappear
                stored_powerup_2.reshape(road_x_left, lane_width)
                # Clears the stored power-up after usage
                stored_powerup_2 = None
                # Deactivates Trigger
                activate_stored_powerup_2 = False

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
                # Powerup effect time is over
                else:
                    powerup.effect_over(playerCar2, incoming_cars_list_left, screen, enemy_player=playerCar1)
                    powerup.powered_up = False

                # Make visual effect of slowing last 1 milisecond (since power up picked)
                if elapsed_time < 100:
                    for car in incoming_cars_list_left:
                        # Only works if power up slowing is caught
                        if car.is_speed_reduced and car.slowing_mask is not None:
                            # Creates a blue mask on top of every incoming car (defined in car.reshape())
                            screen.blit(car.slowing_mask, (car.rect.x, car.rect.y))
                # Makes cars return to normal speed before jet_bomb ends, since due to their high speed, playerCar
                # was almost guaranteed to take a hit from cars that had already spawned before the powerup ended
                # Cant redefine speed in powerup feature jet_bomb else, since cars start to lose fps.
                if elapsed_time > powerup.duration - 100:
                    for car in incoming_cars_list_left:
                        if playerCar2.jet_bomb:
                            car.speed = random.randint(1, 4)

        # Power up countdown Bar
        for powerup in incoming_powerups_list_left_road:
            if powerup.powered_up:
                pygame.draw.rect(screen, WHITE,
                                 [powerup_bar_x - 639, powerup_bar_Y - 5, max_powerup_bar_width + 6, 34])  # border
                pygame.draw.rect(screen, BLACK,
                                 [powerup_bar_x - 638, powerup_bar_Y - 4, max_powerup_bar_width + 4, 32])  # background
                pygame.draw.rect(screen, RED, [powerup_bar_x - 637, powerup_bar_Y, powerup_bar_width, 24])  # timer bar

        # Power up contact with incoming cars
        for powerup in incoming_powerups_list_left_road:
            for car in incoming_cars_list_left:
                # Condition to only run this code on the screen player can see
                # ... otherwise powerup appear to fast in the screen ... and to reduce collisions we can´t see
                if (0 <= powerup.rect.x <= SCREEN_WIDTH - powerup.rect.width and
                        -5 <= powerup.rect.y <= SCREEN_HEIGHT - powerup.rect.height and
                        0 <= car.rect.x <= SCREEN_WIDTH - car.rect.width and
                        -5 <= car.rect.y <= SCREEN_HEIGHT - car.rect.height):
                    if pygame.sprite.collide_mask(powerup, car) is not None:
                        # velocidade aumenta à medida que os níveis sobem
                        powerup.speed = 10 + (level - 1) * 3

        # NoPowerUp Effect
        if not playerCar1.can_catch_powerup:
            # Creates a red mask on top of player affected by NoPowerUp powerup
            screen.blit(playerCar1.nopowerup_mask, (playerCar1.rect.x, playerCar1.rect.y))

        # KeyInverse Effect
        if playerCar1.key_inverse:
            # Creates a yellow mask on top of player affected by KeyInverse powerup
            screen.blit(playerCar1.key_inverse_mask, (playerCar1.rect.x, playerCar1.rect.y))

        # Invincibility Effect
        if playerCar2.invincible:
            screen.blit(playerCar2.mask_surface, (playerCar2.rect.x, playerCar2.rect.y))

        # Jet_bomb features
        if playerCar2.jet_bomb:
            if config.is_sound_enabled:
                jet_bomb.play()
            # Display playerCar nitro particles
            particle4.emit(screen)
            particle5.emit(screen)
            particle6.emit(screen)
            # Car goes "pilot-mode"
            movement_enabled2 = False
            playerCar2.moveUp(1)
            # Doesn't let the car speed up to the top of the screen
            if playerCar2.rect.y < 150:
                playerCar2.moveDown(1)
            # Increase incoming car speed (high speed effect)
            for car in incoming_cars_list_left:
                car.speed += 0.5
            # Increase road velocity (high speed effect)
            road_speed2 = 2
        else:
            movement_enabled2 = True
            road_speed2 = 10

        all_sprites_list.update()

        # Draw the black ribbon for the game settings
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, SCREEN_WIDTH, 30])

        # Draw button
        screen.blit(pause_img, (380, 5))

        # Update timer
        minutes, seconds = divmod(updated_score, 60)
        score_text = score_font.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Calculate the x-coordinate to center the text
        score_x = (SCREEN_WIDTH - score_text.get_width()) // 2
        screen.blit(score_text, (score_x, 5))

        # Level upgrade
        if updated_score == first_lvl_up:
            # Increase the level every minute
            level += 1
            first_lvl_up = first_lvl_up + 60

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

            # Play level-up sound
            if config.is_sound_enabled:
                level_up.play()

            pygame.display.flip()  # Update the full display Surface to the screen

            # Pause for 1 seconds
            pygame.time.wait(1000)
            # Clear the screen
            screen.blit(background, (0, 0))
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

        # Update score
        score += 1
        updated_score = score // 60

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame

    if not carryOn:
        # Transition to the interface
        from interface import interface
        interface()
