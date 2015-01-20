__author__ = 'bubba'

def generalGraphSearch(problem, fringe, name):
    closed = set()

#    fringe.push([(problem.getStartState(), '', 1)])
    fringe.push([makeNode(problem.get_start_state())])
    #print("FIRST NODE: {}".format(makeNode(problem.getStartState)))

    while True:
        if fringe.isEmpty():
            print("{} has failed.".format(name))
            return retSolution(node) #FAILURE
        node = fringe.pop()
        nodeState = stateFromNode(node)
        if problem.is_goal_state(nodeState):
            print("{} has succeeded.".format(name))
            #print("PATH:\n{}".format(retSolution(node)))
            return retSolution(node)
        if nodeState not in closed:
            #Modification to earlier generalization: instead of adding the state, I'm only adding the URL
            #There's no need to revisit a URL regardless of the path it was reached
            closed.add(nodeState[0])
            for successor in problem.get_successors(nodeState):
                newNode = list(node)
                newNode.append(successor)
                #print("Going to push this node: {}".format(newNode))
                fringe.push(newNode)

def makeNode(state):
    node = state, 'BEGIN', 1
    return node

#Error found: I was checking the first element instead of the last
def stateFromNode(node):
    return node[len(node) - 1][0]

def retSolution(nodeS):
    solution = list()
    for n in nodeS:
        solution.append(n[1])
    return solution

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    fringe = Queue()
    #  The fringe is a FIFO Queue of a list of tuples
    #  Example: {S-A-B-G,S-A-B-C,S-A-B-D} can represent a complete stack
    #           S-A-B-G is a list of tuples
    #           G is a tuple as such: G = (1,1, 'South', 1)

    return generalGraphSearch(problem, fringe, "Breadth First Search")

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0