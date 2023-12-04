import pygame
from abc import ABC, abstractmethod

import random

from game import *
from car import PlayerCar, IncomingCars
from messages import *


class PowerUp(ABC, pygame.sprite.Sprite):
    def __init__(self, icon_path, width, initial_x):
        super().__init__()
        original_icon = pygame.image.load(icon_path)
        aspect_ratio = original_icon.get_width() / original_icon.get_height()
        self.image = pygame.transform.scale(original_icon, (width, int(width / aspect_ratio)))
        self.rect = self.image.get_rect()

        self.width = width
        self.height = int(width / aspect_ratio)

        self.rect.x = initial_x

        self.speed = random.randint(4, 8)
        self.active = False
        self.powered_up = False
        self.impulse = False

        self.message_font = pygame.font.SysFont('monospace', 30, bold=True)

    @abstractmethod
    def affect_player(self, player, screen, messages_group):
        pass

    @abstractmethod
    def affect_traffic(self, traffic):
        pass

    @abstractmethod
    def effect_over(self, player, traffic, screen):
        pass

    @abstractmethod
    def visual_effect(self, messages_group, player, text):
        pass

    def moveDown(self, pixels):
        self.rect.y += pixels

    def reshape(self, road_x, lane_width):
        random_lane = random.randint(0, 3)
        edge_offset = 10

        # Power up deactivates
        self.active = False
        # Power up relocates horizontally in a random lane, either to the left, right or center
        self.rect.x = random.choice([
            road_x + (random_lane * lane_width) + edge_offset,
            road_x + (random_lane * lane_width) + (lane_width - self.rect.width) - edge_offset
        ])
        # Power up relocates vertically
        self.rect.y = random.randint(-1000, -100)
        # Power up changes speed
        self.speed = random.randint(4, 8)


"""
Invincibility Complete (falta efeito e som)
"""


class Invincibility(PowerUp):  # Shield icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.duration = 5000
        self.start_time = 0
        self.active = False
        self.active_time = None

    def affect_player(self, player, screen, messages_group):
        # Don't enter if that loses a life when collision
        player.ghost = True
        # Don't enter the if of the player.ghost timer
        player.invincible = True

    def affect_traffic(self, traffic):
        pass

    def effect_over(self, player, traffic, screen):
        player.ghost = False
        player.invincible = False

    def visual_effect(self, messages_group, player, text):
        pass


"""
Slowing Complete (falta efeito e som e message)

visual effect idea: put incoming cars with bluw tone for a second
"""


class SlowDown(PowerUp):  # Hourglass icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.duration = 3000
        self.start_time = 0
        self.active = False
        self.active_time = None
        self.cooldown = 0
        self.powered_up = False
        self.duration = 2000

    def affect_player(self, player, screen, messages_group):
        pass

    def affect_traffic(self, traffic):
        for car in traffic:
            car.is_speed_reduced = True
            car.change_speed(random.randint(3, 5))

    def effect_over(self, player, traffic, screen):
        for car in traffic:
            car.is_speed_reduced = False
            car.change_speed(random.randint(3, 5))

    def visual_effect(self, messages_group, player, text):
        pass


"""
Extra Life Complete (falta efeito e som)
"""


class RestoreLives(PowerUp):  # Heart icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.duration = 0
        self.start_time = 0
        self.active = False
        self.message_color = (249, 65, 68)

    def affect_player(self, player, screen, messages_group):
        player.lives += 1
        self.visual_effect(messages_group, player, "+1")

    def affect_traffic(self, traffic):
        # No effect on traffic
        pass

    def effect_over(self, player, traffic, screen):
        pass

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)


"""
Jet Bomb (meter musica de fundo do pac man com cereja enquanto powerup ativo)
"""


class JetBomb(PowerUp):  # Fire icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.active = False
        self.active_time = None
        self.duration = 2000

    def affect_player(self, player, screen, messages_group):
        player.pac_man = True

    def affect_traffic(self, traffic):
        # No effect on traffic
        pass

    def effect_over(self, player, traffic, screen):
        player.pac_man = False
        for car in traffic:
            car.visible = True


    def visual_effect(self, messages_group, player, text):
        pass


"""
Size Change Complete (falta efeito e som)
"""


class SizeChange(PowerUp):
    """
        Size Change: Changes the player's size, making them smaller (good) or larger (bad) em random.
    """

    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.duration = 5000
        self.start_time = 0
        self.active = False
        self.active_time = None
        self.duration = 3000
        self.message_color = None

    def affect_player(self, player, screen, messages_group):
        aspect_ratio = player.original_image.get_width() / player.original_image.get_height()
        new_size = random.randint(0, 1)
        # If car Small
        if new_size == 0:
            player.size = 20
            player.height = int(20 / aspect_ratio)
            self.message_color = (74, 173, 82)
            self.visual_effect(messages_group, player, "Small")
        # If car Big
        else:
            player.size = 100
            player.height = int(100 / aspect_ratio)
            self.message_color = (249, 65, 68)
            self.visual_effect(messages_group, player, "Big")
        # Scale the image
        player.image = pygame.transform.scale(player.original_image, (player.size, player.height))
        # Print image on screen
        screen.blit(player.image, player.rect)

    def affect_traffic(self, traffic):
        pass

    def effect_over(self, player, traffic, screen):
        aspect_ratio = player.original_image.get_width() / player.original_image.get_height()
        # Restore car back to original size
        player.width = 50
        player.height = int(player.width / aspect_ratio)

        player.image = pygame.transform.scale(player.original_image, (player.width, player.height))
        screen.blit(player.image, player.rect)

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)

