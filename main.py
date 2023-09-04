import pygame
import asyncio
from sys import exit
pygame.init()
pygame.display.set_caption('CHECKING')


def display_Score():
        global score_surf
        current_time = pygame.time.get_ticks()//1000 - start_time
        print(current_time)
        score_surf = test_font.render('Dino '+str(current_time),False,'Black')
        return current_time

screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('Graphics/Sky.png').convert()
ground_surf = pygame.image.load('Graphics/ground.png').convert()

score_surf = test_font.render('Dino',False,'Black')
score_rect = score_surf.get_rect(center = (400,50))

snail_surf = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright =(800,300))

player_surf = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom =(80,300))
player_gravity = 0

#intro and ending
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

title_surf = test_font.render('Dino Game',False,(111,196,162))
title_rect = title_surf.get_rect(center=(400,80))

game_msg = test_font.render('Press Space to Run',False,(111,196,162))
game_msg_rect = game_msg.get_rect(center=(400,320))

async def main():
    global game_active,score,player_gravity,start_time
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom==300:
                    if player_rect.collidepoint(event.pos): 
                        player_gravity = -20

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_rect.bottom==300:
                        player_gravity = -20
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
                    start_time = pygame.time.get_ticks()//1000
        if game_active:
            if snail_rect.right < 0:
                snail_rect.left = 800
            snail_rect.right-=4
            screen.blit(sky_surf,(0,0))
            screen.blit(ground_surf,(0,300))
            screen.blit(score_surf,score_rect)
            screen.blit(snail_surf,snail_rect)
            player_gravity+=1 
            player_rect.y += player_gravity
            if player_rect.bottom>300: 
                player_rect.bottom=300
            screen.blit(player_surf,player_rect)
            score = display_Score()
            if snail_rect.colliderect(player_rect):
                game_active = False
        else:
            screen.fill((94,129,162))
            screen.blit(player_stand,player_stand_rect)
            score_msg = test_font.render(f'Your Score:{score}',False,(111,196,162))
            score_msg_rect = score_msg.get_rect(center = (400,330))
            screen.blit(title_surf,title_rect)
            if score == 0:
                screen.blit(game_msg,game_msg_rect)
            else:
                screen.blit(score_msg,score_msg_rect)
        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())