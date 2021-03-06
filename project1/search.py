# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    solution=[]
    node = (problem.getStartState(),[],0)
    if(problem.isGoalState(node[0])):
        return solution
    frontier = util.Stack()
    frontier.push(node)
    explored = []
    while(not frontier.isEmpty()):
        node = frontier.pop()
        explored.append(node[0])
        for child in problem.getSuccessors(node[0]):
            existsinFrontier=False
            for i in frontier.list:
                if(child[0] == i[0]):
                    existsinFrontier=True
            if((child[0] not in explored) and (not existsinFrontier)):
                if(problem.isGoalState(child[0])):
                    return node[1]+[child[1]]
                frontier.push((child[0],node[1]+[child[1]],0))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    solution=[]
    node = (problem.getStartState(),[],0)
    if(problem.isGoalState(node[0])):
        return solution
    frontier = util.Queue()
    frontier.push(node)
    explored = []
    while(not frontier.isEmpty()):
        node = frontier.pop()
        explored.append(node[0])
        for child in problem.getSuccessors(node[0]):
            existsinFrontier=False
            for i in frontier.list:
                if(child[0] == i[0]):
                    existsinFrontier=True
            if((child[0] not in explored) and (not existsinFrontier)):
                if(problem.isGoalState(child[0])):
                    return node[1]+[child[1]]
                frontier.push((child[0],node[1]+[child[1]],0))

def uniformCostSearch(problem):
    solution=[]
    node = (problem.getStartState(),[],0)
    if(problem.isGoalState(node[0])):
        return solution
    frontier = util.PriorityQueue()
    frontier.push(node,0)
    explored = []
    while(not frontier.isEmpty()):
        node = frontier.pop()
        if(problem.isGoalState(node[0])):
            print "Solution = ",node[1]
            return node[1]
        explored.append(node)
        for child in problem.getSuccessors(node[0]):
            existsinFrontier=False
            existsinExplored=False
            for i in range(len(frontier.heap)):
                if(child[0] == frontier.heap[i][2][0]):
                    existsinFrontier=True
                    frontierPos = i
                    break
            for i in range(len(explored)):
                if(child[0] == explored[i][0]):
                    existsinExplored=True
                    break
            if((not existsinExplored) and (not existsinFrontier)):
                frontier.push((child[0],node[1]+[child[1]],node[2]+child[2]),node[2]+child[2])
            elif(existsinFrontier and frontier.heap[frontierPos][0] > node[2]+child[2]):
                del frontier.heap[frontierPos]
                frontier.push((child[0],node[1]+[child[1]],node[2]+child[2]),node[2]+child[2])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    solution=[]
    node = (problem.getStartState(),[],0)
    if(problem.isGoalState(node[0])):
        return solution
    frontier = util.PriorityQueue()
    frontier.push(node,0)
    explored = []
    while(not frontier.isEmpty()):
        node = frontier.pop()
        if(problem.isGoalState(node[0])):
            return node[1]
        explored.append(node)
        for child in problem.getSuccessors(node[0]):
            existsinFrontier=False
            existsinExplored=False
            for i in range(len(frontier.heap)):
                if(child[0] == frontier.heap[i][2][0]):
                    existsinFrontier=True
                    frontierPos = i
                    break
            for i in range(len(explored)):
                if(child[0] == explored[i][0]):
                    existsinExplored=True
                    break
            h = heuristic(child[0],problem)
            if((not existsinExplored) and (not existsinFrontier)):
                frontier.push((child[0],node[1]+[child[1]],node[2]+child[2]+h),node[2]+child[2]+h)
            elif(existsinFrontier and frontier.heap[frontierPos][0] > node[2]+child[2]+h):
                del frontier.heap[frontierPos]
                frontier.push((child[0],node[1]+[child[1]],node[2]+child[2]+h),node[2]+child[2]+h)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
