class BoardTile(object):
    
  def __init__(self, initialStateList, move="", parent=None, depth=0):
    self.array = initialStateList
    self.move = move
    self.parent = parent
    self.depth = depth
    
  def left(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position % 3 == 0: #first column cannot move left
      return None
    else:
      mylist[position-1], mylist[position] = mylist[position], mylist[position-1]
    return BoardTile(mylist, "Left", self, self.depth+1)

  def right(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [2,5,8]: #last column cannot move right
      return None
    else:
      mylist[position+1], mylist[position] = mylist[position], mylist[position+1]
    return BoardTile(mylist, "Right", self, self.depth+1)

  def up(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [0,1,2]:
      return None
    else:
      mylist[position-3], mylist[position] = mylist[position], mylist[position-3]
    return BoardTile(mylist, "Up", self, self.depth+1)

  def down(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [6,7,8]:
      return None
    else:
      mylist[position+3], mylist[position] = mylist[position], mylist[position+3]
    return BoardTile(mylist, "Down", self, self.depth+1)

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

  def dfs_children(self):
    store=[]
    u = self.up()
    l = self.left()
    r = self.right()
    d = self.down()

    if r != None:
      store.append(r)
    if l != None:
      store.append(l)
    if d != None:
      store.append(d)
    if u != None:
      store.append(u)
    return store

  def getStart(self):
    return self.array

  def getCurrent(self):
    return self.current

  def manhattan_distance(self):
    m = 0
    for index,elem in enumerate(self.array):
      if elem != '0':
        current_x,current_y = self.__coordinates__(index)
        goal_x,goal_y = self.__end_state_distance__(elem)
        m += abs(current_x - goal_x) + abs(current_y - goal_y)
    return m

  def __coordinates__(self,index):
    #return x,y for given index in any state of the board
    x={0:0, 1:1, 2:2, 3:0, 4:1, 5:2, 6:0, 7:1, 8:2}
    y={0:2, 1:2, 2:2, 3:1, 4:1, 5:1, 6:0, 7:0, 8:0}
    return x[index],y[index]
  
  def __end_state_distance__(self,number):
    #for a given number, return the desired x,y co-ordinates for the end state
    x={'1':1, '2':2, '3':0, '4':1, '5':2, '6':0, '7':1, '8':2}
    y={'1':2, '2':2, '3':1, '4':1, '5':1, '6':0, '7':0, '8':0}
    return x[number],y[number]


  def __eq__(self,other):
    if other == None:
      return False
    else:
      return self.array == other.array

  def __ne__(self,other):
    return not self.__eq__(other)

  def __hash__(self):
    #return id(self)
    return hash(tuple(self.array))

  def __str__(self):
    return "[" + ",".join(self.array) + "]"
  
  def getMove(self):
    return self.move

  def getParent(self):
    return self.parent

class PriorityQueue(object):
  from itertools import count
  from heapq import heappush
  from heapq import heappop

  def __init__(self):
    self.pq = []                         # list of entries arranged in a heap
    self.entry_finder = {}               # mapping of games to entries
    self.REMOVED = '<removed-game>'      # placeholder for a removed game
    self.counter = self.count()               # unique sequence count
    self.length = 0

  def add_game(self, game, priority=0):
    'Add a new game or update the priority of an existing game'
    if game in self.entry_finder:
        self.remove_game(game)
    count = next(self.counter)
    entry = [priority, count, game]
    self.entry_finder[game] = entry
    self.heappush(self.pq, entry)
    self.length += 1
      

  def remove_game(self, game):
    'Mark an existing game as REMOVED.  Raise KeyError if not found.'
    entry = self.entry_finder.pop(game)
    entry[-1] = self.REMOVED
    self.length -= 1

  def pop_game(self):
    'Remove and return the lowest priority game. Raise KeyError if empty.'
    while self.pq:
      priority, count, game = self.heappop(self.pq)
      if game is not self.REMOVED:
        del self.entry_finder[game]
        self.length -= 1
        return game
    raise KeyError('pop from an empty priority queue')

  def lowest_priority(self):
    'Return the lowest priority on the queue'
    mypq = sorted(self.pq)
    while mypq:
      priority, count, game = mypq.pop(0)
      if game is not self.REMOVED:
        return priority
    raise KeyError('lowest_priority for an empty priority queue')

  
  def length(self):
    return self.length

class Driver(object):
  import time as time
  import resource as resource
  import sys
  from collections import deque

  def __init__(self):
    pass


  def bfs(self,initialState):
    from collections import deque
    fringer=1
    initialList = initialState.split(",")
    startState = BoardTile(initialList)
    frontier = deque()
    frontier.append(startState)
    explored = deque()
    nodes_expanded = 0
    exclusions = set()
    max_search_depth = 0
    
    import resource
    import time
    t = time.time()
    while not len(frontier) == 0:
      state = frontier.popleft()
      explored.append(state)
      exclusions.add(state)
      #print("CURRENTLY EXPLORING...", state)
      #print("EXPLORED: ", *explored)

      if self.goalTest(state):
        duration = time.time() - t
        ramUsed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
        self.__print_results__(state,frontier,explored,duration, nodes_expanded, ramUsed, fringer, max_search_depth)
        print('SUCCESS')
        return
      
      children = state.children()
      nodes_expanded = nodes_expanded + 1 
      #unions = set(frontier).union(explored)
      for child in children:
        #print("CHILD: ", child.getStart())

        if child in exclusions:
          pass
        else:
          #print("Appending: ", child)
          frontier.append(child)
          exclusions.add(state)
          if child.depth > max_search_depth:
            max_search_depth = child.depth
      if len(frontier) > fringer:
        fringer = len(frontier)
      #print("FRONTIER: ", *frontier)

    import sys
    sys.exit("ALGORITHM FAILURE")
    return

  def dfs(self,initialState):
    from collections import deque
    fringer=1
    initialList = initialState.split(",")
    startState = BoardTile(initialList)
    frontier = deque()
    frontier.append(startState)
    explored = set()
    exclusion = set()
    exclusion.add(startState)
    nodes_expanded = 0
    max_search_depth = 0

    import resource
    import time
    t = time.time()
    while not len(frontier) == 0:
    #while nodes_expanded != 190000 :
      #print("FRONTIER: ", *frontier)
      state = frontier.pop()
      explored.add(state)
      exclusion.add(state)
      #print("CURRENTLY EXPLORING...", state)
      #print("EXPLORED: ", *explored)
      #print("NODES EXPANDED: ", nodes_expanded)
      if self.goalTest(state):
        print('SUCCESS')
        duration = time.time() - t
        ramUsed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
        self.__print_results__(state,frontier,explored,duration, nodes_expanded, ramUsed, fringer, max_search_depth)
        return
      
      children = state.dfs_children()

      nodes_expanded = nodes_expanded + 1 
      
      #print("UNIQUE CHILDREN:...", *unique_children)

      for child in children:
        #print("CHILD: ", child.getStart())
        if child in exclusion:
          pass
        else:
          #print("Appending: ", child)
          frontier.append(child)
          exclusion.add(child)
          if child.depth > max_search_depth:
            max_search_depth = child.depth
      l = len(frontier)
      if l > fringer:
        fringer = l

    import sys
    sys.exit("ALGORITHM FAILURE")

  def astar(self,initialState):
    from collections import deque
    nodes_expanded = 0
    fringer = 1
    max_search_depth = 0
    initialList = initialState.split(",")
    startState = BoardTile(initialList)
    frontier = PriorityQueue()
    frontier.add_game(startState)
    explored = set()
    exclusion = set()
    exclusion.add(startState)

    t = self.time.time()

    while not frontier.length == 0:
      state = frontier.pop_game()
      explored.add(state)
      exclusion.add(state)

      if self.goalTest(state):
        print('SUCCESS')
        duration = self.time.time() - t
        ramUsed = self.resource.getrusage(self.resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
        self.__print_results__(state,frontier,explored,duration, nodes_expanded, ramUsed, fringer, max_search_depth)
        return

      children = state.children()
      nodes_expanded += 1
      for child in children:
        if child in exclusion:
          pass
        else:
          frontier.add_game(child, child.depth + child.manhattan_distance())
          exclusion.add(child)
          if child.depth > max_search_depth:
            max_search_depth = child.depth
      l = frontier.length
      if l > fringer:
        fringer = l

    import sys
    sys.exit("ALGORITHM FAILURE")

  def __limited_ast__(self,initialState,limit):
    from collections import deque
    fringer=1
    initialList = initialState.split(",")
    startState = BoardTile(initialList)
    frontier = PriorityQueue()
    frontier.add_game(startState)
    explored = set()
    exclusion = set()
    exclusion.add(startState)
    nodes_expanded = 0
    max_search_depth = 0
    return_list = list()

    import resource
    import time
    t = time.time()
    while frontier.length:
    #while nodes_expanded != 190000 :
      #print("FRONTIER: ", *frontier)
      state = frontier.pop_game()
      explored.add(state)
      exclusion.add(state)
      #print("CURRENTLY EXPLORING...", state)
      #print("EXPLORED: ", *explored)
      #print("NODES EXPANDED: ", nodes_expanded)
      if self.goalTest(state):
        print('SUCCESS')
        duration = time.time() - t
        ramUsed = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)
        self.__print_results__(state,frontier,explored,duration, nodes_expanded, ramUsed, fringer, max_search_depth)
        return -9
      
      children = state.children()

      nodes_expanded = nodes_expanded + 1 
      
      #print("UNIQUE CHILDREN:...", *unique_children)

      for child in children:
        #print("CHILD: ", child.getStart())
        functional_distance = child.depth + child.manhattan_distance()
        if child in exclusion:
          pass
        elif functional_distance > limit:
          return_list.append(functional_distance)
        else:
          #print("Appending: ", child)
          frontier.add_game(child, functional_distance)
          exclusion.add(child)
          if child.depth > max_search_depth:
            max_search_depth = child.depth
      l = frontier.length
      if l > fringer:
        fringer = l

    return return_list

  def ida(self,initialState):
    max_limit = 200000
    current_limit = BoardTile(initialState.split(",")).manhattan_distance()
    priorities = list()

    while current_limit < max_limit:
      print("CURRENT LIMIT: ", current_limit)
      result = self.__limited_ast__(initialState,current_limit)
      if type(result) is list: 
        for r in result:
          priorities.append(r)
      elif result == -9:
        return
      
      priorities = sorted(priorities)
      while priorities:
        p = priorities.pop(0)
        if p > current_limit:
          current_limit = p
          break



  def __print_results__(self,state,frontier,explored, duration, nodes_expanded, ram_used, max_fringe_size, max_search_depth):
    f = open("output.txt", "w")
    shortestPath = self.findShortestPath(state)
    f.write('path_to_goal: ' + str(shortestPath) + '\n')
    f.write('cost_of_path: ' + str(len(shortestPath)) + '\n')
    f.write('nodes_expanded: ' + str(nodes_expanded) + '\n')
    if type(frontier) is self.deque:
      f.write('fringe_size: ' + str(len(frontier)) + '\n')
    elif type(frontier) is PriorityQueue:
      f.write('fringe_size: ' + str(frontier.length) + '\n')
    f.write('max_fringe_size: ' + str(max_fringe_size) + '\n')
    f.write('search_depth: ' + str(state.depth) + '\n')
    f.write('max_search_depth: ' + str(max_search_depth) + '\n')
    f.write('running_time: ' + str(duration) + '\n')
    f.write('max_ram_usage: ' + str(ram_used) + '\n')
    f.close()

  def goalTest(self, state):
    #print("START: ", state.getStart())
    return state.array == ['0','1','2','3','4','5','6','7','8']

  def findShortestPath(self, state, store=[]):
    #if state.getMove() == '':
      #return store
    
    #store.insert(0,state.getMove())
    #return self.findShortestPath(state.getParent(), store)
    #store = []
    while state.getParent() != None:
      store.insert(0,state.getMove())
      state = state.getParent()
    return store

    

  #def findSearchDepth(self, state, count=0):
    #if state.getParent() == None:
      #return count
     
    #return self.findSearchDepth(state.getParent(), count+1)

  #def maxSearchDepth(self, frontier):
    #depths = []
    #for node in frontier:
      #depths.append(self.findSearchDepth(node))
    #return max(depths)
    
####### MAIN PROGRAM EXECUTION ##############
BoardTile(['2','1','3','5','4','0','6','7','8']).manhattan_distance()
import sys
search_type = sys.argv[1]
board_string = sys.argv[2]
driver = Driver()
if search_type == 'bfs':
  driver.bfs(board_string)
elif search_type == 'dfs':
  driver.dfs(board_string)
elif search_type == 'ast':
  driver.astar(board_string)
elif search_type == 'ida':
  driver.ida(board_string)
