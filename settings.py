"""Defines a settings class for settings of alien_invasion.py"""

class Settings:
    
    def __init__(self):
        """Initialize game static settings"""
        # Screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.font = 'arial'
        self.font_size = 48

        # Settings for Ship
        self.ship_limit = 1 # Max number of ships given to a player

        #settings for bullets
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.numer_of_bullets_allowed = 5

        # Settings for aliens
        self.fleet_drop_speed = 10.0

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change during the game"""
        self.ship_speed = 0.5
        self.bullet_speed = 1.0
        self.alien_speed = 0.3
        self.alien_point = 10

        # fleet_direction of 1 for moving right and -1 for left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed of the ship, bullets and aliens,
        aliens points"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_point *= self.score_scale