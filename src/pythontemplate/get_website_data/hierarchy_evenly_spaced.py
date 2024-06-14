import sys


def hierarchy_pos_evenly_spaced(G, root, levels=None, width=1.0, height=1.0):
    """If there is a cycle that is reachable from root, then this will see infinite recursion.
    G: the graph
    root: the root node
    levels: a dictionary
            key: level number (starting from 0)
            value: number of nodes in this level
    width: horizontal space allocated for drawing
    height: vertical space allocated for drawing"""
    TOTAL = "total"
    CURRENT = "current"

    current_limit = sys.getrecursionlimit()
    print(f"Current recursion limit: {current_limit}")

    # Increase limit (cautiously)
    new_limit = 100000  # Adjust as needed, be mindful of memory usage
    sys.setrecursionlimit(new_limit)

    def make_levels(levels, node=root, currentLevel=0, parent=None):
        """Compute the number of nodes for each level"""
        if not currentLevel in levels:
            levels[currentLevel] = {TOTAL: 0, CURRENT: 0}
        levels[currentLevel][TOTAL] += 1
        print(f"levels[currentLevel][TOTAL]={levels[currentLevel][TOTAL]}")
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                levels = make_levels(levels, neighbor, currentLevel + 1, node)
        return levels

    def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
        dx = 1 / levels[currentLevel][TOTAL]
        left = dx / 2
        pos[node] = (
            (left + dx * levels[currentLevel][CURRENT]) * width,
            vert_loc,
        )
        levels[currentLevel][CURRENT] += 1
        neighbors = G.neighbors(node)
        for neighbor in neighbors:
            if not neighbor == parent:
                pos = make_pos(
                    pos, neighbor, currentLevel + 1, node, vert_loc - vert_gap
                )
        return pos

    if levels is None:
        levels = make_levels({})
    else:
        levels = {l: {TOTAL: levels[l], CURRENT: 0} for l in levels}
    vert_gap = height / (max([l for l in levels]) + 1)
    return make_pos({})
