def solution(l):
    """
    Returns the number of "lucky triples": (x, y, z) or (l[i], l[j], l[k]),
    where l[i] divides l[j] and l[j] divides l[k]. Also, i < j < k.
    """

    # Method
    # Calculate all mod operations first. We build a matrix like this:

    # input: [2, 2, 3, 1, 3, 4, 5, 3, 6]

    # then modm (mod Matrix):
    #      2  2  3  1  3  4  5  3  6
    #     ---------------------------
    # 2 | -1  0  1  1  1  0  1  1  0
    # 2 | -1 -1  1  1  1  0  1  1  0
    # 3 | -1 -1 -1  1  0  1  2  0  0
    # 1 | -1 -1 -1 -1  0  0  0  0  0
    # 3 | -1 -1 -1 -1 -1  1  2  0  0
    # 4 | -1 -1 -1 -1 -1 -1  1  3  2
    # 5 | -1 -1 -1 -1 -1 -1 -1  3  1
    # 3 | -1 -1 -1 -1 -1 -1 -1 -1  0
    # 6 | -1 -1 -1 -1 -1 -1 -1 -1 -1

    # note that we only need the upper right values because i < j < k

    # At the same time we build the matrix, we save all its subsequent factors
    # of the current value on a list

    # modl (mod list)
    # l[i] -> [index, value_that_divides]
    #    2 -> [(1, 2), (5, 4), (8, 6)]
    #    2 -> [(5, 4), (8, 6)]
    #    3 -> [(4, 3), (7, 3), (8, 6)]
    #    1 -> [(4, 3), (5, 4), (6, 5), (7, 3), (8, 6)]
    #    3 -> [(7, 3), (8, 6)]
    #    4 -> []
    #    5 -> []
    #    3 -> [(8, 6)]
    #    6 -> []

    counter = 0
    length = len(l)

    # initialize mod matrix and mod list
    modm = [ [ -1 for i in range(length) ] for j in range(length) ]
    modl = [[] for i in range(length)]

    # build mod matrix and mod list
    for i, n in enumerate(l):
        for j in range(i+1, length):
            m = l[j]
            modm[i][j] = m % n
            if modm[i][j] == 0:
                modl[i].append((j, l[j]))

    # for each element in l, cycle over the list of factors
    for i, x in enumerate(l):
        y_list = modl[i]

        # we have potential x, y. Now looking for z
        for j, z in y_list:
            z_list = modl[j]

            counter += len(z_list)

    return counter
