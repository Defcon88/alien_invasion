import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''a class to manage bullets'''
    
    def __init__(self, ai_settings, screen, ship):
        '''create bullet object at the ship's current position'''
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/blaster.png')
        self.image = pygame.transform.scale(self.image, 
            (ai_settings.bullet_width, ai_settings.bullet_height))
        
        #create a bullet rect and then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.left + 4
        self.rect.top = ship.rect.top
        
        #store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''move the bullet up the screen'''
        #update the decimal position of the bullet
        self.y -= self.speed_factor
        #update rect position
        self.rect.y = self.y
    
    def draw_bullet(self):
        '''draw the bullet to the screen'''
        self.screen.blit(self.image, self.rect)

class RightBullet(Bullet):
    
    def __init__(self, ai_settings, screen, ship):
        super().__init__(ai_settings, screen, ship)
        self.rect.centerx = ship.rect.right -4
