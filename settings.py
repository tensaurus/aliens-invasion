"""Defines a settings class for settings of alien_invasion.py"""

class Settings:
    
    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = 600
        self.screen_height = 400
        self.bg_color = (230, 230, 230)

        # Settings for Ship
        self.ship_speed = 0.5
        self.ship_limit = 3 # Max number of ships given to a player

        #settings for bullets
        self.bullet_speed = 0.5
        self.bullet_width = 300
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.numer_of_bullets_allowed = 5

        # Settings for aliens
        self.alien_speed = 0.5
        self.fleet_drop_speed = 50.0
        # fleet_direction of 1 for moving right and -1 for left
        self.fleet_direction = 1