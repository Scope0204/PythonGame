import pygame
import sys
from time import sleep

padWidth = 400
padHeight = 640

def drawObject(obj,x,y):
    global gamePad
    gamePad.blit(obj, (x,y))

def initGame():
    global gamePad, clock, background, fighter
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('pyShooting') # 게임 창 제목
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    clock = pygame.time.Clock()

#게임이 실행되는 함수
def runGame():
    global gamePad, clock, background,fighter

    #전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    #전투기 초기 위치(x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

        drawObject(background,0,0)

        drawObject(fighter,x,y)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

initGame()
runGame()
