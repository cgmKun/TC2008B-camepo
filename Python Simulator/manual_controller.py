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


# Global variable for roads and testing
roadx = initial_roads()
road_history = []
player_xpos = 0
player_ypos = 0

# Print matrix of the system


def print_new_roads(roads):
    for ren in range(len(roads)):
        for col in range(len(roads[0])):
            print(roads[ren][col].curr_capacity, end=" ")
        print()


def valid_coordinate_roads(ypos, xpos, road):
    if xpos <= len(road) and ypos <= len(road[0]) and xpos >= 0 and ypos >= 0:
        return True
    return False

# Controller to make valid movements


def manual_controller(x):
    global player_xpos
    global player_ypos
    global roadx
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

# Manual control for the simulation matrix


def simulation():
    global roadx

    #SPAWN POINT
    roadx[0][0].curr_capacity += 1

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


def main():
    simulation()


main()
