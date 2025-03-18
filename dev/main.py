#!/usr/bin/env python3
import sys, getopt

from  .wdir.core import rubiks_start
from Rubiks import *

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
        if i < len(notation_string) and notation_string[i] == "'":
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

def main():
    """Main function to run the Rubik's Cube simulation."""
    orientation = '42'
    # Check if move notation was provided as a command line argument
    if len(sys.argv) > 1:
        notation = sys.argv[1]
    else:
        notation = input("Enter Rubik's cube notation: ")
    
    # Parse the notation
    moves_list = Rubiks(notation)
    print(f"Parsed {len(moves_list)} moves: {moves_list}")
    
    # Initialize the cube
    cube = initialize_cube()
    
    # Execute the moves
    result_cube = execute_moves(cube, moves_list) #17/3 'tuple' object has no attribute 'copy'
    
    # Optionally visualize the result
    try:
        from sketch.display import display_cube
       # display_cube(result_cube) 
        display_cube(cube, orientation) #17/3 TypeError: unhashable type: 'numpy.ndarray'
    except ImportError:
        print("Display module not available.")
    
    # Optionally save a video of the moves
    try:
        from sketch.video import create_video
        create_video(cube, moves_list, "cube_solution.mp4")
    except ImportError:
        print("Video module not available.")
      
    return
  
rubiks_start()    

if __name__ == "__main__":
    main(sys.argv[1:])
