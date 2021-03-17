def solution(s):
    # constants
    WAKING_RIGHT = '>'
    WAKING_LEFT = '<'

    def countEmployeesInOderDirection(subhallway, direction):
        """ Count employees coming ahead walking in the other direction """
        count = 0
        for employee in subhallway:
            if employee == direction:
                count += 1
        return count

   # convert s into a list
    hallway = [char for char in s]

    encouters = 0
    # For all employees count encounters:
    #   other employees walking ahead but in the other direction
    for index, employee in enumerate(hallway):
        if employee == WAKING_RIGHT:
            encouters += countEmployeesInOderDirection(hallway[index:], WAKING_LEFT)

        if employee == WAKING_LEFT:
            encouters += countEmployeesInOderDirection(hallway[:index], WAKING_RIGHT)

    return encouters
