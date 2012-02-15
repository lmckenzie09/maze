#go through maze again. If any node has zero neighbors, add one
#go through if any node's previous is 


from sys import argv, exit
import random
from collections import defaultdict 

#Makes the center four squares completely are open, and
#only one path going into the goal
def make_goal(graph, neighbors, size):
  low_l = (size/2-1,size/2-1)
  up_l = (size/2-1,size/2)
  low_r = (size/2,size/2-1)
  up_r = (size/2,size/2)
#Each corner of the center is only connected to another center nodes
#And each center node is already marked as visited
  graph[low_l][1] = True
  graph[low_l][0].append(up_l)
  graph[low_l][0].append(low_r)
  neighbors[low_l] = list()
  
  graph[up_l][1] = True
  graph[up_l][0].append(up_r)
  graph[up_l][0].append(low_l)
  neighbors[up_l] = list()
  
  graph[up_r][1] = True
  graph[up_r][0].append(up_l)
  graph[up_r][0].append(low_r)
  neighbors[up_r] = list()
  
  graph[low_r][1] = True
  graph[low_r][0].append(up_r)
  graph[low_r][0].append(low_l)
  neighbors[low_r] = list()
  
  choices = list([low_l, up_l, up_r, low_r])
  random.shuffle(choices)
  x = choices.pop()
  i, j = x
#Figures out which corner of the center was picked from the list choices.
#Whichever node was chosen is what opens to the rest of the maze
  if graph[(i-1, j)][1] != True:
    if graph[(i, j+1)][1] != True:
      graph[(i,j)][0].append((i,j+1))
      graph[(i,j+1)][0].append((i,j))
      neighbors[(i,j+1)].remove((i,j))
      return (i, j+1)
    else:
      graph[(i,j)][0].append((i-1,j))
      graph[(i-1,j)][0].append((i,j))
      neighbors[(i-1,j)].remove((i,j))
      return (i-1,j)
  else:
    if graph[(i, j+1)][1] != True:
      graph[(i,j)][0].append((i,j+1))
      graph[(i,j+1)][0].append((i,j))
      neighbors[(i,j+1)].remove((i,j))
      return (i,j+1)
    else:
      graph[(i,j)][0].append((i,j-1))
      graph[(i,j-1)][0].append((i,j))
      neighbors[(i,j-1)].remove((i,j))
      return (i,j-1)

#Recursive function that visits every node in a random fashion and
#decides which node is connected to which
def visit(graph, neighbors, node, size):
  if graph[node][1] == True:
    return
  graph[node][1] = True;
#This loop executes for every neighbor of node
  while 1:
    if len(neighbors[node]) == 0:
#If a node has wound up with no neighbors, randomly give it one
      if len(graph[node][0]) == 0:
        x,y = node        
        add = list()
        if x-1 > 0:
          add.append((x-1,y))
        if y-1 > 0:
          add.append((x,y-1))
        if x+1 < size:
          add.append((x+1,y))
        if y+1 < size:
          add.append((x,y+1))
        new =random.choice(add)
        graph[node][0].append(new)
        graph[new][0].append(node)
      return
    random.shuffle(neighbors[node])
#chooses a random node out of the list of nodes neighboring 'node'
    next = neighbors[node][0]
    neighbors[node].pop(0)
#if next has been visited already, return
    if graph[next][1] == True:
      i,j = next
      if i == size/2 or i == size/2-1:
        if j == size/2 or j == size/2-1:
          visit(graph, neighbors, node, size)
      if len(graph[node][0]) == 0:
        graph[node][1] = False
        visit(graph, neighbors, node, size)
      return
#Make sure that node and next are not checked again as potential
#neighbors, and connect them by added them into each other's list in 
#the graph dict   
    neighbors[next].remove(node)    
    graph[node][0].append(next)
    graph[next][0].append(node)
    visit(graph, neighbors, next, size)

#method tha assures that each node is checked at least once
def make_walls(graph, neighbor, size):
  for i in range(size):
    for j in range(size):
      if False == graph[(i,j)][1]:
        visit(graph, neighbor, (i,j), size)

# def final_check(graph, size)
  # for i in range(size):
    # for j in range(size):
      # if graph[(i,j)]

        
#When printing out the graph, the very first character is a space
#Top line alternates between '_' and ' '
#Every element is checked for a path below the current position and a
#path to the right of the current position
#If there is no path below, print '_' else print ' '
#If there is no path to the right print '|' else print ' '
def print_graph(graph,size):
  str = ' '
  for x in range(size):
    str+= '_ '
  str+='\n'
  default = size-1;
  
  for j in range(size):
    str+='|'
    for i in range(size):
      if (i, (default-j-1)) not in graph[(i,default-j)][0]:
        str+='_'
      else:
        str+=' '
      if (i+1, default-j) not in graph[(i,default-j)][0]:
        str+='|'
      else:
        str+=' '
    str+='\n'
   
  print (str)

if __name__ == "__main__":
  if len(argv) < 2:
    print ('Usage: maze_gen height width')
    exit(1)
  
  size = int(argv[1])
  
  if size < 6 or size%2 == 1:
    print ('Incorrect size. Must be even. Min: 6')
    exit(1)
#Neighbor dict is used to hold all possible unvisited neighbors for
#every node  
  neighbors = defaultdict(list)
  for node in [(i,j) for i in range(size) for j in range(size)]:
    x, y = node
    if x != 0:
      neighbors[node].append((x-1,y))
    if y != 0:
      neighbors[node].append((x,y-1))
    if x != size-1:
      neighbors[node].append((x+1,y))
    if y != size-1:
      neighbors[node].append((x,y+1))
#graph dict is used to actually tell which node is connected to which
#for each key in graph you get a list of surrounding neighbors
#and whether that node has been visited or not
  graph = defaultdict(list)
  for  node in [(i,j) for i in range(size) for j in range(size)]:
    graph[node].insert(0,list())
    graph[node].insert(1,False)
  start = make_goal(graph, neighbors, size)
  visit(graph, neighbors, start, size)
  make_walls(graph,neighbors,size)
  print_graph(graph, size)