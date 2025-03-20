# -*- coding: utf-8 -*-
#!/usr/bin/env python
# =====================================================================

import numpy as np

def initialize_cube(orientation_code='02'):
    """
    Initialize a 3D numpy array representing a Rubik's cube with optional orientation.
    
    Args:
        orientation_code (str, optional): A two-digit string specifying the orientation.
                                         First digit is UP face color, second is FRONT face color.
                                         Default is None, which uses standard orientation.
    
    Returns:
        np.ndarray: A 3D array representing the cube state
        
    Cube representation:
    - 6 faces (0=Up, 1=Down, 2=Front, 3=Back, 4=Left, 5=Right)
    - Each face is 3x3
    - Colors are represented by integers 0-5
    """
        # Create a solved cube where each face has a unique color/number

    # Colors for the Rubik's cube faces
    face_colors = {
    'orange': '#FFA500',  # Up (U)
    'red': '#FF0000',     # Down (D)
    'green': '#00FF00',   # Left (L)
    'blue': '#0000FF',    # Right (R)
    'white': '#FFFFFF',   # Front (F)
    'yellow': '#FFFF00'   # Back (B)
    }

    # Define opposite colors for each face
    opposite_colors = {
    'orange': 'red',    # standard Rubiks convention
    'green': 'blue',    # 
    'white': 'yellow', 
    'red': 'orange',
    'blue': 'green',
    'yellow':'white',
    'Unknown':'Unknown'
    }

    # Cube configuration
    side_length = 4.
    width = 638
    height = 638

    # Create a solved cube where each face has a unique color/number
    cube = np.zeros((6, 3, 3), dtype=int)
    
    if orientation_code is None:
        # Default orientation: each face index equals its color
        for i in range(6):
            cube[i, :, :] = i
    else:
        # Custom orientation based on orientation_code
        # Parse the orientation code
        up_color = int(orientation_code[0])
        front_color = int(orientation_code[1])
        
        # Validate the input colors
        if up_color == front_color or not (0 <= up_color < 6 and 0 <= front_color < 6):
            raise ValueError("Invalid orientation code. Colors must be different and between 0-5.")
        
        # Determine the remaining faces based on standard Rubik's cube structure
        # The opposite of UP is DOWN, opposite of FRONT is BACK, etc.
        down_color = get_opposite_color(up_color)
        back_color = get_opposite_color(front_color)
        
        # Determine LEFT and RIGHT colors
        # This is a bit complex due to Rubik's cube constraints
        remaining_colors = set(range(6)) - {up_color, down_color, front_color, back_color}
        remaining_colors = list(remaining_colors)
        
        # In a standard Rubik's cube, if UP is white (0) and FRONT is green (2),
        # then LEFT would be orange (4) and RIGHT would be red (5)
        # We need to determine the correct positions based on the specified UP and FRONT
        if (up_color, front_color) in [(0, 2), (2, 1), (1, 3), (3, 0)]:
            left_color, right_color = remaining_colors
        else:
            right_color, left_color = remaining_colors
        
        # Assign colors to faces
        face_colors = [up_color, down_color, front_color, back_color, left_color, right_color]
        print(face_colors[:])
        for i in range(6):
            cube[i, :, :] = face_colors[i]
    
    return cube , face_colors

def get_opposite_color(color):
    """Get the opposite color in a standard Rubik's cube."""
    opposites = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}
    return opposites.get(color)

def get_face_name(face_index):
    """Convert face index to its name."""
    faces = {
        0: "Up",
        1: "Down",
        2: "Front",
        3: "Back", 
        4: "Left",
        5: "Right"
    }
    return faces.get(face_index, "Unknown")

def get_color_name(color_index):
    """Convert color index to its name."""
    colors = {
        0: "white",
        1: "yellow",
        2: "green",
        3: "blue",
        4: "orange",
        5: "red"
    }
    return colors.get(color_index, "Unknown")

def get_circle_intersections(center1, center2, radius1, radius2):
    """Find the intersection points of two circles."""
    x1, y1 = center1
    x2, y2 = center2

    # Distance between centers
    d = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Circles intersect at two points
    a = (radius1**2 - radius2**2 + d**2) / (2 * d)
    h = np.sqrt(radius1**2 - a**2)

    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d

    x4_1 = x3 + h * (y2 - y1) / d
    y4_1 = y3 - h * (x2 - x1) / d

    x4_2 = x3 - h * (y2 - y1) / d
    y4_2 = y3 + h * (x2 - x1) / d

    return [(x4_1, y4_1), (x4_2, y4_2)]

def get_constants():
    r = np.sqrt(3)/6  
    centers = []
        # Top center
        # Bottom left
        # Bottom right   
    centers = [(0,2.5),(-2,-2*r),(2,-2*r)]
    # Circle radii
    circle_radii = [2.4, 2.8, 3.2]
    # Define constants in a dictionary
    constants = {
        'centers': centers,
        'circle_radii': circle_radii,
        }
    return constants

    
def generate_initial_points():
    consts = get_constants()
    centers = consts['centers']
    circle_radii= consts['circle_radii']
    """Generate initial intersection points and colors."""
    intersections = []
    colors = []
    paired_center_colors = {
        (0, 1): 'white',   # Face RIGHT
        (0, 2): 'green',   # face FRONT 
        (1, 2): 'orange',  # face UP
    }
    
    paired_center_colors = {
        (0, 1): 5,   # Face RIGHT
        (0, 2): 2,   # face FRONT 
        (1, 2): 0  # face UP
    }
    
    # Find intersections and colors
    for i, center1 in enumerate(centers):
        for j, center2 in enumerate(centers):
            if i < j:  # Avoid duplicate pairs
                for r1_idx, radius1 in enumerate(circle_radii):
                    for r2_idx, radius2 in enumerate(circle_radii):
                        # Find intersections between circles from different sets
                        points = get_circle_intersections(center1, center2, radius1, radius2)

                        for point in points:
                            # Check if point is already in the list (within a small tolerance)
                            is_duplicate = False
                            for existing_point in intersections:
                                if np.sqrt((point[0] - existing_point[0])**2 + (point[1] - existing_point[1])**2) < 0.1:
                                    is_duplicate = True
                                    break

                            if not is_duplicate:
                                intersections.append(point)

                                # Calculate distance from diagram center
                                center_x, center_y = 0, 0.1 
                                distance = np.sqrt((point[0] - center_x)**2 + (point[1] - center_y)**2)

                                # Color assignment logic
                                if (distance < 1.912 ):
                                    # face (U/ D/ ...) ; face cube color
                                    a = paired_center_colors[(i,j)]
                                    color = get_color_name(a)
                                    colors.append(color)
                                    #color = 'white' #face_colors[a]
                                    
                                    # Inner regions - visible face colors
                                    # color = paired_center_colors.get((i, j), 'white')
                                else:
                                    # Outer regions - opposite colors of visible faces
                                    b = paired_center_colors[(i,j)]                        
                                    c =get_opposite_color(b)
                                    color = get_color_name(c)
                                    colors.append(color)
                                    # face / cube color
                                    #visible_color = paired_center_colors.get((i, j), 'white')
                                    #color = opposite_colors.get(visible_color, visible_color)                                                          
    
    return intersections, colors
