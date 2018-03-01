import pygame
from pygame.sprite import Sprite

class ShipStat(Sprite):
    
    def __init__(self, ai_settings, screen):
        '''initialize the ship and set its starting position'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/xwing.png')
        self.image = pygame.transform.scale(self.image,(30,32)) 
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
    def blitme(self):
        '''draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)
