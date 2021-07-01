import pygame
from settings import Settings
from ship import Ship
class AlienInvasion:
    """Manage game assets and behavior."""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)

    def run_game(self):
        """Starts the main loop for the game"""
        running = True
        while running:
            running = self._check_events()
            self.ship.update_position()
            self._update_screen()
            
    def _check_events(self):
        """Return whether the loop running it should continue
        returns False to stop the loop else return False"""
        events_list = pygame.event.get()
        if events_list == []:
            return True
        for event in events_list:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
        return True

    def _update_screen(self):
        """Makes new screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

pygame.quit()