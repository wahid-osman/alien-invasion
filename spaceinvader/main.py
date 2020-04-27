import pygame
import random
import math

"""initialize the pygame"""
pygame.init ()

"""create the screen"""
screen = pygame.display.set_mode ((800, 600))

#Background image
background = pygame.image.load('background-3.jpg')

#Caption and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('playerimg.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemies
#Ready state means you cant see the bullet on the screen
#Fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_change = 0
bulletY_change = 10
bullet_state = 'ready'

#Bullet
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    # Game over
    if enemyY[i] > 440:
        for j in range(num_of_enemies):
            enemyY[j] = 2000
            game_over_text()
            break

    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = font.render('GAME OVER ', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:
    #RGB --- Red, Green & Blue
    screen.fill((0, 0, 0))
    #Background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key stroke is pressed check wether ots right or left
        if event.type == pygame.KEYDOWN:
            print('A key stroke has been pressed')
            if event.key == pygame.K_LEFT:
                playerX_change = -4
                print('Left arrow is pressed')
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

#checking for boundaries of space ship so that it does not go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

#enemy movement
for i in range(num_of_enemies):
    enemyX[i]+= enemyX_change[i]
    if enemyX[i] <= 0:
        enemyX_change[i] = 3
        enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 736:
        enemyX_change[i] = -3
        enemyY[i] += enemyY_change[i]
    #Collision
    collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value +=1
        enemyX[i]= random.randint(0, 735)
        enemyY[i]= random.randint(50, 150)
    enemy(enemyX[i], enemyY[i], i)

#Bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire' :
        fire_bullet(bulletX, bulletY)
        bulletY -=bulletY_change


    player(playerX, playerY)

    show_score(textX, textX)

    pygame.display.update()
