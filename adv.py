from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

seed = random.randint(0, 217120)
random.seed(185393)

def reverse(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    else:
        return 'e'
    

def new_entry(room, visited_rooms):
    visited_rooms[room.id] = {}
    
    for exit_direction in room.get_exits():
        visited_rooms[room.id][exit_direction] = '?'
        

        
def bfs(visited_rooms):
    room = player.current_room
    q = Queue()
    q.enqueue([room.id])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        last = path[-1]
        if last not in visited:
            visited.add(last)
            for exit_direction in visited_rooms[last]:
                if (visited_rooms[last][exit_direction] == '?'):
                    return path
                elif (visited_rooms[last][exit_direction] not in visited):
                    new_path = path + [visited_rooms[last][exit_direction]]
                    q.enqueue(new_path)
                
    return path
        

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited_rooms = {}

while(len(visited_rooms) < len(room_graph)):
    
    if player.current_room.id not in visited_rooms:
        new_entry(player.current_room, visited_rooms)
        
    exits = []
    for new_direction in visited_rooms[player.current_room.id]:
        if (visited_rooms[player.current_room.id][new_direction] == '?'):
            exits.append(new_direction)
            
    if (len(exits) == 0):
        path = bfs(visited_rooms)
        # translate room id to direction
        for id in path:
            for exit_direction in visited_rooms[player.current_room.id]:
                if (exit_direction in visited_rooms[player.current_room.id]):
                    # print (f"Current room is {player.current_room.id} and direction is {exit_direction}")
                    if (visited_rooms[player.current_room.id][exit_direction] == id and player.current_room.id != id):
                        traversal_path.append(exit_direction)
                        new_room = player.current_room.get_room_in_direction(exit_direction)
                        visited_rooms[player.current_room.id][exit_direction] = new_room.id
                        if (new_room.id not in visited_rooms):
                            new_entry(new_room, visited_rooms)
                        visited_rooms[new_room.id][reverse(exit_direction)] = player.current_room.id
                        player.travel(exit_direction)
                        
    else:
        new_exit = random.choice(exits)
        traversal_path.append(new_exit)
        new_room = player.current_room.get_room_in_direction(new_exit)
        visited_rooms[player.current_room.id][new_exit] = new_room.id
        if (new_room.id not in visited_rooms):
            new_entry(new_room, visited_rooms)
        visited_rooms[new_room.id][reverse(new_exit)] = player.current_room.id
        player.travel(new_exit)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
#while True:
    #cmds = input("-> ").lower().split(" ")
    #if cmds[0] in ["n", "s", "e", "w"]:
        #player.travel(cmds[0], True)
    #elif cmds[0] == "q":
        #break
    #else:
        #print("I did not understand that command.")
        
        
        
# Traversal
#def traversal(visited=None, previous=None, came_from=None):
 #   # Then we set the current room with the player inside and ID
  #  current_room = player.current_room.id
    # Then we show all avaiable exits
   # exits = player.current_room.get_exits()
    # Then all possible reverse
    #reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    # Check if visited or not
    #if visited is None:
        # create dictionary
     #   visited = {}
    # if its not visisted, we check
    #if current_room not in visited:
     #   visited[current_room] = {}
    # Check the previous node if were not on the first node
    #if previous:
        # how did we get to the current room from the previous?
     #   visited[previous][came_from] = current_room
        # how would we have to get back to the previous 
      #  visited[current_room][reverse[came_from]] = previous
    # now we check on the direction on the exits
    #for direction in exits:
        # if its not in visisted
     #   if direction not in visited[current_room]:
            # we then append (add) onto the existing list
      #      traversal_path.append(direction)
            # we get the direction the player was travelling
       #     player.travel(direction)
            # for each possible direction in every node, we repeat this for loop
        #    traversal(visited, previous=current_room, came_from=direction)
    # however, if the direction is in visisted and we have not yet touched all the nodes
   # if len(visited) < len(room_graph):
        # we then retrace the steps to find out where we came from
    #    retrace = reverse[came_from]
        # we retrace the players travel
     #   player.travel(retrace)
        # we then append (add) what we retrace onto the existing list
      #  traversal_path.append(retrace)
#traversal()
