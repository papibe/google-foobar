@profile
def solution(M, F):

    # Strategy:
    # - reverse replication.
    # - try to apply as many steps on one rule as possible (this works very well
    #   when numbers are apart)

    mach = long(M)
    facula = long(F)

    # no replication yet
    generation = 0

    # Edge case
    if mach == 1 and facula == 1:
        return str(generation)

    # Reverse replication cycle
    while mach > 1 and facula > 1:
        # If one is grater that the other we can conclude which rule was applied
        if mach > facula:
            generation += (mach / facula)
            mach = mach % facula
        else:
            generation += (facula / mach)
            facula = facula % mach


    # Perfect reverse replication to the origin
    if (mach == 1 and facula == 1):
        return str(generation)

    # Two special cases that saves computation time:
    # if any value is 1, it means only one side of the rules was applied, thus
    # it is straightforward how many steps were applied
    if mach == 1:
        return str(generation + facula - 1)

    if facula == 1:
        return str(generation + mach - 1)

    return "impossible"
