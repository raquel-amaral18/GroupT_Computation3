import random
# pygame.org
# pygame works as an old movie that never ends and repeats itself forever (until you die)
import pygame

from car import *
from powerups import *
from messages import *


def game(SCREEN_WIDTH, SCREEN_HEIGHT):
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
    ORANGE = (255, 159, 28)
    BLACK = (0, 0, 0)

    # Font
    arialfont_timer = pygame.font.SysFont('monospace', 20, bold=True)
    message_font = pygame.font.SysFont('monospace', 30, bold=True)
    level_font = pygame.font.SysFont('monospace', 150, bold=True)

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
    playerCar = PlayerCar("Images/00C.png", 50)
    playerCar.rect.x = (SCREEN_WIDTH - playerCar.rect.width) // 2  # which column the car starts
    playerCar.rect.y = SCREEN_HEIGHT - 150  # which row the car starts

    # Opponent cars
    # Opponent cars
    car1 = IncomingCars("Images/04C.png", 50, 2, road_x + (lane_width - 50) // 2)
    car2 = IncomingCars("Images/02C.png", 50, 4, road_x + lane_width + (lane_width - 50) // 2)
    car3 = IncomingCars("Images/05C.png", 50, 3, road_x + (2 * lane_width) + (lane_width - 50) // 2)
    car4 = IncomingCars("Images/07C.png", 50, 1, road_x + (3 * lane_width) + (lane_width - 50) // 2)

    all_sprites_list = pygame.sprite.Group()
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

    # Controls whether the player's input should or not be considered
    movement_enabled = True

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
        offset_y = (pygame.time.get_ticks() // 10) % 40  # Smaller divisor == faster movement
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
            incoming_cars_list.draw(screen)



        # CARS:
        #  car_collision_list = pygame.sprite.spritecollide(playerCar, incoming_cars_list, False)  # If True --> Pacman
        # if len(car_collision_list) > 0:
        # carryOn = False

        for car in incoming_cars_list:
            if not playerCar.ghost and pygame.sprite.collide_mask(playerCar, car) is not None:
                if playerCar.pac_man:
                    car.reshape()
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
                    if playerCar.lives == 0:
                        carryOn = True

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

        """ 
        (Segunda)
            
            1º - Tratar Jet_bom --> mudar nome --> explosion --> playerCar glowing
            
         (Terça)   
            
            2º - Permitir usar só 2 power ups ao mm tempo --> criar variável que conta os powerups apanhados --> 
                 Quando essa variável chega a 2 ... n permitir ativar mais powerups ... smp que um power up acaba, 
                 subtrair 1 dessa variável, para dar espaço ao próximo ... quando player tentar apanhar terceiro powerup
                 ao mm tempo, display mensagem "FULL" --> sq fazer a cena do guardar um powerup para usar depois (EXTRA 1)
            
            3ª -  Não deixar apanhar invincibility quando tamos usar um powerup ... n deixar apanhar jet_bomb quando 
                  tamos a usar invincibility (vice-versa)
                  
            4º - if playerCar collides with car ... any powerup activated ends
        
        (Quarta)
        
            5.(-1)º - Criar 2 powerup timer bars no multiplayer, uma de cada lado de acordo com carros e suas cores
            
            5º - powerups negativos (inverter setas...aumentar/diminuir a speed...deixar carro invisvel...increase speed of incoming cars (slowing inverse))
            
            Perguntar Davide ou Liah --> 9º - Ver se resolvo powerup collision com cars não funcionar 100% das vezes
                
            6º - Perceber coins, e ver como implementar Magnet (tempo)
            
            7º - POWERUP SPEED AUMENTA COM NIVEL (Extra 4)
            
            8º - ver se faço algum extra
            
        (Quinta)
            
            8º- Meter som em tudo
            
            9º- incoming cars effect no slowing
            
            10º- mais effects
            
            11º - ajustar probabilidades e tempos para ficar bacano
            
            
            Extras: 
            
            - In line powerups...have 1, 2 pr 3 slotes...when player picks ups power_up while using anotehr powerup...
            icon stored in box, whe need to click button to activate item (Mario Kart)
            
            - Adicionar cenas à estrada, tipo borders ou textura...que muda a cada nível...em loop
            (perceber como niveis funcionam)
            
            -Moving Background que acompanha linhas da estrada
            (perceber como é que funciona movimento das linhas da estrada)
            
            -Aumentar dificuldade à medida que nível sobre (if level == 3:   car.speed = 20 ...)
        """

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
                pygame.draw.rect(screen, WHITE, [powerup_bar_x - 5, powerup_bar_Y - 5, max_powerup_bar_width + 6, 34])  # border
                pygame.draw.rect(screen, BLACK, [powerup_bar_x - 4, powerup_bar_Y - 4, max_powerup_bar_width + 4, 32])  # background
                pygame.draw.rect(screen, ORANGE, [powerup_bar_x, powerup_bar_Y, powerup_bar_width, 24])  # timer bar

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

        # GAME SETTINGS:
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
        timer_text = arialfont_timer.render("{:02}:{:02}".format(minutes, seconds), True, WHITE)

        # Level upgrade
        if minutes > last_minute:
            # Increase the level every minute
            level += 1
            last_minute = minutes

            # Increase playerCar speed
            playerCar.speed += 1  # You can adjust the increment value as needed

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

        # Calculate the x-coordinate to center the text
        timer_x = (SCREEN_WIDTH - timer_text.get_width()) // 2
        screen.blit(timer_text, (timer_x, 5))

        # Update lives
        for i in range(playerCar.lives):
            screen.blit(heart_img, (SCREEN_WIDTH - 40 - i * 35, 5))

        # Draw and update messages
        messages_group.draw(screen)
        messages_group.update()

        pygame.display.flip()  # Refresh the screen
        clock.tick(60)  # 60 frame per millisecond

    pygame.quit()  # Terminate the pygame
