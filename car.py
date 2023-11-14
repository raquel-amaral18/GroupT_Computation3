import pygame
from abc import ABC, abstractmethod

# COLORS:
WHITE = (255, 255, 255)


# everything that needs to move has to be a child class of this class pygame.sprite.Sprite
class Car(pygame.sprite.Sprite, ABC):
    def __init__(self, color, width, height, speed):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.width = width
        self.height = height
        self.color = color

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        self.speed = speed

    @abstractmethod
    def moveDown(self, *args, **kwargs):
        pass

    @abstractmethod
    def repaint(self, color):
        pass

    @abstractmethod
    def reshape(self, width, height):
        pass

    @abstractmethod
    def change_speed(self, speed):
        pass


class PlayerCar(Car):
    def __init__(self, color, width, height, speed=0, lives=3):
        super().__init__(color, width, height, speed)
        self.invincible = False
        self.visible = True

    # The position of the car is (self.rect.x, self.rect.y)
    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels

    def repaint(self, color):
        super().repaint(color)
        self.color = color
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

    def reshape(self, width, height):
        pass

    def change_speed(self, speed):
        pass


class IncomingCars(Car):
    def __init__(self, color, width, height, speed):
        super().__init__(color, width, height, speed)

    def moveDown(self, playerCar_speed):
        # If we change the "player's car speed" the apparent velocity of the incoming
        # cars is their velocity + the velocity of the player
        pixels = self.speed + playerCar_speed
        self.rect.y += pixels

    def repaint(self, color):
        super().repaint(color)
        self.color = color
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

    def reshape(self, width, height):
        super().reshape(width, height)
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.width = width
        self.height = height
        pygame.draw.rect(self.image, self.color, [0, 0, width, height])

    def change_speed(self, speed):
        super().change_speed(speed)
        self.speed = speed
