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
    char_cw=['U','F','R','L','B','D','S']
    char_acw = ['E','M']
    while i < len(notation_string):
        # Get the current character (face)
        char = notation_string[i]
        i += 1
        
        # Determine the face and direction
        if char.isupper() and char in char_cw:
            face = char
            direction = 'cw'; 
        elif char.isupper() and char in char_acw:
            face = char
            direction = 'ccw';
        else: sys.exit(f'Unknown slice move {char}')
                # Check if the next character is a number (repetition)
        repetitions = 1

        if i < len(notation_string) and notation_string[i]== 'r':
            if notation_string[i-1] in char_cw: direction = 'ccw' 
            else: direction = 'cw'
            i += 1

        if i < len(notation_string) and notation_string[i].isdigit():
            repetitions = int(notation_string[i])
            i += 1
        # Add the move(s) to the list
        for _ in range(repetitions):
            moves.append((face, direction))
    
    print(moves)
    return moves
