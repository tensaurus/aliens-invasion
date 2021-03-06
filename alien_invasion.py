import os
import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

# When a bundled app starts up, the bootloader sets the sys.frozen attribute and 
# stores the absolute path to the bundle folder in sys._MEIPASS. For a one-folder bundle,
# this is the path to that folder. For a one-file bundle, this is the path to the temporary 
# folder created by the bootloader
# https://pyinstaller.readthedocs.io/en/stable/runtime-information.html?highlight=hasattr#run-time-information
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

class AlienInvasion:
    """Manage game assets and behavior."""

    def __init__(self):
        """Initialize game and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                                self.settings.screen_height))
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.ships = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        
        self._create_ship_fleet()
        self._create_alien_fleet()
        
    def run_game(self):
        """Starts the main loop for the game"""
        running = True
        while running:
            running = self._check_events()
            if self.stats.game_is_active:
                self.ship_on_frontline.update_position()
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
            return True
        else:
            return True

    def _check_play_button(self, mouse_pos):
        """Start a new game when play button is clicked"""
        if (self.play_button.rect.collidepoint(mouse_pos) and
                not self.stats.game_is_active):
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.stats.game_is_active = True
            if not self.ships.sprites():
                self._create_ship_fleet()
            self._reset_scene()
            pygame.mouse.set_visible(False) 

    def _check_keydown_events(self, event):
        """Handle all keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship_on_frontline.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship_on_frontline.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Handle all keyup events"""
        if event.key == pygame.K_RIGHT:
            self.ship_on_frontline.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship_on_frontline.moving_left = False

    def _update_screen(self):
        """Makes new screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ships.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()
        # Draw the play button when game is inactive
        if not self.stats.game_is_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        # Create a bullet and to the bullets list
        if (self.stats.game_is_active and 
            len(self.bullets) < self.settings.numer_of_bullets_allowed):
            self.bullets.add(Bullet(self))

    def _update_bullets(self):
        """Manage bullets: remove old and update remaining bullets"""
        for bullet in self.bullets.copy():
            # Remove bullets from the list which crosses the screen
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Update bullets positions
        self.bullets.update()
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for bullets that have hit aliens
        #  If so, get rid of the bullet and the alien hit
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += len(aliens) * self.settings.alien_point
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        # Create new fleet if all aliens are dead
        if not self.aliens:
            self.bullets.empty() # Destroy existing bullets
            self._create_alien_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

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
        if pygame.sprite.spritecollideany(self.ship_on_frontline, self.aliens):
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
        ship_height = self.ship_on_frontline.rect.height
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
        self.settings.fleet_direction = 1 # Reset fleet direction

    def _ship_hit(self):
        """Responds ship being hit by an alien"""
        self.ships.remove(self.ship_on_frontline)
        if self.ships:
            self.ship_on_frontline = self.ships.sprites()[-1]
            self._reset_scene()
            sleep(1.0)
        else:
            self.stats.game_is_active = False
            pygame.mouse.set_visible(True)

    def _create_ship_fleet(self):
        """Start with the fleet with number of ships as ship_limit"""
        for ship_number in range(self.settings.ship_limit):
            ship = Ship(self)
            ship.rect.x = ship_number * (ship.rect.width + 10)
            ship.rect.y = 0
            self.ships.add(ship)
        self.ship_on_frontline = self.ships.sprites()[-1]

    def _reset_scene(self):
        """Remove remaining aliens and bullets on the screen.
        Create new alien fleet and center the ship"""
        self.aliens.empty()        # Delete existing aliens
        self.bullets.empty()       # Delete existing bullets
        self._create_alien_fleet() # Create new aliens fleet
        self.ship_on_frontline.center_ship()    # Center ship on frontline position
    
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