from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import logging
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

def get_paths():
    file = open('unity_path_macros.csv')
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
                print('◌', end=" ")
            else:
                if(roads[ren][col].curr_capacity != 0):
                    print('■', end=' ')
                else:
                    print('▴', end=" ")
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

        self.right_lane_lights = [[1,3],[6,3],[11,3],[1,9],[3,10],[6,8],[9,10],[11,9]]
        self.left_lane_lights = [[0,6],[5,6],[10,6],[2,11],[8,11],[10,12]]

    def check_state(self, space):
        if self.clock == 5:
            self.clock = 0
            self.state = not self.state
            self.update_state(space)
        
        self.clock += 1

    def update_state(self, space):
        print()
        if(self.state):
            print('GREEN FOR RIGHT LANE')
            for i in range(0, len(self.right_lane_lights)):
                ypos = self.right_lane_lights[i][0]
                xpos = self.right_lane_lights[i][1]
                space[ypos][xpos].can_advance = True
            for i in range(0, len(self.left_lane_lights)):
                ypos = self.left_lane_lights[i][0]
                xpos = self.left_lane_lights[i][1]
                space[ypos][xpos].can_advance = False
        else:
            print('GREEN FOR LEFT LANE')
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
        self.trip_spawn_rate = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # KPI's
        self.completion_percentage = 0
        self.trip_length = 0

        # Initialize variables
        self.set_define_path()

    def set_define_path(self):
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
        self.record('trip_length', self.trip_length)
        self.record('trip_completion_rate', self.completion_percentage)
        self.record('ypos', self.ypos)
        self.record('xpos', self.xpos)

# Model class
class Model(ap.Model):
    def setup(self):
        self.space = initial_roads()
        self.vehicles = ap.AgentList(self, self.p.agents, Vehicle)
        self.street_lights = ap.AgentList(self, 1, Street_light)
    
    def step(self):
        self.street_lights.check_state(self.space)
        self.vehicles.movement(self.space)
        print()
        #print_new_roads(self.space)
        time.sleep(0.14)

parameters = {
    'steps': 150,
    'agents': 50,
}

#parameters = pandas´s dataframe
def dataFrame_to_JSON(df):
    json = df.to_json(orient = 'index')
    return json

def JSON_to_dataFrame(json):
    df = pd.read_json(json, orient = 'index')
    return df    

def main():
    # global road_history
    model = Model(parameters)
    result = model.run()
    variables = result.variables.Vehicle
    

    #print(dataFrame_to_JSON(variables))

def generar_json():
    model = Model(parameters)
    result = model.run()
    variables = result.variables.Vehicle
    s_json = dataFrame_to_JSON(variables)
    return s_json

#main()

#----------------SERVER----------------

#El rey del server:
class Server(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                     str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(
            self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        #post_data = self.rfile.read(content_length)
        post_data = json.loads(self.rfile.read(content_length))
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))

        # AQUI ACTUALIZA LO QUE SE TENGA QUE ACTUALIZAR
        self._set_response()
        #AQUI SE MANDA EL SHOW
        resp = "{\"data\":" + generar_json() + "}"
        #print(resp)
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")  # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
