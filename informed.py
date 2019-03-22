from graphviz import Digraph
import os
import copy
import functools
import time


counter = 1
initial_state = [[0, 1, 3],
                [6, 2, 4],
                [7, 5, 8]]

final_state = [[1, 2, 3],
                [6, 5, 4],
                [7, 8, 0]]


class State(object):
    def __init__(self, self_state, parent_id, parent_move, level):
        global counter
        self.self_id = counter
        self.self_state = self_state
        self.parent_id = parent_id
        self.parent_move = parent_move
        self.level = level
        self.cost = 0
        self.l_child = -1
        self.u_child = -1
        self.r_child = -1
        self.d_child = -1
        counter += 1

    def set_child(self, state_id, move):
        if move == "left":
            self.l_child = state_id
        elif move == "right":
            self.r_child = state_id
        elif move == "up":
            self.u_child = state_id
        elif move == "down":
            self.d_child = state_id

    def __repr__(self):
        return str(self.self_state[0])+"\n"+str(self.self_state[1])+"\n"+str(self.self_state[2])


def create_child(parent_state, move):
    i = 0
    j = 0
    found = False
    matrix = copy.deepcopy(parent_state)
    for i in range(0, 3):
        for j in range(0, 3):
            if parent_state[i][j] == 0:
                found = True
                break
        if found:
            break
    if move == "left":
        if j == 0:
            return -1
        else:
            matrix[i][j] = matrix[i][j - 1]
            matrix[i][j - 1] = 0
            return matrix
    if move == "right":
        if j == 2:
            return -1
        else:
            matrix[i][j] = matrix[i][j + 1]
            matrix[i][j + 1] = 0
            return matrix
    if move == "up":
        if i == 0:
            return -1
        else:
            matrix[i][j] = matrix[i - 1][j]
            matrix[i - 1][j] = 0
            return matrix

    if move == "down":
        if i == 2:
            return -1
        else:
            matrix[i][j] = matrix[i + 1][j]
            matrix[i + 1][j] = 0
            return matrix


explored = []
unexplored = []

def custom_sort(a, b):
    if a.cost == b.cost:
        return 0
    elif a.cost < b.cost:
        return 1
    else:
        return -1

def manhattan_distance(current_matrix):
    goal_matrix = [[1,2,3],
                [6,5,4],
                [7,8,0]]
    distance = 0
    for i in range(0,3):
        for j in range(0,3):
            if current_matrix[i][j] != 0:
                for item in goal_matrix:
                    if current_matrix[i][j] in item:
                        x = goal_matrix.index(item)
                        y = item.index(current_matrix[i][j])
                distance = distance + (abs(x - i) + abs(y - j))
    return distance


def A_star():
    global state_space_tree, explored, unexplored
    global id_to_state
    current_state = id_to_state[1]
    counter_g = 0

    dot = Digraph(comment='BFS graph')
    dot.node(str(current_state.self_id), current_state.__str__())

    while True:
        explored.append(current_state)
        # print(current_state.self_id, len(explored))
        # # graph
        # dot.node(str(current_state.self_id), current_state.__str__())
        # dot.edge(str(current_state.parent_id), str(current_state.self_id), label=current_state.parent_move)
        if current_state.self_state == final_state:
            break
        if current_state.u_child != -1:
            child_state = id_to_state[current_state.u_child]
            cost_child = counter_g + manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move)
        if current_state.d_child != -1:
            child_state = id_to_state[current_state.d_child]
            cost_child = counter_g + manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move)
        if current_state.l_child != -1:
            child_state = id_to_state[current_state.l_child]
            cost_child = counter_g + manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move)
        if current_state.r_child != -1:
            child_state = id_to_state[current_state.r_child]
            cost_child = counter_g + manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move)

        unexplored.sort(key=lambda x:x.cost)

        current_state = unexplored.pop(0)
        print([item.self_id for item in unexplored])
        print([item.cost for item in unexplored])
        print("\n")
        # time.sleep(1)
        counter_g += 1

    dot.render(str(os.getcwd() + '/outputs/A_star_graph.gv'), view=True)


def Greedy_best_first():
    global state_space_tree, explored, unexplored
    global id_to_state
    current_state = id_to_state[1]

    explored = []
    unexplored = []

    dot = Digraph(comment='BFS graph')
    dot.node(str(current_state.self_id), current_state.__str__())

    while True:
        explored.append(current_state)
        # print(current_state.self_id, len(explored))
        # # graph
        # dot.node(str(current_state.self_id), current_state.__str__())
        # dot.edge(str(current_state.parent_id), str(current_state.self_id), label=current_state.parent_move)
        if current_state.self_state == final_state:
            break
        if current_state.u_child != -1:
            child_state = id_to_state[current_state.u_child]
            cost_child = manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move+str(child_state.cost))
        if current_state.d_child != -1:
            child_state = id_to_state[current_state.d_child]
            cost_child = manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move+str(child_state.cost))
        if current_state.l_child != -1:
            child_state = id_to_state[current_state.l_child]
            cost_child = manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move+str(child_state.cost))
        if current_state.r_child != -1:
            child_state = id_to_state[current_state.r_child]
            cost_child = manhattan_distance(child_state.self_state)
            child_state.cost = cost_child
            if child_state not in explored and child_state not in unexplored:
                unexplored.append(child_state)
                # graph
                dot.node(str(child_state.self_id), child_state.__str__())
                dot.edge(str(current_state.self_id), str(child_state.self_id), label=child_state.parent_move+str(child_state.cost))

        unexplored.sort(key=lambda x:x.cost)

        current_state = unexplored.pop(0)

    dot.render(str(os.getcwd() + '/outputs/greedy_best_first_graph.gv'), view=True)

state_space_tree = dict()
id_to_state = dict()

if __name__ == "__main__":
    # for graph
    dot = Digraph(comment='State space graph')

    opposite_movements = {"up": "down", "down": "up", "left": "right", "right": "left"}
    goal_found = False
    current_state = State(initial_state, 1, "null", 1)
    id_to_state[1] = current_state
    explore_queue = [current_state.self_id]

    dot.node(str(current_state.self_id), current_state.__str__())

    goal_lvl = 9999

    while (True):
        current_state = id_to_state[explore_queue.pop(0)]

        if current_state.level  > goal_lvl + 1:
            break

        parent_move = current_state.parent_move
        possible_movements = ["up", "left", "down", "right"]
        if (parent_move != "null"):
            possible_movements.remove(opposite_movements[parent_move])
        childs = []
        for move in possible_movements:
            matrix = create_child(current_state.self_state, move)
            if matrix != -1:
                state_obj = State(matrix, current_state.self_id, move, current_state.level+1)
                current_state.set_child(state_obj.self_id, move)
                # put the child id to queue
                explore_queue.append(state_obj.self_id)
                # save the child object
                id_to_state[state_obj.self_id] = state_obj
                childs.append(state_obj.self_id)
                # check if this child is the goal state
                if matrix == final_state and goal_lvl == 9999:
                    goal_lvl = state_obj.level - 1

                if matrix == final_state:
                    dot.node(str(state_obj.self_id), state_obj.__str__(), color='green')
                else:
                    dot.node(str(state_obj.self_id), state_obj.__str__())

                dot.edge(str(state_obj.parent_id), str(state_obj.self_id), label=move)

    A_star()
    Greedy_best_first()
    dot.render(str(os.getcwd() + '/outputs/state_space_tree_informed.gv'), view=True)

