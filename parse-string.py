def parse_move_notation(notation_string):
    """
    Parse a move notation string into a list of (face, direction) tuples for perform_moves.
    
    :param notation_string: String like 'FLRU2Lr' where:
                            - Uppercase letters are clockwise rotations
                            - Lowercase letters are counterclockwise rotations
                            - Numbers after a letter repeat that move that many times
    :return: List of (face, direction) tuples
    """
    moves = []
    i = 0
    
    while i < len(notation_string):
        # Get the current character (face)
        char = notation_string[i]
        i += 1
        
        # Determine the face and direction
        if char.isupper():
            face = char
            direction = 'cw'  # Uppercase is clockwise
        else:
            face = char.upper()
            direction = 'ccw'  # Lowercase is counterclockwise
        
        # Check if the next character is a number (repetition)
        repetitions = 1
        if i < len(notation_string) and notation_string[i].isdigit():
            repetitions = int(notation_string[i])
            i += 1
        
        # Add the move(s) to the list
        for _ in range(repetitions):
            moves.append((face, direction))
    
    return moves

"""
example
checker = 'U2D2L2R2F2B2'

parse_move_notation(checker)
Out[49]: 
[('U', 'cw'),
 ('U', 'cw'),
 ('D', 'cw'),
 ('D', 'cw'),
 ('L', 'cw'),
 ('L', 'cw'),
 ('R', 'cw'),
 ('R', 'cw'),
 ('F', 'cw'),
 ('F', 'cw'),
 ('B', 'cw'),
 ('B', 'cw')]
 """

