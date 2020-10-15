# -*- coding: utf-8 -*-
"""
Community Transmission COVID Model

"""

import pygame
from sys import exit
import random
import math


#initialise pygame & variables
pygame.init()
WIDTH = 800
HEIGHT =  600
BLUE = (57, 34, 227)
RED = (242, 22, 15)
BLACK = (0, 0, 0)
GREEN = (95, 255, 51)
small_font = pygame.font.Font('freesansbold.ttf', 12)
FPS = 60
clock = pygame.time.Clock()
frame_count = 0

#Title & Icon
pygame.display.set_caption('Coronavirus Community Transmission Model')
icon = pygame.image.load('virus.png')
pygame.display.set_icon(icon)

#Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Create Community class:
class Community():
    
    def __init__(self, population, inf_rate, move):
        Community.pop = population
        Community.inf_rate = inf_rate #Percentage as integer
        Community.move = move
        Community.x = []
        Community.y = []
        Community.status = []
        Community.direction = []
        Community.x_change = []
        Community.y_change = []
        Community.exposed = []
        Community.frame_infected = []
        Community.infections = 0
        Community.fatalities = 0
        Community.recovered = 0
    
    def set_coords(self):
        for i in range(self.pop):
            x = random.randint(1, WIDTH)
            y = random.randint(1, HEIGHT)
            direct = random.randint(1, 8)
            self.x.append(x)
            self.y.append(y)
            self.direction.append(direct)
            self.x_change.append(0)
            self.y_change.append(0)
            self.frame_infected.append(0)
            
    def set_status(self, frame_count):
        for i in range(self.pop):
            if self.inf_rate >= random.randint(1, 100):
                state = "infected"
                self.frame_infected[i] = frame_count
                self.infections += 1
            else:
                state = "healthy"
            self.status.append(state)
        
    def render(self, screen):
        for i in range(self.pop):
            if self.status[i] == "healthy":
                pygame.draw.circle(screen, BLUE, (int(self.x[i]), int(self.y[i])), 2)
            elif self.status[i] == "infected":
                pygame.draw.circle(screen, RED, (int(self.x[i]), int(self.y[i])), 2)
            elif self.status[i] == "recovered":
                pygame.draw.circle(screen, GREEN, (int(self.x[i]), int(self.y[i])), 2)
            else:
                pygame.draw.circle(screen, BLACK, (int(self.x[i]), int(self.y[i])), 2)
                
    def reset_direction(self):
        for i in range(self.pop):
            if self.x[i] <= 5 or self.x[i] >= WIDTH-5 or self.y[i] <=5 or self.y[i] >= HEIGHT-5:
                direct = random.randint(1, 8)
                self.direction[i] = direct
            
    def update_coord(self) :
        for i in range(self.pop):
            if self.direction[i] == 1 : #North
                self.x_change[i] = 0
                self.y_change[i] = -self.move
            elif self.direction[i] == 2 : #North-East
                self.x_change[i] = self.move
                self.y_change[i] = -self.move
            elif self.direction[i] == 3 : #East
                self.x_change[i] = self.move
                self.y_change[i] = 0
            elif self.direction[i] == 4 : #South-East
                self.x_change[i] = self.move
                self.y_change[i] = self.move
            elif self.direction[i] == 5 : #South
                self.x_change[i] = 0
                self.y_change[i] = self.move
            elif self.direction[i] == 6 : #South-West
                self.x_change[i] = -self.move
                self.y_change[i] = self.move
            elif self.direction[i] == 7 : #West
                self.x_change[i] = -self.move
                self.y_change[i] = 0
            elif self.direction[i] == 8 : #North-west
                self.x_change[i] = -self.move
                self.y_change[i] = -self.move
            self.x[i] += self.x_change[i]
            self.y[i] += self.y_change[i]
    
    def transmission_event(self, frame_count): #Check for community contact
        for i in range(self.pop):
            if self.status[i] == "infected": 
                    for j in range(self.pop):
                        distance = math.sqrt(math.pow(self.x[i] - self.x[j], 2) 
                        + math.pow(self.y[i] - self.y[j], 2))
                        if distance < 2 and self.status[j] == "healthy":
                            self.status[j] = "infected"
                            self.frame_infected[j] = frame_count
                            self.infections += 1
        
    def outcome_event(self, frame_count, fatality_rate=1):
        for i in range(self.pop):
            if self.status[i] == "infected":
                if (self.frame_infected[i] + 14*FPS) <= frame_count:
                    if fatality_rate >= random.randint(1, 100):
                        self.status[i] = "dead"
                        self.fatalities += 1
                        self.infections -= 1
                    else:
                        self.status[i] = "recovered"
                        self.recovered += 1
                        self.infections -= 1
                        
    def display_outcomes(self, screen, x=5, y=5) :
        outcome_string = "Active infections: {}    Recovered: {}   Fatalities: {}".format(self.infections, self.recovered, self.fatalities)
        text = small_font.render(outcome_string, True, BLACK)
        screen.blit(text, (x, y))

            

#Initialise village community:
village = Community(population = 250, inf_rate = 10, move = 1)
village.set_coords()
village.set_status(frame_count)


while True :
    
    screen.fill((211, 226, 245)) #RGB
    frame_count += 1
    print(frame_count)
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    #Update community coordinates:
    village.reset_direction()
    village.update_coord()
    #Find new infections:
    village.transmission_event(frame_count)
    #Find recovery and fatality events:
    village.outcome_event(frame_count, fatality_rate=10) #Artificially high for illustrative purposes
    #Render village community:
    village.render(screen)
    #Render text:
    village.display_outcomes(screen)
    
    
    pygame.display.update()
    clock.tick(FPS)
            