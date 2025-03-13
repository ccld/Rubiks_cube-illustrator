"""
Function to parse a movement notation string like 'FLRU2Lr' into a format that can be used with the perform_moves function. Here's how I'll interpret the notation:

The parser follows standard Rubik's cube notation:
Letters without modifiers (F, L, R, U) represent clockwise rotations of that face (Front, Left, Right, and Up faces)
A number after a letter means repeat that move that many times (U2 = perform U twice)
Lowercase letters (like r) represent counterclockwise rotations

Implementation will:
Parse 'FLRU2Lr' into the moves: (F,cw), (L,cw), (R,cw), (U,cw), (U,cw), (L,ccw), (R,ccw)
"""

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
            
        # Check if the next character is a lower char or a number (repetition)
        repetitions = 1
        if i < len(notation_string) and notation_string[i].islower():
            direction = 'ccw'  # Lowercase is counterclockwise
            i += 1
        if i < len(notation_string) and notation_string[i].isdigit():
            repetitions = int(notation_string[i])
            i += 1
        
        # Add the move(s) to the list
        for _ in range(repetitions):
            moves.append((face, direction))
    print(moves)
    return moves
