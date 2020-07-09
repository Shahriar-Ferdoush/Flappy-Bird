# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 07:55:47 2020

@author: Shahriar Ferdoush
"""


import pygame
import sys
import random


def draw_base():
    screen.blit(base_surface, (base_x_position + 336, 460))

def creat_pipe():
    random_pipe_y = random.choice(pipe_height)
    random_pipe_x = random.choice([600,500,512,567,475])
    
    bottom_pipe = pipe_img.get_rect(midtop = (random_pipe_x,random_pipe_y))
    top_pipe =  pipe_img.get_rect(midbottom = (random_pipe_x,random_pipe_y-150))
    
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.top < 0:
            flip_pipe_img = pygame.transform.flip(pipe_img,False,True)
            screen.blit(flip_pipe_img, pipe)
        else:
            screen.blit(pipe_img, pipe)

def cheak_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 460:
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 4.5, 1)
    return new_bird

def bird_animation():
    new_bird = bird_imgs[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_text = game_font.render('SCORE: '+str(int(score)), True, (0,0,0))
        score_rect = score_text.get_rect(center = (168,50))
        screen.blit(score_text, score_rect)
        
    if game_state == 'game_over':
        score_text = game_font.render('SCORE: '+str(int(score)), True, (0,0,0))
        score_rect = score_text.get_rect(center = (168,50))
        screen.blit(score_text, score_rect)
        
        high_score_text = game_font.render('HIGH SCORE: '+str(int(high_score)), True, (0,0,0))
        high_score_rect = high_score_text.get_rect(center = (168,425))
        screen.blit(high_score_text, high_score_rect)
        
        game_name = game_name_font.render('FlappyBIRD', True, (255, 255, 255))
        game_name_rect = game_name.get_rect(center = (168, 220))
        screen.blit(game_name, game_name_rect)
        
        text = text_font.render('Press Space to Continue...', True, (255, 255, 255))
        text_rect = text.get_rect(center = (168, 450))
        screen.blit(text, text_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
screen = pygame.display.set_mode((336,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('font.otf',24)
game_name_font = pygame.font.Font('CornFed.ttf',36)
text_font = pygame.font.Font('SFCartoonistHand.ttf', 18)

# Game Variable
gravity = 0.25
bird_movement = 0
base_x_position = 0  # initial position of the base
game_active = True
bird_index = 0
score = 0
high_score = 0

# imports images
bg_surface = pygame.image.load('bg.png').convert()
base_surface = pygame.image.load('base.png').convert()

# imports bird image, adds a rectange to it with center at
# certain co-ordinate
bird_img1 = pygame.image.load('bird1.png').convert_alpha()
bird_img2 = pygame.image.load('bird2.png').convert_alpha()
bird_img3 = pygame.image.load('bird3.png').convert_alpha()
bird_imgs = [bird_img1, bird_img2, bird_img3]

bird_img = bird_imgs[bird_index]
bird_rect = bird_img.get_rect(center = (50,256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 150)

# import pipe images
pipe_img = pygame.image.load('pipe.png').convert()
pipe_list = []
pipe_height = [140,180,256,210,350,300]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


while True:
    """
    Event handler
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                bird_movement = 0
                score = 0
                pipe_list.clear()
                bird_rect.center = (50,256)
                
        if event.type == SPAWNPIPE:
            pipe_list.extend(creat_pipe())
            
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_img, bird_rect = bird_animation()

    if game_active:
        # move base
        base_x_position -= 4
        
        # adds background to the screen             
        screen.blit(bg_surface, (0,0))
        
        # Implements gravity on the bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        
        # Rotate Bird
        rotated_bird = rotate_bird(bird_img)
        
        # adds bird on calculated height
        screen.blit(rotated_bird, bird_rect)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        # Updating and Displaying Score
        score += .08
        score_display('main_game')
        
        #cheaking collision
        game_active = cheak_collision(pipe_list)
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')

    
    draw_base()
    if(base_x_position <= -337):
        base_x_position = 0
    screen.blit(base_surface, (base_x_position,460))
    
    pygame.display.update()
    clock.tick(60)
    



