from abc import ABC, abstractmethod
import pygame
import random


def get_power_up(probabilities):
    total = 100
    spawn_prob = random.randint(0, total)
    cumulative = 0
    for power_up, prob in probabilities.items():
        cumulative += prob
        if spawn_prob <= cumulative:
            return power_up
    return None


class PowerUp(ABC, pygame.sprite.Sprite):
    def __init__(self, width, height, image,
                 speed):  # , pickup_sound, activation_sound, appearence_rate

        super().__init__()
        self.picked_up = False
        self.activation_time = None
        self.width = width
        self.height = height
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = speed
        # self.pickup_sound = pickup_sound
        # self.activation_sound = activation_sound
        # self.appearence_rate = appearence_rate

        self.rect = self.image.get_rect()

    @abstractmethod
    def affect_player(self, player):
        pass

    @abstractmethod
    def affect_traffic(self, traffic):
        pass

    def moveDown(self, pixels):
        self.rect.y += pixels

    """
    se função n fizer codigo mais eficiente simplificar for loop do game
    """

    def spawn(self, road_x, lane_width):
        random_lane = random.randint(0, 3)
        edge_offset = 10

        # Choose randomly to position closer to the left or right edge within the lane
        if random.choice([True, False]):
            self.rect.x = road_x + (random_lane * lane_width) + edge_offset
        else:
            self.rect.x = road_x + (random_lane * lane_width) + (lane_width - self.rect.width) - edge_offset

        # Power up goes Back to top
        self.rect.y = random.randint(-1000, 0)

    @abstractmethod
    def power_up_cicle(self, playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic):
        # Power up falls
        self.moveDown(speed)
        # Power collides or isn't catch
        if pygame.sprite.collide_mask(playerCar, self) is not None or self.rect.y >= screen_height:
            # Power up dispawns
            power_up_list.remove(self)
            # Power up relocates
            self.spawn(road_x, lane_width)

    #  pygame.mixer.Sound.play(self.activation_sound)


class Invincibility(PowerUp):
    def __init__(self, width, height, image, initial_x, speed=0):
        super().__init__(width, height, image, speed)
        self.initial_x = initial_x
        self.rect.x = self.initial_x
        self.rect.y = random.randint(-1000, 0)
        self.invincibility_duration = 5000

    def affect_player(self, player, traffic):
        """
        Descobrir como fazer um efeito do power up durar x tempo antes de acabar logo
        """
        # player.invincible = True

        # player.invincibility_start_time = pygame.time.get_ticks()
        # for car in traffic:
        # if not player.invincible and pygame.sprite.collide_mask(player, car) is not None:
        # if lives[0] == 3:
        #    lives[0] = 3
        # if lives[0] == 2:
        #   lives[0] = 2
        # if lives[0] == 1:
        #   lives[0] = 1
        # print('x')
        """
        Doesn't Work
        """
        if player.invincible:
            current_time = pygame.time.get_ticks()
        if current_time - player.invincibility_start_time > 2000:  # 2 seconds duration
            player.invincible = False
        else:
            # Check for collisions during invincibility
            for car in traffic:
                if pygame.sprite.collide_mask(player, car) is not None:
                    print("Collision with car while invincible")

    def affect_traffic(self, traffic):
        pass

    def power_up_cicle(self, playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic):
        # Power up falls
        self.moveDown(speed)
        # Heart collides
        """
        Invincibility: makes the player invincible for a limited amount of time (add invisibility) 
        """
        if pygame.sprite.collide_mask(playerCar, self) is not None:
            # playerCar.invincible = True
            # playerCar.invincibility_start_time = pygame.time.get_ticks()
            # Power up despawns
            power_up_list.remove(self)
            # Power up relocates
            self.spawn(road_x, lane_width)

        # Heart isn't catch
        elif self.rect.y >= screen_height:
            # Power up dispawns
            power_up_list.remove(self)
            # Power up relocates
            self.spawn(road_x, lane_width)

        # if playerCar.invincible and pygame.time.get_ticks() - playerCar.invincibility_start_time > self.invincibility_duration:
        # playerCar.invincible = False


class Slowing(PowerUp):
    def __init__(self, width, height, image, initial_x, speed=0):
        super().__init__(width, height, image, speed)
        self.initial_x = initial_x
        self.rect.x = self.initial_x
        self.rect.y = random.randint(-1000, 0)

    def affect_player(self, player):
        pass

    def affect_traffic(self, traffic):
        pass

    def power_up_cicle(self, playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic):
        super().power_up_cicle(playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic)
        """
        Slowing: incoming traffic cars slower for a limited amount of time 
        """


class Bomb(PowerUp):
    def __init__(self, width, height, image, initial_x, speed=0):
        super().__init__(width, height, image, speed)
        self.initial_x = initial_x
        self.rect.x = self.initial_x
        self.rect.y = random.randint(-1000, 0)

    def affect_player(self, player):
        pass

    def affect_traffic(self, traffic):
        pass

    def power_up_cicle(self, playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic):
        super().power_up_cicle(playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic)
        """
        Bomb: durante este período o user não precisa de desviar o carro porque este se conduz sozinho. 
        Para além disso deve fazer explodir todos os carros com os quais embate e o tempo deve passar mais rápido
        
        Bomb 2: If car touches in other cars, they explode
        """


class ExtraLife(PowerUp):
    def __init__(self, width, height, image, initial_x, speed=0):
        super().__init__(width, height, image, speed)
        self.initial_x = initial_x
        self.rect.x = self.initial_x
        self.rect.y = random.randint(-1000, 0)

    def affect_player(self, lives):
        lives.append(lives[0] + 1)
        lives.remove(lives[0])

    def affect_traffic(self, traffic):
        pass

    def power_up_cicle(self, playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic):
        # Power up falls
        self.moveDown(speed)
        # Heart collides
        """
        Complete
        """
        if pygame.sprite.collide_mask(playerCar, self) is not None:
            self.affect_player(lives)
            # Power up dispawns
            power_up_list.remove(self)
            # Power up relocates
            self.spawn(road_x, lane_width)

        # Heart isn't catch
        elif self.rect.y >= screen_height:
            # Power up dispawns
            power_up_list.remove(self)
            # Power up relocates
            self.spawn(road_x, lane_width)


class Magnet(PowerUp):
    def __init__(self, width, height, image, speed=0):
        super().__init__(width, height, image, speed)

    def affect_player(self, player):
        pass

    def affect_traffic(self, traffic):
        pass

    def power_up_cicle(self, playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic):
        super().power_up_cicle(playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic)
        """
        Magnet: attracts nearby power-ups and coins towards the player 
        """


class SizeChange(PowerUp):
    def __init__(self, width, height, image, speed=0):
        super().__init__(width, height, image, speed)

    def affect_player(self, player):
        pass

    def affect_traffic(self, traffic):
        pass

    def power_up_cicle(self, playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic):
        super().power_up_cicle(playerCar, road_x, lane_width, speed, power_up_list, screen_height, lives, traffic)
        """
        Size Change: Changes the player's size, making them smaller (good) or larger (bad) em random.
        """
