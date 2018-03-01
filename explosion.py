import pygame
from pygame import time
from pygame.sprite import Sprite


class Explosion(Sprite):
    '''A class for creating explosions'''
    
    def __init__(self, center):
        super().__init__()
        
        #list of file names
        self.explosion_list = ['images/explosion1.png', 'images/explosion2.png', 
    'images/explosion3.png', 'images/explosion4.png']
        
        #make a list to store images
        self.explosion_anim = []
        
        #load the images to create the animation and rescale to proper size
        for img in self.explosion_list:
            image = pygame.image.load(img)
            image = pygame.transform.scale(image, (50,50))
            self.explosion_anim.append(image)
        
        self.center = center
        self.image = self.explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50


    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect.center = center
    
    def draw_explosion(self):
        '''draw the explosion to the screen'''
        self.screen.blit(self.image, self.rect)
        
