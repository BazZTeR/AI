# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        print "----------------------"
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        print action
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        newFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # print newFood
        # for i in newGhostStates:
        #     print i.getPosition()
        # print newScaredTimes

        if action == "Stop":
            return -1
        max = 1000000
        # go to closest food while evading ghosts
        mindist = max
        for food in newFood.asList():
            dist = manhattanDistance(newPos, food)
            closestGhostdist = max
            for ghostState in newGhostStates:
                closestGhostdist = min(closestGhostdist,manhattanDistance(newPos,ghostState.getPosition()))
                closestGhostState = ghostState
            if dist < mindist and (closestGhostdist > 1 or closestGhostState.scaredTimer > closestGhostdist):
                mindist = dist
        print max - mindist
        return max - mindist

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        return self.maxValue(gameState,0,0)

    def maxValue(self,gameState,agentIndex,depth):
        # check for terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        maxval = -float("inf")
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex,action)
            v = self.minValue(successor,agentIndex+1,depth)
            if(v > maxval):
                maxval = v
                returnAction = action

        if depth == 0:
            return returnAction
        return maxval 

    def minValue(self,gameState,agentIndex,depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        minval = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex,action)
            # check if agentIndex is the last ghost to play in this round
            if(agentIndex == gameState.getNumAgents() - 1):
                # call max
                v = self.maxValue(successor,0,depth+1)
                minval = min(v,minval)
            else:
                # call min
                v = self.minValue(successor,agentIndex+1,depth)
                minval = min(v,minval)
        return minval 


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.maxValue(gameState,0,0,-float("inf"),float("inf"))
    
    def maxValue(self,gameState,agentIndex,depth,a,b):
        # check for terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        maxval = -float("inf")
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex,action)
            v = self.minValue(successor,agentIndex+1,depth,a,b)
            if(v > maxval):
                maxval = v
                returnAction = action
            if(v > b):
                return v
            a = max(v,a)
        if depth == 0:
            return returnAction
        return maxval 

    def minValue(self,gameState,agentIndex,depth,a,b):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        minval = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex,action)
            # check if agentIndex is the last ghost to play in this round
            if(agentIndex == gameState.getNumAgents() - 1):
                # call max
                v = self.maxValue(successor,0,depth+1,a,b)
            else:
                # call min
                v = self.minValue(successor,agentIndex+1,depth,a,b)
            minval = min(v,minval)
            if(minval < a):
                return minval
            b = min(b,v)
        return minval 

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.maxValue(gameState,0,0)

    def maxValue(self,gameState,agentIndex,depth):
        # check for terminal state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        maxval = -float("inf")
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex,action)
            v = self.minValue(successor,agentIndex+1,depth)
            if(v > maxval):
                maxval = v
                returnAction = action

        if depth == 0:
            return returnAction
        return maxval 

    def minValue(self,gameState,agentIndex,depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        minval = float("inf")
        retVal = 0
        chance = 1.0/len(gameState.getLegalActions(agentIndex))
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex,action)
            # check if agentIndex is the last ghost to play in this round
            if(agentIndex == gameState.getNumAgents() - 1):
                # call max
                v = self.maxValue(successor,0,depth+1)
                minval = min(v,minval)
            else:
                # call min
                v = self.minValue(successor,agentIndex+1,depth)
                minval = min(v,minval)
            retVal += v*chance
        return retVal 

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

