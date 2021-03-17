def solution(entrances, exits, path):
    """
    Maximizes the number of bunnies that can get out to the escape pods at each
    time step.
    """

    # --------------------------------------------------------------------------
    # General method:
    # Abstraction: This is an equivalent problem of finding the maximum flow on
    # a graph. Thus:
    # - the vertices will represent the rooms,
    # - the edges will be the corridors,
    # - the graph source will be connected to the entrances,
    # - the exits will lead to a sink
    # - finally the path represents the capacities of the edges (corridors).

    # This will implement a version of the Edmond-Karp algorithm (based on the
    # Ford-Fulkerson method)
    # --------------------------------------------------------------------------


    # Capacity of the super source.
    # Big enough to fill up the maximum number of entrances (50) with the maximum
    # number of bunnies that can fit at a time (2,000,000)
    INFINITE = 2000000*50


    def superPath(path, entrances, exits):
        """
        Creates a new path of size n=(len(path)+2).
        Adds both a super source and a super sink.
        Super source will be at 0, and super sink at (n-1).
        Connects the super source to the entrances, and the exits to the super
        sink.
        """

        # new size
        n = len(path) + 2

        # initialize super path
        spath = [[0]*n for i in range(n)]

        # copy path inside new super path
        for i, row in enumerate(path):
            for j, _ in enumerate(row):
                spath[i+1][j+1] = path[i][j]

        # connect super source with entrances and set capacity
        for i, _ in enumerate(entrances):
            spath[0][i+1] = INFINITE

        # connect exits with the super sink and set capacity
        for i, e in enumerate(exits):
            spath[e+1][n-1] = INFINITE

        return n, spath


    def getAugmentedPath(spath, s, t, previous):
        """
        Search for an augmented path in the residual graph.
        Uses a version of BFS to find a path from source (s) to the sink (t).
        Saves the _journey_ in the previous dictionary to later retrace path.
        """

        # BFS initialization
        visited = {}
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for v, residualc in enumerate(spath[u]):
                # only extend path if there is residual capacity
                if residualc > 0 and (v not in visited):
                    previous[v] = u
                    visited[v] = True
                    queue.append(v)

                    # We got the the sink
                    if v == t:
                        return True

        # unable to reach the sink, so no augmented path found
        return False


    # solution's main ----------------------------------------------------------

    # Create a new path with both a unique super source, and a super sink
    n, spath = superPath(path, entrances, exits)

    # Initialization
    source = 0
    sink = n - 1
    maxflow = 0     # maximum flow
    previous = {}   # map to retrace steps from sink to source

    # Check if there's an augmented path
    while getAugmentedPath(spath, source, sink, previous):

        # calculate minimum residual capacity (bottle neck)
        cflow = INFINITE    # current flow
        node = sink
        # retrace path from sink to source
        while node != source:
            pnode = previous[node]          # previous node
            if spath[pnode][node] < cflow:  # check if capacity is lower
                cflow = spath[pnode][node]
            node = pnode

        # increase maximum flow
        maxflow += cflow

        # update residual capacities
        node = sink
        while node != source:
            pnode = previous[node]
            spath[pnode][node] -= cflow     # decrease capacity
            spath[node][pnode] += cflow     # increase in other direction
            node = pnode

    return maxflow
