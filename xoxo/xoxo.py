import os
import random as rand
import configparser as cp
import colorterm
import pdb

#не сходить на досках размера > 9


def cls():
  os.system('cls' if os.name == 'nt' else 'clear')
  
class GAMEST:
  gamerun = 2
  quitexit = 4
  mainmenu = 1
  winview = 3
  initState = 0

class GameState:
  boardSize = 5
  emptyCell = "."
  xtile = "X"
  otile = "O"
  turn = 0
  maxTurns = boardSize * boardSize
  winline = []
  w = False
  lastTurn = (0, 0)
  playerOneName = 'Player 1'
  playerTwoName = 'Player 2'
  playerOneWins = 0
  playerTwoWins = 0
  state = GAMEST.initState
  needInLine = 3
  bots = 0
  stepHistory = []

  board = [list(emptyCell * boardSize)] * boardSize
  xoturn = xtile
  
  def setState(self, st):
    self.state = st
    
  def state2MainMenu(self):
    self.setState(GAMEST.mainmenu)
  
  def state2Exit(self):
    self.setState(GAMEST.quitexit)
  
  def state2WinView(self):
    self.setState(GAMEST.winview)
    cls()
    self.printBoard()
    print("win", self.whowin)
    input("Press any key")
    self.state2MainMenu()
  
  def state2GameRun(self, bots = 0):
    self.setState(GAMEST.gamerun)
    self.gameNewStart(bots)
  
  def __init__(self, size = 5):
    pass
    
  def stateHandle(self):
    stateEvents = {
      GAMEST.gamerun : self.gameStep,
      GAMEST.mainmenu: self.mainMenu,
      GAMEST.quitexit: lambda: True
    }
    fun = stateEvents.get(self.state)
    return fun() # isEnd?

    
  def printBoard(self):
    cls()
    if self.w == None:
      w = 'draw'
    elif self.w :
      w = self.xoturn
    else:
      w = 'no'
    self.whowin = w
    lastNhistory = self.stepHistory[-self.boardSize : -1]
    
    print('    ' + self.headerNum)
    linevars = {
      1: "Turn: " + str(self.turn),
      2: "Player: " + self.xoturn,
      3: "Win: " + str(w), #+ str(self.winline),
      4: "Last turn: " + str(self.lastTurn),
      5: self.playerOneName + ' (X) wins: ' + str(self.playerOneWins),
      6: self.playerTwoName + ' (O) wins: ' + str(self.playerTwoWins)
    }
    print(('   ' + "-" * (self.boardSize + 2)).ljust(30 + self.boardSize + 6) \
      + "Last", str(self.boardSize) ,"steps")
    i = 1
    for x in range(0, self.boardSize):
      line = str(i).ljust(3) + '|'
      tiles = ''
      for y in range(0, self.boardSize):
        if (x,y) in self.winline:
          tiles += colorterm.gtextr(self.board[x][y])
        else:
          tiles += self.board[x][y]
      line += tiles
      line += '| ' + linevars.get(i, "").ljust(30)
      hist = ''
      if len(lastNhistory) > i - 1:
        hx, hy, ht = lastNhistory[i - 1] 
        hist = '' + str(ht) + ': ' + str(hx) + ', ' + str(hy)
      line += hist 
      print (line)
      i += 1
    print('   ' + "-" * (self.boardSize + 2))
  
    
  def putAt(self, x, y, e):
    self.board[x]= list(self.board[x][:y] + [e] + self.board[x][y+1:])
  
  def getAt(self, x, y):
    return self.board[x][y]

  def step(self, x, y):
    if self.board[x][y] == self.emptyCell:
      self.putAt(x, y, self.xoturn)
      self.stepHistory += [(x + 1, y + 1, self.xoturn)]
      self.w = self.winCheck(x, y)
      if self.w:
        self.state2WinView()
        #colorterm.ctextc(str(self.winline))
        
        if self.xoturn == self.xtile:
          self.playerOneWins += 1
        else: 
          self.playerTwoWins += 1
          
      elif self.w == None: #draw
        self.state2WinView()
        
      self.turn += 1
      self.lastTurn = (y + 1, x + 1)
      
      if self.xoturn == self.xtile:
        self.xoturn = self.otile
      else:
        self.xoturn = self.xtile

  def query(self):
    x = y = -1
    while not (0 <= x < self.boardSize and 0 <= y < self.boardSize):
      try:
        y, x= input("enter xy (qq:quit):")
      except:
        x = y = -1
      if (y == 'q'):
        self.state2MainMenu()
        return
      x = int(x) - 1
      y = int(y) - 1
      try:
        if self.board[x][y] != self.emptyCell:
          x = y = -1
      except:
        x = y = -1
      self.printBoard()
      if not (0 <= x < self.boardSize and 0 <= y < self.boardSize):
        colorterm.ctextr("Invalid input")
      
    self.step(x, y)

  #TODO: Сделать чтобы находил максимальную линию.
  def winCheck(self, x, y):
    #pdb.set_trace()
    self.winline = []
    if self.turn == self.maxTurns:
      return None
    col = row = diag = rdiag = 0
    n = self.needInLine
    winlineRow = []
    winlineCol = []
    winlineDiag = []
    winlineRDiag = []
    for i in range(0, self.boardSize):
      if col == n or row ==n or diag == n or rdiag == n:
        if row == n:
          self.winline = winlineRow
        elif col == n:
          self.winline = winlineCol
        elif diag == n:
          self.winline = winlineDiag
        elif rdiag == n:
          self.winline = winlineRDiag

        return True
      if self.board[x][i] == self.xoturn:
        col += 1
        winlineCol += [(x, i)]
      else:
        col = 0
        winlineCol = []
      if self.board[i][y] == self.xoturn:
        row += 1
        winlineRow += [(i, y)]
      else:
        row = 0
        winlineRow = []
      if self.board[i][i] == self.xoturn:
        diag += 1
        winlineDiag += [(i, i)]
      else:
        diag = 0
        winlineDiag = []
      if self.board[i][n-i+1] == self.xoturn:
        rdiag += 1
        winlineRDiag += [(i, n-i+1)]
      else:
        rdiag = 0
        winlineRDiag = []

    if row == n:
      self.winline = winlineRow
    elif col == n:
      self.winline = winlineCol
    elif diag == n:
      self.winline = winlineDiag
    elif rdiag == n:
      self.winline = winlineRDiag
    
    return row == n or col == n or diag == n or rdiag == n
        
  def gameStep(self):
    self.printBoard()
    if self.bots == 0:
      self.query()
    elif self.bots == 1:
      self.query()
      self.botStepXY()
    elif self.bots == 2:
      self.botStepXY()
      self.botStepXY()
    
  def gameNewStart(self, bots = 0):
    self.board = [list(self.emptyCell * self.boardSize)] * self.boardSize
    #self.board = testboard
    self.xoturn = self.xtile
    self.w = False
    self.winline = []
    self.bots = bots
    self.maxTurns = self.boardSize * self.boardSize
    self.turn = 0
    self.stepHistory = []
      
  # сделать потом альтернативное меню с навигацией
  def mainMenu(self):
    def key(k):
      return '(' + str(k) + ') : '
      
    menL = [
      ('n', ("New game with bot", lambda: self.state2GameRun(1))),
      ('p', ("New game 2 players", self.state2GameRun)),
      ('r', ("New game 2 bots", lambda: self.state2GameRun(2))),
      ('s', ("Settings. Change players names", 0)),
      ('q', ("exit", self.state2Exit))
      
    ]
    men = dict(menL)
    cls()
    colorterm.ctextbr(self.playerOneName + ' (X) wins: ' + str(self.playerOneWins))
    colorterm.ctextbr(self.playerTwoName + ' (O) wins: ' + str(self.playerTwoWins))
    for k, (s, _) in menL:
      print(key(k) + s)
    try:
      x = input("Choose: ")
    except:
      x = -1
    (_, fun) = men.get(x, (0, lambda:False))
    if fun:
      fun()
  
  def start(self):
    configFileName = 'cxoxo.ini'
    config = cp.ConfigParser()
    config.read(configFileName)
    self.boardSize = int(config['main']['boardSize']) or 5
    self.playerOneName = config['main']['PlayerOneName'] or '.'
    self.playerTwoName = config['main']['PlayerTwoName'] or 'b'
    self.playerOneWins = int(config['main']['PlayerOneWins']) or 0
    self.playerTwoWins = int(config['main']['PlayerTwoWins']) or 0
    self.needInLine = int(config['main']['needInLine']) or 3
    
    self.headerNum = ''.join(list('123456789')[:self.boardSize])
    rand.seed()
    self.state2MainMenu()
    # Main Event Loop
    isEnd = False
    while not isEnd:
      isEnd = self.stateHandle()

    #save
    config.set('main', 'boardSize', str(self.boardSize))
    config.set('main', 'needInLine', str(self.needInLine))
    config.set('main', 'PlayerOneName', str(self.playerOneName))
    config.set('main', 'PlayerTwoName', str(self.playerTwoName))
    config.set('main', 'PlayerOneWins', str(self.playerOneWins))
    config.set('main', 'PlayerTwoWins', str(self.playerTwoWins))    
    config.write(open(configFileName, 'w'))
  
  def botStepXY(self):
    findEmptyCell = False
    x = y = 0
    while not findEmptyCell:
      x = rand.randint(0, self.boardSize - 1)
      y = rand.randint(0, self.boardSize - 1)
      findEmptyCell = self.getAt(x, y) == self.emptyCell
    self.step(x, y)
    
def mainplay():
  gs = GameState()
  gs.start()

testboard = [['.','X','.','.','.'],\
['X','X','.','.','.'],\
['X','.','.','.','.'],\
['.','.','.','.','.'],\
['.','.','.','.','.']]

if __name__ == '__main__':
    mainplay()





