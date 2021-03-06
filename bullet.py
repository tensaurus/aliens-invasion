import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet at the present position of the ship"""
        super().__init__()
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.screen = ai_game.screen

        # Create a bullet rect at (0, 0) and then change position according to ship
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship_on_frontline.rect.midtop

        # Store bullet's y position as decimal
        self.y = float(self.rect.y)

    def update(self):
        """Move bullet up on the screen"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draws bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)