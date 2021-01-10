import pygame
from pygame.locals import *
import os
import random
import sys
import math      
pygame.init()
W=400
H=400
k=0
win=pygame.display.set_mode((W,H))
pygame.display.set_caption("lets rock")
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
bg = pygame.image.load('bg.png').convert()
 
bgk1 = 0
bgk2 = bg.get_width()
char = pygame.image.load('standing.png')

         
clock = pygame.time.Clock()
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.right = False
        self.left = False
        self.falling=False
        self.walkCount = 0
        self.jumpCount = 10
        self.jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,
            -2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
        self.jump = [pygame.image.load((str(x) + '.png')) for x in range(1,8)]
        self.fall = pygame.image.load('0.png')
 

        
    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))

    
        elif self.isJump:
            self.y -= self.jumpList[self.jumpCount] * 1.6
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.isJump=False
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10) 
 
        else:
             if self.walkCount + 1 >= 36:
                self.walkCount = 0
             win.blit(walkRight[self.walkCount//4], (self.x,self.y))
             self.walkCount +=1
             self.hitbox = (self.x+ 4,self.y+9,self.width-24,self.height-13)
        pygame.draw.rect(win, (255,0,0),self.hitbox, 2) 
 
    

class saw(object):
    rotate = [pygame.image.load('SAW0.PNG'),pygame.image.load('SAW1.PNG')
              ,pygame.image.load('SAW2.PNG'),pygame.image.load('SAW3.PNG')]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4
    def draw(self,win):
        self.hitbox = (self.x + 4, self.y + 5, self.width - 7, self.height - 5) 
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2],
        (58,58)), (self.x,self.y))
        self.rotateCount += 1
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False



class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
class enemy(object):
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'),
    pygame.image.load('L3E.png'), pygame.image.load('L4E.png'),
    pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'),
    pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'),
    pygame.image.load('L11E.png')]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel=3
        self.left=False
        self.right=False
        self.health=10
        self.visible=True
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)

 
 
    def draw(self,win):
        if self.visible:
            self.hitbox = (self.x + 20, self.y + 5, self.width - 25, self.height - 5)
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
                win.blit(pygame.transform.scale(self.walkLeft[self.walkCount//3],
                (58,58)), (self.x,self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        else:
            k=1
        

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

 

def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])
    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()
        return score
    return last
def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                man.falling = False
                man.sliding = False
                man.jumpin = False
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(0,0,0))
        currentScore = largeFont.render('Score: '+ str(score),1,(0,0,0))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0





    
obstacles = []
def redrawGameWindow():
    win.blit(bg,(bgk1, 0))
    win.blit(bg,(bgk2, 0))
    largeFont = pygame.font.SysFont('comicsans', 30,True)
    text = largeFont.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (700, 10))
     
    
    
    man.draw(win)
 
    for obstacle in obstacles:
        obstacle.draw(win)
        
    for bullet in bullets:
        bullet.draw(win)
    
    
     
    pygame.display.update()

speed=30
run=True
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+3,random.randrange(2000,4000))
shootLoop=0
goblin = enemy(100, 410, 58, 58)

#mainloop
man = player(50,305, 64,64)
run = True
bullets=[]
score=0
pause = 0
fallSpeed = 0
while run:
    clock.tick(speed)
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()
        
    score = speed//10 - 3

    for obstacle in obstacles:
        if obstacle.collide(man.hitbox):
            man.falling = True
            
            if pause == 0:
                pause = 1
                fallSpeed = speed
    bgk1=bgk1-1.4
    bgk2=bgk2-1.4
    if(bgk1<bg.get_width()*-1):
        bgk1=bg.get_width()
    if(bgk2<bg.get_width()*-1):
        bgk2=bg.get_width()
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == USEREVENT+1:
            speed=speed+1

        if event.type == USEREVENT+3:
            r=random.randrange(0,2)
            if r==0:
                obstacles.append(saw(800, 310, 58, 58))
            elif r==1 and k==0:
                obstacles.append(enemy(800, 310,58,58))
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3]and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x -bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    score=score+1
                    bullets.pop(bullets.index(bullet))
            if bullet.x < 400 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

                
    keys = pygame.key.get_pressed()


    if keys[pygame.K_RIGHT] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 6:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))
        shootLoop=1
    if keys[pygame.K_SPACE]:
        if not(man.isJump):
            man.isJump = True
    for obstacle in obstacles: 
     obstacle.x -= 1.4
     if obstacle.x < obstacle.width * -1:
          obstacles.pop(obstacles.index(obstacle))



         
    redrawGameWindow()
pygame.quit()

    
        




