import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, width, x, y):
        super().__init__()
        original_image = pygame.image.load(image_path)
        aspect_ratio = original_image.get_width() / original_image.get_height()
        self.image = pygame.transform.scale(original_image, (width, int(width / aspect_ratio)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 5

    def moveDown(self):
        self.rect.y += self.speed
