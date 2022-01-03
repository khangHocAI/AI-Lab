from Seeker import Seeker
import pygame


def draw_style_rect(screen, x,y, w,h, flag, hider_image, seeker_image):
    if flag == 1:
        pygame.draw.rect(screen, (0,0,0),(x,y,w,h))
    elif flag == 2:
        pygame.draw.rect(screen, (255,255,0),(x,y,w,h))
    else:
        pygame.draw.rect(screen, (0,0,0),(x,y,w,h), 1)
        if flag == 3:
            screen.blit(hider_image, (x+4, y+4))
        elif flag == 4:
            screen.blit(seeker_image, (x+4, y+4))


def draw_map(screen, size,map, hider_image, seeker_image):
    pixel_x = 10
    pixel_y = 10
    for i in range (size):
        for j in range (size):
            draw_style_rect(screen, pixel_x, pixel_y,40,40, map[i][j], hider_image, seeker_image)
            pixel_x += 45
        pixel_y += 45 
        pixel_x = 10 