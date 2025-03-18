# Rubiks_cube-illustrator
A mathematical visualization tool that represents a Rubik's Cube using overlapping Venn diagrams, allowing for intuitive tracking of cube state during move sequences.

![Rubik's Cube Checkboard pattern](https://github.com/ccld/Rubiks_cube-illustrator/blob/main/Figure_2025-03-08.png) 

## Overview

This project offers a novel way to visualize and simulate Rubik's Cube movements using a Venn diagram representation. Rather than showing the traditional 3D cube, this approach maps the cube's state onto a system of three overlapping circles, with colored nodes representing the cube's facets.

### Key Features

- **Intuitive Venn Diagram Visualization**: Represents the Rubik's Cube state using overlapping circles and colored nodes
- **Move Simulation**: Accurately simulates standard Rubik's Cube rotations (U, F, R, L, D, B faces, and M, E, S middle slices)
- **Sequence Execution**: Supports execution of multiple moves in sequence
- **Clockwise and Counterclockwise Rotations**: Implements standard cube notation for both CW and CCW moves

## How It Works

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

Using the command line, we define the colors of the UP and FRONT sides of the Rubik's Cube when it is placed on the play mat.
We also enter the sequence of moves to be performed.

```python
# Generate the initial state with red face as Down at bottom of diagram and green face as Front at the left of diagram
initial_points, initial_colors = generate_initial_points()

# Visualize the initial state
create_rubiks_diagram(initial_points, initial_colors)

# Perform a sequence of moves (e.g., R U R' U')
points_after_moves, colors_after_moves = perform_moves(
    initial_points, initial_colors, 
    [('R', 'cw'), ('U', 'cw'), ('R', 'ccw'), ('U', 'ccw')]
)

# Visualize the result
create_rubiks_diagram(points_after_moves, colors_after_moves)
```

## Mathematical Background

This representation leverages principles from:
- Graph theory
- Combinatorial topology
- Group theory (the basis of Rubik's Cube movements)

The visualization creates a mapping between the permutation group of the Rubik's Cube and a visually intuitive graph structure.

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

- Interactive GUI for move input
- Solution algorithms visualization
- Pattern generation
- Cube state import/export

## License

[![CC BY-NC](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)
Copyright © 2025

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to 
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

## Acknowledgments

This project was inspired by mathematical approaches to visualizing complex systems and the elegant mathematical structure of the Rubik's Cube.
