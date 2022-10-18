import pygame
from sys import exit
class Character(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
##        first = pygame.image.load("dude.png").convert_alpha()
##        third = pygame.image.load("third dude.png").convert_alpha()
##        fourth = pygame.image.load("fourth dude.png").convert_alpha()
##        fifth = pygame.image.load("fifth dude.png").convert_alpha()
##        sixth = pygame.image.load("sixth dude.png").convert_alpha()
##        seventh = pygame.image.load("seventh dude.png").convert_alpha()
##        second = pygame.image.load("middledede.png").convert_alpha()
        first = pygame.image.load("real1.png").convert_alpha()
        third = pygame.image.load("3.png").convert_alpha()
        fourth = pygame.image.load("4.png").convert_alpha()
        fifth = pygame.image.load("5.png").convert_alpha()
        sixth = pygame.image.load("6.png").convert_alpha()
        seventh = pygame.image.load("1.png").convert_alpha()
        second = pygame.image.load("2.png").convert_alpha()
        self.move = [first, second, third, fourth, fifth, sixth,seventh]
        self.index = 0
        self.image = self.move[self.index]
        self.direction = "right"
        self.image = pygame.transform.scale(self.image,(120,130))
        self.rect = self.image.get_rect(midbottom = (100, 720))
        self.gravity = 0
        self.rightreset = False
        self.leftreset = False

    def getLeft(self):
        return self.rect.midleft

    def getRight(self):
        return self.rect.midright
    
    def gravities(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.bottom >= 720:
            self.gravity = -20
        
    def jump(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 720:
            self.rect.bottom = 720

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
        
    def moves(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if self.rect.x >= 1350:
                pass
            else:
                if self.direction == "right":
                    self.rect.x += 8
                    self.animateRight()
                else:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.direction = "right"
                    self.rect.x += 8
                    self.swap()
                    self.animateRight()
        elif keys[pygame.K_a]:
            if self.rect.x <= -50:
                pass
            else:
                if self.direction == "right":
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.direction = "left"
                    self.rect.x -= 8
                    self.swap()
                    self.animateRight()
                else:
                    self.rect.x -= 8
                    self.animateRight()
                    
    def update(self):
        self.gravities()
        self.jump()
        self.moves()
        self.resets()

    def resets(self):
        if self.rightreset == True:
            self.rect.midbottom = (100, 720)
            self.rightreset = False
        if self.leftreset == True:
            self.rect.midbottom = (1300, 720)
            self.leftreset = False
##
##class Button():
##    def __init__(self, pic):
##        self.image = pygame.image.load(pic).convert_alpha()
##        self.image = pygame.transform.scale(self.image, (20, 20))
##        self.rect = self.image.get_rect(center = (700, 300))
##        
##    def hover(self):
##        pos = pygame.mouse.get_pos()
##        return self.rect.collidepoint(pos[0], pos[1])
##        
    
class Screen():
    def __init__(self, pic, right = None, left = None):
        self.screen = pygame.display.set_mode((1400, 790))
        self.image = pygame.image.load(pic).convert_alpha()
        self.image = pygame.transform.scale(self.image, (1400, 790))
        self.right = right
        self.left = left
        self.screen.blit(self.image, (0,0))
        if self.right != None:
            self.right = pygame.image.load(right).convert_alpha()
            self.right = pygame.transform.scale(self.right,(80,60))
            self.rightRect = self.right.get_rect(center=(1310, 590))
            self.screen.blit(self.right, self.rightRect)
        if self.left != None:
            self.left = pygame.image.load(left).convert_alpha()
            self.left = pygame.transform.scale(self.left,(80,60))
            self.leftRect = self.left.get_rect(center=(30, 590))
            self.screen.blit(self.left, self.leftRect)
        self.toggleRight = False
        self.toggleLeft = False

    def update(self):
        self.screen.blit(self.image, (0,0))
        if self.right != None:
            self.screen.blit(self.right, (1310, 590))
        if self.left != None:
            self.screen.blit(self.left, (30, 590))

    def change(self, index, starting):
        print(index)
        index += 0.2
        if index >= len(starting):
            index = 0
        self.image = starting[int(index)]
        
    def blit(self, image, rect):
        self.screen.blit(image, rect)

    def quit(self):
        self.screen.pygame.display.quit()

    def fill(self, color):
        self.screen.fill(color)

    def getRight(self):
        return self.rightRect
    
    def collide(self, player):
        if self.left == None:
            if player.sprite.rect.midright >= self.rightRect.midleft:
                self.toggleRight = True
                return True
        elif self.right == None:
             if player.sprite.rect.midleft <= self.leftRect.midright:
                 self.toggleLeft = True
                 return True
        else:
            if player.sprite.rect.midright >= self.rightRect.midleft or player.sprite.rect.midleft <= self.leftRect.midright:
                if player.sprite.rect.midright >= self.rightRect.midleft:
                    self.toggleRight = True
                else:
                    self.toggleLeft = True
                return True
        return False
        
        
pygame.init()
peng = pygame.image.load("peng.png")
#screen = pygame.display.set_mode((1400, 790))
pygame.display.set_icon(peng)

i = "living.webp"
j = "ice.jpeg"
k = "for nwot.jpeg"
l = "iceback.webp"
m = "backs.jpeg"
screen1 = Screen(i, "arrow.png")
screen2 = Screen(j, "arrow.png", "otherarrow.png")
screen3 = Screen(k, "arrow.png","otherarrow.png")
screen4 = Screen(m, "arrow.png","otherarrow.png")
screen5 = Screen(l, left = "otherarrow.png")

screens = [screen1, screen2, screen3, screen4, screen5]
index = 0
screen = screens[index]
clock = pygame.time.Clock()

font = pygame.font.Font("mario.ttf", 70)
fonts = pygame.font.Font("mario.ttf", 40)
player = pygame.sprite.GroupSingle()
player.add(Character())
font = pygame.font.Font("mario.ttf", 70)
fonts = pygame.font.Font("mario.ttf", 40)
game_active = False
startingScreen = Screen("frame1.png")
otherStarting = Screen ("frame2.png")
starting = [startingScreen, otherStarting]
startIndex = 0
start = starting[startIndex]
timer = 0
button = pygame.image.load("button.png").convert_alpha()
gameStart = pygame.transform.scale(button, (200, 60))
startRect = gameStart.get_rect(center = (700, 300))

def mouseCollide(textRect):
    pos = pygame.mouse.get_pos()
    return textRect.collidepoint(pos[0], pos[1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        screen = screens[index]
        screen.update()
        player.draw(screen)
        player.update()
        if not screen.collide(player):
            screen.toggleRight = False
            screen.toggleLeft = False
        if screen.collide(player) and screen.toggleRight:
            text = fonts.render("next?", False, 'White')
            textRect = text.get_rect(center = (1350, 450))
            screen.blit(text, textRect)
            diff = index
            print(event.type == pygame.MOUSEBUTTONDOWN)
            print(mouseCollide(textRect))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and mouseCollide(textRect):
                    index = index + 1
                    player.sprite.rightreset = True
        elif screen.collide(player) and screen.toggleLeft:
            text = fonts.render("back?", False, 'White')
            textRect = text.get_rect(center = (60, 450))
            screen.blit(text, textRect)
            diff = index
            print(event.type == pygame.MOUSEBUTTONDOWN)
            print(mouseCollide(textRect))
            for event in pygame.event.get():
                if mouseCollide(textRect) and event.type == pygame.MOUSEBUTTONUP:
                    index = index - 1
                    player.sprite.leftreset = True
    else:
        start = starting[startIndex]
        start.update()
        timer = timer + 2
        titleText = font.render("Articventure", False, 'Black', "White")
        titleTextRect = titleText.get_rect(center = (700, 100))
        start.blit(titleText, titleTextRect)
        start.blit(gameStart, startRect)
        if mouseCollide(startRect):
            gameStart = pygame.transform.scale(button, (250, 75))
            startRect = gameStart.get_rect(center = (700, 300))
            for event in pygame.event.get():
                print("s",event.type == pygame.MOUSEBUTTONDOWN)
                print(mouseCollide(startRect))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_active = True
        else:
            gameStart = pygame.transform.scale(button, (200, 60))
            startRect = gameStart.get_rect(center = (700, 300))
        if timer%128 == 0:
            startIndex +=1
            startIndex = startIndex%2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_active = True
    clock.tick(60)
    pygame.display.update()

