import pygame
from sys import exit
from rand import *
from random import choice, randrange
from second import *
##def draw_speech_bubble(screen, text, text_colour, bg_colour, pos, size):
##
##    font = pg.font.SysFont(None, size)
##    text_surface = font.render(text, True, text_colour)
##    text_rect = text_surface.get_rect(midbottom=pos)
##
##    # background
##    bg_rect = text_rect.copy()
##    bg_rect.inflate_ip(10, 10)
## 
##    # Frame
##    frame_rect = bg_rect.copy()
##    frame_rect.inflate_ip(4, 4)
##
##    pg.draw.rect(screen, text_colour, frame_rect)
##    pg.draw.rect(screen, bg_colour, bg_rect)
##    screen.blit(text_surface, text_rect)

class Others(pygame.sprite.Sprite):
    def __init__(self, pic, x, y, file, obstacles = None, direction = None, index = 0):
        super().__init__()
        self.screen = pygame.display.set_mode((1400, 790))
        self.image = pygame.image.load(pic).convert_alpha()
        self.image = pygame.transform.scale(self.image,(150,160))
        self.rect = self.image.get_rect(midbottom = (x, y))
        self.font = pygame.font.Font(None, 30)
        self.spoke = False
        self.speaking = False
        self.screenChange = False
        self.hits = 0
        self.dx = 3
        if file:
            self.filehandle = open(file,"r")
            self.convo = self.filehandle.readline().strip()
        else:
            self.filehandle = ""
        self.pause = False
        self.obstacles = obstacles
        self.obstacles.rect.x = x
        self.passed = False
        self.move = ["s"]
        self.timer = randrange(50, 150, 10)
        self.y = y
        self.x = x
        self.direction = direction
        self.index = index
        
    def jump(self):
        self.gravity = -20
        self.gravity +=1
        while self.rect.bottom < self.y:
            self.rect.bottom +=self.gravity
            self.gravity +=1
        if self.rect.bottom >= self.y:
            self.rect.bottom = self.y
        
    def right(self):
        if self.rect.x <= 1360:
            self.rect.x += self.dx

    def left(self):
        if self.rect.x >= 850:
            self.rect.x -= self.dx

    def swap(self):
        self.image = pygame.transform.flip(self.image, True, False)


    def gravities(self):
        keys = pygame.keys_pressed()
        if keys[K_w] and self.rect.bottom >= self.bottom:
            self.gravity = -20
        
    def jump(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.bottom:
            self.rect.bottom = self.bottom
            
    def randomMove(self):
        x = choice(self.move)
        if x == "d":
            self.right()
        elif x == "s":
            self.left()
        else:
            self.swap()
            
    def shootLaser(self):
        if self.direction == "right":
            self.obstacles.rect.x += 2
            if self.obstacles.rect.x > 1400:
                self.obstacles.rect.x = self.x
        else:
            self.obstacles.image = pygame.transform.flip(self.obstacles.image, True, False)
            self.obstacles.rect.x -= 2
            if self.obstacles.rect.x < 0:
                self.obstacles.rect.x = self.x
        #self.obstacles.rect.x += 1
        
    def collide(self):
        if self.rect.colliderect(player.sprite.rect):
            return True
    
    def speak(self):
        if self.collide() and self.filehandle:
            text = self.font.render("press E to speak", False, 'Black')
            textRect = text.get_rect(midbottom = (self.rect.midtop))
            bg_rect = textRect.copy()
            bg_rect.inflate_ip(10, 10)
            frame_rect = bg_rect.copy()
            frame_rect.inflate_ip(4, 4)
            pygame.draw.rect(self.screen, 'Black', frame_rect)
            pygame.draw.rect(self.screen, (255, 235, 231), bg_rect)
            screen.blit(text, bg_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.speaking = True
            if self.speaking and keys[pygame.K_SPACE] and not self.pause:
                self.convo = self.filehandle.readline().strip()
                #print(self.convo)
                if self.convo:
                    self.pause = True
                #self.printSpeak()
                #self.screen = pygame.display.set_mode((1400, 790))
            if self.speaking and not keys[pygame.K_SPACE] and self.pause:
                #print("Setting pause to False in speak")
                self.pause = False
            if self.index == 1:
                self.bearSpeak()
##            if self.spoke == True:
##                x, y = self.obstacles.puzzleSolve()
##                print(self.pause)
##                if x == None:
##                    pass
##                    #self.convo = "Go on! Guess!"
##                elif x == 5 and not self.pause:
##                    self.convo = "WOOOO. you did it!! go on to the next puzzle"
##                    self.passed = True
##                else:
##                    self.convo = f"you got {x} correct and {y} almost"
##            if self.passed == True:
##                #print("yo")
##                self.convo = "Didnt i tell you to get out of here. Go shoo, you did it already"
##                #self.pause = False

    def bearSpeak(self):
        if self.spoke == True:
            x, y = self.obstacles.puzzleSolve()
            #print(self.pause)
            if x == None:
                pass
                #self.convo = "Go on! Guess!"
            elif x == 5 and not self.pause:
                self.convo = "WOOOO. you did it!! go on to the next puzzle"
                self.passed = True
            else:
                self.convo = f"you got {x} correct and {y} almost"
        if self.passed == True:
            #print("yo")
            self.convo = "Didnt i tell you to get out of here. Go shoo, you did it already"
            #self.pause = False
                
    def obstacleUpdate(self):
##        if self.index == 3:
##            self.timer += 10
##            if self.timer % 20 == 0:
##                self.shootLaser()
##            if self.timer % 80 == 0:
##                self.randomMove()
##            self.screen.blit(self.obstacles.image, (self.obstacles.rect.x, self.obstacles.rect.y))
        self.speak()
        self.check()
       
    def check(self):
        if self.speaking == True or self.spoke == True:
            if self.speaking:
                keys = pygame.key.get_pressed()
                #print("here",keys[pygame.K_SPACE],not self.pause)
                if keys[pygame.K_SPACE] and not self.pause:
                    #print("reading line:"+self.filehandle.readline())
                    if not self.filehandle.readline():
                        self.speaking = False
                        self.spoke = True
                    #self.filehandle = open("newtrial.txt","r")
                    #print("set speaking to false")
        #if not self.filehandle.readline():
            #self.filehandle = open("newtrial.txt","w")

    def printSpeak(self):
        chat = pygame.image.load("mk.png").convert_alpha()
        chat = pygame.transform.scale(chat,(1200,300))
        chatRect = chat.get_rect(midbottom = (700, 750))
        print(self.convo)
        text = self.font.render(self.convo, False, 'White')
        textRect = text.get_rect(topleft = (250, 550))
        #chat.blit(text,chatRect)
            #while not keys[pygame.K_SPACE]:
        self.screen.blit(chat, chatRect)
        self.screen.blit(text, textRect)
            #self.screen.blit(chat.blit(text,chatRect))
        self.screen.blit(self.image, (80, 640))
        #self.spoke = True
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pic, x, y, scalex, scaley, index):
        super().__init__()
        self.screen = pygame.display.set_mode((1400, 790))
        self.image = pygame.image.load(pic).convert_alpha()
        self.image = pygame.transform.scale(self.image,(scalex,scaley))
        self.rect = self.image.get_rect(center = (x, y))
        self.font = pygame.font.Font(None, 30)
        self.otherscreen = pygame.image.load("words.png").convert_alpha()
        self.otherscreen = pygame.transform.scale(self.otherscreen,(1400,790))
        self.screenChange = False
        self.index = index
        if self.index == 1:
            self.initializePuzzle()
            self.trial = []
        self.passed = False

    def initializePuzzle(self):
        self.puzzleDictionary = {}
        A = pygame.image.load("A.png").convert_alpha()
        A = pygame.transform.scale(A,(90,120))
        Arect = A.get_rect(midleft = (130, 700))
        E = pygame.image.load("E.png").convert_alpha()
        E = pygame.transform.scale(E,(100,120))
        Erect = E.get_rect(midleft = Arect.midright)
        I = pygame.image.load("I.png").convert_alpha()
        I = pygame.transform.scale(I,(100,120))
        Irect = I.get_rect(midleft = Erect.midright)
        O = pygame.image.load("O.png").convert_alpha()
        O = pygame.transform.scale(O,(100,120))
        Orect = O.get_rect(midleft = Irect.midright)
        P = pygame.image.load("P.png").convert_alpha()
        P = pygame.transform.scale(P,(100,120))
        Prect = P.get_rect(midleft = Orect.midright)
        F = pygame.image.load("F.png").convert_alpha()
        F = pygame.transform.scale(F,(100,120))
        Frect = F.get_rect(midleft = Prect.midright)
        G = pygame.image.load("G.png").convert_alpha()
        G = pygame.transform.scale(G,(100,120))
        Grect = G.get_rect(midleft = Frect.midright)
        H = pygame.image.load("HH.png").convert_alpha()
        H = pygame.transform.scale(H,(100,120))
        Hrect = H.get_rect(midleft = Grect.midright)
        N = pygame.image.load("N.png").convert_alpha()
        N = pygame.transform.scale(N,(100,120))
        Nrect = N.get_rect(midleft = Hrect.midright)
        R = pygame.image.load("R.png").convert_alpha()
        R = pygame.transform.scale(R,(100,120))
        Rrect = R.get_rect(midleft = Nrect.midright)
        T = pygame.image.load("T.png").convert_alpha()
        T = pygame.transform.scale(T,(100,120))
        Trect = T.get_rect(midleft = Rrect.midright)
        S = pygame.image.load("S.png").convert_alpha()
        S = pygame.transform.scale(S,(100,120))
        Srect = S.get_rect(midleft = Trect.midright)
        self.puzzleDictionary['A'] = (A, Arect)
        self.puzzleDictionary['E'] = (E, Erect)
        self.puzzleDictionary['I'] = (I, Irect)
        self.puzzleDictionary['O'] = (O, Orect)
        self.puzzleDictionary['P'] = (P, Prect)
        self.puzzleDictionary['F'] = (F, Frect)
        self.puzzleDictionary['G'] = (G, Grect)
        self.puzzleDictionary['H'] = (H, Hrect)
        self.puzzleDictionary['N'] = (N, Nrect)
        self.puzzleDictionary['R'] = (R, Rrect)
        self.puzzleDictionary['T'] = (T, Trect)
        self.puzzleDictionary['S'] = (S, Srect)
        
        
    def interact(self):
        if abs(player.sprite.rect.center[0] - self.rect.center[0]) < 100:
            if not self.screenChange:
                text = self.font.render("press E", False, 'Black')
                textRect = text.get_rect(midbottom = (player.sprite.rect.midright))
                screen.blit(text, textRect)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    self.screenChange = True
                    self.puzzle()
                 #self.screen.blit(self.otherscreen, (0,0))

    def mouse(self, rect):
        pos = pygame.mouse.get_pos()
        return rect.collidepoint(pos[0], pos[1])

    def puzzleSolve(self):
        right = "faith"
        numCorrect = 0
        numAlmost = 0
        if len(self.trial) == 5:
            print(self.trial)
            for count in range(5):
                if self.trial[count].lower() == right[count]:
                    numCorrect += 1
                    print(self.trial[count])
                    self.trial[count] = "X"
            for i in self.trial:
                if i != "X" and i.lower() in right:
                    print(i)
                    numAlmost += 1
            self.trial = []
            if numCorrect == 5:
                self.passed = True
            return numCorrect, numAlmost
        return None,None
    
    def puzzle(self):
        for i in self.puzzleDictionary:
            #print(self.mouse(self.puzzleDictionary[i][1]))
            if self.mouse(self.puzzleDictionary[i][1]):
                for event in pygame.event.get():
                    #print(event.type == pygame.MOUSEBUTTONDOWN)
                    if event.type == pygame.MOUSEBUTTONDOWN and len(self.trial)!=5:
                        rect = self.puzzleDictionary[i][1]
                        if rect.y < 600 and self.trial.index(i) == (len(self.trial)-1):
                            rect.y = 700
                            temp = self.trial.index(i)
                            self.trial.pop(temp)
                        elif rect.centery == 700:
                            rect.x = 150 + (len(self.trial)*250)
                            rect.y = 350
                            self.puzzleDictionary[i] = (self.puzzleDictionary[i][0], rect)
                            self.trial.append(i)
                        #print("hiii/")       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.screenChange = False
            if len(self.trial) ==5:
                self.initializePuzzle()
            
    def obstacleUpdate(self):
        if self.index == 1:
            self.interact()
            self.puzzle()
            
            
        
class Character(pygame.sprite.Sprite):
    def __init__ (self, index):
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
        self.index = index
        self.bottom = 720
        if self.index == 0:
            self.bottom = 665
        self.image = pygame.transform.scale(self.image,(100,110))
        self.rect = self.image.get_rect(midbottom = (100, self.bottom))
        self.gravity = 0
        self.rightreset = False
        self.leftreset = False
        self.index = index

    def getLeft(self):
        return self.rect.midleft

    def getRight(self):
        return self.rect.midright
    
    def gravities(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.bottom >= self.bottom:
            self.gravity = -20
        
    def jump(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.bottom:
            self.rect.bottom = self.bottom

    def animateRight(self):
        if self.rect.bottom < self.bottom:
            pass
        else:
            self.index += 0.2
            if self.index >= len(self.move):
                self.index = 0
            self.image = self.move[int(self.index)]
            self.image = pygame.transform.scale(self.image,(100,110))
    
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
##        elif keys[pygame.K_w]:
##            if self.rect.y <= 100:
##                pass
##            else:
##                print(self.rect.y)
##                self.rect.y -= 5
                
                    
    def update(self):
        self.gravities()
        self.jump()
        self.moves()
        self.resets()

    def resets(self):
        if self.rightreset == True:
            self.rect.midbottom = (100, self.bottom)
            self.rightreset = False
        if self.leftreset == True:
            self.rect.midbottom = (1300, self.bottom)
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
    def __init__(self, pic, right = None, left = None, passes = True, obstacles = {}, people = {}, index = 0):
        self.pic = pic
        self.screen = pygame.display.set_mode((1400, 800))
        self.image = pygame.image.load(pic).convert_alpha()
        self.image = pygame.transform.scale(self.image, (2000, 800))
        self.right = right
        self.left = left
        self.obstacles = obstacles
        self.people = people
        self.screen.blit(self.image, (0,0))
        self.toggleRight = False
        self.toggleLeft = False
        self.Puzzle = False
        self.imageChange = False
        self.speakChange = False
        self.passed = passes
        self.index = index
        print(self.index)
        if self.right != None:
            self.right = pygame.image.load(right).convert_alpha()
            self.right = pygame.transform.scale(self.right,(80,60))
            self.rightRect = self.right.get_rect(center=(1310, 590))
            if self.passed:
                self.screen.blit(self.right, self.rightRect)
        if self.left != None:
            self.left = pygame.image.load(left).convert_alpha()
            self.left = pygame.transform.scale(self.left,(80,60))
            self.leftRect = self.left.get_rect(center=(30, 590))
            self.screen.blit(self.left, self.leftRect)

    def obstaclesCall(self):
        for i in self.obstacles:
            i.obstacleUpdate()
        for i in self.people:
            i.obstacleUpdate()

    def speakCall(self):
        for i in self.people:
            if i .speaking == True:
                    i.printSpeak()
                    self.speakChange = True
            else:
                self.speakChange = False
                
    def puzzleCall(self):
        for i in self.obstacles:
            if i.passed == True:
                self.passed = True
            if i.screenChange == True:
                self.image = i.otherscreen
                self.imageChange = True
            else:
                self.image = pygame.image.load(self.pic).convert_alpha()
                self.image = pygame.transform.scale(self.image, (1400, 800))
                self.imageChange = False
                
    def update(self):
        self.screen.blit(self.image, (0,0))
        if not self.imageChange:
            for i in self.obstacles:
                self.screen.blit(self.obstacles[i][0], self.obstacles[i][1])
            for i in self.people:
                self.screen.blit(self.people[i][0], self.people[i][1])
            if self.right != None and self.passed:
                self.screen.blit(self.right, (1310, 590))
            if self.left != None:
                self.screen.blit(self.left, (30, 590))
        elif self.index == 1:
            for i in self.obstacles:
                for j in i.puzzleDictionary:
                    self.screen.blit(i.puzzleDictionary[j][0], i.puzzleDictionary[j][1])
        self.obstaclesCall()
        self.speakCall()
        if self.index == 1:
            self.puzzleCall()

    def change(self, index, starting):
        #print(index)
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


class Event():
    def __init__(self):
        self.type = "move"
pygame.init()
peng = pygame.image.load("peng.png")
#screen = pygame.display.set_mode((1400, 790))
pygame.display.set_icon(peng)

def playerCollide(self):
    if pygame.sprite.spritecollide(player.sprite, board, False):
        return True
    return False

i = "living.webp"
j = "ice.jpeg"
k = "for nwot.jpeg"
l = "iceback.webp"
m = "backs.jpeg"
##jObstacles = pygame.sprite.Group()
##jObstacles.add(Others())
##jObstacles.add(Obstacles())
board = Obstacle("boards.png", 700, 350, 1000, 600, 1)
laser = Obstacle("fishy.png", 0, 620, 40, 30, 3)
jPeople = {}
jObstacles = {}
cats = {}
lasers = {}
lasers[laser] = (laser.image, laser.rect, laser)
jObstacles[board] = (board.image, board.rect, board)
bear = Others("bear.png", 200, 620,"trial.txt",  board, index = 1)
cat = Others("cat.png", 1300, 680, "battle.txt", laser, index = 3)
cat1 = Others("morecat.png", 200, 690, "battle.txt", laser, "right", index = 3)
#cat2 = Others("reslguncat.png", 1300, 665, "")
cat3 = Others("othercat.png", 1150, 680, "", laser, index = 3)
cat4 = Others("evenmorecat.png", 1000, 680,"", laser, index = 3)
cats[cat] = (cat.image, cat.rect, cat)
cats[cat1] = (cat1.image, cat1.rect, cat1)
#cats[cat2] = (cat2.image, cat2.rect, cat2)
cats[cat3] = (cat3.image, cat3.rect, cat3)
cats[cat4] = (cat4.image, cat4.rect, cat4)
jPeople[bear] = (bear.image, bear.rect, bear)
screen1 = Screen(i, "arrow.png")
screen2 = Screen(j, "arrow.png", "otherarrow.png", False, jObstacles, jPeople, index = 1)
#screen3 = Screen(k, "arrow.png","otherarrow.png", passes = False)
screen5 = Screen("roog.png", "arrow.png","otherarrow.png",False, {}, index = 3)
#screen4 = Screen(l,"arrow.png", "otherarrow.png")
screen4 = Map(grass, bushes, signs)
coins = 0
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 9, 0, 2, 1, 1, 1, 3, 0, 1, 3, 1, 1, 1, 3, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1], 
[1, 1, 0, 0, 2, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 3, 0, 0, 0, 1, 1, 1, 1, 1], 
[1, 1, 0, 0, 0, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1], 
[1, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6, 0, 0, 0, 2, 1, 1, 1, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 2, 1, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1, 1],
[1, 1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1, 1],
[1, 1, 5, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
[1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 1, 0, 0, 0, 0, 2, 0, 0, 6, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1 ,1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 10, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
screen3 = World(world_data)

screens = [screen1, screen2, screen3, screen4, screen5]
index = 0
screen = screens[index]
clock = pygame.time.Clock()
font = pygame.font.Font("mario.ttf", 70)
fonts = pygame.font.Font("mario.ttf", 40)
newfont = pygame.font.Font("mario.ttf", 20)
player = pygame.sprite.GroupSingle()
player.add(Character(index))
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
bg_img = pygame.image.load('sku.png')
bg_img = pygame.transform.scale(bg_img, (1400, 2000))
bgrect = bg_img.get_rect(center = (700, 400))
move = Event()

def mouseCollide(textRect):
    pos = pygame.mouse.get_pos()
    return textRect.collidepoint(pos[0], pos[1])

while True:
    events = [move]
    temp = pygame.event.get()
    events.extend(temp)
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if game_active:
            if index == 3:
                screen = screens[index]
                screen.fill((20, 36, 15))
                screen.update()
                screen.player.move = True
                if screen.sign() == "next":
                    text = fonts.render("next?", False, 'Black')
                    textRect = text.get_rect(center = (1350, 560))
                    screen.blit(text, textRect)
                if event.type == pygame.MOUSEBUTTONDOWN and mouseCollide(textRect):
                    index = index + 1
                    player.sprite.rightreset = True
                elif screen.sign() == "back":
                    text = newfont.render("back?", False, 'Black')
                    textRect = text.get_rect(midbottom = (screen.player.rect.midtop))
                    screen.blit(text, textRect)
                    if mouseCollide(textRect) and event.type == pygame.MOUSEBUTTONDOWN:
                        index = index - 1
                        player.sprite.leftreset = True
            elif index != 2:
                screen = screens[index]
                screen.update()
                if screen.speakChange == True or screen.imageChange == True:
                    pass
                else:
                    player.draw(screen)
                    player.update()
                if not screen.collide(player):
                    screen.toggleRight = False
                    screen.toggleLeft = False
                if screen.collide(player) and screen.toggleRight and screen.passed:
                    text = fonts.render("next?", False, 'Black')
                    textRect = text.get_rect(center = (1350, 560))
                    screen.blit(text, textRect)
                    diff = index
                    if event.type == pygame.MOUSEBUTTONDOWN and mouseCollide(textRect):
                        index = index + 1
                        player.sprite.rightreset = True
                elif screen.collide(player) and screen.toggleLeft:
                    text = fonts.render("back?", False, 'Black')
                    textRect = text.get_rect(center = (60, 560))
                    screen.blit(text, textRect)
                    if mouseCollide(textRect) and event.type == pygame.MOUSEBUTTONDOWN:
                        index = index - 1
                        player.sprite.leftreset = True

            else:
                screen.blit(bg_img, bgrect)
                screen = screens[index]
                screen.update()
                #screen.player.update()
                screen.reset()
                if screen.collide(screen.lists):
                    text = newfont.render("back?", False, 'Black')
                    textRect = text.get_rect(midbottom = (screen.player.rect.midtop))
                    screen.blit(text, textRect)
                    if mouseCollide(textRect) and event.type == pygame.MOUSEBUTTONDOWN:
                        index = index - 1
                        player.sprite.leftreset = True
                if screen.collide(screen.listss):
                    text = fonts.render("next?", False, 'Black')
                    textRect = text.get_rect(midbottom = (screen.player.rect.midtop))
                    screen.blit(text, textRect)
                    if event.type == pygame.MOUSEBUTTONDOWN and mouseCollide(textRect):
                        index = index + 1
                        player.sprite.rightreset = True
                if screen.collide(screen.coins):
                    # play sound
                    coins += 1
                    
                
        else:
            temp = (176, 180, 207)
            screen.fill(temp)
            timer = timer + 2
            titleText = font.render("Articventure", False, 'Black')
            titleTextRect = titleText.get_rect(center = (700, 100))
            screen.blit(titleText, titleTextRect)
            screen.blit(gameStart, startRect)
            if mouseCollide(startRect):
                gameStart = pygame.transform.scale(button, (250, 75))
                startRect = gameStart.get_rect(center = (700, 300))
                if event.type == pygame.MOUSEBUTTONDOWN and not game_active:
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
