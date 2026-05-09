class Settings:
    # A class to store all settings for Alien Invasion
    def __init__(self):
        # Initialize the game's settings
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (42, 82, 190)
        
        
        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 10
        self.bullet_height = 25
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 5.0
        self.fleet_drop_speed = 20
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Ship settings
        self.ship_speed = 10
        self.ship_limit = 3