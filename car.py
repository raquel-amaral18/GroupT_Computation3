import pygame
from abc import ABC, abstractmethod

import random


# COLORS:
WHITE = (255, 255, 255)


# everything that needs to move has to be a child class of this class pygame.sprite.Sprite
class Car(pygame.sprite.Sprite, ABC):
    def __init__(self, image_path, width, speed):
        super().__init__()
        original_image = pygame.image.load(image_path)
        aspect_ratio = original_image.get_width() / original_image.get_height()
        self.image = pygame.transform.scale(original_image, (width, int(width / aspect_ratio)))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = int(width / aspect_ratio)
        self.speed = speed

    @abstractmethod
    def change_speed(self, speed):
        pass


class PlayerCar(Car):
    def __init__(self, image_path, width, speed=0):
        super().__init__(image_path, width, speed)
        self.invincible = False
        self.visible = True
        self.speed = 2

    # The position of the car is (self.rect.x, self.rect.y)
    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels

    def change_speed(self, speed):
        pass


class IncomingCars(Car):
    def __init__(self, image_path, width, speed, initial_x):
        super().__init__(image_path, width, speed)
        self.initial_x = initial_x
        self.rect.x = self.initial_x
        self.rect.y = random.randint(-1000, 0)

    def moveDown(self, playerCar_speed):
        # If we change the "player's car speed" the apparent velocity of the incoming
        # cars is their velocity + the velocity of the player
        pixels = self.speed + playerCar_speed
        self.rect.y += pixels

    def reshape(self):
        # Manually update the image paths available for each vehicle type
        vehicle_images = {
            "motorcycles": ["Images/00M.png", "Images/01M.png"],
            "cars": ["Images/01C.png", "Images/02C.png", "Images/03C.png", "Images/04C.png",
                     "Images/05C.png", "Images/06C.png", "Images/07C.png"],
            "trucks": ["Images/00T.png", "Images/01T.png"],
        }

        chosen_type = random.choice(list(vehicle_images.keys()))
        images = vehicle_images[chosen_type]  # returns a list of image paths within the chosen type
        chosen_image_path = random.choice(images)

        target_width = 0
        if chosen_type == "motorcycles":
            target_width = 41
        elif chosen_type == "cars":
            target_width = 50
        elif chosen_type == "trucks":
            target_width = 60

        original_image = pygame.image.load(chosen_image_path)
        aspect_ratio = original_image.get_width() / original_image.get_height()
        scaled_height = int(target_width / aspect_ratio)

        self.image = pygame.transform.scale(original_image, (target_width, scaled_height))
        self.rect = self.image.get_rect()
        self.width = target_width
        self.height = scaled_height

        self.rect.x = self.initial_x
        self.rect.y = random.randint(-2000, 0)
        self.change_speed(random.randint(3, 5))


    def change_speed(self, speed):
        super().change_speed(speed)
        self.speed = speed
