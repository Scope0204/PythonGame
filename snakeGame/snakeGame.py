import pygame
import sys #창 종료 , sys : 파이썬 인터프리터가 제공하는 변수와 함수를 사용할 수 있게 해 줌
import time # 게임 시간
import random # random : 무작위 선택

# from 모듈 import 함수
from pygame.locals  import *

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
    # 뱀 설정
    def __init__(self):
        self.create() # 생성
        self.color = GREEN # 뱀 색깔

    # 생성
    def create(self):
        self.length = 2 # 뱀의 길이
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT/2))] # 뱀 시작 위치 : 화면 중앙
        self.direction = random.choice([UP,DOWN,LEFT,RIGHT]) # choice() : 아무 원소나 하나 뽑아줌

    def control(self, xy):
        #반대 방향으로 조작되는 것을 막아야함
        if(xy[0] *  -1 , xy[1] * -1) == self.direction:
            return # 변화를 주지 않는다
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
        if new in self.positions[2:]: # 뱀이 자신을 먹을 경우
            self.create() # 새로 만들어 줌
        else:
            self.positions.insert(0,new) # 새로 만든애를 insert 시켜줌
            if len(self.positions) > self.length: # 실제 길이보다 클 경우에
                self.positions.pop() # 꺼내줌

    # 먹을경우 하나 증가
    def eat(self):
        self.length += 1
    # 뱀을 그려주는 역할
    def draw(self, surface): # surface : 화면에 표시되는 네
        for p in self.positions:
            draw_object(surface,self.color,p)

#먹이
class Feed(object):
    def __init__(self):
        self.position = (0,0) # positions 가 아닌것에 주의(1칸짜리니깐)
        self.color = ORANGE
        self.create()
    # 생성
    def create(self):
        self.position = (random.randint(0, GRID_SIZE -1) * GRID_SIZE , random.randint(0, GRID_HEIGHT -1) * GRID_SIZE)
    # 먹이를 그려주는 역할
    def draw(self,surface):
        draw_object(surface,self.color,self.position)

# 오브젝트를 그리는 역할
def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface,color,r)

# 먹이를 먹은 경우
def check_eat(python, feed):
    # 뱀의 머리 위치 == 먹이 위치 -> 먹었다
    if python.positions[0] == feed.position:
        python.eat() # 먹으면 길이 1 증가
        feed.create() # 먹이 재생성

# 정보 제공
def show_info(length,speed,surface):
    font = pygame.font.Font(None, 34)
    text = font.render("length: " + str(length)+ "      Speed: " + str(round(speed,2)), 1, GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text,pos)

# java의 main과 같은 역할
if __name__ == '__main__':  # 내 코드가 메인 함수로 실행되는가 import 되어 실행되는가를 판단할 수 있음

    # 만든 클래스를 사용하는 객체 생성
    python = Python()
    feed = Feed()

    # 초기화 명령
    pygame.init()
    # 게임 화면. set_mode() : 크기 지정
    window = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT) , 0 , 32)
    # 캡션, 위에 윈도우 이름 있는곳
    pygame.display.set_caption('python game')
    #
    surface = pygame.Surface(window.get_size())
    surface = surface.convert() # convert(데이터형식[(길이)] , 유효한식[,스타일]) : 형변환
    surface.fill(WHITE)
    # 게임 시간
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,40)
    # 비트 연산을 통한 화면 구성
    window.blit(surface,(0,0))

    # 키 조작
    while True:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT: # 조작 전에 끝내면
                pygame.quit() # 나가주고
                sys.exit() # sys 꺼줌
            elif event.type == KEYDOWN: # KETDOWN = 키보드를 눌렀을때
                if event.key == K_UP: # 위
                    python.control(UP)
                if event.key == K_DOWN: # 아래
                    python.control(DOWN)
                if event.key == K_LEFT: # 왼쪽
                    python.control(LEFT)
                if event.key == K_RIGHT: # 오른쪽
                    python.control(RIGHT)

        surface.fill(WHITE) # 게임 화면을 하양으로 칠해줌
        python.move()
        check_eat(python,feed) # 먹이를 먹을 경우
        speed = (FPS + python.length) / 2 # 난이도를 위해 먹이를 먹을 경우 스피드 증가
        show_info(python.length , speed, surface)
        python.draw(surface) # 뱀 그려주는 거
        feed.draw(surface) # 먹이 그려주는 거
        window.blit(surface, (0,0)) # window에 뿌려줌
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed) # 초당 speed번의 화면을 출력해 주겠다.
