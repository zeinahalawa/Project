import pygame
pygame.init()
screen = pygame.display.set_mode((1400, 790))
index = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            index += 1
            print(index)
    pygame.display.update()
