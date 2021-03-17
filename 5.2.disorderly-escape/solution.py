from math import factorial
from fractions import gcd

def solution(w, h, s):
    """
    Returns the number of unique, non-equivalent configurations that can be
    found on a star grid w blocks wide and h blocks tall where each celestial
    body has s possible states.

    Inputs:
        w: width
        h: height
        s: number of possible states

    Research Summary:
    =================

    I interpreted this problem as one similar of the problem of counting the
    equivalent classes of coloring a physical object that are the same under
    symmetries (like a cube, necklace of beads, or a square token).

    From the Orbit-stabilizer theorem, I confirmed that all the transformations
    are (h! x w!)

    Using Burnside's lemma I manually solved both the example cases, but this
    method does not scale.

    Closer to a generalization are the Polya's polynomials. However, it turned
    out to be difficult to create a generalized polynomial for a (h x w) matrix.

    I had the intuition that you could multiply the polynomials for (h) and (w),
    but the regular algebraic multiplication did not work.

    After some research, I found a way to multiply those polynomials correctly
    reflecting the composition of the vertical and horizontal transformations
    (permutations):

        if you multiply a permutation with a cycle of size r, repeated jr times,
        with another permutation with a cycle of size t that it's repeated jt
        times. The result will be a permutation with a cycle lcm(r,t), that
        repeats (gcd(r,t) * jr * jt) times.

    Personal research notes: https://docs.google.com/presentation/d/1femY3unzDnsIglsT-bVQqtPeTCse_LGQ4o9-mPMZMh8/edit?usp=sharing

    Solution:
    =========

    1. Calculate the partition vectors for each dimension.
    2. Calculate the coefficient for each permutation vector
    3. For each combination of those vectors calculate how many times the new
       cycle will repeat.
       This inner loop represent the calculation of the exponent of the term.
       For instance, if
            r = (r=2, j2= 1)
            t = (t=2, j2= 1; t=1, j1= 1)
        then
            exponent = (gcd(2,2) * 1 * 1) + (gcd(2,1) * 1 * 1)

        (see personal research notes for more examples)

       Note that I am ignoring the size of the cycle (lcm), because it does not
       matter when you replace it with the number of states (coloring). Another
       way to see the latter is that a cycle fixes the same amount of elements
       regarding of the size of the cycle itself.
    4. Add to the total the multiplication of:
            both coefficients, and
            s**exponent
    """


    def partitionsGen(n, lower=1):
        """
        Generator function that returns all partitions of an integer. For
        example: if n is 3, then it would return in each subsequent iteration:
            [3]
            [2, 1]
            [1, 1, 1]
        """
        yield [n]
        for i in range(lower, n//2 + 1):
            for p in partitionsGen(n - i, i):
                yield [i] + p


    def partitions(n):
        """
        Returns a list of dictionaries with counted partitions.

        It obtains all partitions and then creates a dictionary that counts how
        many times a number appears in the partition.

        For example: for n=3
            [3]         ->  {3: 1}          because 3 appears one time
            [2, 1]      ->  {2: 1, 1: 1}    2 appears one time, and 1 one time
            [1, 1, 1]   ->  {1: 3}          1 appears three times
        Then, it would return the list [{3: 1}, {2: 1, 1: 1}, {1: 3}]

        The purpose of this method is to implement the vector that appears in
        the polynomial formula for Sn:

            1*j1 + 2*j2 + 3*j3 + ... + k*jk + ... + n*jn = n
        """
        # Get all partitions into a list
        parts = [p for p in partitionsGen(n)]

        # Go through every partition and form a dictionary with occurrences
        nparts = []
        for part in parts:
            counterD = {}   # dictionary to count occurrences
            for i in part:
                counterD[i] = counterD.get(i, 0) + 1
            nparts.append(counterD)

        return nparts


    def cycle_coefficient(jpartition, n):
        """
        Counts how many jk cycles of size k are in cycle index polynomial.

        It is the coefficient of Sk**jk in the cycle index polynomial formula.

        Using the language of Graphical Enumeration Paperback by Frank Harary:

            Calculates the number of permutations in Sn whose cycle
            decomposition determines the partition jpartition, so that for each
            k,
                jk = jk(permutation)    # have jk parts equal to k

        The formula is: (n!) / PI( (k**jk)*jk!)

        where:
            PI is the product notation
            j, and jk are all the parts of the partition vector jpartition
        """
        divisor = 1
        for k, jk in jpartition.items():
            divisor *= (k**jk) * factorial(jk)

        return factorial(n) // divisor


    # main ---------------------------------------------------------------------

    h_partition_vectors = partitions(h)
    w_partition_vectors = partitions(w)

    total = 0
    for hp in h_partition_vectors:
        for wp in w_partition_vectors:
            # coefficient of each partition vector
            wcoeff = cycle_coefficient(wp, w)
            hcoeff = cycle_coefficient(hp, h)

            # Calculates the exponent of the direct group multiplication
            exponent = 0
            for r, jr in hp.items():
                for t, jt in wp.items():
                    exponent += gcd(r, t) * jr * jt

            total += wcoeff * hcoeff * s**exponent

    result = total // (factorial(h) * factorial(w))
    return str(result)
