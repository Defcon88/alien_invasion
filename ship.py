import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self, ai_settings, screen):
        '''initialize the ship and set its starting position'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/xwing.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start each new shop at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # store a decimal value for the ship's center
        self.center = float(self.rect.centerx)
        
        # movement flag
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        '''Update the ship's position based on the movement flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        
        
        #Update rect object from self.center.
        self.rect.centerx = self.center
        
    def blitme(self):
        '''draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        '''center the ship on teh screen.'''
        self.center = self.screen_rect.centerx
