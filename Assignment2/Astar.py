import sys
from Map import Map_Obj

'''
    all code is based on psudocode presented in the assignment.

    The node class has method f to not have to recalculate when g or h changes
    find_successors uses map to check if neighbours are valid fields, and returns list with them
'''

class Node:
    def __init__(self, pos, cost):
        self.parent = None
        self.children = []
        self.pos = pos

        self.cost = cost
        self.g = float('inf')  # g(s)
        self.h = None  # h(s)

    def f(self):
        return self.g + self.h

    def find_successors(self, map_obj: Map_Obj):
        possible_successors = [[self.pos[0] - 1, self.pos[1]],
                               [self.pos[0] + 1, self.pos[1]], [self.pos[0], self.pos[1] - 1],
                               [self.pos[0], self.pos[1] + 1]]
        successors = []
        for possible in possible_successors:
            cost = map_obj.get_cell_value(possible)
            if cost >= 0:
                successors.append(Node(possible, cost))

        return successors

    def __str__(self):
        return "x: " + str(self.pos[0]) + ", y: " + str(self.pos[1]) + ", cost: " + str(self.cost)

'''
    the method for searching

'''
def best_first_search(start_node: Node, goal_node: Node, map_obj: Map_Obj):
    closed_set = []
    open_set = []
    start_node.g = 0
    start_node.h = euclidean_distance(start_node.pos, goal_node.pos)

    open_set.append(start_node)

    current = start_node

    while current.pos != goal_node.pos:
        # no more nodes, search failed
        if len(open_set) == 0:
            print("error")
            return "fail", "fail"

        # moves current from open to closed
        current = open_set.pop()
        closed_set.append(current)

        if current.pos == map_obj.goal_pos:
            return current, "success"

        successors = current.find_successors(map_obj)
        for successor in successors:
            exist = has_been_created(successor, open_set, closed_set) or successor
            if exist not in open_set and exist not in closed_set:
                attach_and_eval(exist, current, map_obj)
                open_set.append(exist)
                open_set.sort(key=lambda y: y.f(), reverse=True)
            elif current.f() + map_obj.get_cell_value(exist.pos) < exist.f():
                attach_and_eval(exist, current, map_obj)
                if exist in closed_set:
                    propagate_path_improvements(exist)


'''
    uses pos to check if a node with same pos is in open or closed set
'''
def has_been_created(node: Node, open_set, closed_set):

    for element in open_set:
        if node.pos == element.pos:
            return element

    for element in closed_set:
        if node.pos == element.pos:
            return element

    return None

'''
    set parent for the child node
    updates childs g based on parent and cost
    set child h to distance
'''
def attach_and_eval(child: Node, parent: Node, map_obj: Map_Obj):
    child.parent = parent
    child.g = parent.g + child.cost
    child.h = euclidean_distance(child.pos, map_obj.get_goal_pos())

'''
    uses this distance as path is only left/right and up/down not diagonal
'''
def euclidean_distance(from_pos, goal_pos):

    return abs(from_pos[0] - goal_pos[0]) + abs(from_pos[1] - goal_pos[1])

'''
    goes througt all children from parent
    if child g is lower thans parent g and cost
    we set child parent to parent
    upate child g
    recurive on found child
'''
def propagate_path_improvements(parent: Node):
    for child in parent.children:
        if parent.g + child.cost < child.g:
            child.parent = parent
            child.g = parent.g + child.cost
            propagate_path_improvements(child)

'''
    create nodes based on pos for start and end, and values given in map
'''
def create_start_nodes(start, end, map: Map_Obj):
    start_node = Node(start, map.get_cell_value(start))
    end_node = Node(end, map.get_cell_value(end))

    return start_node, end_node


'''
    goes through all nodes in path and set the color to yellow
    uses node.parent as next node
    shows map
'''
def print_map(node: Node, map_obj):
    node = node.parent

    while node.parent is not None:
        map_obj.set_cell_value(node.pos, 4)
        node = node.parent
    map_obj.show_map()

'''
    set up nodes based on goal and start given by task
'''
def main(task):
    map_obj = Map_Obj(task=task)
    start = map_obj.get_start_pos()
    end = map_obj.get_goal_pos()

    start_node, end_node = create_start_nodes(start, end, map_obj)

    val, msg = best_first_search(start_node, end_node, map_obj)

    try:
        print_map(val, map_obj)
    except AttributeError:
        print("failed")


'''
    checks if task is given as param, else task 1 is given
'''
if __name__ == "__main__":
    task = 1
    if len(sys.argv) > 1:
        task = int(sys.argv[1])

    main(task)
