import pygame


class Message(pygame.sprite.Sprite):
    def __init__(self, text, font, position, color):
        super().__init__()
        self.font = font
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(topleft=position)
        self.alpha = 255  # transparency of the message, initialized to 255 (fully opaque)

    def update(self):
        self.rect.y -= 2  # Move the message upward
        self.alpha -= 5  # Increase the transparency
        if self.alpha <= 0:
            self.kill()  # Remove the message from the screen when it becomes fully transparent


def show_message(messages_group, text, font, position, color, font_size=30):
    message_font = pygame.font.SysFont('monospace', font_size, bold=True)
    message = Message(text, font, position, color)
    messages_group.add(message)
