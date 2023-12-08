import pygame
from abc import ABC, abstractmethod

import random

# COLORS:
WHITE = (255, 255, 255)


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
            moveDown(self, *args, **kwargs):
                moves the car down on the screen
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
        self.rect.center = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)

    @abstractmethod
    def moveDown(self, *args, **kwargs):
        """
            Moves the car down on the screen.

            Parameters
            ----------
            *args, **kwargs:
                Variable-length arguments and keyword arguments that allow flexibility for different
                implementations in child classes
        """
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
            speed: int
                the speed of the player's car
            lives: int
                the number of lives the player has
            ghost: bool
                indicates if the player's car is in a ghost state after a collision
            visible: bool
                indicates if the player's car is visible
            powered_up: bool
                indicates if the player's car is currently powered up
            invincible: bool
                indicates if the player's car is invincible
            pac_man: bool
                indicates if the player's car is in Pac-Man mode
            can_catch_powerup: bool
                indicates if player is affected by NoPowerUp powerup

        Methods
        -------
            __init__(self, image_path, width, speed=0):
                constructs the attributes for the PlayerCar object
            moveRight(self, pixels):
                moves the player's car the specified number of pixels to the right
            moveLeft(self, pixels):
                moves the player's car the specified number of pixels to the left
            moveUp(self, pixels):
                moves the player's car the specified number of pixels up
            moveDown(self, pixels):
                moves the player's car the specified number of pixels down
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
        self.speed = 3
        self.lives = 3

        self.ghost = False
        self.visible = True

        self.powered_up = False
        self.invincible = False
        self.pac_man = False
        self.jet_bomb = False
        self.mask_surface = self.mask.to_surface(setcolor=(255, 255, 255, 100), unsetcolor=(0, 0, 0, 0))  # unset, to transparent background
        self.nopowerup_mask = self.mask.to_surface(setcolor=(249, 65, 68, 100), unsetcolor=(0, 0, 0, 0))
        self.key_inverse_mask = self.mask.to_surface(setcolor=(225, 188, 41, 100), unsetcolor=(0, 0, 0, 0))
        self.can_catch_powerup = True
        self.key_inverse = False
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
        """
            Moves the player's car up by the specified number of pixels.

            Parameters
            ----------
                pixels: int
                    the number of pixels to move the player's car up
        """
        self.rect.y -= pixels

    def moveDown(self, pixels):
        """
            Moves the player's car down by the specified number of pixels.

            Parameters
            ----------
                pixels: int
                    the number of pixels to move the player's car down
        """
        self.rect.y += pixels

    def change_speed(self, speed):
        """
            Changes the speed of the object.

            Parameters
            ----------
                speed: int
                    the new speed of the object
        """
        pass


class IncomingCars(Car):
    """
        A class representing incoming cars in the game.

        Attributes
        ----------
            initial_x: int
                the initial x-coordinate of the incoming car
            is_speed_reduced: bool
                indicates if the speed of the incoming car is currently reduced (due to a powerUp)


        Methods
        -------
            __init__(self, image_path, width, speed, initial_x):
                constructs the attributes for the IncomingCar object.
            moveDown(self, playerCar_speed):
                moves the incoming car downward based on the player's car speed
            reshape(self):
                reshapes the incoming car with a random image, initial position and speed
            change_speed(self, speed):
                overrides the base class method to change the speed of the incoming car
    """

    def __init__(self, image_path, width, speed, initial_x):
        """
            Constructs the attributes for the IncomingCar object.

            Parameters
            ----------
                image_path: str
                    the path to the image file for the incoming car
                width: int
                    the width of the incoming car in pixels
                speed: int
                    the initial speed of the incoming car
                initial_x: int
                    the initial x-coordinate of the incoming car
        """
        super().__init__(image_path, width, speed)
        self.initial_x = initial_x
        self.rect.x = self.initial_x
        self.rect.y = random.randint(-1000, 0)
        self.is_speed_reduced = False
        self.slowing_mask = None

    def moveDown(self, playerCar_speed):
        """
            Moves the incoming car downward based on the player's car speed, since the apparent velocity of the
            incoming cars is their velocity + the velocity of the player.

            Parameters
            ----------
                playerCar_speed: int
                    the speed of the player's car
        """
        pixels = self.speed + playerCar_speed
        self.rect.y += pixels

    def reshape(self):
        """
            Reshapes the incoming car with a random image, initial position, and speed.
        """

        vehicle_images = {
            "motorcycles": ["Images/Vehicles/IncomingCars/00M.png", "Images/Vehicles/IncomingCars/01M.png",
                            "Images/Vehicles/IncomingCars/02M.png"],
            "cars": ["Images/Vehicles/IncomingCars/01C.png", "Images/Vehicles/IncomingCars/02C.png",
                     "Images/Vehicles/IncomingCars/03C.png", "Images/Vehicles/IncomingCars/04C.png",
                     "Images/Vehicles/IncomingCars/05C.png", "Images/Vehicles/IncomingCars/06C.png",
                     "Images/Vehicles/IncomingCars/07C.png", "Images/Vehicles/IncomingCars/08C.png",
                     "Images/Vehicles/IncomingCars/09C.png"],
            "trucks": ["Images/Vehicles/IncomingCars/00T.png", "Images/Vehicles/IncomingCars/01T.png",
                       "Images/Vehicles/IncomingCars/02T.png", "Images/Vehicles/IncomingCars/03T.png",
                       "Images/Vehicles/IncomingCars/04T.png", "Images/Vehicles/IncomingCars/05T.png"],
        }

        chosen_type = random.choice(list(vehicle_images.keys()))
        images = vehicle_images[chosen_type]  # returns a list of image paths within the chosen type
        chosen_image_path = random.choice(images)

        target_width = 0
        if chosen_type == "motorcycles":
            target_width = 50
        elif chosen_type == "cars":
            target_width = 60
        elif chosen_type == "trucks":
            target_width = 70

        original_image = pygame.image.load(chosen_image_path)
        aspect_ratio = original_image.get_width() / original_image.get_height()
        scaled_height = int(target_width / aspect_ratio)

        self.image = pygame.transform.scale(original_image, (target_width, scaled_height))
        self.mask = pygame.mask.from_surface(self.image)
        self.slowing_mask = self.mask.to_surface(setcolor=(47, 151, 193, 100), unsetcolor=(0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.width = target_width
        self.height = scaled_height

        self.rect.x = self.initial_x
        self.rect.y = random.randint(-2000, -1000)
        self.change_speed(random.randint(3, 5))

    def change_speed(self, speed):
        """
            Overrides the base class method to change the speed of the incoming cars.

            Parameters
            ----------
                speed: int
                    the new speed of the incoming car
        """
        super().change_speed(speed)
        if not self.is_speed_reduced:
            self.speed = speed
        else:
            self.speed /= 4
