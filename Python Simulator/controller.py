import agentpy as ap
import os
import random
import time

# Initial matrix for the road system
def initial_roads():
    roads = [
    [2, 0, 0, 0], 
    [0, 'x', 'x', 0], 
    [0, 0, 0, 0], 
    [0, 0, 0, 0]]
    return roads

# Global variable for roads and testing
roadx = initial_roads()
road_history = []
player_xpos = 0
player_ypos = 0

# Print matrix of the system
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

# Manual control for the simulation matrix
def simulation():
    curr_road = roadx
    x = ""
    while x != "-1":
        x = input("Movement: ")
        
        # Limpiar pantalla en mac / linux
        os.system('clear')
        
        # Limpiar pantalla en windows
        #os.system('cls')
        
        controller(x)
        print_roads(curr_road)
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
    # simulation()
    global road_history
    model = Model(parameters)
    result = model.run()
    print(result.variables.Vehicle)
    
    #for i in range(len(road_history)):
     #   print('i = ', i)
      #  print_roads(road_history[i])
       # print()
        #time.sleep(1)
        #os.system('clear')

    #print(result.reporters)
main()