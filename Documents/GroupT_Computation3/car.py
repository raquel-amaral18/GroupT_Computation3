import pygame
from abc import ABC, abstractmethod

import random
import math

# COLORS:
WHITE = (255, 255, 255)

screen_width = 700
screen_height = 600


# everything that needs to move has to be a child class of this class pygame.sprite.Sprite
class Car(pygame.sprite.Sprite, ABC):
    """
        A class representing a car in the game.

        ...
        Attributes
        ----------
            image_path : str
                the path to the image file for the object
            width : int
                the width of the object in pixels
            speed : int
                the initial speed of the object

        Methods
        -------
            __init__(self, image_path, width, speed):
                constructs the attributes for the Car object
            change_speed(self, speed):
                changes the speed of the object
        """

    def __init__(self, image_path, width, speed):
        """
            Constructs all the necessary attributes for the Car object.

            Parameters
            ----------
               image_path : str
                   the path to the image file for the object
               width : int
                   the width of the object in pixels
               speed : int
                   the initial speed of the object
        """
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        aspect_ratio = self.original_image.get_width() / self.original_image.get_height()
        self.image = pygame.transform.scale(self.original_image, (width, int(width / aspect_ratio)))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = int(width / aspect_ratio)
        self.speed = speed

    @abstractmethod
    def moveDown(self, *args, **kwargs):
        pass

    @abstractmethod
    def change_speed(self, speed):
        """
            Changes the speed of the object.

            Parameters
            ----------
                speed: int
                    the new speed of the object
        """
        pass


class PlayerCar(Car):
    """
        A class representing the player's car in the game.

        Attributes
        ----------
            invincible: bool
                indicates if the player's car is invincible
            visible: bool
                indicates if the player's car is visible
            speed: int
                the initial speed of the player's car

        Methods
        -------
            __init__(self, image_path, width, speed=0):
                constructs the attributes for the PlayerCar object
            moveRight(self, pixels):
                moves the player's car the specified number of pixels to the right
            moveLeft(self, pixels):
                moves the player's car the specified number of pixels to the left
            change_speed(self, speed):
                overrides the base class method to change the speed of the player's car
    """

    def __init__(self, image_path, width, speed=0):
        """
            Constructs the attributes for the PlayerCar object.

            Parameters
            ----------
                image_path: str
                    the path to the image file for the player's car
                width: int
                    the width of the player's car in pixels
                speed: int
                    the initial speed of the player's car
        """
        super().__init__(image_path, width, speed)
        self.ghost = False
        self.visible = True
        self.invincible = False
        self.powered_up = False
        self.speed = 3
        self.size = width
        self.lives = 3
        self.pac_man = False

    # The position of the car is (self.rect.x, self.rect.y)
    def moveRight(self, pixels):
        """
            Moves the player's car to the right by the specified number of pixels.

            Parameters
            ----------
                pixels: int
                    the number of pixels to move the player's car to the right
        """
        self.rect.x += pixels

    def moveLeft(self, pixels):
        """
            Moves the player's car to the left by the specified number of pixels.

            Parameters
            ----------
                pixels: int
                    the number of pixels to move the player's car to the left
        """
        self.rect.x -= pixels

    def moveUp(self, pixels):
        self.rect.y -= pixels

    def moveDown(self, pixels):
        self.rect.y += pixels

    def change_speed(self, speed):
        pass


class IncomingCars(Car):
    """
        A class representing incoming cars in the game.

        Attributes
        ----------
            initial_x: int
                the initial x-coordinate of the incoming car

        Methods
        -------
            __init__(self, image_path, width, speed, initial_x):
                constructs the attributes for the IncomingCar object.
            moveDown(self, playerCar_speed):
                moves the incoming car downward based on the player's car speed
            reshape(self):
                reshapes the incoming car with a random image and initial position
            change_speed(self, speed):
                overrides the base class method to change the speed of the incoming car
    """

    def __init__(self, image_path, width, speed, initial_x):
        super().__init__(image_path, width, speed)
        self.initial_x = initial_x
        self.rect.x = self.initial_x
        self.rect.y = random.randint(-1000, 0)
        self.is_speed_reduced = False

    def moveDown(self, playerCar_speed):
        # If we change the "player's car speed" the apparent velocity of the incoming
        # cars is their velocity + the velocity of the player
        pixels = self.speed + playerCar_speed
        self.rect.y += pixels

    def reshape(self):
        # Manually update the image paths available for each vehicle type

        vehicle_images = {
            "motorcycles": ["Images/00M.png", "Images/01M.png", "Images/02M.png"],
            "cars": ["Images/02C.png", "Images/03C.png", "Images/04C.png",
                     "Images/05C.png", "Images/07C.png", "Images/08C.png", "Images/09C.png", "Images/10C.png"],
            "trucks": ["Images/00T.png", "Images/01T.png", "Images/02T.png", "Images/03T.png", "Images/04T.png",
                       "Images/05T.png"],
        }

        chosen_type = random.choice(list(vehicle_images.keys()))
        images = vehicle_images[chosen_type]  # returns a list of image paths within the chosen type
        chosen_image_path = random.choice(images)

        target_width = 0
        if chosen_type == "motorcycles":
            target_width = 40
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
        self.rect.y = random.randint(-2000, -100)
        self.change_speed(random.randint(3, 5))

    def change_speed(self, speed):
        super().change_speed(speed)
        if not self.is_speed_reduced:
            self.speed = speed
        else:
            self.speed /= 4
