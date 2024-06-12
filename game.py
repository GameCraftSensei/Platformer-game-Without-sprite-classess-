import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{current_time}',False,'Red')
    score_rect = score_surf.get_rect(midleft = (350,50))
    Screen.blit(score_surf,score_rect)
    return current_time

def obsticle_movement(obsticle_list):
    if obsticle_list:
        for obsticle_rect in obsticle_list:
            obsticle_rect.x -= 5

            if obsticle_rect.bottom == 300: Screen.blit(snail_surf,obsticle_rect)  
            else: Screen.blit(fly_surf,obsticle_rect)

        obsticle_list = [obsticle for obsticle in obsticle_list if obsticle.x > -100]

        return obsticle_list
    else: return []

def collisions(player,obsticles):
    if obsticles:
        for obsticle_rect in obsticles:
            if player.colliderect(obsticle_rect): return False

    return True

def player_animation():
    global player_surf,player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else: 
        player_index += .1
        if player_index >= len(player_walk_images): player_index = 0
        player_surf = player_walk_images[int(player_index)]






pygame.init()
Screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
Clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)
game_active = False
start_time = 0
Score = 0
bg_music = pygame.mixer.Sound('bg music.wav')
bg_music.play(loops = -1)

#Background
Sky_surf = pygame.image.load('bg.png').convert()
Grass_surf = pygame.image.load('ground.png').convert()

# text = test_font.render('My game', False , 'red')
# text_rect = text.get_rect(midright = (450,50))

#obsticle
#Snail
snail_1 = pygame.image.load('Enemies/snailWalk1.png').convert_alpha()
snail_2 = pygame.image.load('Enemies/snailWalk2.png').convert_alpha()
snail_walk = [snail_1,snail_2]
snail_index = 0
snail_surf = snail_walk[snail_index]

#fly
fly_1 = pygame.image.load('Enemies/flyFly1.png').convert_alpha()
fly_2 = pygame.image.load('Enemies/flyFly2.png').convert_alpha()
fly_walk = [fly_1,fly_2]
fly_index = 0
fly_surf = fly_walk[fly_index]


obsticle_rect_list = []

# Player 

player_walk1 = pygame.image.load('Player/p1_walk/PNG/p1_walk01.png')
player_walk2 = pygame.image.load('Player/p1_walk/PNG/p1_walk03.png')
player_walk_images = [player_walk2,player_walk1]

player_jump = pygame.image.load('player/p1_jump.png')
player_index = 0
player_surf = player_walk_images[player_index]
player_rect = player_surf.get_rect(midbottom=(40,300))
gravity = 0
jump_sound = pygame.mixer.Sound('jump-15984.mp3')

#Intro screen
player_stand = pygame.image.load('Player/p1_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Picxel blade runner', False ,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,50))

start_game = test_font.render('press SPACE to enter', False ,(111,196,169))
start_game_rect = start_game.get_rect(center = (400,350))



#Timer
obsticle_Timer = pygame.USEREVENT + 1
pygame.time.set_timer(obsticle_Timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)


#EVent loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    jump_sound.play()
                    jump_sound.set_volume(0.5)
                    gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obsticle_Timer:
                if randint(0,2):
                    obsticle_rect_list.append(snail_surf.get_rect(midbottom =(randint(900,1100),300)))
                else:
                    obsticle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900,1100),200)))

            if event.type == snail_animation_timer:
                if snail_index == 0 : snail_index = 1
                else: snail_index = 0
                snail_surf = snail_walk[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = fly_walk[fly_index]
            
            
    if game_active:
    #background
        Screen.blit(Sky_surf,(0,0))
        Screen.blit(Grass_surf,(0,300))

    #Score
        # Screen.blit(text,text_rect)
        Score = display_score()

    #Snail
        # Screen.blit(snail,snail_rect)
        # snail_rect.left -= 4
        # if snail_rect.right < 0: snail_rect.left = 800 

    #Player
        gravity += 1 
        player_rect.y += gravity
        if player_rect.bottom > 300 : player_rect.bottom = 300
        player_animation()
        Screen.blit(player_surf,player_rect)

        #obsticle movement
        obsticle_rect_list = obsticle_movement(obsticle_rect_list)

        

    # COLLISSIONS  
        game_active = collisions(player_rect,obsticle_rect_list)

    else:
        Screen.fill((94,129,162))
        Screen.blit(player_stand,player_stand_rect)
        obsticle_rect_list.clear()
        player_rect.midbottom = (80,300)


        Score_mess = test_font.render(f'Your Score: {Score}', False , (111,196,169))
        Score_mess_rect = Score_mess.get_rect(center = (400,350))
        Screen.blit(game_name,game_name_rect)
        gravity = 0
    

        if Score == 0: Screen.blit(start_game,start_game_rect)
        else: Screen.blit(Score_mess,Score_mess_rect) 
            
        
        

    pygame.display.update()
    Clock.tick(60)

