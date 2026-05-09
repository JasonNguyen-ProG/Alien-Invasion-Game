import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:
    # Overall class to manage game assets and behavior

    def __init__(self):
        # Initialize game and create game resources
        pygame.init()
        
        self.settings = Settings()

        # Set display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)    # Set game in full screen mode
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics
        self.stats= GameStats(self)
        # and create a scoreboard
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Create clock to help control Frame Rate
        self.clock = pygame.time.Clock()

        # Start Alien Invasion in an active state
        self.game_active = False

        # Make the Play Button
        self.play_button = Button(self, "Play")


    def run_game(self) -> None:
        # Main game loop
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)     # Makes sure loop runs exactly 60 times/sec


    def _check_events(self) -> None:
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)  
            # Handle left-right movement
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # If user no longer presses key, movement stops
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos)  -> None:
        # Start a new game when the player cliks Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event) -> None:
        # Respond to key presses
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()


    def _check_keyup_events(self, event) -> None:
        # Respond to key releases
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self) -> None:
        # Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self) -> None:
        # Update position of bullets and get rid of old bullets
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self) -> None:
        # Respond to bullet-alien collisions
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) # First bool can be False to make the bullet continue to the top of screen

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()


    def _create_fleet(self) -> None:
        # Create the fleet of aliens
        # Create an alien and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        # Slight condition change: the right edge of the screen has 7 alien's width worth of margin
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 7 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position) -> None:
        # Create an alien and place it in the row
        new_alien = Alien(self)
        new_alien.x= x_position
        new_alien.rect.x, new_alien.rect.y = x_position, y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self) -> None:
        # Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self) -> None:
        # Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1
            

    def _update_screen(self) -> None:
        # Redraw the screen during each pass through the loop
        # Update images on the screen, and flip to the new screen
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score info
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


    def _update_aliens(self) -> None:
        # Check if the fleet is at an edge, then update positions
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    
    def _ship_hit(self) -> None:
        if self.stats.ships_left > 0:
            # Respond to the ship being hit by an alien
            # Decrement ship_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self) -> None:
        # Check if any aliens have reached the bottom of the screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

# SUGGESTION: modify the aliens movement so each row moves opposite of each other
# TODO: add a message after every time an alien hits the ship
# TODO: use a space image for background

if __name__=='__main__':
    # Make game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()