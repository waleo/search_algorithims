class BoardTile(object):
    
  def __init__(self, initialStateList, moves=[]):
    self.array = initialStateList
    self.moves = moves
    
  def left(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position % 3 == 0: #first column cannot move left
      return None
    else:
      mylist[position-1], mylist[position] = mylist[position], mylist[position-1]
      self.moves.append('Left')
    return BoardTile(mylist, self.moves)

  def right(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [2,5,8]: #last column cannot move right
      return None
    else:
      mylist[position+1], mylist[position] = mylist[position], mylist[position+1]
      self.moves.append('Right')
    return BoardTile(mylist, self.moves)

  def up(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [0,1,2]:
      return None
    else:
      mylist[position-3], mylist[position] = mylist[position], mylist[position-3]
      self.moves.append('Up')
    return BoardTile(mylist, self.moves)

  def down(self):
    mylist = self.array.copy()
    position = mylist.index("0")
    if position in [6,7,8]:
      return None
    else:
      mylist[position+3], mylist[position] = mylist[position], mylist[position+3]
      self.moves.append('Down')
    return BoardTile(mylist, self.moves)

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
  
  def getMoves(self):
    return self.moves

class Driver(object):

  def __init__(self):
    pass

  def bfs(self,initialState):
    from collections import deque
    initialList = initialState.split(",")
    startState = BoardTile(initialList)
    frontier = deque()
    frontier.append(startState)
    explored = set()

    while not len(frontier) == 0:
      state = frontier.popleft()
      explored.add(state)
      print("CURRENTLY EXPLORING...", state)

      if self.goalTest(state):
        print('SUCCESS')
        print("MOVES: ", state.getMoves())
        return
      
      print("EXPLORED: ", *explored)
      for child in state.children():
        print("CHILD: ", child.getStart())

        if child in frontier or child in explored:
          pass
        else:
          #print("Appending: ", child)
          frontier.append(child)
      print("FRONTIER: ", *frontier)

    print('FAILURE')
    return

  def goalTest(self, state):
    #print("START: ", state.getStart())
    return state == BoardTile(['0','1','2','3','4','5','6','7','8'])
    
driver = Driver()
driver.bfs("1,2,5,3,4,0,6,7,8")
