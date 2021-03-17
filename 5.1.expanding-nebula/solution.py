def solution(g):
    """
    Returns an int with the number of possible previous states that could have
    resulted in that grid after 1 time step.

    General method:
        1. Calculate all previous states of the first nebula row. Create ids
        for the upper and bottom rows. Assign this solution as the current
        overall solution
        2. Go the the next row in the nebula and calculate its previous states
        independently of what have happened before.
        3. Merge the previous states into the overall solution using the rows
        ids: merge the matching ids of the bottom rows of the current solution
        to the upper ids of the previous states of the current nebula row.
        4. Go to the next row and repeat until all row solutions are merged

    Initialization and memoization:
        I noticed that this method works better on a narrow and tall matrix.
        Since the original nebula is the opposite: wide and short, I transposed
        it.
        Also, it is so be much simpler to calculate previous states if you can
        sum the values of the cell's neighbors. Therefore, I converted the
        nebula into binary (True -> 1, False -> 0). An additional bonus of the
        latter is that you can create a unique id for a row (nebula's or from
        a previous state). This works pretty well for merging solutions.
        Since the nebula is now a tall, narrow and binary matrix, I added
        memoization, in the possible case that the nebula's rows are repeated.


    Parameters:
        g: a boolean matrix representing the current state of the nebula

    Returns:
        an integer representing all the previous states of the nebula
    """

    from copy import deepcopy

    # Map of previous states from a current cell
    firstMoveOptions = {
        # previous state of a cell with gas
        1: (
            (1, 0, 0, 0),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (0, 0, 0, 1),
        ),

        # previous state of a cell with no gas
        0: (
            (0, 0, 0, 0),
            (1, 1, 0, 0),
            (1, 0, 1, 0),
            (1, 0, 0, 1),
            (0, 1, 1, 0),
            (0, 1, 0, 1),
            (0, 0, 1, 1),
            (0, 1, 1, 1),
            (1, 0, 1, 1),
            (1, 1, 0, 1),
            (1, 1, 1, 0),
            (1, 1, 1, 1),
        )
    }

    # Map of possible states considering the previous inherited value from
    # the previous choice, and the current target
    #   moveOptions[target][value]
    moveOptions = {
        0: {
            0: (
                (0, 0),
                (1, 1),
            ),
            1: (
                (1, 0),
                (0, 1),
                (1, 1)
            ),
            2: (
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1)
            )
        },
        1: {
            0: (
                (1, 0),
                (0, 1)
            ),
            1: (
                (0, 0),
            ),
            2: ()
        }
    }


    def convertToBin(g):
        """
        Convert the nebula representation from boolean to binary:
            True -> 0
            False -> 0
        Now pplying the gas-rule for a cell is easier because you can add the
        neighbors' values.

        Parameters:
            g: a boolean matrix representing the nebula
        """
        return [[1 if item else 0 for item in row] for row in g]


    class Solution:
        """
        Represents the current solution: number of previous states up to the
        current scanned nebula row.

        Attributes:
            bottomIDs: a dictionary representing the count of how many bottom
            rows of the current solution end in a particular id. For instance,
            bottomIDs[123] = 5 means that there are 5 previous states that ends
            with a row id  of 123 (see _getId method)

            bottomIDSet: a set with all of the bottom ids of the current
            solutions. Using a set is more efficient to merge new solutions rows
            by doing set intersection.
        """
        def __init__(self, rsolution):
            """
            Creates a Solution object from a RowSolution object. This is done
            one time after a RowSolution is found for the first row.

            Parameters:
                rsolution: a RowSolution object.
            """
            self.bottomIDs = {}
            self.bottomIDSet = rsolution.bottomSet

            for bid in rsolution.bottomIDs:
                self.bottomIDs[bid] = len(rsolution.bottomIDs[bid])


        def merge(self, rsolution):
            """
            Merges a single nebula row's previous states (rsolution) with the
            previous states already calculated.

            Parameters:
                rsolution: a RowSolution object representing all the previous
                states of the a nebula row that hasn't been merge
            """
            # intersection
            interSet = self.bottomIDSet & rsolution.upperSet

            newBottomIDs = {}
            newBottomSet = set()

            # count while merging the new rows
            for bid in interSet:
                for newBid in rsolution.upperIDs[bid]:
                    newBottomIDs[newBid] = self.bottomIDs[bid] + newBottomIDs.get(newBid, 0)
                    newBottomSet.add(newBid)

            # Replace previous ids and set
            self.bottomIDs = newBottomIDs
            self.bottomIDSet = newBottomSet


        def countSolutions(self):
            """
            Count all the previous states

            Returns:
                an integer representing all the previous states currently
                calculated
            """
            total = 0
            for bid, value in self.bottomIDs.items():
                total += value

            return total


    class RowSolution:
        """
        Represents all the possible previous states of a single nebula row.

        Attributes:
            upperIDs: dictionary mapping the ids of the upper row to the list of
            bottom row ids

            bottomIDs: dictionary mapping the ids of the bottom row to the list
            upper of row id

            upperSet: a set with the ids of the first row of all the previous
            states

            bottomSet: a set with the ids of the bottom row of all the previous
            states
        """
        def __init__(self):
            """
            Creates an empty object. The method 'add' will add a single previous
            state to the object one at a time as they are calculated.
            """
            self.upperIDs = {}
            self.bottomIDs = {}
            self.upperSet = set()
            self.bottomSet = set()


        def _getId(self, row):
            """
            Creates a unique id from a row from a previous state.

            Parameter:
                row: a row from a previous state

            Returns:
                an integer representing the decimal value of the row (which it
                is interpreted as a binary number)
            """
            l = len(row) -1
            sum = 0
            for i, item in enumerate(row):
                sum += item * (2**(l-i))
            return sum


        def add(self, solution):
            """
            Adds a matrix representing one possible previous state to the
            RowSolution object.

            Parameters:
                solution: a matrix of 2x(w+1) size representing a single
                previous state of a nebula row
            """
            # calculates both ids
            upperID = self._getId(solution[0])
            bottomID = self._getId(solution[len(solution)-1])

            # adds ids the proper set
            self.upperSet.add(upperID)
            self.bottomSet.add(bottomID)

            # adds the ids the the lists in its dictionaries
            if (upperID in self.upperIDs):
                self.upperIDs[upperID].append(bottomID)
            else:
                self.upperIDs[upperID] = [bottomID]

            if (bottomID in self.bottomIDs):
                self.bottomIDs[bottomID].append(upperID)
            else:
                self.bottomIDs[bottomID] = [upperID]


    def solBFS(bgRow):
        """
        Breath-first-like procedure to calculate all the possible previous
        states of a single nebula row
        """
        # creates empty solution
        rsolution = RowSolution()

        w = len(bgRow)
        queue = []

        # Creates and push all previous states of the first element of the
        # nebula row
        target = bgRow[0]
        for a, b, c, d in firstMoveOptions[target]:
            pg = [
                [a, b],
                [c, d]
            ]
            queue.append((pg, 1, b + d))    # push

        while queue:
            pg, j, value = queue.pop()

            # If we reached the end, add the solution to rsolution
            if j >= w:
                rsolution.add(pg)
                continue

            # create and push all possible states from the previous one
            target = bgRow[j]
            for a, b in moveOptions[target][value]:
                npg = deepcopy(pg)
                npg[0].append(a)
                npg[1].append(b)
                queue.append((npg, j + 1, a + b))    # push

        return rsolution


    def getId(row):
        """
        Creates a unique id from a nebula row with the purpose of using
        memoization.

        Parameter:
            row: a row from a previous state

        Returns:
            an integer representing the decimal value of the row (which it
            is interpreted as a binary number)
        """
        l = len(row) -1
        sum = 0
        for i, item in enumerate(row):
            sum += item * (2**(l-i))
        return sum



    # ------- main solution ----------------------------------------------------

    # transpose nebula and convert it to binary
    tg = zip(*g)
    bg = convertToBin(tg)

    h = len(bg)
    w = len(bg[0])

    # memoization dictionary
    calulatedRows = {}

    # row = 0
    rsolution = solBFS(bg[0])
    puzzle = Solution(rsolution)
    calulatedRows[getId(bg[0])] = deepcopy(rsolution)

    for row in range(1, h):
        # get row id
        rowId = getId(bg[row])

        # check if already calculated. If so, use memo
        if rowId in calulatedRows:
            rsolution = calulatedRows[rowId]
        else:
            # calculate previous states of current row and memo'it
            rsolution = solBFS(bg[row])
            calulatedRows[rowId] = rsolution

        # merge the current row solution to the overall solution
        puzzle.merge(rsolution)


    return puzzle.countSolutions()
