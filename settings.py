class Settings:
    # A class to store all settings for Alien Invasion
    def __init__(self):
        # Initialize the game's settings
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (42, 82, 190)
        self.ship_speed = 10
        
        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 10
        self.bullet_height = 25
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5