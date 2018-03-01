import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
from pygame import mixer
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from sound_fx import Blaster
from music import Music
from scoreboard import Scoreboard

import game_functions as gf
from explosion import Explosion


def run_game():
    #initialize game and create a screen object.
    pygame.init()
    mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    ai_settings = Settings()
    screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    blaster = Blaster()
    music = Music()
    
    #make the Play button
    play_button = Button(ai_settings, screen, "Play")
    
    #create an instance to store game stats and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    explosions = Group()
    
    #create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    pygame.mixer.music.play(-1, 24.8)
    
    #start the main loop of the game
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, 
            aliens, bullets, blaster, sb)
        if stats.game_active ==  True:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, 
                bullets, blaster, explosions, sb, stats)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, 
                bullets, sb)
            explosions.update()
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, 
            play_button, explosions, sb)
            
run_game()
