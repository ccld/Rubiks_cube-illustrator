# -*- coding: utf-8 -*-
#!/usr/bin/env python
# =====================================================================

# Globally useful modules:

import numpy
import os
import sys,getopt
import structure

# =====================================================================

def Rubiks(argv):
    # -------------------------------------------------------------------

    try:
        opts, args = getopt.getopt(argv, "hvp:",\
        ["help","verbose","pars"])
    except (getopt.GetoptError):
        print ('Error') # will print something like "option -a not recognized"
        return
    
    vb = False  
    pars = False
    
    # -------------------------------------------------------------------


    for o,a in opts:
        if o in ("-h", "--help"):
            print ('help')
            return
        elif o in ("-v", "--verbose"):
            vb = True
        elif o in ("-p","--parameters"):
            pars = True
            print ('create video file')
            return
        else:
            assert False, "Unhandled option"
    
        return

    # Check for datafiles in array args:

    print (len(args))

    if len(args) == 1:
        algorithm = args[:]

    else:
        print ('Error') # will print something like "option -a not recognized"
        return

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

    # Implement the animation
    rotations = parse_move_notation(algorithm)
    print(rotations)
    structure.illustrator(rotations)                 
return
# ======================================================================


if __name__ == '__main__':
    Rubiks(sys.argv[:])

# ======================================================================
    
