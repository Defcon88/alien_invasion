import pygame
from pygame import *
import sys
from random import randint

class Blaster():
    def __init__(self):
        self.blast = pygame.mixer.Sound('sound_fx/blaster.wav')
        self.explode1 = pygame.mixer.Sound('sound_fx/explosion1.wav')
        self.explode2 = pygame.mixer.Sound('sound_fx/explosion2.wav')
        self.explode3 = pygame.mixer.Sound('sound_fx/explosion3.wav')
    
    def get_explosion(self):
        self.randomx = randint(1,3)
        if self.randomx == 1:
            return self.explode1
        if self.randomx == 2:
            return self.explode2
        else:
            return self.explode3
