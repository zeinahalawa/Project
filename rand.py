# file that creates the platformer game
# and contains the camera class that is used in most puzzles

import pygame
from pygame.locals import *
pygame.init()

screen_width = 1400
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

tile_size = 50

bg_img = pygame.image.load('sku.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, lists):
        self.image = pygame.image.load("platrom.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 3
        self.lists = lists


    def update(self):
        self.rect.x += self.dx
        for tile in self.lists:
            if self.rect.colliderect(tile.rect):
                self.dx = 0-self.dx

class Fox(pygame.sprite.Sprite):
    def __init__(self, img, rect, lists):
        self.fox1 = pygame.image.load("fox1.png").convert_alpha()
        self.fox2 = pygame.image.load("fox2.png").convert_alpha()
        self.fox3 = pygame.image.load("fox3.png").convert_alpha()
        self.fox4 = pygame.image.load("fox4.png").convert_alpha()
        self.fox5 = pygame.image.load("fox5.png").convert_alpha()
        self.foxes = [self.fox1, self.fox2, self.fox3, self.fox4, self.fox5]
        self.index = 0
        self.image = pygame.transform.scale(self.foxes[self.index],(50,30))
        self.rect = self.image.get_rect()
        self.rect.top = rect.y
        self.rect.x = rect.x
        self.dx = 3
        self.lists = lists

    def update(self):
        self.rect.x += self.dx
        for tile in self.lists:
            if self.rect.colliderect(tile.rect):
                self.swap()
                self.dx = 0-self.dx
        self.index += 0.1
        if self.index >= len(self.foxes):
            self.index = 0
        self.image = self.foxes[int(self.index)]
        self.image = pygame.transform.scale(self.image,(50,30))

    def swap(self):
        for i in range(len(self.foxes)):
            self.foxes[i] = pygame.transform.flip(self.foxes[i], True, False)
            
class Coin(pygame.sprite.Sprite):
    def __init__(self,x ,y):
        super().__init__()
        self.imaged = pygame.image.load("coins1.png").convert_alpha()
        self.image1 = pygame.image.load("coins2.png").convert_alpha()
        self.image2 = pygame.image.load("coins33.jpeg").convert_alpha()
        self.image3 = pygame.image.load("coins4.png").convert_alpha()
        self.image4 = pygame.image.load("coins5.png").convert_alpha()
        self.image5 = pygame.image.load("coins6.png").convert_alpha()
        self.image6 = pygame.image.load("coins7.png").convert_alpha()
        self.image7= pygame.image.load("coins8.png").convert_alpha()
        self.array = [self.imaged, self.image1, self.image2, self.image3, self.image4, self.image5, self.image6, self.image7]
        self.index = 0
        self.image = pygame.transform.scale(self.array[self.index],(25,25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.index += 0.1
        if self.index >= len(self.array):
            self.index = 0
        self.image = self.array[int(self.index)]
        self.image = pygame.transform.scale(self.image,(25,25))
        
class Character(pygame.sprite.Sprite):
    def __init__ (self, x, y, lists, platforms, obstacle):
        super().__init__()
        first = pygame.image.load("real1.png").convert_alpha()
        third = pygame.image.load("3.png").convert_alpha()
        fourth = pygame.image.load("4.png").convert_alpha()
        fifth = pygame.image.load("5.png").convert_alpha()
        sixth = pygame.image.load("6.png").convert_alpha()
        seventh = pygame.image.load("1.png").convert_alpha()
        second = pygame.image.load("2.png").convert_alpha()
        self.images_right = [first, second, third, fourth, fifth, sixth,seventh]
        self.images_left = [0]*7
        for i in range(7):
            self.images_left[i] = pygame.transform.flip(self.images_right[i], True, False)
        self.index = 0
        self.image = self.images_right[self.index]
        self.direction = "right"
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect(center = (x, y))
        self.gravity = 0
        self.rightreset = False
        self.leftreset = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.lists = lists
        self.platforms = platforms
        self.obstacle = obstacle
        self.counter = 0
        self.reset = False

    def getLeft(self):
        return self.rect.midleft

    def getRight(self):
        return self.rect.midright

    def animateRight(self):
        if self.rect.bottom < 720:
            pass
        else:
            self.index += 0.2
            if self.index >= len(self.move):
                self.index = 0
            self.image = self.move[int(self.index)]
            self.image = pygame.transform.scale(self.image,(120,130))
    
    def swap(self):
        for i in range(len(self.move)):
            self.move[i] = pygame.transform.flip(self.move[i], True, False)
    
      # this moving function was taken from https://youtu.be/ML2w92TIzoA
    def moves(self):
        #check for collision
        dx = 0
        dy = 0
        walk_cooldown = 5
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.jumped == False:
            self.vel_y = -12
            self.jumped = True
        if key[pygame.K_a]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_d]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_d] == False and key[pygame.K_a] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        if self.counter > walk_cooldown:
            self.counter = 0	
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for fox in self.obstacle:
            if self.rect.colliderect(fox.rect):
                self.reset = True
                
        for tile in self.lists:
                #check for collision in x direction
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #check for collision in y direction
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.vel_y = 0
                        #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.jumped = False
                    
        for platform in self.platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y >= 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.jumped = False
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

    def update(self):
        self.moves()

    def resets(self):
        if self.rightreset == True:
            self.rect.midbottom = (100, 720)
            self.rightreset = False
        if self.leftreset == True:
            self.rect.midbottom = (1300, 720)
            self.leftreset = False

class Tile(pygame.sprite.Sprite):
    def __init__(self, pic, rect):
        super().__init__()
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y

    def update(self):
        pass

class OtherTile(Tile):
    def __init__(self, pic, rect):
        super().__init__(pic, rect)
        self.initial = self.rect.x
        
    def update(self):
        self.rect.x += 1
        if self.rect.x - self.initial >= 50:
            self.rect.x = self.initial
            
class ExtraTile(Tile):
    def __init__(self, pic, rect):
        super().__init__(pic, rect)
        self.timer = 0
        
    def update(self):
        self.timer +=1
        if self.timer % 128 == 0:
            self.rect.centerx -= 1
        
class World(pygame.sprite.Group):
    def __init__(self, data):
        super().__init__()
        self.screen = pygame.display.set_mode((1400, 800))
        self.tile_list = []
        dirt_img = pygame.image.load('dirt.png')
        grass_img = pygame.image.load('grass.png')
        rightarrow_img = pygame.image.load('arrow.png').convert_alpha()
        leftarrow_img = pygame.image.load('otherarrow.png').convert_alpha()
        coin = pygame.image.load("coin1.jpeg").convert_alpha()
        platform = pygame.image.load("platrom.png").convert_alpha()
        foximg = pygame.image.load("fox1.png").convert_alpha()
        row_count = 0
        max_row = 22
        self.list = []
        self.lists = []
        self.listss = []
        self.coins = []
        self.platforms = []
        self.foxes = []
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = Tile(img, img_rect)
                    self.tile_list.append(temp)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = Tile(img, img_rect)
                    self.tile_list.append(temp)
                if tile == 3:
                    img = pygame.transform.scale(foximg, (tile_size, 30))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = Fox(img, img_rect, self.tile_list)
                    self.foxes.append(temp)
                if tile == 4:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-2) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = OtherTile(img, img_rect)
                    self.tile_list.append(temp)
                if tile == 5:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = ExtraTile(img, img_rect)
                    self.tile_list.append(temp)
                if tile == 6:
                    img = pygame.transform.scale(platform, (25, 25))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = Platform(img_rect.x, img_rect.y, self.tile_list)
                    self.platforms.append(temp)
                if tile == 7:
                    img = pygame.transform.scale(coin, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = Coin(img_rect.x, img_rect.y)
                    self.coins.append(temp)
                if tile == 9:
                    img = pygame.transform.scale(leftarrow_img, (tile_size, 50))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = Tile(img, img_rect)
                    self.lists.append(temp)
                if tile == 10:
                    img = pygame.transform.scale(rightarrow_img, (tile_size, 50))
                    img_rect = img.get_rect()
                    img_rect.x = (col_count-1) * tile_size
                    img_rect.y = (max_row - row_count) * tile_size
                    temp = Tile(img, img_rect)
                    self.listss.append(temp)
                col_count += 1
            row_count += 1
        self.player = Character(25, 750, self.tile_list, self.platforms, self.foxes)
        self.list.append(self.player)
        
    def update(self):
        for sprite in sorted(self.tile_list, key = lambda sprite: sprite.rect.centery):
            offset_pos = camera.calculate(self.player, sprite.rect)
            sprite.rect.x = offset_pos[0]
            sprite.rect.y = offset_pos[1]
            screen.blit(sprite.image, sprite.rect)
            sprite.update()
        for sprite in sorted(self.lists, key = lambda sprite: sprite.rect.centery):
            offset_pos = camera.calculate(self.player, sprite.rect)
            sprite.rect.x = offset_pos[0]
            sprite.rect.y = offset_pos[1]
            screen.blit(sprite.image, sprite.rect)
        for sprite in sorted(self.listss, key = lambda sprite: sprite.rect.centery):
            offset_pos = camera.calculate(self.player, sprite.rect)
            sprite.rect.x = offset_pos[0]
            sprite.rect.y = offset_pos[1]
            screen.blit(sprite.image, sprite.rect)
        for sprite in sorted(self.coins, key = lambda sprite: sprite.rect.centery):
            offset_pos = camera.calculate(self.player, sprite.rect)
            sprite.rect.x = offset_pos[0]
            sprite.rect.y = offset_pos[1]
            screen.blit(sprite.image, sprite.rect)
            sprite.update()
        for sprite in sorted(self.platforms, key = lambda sprite: sprite.rect.centery):
            offset_pos = camera.calculate(self.player, sprite.rect)
            sprite.rect.x = offset_pos[0]
            sprite.rect.y = offset_pos[1]
            sprite.update()
            screen.blit(sprite.image, sprite.rect)
        for sprite in sorted(self.foxes, key = lambda sprite: sprite.rect.centery):
            offset_pos = camera.calculate(self.player, sprite.rect)
            sprite.rect.x = offset_pos[0]
            sprite.rect.y = offset_pos[1]
            sprite.update()
            screen.blit(sprite.image, sprite.rect)
        for sprite in sorted(self.list, key = lambda sprite: sprite.rect.centery):
            offset_pos = camera.calculate(self.player, sprite.rect)
            sprite.rect.x = offset_pos[0]
            sprite.rect.y = offset_pos[1]
            screen.blit(sprite.image, sprite.rect)
        self.player.update()

    def collide(self, x):
        for i in range (len(x)):
            if x[i].rect.collidepoint((self.player.rect.x, self.player.rect.y)):
                if x == self.coins:
                    x.pop(i)
                return True
        
    def blit(self, image, rect):
        self.screen.blit(image, rect)

    def reset(self):
        if self.player.reset:
            self.player.rect.center = (25, 750)
            for tile in self.tile_list:
                try:
                    tile.rect.x = tile.initial
                except:
                    pass
            self.player.reset = False

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[9, 0, 2, 1, 1, 1, 3, 0, 1, 3, 1, 1, 1, 3, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1], 
[1, 0, 0, 2, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 3, 0, 0, 0, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 1, 0, 0, 0, 0, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6, 0, 0, 0, 2, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 2, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 5, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 6, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_grid():
    for line in range(0, 16):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (2000, line * tile_size))
    for line in range(0, 28):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height ))

# this camera code was taken from https://youtu.be/u7LPRqrzry8

class Camera():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
	
    def center_target_camera(self,target):
        #self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def center_target_cameras(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h
     
    def coin_calculate(self, player, x):
        self.center_target_camera(player)
        offset_pos = x.center - self.offset
        return offset_pos

    def othercalculate(self, player, x):
        self.center_target_cameras(player)
        #offset_pos = (100, 700)
        offset_pos = x.topleft - self.offset
        return offset_pos
    
    def calculate(self, player, x):
        self.center_target_camera(player)
        offset_pos = x.topleft - self.offset
        return offset_pos
    
camera = Camera()

