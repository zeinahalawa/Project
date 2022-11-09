import pygame
from random import choice
from sys import exit

class Screened():
    def __init__(self, pic, cardArray):
        self.screen = pygame.display.set_mode((1400, 800))
        self.image = pygame.image.load(pic).convert_alpha()
        self.image = pygame.transform.scale(self.image, (1400, 800))
        self.screen.blit(self.image, (0,0))
        self.timer = 0
        self.chosen =[]
        self.matched = 0
        self.back = "cardback.png"

    def blit(self, image, rect):
        self.screen.blit(image, rect)

    def quit(self):
        self.screen.pygame.display.quit()

    def fill(self, color):
        self.screen.fill(color)

    def run(self, cardArray):
        self.timer += 1
        for i in cardArray:
            self.screen.blit(i.image, (i.rect))
            #pygame.draw.rect(self.screen, 'White', i.rect,  2)

        for i in cardArray:
            i.update(self.chosen)
            if i.swapped and len(self.chosen) < 2 and i not in self.chosen:
                self.chosen.append(i)
                
        if self.timer%80 ==0:
            self.timer = 1
            if len(self.chosen) == 2:
                if self.chosen[0].index == self.chosen[1].index:
                    self.chosen[0].clickable = False
                    self.chosen[1].clickable = False
                    self.chosen[1].swapped = False
                    self.chosen[0].swapped = False
                    self.matched +=1
                    self.chosen = []
                else:
                    self.chosen[0].image = pygame.transform.scale(pygame.image.load(self.back).convert_alpha(), (100, 150))
                    self.chosen[1].image = pygame.transform.scale(pygame.image.load(self.back).convert_alpha(), (100, 150))
                    self.chosen[1].swapped = False
                    self.chosen[0].swapped = False
                    self.chosen[0].rect.y = self.chosen[0].y
                    self.chosen[1].rect.y = self.chosen[1].y
                    self.chosen = []
    
class Card():
    def __init__(self, pic, back, index):
        self.image = pygame.transform.scale(pygame.image.load(back).convert_alpha(), (100, 150))
        self.pic = pic
        self.rect = self.image.get_rect()
        self.swapped = False
        self.matched = False
        self.index = index
        self.clickable = True
        self.x = None
        self.y = None

    def collide(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos[0], pos[1])

    def update(self, chosen):
        if self.collide() and self.clickable and not self.swapped and len(chosen) < 2:
            self.swapped = True
            self.image =  pygame.transform.scale(pygame.image.load(self.pic).convert_alpha(), (100, 150))
            self.rect.y -= 10
            

def create(array):
    for i in range(len(array)):
        if i%4 == 0:
            array[i].rect.x = 400
            array[i].x = 400
        elif i%4 == 1:
            array[i].rect.x = 600
            array[i].x = 600
        elif i%4 == 2:
            array[i].rect.x = 800
            array[i].x = 800
        elif i%4 == 3:
            array[i].rect.x = 1000
            array[i].x = 1000
        if i <=3:
            array[i].rect.y = 50
            array[i].y = 50
        elif i > 3 and i <=7:
            array[i].rect.y = 250
            array[i].y = 250
        elif i > 7 and i <=11:
            array[i].rect.y = 450
            array[i].y = 450
        elif i >11 and i <=15:
            array[i].rect.y = 650
            array[i].y = 650
    return array

#screen = pygame.display.set_mode((1400,800))           
#background = pygame.transform.scale(pygame.image.load("poker.jpg"), (1400, 800))
def cardInitialize():
    back = "cardback.png"
    card1 = Card("meee.jpg", "cardback.png", 0)
    card2 = Card("me.JPG", "cardback.png", 0)
    card3 = Card("mugur.JPG", "cardback.png", 1)
    card4 = Card("girlmuugu.JPG",  "cardback.png", 1)
    card5 = Card("deep.jpg",  "cardback.png", 2)
    card6 = Card("girldeep.JPG", "cardback.png", 2)
    card7 = Card("test.JPG","cardback.png", 3)
    card8 = Card("girlaadi.JPG", "cardback.png", 3)
    card9 = Card("prof.jpg", "cardback.png", 4)
    card10 = Card("girlprof.JPG", "cardback.png", 4)
    card11 = Card("steve.jpg", "cardback.png", 5)
    card12 = Card("girlsteve.JPG", "cardback.png", 5)
    card13 = Card("sunayas.jpg", "cardback.png", 6)
    card14 = Card("girlsunaya.JPG", "cardback.png", 6)
    card15 = Card("imron.jpg", "cardback.png", 7)
    card16 = Card("femaleimron.JPG", "cardback.png", 7)
    matched = 0
    cardArray = []
    temp = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10, card11, card12, card13, card14, card15, card16]

    for count in range(16):
        x = choice(temp)
        y = temp.index(x)
        cardArray.append(x)
        temp.pop(y)
    return cardArray

#create(cardArray)


##    pygame.display.update()
##    clock.tick(60)
    
