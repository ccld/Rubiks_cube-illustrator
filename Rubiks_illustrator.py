"""Rubiks_illustrator.py: a Rubik's cube perspective image simulator tool using overlapping Venn diagram
"""
#!/usr/bin/env python3
# ===============================
import sys, getopt

from structure import *
from sketch import display

def Rubiks(twists):
    """Parse Rubik's Cube notation into a list of moves."""
    # Check if argv is a list or a string
    if isinstance(twists, list):
        # If it's a list (like from sys.argv), join it
        notation_string = ''.join(argv)
    else:
        # If it's already a string
        notation_string = twists
        
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
        if face in "BDLME":
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
    fur = None
    turns = ''
    outfile = False
    cleanfile = False
    
    optlist, args = getopt.getopt(argv, "vx:t:co")

    for o, a in optlist:
      if o in ("-v", "--verbose"):
        vb = True
      elif o in ("-x", "--upfront"):
          fur  = a               
      elif o in ("-t", "--twist"):
          turns = a               
      elif o in ("-c", "--clean"):
          cleanfile = True
      elif o in ("-o", "--output"):
          outfile = True
    
    moves_list = Rubiks(turns)
    print(f"Parsed {len(moves_list)} moves: {moves_list}")
    print('FUR', fur) 

    corner=[]
      
    # Initialize the cube

    cube, face_colors, corner = framesetup.initialize_cube(orientation_code = fur) 
    points_after_url, colors_after_url, outergroups, centerpieces = framesetup.generate_initial_points(corner)
    display.create_rubiks_diagram(points_after_url, colors_after_url,fur,'start')

    if len(moves_list) > 0:
        if outfile:
            display.create_animation( fur, moves_list, twists = turns, cleanfile= cleanfile) # output_filename=output, fps=1,
        else:
            for move in moves_list:
                print(move)
                points_after_url, colors_after_url = perform_moves(
                    points_after_url, colors_after_url,
                    [move], outergroups,centerpieces
                    ) 
                display.create_rubiks_diagram(points_after_url, colors_after_url, fur, subtext)

        # check 6x9 cubelets color
    unique_colors = np.unique(colors_after_url)
    color_counts = {color: colors_after_url.count(color) for color in unique_colors}
    print(color_counts)
    for color in unique_colors: 
        if colors_after_url.count(color) != 9:
            print(color, 'error color count')
        else: print (color, 'OK')        
    return 
# =======================================================
if __name__ == "__main__":
    n=3 # for diagraam subtitle 
    print ('Argument List:', sys.argv[1:])        
    subtext = 'test'
    main(sys.argv[1:])
