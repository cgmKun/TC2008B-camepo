import agentpy as ap
import os
import random
import time

# Class to set the individual
class road_block:
    def __init__(self, max_capacity, direction):
        self.max_capacity = max_capacity
        self.curr_capacity = 0
        self.direction = direction

    def isFull(self):
        if self.curr_capacity == self.max_capacity:
            return True
        return False
        

# Initial matrix for the road system
def initial_roads():
    
    up = road_block(2, 'up')
    down = road_block(2, 'down')
    left = road_block(2, 'left')
    right = road_block(2, 'right')
    null = road_block(0, 'null')
    null.curr_capacity = -1
    
    roads = [
        [road_block(2, 'down'), road_block(2, 'left'), road_block(2, 'left'), road_block(2, 'left')],
        [road_block(2, 'down'), road_block(0, 'null'), road_block(0, 'null'), road_block(2, 'up')],
        [road_block(2, 'down'), road_block(0, 'null'), road_block(0, 'null'), road_block(2, 'up')],
        [road_block(2, 'right'), road_block(2, 'right'), road_block(2, 'right'), road_block(2, 'up')]
    ]

    # roads = [
    # [1, 0, 0, 0], 
    # [0, 'x', 'x', 0], 
    # [0, 0, 0, 0],
    # [0, 0, 0, 0]]

    return roads

# Print matrix of the system
def print_new_roads(roads):
    for ren in range(len(roads)):
        for col in range(len(roads[0])):
            print(roads[ren][col].curr_capacity, end=" ")
        print()

def print_roads(matriz):
    for ren in range(len(matriz)):
        for col in range(len(matriz[0])):
            print(matriz[ren][col], end=" ")
        print()

# Check if the current position in the matrix is not out of bounds
def valid_coordinate(ypos, xpos, road):
    if xpos <= 3 and ypos <= 3 and xpos >= 0 and ypos >= 0 and road[ypos][xpos] != 'x':
        return (True)
    return (False)

def valid_coordinate_roads(ypos, xpos, road):
    if xpos <= 3 and ypos <= 3 and xpos >= 0 and ypos >= 0:
        return True
    return False
    
# Controller to make valid movements
def controller(x, player_xpos, player_ypos, road):
    
    if x == 'w':
        if valid_coordinate(player_ypos-1, player_xpos, road):
            player_ypos -= 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos+1][player_xpos] -= 1
            print()
            print_roads(road)
    elif x == 'a':
        if valid_coordinate(player_ypos, player_xpos-1, road):
            player_xpos -= 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos][player_xpos+1] -= 1
            print()
            print_roads(road)
    elif x == 's':
        if valid_coordinate(player_ypos+1, player_xpos, road):
            player_ypos += 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos-1][player_xpos] -= 1
            print()
            print_roads(road)
    elif x == 'd':
        if valid_coordinate(player_ypos, player_xpos+1, road):
            player_xpos += 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos][player_xpos-1] -= 1
            print()
            print_roads(road)
    else:
        print("movimiento invalido")


# Global variable for roads and testing
roadx = initial_roads()
road_history = []
player_xpos = 0
player_ypos = 0

# Controller to make valid movements
def manual_controller(x):
    global player_xpos
    global player_ypos
    global roadx
    if x == 'w':
        if valid_coordinate_roads(player_ypos-1, player_xpos, roadx):
            player_ypos -= 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos+1][player_xpos].curr_capacity -= 1
    elif x == 'a':
        if valid_coordinate_roads(player_ypos, player_xpos-1, roadx):
            player_xpos -= 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos][player_xpos+1].curr_capacity -= 1
    elif x == 's':
        if valid_coordinate_roads(player_ypos+1, player_xpos, roadx):
            player_ypos += 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos-1][player_xpos].curr_capacity -= 1
    elif x == 'd':
        if valid_coordinate_roads(player_ypos, player_xpos+1, roadx):
            player_xpos += 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos][player_xpos-1].curr_capacity -= 1
    else:
        print("movimiento invalido")

# Manual control for the simulation matrix
def simulation():
    global roadx
    x = ""
    while x != "-1":
        print('posX ', player_xpos)
        print('posY ', player_ypos)
        x = input("Movement: ")
        
        # Limpiar pantalla en mac / linux
        #os.system('clear')
        
        # Limpiar pantalla en windows
        #os.system('cls')
        
        manual_controller(x)
        print_new_roads(roadx)
        print()
    print("End controller simulation")

# Vehicle Class
class Vehicle(ap.Agent):
    def setup(self):
        # Initial coordinates for the agent
        self.xpos = 0
        self.ypos = 0

    def movement(self, space):
        # valid_coordinate(self.ypos-1, self.xpos)
        white_list = ['w', 'a', 's', 'd']
        choice = random.choice(white_list)

        if choice == 'w' and valid_coordinate(self.ypos-1, self.xpos, space):
            controller(choice, self.xpos, self.ypos, space)
            self.ypos -= 1
        elif choice == 'a' and valid_coordinate(self.ypos, self.xpos-1, space):
            controller(choice, self.xpos, self.ypos, space)
            self.xpos -= 1
        elif choice == 's' and valid_coordinate(self.ypos+1, self.xpos, space):
            controller(choice, self.xpos, self.ypos, space)
            self.ypos += 1
        elif choice == 'd' and valid_coordinate(self.ypos, self.xpos+1, space):
            controller(choice, self.xpos, self.ypos, space)
            self.xpos += 1
        
        self.record('ypos', self.ypos)
        self.record('xpos', self.xpos)

# Model class
class Model(ap.Model):
    def setup(self):
        self.space = initial_roads()
        self.agents = ap.AgentList(self, 2, Vehicle)
    
    def step(self):
        self.agents.movement(self.space)

parameters = {
    'steps': 20,
}

def main():
    simulation()
    #global road_history
    #model = Model(parameters)
    #result = model.run()
    #print(result.variables.Vehicle)
    
    #for i in range(len(road_history)):
     #   print('i = ', i)
      #  print_roads(road_history[i])
       # print()
        #time.sleep(1)
        #os.system('clear')

    #print(result.reporters)
main()