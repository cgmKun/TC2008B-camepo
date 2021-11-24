import agentpy as ap
import os
import random
import time
import csv

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

    file = open('road.csv')
    type(file)

    reader = csv.reader(file)
    rows = []
    for row in reader:
        rows.append(row)

    # Load the roads layout from a csv file
    roads = []
    for i in range(0, len(rows)):
        temp_row = []
        for j in range(0, len(rows[0])):
            temp_row.append(road_block(rows[i][j][0], rows[i][j][1:]))
        roads.append(temp_row)

    return roads

# Print matrix of the system
def print_new_roads(roads):
    for ren in range(len(roads)):
        for col in range(len(roads[0])):
            if roads[ren][col].direction == 'N':
                print('X', end=" ")
            else:
                print(roads[ren][col].curr_capacity, end=" ")
        print()

# Check if the current position in the matrix is not out of bounds
def valid_coordinate_roads(ypos, xpos, road):
    if xpos <= 3 and ypos <= 3 and xpos >= 0 and ypos >= 0:
        return True
    return False
    
# Controller to make valid movements
# def controller(x, player_xpos, player_ypos, road):
#     if x == 'w':
#         if valid_coordinate(player_ypos-1, player_xpos, road):
#             player_ypos -= 1
#             road[player_ypos][player_xpos] += 1
#             road[player_ypos+1][player_xpos] -= 1
#             print()
#             print_roads(road)
#     elif x == 'a':
#         if valid_coordinate(player_ypos, player_xpos-1, road):
#             player_xpos -= 1
#             road[player_ypos][player_xpos] += 1
#             road[player_ypos][player_xpos+1] -= 1
#             print()
#             print_roads(road)
#     elif x == 's':
#         if valid_coordinate(player_ypos+1, player_xpos, road):
#             player_ypos += 1
#             road[player_ypos][player_xpos] += 1
#             road[player_ypos-1][player_xpos] -= 1
#             print()
#             print_roads(road)
#     elif x == 'd':
#         if valid_coordinate(player_ypos, player_xpos+1, road):
#             player_xpos += 1
#             road[player_ypos][player_xpos] += 1
#             road[player_ypos][player_xpos-1] -= 1
#             print()
#             print_roads(road)
#     else:
#         print("movimiento invalido")

# Controller to make valid movements
def manual_controller(x, player_xpos, player_ypos, roadx):
    if x == 'w':
        if valid_coordinate_roads(player_ypos-1, player_xpos, roadx) and 'U' in roadx[player_ypos][player_xpos].direction:
            player_ypos -= 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos+1][player_xpos].curr_capacity -= 1
    elif x == 'a':
        if valid_coordinate_roads(player_ypos, player_xpos-1, roadx) and 'L' in roadx[player_ypos][player_xpos].direction:
            player_xpos -= 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos][player_xpos+1].curr_capacity -= 1
    elif x == 's':
        if valid_coordinate_roads(player_ypos+1, player_xpos, roadx) and 'D' in roadx[player_ypos][player_xpos].direction:
            player_ypos += 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos-1][player_xpos].curr_capacity -= 1
    elif x == 'd':
        if valid_coordinate_roads(player_ypos, player_xpos+1, roadx) and 'R' in roadx[player_ypos][player_xpos].direction:
            player_xpos += 1
            roadx[player_ypos][player_xpos].curr_capacity += 1
            roadx[player_ypos][player_xpos-1].curr_capacity -= 1
    else:
        print("movimiento invalido")

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

        print('choice: ', choice)

        if choice == 'w' and valid_coordinate_roads(self.ypos-1, self.xpos, space):
            manual_controller(choice, self.xpos, self.ypos, space)
            self.ypos -= 1
        elif choice == 'a' and valid_coordinate_roads(self.ypos, self.xpos-1, space):
            manual_controller(choice, self.xpos, self.ypos, space)
            self.xpos -= 1
        elif choice == 's' and valid_coordinate_roads(self.ypos+1, self.xpos, space):
            manual_controller(choice, self.xpos, self.ypos, space)
            self.ypos += 1
        elif choice == 'd' and valid_coordinate_roads(self.ypos, self.xpos+1, space):
            manual_controller(choice, self.xpos, self.ypos, space)
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
        print()
        print_new_roads(self.space)

parameters = {
    'steps': 10,
}

def main():
    #global road_history
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
