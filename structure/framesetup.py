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

    corner_colors= [
         'BWO',
         'BYR',
         'GRY',
         'GWR',
         'GYO',
         'OGY',
         'OWG',
         'OYB',
         'RBY',
         'RGW',
         'RWB',
         'RYG',
         'WGO',
         'WOB',
         'WRG',
         'YGR',
         'YRB',
         'YRB'
         ]

    fur= orientation_code
    
    if fur in corner_colors: 
        front_color = get_color_center(fur[0])
        up_color = get_color_center(fur[1])
        right_color = get_color_center(fur[2])
        
        down_color = get_opposite_color(up_color)
        left_color = get_opposite_color(right_color)
        back_color = get_opposite_color(front_color)
        print (f"UP: {get_color_name(up_color)}; RIGHT: {get_color_name(right_color)}; FRONT: {get_color_name(front_color)}")
        print (f"DOWN: {get_color_name(down_color)}; BACK: {get_color_name(back_color)}; LEFT: {get_color_name(left_color)}")

    else: 
        print(f'unknown corner: {fur}')
        sys.exit()

    # Create a solved cube where each face has a unique color/number
    cube = np.zeros((6, 3, 3), dtype=int)
    
        # Assign colors to faces
    face_colors = [up_color, down_color, front_color,
                   back_color, left_color, right_color]

    for i in range(6):
        cube[i, :, :] = face_colors[i]

    corner = [face_colors[5], face_colors[2], face_colors[0]]

    return cube, face_colors, corner

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
                                
                                if (i,j)   == (0,1): b = corner[0]
                                elif (i,j) == (0,2): b = corner[1]
                                elif (i,j) == (1,2): b = corner[2]
    
                                if (distance < 1.912 ):
                                    color = get_color_name(b)
                                    colors.append(color)
                                else:
                                    # Outer regions - opposite colors of visible faces
                 
                                    c =get_opposite_color(b)
                                    color = get_color_name(c)
                                    colors.append(color)                                                     
    
    return intersections, colors

def perform_moves(points, colors, moves):
    """
    Perform a sequence of moves starting from the given state.    
    :param points: List of intersection points
    :param colors: List of colors for the points
    :param moves: List of tuples (face, direction) 
                  where face is 'U' for up, 'R' for right, 'F' for front
                  and direction is 'cw' or 'ccw'
    :return: Tuple of final points and colors
    """
    consts = get_constants()
    centers = consts['centers']
    circle_radii= consts['circle_radii']
    current_points = points.copy()
    current_colors = colors.copy()
   
    for face, direction in moves:
            if face == 'U':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[0],radius=circle_radii[0])
            elif face == 'F':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[1],radius=circle_radii[0])
            elif face == 'R':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[2],radius=circle_radii[0])
            elif face == 'L':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[2],radius=circle_radii[2])
            elif face == 'B':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[1],radius=circle_radii[2])
            elif face == 'D':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[0],radius=circle_radii[2])
            elif face == 'M':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[2],radius=circle_radii[1])
            elif face == 'S':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[1],radius=circle_radii[1])
            elif face == 'E':
                current_points, current_colors = rotate_face(current_points, current_colors, direction, center=centers[0],radius=circle_radii[1])

    return current_points, current_colors
    
def rotate_face(points, colors, direction, center ,radius):    
    # Find indices of points on the inner circle of the  face
    face_indices = []
    for i, point in enumerate(points):
        # Check if point is on the smallest circle of the  face (with tolerance)
        if abs(np.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2) - radius) < 0.2:
            face_indices.append(i)
    
    # We should have exactly 12 points
    if len(face_indices) != 12:
        print(f"Warning: Expected 12 points on inner circle of  face, found {len(face_indices)}")
    
    # Enhanced grouping for  face - grouping points based on proximity and position
    # Calculate the angle of each point relative to the  center
    point_angles = [(i, np.arctan2(points[i][1] - center[1], 
                                   points[i][0] - center[0])) 
                   for i in face_indices]     
    # Sort points by angle to get them in order around the circle
    point_angles.sort(key=lambda x: x[1])
    sorted_indices_with_angles = [(idx, angle) for idx, angle in point_angles]
    
    # Group into 4 sets of 3 points with their angles
    groups_with_angles = [sorted_indices_with_angles[i:i+3] for i in range(0, 12, 3)]
    
    # For each group, sort by angle again (may not be necessary if already sorted)
    groups = []
    for group in groups_with_angles:
        # Sort each group by angle
        group.sort(key=lambda x: x[1])
        # Extract just the indices
        sorted_group = [idx for idx, angle in group]
        groups.append(sorted_group)
        
    # Now perform the rotation
    new_colors = colors.copy()
    
    if direction == 'cw':
        # For  face, we want to rotate counterclockwise when viewed from  side
        shifted_groups = [groups[1], groups[2], groups[3], groups[0]]
    else:  # cw
        # For  face, we want to rotate clockwise when viewed from  side
        shifted_groups = [groups[3], groups[0], groups[1], groups[2]]
    
    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]
    return points, new_colors
