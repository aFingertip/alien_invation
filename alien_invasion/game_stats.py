class GameStats():
    """Track game statistics"""

    def __init__(self,ai_settings):
        """initialization statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False

        #the hightest score which shoud not be reseted in any case
        self.high_score = 0

    def reset_stats(self):
        """reset variable statistics when game run """
        self.ships_left = self.ai_settings.ships_limit
        self.score = 0
        self.level = 1

