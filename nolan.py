#Nolan Kondrich ~ COMP155B ~ Sink the Shot
#Sink the Shot

import pygame, sys
from pygame.locals import *

pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Sink the Shot")

# set colors
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

#draw some shapes
DISPLAYSURF.fill(WHITE)
pygame.draw.circle(DISPLAYSURF, ORANGE, (0, 0), 20, 0)
pygame.draw.ellipse(DISPLAYSURF, BLACK, (0, 640, 70, 50))


class Projectile:
#Attributes are:
    def __init__(self, angle, velocity, height, time):
        self.xPos = 0.0
        self.yPos = height
        self.theta = angle(radians)
        self.xVeloz = velocity*cos(theta)
        self.yVeloz = velocity*sin(theta)
#getters and setters:
    def getxpos():
        return xPos
    def setxpos(x):
        xPos = x
    def update():
        self.xPos= self.xPos + self.xVeloz * time
        newYveloz = self.yVeloz - time*9.8
        self.yPos = self.yPos + time * ((self.yVeloz + newYveloz)/2)
        self.yVeloz = newYveloz
#Init
print("Nolan Kondrich ~ COMP155B ~ Sink the Shot")
print("Please enter initial shot values")

#Input: promt user & read our values
num1=eval(input("Enter angle: "))
num2=eval(input("Enter velocity: "))
num3=eval(input("Enter height: "))
num4=eval(input("Enter time: "))

# data echo
print("\n\nEcho of the Data: ")
print("Angle: ", angle)
print("Velocity: ", velocity)
print("Height: ", height)
print("Time: ", time)

ball = Projectile(angle, veloz, height, time)

while(ball.getY()>=0): #in flight
    ball.update()


