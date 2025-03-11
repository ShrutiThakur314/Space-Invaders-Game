import pygame
import random
import math
from pygame import mixer


pygame.init()

screen = pygame.display.set_mode((800, 600))

mixer.music.load('Chaandaniya.mp3')
mixer.music.play(-1)
pygame.display.update()