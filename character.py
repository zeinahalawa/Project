import pygame

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
        self.bottom = 720
        self.image = pygame.transform.scale(self.image,(100,110))
        self.rect = self.image.get_rect(midbottom = (100, self.bottom))
        self.gravity = 0
        self.rightreset = False
        self.leftreset = False

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
        print("hi")
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
