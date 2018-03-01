class GameStats():
    '''track statistics for alien invasion'''

    def __init__(self, ai_settings):
        '''initialize settings'''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.high_score = 0

        #start alien invasion in a game active state
        self.game_active = False
        
        #start alien invasion un-paused
        self.pause_game = False
        
    def reset_stats(self):
        '''initialize statistics that can change during the game'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
