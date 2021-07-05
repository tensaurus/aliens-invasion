import pygame
"""Alien to be used in Alien Invasion"""

class Alien():
    """A class to define an alien of the alien fleet"""
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # Set initial position of alien as top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store alien's horizontal position in floating value
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update_horizontal_position(self):
        """Move the alien to the right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def update_vertical_position(self):
        self.rect.y += self.settings.fleet_drop_speed

    def is_at_edge(self):
        """Returns true if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.x <= 0