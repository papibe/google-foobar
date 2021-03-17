def solution(map):

    def getnextmove(position):
        y, x = position
        return [
            (y + 1, x), # south
            (y - 1, x), # north
            (y, x - 1), # west
            (y, x + 1), # east
        ]

    def getWallEdges(position):
        """Get the walls around this position"""
        nextmoves = getnextmove(position)
        return {neighbor for neighbor in nextmoves if ((neighbor[0] in yRange) and (neighbor[1] in xRange) and map[neighbor[0]][neighbor[1]] == WALL)}


    def getNonWallNeighbors(position):
        """Get the non walls around this position"""
        nextmoves = getnextmove(position)
        return [neighbor for neighbor in nextmoves if ((neighbor[0] in yRange) and (neighbor[1] in xRange) and map[neighbor[0]][neighbor[1]] != WALL)]


    def getNeighbors(position):
        """Get all neighbors for this position"""
        y, x = position
        nextmoves = [
            [y + 1, x], # south
            [y - 1, x], # north
            [y, x - 1], # west
            [y, x + 1], # east
        ]
        return [neighbor for neighbor in nextmoves if (neighbor[0] in yRange) and (neighbor[1] in xRange)]


    def solve(map, start, end, distanceMap):
        """
        Mod version of Dijkstra's and BFS:

        - Traverse all possible paths from start
        - Records the path and the distance to the start
        """
        queue = []
        visited = [start]
        path = [start]

        queue.append([start, 0])

        while queue:

            # remove from queue
            node, distance = queue.pop(0)
            currentNodey, currentNodex = node # unpack

            # get neighbors
            neighbors = getNeighbors(node)

            for neighbor in neighbors:

                if map[neighbor[0]][neighbor[1]] == WALL:
                    continue

                tentative_gScore = distanceMap[currentNodey][currentNodex] + 1

                if neighbor not in visited:
                    # record distance
                    distanceMap[neighbor[0]][neighbor[1]] = tentative_gScore

                    # Add to visited,queue and path
                    visited.append(neighbor)
                    queue.append([neighbor, distance + 1])
                    path.append(neighbor)

        # clean path to the end
        if end in path:
            return (distanceMap[end[0]][end[1]] + 1, path)

        # no final node in path
        return (None, path)


    # Initialization
    WALL = 1

    # size of the map
    w = len(map[0])
    h = len(map)

    # index limits
    xlimit = w - 1
    ylimit = h -1

    # range of limits
    xRange = range(w)
    yRange = range(h)

    # Good enough big number for infinity
    INFINITY = w * h

    start = [0, 0]
    end = [ylimit, xlimit]

    # Distance maps with infinity values
    distanceFromStart = [[INFINITY for x in xRange] for y in yRange]
    distanceFromStart[0][0] = 0

    distanceFromEnd = [[INFINITY for x in xRange] for y in yRange]
    distanceFromEnd[ylimit][xlimit] = 0

    solutions = []

    # Get paths from the start
    scount, spath = solve(map, start, end, distanceFromStart)
    solutions.append(scount)

    # Get paths from the end
    ecount, epath = solve(map, end, start, distanceFromEnd)

    # Get walls that intersect both paths

    # Wall edges from the path from the start (spath)
    commonWallEdges = set()
    for node in spath:
        commonWallEdges = commonWallEdges.union(getWallEdges(node))

    # If no solution from start, get walls from the end's path (epath)and intersect
    if scount is None:
        epatWallEdges = set()
        for node in epath:
            epatWallEdges = epatWallEdges.union(getWallEdges(node))

        commonWallEdges = commonWallEdges.intersection(epatWallEdges)

    # if there were a solution the first time, and it is the shortest one, return it
    elif scount == (h + w - 1):
        return scount

    # try to join paths for each wall edge:
    # - get the shortest distance from the start from one side, and
    # - the shortest distance to the end on the other
    for wallEdge in commonWallEdges:
        neighbors = getNonWallNeighbors(wallEdge)
        d2e = [distanceFromEnd[n[0]][n[1]] for n in neighbors]
        mind2e = min(d2e) + 1

        d2s = [distanceFromStart[n[0]][n[1]] for n in neighbors]
        mind2s = min(d2s) + 1

        solutions.append(mind2e + mind2s + 1)

    # remove None
    cleanSolutions = [count for count in solutions if count is not None]
    return min(cleanSolutions)
