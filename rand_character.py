import pygame

class Ship():
    
    def __init__(self, screen):
        '''initialize the ship and set its starting position'''
        self.screen = screen
        
        # Load the ship image and get its rec t.
        self.image = pygame.image.load('images/mario03.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
    
    def blitme(self):
        '''draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)
