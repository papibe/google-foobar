from math import factorial

def solution(num_buns, num_required):
    """
    Calculate: the number of locks required, the number of keys per bunny, and
    the distribution of those keys such that any num_required bunnies can open
    the locks, but no group of (num_required - 1) bunnies can.
    """
    # General method
    # We calculate the number of locks required:
    #   nlocks = choose(num_buns, num_required - 1)
    #
    # and the number of keys per bunny:
    #   kpb = choose(num_buns - 1, num_required - 1)
    #
    # The combinations are calculated in the function lexCombs. A set of keys is
    # represented as a bit string. For example, if the number of locks is 10,
    # and the number of keys for bunny is 6, this would represent a set of keys
    # hold by a bunny:
    #   [1, 0, 0, 1, 1, 0, 1, 1, 0, 1]
    #
    # representing this list of keys:
    #   [0, 3, 4, 6, 7, 9]
    #
    # Thus I can think of the problem as the same as combinations of 0s, and 1s.
    # Also, since (num_buns - 1) bunnies can't open the cells, it means
    # that a particular key should be only be distributed:
    #   (num_buns - num_required + 1) times.
    #
    # So the combination problem is equivalent as combination of how to choose
    # (num_buns - num_required + 1), from num_buns, which is exactly nlocks.
    # In other words:
    # nlocks =  choose(num_buns, num_required - 1) = \
    #           choose(num_buns, num_buns - num_required + 1)
    #
    # (because choose(n, k) = choose(n, n-k))


    def choose(n, k):
        """
        Math choose function, aka nCk.
        Counts the ways you can choose k elements from a set of n
        """
        f = factorial
        return int(f(n) / (f(k) * f(n-k)))


    def lexCombs(n, t):
        """
        Generate all combinations of t elements of a set of n, represented as
        bit strings
        """
        # This method is my interpretation of a Knuth algorithm from TAoCP which
        # generate bit string combinations. Its main feature is that you can
        # generate combs by moving the 1s in a certain pattern.

        # Edge easy case: one key distributed to all bunnies
        if n == t:
            output = [[1] for i in range(0, num_buns)]
            return output

        # Illogical case.
        # No keys per bunny represented as an empty list. Just in case
        if n < t:
            output = [[] for i in range(0, num_buns)]
            return output

        # Illogical case. Just in case
        if t == 0:
            output = [[0 for i in range(0, nlocks)] for i in range(0, num_buns)]
            return output

        # Generate matrix
        output = [[None for i in range(0, nlocks)] for i in range(0, num_buns)]

        # This is going to represent a single combination
        comb = [None for i in range(0, n)]

        # Matrix is going to be fill starting from last column
        target = nlocks - 1

        # Initialize comb
        for i in range(n-1, t-1, -1):   # zeros
            comb[i] = 0
        for i in range(t-1, 0-1, -1):   # ones
            comb[i] = 1

        comb.append(0)  # padding

        # indexes to track
        q = t   # last 1
        r = 0   # needed when shifting a set of 1s

        while True:
            # Save combination on a matrix's column
            index = 0
            for i in range(n-1, 0-1, -1):
                output[index][target] = comb[i]
                index = index + 1

            target = target - 1 # move target one column

            # Move a 1 to the left (or up, if you see the matrix as transpose)
            if q != 0:
                comb[q] = 1
                comb[q-1] = 0
                q = q - 1

                # We got the the end
                if q == 0:
                    r = 1
            else:
                # we got to the end, so we need to shift a group of 1s
                while True:
                    comb[r] = 0
                    r = r + 1
                    if comb[r] == 1:
                        comb[q] = 1
                        q = q + 1
                    else:
                        break

                # All combinations obtained
                if r == n:
                    break
                else:
                    comb[r] = 1 # remaining 1 from shift

                if q > 0:
                    r = 0

        return output


    def bitToKeys(bitstring):
        """
        Convert a subset of keys represented by a bit string to the actual list
        of keys
        """
        newoutput = []
        for line in bitstring:
            row = []
            for i, bit in enumerate(line):
                # a 1 in position i means the key i was selected
                if bit == 1:
                    row.append(i)
            newoutput.append(row)

        return newoutput


    # Main solution -----------------------------------------------------------

    if num_required > num_buns:
        # Illogical edge case. Just in case
        nlocks = 0
        keysPerBunny = 0
    else:
        nlocks = choose(num_buns, num_required - 1)
        kpb = choose(num_buns - 1, num_required - 1) # keys per bunny

    # Generate combinations using bit strings representing the distribution
    bitString = lexCombs(num_buns, num_buns - num_required + 1)

    # Translate bit strings in a list of keys
    output = bitToKeys(bitString)

    return output
