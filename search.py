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

    """
    #print "StartProblem:", problem
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    #print "Start's successors type:", type(problem.getSuccessors(problem.getStartState()))
    "*** YOUR CODE HERE ***"
    ret = _dfs(problem.getStartState(), problem, [])[1]
    return ret


def _dfs(state, problem, visited):
    if state in visited :
        return (False,)
    visited.append(state)
    if problem.isGoalState(state):
        return (True, [])
    successors = problem.getSuccessors(state);
    for successor in successors :
        result = _dfs(successor[0], problem, visited);
        if result[0] :
            #print 'result: ', result
            result[1].insert(0,successor[1])
            return (True, result[1])
    return (False,)

def some(fun, iterable):
    for element in iterable:
        if fun(element) :
            return True
    return False
#((x,y), direction, cost?)
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = [{ 'state': problem.getStartState(),'route':[]}]
    visited = []
    while frontier :
        #print frontier
        toVisit = frontier.pop()
        visited.append(toVisit['state'])
        if problem.isGoalState(toVisit['state']):
            return toVisit['route']
        else:
            #expand
            successors = problem.getSuccessors(toVisit['state'])
            frontier[:0] = filter(lambda new_node: not (new_node['state'] in visited or some( lambda frontier_node: frontier_node['state'] == new_node['state'], frontier)) ,map(lambda successor: {'state':successor[0], 'route': toVisit['route']+[successor[1]] } , successors));
    return None;

#((x,y), direction, cost?)
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = [{ 'state': problem.getStartState(),'route':[], 'cost':0}]
    visited = []
    while frontier :
        toVisit = frontier.pop(0)
        visited.append(toVisit['state'])
        if problem.isGoalState(toVisit['state']):
            return toVisit['route']
        else:
            #expand, add 
            frontier[:0] = filter(lambda new_node: not new_node['state'] in visited,
                                    map(lambda successor: 
                                        {'state':successor[0],
                                         'route': toVisit['route']+[successor[1]],
                                         'cost':toVisit['cost']+successor[2] },
                                     problem.getSuccessors(toVisit['state'])));
            #remove duplicates
            frontier = filter(lambda node1: not some( 
                                lambda node2: node2['state'] == node1['state'] and 
                                              node2['cost'] < node1['cost'], frontier),frontier)
            frontier.sort(lambda a,b: 1 if a['cost'] > b['cost'] else -1)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    print 'FOOOOBARRRR'
    frontier = [{ 'state': problem.getStartState(),'route':[], 'gCost':0,'fCost':heuristic(problem.getStartState(), problem)}]
    visited = []
    while frontier :
        toVisit = frontier.pop(0)
        visited.append(toVisit['state'])
        if problem.isGoalState(toVisit['state']):
            return toVisit['route']
        else:
            #expand, add 
            frontier[:0] = filter(lambda new_node: not new_node['state'] in visited,
                                    map(lambda successor: 
                                        {'state':successor[0],
                                         'route': toVisit['route']+[successor[1]],
                                         'gCost':toVisit['gCost']+successor[2],
                                         'fCost':toVisit['gCost']+successor[2]+heuristic(successor[0],problem) },
                                     problem.getSuccessors(toVisit['state'])));
            #remove duplicates
            frontier = filter(lambda node1: not some( 
                                lambda node2: node2['state'] == node1['state'] and 
                                              node2['gCost'] < node1['gCost'], frontier),frontier)
            frontier.sort(lambda a,b: 1 if a['fCost'] > b['fCost'] else -1)
            print frontier
            print '######################################'

    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
