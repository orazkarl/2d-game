import pygame
import random
import math
from os import path
import time


pygame.init()


# Creating multiple colors just in case if we use them in the code
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Загрузка музыки и звуковых эффектов
shoot = pygame.mixer.Sound('shoot.wav')
hit = pygame.mixer.Sound('hit.wav')
deathPlayer = pygame.mixer.Sound('death.wav')
defeat = pygame.mixer.Sound('defeat.wav')
music = pygame.mixer.music.load("background-music.mp3")
pygame.mixer.music.play(-1)

# Create the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600 
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
background = pygame.image.load('background_image.jpg')

# Title of the game
pygame.display.set_caption("Pygame Assessment 2")

level = 1
# Main player and starting position
R1 = pygame.image.load('R1.png')
L1 = pygame.image.load('L1.png')
playerImage = R1
# Initial positioning of the main character (100,300)
locationX = 100
locationY = 300
xChange = 0
yChange = 0
# Параметры героя
playerHealth = 100
attackPlayer = 50
speedPlayer = 5
lifePlayer = 3

font = pygame.font.Font(None, 36)

# Сортировка 1-го элемента. Нужен для сортировки в таблице рекордов
def sortFirst(val): 
    return val[0]  
# Таймер. Запускается когда прошел уровень или зашел первый раз в игру
def timer():
    counter, text = 3, '3'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 300)
    font = pygame.font.SysFont('arial', 30)

    while True:
        
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT: 
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'start'
            if e.type == pygame.QUIT: break
        if counter <=0:
            print('start')
        else:
            screen.fill(GRAY)
            screen.blit(background, (0, 0))
            screen.blit(font.render(text, True, (255, 0, 0)), (32, 48))
            pygame.display.flip()
            continue
        break
    
    return    

# Создание врага
# Параметры врага
# Количество врагов увеличивается на 1 с каждым уровнем
ImageOfEnemy=list()
locationXenemy=list()
locationYenemy=list()
xChangeEnemy=list()
yChangeEnemy=list()
deathHealth=list()

speedEnemy=1
enemy_alive = list()
countDeathEnemy = 0     
# Enemy and its starting position (with random module using random.randint())
def createEnemy(level):            
    for i in range(0, level):
        ImageOfEnemy.insert(i, pygame.image.load('death.png'))
        locationXenemy.insert(i,random.randint(500, 736))
        locationYenemy.insert(i,random.randint(0, 536))
        xChangeEnemy.insert(i,0)
        yChangeEnemy.insert(i,0)
        deathHealth.insert(i,100)
        speedEnemy=level
        enemy_alive.insert(i, True)
createEnemy(level)

# Shooting item by the main character
itemImage = pygame.image.load('elixir.png')
itemX = locationX  # Same location as the main character
itemY = locationY
itemChangeX = 40
itemChangeY = 0

itemXL = locationX  # Same location as the main character
itemYL = locationY
shootingR = False
shootingL = False
direction = 1
player_alive = True


score = 0
#distance_between_enemy_and_item = math.sqrt(math.pow(locationXenemy - itemX, 2) + math.pow(locationYenemy - itemY, 2))
#distance_main_and_enemy = math.sqrt(math.pow(locationX - locationXenemy, 2) + math.pow(locationY - locationYenemy,2))
RunningTheGame = False
HighScores = False
while True:
    #Меню
    screen.fill(GRAY)
    screen.blit(background, (0, 0)) 
    def draw_text(surface, text, size, x, y, color):
        '''draw text to screen'''
        font = pygame.font.Font(pygame.font.match_font('arial'), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
    arrow_keys = pygame.image.load(path.join( 'arrowkeys.png')).convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (150, 85))
    spacebar = pygame.image.load(path.join( 'spacebar.png')).convert_alpha()
    spacebar = pygame.transform.scale(spacebar, (150, 50))
    
    screen.blit(arrow_keys, (400, 350))
    screen.blit(spacebar, (400, 450))
    draw_text(screen, "PRESS [ENTER] TO BEGIN", 35, WINDOWWIDTH/2, 200, WHITE)
    draw_text(screen, "PRESS [R] TO SHOW HIGHSCORES", 35, WINDOWWIDTH/2, 250, WHITE)
    draw_text(screen, "PRESS [Q] TO QUIT", 35, WINDOWWIDTH/2, 300, WHITE)
    
    draw_text(screen, "MOVE:", 35, 300, 370, WHITE)
    draw_text(screen, "SHOOT:", 35, 300, 455, WHITE)

    pygame.display.flip()
    inMenu = True
    while inMenu:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                timer()                
                RunningTheGame = True
                inMenu = False
                break
            elif event.key == pygame.K_r:
                HighScores = True
                inMenu = False
                
            elif event.key == pygame.K_q:
                pygame.quit()
            
        elif event.type == pygame.QUIT:
            pygame.quit()
            
    # Таблица рекордов
    while HighScores:
        screen.blit(background, (0, 0))  
        draw_text(screen, "HIGHSCORES", 35, WINDOWWIDTH/2, 10, WHITE)
        file = "highscore.txt"
        highscores = []
        # С файла считается данные по линию
        with open(file, "r") as f:
            data = f.readlines() 
        # В стороке записано имя и счет. Здесь из разделять и делает конверт счет из str в int`    
        for i in range(len(data)):
            item = data[i]
            l = tuple()
            l = item.split(' ')
            l = l[:-1]
            l[0] = int(l[0])
            highscores.append(l)
        # Делает сортировку    
        highscores.sort(key = sortFirst, reverse = True)    
        highscores = highscores[:10]
        for i in range(len(highscores)):
            draw_text(screen, str(highscores[i][1]), 35, 250, 100+i*50, WHITE)
            draw_text(screen, str(highscores[i][0]), 35, 550, 100+i*50, WHITE)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                HighScores = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    HighScores = False
                    inMenu = True
                if event.key == pygame.K_ESCAPE:
                    HighScores = False
                    inMenu = True            
                    


        pygame.display.flip()    
        
        
        
    
    # Loop to keep the window opened
    # Everything what is happening while the window is opened is inside of this loop 
    # Сама игра
    while RunningTheGame:
        
        draw_text(screen, "LIFE OF PLAYER:", 20, 85, 0, WHITE)
        draw_text(screen, str(lifePlayer), 20, 180, 0, WHITE)
        draw_text(screen, "HEALTH OF PLAYER:", 20, 100, 30, WHITE)
        draw_text(screen, str(playerHealth), 20, 230, 30, WHITE)
        draw_text(screen, "SCORE:", 20, 700, 0, WHITE)
        draw_text(screen, str(score), 20, 770, 0, WHITE)
        draw_text(screen, "LEVEL:", 30, 400, 0, WHITE)
        draw_text(screen, str(level), 30, 480, 0, WHITE)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            # Adding the arrows control to the character
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xChange = -speedPlayer
                    direction = -1
                    playerImage = L1
                if event.key == pygame.K_RIGHT:
                    xChange = +speedPlayer
                    direction = 1
                    playerImage = R1
                if event.key == pygame.K_DOWN:
                    yChange = +speedPlayer
                if event.key == pygame.K_UP:
                    yChange = -speedPlayer
                if event.key == pygame.K_SPACE:
                    
                    if playerImage == R1:
                        if shootingR == False:
                            itemX = locationX
                            itemY = locationY
                            itemDirection = direction
                            shootingR = True
                    elif playerImage == L1:   
                        if shootingL == False:
                            itemXL = locationX
                            itemYL = locationY
                            itemDirection = direction
                            
                            shootingL = True
                        
                    #shootSound()
                    shoot.play()
                if event.key == pygame.K_q:
                    RunningTheGame = False
                    inMenu = True
                if event.key == pygame.K_ESCAPE:
                    RunningTheGame = False
                    inMenu = True            
                    


                    #distance_between_enemy_and_item = math.sqrt(math.pow(locationXenemy - itemX, 2) + math.pow(locationYenemy - itemY, 2))
                    #print(distance_between_enemy_and_item)




            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xChange = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    yChange = 0

        #distance_between_enemy_and_item = math.sqrt(math.pow(locationXenemy - itemX, 2) + math.pow(locationYenemy - itemY, 2))
        #print(distance_between_enemy_and_item)

        screen.fill(GRAY)
        screen.blit(background, (0, 0))  # background_image was added

        # Creating boundaries so the main character doesn't go beyond our window
        # Since our icon is 64 pixels, on the right the location on the x-axis is 736, not 800; 536 for y-axis
        locationX += xChange
        locationY += yChange
        if locationX <= 0:
            locationX = 0
        elif locationX >= 736:
            locationX = 736
        if locationY <= 0:
            locationY = 0
        elif locationY >= 536:
            locationY = 536

        # This if statements make the enemy follow the main character
        
        
        for i in range(0,len(locationXenemy)):
            if locationX >= locationXenemy[i]:
                xChangeEnemy[i] = +speedEnemy
            if locationX <= locationXenemy[i]:
                xChangeEnemy[i] = -speedEnemy
            if locationY >= locationYenemy[i]:
                yChangeEnemy[i] = +speedEnemy
            if locationY <= locationYenemy[i]:
                yChangeEnemy[i] = -speedEnemy
        # For the obstacle(death) and movement
            locationXenemy[i] += xChangeEnemy[i]
            locationYenemy[i] += yChangeEnemy[i]

        screen.blit(playerImage, (locationX, locationY))
        # Убирает врага из экрана который умер
        for i in range(0, len(deathHealth)):            
            if deathHealth[i] == 0:
                enemy_alive[i] = False
            if enemy_alive[i]:
                screen.blit(ImageOfEnemy[i], (locationXenemy[i], locationYenemy[i]))
            elif enemy_alive[i] == False:                
                screen.blit(ImageOfEnemy[i], (800, 800))
            
                
                
        if shootingR:
            screen.blit(itemImage, (itemX, itemY))
            if 0 <= itemX <= 736:
                itemX = itemX + itemChangeX
            else:
                itemX = locationX
                shootingR = False
            # Нанесет удар врагу при столкновения с огнем
            for i in range(0, len(locationXenemy)):                
                
                if -15<=(locationXenemy[i]-itemX)<=15 and -50<=(locationYenemy[i]-itemY)<=50:
                    if enemy_alive[i] == True:
                        deathHealth[i] = deathHealth[i] - attackPlayer
                        shootingR = False
                    # Если враг умер то добавляется 1 очко и считает количество мертвых врагом в этом уровне
                        if deathHealth[i] == 0:
                            score = score + 1
                            countDeathEnemy = countDeathEnemy + 1
        if shootingL:
            screen.blit(itemImage, (itemXL, itemYL))
            if 0 <= itemXL <= 736:
                itemXL = itemXL - itemChangeX
                
            else:
                itemXL = locationX
                shootingL = False
            # Нанесет удар врагу при столкновения с огнем
            for i in range(0, len(locationXenemy)):                
                if -15<=(locationXenemy[i]-itemXL)<=15 and -50<=(locationYenemy[i]-itemYL)<=50:
                    if enemy_alive[i] == True:
                        deathHealth[i] = deathHealth[i] - attackPlayer
                        shootingL = False
                        # Если враг умер то добавляется 1 очко и считает количество мертвых врагом в этом уровне
                        if deathHealth[i] == 0:
                            score = score + 1
                            countDeathEnemy = countDeathEnemy + 1
        differencePlayerAndEnemyX = list()
        differencePlayerAndEnemyY = list()
        #print(locationXenemy)
        for i in range(0, len(locationXenemy)):                                
            differencePlayerAndEnemyX.insert(i, locationXenemy[i]-locationX)
            differencePlayerAndEnemyY.insert(i, locationYenemy[i]-locationY)
            # Нанесет удар герою при столкновения с врагом
            if -5<=differencePlayerAndEnemyX[i]<=5 and -5<=differencePlayerAndEnemyY[i]<=5:
                playerHealth = playerHealth - 1
                hit.play()
                # Если героя умер он использует свою жизнь и продолжает игру в координатах(100,300)
                if playerHealth <= 0:
                    locationX = 100
                    locationY = 300
                    lifePlayer = lifePlayer - 1
                    playerHealth = 100
                    
        
        
        # Если уровень равен к количеству мертвых врагов то запускается след уровень
        if countDeathEnemy == level:
            locationX = 100
            locationY = 300
            countDeathEnemy = 0
            level = level + 1
            ImageOfEnemy=list()
            locationXenemy=list()
            locationYenemy=list()
            xChangeEnemy=list()
            yChangeEnemy=list()
            deathHealth=list()
            
            speedEnemy=1
            enemy_alive = list()
            timer()
            createEnemy(level)
            
        # Если у героя нету жизни то игрок должен записать свою имя. Имя и счет сохроняется в файле 'highscore.txt'
        if lifePlayer == 0:
            
            clock = pygame.time.Clock()
            defeat.play()

            
            input_box = pygame.Rect(WINDOWWIDTH/2-140, 300, 300, 32)
            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            color = color_inactive
            active = True
            text = ''
            done = True
            while done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                done = False
                                inMenu = True
                                screen.blit(background, (0, 0))
                                break
                            if event.key == pygame.K_RETURN:
                                with open('highscore.txt', 'a', encoding = 'utf-8') as file:
                                    file.write(f'{score} {text} \n')  
                                text = ''
                                done = False
                                inMenu = True
                                screen.blit(background, (0, 0))
                                break
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            
                            else:
                                text += event.unicode
                                
                draw_text(screen, "ENTER YOU NAME:", 35, WINDOWWIDTH/2, 250, WHITE) 
                surf1 = pygame.Surface((300, 40))
                surf1.fill((0, 0, 0)) 
                screen.blit(surf1, (WINDOWWIDTH/2-140,300))
                txt_surface = font.render(text, True, color)
                width = max(200, txt_surface.get_width()+10)
                input_box.w = width
                screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                pygame.draw.rect(screen, BLACK, input_box, 2)
                pygame.display.flip()
                #clock.tick(30)                   
                lifePlayer = 3
                playerHealth = 100
                level = 1
                score = 0
            break
        
        
