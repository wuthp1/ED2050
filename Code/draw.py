#/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provides functions to visualize state of the power plant model.

"""
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
"""Maximimum allowable load angle.

Defines, at what angle the maximum load angle constraint line will be
drawn in the opaerating chart."""

#globals
global screen
"""pygame.Surface: screen to draw on"""

#define serial reactance p.u.
XD = 2



def init():
    """Initializes pygame.
    
    pygame is the library which provides functions to do the graphics.
    
    Returns:
        pygame.Surface: fullscreen surface to draw on.
    """
    # Initialize Pygame.
    pygame.init()
    # Set size of pygame window.
    screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return screen


def write(msg, font = "Courier New", size = 40):
    """Draws a text on a new surface.
    
    Args:
        msg (str): text to be written.
        font (str): font to use for the text.
        size (int): font size in pixels.
    
    Returns:
        pygame.Surface: surface with text on it.
        
    """
    myfont = pygame.font.SysFont(font, size)
    mytext = myfont.render(msg, True, (0,0,0))
    mytext = mytext.convert_alpha()
    return mytext


def op_chart(screen,p,q):
    """Draws operating chart of the synchronous machine.
    
    Args:
        screen (pygame.Surface): Surface to draw chart onto
        p (float): active power of the synchronous machine p.u.
        q (float): reactive power of the synchronous machine p.u.
    
    Returns:
        pygame.Surface: surface with the power chart on it
    
    """
    
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
    """Draws an arrow on a surface.
    
    Draws a single ended arrow. The line consists of single lines, so the
    arrowhead will not be filled.
    
    Args:
        surf (pygame.Surface): surface to draw arrow onto
        color (pygame.Color): color of the arrow
        start (tuple(int or float x, int or float y): start position of
            arrow in pixels.
        end (tuple(int or float x, int or float y): end position of
            arrow in pixels.
    
    """
    
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
    
    pygame.draw.lines(surf,color,True,[(end),(x_a, y_a),(x_b, y_b)])


def op_arrows(surf,p,q,center,gd):
    """Draws arrows of operating chart on surface.
    
    Args:
        surf (pygame.Surface): surface to draw arrows onto.
        p (float): active power of the synchronous machine p.u.
        q (float): reactive power of the synchronous machine p.u.
        center (tuple(int or float x, int or float y): center position of
            the chart (=start position of arrows) in pixels.
        gd (float): synchronous admittance (1/xd) of synchronous machine
            in p.u.
    
    """
    
    color = BLACK
    arrow(surf, color, center, (center[0]+q,center[1]-p))
    arrow(surf, color, (int(center[0]-gd),center[1]), (center[0]+q,center[1]-p))
    return


def op_arc(surf, screen_width, center):
    """Draws arc of operating chart on surface.
    
    Args:
        surf (pygame.Surface): surface to draw arrows onto.
        screen_width (int): width of surf in pixels.
        center (tuple(int or float x, int or float y): center position of
            the chart (=start position of arrows) in pixels.
        gd (float): synchronous admittance (1/xd) of synchronous machine
            in p.u.
    
    """
    
    arc_size = screen_width*0.9
    #calculate zero point of the rectangle with the arc in it (upper left point)
    arc_zero = (int(center[0]-(arc_size/2)),int(center[1]-(arc_size/2)))
    pygame.draw.arc(surf,BLACK,pygame.Rect(arc_zero,(int(arc_size),int(arc_size))),-pi/2,pi*3/2)
    return
