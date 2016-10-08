# Моя State System.
# должна быть таблица состояний = состояниеБыло состояние стало = функцияПерехода
# + состояние сейчас + собите = обработчик
from collections import defaultdict
stateChangeHandlers = defaultdict(bool)
stateEventHanders = defaultdict(bool)
states = list()
currentState = None

def changeState(newState):
    global currentState, states
    if newState in states:
        handleChangeState(newState)
        currentState = newState

def setChangeHandler(stateFrom, stateTo, fun):
    stateChangeHandlers[(stateFrom, stateTo)] = fun

def setEventHandler(state, event, fun):
    stateEventHanders[(state, event)] = fun

def addState(state):
    global states
    states += [state]

def handleChangeState(new):
    global stateChangeHandlers, currentState
    fun = stateChangeHandlers[(currentState, new)]
    if fun:
        fun()

def handleEvent(event, *args):
    global currentState
    fun = stateEventHanders[(currentState, event)]
    if fun:
        fun(*args)

