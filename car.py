import random

import pygame

# COLORS:
WHITE = (255, 255, 255)


# everything that needs to move has to be a child class of this class pygame.sprite.Sprite
class Car(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed=0):
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

    # The position of the car is (self.rect.x, self.rect.y)
    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft (self, pixels):
        self.rect.x -= pixels

    def moveUp (self, pixels):
        self.rect.y -= pixels

    def moveDown (self, playerCar_speed):
        # If we change the "player's car speed" the apparent velocity of the incoming
        # cars is their velocity + the velocity of the player
        pixels = self.speed + playerCar_speed
        self.rect.y += pixels

    def repaint(self, color):
        self.color = color
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

    def reshape(self, width, height):
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.width = width
        self.height = height
        pygame.draw.rect(self.image, self.color, [0, 0, width, height])

    def change_speed(self, speed):
        self.speed = speed

