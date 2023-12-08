import pygame


class Button:
    """
    Button class for use in other parts of the game.


    Attributes:
        text (str): The text displayed on the button
        x (int): The x-coordinate of the button
        y (int): The y-coordinate of the button
        width (int): The width of the button
        height (int): The height of the button
        font_size (int): The font size of the text on the button
        text_color (tuple): The color of the text
        button_color (tuple): The background color of the button
        border_radius (int): The radius of the button's corners for rounded edges

    Methods:
        draw(screen): Draws the button on the pygame screen
        is_clicked(position): Returns True if the button is clicked, False if not.

    """
    def __init__(self, text, x, y, width, height, font_size, text_color, button_color, border_radius):
        """
        Initializes the attributes of the Button class.
        """
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color
        self.border_radius = border_radius

        self.font = pygame.font.Font("Fonts/TT_Rounds_Neue_Compres_Bold.ttf", self.font_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        Draws the button on the specified pygame screen.

        Parameters:
            screen: The pygame screen where the button will be drawn.
        """
        # Draw the button
        pygame.draw.rect(screen, self.button_color, self.rect, self.width, self.border_radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        # Center the text on the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, position):
        """
        Checks if the button is clicked based on the mouse position.

        Parameters:
            position (tuple): The x and y coordinates of the mouse click.

        Returns:
            bool: True if the button is clicked, False if not.
        """
        # Check if the button is clicked
        return self.rect.collidepoint(position)
