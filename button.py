import pygame
class Button:
    def __init__(self, text, x, y, width, height, font_size=20, text_color=(255, 255, 255), button_color=(0, 0, 255)):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color

        self.font = pygame.font.SysFont('monospace', self.font_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # Draw the button
        pygame.draw.rect(screen, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        # Center the text on the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, position):
        # Check if the button is clicked
        return self.rect.collidepoint(position)