"""Defines a settings class for settings of alien_invasion.py"""

class Settings:
    
    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = 600
        self.screen_height = 400
        self.bg_color = (230, 230, 230)

        # Settings for Ship
        self.ship_speed = 0.1

        #settings for bullets
        self.bullet_speed = 0.8
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)