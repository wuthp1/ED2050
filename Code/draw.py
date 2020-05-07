import pygame
from math import pi, sin, cos, tan, atan2, pow, sqrt

# Define the colors use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#define maximal Load Angle in radians
MAX_LOAD_ANGLE = 70*pi/180


#globals
global screen

#define serial reactance p.u.
XD = 2



def init():
    # Initialize Pygame.
    pygame.init()
    # Set size of pygame window.
    screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return screen


def write(msg, font = "Courier New"):
    myfont = pygame.font.SysFont(font, 40)
    mytext = myfont.render(msg, True, (0,0,0))
    mytext = mytext.convert_alpha()
    return mytext

def op_chart(screen,p,q):
    
    screensize = screen.get_size()
    x = int(screensize[0]/2)
    y = int(screensize[1]/2)
    
    #create surface for operating chart
    chart = pygame.Surface((x,y))
    #create white background for operating chart
    bg_chart = pygame.Surface(chart.get_size())
    bg_chart.fill(WHITE)
    bg_chart=bg_chart.convert()
    chart.blit(bg_chart,(0,0))
    
    #calculate scaling factor pixel/(p.u.)
    scale = x*0.45
    #claculate diagram center
    center = (x/2, y-100)
    #draw horizontal axis
    arrow(chart,BLACK,(0,int(center[1])),(x,int(center[1])))
    #draw vertical axis
    arrow(chart,BLACK,(int(center[0]),y),(int(center[0]),0))
    #draw arc
    op_arc(chart,x,center)
    #draw load angle limit line
    pygame.draw.line(chart, RED, (center[0]-(100/tan(MAX_LOAD_ANGLE))-(scale/XD),y),(center[0]+((y-100)/tan(MAX_LOAD_ANGLE))-(scale/XD),0))
    
    #draw the arrows indicating the operating point
    op_arrows(chart,p*scale,q*scale,center,scale/XD)
    
    return chart

def arrow(surf,color,start,end,arr_size=10,arr_angle=(pi/6)):
    pygame.draw.line(surf,color,start,end)
    angle = atan2(end[1]-start[1],end[0]-start[0])
    #calculate arrow cornerpoints a and b
    dx_a = cos(pi+angle-arr_angle)*arr_size
    dy_a = sin(pi+angle-arr_angle)*arr_size
    dx_b = cos(pi+angle+arr_angle)*arr_size
    dy_b = sin(pi+angle+arr_angle)*arr_size
    x_a = end[0]+dx_a
    y_a = end[1]+dy_a
    x_b = end[0]+dx_b
    y_b = end[1]+dy_b
    
    return pygame.draw.lines(surf,color,True,[(end),(x_a, y_a),(x_b, y_b)])

def op_arrows(surf,p,q,center,gd):
    color = BLACK
    arrow(surf, color, center, (center[0]+q,center[1]-p))
    arrow(surf, color, (int(center[0]-gd),center[1]), (center[0]+q,center[1]-p))
    return

def op_arc(surf, screen_width, center):
    arc_size = screen_width*0.9
    #calculte zero point of the rectangle with the arc in it (upper left point)
    arc_zero = (int(center[0]-(arc_size/2)),int(center[1]-(arc_size/2)))
    pygame.draw.arc(surf,BLACK,pygame.Rect(arc_zero,(int(arc_size),int(arc_size))),-pi/2,pi*3/2)
    return
