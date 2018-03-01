import pygame
from pygame import *
import sys
from random import randint

class Music():
    def __init__(self):
        self.song = pygame.mixer.music.load('music/song.mp3')
