def hierarchy_pos_no_recur(
    G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5
):
    """If there is a cycle that is reachable from root, then result will not be a hierarchy.

    G: the graph
    root: the root node of current branch
    width: horizontal space allocated for this branch - avoids overlap with other branches
    vert_gap: gap between levels of hierarchy
    vert_loc: vertical location of root
    xcenter: horizontal location of root
    """

    def h_recur(
        G,
        root,
        width=1.0,
        vert_gap=0.2,
        vert_loc=0,
        xcenter=0.5,
        pos=None,
        parent=None,
        parsed=[],
    ):
        if root not in parsed:
            parsed.append(root)
            if pos == None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            neighbors = list(G.neighbors(root))
            if parent != None and parent in neighbors:
                neighbors.remove(parent)
            print(f"{len(neighbors)}, {root}")
            if len(neighbors) > 0:
                dx = width / len(neighbors)
                nextx = xcenter - width / 2 - dx / 2
                for neighbor in neighbors:
                    nextx += dx
                    # print(f'nextx={nextx}, neighbor={neighbor}')
                    pos = h_recur(
                        G,
                        neighbor,
                        width=dx,
                        vert_gap=vert_gap,
                        vert_loc=vert_loc - vert_gap,
                        xcenter=nextx,
                        pos=pos,
                        parent=root,
                        parsed=parsed,
                    )
        return pos

    return h_recur(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5)
