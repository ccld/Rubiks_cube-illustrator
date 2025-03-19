#!/usr/bin/env python3
import sys, getopt

from structure import framesetup
from structure.framesetup import *
from structure import moves
from structure.moves import *
from sketch.display import *

def Rubiks(argv):
    """Parse Rubik's Cube notation into a list of moves."""
    # Check if argv is a list or a string
    if isinstance(argv, list):
        # If it's a list (like from sys.argv), join it
        notation_string = ''.join(argv)
    else:
        # If it's already a string
        notation_string = argv
        
    moves = []
    i = 0
    while i < len(notation_string):
        # Get the current character (face)
        char = notation_string[i]
        i += 1
        
        # Skip non-alphabetic characters
        if not char.isalpha():
            continue
            
        # Keep the face as is (uppercase or lowercase matters in Rubik's notation)
        face = char
        
        # For slice turns (M, E, S), the default direction is counterclockwise
        if face in "MES":
            direction = 'ccw'  # Default for M, E, S is counterclockwise
        else:
            direction = 'cw'  # Default for all other moves is clockwise
            
        # Check for prime symbol (') which indicates the opposite of default direction
        if i < len(notation_string) and notation_string[i] == "!":
            # Flip the direction
            direction = 'cw' if direction == 'ccw' else 'ccw'
            i += 1
            
        # Check for repetition
        repetitions = 1
        if i < len(notation_string) and notation_string[i].isdigit():
            repetitions = int(notation_string[i])
            i += 1
            
        # Add the move(s) to the list
        for _ in range(repetitions):
            moves.append((face, direction))
            
    return moves

def main(argv):
    up ='42'
    # Check if argv is a list or a string
    if isinstance(argv, list):
        # If it's a list (like from sys.argv), join it
        notation_string = ''.join(argv)
    else:
        # If it's already a string
        notation_string = argv
    
    try:
        args = notation_string.split()
        turns = args[0]
        args = args[1:]        
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
    
    algo= Rubiks(turns)
    vb = False
    # Defaults 
    outfile = False
    
    optlist, args = getopt.getopt(args, "vx:co")
    for o, a in optlist:
        if o in ("-v", "--verbose"):
            vb = True
        elif o in ("-x", "--upfront"):
            up = a               
        elif o in ("-c", "--clean"):
            cleaner = True
        elif o in ("-o", "--output"):
            outfile = True
        else:
            assert False, "Unhandled option"
    
    print(f"Parsed orientation: {up}")   
    moves_list = Rubiks(turns)
    print(f"Parsed {len(moves_list)} moves: {moves_list}")
    # Initialize the cube
    cube = initialize_cube()   
    display_cube(cube, up)
    result_cube = excute_moves(cube, moves_list)
    return 

if __name__ == "__main__":
    main(sys.argv[1:])


