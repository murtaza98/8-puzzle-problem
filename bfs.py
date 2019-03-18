while (not goal_found):
    current_state = id_to_state[explore_queue.pop(0)]

    print(current_state)

    parent_move = current_state.parent_move
    possible_movements = ["left", "right", "up", "down"]
    if (parent_move != "null"):
        possible_movements.remove(opposite_movements[parent_move])
    childs = []
    for move in possible_movements:
        matrix = create_child(current_state.self_state, move)
        if matrix != -1:
            state_obj = State(matrix, current_state.self_id, move, current_state.level + 1)
            current_state.set_child(state_obj.self_id, move)
            # put the child id to queue
            explore_queue.append(state_obj.self_id)
            # save the child object
            id_to_state[state_obj.self_id] = state_obj
            childs.append(state_obj.self_id)
            # check if this child is the goal state
            if matrix == final_state:
                goal_found = True