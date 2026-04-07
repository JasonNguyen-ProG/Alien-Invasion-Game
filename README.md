# Alien-Invasion-Game
## General Gameplay Overview:
- Player controls 1 rocket ships at the bottom center of the screen
- Player can move left and right using arrow keys and shoot bullets using spacebar
- When game starts, an alien fleet moves across and down the screen and the player has to destroy them all
- If the player destroys all the aliens, a new fleet appears that moves faster than the previous fleet. If any alien hits the player’s ship or reaches the bottom of the screen, the player loses a ship. If the player loses three ships, the game ends.

### Phase 1 Development:
- Create alien_invasion file for main game loop
- Create settings file for storing information (game window, color, etc) about game
- Create ship file to manage ship
- Create bullet file to manage bullets fired from ship 
- Implement moving left and right function using arrow keys and shooting function using spacebar

### Phase 2 Development:
- Add a single alien to the top-left corner of the screen, with appropriate spacing
- Fill the top portion of the screen with as many aliens as possible horizontally. Additional rows of aliens will be created until an entire fleet is created
- Make the fleet move sideways and down until they all get shot down. Then, a new fleet will be created after that.
- If an alien hits a ship or the ground, the ship will be destroyed and a new fleet will be created
- Limit the number of ships the player can use and end the game when they run out of ships

### NOTE: cmd to run game -> py -3.12 alien_invasion.py
