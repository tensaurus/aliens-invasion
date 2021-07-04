import sys
import copy

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Manage game assets and behavior."""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = []

    def run_game(self):
        """Starts the main loop for the game"""
        running = True
        while running:
            running = self._check_events()
            self.ship.update_position()
            
            for bullet in copy.copy(self.bullets):
                # Remove bullets from the list which crosses the screen
                if bullet.rect.y <= 0:
                    self.bullets.remove(bullet)
                else:
                    bullet.update_position()
            
            self._update_screen()
            
    def _check_events(self):
        """Return whether the loop running it should continue
        returns False to stop the loop else return False"""
        events_list = pygame.event.get()
        if events_list:
            for event in events_list:
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
            return True
        else:
            return True

    def _check_keydown_events(self, event):
        """Handle all keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Handle all keyup events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Makes new screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets:
            bullet.draw_bullet()
        pygame.display.flip()

    def _fire_bullet(self):
        # Create a bullet and to the bullets list
        if len(self.bullets) < self.settings.numer_of_bullets_allowed:
            self.bullets.append(Bullet(self))

    def _update_bullets(self):
        """"""
        pass


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

pygame.quit()