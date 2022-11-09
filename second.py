# file that contains the maze screen
# intiializes and blits the player and the map

# some code was adapted from https://www.youtube.com/watch?v=ML2w92TIzoA&t=77s&ab_channel=CodingWithRuss
import pygame
from pytmx.util_pygame import load_pygame
from rand import camera
import copy

class Player(pygame.sprite.Sprite):
    def __init__(self, tiles, screen):
        super().__init__()
        self.image1 = pygame.image.load("lilwalk1.png")
        self.image2 = pygame.image.load("lilwalk2.png")
        self.image3 = pygame.image.load("lilwalk3.png")
        self.image4 = pygame.image.load("lilwalk4.png")
        self.images = [self.image1, self.image2, self.image3, self.image4]
        self.index = 0
        self.image = pygame.image.load("lilpeng.png")
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.tiles = tiles
        self.move = True
        self.screen = screen

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            temp = copy.deepcopy(self.rect)
            temp.x +=5
            if temp.collidelistall(self.tiles) == [] and self.move:
                self.rect.x += 5
                self.move = False
        if keys[pygame.K_a]:
            temp = copy.deepcopy(self.rect)
            temp.x -=5
            if temp.collidelistall(self.tiles) == [] and self.move:
                self.rect.x -= 5
                self.move = False

        if keys[pygame.K_w]:
            temp = copy.deepcopy(self.rect)
            temp.y -=3
            if temp.collidelistall(self.tiles) == [] and self.move:
                self.rect.y -= 3
                self.move = False
        if keys[pygame.K_s]:
            temp = copy.deepcopy(self.rect)
            temp.y +=3
            if temp.collidelistall(self.tiles) == [] and self.move:
                self.rect.y += 3
                self.move = False

        self.screen.blit(self.image, self.rect)
                
    def pics(self):
        self.index += 0.2
        if self.index >= len(self.move):
            self.index = 0
        self.image = self.images[int(self.index)]
        self.image = pygame.transform.scale(self.image,(16, 16))
        
class Tile(pygame.sprite.Sprite):
    def __init__(self,pic, pos):
        super().__init__()
        self.image = pic
        self.rect = self.image.get_rect(topleft = pos)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        pass


class Map():
    def __init__(self, tiles, bushes, signs):
        self.screen = pygame.display.set_mode((1400, 800))
        self.tiles = tiles
        #self.player = player
        self.player = Player(bushes, self.screen)
        self.players = [self.player]
        self.bushes = bushes
        self.signs = signs
        #print(self.signs)
        self.index = 0
        reset()

    def update(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.player.rect, 2)
        for tile in self.tiles:
            offset_pos = camera.othercalculate(self.player, tile.rect)
            tile.rect.x = offset_pos[0]
            tile.rect.y = offset_pos[1]
            self.screen.blit(tile.image, tile.rect)
        for tile in self.bushes:
            offset_pos = camera.othercalculate(self.player, tile.rect)
            tile.rect.x = offset_pos[0]
            tile.rect.y = offset_pos[1]
            self.screen.blit(tile.image, tile.rect)
        for tile in self.signs:
            offset_pos = camera.othercalculate(self.player, tile.rect)
            tile.rect.x = offset_pos[0]
            tile.rect.y = offset_pos[1]
            self.screen.blit(tile.image, tile.rect)
        for player in self.players:
            offset_pos = camera.othercalculate(self.player, player.rect)
            player.rect.x = offset_pos[0]
            player.rect.y = offset_pos[1]
            self.screen.blit(player.image, player.rect)
            player.update()

    def sign(self):
        if self.player.rect.collidelistall(self.signs) != []:
            if self.player.rect.collidelistall(self.signs)[0] == self.index:
                return "next"
            else:
                return "back"

    def blit(self, image, rect):
        self.screen.blit(image, rect)

    def fill(self, colour):
        self.screen.fill(colour)

pygame.init()
tmx_data = load_pygame("test.tmx")
bushes = []
signs = []
grass = []
def reset():
    layer = tmx_data.get_layer_by_name("grass").tiles()
    for x,y,surf in layer:
        pos = (((x*16)), ((y*16)-1074))
        grass.append(Tile(surf, pos))
    layer = tmx_data.get_layer_by_name("bush").tiles()
    for x,y,surf in layer:
        pos = (((x*16)), ((y*16)-1074))
        bushes.append(Tile(surf, pos))
    layer = tmx_data.get_layer_by_name("sign").tiles()
    for x,y,surf in layer:
        pos = (((x*16)), ((y*16)-1074))
        signs.append(Tile(surf, pos))
