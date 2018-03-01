import sys
import pygame

from settings import Settings
from rand_character import Ship

import game_functions as gf

def run_game():
    #initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    
    #make a ship
    ship = Ship(screen)
    
    #start the main loop of the game
    while True:
        gf.check_events()
        gf.update_screen(ai_settings, screen, ship)

run_game()

