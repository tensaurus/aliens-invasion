import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

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
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_alien_fleet()

    def run_game(self):
        """Starts the main loop for the game"""
        running = True
        while running:
            running = self._check_events()
            self.ship.update_position()
            self._update_bullets()
            self._update_aliens()
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
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _fire_bullet(self):
        # Create a bullet and to the bullets list
        if len(self.bullets) < self.settings.numer_of_bullets_allowed:
            self.bullets.add(Bullet(self))

    def _update_bullets(self):
        """Manage bullets: remove old and update remaining bullets"""
        for bullet in self.bullets.copy():
            # Remove bullets from the list which crosses the screen
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Update bullets positions
        self.bullets.update()
        # Check for bullets that have hit aliens
        #  If so, get rid of the bullet and the alien hit
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, False, True)
        # Create new fleet if all aliens are dead
        if not self.aliens:
            self.bullets.empty() # Destroy existing bullets
            self._create_alien_fleet()

    def _update_aliens(self):
        """Check if fleet is at the edge, change direction and
        then update the position of all aliens in the fleet"""
        if self._is_fleet_at_edge():
            # Change fleet direction
            self.settings.fleet_direction *= -1
            # Drop fleet by one step
            for alien in self.aliens.sprites():
                alien.update_vertical_position()
        self.aliens.update() # Move aliens horizontally
        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._on_aliens_reach_bottom()

    def _is_fleet_at_edge(self):
        """Returns true if fleet reaches any edge of the screen"""
        for alien in self.aliens:
            if alien.is_at_edge():
                return True
    
    def _create_alien_fleet(self):
        """Create all the aliens in the fleet"""
        # Make one alien for width calculation
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height
        available_horizontal_space = self.settings.screen_width - (2 * alien_width)
        available_vertical_space = (self.settings.screen_height - 
                                        (3 * alien_height) - ship_height)
        number_of_aliens_per_row = available_horizontal_space // (2 * alien_width)
        number_of_rows = available_vertical_space // (2 * alien_height)
        # Make alien fleet
        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens_per_row):
                alien = Alien(self)
                alien.x = alien_width + (2 * alien_width) * alien_number
                alien.rect.x = alien.x
                alien.rect.y = alien_height + (2 * alien_height) * row_number
                self.aliens.add(alien)

    def _ship_hit(self):
        """Responds ship being hit by an alien"""
        self.stats.ships_left -= 1 # Decrement ships left by one
        self.aliens.empty()        # Delete existing aliens
        self.bullets.empty()       # Delete existing bullets
        self._create_alien_fleet() # Create new aliens fleet
        self.ship.center_ship()    # Center ship position

        sleep(1.0)                 # Pause

    def _on_aliens_reach_bottom(self):
        """When aliens reach bottom of the screen,
        treat same as shit is hit by an alien"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

pygame.quit()