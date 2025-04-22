# Rubiks_cube-illustrator
A mathematical visualization tool that represents a Rubik's Cube using overlapping Venn diagrams, allowing for intuitive tracking of cube state during move sequences.

![Rubik's Cube Checkboard pattern](https://github.com/ccld/Rubiks_cube-illustrator/blob/main/U2D2F2B2L2R2%20checkerboardYOG.png) 

## Overview

This project offers a novel way to visualize and simulate Rubik's Cube movements using a Venn diagram representation. Rather than showing the traditional 3D cube, this approach maps the cube's state onto a system of three overlapping circles, with colored nodes representing the cube's facets.

### Key Features

- **Intuitive Venn Diagram Visualization**: Represents the Rubik's Cube state using overlapping circles and colored nodes
- **Move Simulation**: Accurately simulates standard Rubik's Cube rotations clockwise (U, F, R, L, D, B faces, and M, E, S middle slices) or counterclockwise (i)
- **Sequence Execution**: Supports execution of multiple moves in sequence
- **Clockwise and Counterclockwise Rotations**: Implements standard cube notation for both CW and CCW moves

## How pattern generation Works

The representation uses three overlapping circles with concentric rings to create intersection points that correspond to the facets of a Rubik's Cube:

- **Colors**: The six standard Rubik's Cube colors (orange, red, green, blue, white, yellow) represent the different faces
- **Intersection Points**: Each colored node represents a facet of the cube
- **Rotations**: Moves are simulated by rotating colors between nodes according to how an actual Rubik's Cube would behave

## Technical Implementation

The visualization is built with Python using matplotlib for rendering. Key components include:

- Circle intersection calculation algorithms
- Rotation logic for each of the six faces and of the three middle slices
- Color management and tracking
- Move sequencing and execution

## Usage

The main executable script is Rubiks.py. It takes an orientation parameter of the cube on the game mat , and optional parameters
-   a parameter -x for the string of the 3 colors of the chosen corner as perspective view of the cube, in the order FUR (Front at left, UP at top, Right at right)
-	a parameter -t for the algorithm of twists to be performed on sequence. 
-	a boolean flag -c (cleaning) for deleting all intermediate png files created by the successive twists of the cube
-	a boolean flag -o (output) for an animated mp4 file of all the diagrams created by the successive twists of the cube

```
# For example, if the top cube is white when you begin, with blue at right you could execute the command line
    'Rubiks_illustrator.py -x RWB -t R2L2U2D2F2B2'  to perform Right twice , Left twice, UP twice et cetera

# For coding the algorithm don't use spaces between the moves

# For a counterclockwise rotation replace the usual prime symbol (') by the lower case character 'i' like "inverse" (exponent "-1" in mathematical notation)

```

## Mathematical Background

This representation leverages principles from:
- Graph theory (polyhedral graph on eight nodes)
- Combinatorial topology
- Group theory (the basis of Rubik's Cube movements)

The visualization creates a mapping between the permutation group of the Rubik's Cube and a visually intuitive graph structure which is the planar graph representation skeleton of the dual octahedron.

## Installation

```bash
git clone https://github.com/yourusername/rubiks-cube-illustrator.git
cd rubiks-cube-illustrator
pip install -r requirements.txt
```

## Requirements

- Python 3.6+
- NumPy
- Matplotlib

## Future Enhancements

- Input of a scrambled cube to be solved
- Solution algorithms visualization
- Cube state import/export
- Interactive GUI for move input


## License

[![CC BY-NC](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)
Copyright © 2025

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to 
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

## Acknowledgments

This project was inspired by mathematical approaches to visualizing complex systems and the elegant mathematical structure of the Rubik's Cube.

[Lecture note](https://math.berkeley.edu/~hutching/rubik.pdf) "Slides for a Berkeley Math Circle colloquium talk on Rubik's cube, 2022." From Professor Michael Hutchings, UC Berkeley, 
