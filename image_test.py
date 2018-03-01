import pygame


image = pygame.image.load('images/t_fighter.png')
rect = image.get_rect()
print(rect.top)
print(rect.bottom)
print(rect.left)
print(rect.right)

image = pygame.transform.scale(image, (100, 81))
