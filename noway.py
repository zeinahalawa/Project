import pygame, sys
from pytmx.util_pygame import load_pygame
from rand import camera

pygame.init()
screen = pygame.display.set_mode((400, 500))
data = load_pygame("min.tmx")
