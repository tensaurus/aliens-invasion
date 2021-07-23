"""Module to have scoreboard related code"""

import pygame.font

class Scoreboard:
    """A class to tore scoring information of the game"""
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats

        # Font setting for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(self.settings.font, self.settings.font_size)

        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """Prepare score image and position it"""
        self.score_string = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(self.score_string, True,
                                                self.text_color, self.settings.bg_color)
        
        # Position score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Prepare high score image and position it"""
        self.high_score_string = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(self.high_score_string, True,
                                                self.text_color, self.settings.bg_color)
        
        # Position score at top middle of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def show_score(self):
        """Display scores on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def check_high_score(self):
        """Update high score if current score exceed previous high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()