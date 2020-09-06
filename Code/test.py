import pygame
import draw
import time

screen = draw.init()
screensize = screen.get_size()
background = pygame.Surface(screen.get_size())
# Fill the background white color.
background.fill((255,255,255))
# Convert Surface object to make blitting faster.
background = background.convert()
uk=0.6
i = 0.1
p=0.3
q=-0.3
chart = draw.arr_chart(screen,uk,i,p,q)
screen.blit(chart,(0,0))
pygame.display.flip()
time.sleep(10)
pygame.quit()