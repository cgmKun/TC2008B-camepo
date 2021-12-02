import numpy as np
import agentpy as ap
import pandas as pd
import random
import time
import csv
import json
from termcolor import colored

#General array to store runs information
runs_statistics = []

# Class to set the individual
class road_block:
    def __init__(self, max_capacity, direction):
        self.max_capacity = max_capacity
        self.curr_capacity = 0
        self.direction = direction
        self.can_advance = True

    def isFull(self):
        if self.curr_capacity == self.max_capacity:
            return True
        return False

# Initial matrix for the road system
def initial_roads():

    file = open('unity_roads.csv')
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

# Get the agent path macros
def get_paths():
    file = open('better_path_macros.csv')
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
                print(colored('▴', 'green'), end=" ")
            else:
                if(roads[ren][col].curr_capacity != 0):
                    print(colored('■','magenta'), end=' ')
                else:
                    print('◌', end=" ")
                #print(roads[ren][col].curr_capacity, end=' ')
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

# Street light Class
class Street_light(ap.Agent):
    def setup(self):
        self.clock = 0
        self.state = False

        self.right_lane_lights = [[1,3],[6,3],[11,3],[1,9],[3,10],[6,8],[9,10],[11,9],[4,4],[9,4],[3,10],[9,10]]
        self.left_lane_lights = [[0,6],[5,6],[10,6],[2,11],[8,11],[10,12],[2,5],[7,5],[2,11],[8,11]]

    def check_state(self, space):
        if self.clock == 3:
            self.clock = 0
            self.state = not self.state
            self.update_state(space)
        
        self.clock += 1

    def update_state(self, space):  
        if(self.state):
            for i in range(0, len(self.right_lane_lights)):
                ypos = self.right_lane_lights[i][0]
                xpos = self.right_lane_lights[i][1]
                space[ypos][xpos].can_advance = True
            for i in range(0, len(self.left_lane_lights)):
                ypos = self.left_lane_lights[i][0]
                xpos = self.left_lane_lights[i][1]
                space[ypos][xpos].can_advance = False
        else:
            for i in range(0, len(self.right_lane_lights)):
                ypos = self.right_lane_lights[i][0]
                xpos = self.right_lane_lights[i][1]
                space[ypos][xpos].can_advance = False
            for i in range(0, len(self.left_lane_lights)):
                ypos = self.left_lane_lights[i][0]
                xpos = self.left_lane_lights[i][1]
                space[ypos][xpos].can_advance = True

# Vehicle Class
class Vehicle(ap.Agent):
    def setup(self):
        # Control values for agents
        self.xpos = 0
        self.ypos = 0
        self.curr_step = 0
        self.path = []

        # RNG spawn state
        self.trip_begin = False
        self.trip_end = False
        
        # Trip spawn rate, given by the numbers of 0 and 1 on the matrixy
        # 1 -> trip_begin = true
        # 0 -> trip_begin = false
        # Standard probability -> 1/40 -> 2.5%
        self.trip_spawn_rate = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # KPI's
        self.completion_percentage = 0
        self.trip_length_ratio = 0
        self.trip_length = 0

        # Initialize variables
        self.set_define_path()

    def set_define_path(self):
        white_list = [0,1,2,3,4,5]
        white_list_paths = [0,1]
        path_pool_choice = random.choice(white_list)
        
        if(path_pool_choice == 0):
            path_choice = random.choice(white_list_paths)
            self.xpos = 0
            self.ypos = 1
            self.path = get_paths()[path_choice]
        elif(path_pool_choice == 1):
            path_choice = random.choice(white_list_paths)
            self.xpos = 0
            self.ypos = 6
            self.path = get_paths()[path_choice + 2]
        elif(path_pool_choice == 2):
            path_choice = random.choice(white_list_paths)
            self.xpos = 0
            self.ypos = 11
            self.path = get_paths()[path_choice + 4]
        elif(path_pool_choice == 3):
            path_choice = random.choice(white_list_paths)
            self.xpos = 12
            self.ypos = 0
            self.path = get_paths()[path_choice + 6]
        elif(path_pool_choice == 4):
            path_choice = random.choice(white_list_paths)
            self.xpos = 13
            self.ypos = 5
            self.path = get_paths()[path_choice + 8]
        elif(path_pool_choice == 5):
            path_choice = random.choice(white_list_paths)
            self.xpos = 12
            self.ypos = 10
            self.path = get_paths()[path_choice + 10]

    def old_set_define_path(self):
        white_list = [0,1,2]
        white_list_paths = [0,1,2,3]
        path_pool_choice = random.choice(white_list)
        
        if(path_pool_choice == 0):
            path_choice = random.choice(white_list_paths)
            self.xpos = 0
            self.ypos = 1
            self.path = get_paths()[path_choice]
        elif(path_pool_choice == 1):
            path_choice = random.choice(white_list_paths)
            self.xpos = 0
            self.ypos = 11
            self.path = get_paths()[path_choice + 4]
        elif(path_pool_choice == 2):
            path_choice = random.choice(white_list_paths)
            self.xpos = 12
            self.ypos = 10
            self.path = get_paths()[path_choice + 8]
        

    def movement(self, space):

        #Check if the vehicle has been deployed
        if self.trip_begin == False:
            rng = random.choice(self.trip_spawn_rate)
            if(rng == 1):
                self.trip_begin = True
                space[self.ypos][self.xpos].curr_capacity += 1
                self.record('ypos', self.ypos)
                self.record('xpos', self.xpos)

        # If the agent has any moves left to do
        if self.curr_step < len(self.path) and self.trip_begin == True:
            choice = self.path[self.curr_step]
            # Check the choice from the macro
            if choice == 'w':
                #If valid, perform the move
                if valid_coordinate(self.ypos-1, self.xpos, space) and 'U' in space[self.ypos][self.xpos].direction and space[self.ypos-1][self.xpos].curr_capacity < space[self.ypos-1][self.xpos].max_capacity and space[self.ypos][self.xpos].can_advance:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.ypos -= 1
            elif choice == 'a':
                if valid_coordinate(self.ypos, self.xpos-1, space) and 'L' in space[self.ypos][self.xpos].direction and space[self.ypos][self.xpos-1].curr_capacity < space[self.ypos][self.xpos-1].max_capacity and space[self.ypos][self.xpos].can_advance:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.xpos -= 1
            elif choice == 's':
                if valid_coordinate(self.ypos+1, self.xpos, space) and 'D' in space[self.ypos][self.xpos].direction and space[self.ypos+1][self.xpos].curr_capacity < space[self.ypos+1][self.xpos].max_capacity and space[self.ypos][self.xpos].can_advance:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.ypos += 1
            elif choice == 'd':
                if valid_coordinate(self.ypos, self.xpos+1, space) and 'R' in space[self.ypos][self.xpos].direction and space[self.ypos][self.xpos+1].curr_capacity < space[self.ypos][self.xpos+1].max_capacity and space[self.ypos][self.xpos].can_advance:
                    agent_controller(choice, self.xpos, self.ypos, space)
                    self.curr_step += 1
                    self.xpos += 1
            # If the agent has arrived at its destination, despawn from the scene
            if(self.curr_step == len(self.path)):
                self.trip_end = True
                space[self.ypos][self.xpos].curr_capacity -= 1
            # Add the tracker
            self.trip_length += 1

        self.completion_percentage = (self.curr_step / len(self.path))*100
        self.trip_length_ratio = (self.trip_length / len(self.path))*100

        # Records
        self.record('trip_length', self.trip_length)
        self.record('trip_completion_rate', self.completion_percentage)
        self.record('trip_length_ratio', self.trip_length_ratio)
        self.record('ypos', self.ypos)
        self.record('xpos', self.xpos)


# Model class
class Model(ap.Model):
    def setup(self):
        self.space = initial_roads()
        self.vehicles = ap.AgentList(self, self.p.agents, Vehicle)
        self.street_lights = ap.AgentList(self, 1, Street_light)

    def get_average_trip_length(self):
        return round(sum(self.vehicles.trip_length) / self.p.agents, 2)

    def get_average_trip_completion_percentage(self):
        return round(sum(self.vehicles.completion_percentage) / self.p.agents, 2)
        
    def get_average_trips_completed(self):
        completed_trips = self.vehicles.select(self.vehicles.trip_end == True)
        return round(len(completed_trips) / self.p.agents, 2)
    
    def step(self):
        self.street_lights.check_state(self.space)
        self.vehicles.movement(self.space)
        #print()
        #print_new_roads(self.space)
        #time.sleep(0.1)
    
    def end(self):
        global runs_statistics
        buffer_array = []
        buffer_array.append(self.space)
        buffer_array.append(self.get_average_trip_length())
        buffer_array.append(self.get_average_trip_completion_percentage())
        buffer_array.append(self.get_average_trips_completed())
        runs_statistics.append(buffer_array)
        # Statistic in individual Run
        # print_new_roads(self.space)
        # print("Porcentaje de viajes completados: ", self.get_average_trips_completed())
        # print("Promedio de porcentaje de complecion de viaje", self.get_average_trip_completion_percentage())
        # print("Promedio de duracion de viaje", self.get_average_trip_length())

# Model Result = pandas´s dataframe
def dataFrame_to_JSON(df):
    json = df.to_json(orient = 'index')
    return json

def JSON_to_dataFrame(json):
    df = pd.read_json(json, orient = 'index')
    return df    

# Get global statistics from multiple Runs
def get_runs():
    
    blocked_cases = 0
    total_runs_trip_duration = 0
    total_runs_trip_completion_rate = 0
    total_runs_completed_trips_percentage = 0

    for i in range(0,10):
        model = Model(parameters)
        result = model.run()


    for i in range(len(runs_statistics)):
        if runs_statistics[i][2] < 73.0 and runs_statistics[i][3] < 0.6:
            blocked_cases += 1

        total_runs_trip_duration += runs_statistics[i][1]
        total_runs_trip_completion_rate += runs_statistics[i][2]
        total_runs_completed_trips_percentage += runs_statistics[i][3]

        # Statistics per run
        # print("Corrida ", i)
        # print_new_roads(runs_statistics[i][0])
        # print("Duracion Promedio de viaje: ", runs_statistics[i][1])
        # print("Porcentaje promedio de complecion de viaje: ", runs_statistics[i][2])
        # print("Porcentaje de viajes completados: ", runs_statistics[i][3])
        # print()

    average_run_trip_length = round(total_runs_trip_duration / len(runs_statistics), 2)
    average_run_trip_completion_rate = round(total_runs_trip_completion_rate / len(runs_statistics), 2)
    average_run_completed_trips_percentage = round(total_runs_completed_trips_percentage / len(runs_statistics), 2)

    print("-----------------------------------------")
    print("Corridas de simulacion: ", len(runs_statistics))
    print("Duracion promedio de viaje: ", average_run_trip_length)
    print("Porcentaje promedio de complecion de viaje: ", average_run_trip_completion_rate)
    print("Porcentaje de viajes completados: ", average_run_completed_trips_percentage)
    print("CASOS BLOQUEADOS TOTALES: ", blocked_cases)
    print()

# Generate a json file from the Run Dataframe
def generate_json():
    model = Model(parameters)
    result = model.run()

    variables = result.variables.Vehicle
    val_Y = variables['ypos'].values
    val_X = variables['xpos'].values

    steps = parameters["steps"]
    agents = parameters["agents"]
    
    split_lY = np.array_split(val_Y, agents)
    split_lX = np.array_split(val_X, agents)

    dic_json = {"parameters" : parameters}

    print(variables)

    for ag in range(agents):
        steps_aux = {}
        lg_splitY = split_lY[ag]
        lg_splitX = split_lX[ag]

        for step in range(steps):
            steps_aux[str(step+1)] = [int(lg_splitX[step]), int(lg_splitY[step])]
        dic_json[str(ag+1)] = steps_aux

    final_json = json.dumps(dic_json)
    return final_json

parameters = {
    'steps': 100,
    'agents': 100,
}

def main():
    model = Model(parameters)
    result = model.run()
    variables = result.variables.Vehicle
    
    # Dataframe 
    s_json = dataFrame_to_JSON(variables)
    #print(s_json)
    #print(variables.columns)

#main()
get_runs()
#print(generate_json())
