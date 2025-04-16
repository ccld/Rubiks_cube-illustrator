# -*- coding: utf-8 -*-
#!/usr/bin/env python
# =====================================================================
import sys
import numpy as np

def initialize_cube(orientation_code):
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
        'BOY',
        'BRW',
        'BWO',
        'BYR',
        'GOW',
        'GRY',
        'GWR',
        'GYO',
        'OBW',
        'OGY',
        'OWG',
        'OYB',
        'RBY',
        'RGW',
        'RWB',
        'RYG',
        'WBR',
        'WGO',
        'WOB',
        'WRG',
        'YBO',
        'YGR',
        'YOG',
        'YRB',
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

def get_color_center(face_color):
    colors_digit =  {
         "W" :0, # "white",
         "Y" :1, # "yellow",
         "G" :2, # "green",
         "B" :3, # "blue",
         "O" :4, # "orange",
         "R" :5, # "red"
        }
    return colors_digit.get(face_color, "Unknown")

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
  
def generate_initial_points(corner):
    consts = get_constants()
    centers = consts['centers']
    circle_radii= consts['circle_radii']
    """Generate initial intersection points and colors."""
    intersections = []
    colors = []
    Xpoints= []
    Xcenter= []    
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
                                if (i,j) == (1,2)  : 
                                    
                                    if point[1]> 0:
                                        row = (0,point[0], point[1])
                                        if (r1_idx,r2_idx) != (1,1) : Xpoints.append(row)
                                        else: Xcenter.append(row) 
                                    elif point[1] < 0: 
                                        row = (1,point[0], point[1])
                                        if (r1_idx,r2_idx) != (1,1) : Xpoints.append(row)
                                        else: Xcenter.append(row) 
                                        
                                if (i,j) == (0,1)  : 
                                    
                                    if point[0] > 0:
                                        row = (5,point[0], point[1])
                                        if (r1_idx,r2_idx) != (1,1) : Xpoints.append(row)
                                        else: Xcenter.append(row) 
                                    elif point[0] < 0: 
                                        row = (4,point[0], point[1])
                                        if (r1_idx,r2_idx) != (1,1) : Xpoints.append(row)
                                        else: Xcenter.append(row)                                         
    
                                if (i,j) == (0,2)  : 
                                    
                                    if point[0] < 0:
                                        row = (2,point[0], point[1])
                                        if (r1_idx,r2_idx) != (1,1) : Xpoints.append(row)
                                        else: Xcenter.append(row) 
                                    elif point[0] > 0: 
                                        row = (3,point[0], point[1])
                                        if (r1_idx,r2_idx) != (1,1) : Xpoints.append(row)
                                        else: Xcenter.append(row)                                         
    faceouter = {0: [], 1: [], 2: [], 3: [] , 4: [], 5: []}

    for idx, item in enumerate(Xpoints):
        face = item[0]
        x_coord = item[1]
        y_coord = item[2]
        faceouter[face].append([x_coord, y_coord])
         
        
    centerpieces = {0: [], 1: [], 2: [], 3: [] , 4: [], 5: []}
    for idx, item in enumerate(Xcenter):
        face = item[0]
        x_coord = item[1]
        y_coord = item[2]
        centerpieces[face].append([x_coord, y_coord])
        
    outergroups = {0: [], 1: [], 2: [], 3: [] , 4: [], 5: []}
    for face in faceouter:
        face_indices = []
        if face == 0: 
            print('center UP', centerpieces[face][0][0], centerpieces[face][0][1] )
            print('outer', len(faceouter[face]), faceouter[face])  
    
        for i, point in enumerate(intersections):
            if i in faceouter[face]:
                continue
            sep = np.sqrt((point[0] - centerpieces[face][0][0])**2 + (point[1] - centerpieces[face][0][1])**2)
            if 0.001 < sep < 0.7 :
                face_indices.append(i)
                
        # Calculate the angle of each point relative to the  center
        point_angles = [(i, np.arctan2((intersections[i][1] - centerpieces[0][0][1]), (intersections[i][0]-centerpieces[0][0][0]))) for i in face_indices]     
            # Sort points by angle to get them in order around the circle
        point_angles.sort(key=lambda x: x[1])
        sorted_indices_with_angles = [(idx, angle) for idx, angle in point_angles]
        #print('moving points', len(point_angles), point_angles)
        point_angles.sort(key=lambda x: x[1])
        #print('moving points', len(point_angles))
        
        sorted_indices_with_angles = [(idx, angle) for idx, angle in point_angles]
        
        # Group into 4 sets of 3 points with their angles
        groups_with_angles = [sorted_indices_with_angles[i:i+2] for i in range(0, 8, 2)]
        
        # For each group, sort by angle again (may not be necessary if already sorted)
        
        for group in groups_with_angles:
            # Sort each group by angle
            group.sort(key=lambda x: x[1])
            # Extract just the indices
            sorted_group = [idx for idx, angle in group]
            outergroups[face].append(sorted_group)        
        
    return intersections, colors , outergroups, centerpieces

def perform_moves(points, colors, moves , outergroups):
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
    # Circle center positions
    circle_centers = {
        0: centers[0],  # U face center
        1: centers[0],  # D face center (same x,y as U but different radius)
        2: centers[1],  # F face center
        3: centers[1],  # B face center (same x,y as F but different radius)
        4: centers[2],  # L face center
        5: centers[2],  # R face center (same x,y as L but different radius)
        }
    
    # Map face codes to indices and radius indices
    face_map = {'U': 0, 'D': 1, 'F': 2, 'B': 3, 'L': 4, 'R': 5,
                'M': 'M', 'S': 'S', 'E': 'E'}
    
    # Map faces to their appropriate radius index (0=inner, 2=outer)
    radius_map = {'U': 0, 'D': 2, 'F': 0, 'B': 2, 'L': 2, 'R': 0}
    
    for face_code, direction in moves:
        if face_code in 'UDFBLR':  # Regular face moves
            face = face_map[face_code]
            radius_idx = radius_map[face_code]
            
            # Rotate the face edges
            current_points, current_colors = rotate_face(
                current_points, current_colors, direction, 
                center=circle_centers[face], radius=circle_radii[radius_idx]
            )
            
            # Dynamically detect corner pieces for this specific layer
            corner_groups = detect_layer_corners(
                current_points, centerpieces[face], 
                circle_radii[radius_idx], face_code
            )
            
            # Rotate the corners
            if corner_groups:
                current_points, current_colors = rotate_facelet(
                    current_points, current_colors, corner_groups, direction
                )
            
        else:  # Middle slice moves
            if face_code == 'M':
                current_points, current_colors = rotate_face(
                    current_points, current_colors, direction, 
                    center=centers[2], radius=circle_radii[1]
                )
            elif face_code == 'S':
                current_points, current_colors = rotate_face(
                    current_points, current_colors, direction, 
                    center=centers[1], radius=circle_radii[1]
                )
            elif face_code == 'E':
                current_points, current_colors = rotate_face(
                    current_points, current_colors, direction, 
                    center=centers[0], radius=circle_radii[1]
                )
    
    return current_points, current_colors

def detect_layer_corners(points, centerpieces, layer_radius, face_code):
    """
    Detect corner pieces specifically for the layer being rotated.
    
    Args:
        points: List of point coordinates
        face_center: Center coordinates of the face
        layer_radius: Radius of the specific layer being rotated
        face_code: Face code (U, D, F, B, L, R)
    
    Returns:
        List of corner groups for this specific layer
    """
    # Map face codes to indices and radius indices
    face_map = {'U': 0, 'D': 1, 'F': 2, 'B': 3, 'L': 4, 'R': 5,
                'M': 'M', 'S': 'S', 'E': 'E'}

    # Tolerance for detecting points on the layer
    radius_tolerance = 0.09
    # For each face, determine where the 4 corners should be located
    # in terms of angular regions around the face center
    corner_regions = {
        'U': [(-np.pi/4, np.pi/4), (np.pi/4, 3*np.pi/4), 
              (3*np.pi/4, 5*np.pi/4), (5*np.pi/4, 7*np.pi/4)],
        'D': [(-np.pi/4, np.pi/4), (np.pi/4, 3*np.pi/4), 
              (3*np.pi/4, 5*np.pi/4), (5*np.pi/4, 7*np.pi/4)],
        'F': [(-np.pi/4, np.pi/4), (np.pi/4, 3*np.pi/4), 
              (3*np.pi/4, 5*np.pi/4), (5*np.pi/4, 7*np.pi/4)],
        'B': [(-np.pi/4, np.pi/4), (np.pi/4, 3*np.pi/4), 
              (3*np.pi/4, 5*np.pi/4), (5*np.pi/4, 7*np.pi/4)],
        'L': [(-np.pi/4, np.pi/4), (np.pi/4, 3*np.pi/4), 
              (3*np.pi/4, 5*np.pi/4), (5*np.pi/4, 7*np.pi/4)],
        'R': [(-np.pi/4, np.pi/4), (np.pi/4, 3*np.pi/4), 
              (3*np.pi/4, 5*np.pi/4), (5*np.pi/4, 7*np.pi/4)]
    }
    
    face = face_map[face_code]
    print('def detect_layer_corners',face)
    print(centerpieces)
    print('centerx', centerpieces[0][0], 'centery' ,centerpieces[0][1] )
    print('len(points)' , len(points))
    # Find points that could be corners for this layer
    corner_candidates = []
    for i, point in enumerate(points):
        # Calculate distance from face centerpiece
        distance = np.sqrt((point[0] - centerpieces[0][0])**2 + (point[1] - centerpieces[0][1])**2)
        # If point is close to the layer radius, it's on the face edge and not a corner
        if 0.001<distance < 0.7:
            corner_candidates.append(i)
    # Calculate the angle of each point relative to the  center
    point_angles = [(i, np.arctan2(points[i][1] - centerpieces[0][1], points[i][0] - centerpieces[0][0])) 
                    for i in  corner_candidates]     
        # Sort points by angle to get them in order around the circle
    point_angles.sort(key=lambda x: x[1])
    sorted_indices_with_angles = [(idx, angle) for idx, angle in point_angles]
    
    point_angles.sort(key=lambda x: x[1])
    
    sorted_indices_with_angles = [(idx, angle) for idx, angle in point_angles]
    
    # Group into 4 sets of 2 points with their angles
    groups_with_angles = [sorted_indices_with_angles[i:i+2] for i in range(0, 8, 2)]
    print('4 sets',groups_with_angles)
    # For each group, extract just the indices
    corner_groups = []
    for group in groups_with_angles:
        sorted_group = [idx for idx, angle in group]
        corner_groups.append(sorted_group)

    # We should ideally have 4 groups
    if len(corner_groups) != 4:
        print(f"Warning: Expected 4 corner groups, found {len(corner_groups)}")
    
    return corner_groups

    
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
        shifted_groups = groups[1:] + [groups[0]]
    else:  # ccw
        # For  face, we want to rotate clockwise when viewed from  side
        shifted_groups = [groups[-1]] + groups[:-1]
    
    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]
    return points, new_colors

def rotate_facelet( points, colors, corner_groups, direction ):  
    new_colors = colors.copy()
    if direction == 'cw'and face_code in ("UFR"):
        # For  face, we want to rotate counterclockwise when viewed from  side
        shifted_groups = corner_groups[1:] + [corner_groups[0]]
    else:  # ccw
        # For  face, we want to rotate clockwise when viewed from  side
        shifted_groups = [corner_groups[-1]] + corner_groups[:-1]
        
    if direction == 'cw' and face_code in ("BLD"):
        # Clockwise rotation
        shifted_groups = [corner_groups[-1]] + corner_groups[:-1]
    else:  # ccw
        # Counter-clockwise rotation
        shifted_groups =  corner_groups[1:] + [corner_groups[0]]
 
    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]
    print('facelet_shifted',shifted_groups)

    return points, new_colors

