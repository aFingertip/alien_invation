class Settings():
    """Storage all setting classes in Alien_Invasion"""

    def __init__(self):
        """initialization the settings of game"""
        #setting of screen
        self.screen_width = 1200
        self.screen_height = 650
        self.bg_color = (230,230,230)

        #setting of ship
        self.ship_speed_factor = 1.5
        self.ships_limit = 3

        #setting of bullet
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        #setting of aliens
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 30
        #if fleet_direction = 1 : aliens move right
        #if fleet_direction = -1: aliens move left
        self.fleet_direction = 1

        #turn up game speed in which way
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initalize_settings which change with changes in the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction =1
        self.alien_points = 50

    def increase_speed(self):
        """settings about increase speed"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)