import pygame
import csv
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Map():
    def __init__(self, file):
        self.tile_size = 16
        self.file = file



    def read(self):
        maps = []
        with open(os.path.join((self.file))) as data:
            for row in data:
                maps.append(list(row))

        return maps

    def load(self):
        tiles = []
        cutes = []
        max_row = 30
        y = 0
        maps = self.read()
        for row in maps:
            x = 0
            for tile in row:
                if tile == 177:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("grass.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 286:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("bush.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 337:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("shroom.png", temp_x, temp_y)
                    cutes.append(temp)
                if tile == 318:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("part1.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 319:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("part2.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 320:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("part3.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 321:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("part4.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 338:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("shrooms.png", temp_x, temp_y)
                    cutes.append(temp)
                if tile == 250:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("flour.png", temp_x, temp_y)
                    cutes.append(temp)
                if tile == 251:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("flours.png", temp_x, temp_y)
                    cutes.append(temp)
                if tile == 252:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("flourss.png", temp_x, temp_y)
                    cutes.append(temp)
                if tile == 61:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("orange.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 292:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("minibush.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 291:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("biggerbush.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 333:
                    temp_x = x*self.tile_size
                    temp_y = (max_row - y) * self.tile_size
                    temp = Tile("statue.png", temp_x, temp_y)
                    tiles.append(temp)
                if tile == 290:
                    tiles.append(Tile("statue.png", x*self.tile_size, (max_row - y) * self.tile_size))
                    
                    
                
                    
                x +=1
            y +=1
                
                  
        
