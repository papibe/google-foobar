def solution(x, y):

    # | 7
    # | 4 8
    # | 2 5 9
    # | 1 3 6 10

    def sum1to(n):
        return (n*(n+1))/2

    # if right edge is (n,1)
    # then triangle size = 1 + 2 + 3... = n(n+1)/2

    # value at (x,1)
    bottomValue = sum1to(x)

    # now we can go up in the same column
    # how much: x + (x+1) + ... (x-y-2)
    Sn = sum1to(x+y-2)
    Sk = sum1to(x-1)
    Sx = Sn - Sk

    id = bottomValue + Sx

    return str(id)
