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

pygame.init()
screen = pygame.display.set_mode((336,512))
clock = pygame.time.Clock()

# Game Variable
gravity = 0.25
bird_movement = 0
base_x_position = 0  # initial position of the base
game_active = True

# imports images
bg_surface = pygame.image.load('bg.png').convert()
base_surface = pygame.image.load('base.png').convert()

# imports bird image, adds a rectange to it with center at
# certain co-ordinate
bird_img = pygame.image.load('bird1.png').convert()
bird_rect = bird_img.get_rect(center = (50,256))

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
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6
                
        if event.type == SPAWNPIPE:
            pipe_list.extend(creat_pipe())

    if game_active:
        # move base
        base_x_position -= 4
        
        # adds background to the screen             
        screen.blit(bg_surface, (0,0))
        
        # Implements gravity on the bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        
        # adds bird on calculated height
        screen.blit(bird_img, bird_rect)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        #cheaking collision
        game_active = cheak_collision(pipe_list)
    

    
    draw_base()
    if(base_x_position <= -337):
        base_x_position = 0
    screen.blit(base_surface, (base_x_position,460))
    
    pygame.display.update()
    clock.tick(60)
    



