import pygame
import sys
from time import sleep # from 모듈 import 함수 . sleep() : 일시정지함수
import random

# 게임 크기 설정
padWidth = 400
padHeight = 640
rockImage = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png',
             'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png',
             'rock11.png','rock12.png','rock13.png','rock14.png','rock15.png',
             'rock16.png','rock17.png','rock18.png','rock19.png','rock20.png',
             'rock21.png','rock22.png','rock23.png','rock24.png','rock25.png',
             'rock26.png','rock27.png','rock28.png','rock29.png','rock30.png']
explosionSound = ['explosion01.wav', 'explosion02.wav' , 'explosion03.wav' ,'explosion04.wav']

def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('파괴한 운석 수: ' + str(count), True, (255,255,255))
    gamePad.blit(text , (10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('지나친 운석 수: ' + str(count), True, (255,0,0))
    gamePad.blit(text , (240,0))

def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('NanumGothic.ttf',60)
    text = textfont.render(text , True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2 , padHeight/2) # 중앙
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop() # 배경 음악 정지
    gameoverSound.play() # 게임 오버 사운드 재생
    sleep(2) # 2초 쉬고
    pygame.mixer.music.play(-1) # 배경 음악 재생
    runGame() # 게임 시작

# 전투기가 충돌 났을 때
def crash():
    global gamePad
    writeMessage('전투기 파괴')

# 게임 오버 메시지 보이기
def gameOver():
    global gamePad
    writeMessage('게임 오버')

def drawObject(obj,x,y):
    global gamePad
    gamePad.blit(obj, (x,y)) # bliting = painting . 그려주는 역할이라고 보면 됨

def initGame():
    global gamePad, clock, background, fighter, missile,explosion,missileSound, gameoverSound # 선언. 글로벌 변수
    pygame.init() # pygame 라이브러리 초기화 : 안하면 일부 기능이 정상 동작하지 않을 수 있다
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('pyShooting') # 게임 창 제목
    background = pygame.image.load('background.png') # 배경 그림
    fighter = pygame.image.load('fighter.png') # 전투기 그림
    missile = pygame.image.load('missile.png') # 미사일 그림
    explosion = pygame.image.load('explosion.png') # 폭발 그림
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('missile.wav')
    gameoverSound = pygame.mixer.Sound('gameover.wav')
    clock = pygame.time.Clock()

#게임이 실행되는 함수
def runGame():
    global gamePad, clock, background,fighter,missile,explosion

    #전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    #전투기 초기 위치(x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    # 미사일 좌표 리스트
    missileXY = [] # 미사일을 여러개 가져오기 때문에

    #운석
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # 운석 크기가 다 다르기 때문에 가져온 그림의 실제 크기를 가지고 폭과 너비를 가져옴
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    rockX = random.randrange(0 , padWidth - rockWidth) # 운석의 x좌표만 랜덤으로 지정해줌
    rockY = 0
    rockSpeed = 2 # 운석이 떨어지는 스피드

    # 전추기 미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0


    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]: # 키를 눌렀을 때
                if event.key == pygame.K_LEFT:
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5
                # 미사일 발사
                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth/2 # 미사일이 현재 비행기의 중간쯤 나가도록 설정
                    missileY = y - fighterHeight # 전체 y 좌표 - 비행기 크기
                    missileXY.append([missileX , missileY])

            if event.type in [pygame.KEYUP]: # 키를 땔 때
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0


        # 배경 화면 그리기
        drawObject(background,0,0)

        # 전투기 위치 재조정
        x +=  fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth # 게임화면 끝까지 오른쪽으로 갔을 때

        # 전투기가 운석과 충돌 했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()

        # 전투기 그리기
        drawObject(fighter,x,y)

        if len(missileXY)!=0:
            for i, bxy in enumerate(missileXY): # enumerate(리스트/튜플/문자열) : 인덱스 값을 포함하는 enumerate 객체를 돌려준다
                bxy[1] -= 10 # 미사일이 위로 발사되기 때문에 ( = y는 -10씩 이동한다) 미사일이 빠르게 이동되는 형태로 만듬
                missileXY[i][1] = bxy[1] # -10 만큼 바뀐값이 XY에 할당

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth: # 미사일과 돌과 겹칠경우
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                #미사일이 화면밖으로 나간 경우
                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY)!= 0:
            for bx, by in missileXY:
                drawObject(missile,bx,by)

        writeScore(shotCount)

        rockY += rockSpeed

        if rockY > padHeight: #운석이 화면사이즈보다 더 많이 떨어지면
            # 다시 새로운 운석을 선택하게 함
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size # 운석 크기가 다 다르기 때문에 가져온 그림의 실제 크기를 가지고 폭과 너비를 가져옴
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0 , padWidth - rockWidth) # 운석의 x좌표만 랜덤으로 지정해줌
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            gameOver()

        writePassed(rockPassed)

        if isShot: # True가 되는 경우 = 미사일로 맞춘 경우
            drawObject(explosion,rockX,rockY) # 다시 그려줌
            destroySound.play()

            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size # 운석 크기가 다 다르기 때문에 가져온 그림의 실제 크기를 가지고 폭과 너비를 가져옴
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0 , padWidth - rockWidth) # 운석의 x좌표만 랜덤으로 지정해줌
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False # 다시 False로 바꿔줌

            rockSpeed += 0.5 # 속도를 올림
            if rockSpeed >= 10:
                rockSpeed = 10 # 최대치 설정

        drawObject(rock, rockX , rockY)
        pygame.display.update() # 게임 화면을 다시 그림

        clock.tick(60)

    pygame.quit()

initGame()
runGame()
