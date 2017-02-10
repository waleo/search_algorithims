class BoardTile(object):
    
  def __init__(self, initialStateList, move="", parent=None):
    self.array = initialStateList
    self.move = move
    self.parent = parent
    
  def left(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position % 3 == 0: #first column cannot move left
      return None
    else:
      mylist[position-1], mylist[position] = mylist[position], mylist[position-1]
    return BoardTile(mylist, "Left", self)

  def right(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [2,5,8]: #last column cannot move right
      return None
    else:
      mylist[position+1], mylist[position] = mylist[position], mylist[position+1]
    return BoardTile(mylist, "Right", self)

  def up(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [0,1,2]:
      return None
    else:
      mylist[position-3], mylist[position] = mylist[position], mylist[position-3]
    return BoardTile(mylist, "Up", self)

  def down(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [6,7,8]:
      return None
    else:
      mylist[position+3], mylist[position] = mylist[position], mylist[position+3]
    return BoardTile(mylist, "Down", self)

  def children(self):
    store=[]
    u = self.up()
    l = self.left()
    r = self.right()
    d = self.down()

    if u != None:
      store.append(u)
    if d != None:
      store.append(d)
    if l != None:
      store.append(l)
    if r != None:
      store.append(r)
    return store

  def getStart(self):
    return self.array

  def getCurrent(self):
    return self.current

  def __eq__(self,other):
    if other == None:
      return False
    else:
      return self.getStart() == other.getStart()

  def __hash__(self):
    return hash("".join(self.getStart()))

  def __str__(self):
    return "[" + ",".join(self.array) + "]"
  
  def getMove(self):
    return self.move

  def getParent(self):
    return self.parent

class Driver(object):

  def __init__(self):
    pass


  def bfs(self,initialState):
    from collections import deque
    initialList = initialState.split(",")
    startState = BoardTile(initialList)
    frontier = deque()
    frontier.append(startState)
    explored = deque()
    nodes_expanded = 0
    
    import resource
    import time
    t = time.time()
    while not len(frontier) == 0:
      state = frontier.popleft()
      explored.append(state)
      print("CURRENTLY EXPLORING...", state)
      print("EXPLORED: ", *explored)

      if self.goalTest(state):
        duration = time.time() - t
        ramUsed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
        print('SUCCESS')
        #print("MOVES: ", state.getMoves())
        f = open("output.txt", "w")
        shortestPath = self.findShortestPath(state)
        f.write('path_to_goal: ' + str(shortestPath) + '\n')
        f.write('cost_of_path: ' + str(len(shortestPath)) + '\n')
        f.write('nodes_expanded: ' + str(nodes_expanded) + '\n')
        f.write('fringe_size: ' + str(len(frontier)) + '\n')
        f.write('max_fringe_size: ' + str(len(frontier) + 1) + '\n')
        f.write('search_depth: ' + str(self.findSearchDepth(state)) + '\n')
        f.write('max_search_depth: ' + str(self.maxSearchDepth(frontier)) + '\n')
        f.write('running_time: ' + str(duration) + '\n')
        f.write('max_ram_usage: ' + str(ramUsed) + '\n')
        f.close()
        return
      
      children = state.children()
      nodes_expanded = nodes_expanded + 1 
      for child in children:
        print("CHILD: ", child.getStart())

        if child in frontier or child in explored:
          pass
        else:
          #print("Appending: ", child)
          frontier.append(child)
      print("FRONTIER: ", *frontier)

    import sys
    sys.exit("ALGORITHM FAILURE")
    return

  def goalTest(self, state):
    #print("START: ", state.getStart())
    return state == BoardTile(['0','1','2','3','4','5','6','7','8'])

  def findShortestPath(self, state, store=[]):
    if state.getMove() == '':
      return store
    
    store.insert(0,state.getMove())
    return self.findShortestPath(state.getParent(), store)

    

  def findSearchDepth(self, state, count=0):
    if state.getParent() == None:
      return count
     
    return self.findSearchDepth(state.getParent(), count+1)

  def maxSearchDepth(self, frontier):
    depths = []
    for node in frontier:
      depths.append(self.findSearchDepth(node))
    return max(depths)
    
####### MAIN PROGRAM EXECUTION ##############
import sys
search_type = sys.argv[1]
board_string = sys.argv[2]
driver = Driver()
if search_type == 'bfs':
  driver.bfs(board_string)
