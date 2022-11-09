# the main file
# imports all other files that are used, and calls them
# starts the game

import pygame
from sys import exit
from rand import *
from random import choice
from second import *
from login import begin, please, save
from cards import cardInitialize, Screened, create

#initializing a button class
class Button(pygame.sprite.Sprite):
    def __init__(self, pic, x, y, scalex, scaley, hoverx, hovery):
        super().__init__()
        self.image =  pygame.transform.scale(pygame.image.load(pic).convert_alpha(),(scalex, scaley))
        self.rect = self.image.get_rect(center = (x, y))
        # variables on where to position it, and how much to scale it by
        self.x = x
        self.y = y
        self.scalex = scalex 
        self.scaley = scaley
        # as well as the scale when hovering over it
        self.hoverx = hoverx
        self.hovery = hovery
        self.active = False # to check whether its clicked or not
        self.loggedIn = False # speciic to the login button
        self.count = 0

    def collide(self): # checks the mouse position
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos[0], pos[1])

    # checks if a button is being hovered over
    def update(self, mouse):
        if self.collide():
            self.image = pygame.transform.scale(self.image, (self.hoverx, self.hovery))
            self.rect = self.image.get_rect(center = (self.x, self.y))
            self.count +=0.2
        else:
            self.image = pygame.transform.scale(self.image, (self.scalex, self.scaley))
            self.rect = self.image.get_rect(center = (self.x, self.y))
        self.activate(mouse)

    # checks if a button has been clicked
    def activate(self, mouse):
        if self.collide() and mouse:
            self.active = True
            #mouse = False

# class for character that you can talk to            
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
        if file: # loading the file in which the dialogue is stored 
            self.filehandle = open(file,"r")
            self.convo = self.filehandle.readline().strip()
        else:
            self.filehandle = ""
        self.pause = False
        self.obstacles = obstacles
        self.obstacles.rect.x = x
        self.passed = False
        self.y = y
        self.x = x
        self.direction = direction
        self.index = index

    # checks if the player is colliding with the character        
    def collide(self):
        if self.rect.colliderect(player.sprite.rect):
            return True

    # handling all the speaking and interactions
    # between the player and the character
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
                if self.convo:
                    self.pause = True
            if self.speaking and not keys[pygame.K_SPACE] and self.pause:
                self.pause = False
            if self.index == 1:
                self.bearSpeak()

    # assessing the persons guess
    def bearSpeak(self):
        if self.spoke == True:
            x = self.obstacles.puzzleSolve()
            if x == None:
                pass
            elif "WOO" in x:
                self.passed = True
                self.convo = x
            else:
                self.convo = x

    # calling the functions that need to be constantly checked or updated          
    def obstacleUpdate(self):
        self.speak()
        self.check()

    # checking if the dialogue has ended 
    def check(self):
        if self.speaking == True or self.spoke == True:
            if self.speaking:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and not self.pause:
                    if not self.filehandle.readline():
                        self.speaking = False
                        self.spoke = True
                        
    # blitting the actual chat box and dialogue onto the screen
    def printSpeak(self):
        chat = pygame.image.load("mk.png").convert_alpha()
        chat = pygame.transform.scale(chat,(1200,300))
        chatRect = chat.get_rect(midbottom = (700, 750))
        text = self.font.render(self.convo, False, 'White')
        textRect = text.get_rect(topleft = (250, 550))
        self.screen.blit(chat, chatRect)
        self.screen.blit(text, textRect)
        self.screen.blit(self.image, (80, 640))

# a class for the board obstacle used            
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
        self.clicked = False
        if self.index == 1:
            self.initializePuzzle()
            self.trial = []
        self.passed = False
        self.filehandle = open("words.txt","r")
        self.word = choice(self.filehandle.readlines())

    # intializing the dictionary of the letters allowed 
    def initializePuzzle(self):
        self.puzzleDictionary = {}
        A = pygame.image.load("A.png").convert_alpha()
        A = pygame.transform.scale(A,(90,120))
        Arect = A.get_rect(midleft = (130, 700))
        Atemp = (130, 700)
        E = pygame.image.load("E.png").convert_alpha()
        E = pygame.transform.scale(E,(100,120))
        Erect = E.get_rect(midleft = Arect.midright)
        Etemp = Arect.midright
        I = pygame.image.load("I.png").convert_alpha()
        I = pygame.transform.scale(I,(100,120))
        Irect = I.get_rect(midleft = Erect.midright)
        self.Itemp = Erect.midright
        O = pygame.image.load("O.png").convert_alpha()
        O = pygame.transform.scale(O,(100,120))
        Orect = O.get_rect(midleft = Irect.midright)
        self.Otemp = Irect.midright
        P = pygame.image.load("P.png").convert_alpha()
        P = pygame.transform.scale(P,(100,120))
        Prect = P.get_rect(midleft = Orect.midright)
        self.Ptemp = Orect.midright
        F = pygame.image.load("F.png").convert_alpha()
        F = pygame.transform.scale(F,(100,120))
        Frect = F.get_rect(midleft = Prect.midright)
        self.Ftemp = Prect.midright
        G = pygame.image.load("G.png").convert_alpha()
        G = pygame.transform.scale(G,(100,120))
        Grect = G.get_rect(midleft = Frect.midright)
        self.Gtemp = Frect.midright
        H = pygame.image.load("HH.png").convert_alpha()
        H = pygame.transform.scale(H,(100,120))
        Hrect = H.get_rect(midleft = Grect.midright)
        self.Htemp = Grect.midright
        N = pygame.image.load("N.png").convert_alpha()
        N = pygame.transform.scale(N,(100,120))
        Nrect = N.get_rect(midleft = Hrect.midright)
        self.Ntemp = Hrect.midright
        R = pygame.image.load("R.png").convert_alpha()
        R = pygame.transform.scale(R,(100,120))
        Rrect = R.get_rect(midleft = Nrect.midright)
        self.Rtemp = Nrect.midright
        T = pygame.image.load("T.png").convert_alpha()
        T = pygame.transform.scale(T,(100,120))
        Trect = T.get_rect(midleft = Rrect.midright)
        self.Ttemp = Rrect.midright
        S = pygame.image.load("S.png").convert_alpha()
        S = pygame.transform.scale(S,(100,120))
        Srect = S.get_rect(midleft = Trect.midright)
        self.Stemp = Trect.midright
        self.puzzleDictionary['A'] = [A, Arect, Atemp]
        self.puzzleDictionary['E'] = [E, Erect, Etemp]
        self.puzzleDictionary['I'] = [I, Irect, self.Itemp]
        self.puzzleDictionary['O'] = [O, Orect, self.Otemp]
        self.puzzleDictionary['P'] = [P, Prect, self.Ptemp]
        self.puzzleDictionary['F'] = [F, Frect, self.Ftemp]
        self.puzzleDictionary['G'] = [G, Grect, self.Gtemp]
        self.puzzleDictionary['H'] = [H, Hrect, self.Htemp]
        self.puzzleDictionary['N'] = [N, Nrect, self.Ntemp]
        self.puzzleDictionary['R'] = [R, Rrect, self.Rtemp]
        self.puzzleDictionary['T'] = [T, Trect, self.Ttemp]
        self.puzzleDictionary['S'] = [S, Srect, self.Stemp]
        
    # checking if the player is within a certain distance of the board
    # and whether they want to interact with the board
    def interact(self, mouse):
        if abs(player.sprite.rect.center[0] - self.rect.center[0]) < 100:
            if not self.screenChange:
                text = self.font.render("press E", False, 'Black', 'White')
                textRect = text.get_rect(midbottom = (player.sprite.rect.midtop))
                screen.blit(text, textRect)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    self.screenChange = True
                    self.puzzle(mouse)

    # checking the mouse position 
    def mouse(self, rect):
        pos = pygame.mouse.get_pos()
        return rect.collidepoint(pos[0], pos[1])



    def puzzleSolve(self):
        right = self.word
        stored = []
        newstring = ""
        if len(self.trial) == 5:
            for counter in range(0,5):
                if right[counter].lower() == self.trial[counter].lower():
                    newstring = newstring + self.trial[counter].lower()
                else:
                    newstring = newstring + " "
            for counter in range(5):
                for x in range(5):
                    if self.trial[counter].lower() == right[x] and newstring[counter]==" " and newstring[x] == " ":
                        if stored.count(self.trial[counter].lower())< right.count(self.trial[counter].lower()):
                            if stored.count(self.trial[counter].lower()) !=1 and right.count(self.trial[counter].lower()) >= 1:
                                stored.append(self.trial[counter])
                            elif self.trial.count(self.trial[counter].lower()) == right.count(self.trial[counter].lower()):
                                stored.append(self.trial[counter])
            self.trial = []
            passes = True
            for i in range(5):
                if newstring[i] != right[i]:
                    passes = False
            if passes:
                convo = "WOO, you did it"
                self.passed = True
            else:
                convo = "these letters are in the correct spots: "+ newstring + " and these letters are not in the correct spots:" +"".join(stored)
        else:
            convo = None
        return convo

    # calls and updates the letters
    def puzzle(self, mouse):
        for i in self.puzzleDictionary:
            if self.mouse(self.puzzleDictionary[i][1]):
                if mouse and len(self.trial)!=5:
                    self.clicked = True
                    rect = self.puzzleDictionary[i][1]
                    if rect.y < 600 and self.trial.index(i) == (len(self.trial)-1):
                        self.puzzleDictionary[i][1].midleft = self.puzzleDictionary[i][2]
                        temp = self.trial.index(i)
                        self.trial.pop(temp)
                    elif rect.centery == 700:
                        rect.x = 150 + (len(self.trial)*250)
                        rect.y = 350
                        self.trial.append(i)

                    mouse = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.screenChange = False
            if len(self.trial) ==5:
                self.initializePuzzle()

    # calls all the functions that need to be checked and updated       
    def obstacleUpdate(self, mouse):
        if self.index == 1:
            self.interact(mouse)
            self.puzzle(mouse)
            
            
# player class       
class Character(pygame.sprite.Sprite):
    def __init__ (self, index):
        super().__init__()
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

    # dealing with the movement of the player
    
    def gravities(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.bottom >= self.bottom:
            self.gravity = -20
    # these two functions were adapted from https://www.youtube.com/watch?v=AY9MnQ4x3zk&ab_channel=ClearCode
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

# class for each screen that has basic functions 
class Screen():
    def __init__(self, pic, right = None, left = None, passes = True, obstacles = {}, people = {}, index = 0):
        self.pic = pic
        self.screen = pygame.display.set_mode((1400, 800))
        self.image = pygame.image.load(self.pic).convert_alpha()
        self.image = pygame.transform.scale(self.image, (1400, 800))
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
        self.clicked = False
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

    # calling and updating obstacles associated with that screen 
    def obstaclesCall(self, mouse):
        for i in self.obstacles:
            i.obstacleUpdate(mouse)
        for i in self.people:
            i.obstacleUpdate()
            
    # checking for any dialogue 
    def speakCall(self):
        for i in self.people:
            if i .speaking == True:
                i.printSpeak()
                self.speakChange = True
            else:
                self.speakChange = False

    # changing the screen based on what the player is interacting with    
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

    # calling and updating the whole screen associated with that screen           
    def update(self, mouse):
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
        self.obstaclesCall(mouse)
        self.speakCall()
        if self.index == 1:
            self.puzzleCall()
            for i in self.obstacles:
                if i.clicked:
                    mouse = False
                    i.clicked = False
        return mouse

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
pygame.display.set_icon(peng)

def playerCollide():
    if pygame.sprite.spritecollide(player.sprite, board, False):
        return True
    return False

def check(user):
    lines = printing()
    for counter in range(len(lines)):
        temp = lines[counter].split()
        if temp[0] == user:
            return True
    return False

def reset(index, game_active, mouse, escape, timer):
    index = 0
    player.sprite.rightreset = True
    game_active = False
    mouse = False
    escape = False
    timer = 0
    return index, game_active, mouse, escape, timer
    
def write(array):
    boardFile = open("board.txt","w")
    for i in array:
        boardFile.write("\n"+i)
    boardFile.close()
    
def edit(user, score):
    new = []
    lines = printing()
    for counter in range(len(lines)):
        temp = lines[counter].split()
        if temp[0] == user:
            temp[1] = str(score)
        new.append(" ".join(temp))
    return new

        
def printing():
    lines = []
    boardFile = open("board.txt","r")
    boardLine = boardFile.readline()
    temp = (176, 180, 207)
    screen.fill(temp)
    for boardLine in boardFile:
        lines.append(boardLine)
    boardFile.close()
    return lines

i = "igloo.jpg"
j = "ice.jpeg"
k = "for nwot.jpeg"
l = "iceback.webp"
m = "backs.jpeg"
array = cardInitialize()
cardArray = create(array)
board = Obstacle("boards.png", 700, 350, 1000, 600, 1)
laser = Obstacle("fishy.png", 0, 620, 40, 30, 3)
jPeople = {}
jObstacles = {}
jObstacles[board] = (board.image, board.rect, board)
bear = Others("bear.png", 200, 620,"trial.txt",  board, index = 1)

jPeople[bear] = (bear.image, bear.rect, bear)
screen1 = Screen(i, "arrow.png")
screen2 = Screen(j, "arrow.png", "otherarrow.png", False, jObstacles, jPeople, index = 1)
screen5 = Screened("poker.jpg", cardArray)
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

lines = printing()
end = pygame.transform.scale(pygame.image.load("ending.jpeg"), (1400, 800))
game_end = False
screen3 = World(world_data)
screens = [screen1, screen2, screen3, screen4, screen5]
index = 0
screen = screens[index]
clock = pygame.time.Clock()
font = pygame.font.Font("mario.ttf", 70)
fonts = pygame.font.Font("mario.ttf", 40)
newfont = pygame.font.Font("mario.ttf", 20)
otherfont = pygame.font.Font(None, 40)
player = pygame.sprite.GroupSingle()
player.add(Character(index))
game_active = False
startButton = Button("start.png", 700, 300, 220, 80, 270, 95)
loginButton = Button("login.png", 700, 400, 220, 80, 270, 95)
boardButton = Button("biard.png", 700, 500, 220, 80, 270, 95)
otherBoardButton = Button("biard.png", 700, 400, 220, 80, 270, 95)
helpButton = Button("help.png", 700, 600, 220, 80, 270, 95)
otherHelpButton = Button("help.png", 700, 400, 220, 80, 270, 95)
resumeButton = Button("resume.png", 700, 300, 220, 80, 270, 95)
exitButton = Button("exit.png", 700, 500, 220, 80, 270, 95)
backButton = Button("back.png", 100, 100, 120, 60, 170, 75)
saveButton = Button("save.png", 700, 400, 220, 80, 270, 95)
bg_img = pygame.image.load('sku.png')
bg_img = pygame.transform.scale(bg_img, (1400, 2000))
bgrect = bg_img.get_rect(center = (700, 400))
mouse, escape, horror, swap = False, False, False, False
back = pygame.transform.scale(pygame.image.load("temp.jpg"), (1400, 800))
startTimer = 4
pygame.mixer.init()
pygame.mixer.music.load("minecraft.mp3")
pygame.mixer.music.set_volume(0.4)
faces = ["erica.JPG", "sunaya.JPG", "enochi.JPG", "rainier.jpg"]
pygame.mixer.music.play(-1)

def mouseCollide(textRect):
    pos = pygame.mouse.get_pos()
    return textRect.collidepoint(pos[0], pos[1])
timer = -3
while True:
    temp = pygame.event.get()
    for event in temp:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type ==pygame.MOUSEBUTTONDOWN:
            mouse = True
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            escape = True
    
    if game_active and not horror and not game_end:
        if escape:
            temp = (176, 180, 207)
            screen.fill(temp)
            screen.blit(resumeButton.image, resumeButton.rect)
            screen.blit(otherHelpButton.image, otherHelpButton.rect)
            screen.blit(exitButton.image, exitButton.rect)
            resumeButton.update(mouse)
            otherHelpButton.update(mouse)
            exitButton.update(mouse)
            if resumeButton.collide() and mouse:
                escape = False
                mouse = False
            if otherHelpButton.active:
                screen.blit(back, (0,0))
                screen.blit(backButton.image, backButton.rect)
                backButton.update(mouse)
                if backButton.collide() and mouse:
                    otherHelpButton.active = False
                    mouse = False
            if exitButton.collide() and mouse:
                startButton.count = 0
                loginButton.count = 0
                boardButton.count = 0
                helpButton.count = 0
                index, game_active, mouse, escape, timer = reset(index, game_active, mouse, escape, timer)

        else:
            if index == 3:
                screen = screens[index]
                screen.fill((20, 36, 15))
                timers = font.render(str(int(timer)), False, 'White')
                screen.blit(timers, (700, 30))
                screen.update()
                screen.player.move = True
                if screen.sign() == "next":
                    text = fonts.render("next?", False, 'Black')
                    textRect = text.get_rect(midbottom = (screen.player.rect.midtop))
                    screen.blit(text, textRect)
                    if mouse and mouseCollide(textRect):
                        index = index + 1
                        player.sprite.rightreset = True
                        mouse = False
                elif screen.sign() == "back":
                    text = newfont.render("back?", False, 'Black')
                    textRect = text.get_rect(midbottom = (screen.player.rect.midtop))
                    screen.blit(text, textRect)
                    if mouseCollide(textRect) and mouse:
                        index = index - 1
                        player.sprite.leftreset = True
                        mouse = False
            elif index == 4:
                screen = screens[index]
                screen.blit(pygame.transform.scale(pygame.image.load("poker.jpg"),(1400, 800)), (0,0))
                timers = font.render(str(int(timer)), False, 'Black')
                screen.blit(timers, (700, 30))
                screen.run(cardArray)
                if screen.matched == 8:
                    player.draw(screen)
                    player.update()
                    text = fonts.render("stop?", False, 'Black')
                    textRect = text.get_rect(center = (1350, 560))
                    screen.blit(text, textRect)
                    if mouse and mouseCollide(textRect) and player.sprite.rect.colliderect(textRect):
                        game_end = True
                    
            elif index != 2:
                screen = screens[index]
                mouse = screen.update(mouse)
                timers = font.render(str(int(startTimer)), False, 'Black')
                screen.blit(timers, (700, 30))
                if startTimer <= 0:
                    mouse = screen.update(mouse)
                    timers = font.render(str(int(timer)), False, 'Black')
                    screen.blit(timers, (700, 30))
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
                        if mouse and mouseCollide(textRect):
                            index = index + 1
                            player.sprite.rightreset = True
                            mouse = False
                    elif screen.collide(player) and screen.toggleLeft:
                        text = fonts.render("back?", False, 'Black')
                        textRect = text.get_rect(center = (60, 560))
                        screen.blit(text, textRect)
                        if mouseCollide(textRect) and mouse:
                            index = index - 1
                            player.sprite.leftreset = True
                            mouse = False
                else:
                    startTimer -= (1/60)
                    
            else:
                screen.blit(bg_img, bgrect)
                screen = screens[index]
                screen.update()
                screen.reset()
                timers = font.render(str(int(timer)), False, 'Black')
                screen.blit(timers, (700, 30))
                if screen.collide(screen.lists):
                    text = newfont.render("back?", False, 'Black')
                    textRect = text.get_rect(midbottom = (screen.player.rect.midtop))
                    screen.blit(text, textRect)
                    if mouseCollide(textRect) and mouse:
                        index = index - 1
                        player.sprite.leftreset = True
                        mouse = False
                if screen.collide(screen.listss):
                    text = fonts.render("next?", False, 'Black')
                    textRect = text.get_rect(midbottom = (screen.player.rect.midtop))
                    screen.blit(text, textRect)
                    if mouse and mouseCollide(textRect):
                        index = index + 1
                        player.sprite.rightreset = True
                        mouse = False
                if screen.collide(screen.coins):
                    coins += 1
            timer = float(timer) +(1/60)
    elif horror:
        # horror aspect
        screened = pygame.display.set_mode((1400,800))
        screen.fill((0,0,0))
        horrorPic = pygame.image.load("scary.webp")
        screen.blit(pygame.transform.scale(horrorPic, (1400, 800)), (0,0))
        pygame.display.update()
        screen.fill((0,0,0))

    elif game_end:
        # end screen
        screen.blit(end, (0,0))
        titleText = font.render("The End", False, 'White')
        titleTextRect = titleText.get_rect(center = (700, 100))
        screen.blit(titleText, titleTextRect)
        screen.blit(saveButton.image, saveButton.rect)
        screen.blit(exitButton.image, exitButton.rect)
        saveButton.update(mouse)
        exitButton.update(mouse)
        if exitButton.collide() and mouse:
            startButton.count = 0
            loginButton.count = 0
            boardButton.count = 0
            helpButton.count = 0
            index, game_active, mouse, escape, timer = reset(index, game_active, mouse, escape, timer)
            game_end = False
        if saveButton.active and loginButton.loggedIn:
            checking = check(user)
            if not checking:
                boardFile = open("board.txt","a")
                boardFile.write("\n" + user + "  " + str(int(timer)))
                boardFile.close()
                save()
                saveButton.active = False
            else:
                lines = edit(user, str(int(timer)))
                write(lines)
                save()
                saveButton.active = False
            mouse = False
        elif saveButton.active and not loginButton.loggedIn:
            please()
            saveButton.active = False
    else:
        # start screen
        temp = pygame.transform.scale(pygame.image.load("maybee.jpeg"), (1400, 800))
        screen.blit(temp, (0,0))
        titleText = font.render("Articventure", False, 'Black')
        titleTextRect = titleText.get_rect(center = (700, 100))
        screen.blit(titleText, titleTextRect)
        screen.blit(startButton.image, startButton.rect)
        screen.blit(loginButton.image, loginButton.rect)
        screen.blit(boardButton.image, boardButton.rect)
        screen.blit(helpButton.image, helpButton.rect)
        startButton.update(mouse)
        loginButton.update(mouse)
        boardButton.update(mouse)
        helpButton.update(mouse)
        if startButton.count > 15 or loginButton.count > 15 or boardButton.count > 15 or \
           helpButton.count > 15:
            swap = True
        if startButton.collide() and mouse and not swap:
            game_active = True
            mouse = False
        elif startButton.collide() and mouse and swap:
            horror = True
        if not loginButton.loggedIn and loginButton.collide() and mouse and not swap and not helpButton.active and not boardButton.active:
            user = begin()
            loginButton.loggedIn = True
            mouse = False
        elif loginButton.collide() and mouse and swap:
            horror = True
        if helpButton.active and not swap:
            screen.blit(back, (0,0))
            screen.blit(backButton.image, backButton.rect)
            backButton.update(mouse)
            if backButton.collide() and mouse:
                helpButton.active = False
                mouse = False
        elif helpButton.active and swap:
            horror= True
        if boardButton.active and loginButton.loggedIn and mouse:
            temp = (176, 180, 207)
            screen.fill(temp)
            for i in range(len(lines)):
                screen.blit(otherfont.render(lines[i], False, 'Black'), (700, (i+3)*50))
            screen.blit(backButton.image, backButton.rect)
            backButton.update(mouse)
            if backButton.collide() and mouse:
                boardButton.active = False
                mouse = False
        elif boardButton.active and not loginButton.loggedIn and not swap:
            please()
            boardButton.active = False
            mouse = False
        elif boardButton.active and swap:
            horror = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_active = True

    clock.tick(60)
    pygame.display.update()
