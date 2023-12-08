import pygame
from abc import ABC, abstractmethod

import random

from game import *

from car import PlayerCar, IncomingCars
from messages import *


class PowerUp(ABC, pygame.sprite.Sprite):
    """
        A base class representing a power-up in the game.

        ...

        Attributes
        ----------
            icon_path : str
                the path to the image file for the power-up icon
            width : int
                the width of the power-up icon in pixels
            initial_x : int
                the initial x-coordinate of the power-up icon
            speed : int
                the speed of the power-up icon
            active : bool
                indicates whether the power-up is currently active
            powered_up : bool
                indicates whether the power-up has been activated
            message_font : pygame.font.Font
                the font used for displaying messages related to the power-up

        Methods
        -------
            __init__(self, icon_path, width, initial_x):
                constructs the attributes for the PowerUp object
            affect_player(self, player, screen, messages_group):
                abstract method to define the effect of the power-up on the player
            affect_traffic(self, traffic):
                abstract method to define the effect of the power-up on the traffic
            effect_over(self, player, traffic, screen):
                abstract method to define the effect of the power-up when it's over
            visual_effect(self, messages_group, player, text):
                abstract method to define the visual effect of the power-up
            moveDown(self, pixels):
                moves the power-up icon down on the screen
            reshape(self, road_x, lane_width):
                reshapes the power-up icon with a new position and speed
    """

    def __init__(self, icon_path, width, initial_x):
        super().__init__()
        original_icon = pygame.image.load(icon_path)
        aspect_ratio = original_icon.get_width() / original_icon.get_height()
        self.image = pygame.transform.scale(original_icon, (width, int(width / aspect_ratio)))
        self.rect = self.image.get_rect()

        self.width = width
        self.height = int(width / aspect_ratio)

        self.rect.x = initial_x

        self.speed = random.randint(4, 6)
        self.active = False
        self.powered_up = False

        self.message_font = pygame.font.SysFont('monospace', 30, bold=True)

    @abstractmethod
    def affect_player(self, player, screen, messages_group, enemy_player=None):
        pass

    @abstractmethod
    def affect_traffic(self, traffic, messages_group):
        pass

    @abstractmethod
    def effect_over(self, player, traffic, screen, enemy_player=None):
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


class Invincibility(PowerUp):  # Shield icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.duration = 4000
        self.start_time = 0
        self.active = False
        self.active_time = None

    def affect_player(self, player, screen, messages_group, enemy_player=None):
        player.invincible = True

    def affect_traffic(self, traffic, messages_group):
        pass

    def effect_over(self, player, traffic, screen, enemy_player=None):
        player.invincible = False

    def visual_effect(self, messages_group, player, text):
        pass


class SlowDown(PowerUp):  # Hourglass icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.duration = 3000
        self.active = False
        self.active_time = None
        self.powered_up = False
        self.message_color = (47, 151, 193)

    def affect_player(self, player, screen, messages_group, enemy_player=None):
        pass

    def affect_traffic(self, traffic, messages_group):
        for car in traffic:
            car.is_speed_reduced = True
            car.change_speed(random.randint(3, 5))
            self.visual_effect(messages_group, car, "Slow")

    def effect_over(self, player, traffic, screen, enemy_player=None):
        for car in traffic:
            car.is_speed_reduced = False
            car.change_speed(random.randint(3, 5))

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)


class RestoreLives(PowerUp):  # Heart icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.duration = 0
        self.active = False
        self.message_color = (249, 65, 68)

    def affect_player(self, player, screen, messages_group, enemy_player=None):
        player.lives += 1
        self.visual_effect(messages_group, player, "+1")
        # Since ExtraLife has no effect, this line doesn't allow it to enter the "Power up Timer" condition
        self.powered_up = False

    def affect_traffic(self, traffic, messages_group):
        # No effect on traffic
        pass

    def effect_over(self, player, traffic, screen, enemy_player=None):
        pass

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)


class JetBomb(PowerUp):  # Fire icon
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.active = False
        self.active_time = None
        self.duration = 4000

    def affect_player(self, player, screen, messages_group, enemy_player=None):
        player.jet_bomb = True

    def affect_traffic(self, traffic, messages_group):
        # No effect on traffic
        pass

    def effect_over(self, player, traffic, screen, enemy_player=None):
        player.jet_bomb = False

    def visual_effect(self, messages_group, player, text):
        pass


class SizeChange(PowerUp):
    """
        Size Change: Changes the player's size, making them smaller (good) or larger (bad) em random.
    """

    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.active = False
        self.active_time = None
        self.duration = 3000
        self.message_color = None

    def affect_player(self, player, screen, messages_group, enemy_player=None):
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
            player.size = 80
            player.height = int(80 / aspect_ratio)
            self.message_color = (249, 65, 68)
            self.visual_effect(messages_group, player, "Big")
        # Scale the image
        player.image = pygame.transform.scale(player.original_image, (player.size, player.height))
        # Updates the playerCar's mask, so that pygame.sprite.collide_mask can be done with the new size and not the original one
        player.mask = pygame.mask.from_surface(player.image)
        # Print image on screen
        screen.blit(player.image, player.rect)

    def affect_traffic(self, traffic, messages_group):
        pass

    def effect_over(self, player, traffic, screen, enemy_player=None):
        aspect_ratio = player.original_image.get_width() / player.original_image.get_height()
        # Restore car back to original size
        player.width = 60
        player.height = int(player.width / aspect_ratio)

        player.image = pygame.transform.scale(player.original_image, (player.width, player.height))
        player.mask = pygame.mask.from_surface(player.image)
        screen.blit(player.image, player.rect)

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)


"""
    Negative Powerups for multiplayer
"""


class Invisible(PowerUp):
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.active = False
        self.active_time = None
        self.duration = 2000
        self.message_color = (239, 230, 221)

    def affect_player(self, player, screen, messages_group, enemy_player=None):
        enemy_player.visible = False
        self.visual_effect(messages_group, enemy_player, "Invisible")

    def affect_traffic(self, traffic, messages_group):
        # No effect on traffic
        pass

    def effect_over(self, player, traffic, screen, enemy_player=None):
        enemy_player.visible = True

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)


class NoPowerUp(PowerUp):
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.active = False
        self.active_time = None
        self.duration = 4000
        self.message_color = (249, 65, 68)

    def affect_player(self, player, screen, messages_group, enemy_player=None):
        enemy_player.can_catch_powerup = False
        self.visual_effect(messages_group, enemy_player, "Blocked")

    def affect_traffic(self, traffic, messages_group):
        # No effect on traffic
        pass

    def effect_over(self, player, traffic, screen, enemy_player=None):
        enemy_player.can_catch_powerup = True

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)


class KeyInversion(PowerUp):
    def __init__(self, icon_path, width, initial_x):
        super().__init__(icon_path, width, initial_x)
        self.rect.y = random.randint(-2000, -1000)
        self.active = False
        self.active_time = None
        self.duration = 3000
        self.message_color = (225, 188, 41)

    def affect_player(self, player, screen, messages_group, enemy_player=None):
        enemy_player.key_inverse = True
        self.visual_effect(messages_group, enemy_player, "Inverse")

    def affect_traffic(self, traffic, messages_group):
        # No effect on traffic
        pass

    def effect_over(self, player, traffic, screen, enemy_player=None):
        enemy_player.key_inverse = False

    def visual_effect(self, messages_group, player, text):
        show_message(messages_group, text, self.message_font, (player.rect.x, player.rect.y), self.message_color)
