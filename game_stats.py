class GameStats:
    """A class to hold all the stats of the game"""
    def __init__(self, ai_game):
        """Initialize game statistics"""
        self.settings = ai_game.settings
        self.game_is_active = False
        self.high_score = 0 # High score should never be reset
        self.reset_stats()

    def reset_stats(self):
        """Initialize stats which can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0