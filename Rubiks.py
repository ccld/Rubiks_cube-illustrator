# -*- coding: utf-8 -*-
#!/usr/bin/env python
# =====================================================================

import argparse
import sys
# =====================================================================
def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Illustrator tool')    
    # Add arguments
    parser.add_argument('-o', '--output', type=str, 
                        help='video output file path')
    parser.add_argument('-p', '--parameters', type=str, required=True, 
                        help='actions code')
    parser.add_argument('-c', '--clean', type=str, default='False',
                    help='remove files (True/False)')
        
    args = parser.parse_args()
   
    clean_flag = args.clean.lower() == 'true'
    if clean_flag:
        print("delete files enabled")
    else:
        print("delete files disabled")
    
    if args.output is not None:
        print(f"video: {args.output}")
    
    if args.parameters:
        params = args.parameters #[float(x) for x in args.parameters.split(',')]
        print(f"Parameters: {params}")  
    
    print(f"Output file: {args.output}")

    process_actions(args)

def process_actions(args):
    rotations = parse_move_notation(args.parameters)
    print(rotations)    
    process= cubeprocess(rotations)
    print(f"Actions processed and saved to {args.output}")
     
def parse_move_notation(notation_string):
    moves = []
    i = 0    
    while i < len(notation_string):
        char = notation_string[i]
        i += 1
             
        # Determine the face and direction
        if char.isupper():
            face = char
            direction = 'cw'
        # Check if the next character is a number (repetition)
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

# =====================================================================
if __name__ == '__main__':
    main()
# ======================================================================
    
