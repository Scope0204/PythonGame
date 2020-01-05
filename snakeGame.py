import pygame
import sys #창 종료
import time # 게임 시간
import random

from pygame.locals import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
#창을 하나의 픽셀 단위로 쓰기엔 너무 작기떄문에 그리드로 크게 나눠줌
#한 칸을 그리드로 20으로 잡음
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE


WHITE = (255,255,255)
GREEN = ( 0 , 50 , 0)
ORANGE = (250,150,0)
GRAY = (100,100,100)

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

FPS = 10

class Python(object):
    def __init__(self):
        self.create()
        self.color = GREEN

    def create(self):
        self.length = 2 # 뱀의 길이
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT/2))] # 화면 중앙
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT])

    def control(self, xy):
        #반대 방향으로 조작되는 것을 막아야함
        if(xy[0] *  -1 , xy[1] * -1) == self.direction:
            return
        #정상 이동시에는 좌표값을 이동시켜 줌
        else:
            self.direction = xy

    # 이동
    def move(self):
        # positions[0] : 뱀의 머리
        cur = self.positions[0]
        x , y = self.direction
        #뱀이 계속 움직이는 것을 표현 -> 머리 이후 부분을 그려주는 부분 = new
        new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH), (cur[1] + ( y * GRID_SIZE )) % WINDOW_HEIGHT)
        if new in self.positions[2:]:
            self.create()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # 먹을경우 하나 증가
    def eat(self):
        self.length += 1

    def draw(self, surface):
        for p in self.positions:
            draw_object(surface,self.color,p)

#먹이
class Feed(object):
    def __init__(self):
        self.position = (0,0)
        self.color = ORANGE
        self.create()

    def create(self):
        self.position = (random.randint(0, GRID_SIZE -1) * GRID_SIZE , random.randint(0, GRID_HEIGHT -1) * GRID_SIZE)

    def draw(self,surface):
        draw_object(surface,self.color,self.position)

def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface,color,r)

# 먹이를 먹은 경우
def check_eat(python, feed):
    # 뱀의 머리 위치 == 먹이 위치
    if python.positions[0] == feed.position:
        python.eat()
        feed.create()

# 정보 제공
def show_info(length,speed,surface):
    font = pygame.font.Font(None, 34)
    text = font.render("length: " + str(length)+ "      Speed: " + str(round(speed,2)), 1, GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text,pos)

if __name__ == '__main__':
    python = Python()
    feed = Feed()

    # 초기화 명령
    pygame.init()
    # 게임 화면
    window = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT) , 0 , 32)
    # 캡션, 위에 윈도우 이름 있는곳
    pygame.display.set_caption('python game')
    #
    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    surface.fill(WHITE)
    # 게임 시간
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,40)
    # 비트 연산을 통한 화면 구성
    window.blit(surface,(0,0))


    while True:

        # 키 조작
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.control(UP)
                if event.key == K_DOWN:
                    python.control(DOWN)
                if event.key == K_LEFT:
                    python.control(LEFT)
                if event.key == K_RIGHT:
                    python.control(RIGHT)

        surface.fill(WHITE)
        python.move()
        check_eat(python,feed)
        speed = (FPS + python.length) / 2
        show_info(python.length , speed, surface)
        python.draw(surface)
        feed.draw(surface)
        window.blit(surface, (0,0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed)
