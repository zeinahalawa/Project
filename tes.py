import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        stand = pygame.image.load("dude.png").convert_alpha()
        walk = pygame.image.load("middledede.png").convert_alpha()
        self.move = [stand, walk]
        self.player_index = 0
        self.image = self.move[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.bottom >= 300:
            self.gravity = -20


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = True
start_time = 0
score = 0

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

image = pygame.image.load("iceback.webp")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    if game_active:
        screen.blit(image, (0,0))
        player.draw(screen)
        player.update()

    pygame.display.update()
    clock.tick(60)
