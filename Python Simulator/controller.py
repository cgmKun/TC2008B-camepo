import agentpy as ap
import pandas as pd
import os
import random
import time
import csv
import json

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
            temp_row.append(road_block(int(rows[i][j][0]), rows[i][j][1:]))
        roads.append(temp_row)

    return roads

def get_paths():
    file = open('path_macros.csv')
    type(file)

    reader = csv.reader(file)
    paths = []

    for row in reader:
        paths.append(row)

    return paths

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
def valid_coordinate(ypos, xpos, road):
    return xpos < len(road[0]) and ypos < len(road) and xpos >= 0 and ypos >= 0

# Controller to make valid movements
def agent_controller(x, player_xpos, player_ypos, roadx):
    if x == 'w':
        player_ypos -= 1
        roadx[player_ypos][player_xpos].curr_capacity += 1
        roadx[player_ypos+1][player_xpos].curr_capacity -= 1
    elif x == 'a':
        player_xpos -= 1
        roadx[player_ypos][player_xpos].curr_capacity += 1
        roadx[player_ypos][player_xpos+1].curr_capacity -= 1
    elif x == 's':
        player_ypos += 1
        roadx[player_ypos][player_xpos].curr_capacity += 1
        roadx[player_ypos-1][player_xpos].curr_capacity -= 1
    elif x == 'd':
        player_xpos += 1
        roadx[player_ypos][player_xpos].curr_capacity += 1
        roadx[player_ypos][player_xpos-1].curr_capacity -= 1
    else:
        print("Err. Invalid movement")

# Vehicle Class
class Vehicle(ap.Agent):
    def setup(self):
        # Control values for agents
        self.xpos = 0
        self.ypos = 0
        self.curr_step = 0
        self.path = get_paths()[0]

        # RNG spawn state
        self.trip_begin = False
        self.trip_end = False
        
        # Trip spawn rate, given by the numbers of 0 and 1 on the matrix
        # 1 -> trip_begin = true
        # 0 -> trip_begin = false
        # Current rate 50% of spawn
        self.trip_spawn_rate = [1, 0, 0, 0, 0]

        # KPI's
        self.completion_percentage = 0
        self.trip_length = 0

    def movement(self, space):

        #Check if the vehicle has been deployed
        if self.trip_begin == False:
            rng = random.choice(self.trip_spawn_rate)
            if(rng == 1):
                self.trip_begin = True

        # If the agent has any moves left to do
        if self.curr_step < len(self.path) and self.trip_begin == True:
            choice = self.path[self.curr_step]
            # Check the choice from the macro
            if choice == 'w':
                #If valid, perform the move
                if valid_coordinate(self.ypos-1, self.xpos, space) and 'U' in space[self.ypos][self.xpos].direction and space[self.ypos-1][self.xpos].curr_capacity < space[self.ypos-1][self.xpos].max_capacity:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.ypos -= 1
            elif choice == 'a':
                if valid_coordinate(self.ypos, self.xpos-1, space) and 'L' in space[self.ypos][self.xpos].direction and space[self.ypos][self.xpos-1].curr_capacity < space[self.ypos][self.xpos-1].max_capacity:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.xpos -= 1
            elif choice == 's':
                if valid_coordinate(self.ypos+1, self.xpos, space) and 'D' in space[self.ypos][self.xpos].direction and space[self.ypos+1][self.xpos].curr_capacity < space[self.ypos+1][self.xpos].max_capacity:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.ypos += 1
            elif choice == 'd':
                if valid_coordinate(self.ypos, self.xpos+1, space) and 'R' in space[self.ypos][self.xpos].direction and space[self.ypos][self.xpos+1].curr_capacity < space[self.ypos][self.xpos+1].max_capacity:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.xpos += 1
            # Add the tracker
            self.trip_length += 1

        self.completion_percentage = (self.curr_step / len(self.path))*100
        self.record('trip_length', self.trip_length)
        self.record('trip_completion_rate', self.completion_percentage)
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
        time.sleep(1)

parameters = {
    'steps': 20,
}

#parameters = pandas´s dataframe
def dataFrame_to_JSON(df):
    json = df.to_json(orient = 'records')
    return json

def JSON_to_dataFrame(json):
    df = pd.read_json(json, orient = 'index')
    return df    


def main():
    #global road_history
    model = Model(parameters)
    result = model.run()
    variables = result.variables.Vehicle

    print(dataFrame_to_JSON(variables))
main()

