class Settings:
    # A class to store all settings for Alien Invasion
    def __init__(self):
        # Initialize the game's settings
        # Screen settings
        self.screen_width: int = 1200
        self.screen_height: int = 800
        self.bg_color: tuple[int, int, int] = (42, 82, 190)
        self.ship_speed: int = 10
        
        # Bullet settings
        self.bullet_speed: float = 2.5
        self.ship_limit: int = 3
        self.bullet_width: int = 10
        self.bullet_height: int = 25
        self.bullet_color: tuple[int, int, int] = (60, 60, 60)
        self.bullets_allowed: int = 3

        # Alien settings
        self.alien_speed: float = 5.0
        self.fleet_drop_speed: int = 100
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction: int = 1