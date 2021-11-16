import agentpy as ap

# Initial matrix for the road system
def initial_roads():
    roads = [
    [1, 0, 0, 0], 
    [0, 'x', 'x', 0], 
    [0, 0, 0, 0], 
    [0, 0, 0, 0]]
    return roads

# Global variable for roads
road = initial_roads()
player_xpos = 0
player_ypos = 0

# Print matrix of the system
def print_roads(matriz):
    for ren in range(len(matriz)):
        for col in range(len(matriz[0])):
            print(matriz[ren][col], end=" ")
        print()

# VALIDAR RANGOS PARA QUE NO TRUENE EL ASUNTO
def valid_coordinate(ypos, xpos):
    if xpos <= 15 and ypos <= 15 and xpos >= 0 and ypos >= 0 and road[ypos][xpos] != 'x':
        return (True)
    return (False)
    
# Controller to make valid movements
def controller(x):
    global player_xpos
    global player_ypos
    global road
    
    if x == 'w':
        if valid_coordinate(player_ypos-1, player_xpos):
            player_ypos -= 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos+1][player_xpos] -= 1
            print("arriba")
    elif x == 'a':
        if valid_coordinate(player_ypos, player_xpos-1):
            player_xpos -= 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos][player_xpos+1] -= 1
            print("izquierda")
    elif x == 's':
        if valid_coordinate(player_ypos+1, player_xpos):
            player_ypos += 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos-1][player_xpos] -= 1
            print("abajo")
    elif x == 'd':
        if valid_coordinate(player_ypos, player_xpos+1):
            player_xpos += 1
            road[player_ypos][player_xpos] += 1
            road[player_ypos][player_xpos-1] -= 1
            print("derecha")
    else:
        print("movimiento invalido")

# Manual control for the simulation matrix
def simulation():
    curr_road = road
    x = ""
    while x != "-1":
        x = input("Movement: ")
        controller(x)
        print_roads(curr_road)
    print("End controller simulation")


def main():
    simulation()

main()