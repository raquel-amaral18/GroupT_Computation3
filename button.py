import pygame


class Button:
    """
    Button class for use in other parts of the game.

    ...
    Attributes
    ----------
        text : str
            the text displayed on the button
        x : int
            the x-coordinate of the button
        y : int
            the y-coordinate of the button
        width : int
            the width of the button
        height : int
            the height of the button
        font_size : int
            the font size of the text on the button
        text_color : tuple
            the color of the text (RGB)
        button_color : tuple
            the background color of the button (RGB)
        border_radius : int
            the radius of the button's corners for rounded edges

    Methods
    -------
        draw(screen):
            draws the button on the pygame screen
        is_clicked(position):
            returns True if the button is clicked, False otherwise

    """
    def __init__(self, text, x, y, width, height, font_size, text_color, button_color, border_radius):
        """
        Constructs all the necessary attributes for the Button object.
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

        Parameters
        ---------
            screen:
                the pygame screen where the button will be drawn.
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

        Parameters
        ----------
            position : tuple
                the x and y coordinates of the mouse click

        Returns
        -------
            bool:
                true if the button is clicked, False otherwise
        """
        # Check if the button is clicked
        return self.rect.collidepoint(position)
