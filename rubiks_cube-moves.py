# -*- coding: utf-8 -*-
"""
Rubik's Cube Venn Diagram Move Simulation
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
import copy

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
    'orange': 'red',    # Top opposite bottom
    'green': 'blue',    # Left opposite right
    'white': 'yellow'   # Front opposite back
}

# Cube configuration
side_length = 4.

centers = []
     # Top center
    # Bottom left
      # Bottom right

r = np.sqrt(3)/6   
centers = [(0,2.5),(-2,-2*r),(2,-2*r)]
# Circle radii
circle_radii = [2.4, 2.8, 3.2]


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

def find_closest_point(point, point_list, tolerance=0.05):
    """Find the index of the closest point in the list."""
    for idx, existing_point in enumerate(point_list):
        if np.sqrt((point[0] - existing_point[0])**2 + (point[1] - existing_point[1])**2) < tolerance:
            return idx
    return -1

def rotate_points(points, center, angle_degrees):
    """Rotate points around a center point by a given angle."""
    # Convert angle to radians
    angle = np.radians(angle_degrees)
    
    # Rotation matrix
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])
    
    # Translate points relative to center, rotate, then translate back
    rotated_points = []
    for point in points:
        # Translate point relative to center
        translated_point = (point[0] - center[0], point[1] - center[1])
        
        # Rotate point
        rotated_point = np.dot(rotation_matrix, translated_point)
        
        # Translate back
        final_point = (rotated_point[0] + center[0], rotated_point[1] + center[1])
        rotated_points.append(final_point)
    
    return rotated_points

def create_rubiks_diagram(points, colors):
    """Create the Rubik's Cube Venn diagram."""
    plt.figure(figsize=(6.38,6.38), dpi=100)
    ax = plt.subplot(111, aspect='equal')
    
    # Draw concentric circles
    for center in centers:
        for radius in circle_radii:
            circle = Circle(center, radius, fill=False, color='gray', linestyle='-', linewidth=1)
            ax.add_patch(circle)
    
    # Draw the intersection points as colored nodes
    for point, color in zip(points, colors):
        plt.plot(point[0], point[1], 'o', markersize=15, markerfacecolor=face_colors[color], markeredgecolor='black')
    
    # Set plot limits and remove axes
    plt.xlim(-5.5, 5.5)
    plt.ylim(-5.5, 5.5)
    plt.axis('off')
    plt.title("Rubik's Cube Venn Representation", fontsize=14)
    plt.tight_layout()
    plt.show()

def generate_initial_points():
    """Generate initial intersection points and colors."""
    intersections = []
    colors = []
    paired_center_colors = {
        (0, 1): 'white',   # Between top and bottom-left (yellow and blue)
        (0, 2): 'green',   # Between top and bottom-right (yellow and red)
        (1, 2): 'orange',  # Between bottom-left and bottom-right (blue and red)
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
                                    # Inner regions - visible face colors
                                    color = paired_center_colors.get((i, j), 'white')
                                else:
                                    # Outer regions - opposite colors of visible faces
                                    visible_color = paired_center_colors.get((i, j), 'white')
                                    color = opposite_colors.get(visible_color, visible_color)                                                          
                                colors.append(color)
    
    return intersections, colors

def rotate_up_face(points, colors, direction='ccw'):
    """
    Perform a rotation of the UP (U) face by rotating colors at the 12 intersection points.  
    :param points: List of intersection points
    :param colors: List of colors for the points (current state)
    :param direction: 'cw' for clockwise, 'ccw' for counterclockwise
    :return: Tuple of points and updated colors
    """
    # Top center
    top_center = centers[0]
    inner_radius = circle_radii[0]
    
    # Find indices of points on the inner circle of the top face
    top_face_indices = []
    for i, point in enumerate(points):
        # Check if point is on the smallest circle of the top face (with tolerance)
        if abs(np.sqrt((point[0] - top_center[0])**2 + (point[1] - top_center[1])**2) - inner_radius) < 0.1:
            top_face_indices.append(i)
    
    # We should have exactly 12 points
    if len(top_face_indices) != 12:
        print(f"Warning: Expected 12 points on inner circle, found {len(top_face_indices)}")
    
    # Group points into 4 sets of 3 (for each "edge" of the face)
    # We'll identify points by their relative positions to each other
    
    # Step 1: Find the center of each group (these are "edges")
    # We can identify these by checking their distances to other points
    
    # First, calculate distances between all points in the top face
    distances = {}
    for i, idx1 in enumerate(top_face_indices):
        for j, idx2 in enumerate(top_face_indices[i+1:], i+1):
            p1 = points[idx1]
            p2 = points[idx2]
            dist = np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
            distances[(idx1, idx2)] = dist
    
    # Group points by proximity
    groups = [[] for _ in range(4)]
    assigned = set()
    
    # Find a starting point
    start_idx = top_face_indices[0]
    groups[0].append(start_idx)
    assigned.add(start_idx)
    
    # Find two closest points to the starting point
    closest_to_start = sorted([(idx2, distances[(start_idx, idx2)]) 
                              if (start_idx, idx2) in distances 
                              else (idx2, distances[(idx2, start_idx)]) 
                              for idx2 in top_face_indices if idx2 != start_idx], 
                             key=lambda x: x[1])
    
    for idx, _ in closest_to_start[:2]:
        groups[0].append(idx)
        assigned.add(idx)
    
    # Find next group starting point (furthest from previous group center)
    prev_center = np.mean([points[idx] for idx in groups[0]], axis=0)
    
    for g in range(1, 4):
        # Find point furthest from previous center
        remaining = [idx for idx in top_face_indices if idx not in assigned]
        if not remaining:
            break
            
        next_start = max(remaining, 
                         key=lambda idx: np.sqrt((points[idx][0] - prev_center[0])**2 + 
                                                (points[idx][1] - prev_center[1])**2))
        
        groups[g].append(next_start)
        assigned.add(next_start)
        
        # Find two closest points to this new start
        closest = sorted([(idx2, np.sqrt((points[next_start][0] - points[idx2][0])**2 + 
                                         (points[next_start][1] - points[idx2][1])**2))
                          for idx2 in top_face_indices if idx2 != next_start and idx2 not in assigned], 
                         key=lambda x: x[1])
        
        for idx, _ in closest[:2]:
            groups[g].append(idx)
            assigned.add(idx)
        
        prev_center = np.mean([points[idx] for idx in groups[g]], axis=0)
    
    # Ensure groups are in clockwise/counterclockwise order
    # Calculate angle of each group's center relative to the top center
    group_centers = [np.mean([points[idx] for idx in group], axis=0) for group in groups]
    group_angles = [np.arctan2(center[1] - top_center[1], center[0] - top_center[0]) for center in group_centers]
    
    # Sort groups by angle
    sorted_indices = np.argsort(group_angles)
    groups = [groups[i] for i in sorted_indices]
    
    # Now perform the rotation
    new_colors = colors.copy()
    
    if direction == 'ccw':
        # Rotate groups clockwise (3->0, 0->1, 1->2, 2->3)
        shifted_groups = [groups[3], groups[0], groups[1], groups[2]]
    else:  # ccw
        # Rotate groups counterclockwise (1->0, 2->1, 3->2, 0->3)
        shifted_groups = [groups[1], groups[2], groups[3], groups[0]]
    
    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]
    
    return points, new_colors

def rotate_right_face(points, colors, direction='ccw'):
    """
    Perform a rotation of the RIGHT (R) face by rotating colors at the 12 intersection points.    
    :param points: List of intersection points
    :param colors: List of colors for the points (current state)
    :param direction: 'cw' for clockwise, 'ccw' for counterclockwise
    :return: Tuple of points and updated colors
    """
    # Right center (bottom right in the diagram)
    right_center = centers[2]  # Bottom right
    inner_radius = circle_radii[0]
    
    # Find indices of points on the inner circle of the right face
    right_face_indices = []
    for i, point in enumerate(points):
        # Check if point is on the smallest circle of the right face (with tolerance)
        if abs(np.sqrt((point[0] - right_center[0])**2 + (point[1] - right_center[1])**2) - inner_radius) < 0.1:
            right_face_indices.append(i)
    
    # We should have exactly 12 points
    if len(right_face_indices) != 12:
        print(f"Warning: Expected 12 points on inner circle of right face, found {len(right_face_indices)}")
    
    # Enhanced grouping for right face - grouping points based on proximity and position
    # Calculate the angle of each point relative to the right center
    point_angles = [(i, np.arctan2(points[i][1] - right_center[1], 
                                    points[i][0] - right_center[0])) 
                    for i in right_face_indices]
    
    # Sort points by angle to get them in order around the circle
    point_angles.sort(key=lambda x: x[1])
    sorted_indices = [idx for idx, _ in point_angles]
    
    # Group into 4 sets of 3 points (each "edge" of the face)
    groups = [sorted_indices[i:i+3] for i in range(0, 12, 3)]
    
    # Now perform the rotation
    new_colors = colors.copy()
    
    if direction == 'ccw':
        # For right face, we want to rotate counterclockwise when viewed from right side
        shifted_groups = [groups[1], groups[2], groups[3], groups[0]]
    else:  # cw
        # For right face, we want to rotate clockwise when viewed from right side
        shifted_groups = [groups[3], groups[0], groups[1], groups[2]]
    
    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]
    
    return points, new_colors


def rotate_front_face(points, colors, direction='ccw'):
    """
    Perform a rotation of the FRONT (F) face by rotating colors at the 12 intersection points.    
    :param points: List of intersection points
    :param colors: List of colors for the points (current state)
    :param direction: 'cw' for clockwise, 'ccw' for counterclockwise
    :return: Tuple of points and updated colors
    """
    # Front center (bottom left in the diagram)
    front_center = centers[1]  # Bottom left
    inner_radius = circle_radii[0]
    
    # Find indices of points on the inner circle of the left face
    front_face_indices = []
    for i, point in enumerate(points):
        # Check if point is on the smallest circle of the front face (with tolerance)
        if abs(np.sqrt((point[0] - front_center[0])**2 + (point[1] - front_center[1])**2) - inner_radius) < 0.1:
            front_face_indices.append(i)
    
    # We should have exactly 12 points
    if len(front_face_indices) != 12:
        print(f"Warning: Expected 12 points on inner circle of left face, found {len(front_face_indices)}")
    
    # Group points into 4 sets of 3 (for each "edge" of the face)
    # First, calculate distances between all points in the front face
    distances = {}
    for i, idx1 in enumerate(front_face_indices):
        for j, idx2 in enumerate(front_face_indices[i+1:], i+1):
            p1 = points[idx1]
            p2 = points[idx2]
            dist = np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
            distances[(idx1, idx2)] = dist
    
    # Group points by proximity
    groups = [[] for _ in range(4)]
    assigned = set()
    
    # Find a starting point
    start_idx = front_face_indices[0]
    groups[0].append(start_idx)
    assigned.add(start_idx)
    
    # Find two closest points to the starting point
    closest_to_start = sorted([(idx2, distances[(start_idx, idx2)]) 
                              if (start_idx, idx2) in distances 
                              else (idx2, distances[(idx2, start_idx)]) 
                              for idx2 in front_face_indices if idx2 != start_idx], 
                             key=lambda x: x[1])
    
    for idx, _ in closest_to_start[:2]:
        groups[0].append(idx)
        assigned.add(idx)
    
    # Find next group starting point (furthest from previous group center)
    prev_center = np.mean([points[idx] for idx in groups[0]], axis=0)
    
    for g in range(1, 4):
        # Find point furthest from previous center
        remaining = [idx for idx in front_face_indices if idx not in assigned]
        if not remaining:
            break
            
        next_start = max(remaining, 
                         key=lambda idx: np.sqrt((points[idx][0] - prev_center[0])**2 + 
                                                (points[idx][1] - prev_center[1])**2))
        
        groups[g].append(next_start)
        assigned.add(next_start)
        
        # Find two closest points to this new start
        closest = sorted([(idx2, np.sqrt((points[next_start][0] - points[idx2][0])**2 + 
                                         (points[next_start][1] - points[idx2][1])**2))
                          for idx2 in front_face_indices if idx2 != next_start and idx2 not in assigned], 
                         key=lambda x: x[1])
        
        for idx, _ in closest[:2]:
            groups[g].append(idx)
            assigned.add(idx)
        
        prev_center = np.mean([points[idx] for idx in groups[g]], axis=0)
    
    # Ensure groups are in clockwise/counterclockwise order
    # Calculate angle of each group's center relative to the left center
    group_centers = [np.mean([points[idx] for idx in group], axis=0) for group in groups]
    group_angles = [np.arctan2(center[1] - front_center[1], center[0] - front_center[0]) for center in group_centers]
    
    # Sort groups by angle
    sorted_indices = np.argsort(group_angles)
    groups = [groups[i] for i in sorted_indices]
    
    # Now perform the rotation
    new_colors = colors.copy()
    
    if direction == 'ccw':
        # Rotate groups clockwise (3->0, 0->1, 1->2, 2->3)
        shifted_groups = [groups[3], groups[0], groups[1], groups[2]]
    else:  # ccw
        # Rotate groups counterclockwise (1->0, 2->1, 3->2, 0->3)
        shifted_groups = [groups[1], groups[2], groups[3], groups[0]]
    
    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]
    
    return points, new_colors

def rotate_left_face(points, colors, direction='ccw'):
    """
    Perform a rotation of the LEFT (L) face by rotating colors at the 12 intersection points.    
    :param points: List of intersection points
    :param colors: List of colors for the points (current state)
    :param direction: 'cw' for clockwise, 'ccw' for counterclockwise
    :return: Tuple of points and updated colors
    """
    # Left center (in the diagram, this is actually the top center)
    left_center = centers[2]  # Top center
    outer_radius = circle_radii[2]

    # Find indices of points on the inner circle of the left face
    left_face_indices = []
    for i, point in enumerate(points):
        # Check if point is on the smallest circle of the left face (with tolerance)
        if abs(np.sqrt((point[0] - left_center[0])**2 + (point[1] - left_center[1])**2) - outer_radius) < 0.1:
            left_face_indices.append(i)

    # We should have exactly 12 points
    if len(left_face_indices) != 12:
        print(f"Warning: Expected 12 points on inner circle of left face, found {len(left_face_indices)}")

    # Enhanced grouping for left face - grouping points based on angular position
    # Calculate the angle of each point relative to the left center
    point_angles = [(i, np.arctan2(points[i][1] - left_center[1], 
                                   points[i][0] - left_center[0])) 
                   for i in left_face_indices]

    # Sort points by angle to get them in order around the circle
    point_angles.sort(key=lambda x: x[1])
    sorted_indices = [idx for idx, _ in point_angles]

    # Group into 4 sets of 3 points (each "edge" of the face)
    groups = [sorted_indices[i:i+3] for i in range(0, 12, 3)]

    # Now perform the rotation
    new_colors = colors.copy()

    # Left face is viewed from the left side, so the rotation directions are inverted
    # compared to how they appear in the diagram
    if direction == 'ccw':
        # For left face, we want to rotate counterclockwise when viewed from left side
        shifted_groups = [groups[1], groups[2], groups[3], groups[0]]
    else:  # cw
        # For left face, we want to rotate clockwise when viewed from left side
        shifted_groups = [groups[3], groups[0], groups[1], groups[2]]

    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]

    return points, new_colors

def rotate_down_face(points, colors, direction='ccw'):
    """
    Perform a rotation of the DOWN (D) face by rotating colors at the 12 intersection points.    
    :param points: List of intersection points
    :param colors: List of colors for the points (current state)
    :param direction: 'cw' for clockwise, 'ccw' for counterclockwise
    :return: Tuple of points and updated colors
    """
    # Left center (in the diagram, this is actually the top center)
    bottom_center = centers[0]  # Top center
    outer_radius = circle_radii[2]

    # Find indices of points on the inner circle of the left face
    bottom_face_indices = []
    for i, point in enumerate(points):
        # Check if point is on the smallest circle of the left face (with tolerance)
        if abs(np.sqrt((point[0] -bottom_center[0])**2 + (point[1] - bottom_center[1])**2) - outer_radius) < 0.1:
            bottom_face_indices.append(i)

    # We should have exactly 12 points
    if len(bottom_face_indices) != 12:
        print(f"Warning: Expected 12 points on inner circle of bottom face, found {len(bottom_face_indices)}")

    # Enhanced grouping for left face - grouping points based on angular position
    # Calculate the angle of each point relative to the left center
    point_angles = [(i, np.arctan2(points[i][1] - bottom_center[1], 
                                   points[i][0] - bottom_center[0])) 
                   for i in bottom_face_indices]

    # Sort points by angle to get them in order around the circle
    point_angles.sort(key=lambda x: x[1])
    sorted_indices = [idx for idx, _ in point_angles]

    # Group into 4 sets of 3 points (each "edge" of the face)
    groups = [sorted_indices[i:i+3] for i in range(0, 12, 3)]

    # Now perform the rotation
    new_colors = colors.copy()

    # Left face is viewed from the left side, so the rotation directions are inverted
    # compared to how they appear in the diagram
    if direction == 'ccw':
        # For left face, we want to rotate counterclockwise when viewed from left side
        shifted_groups = [groups[1], groups[2], groups[3], groups[0]]
    else:  # cw
        # For left face, we want to rotate clockwise when viewed from left side
        shifted_groups = [groups[3], groups[0], groups[1], groups[2]]

    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]

    return points, new_colors

def rotate_back_face(points, colors, direction='ccw'):
    """
    Perform a rotation of the LEFT (L) face by rotating colors at the 12 intersection points.    
    :param points: List of intersection points
    :param colors: List of colors for the points (current state)
    :param direction: 'cw' for clockwise, 'ccw' for counterclockwise
    :return: Tuple of points and updated colors
    """
    # Left center (in the diagram, this is actually the top center)
    back_center = centers[1]  # Top center
    outer_radius = circle_radii[2]

    # Find indices of points on the inner circle of the left face
    back_face_indices = []
    for i, point in enumerate(points):
        # Check if point is on the smallest circle of the left face (with tolerance)
        if abs(np.sqrt((point[0] -back_center[0])**2 + (point[1] - back_center[1])**2) - outer_radius) < 0.1:
            back_face_indices.append(i)

    # We should have exactly 12 points
    if len(back_face_indices) != 12:
        print(f"Warning: Expected 12 points on inner circle of back face, found {len(back_face_indices)}")

    # Enhanced grouping for left face - grouping points based on angular position
    # Calculate the angle of each point relative to the left center
    point_angles = [(i, np.arctan2(points[i][1] - back_center[1], 
                                   points[i][0] - back_center[0])) 
                   for i in back_face_indices]

    # Sort points by angle to get them in order around the circle
    point_angles.sort(key=lambda x: x[1])
    sorted_indices = [idx for idx, _ in point_angles]

    # Group into 4 sets of 3 points (each "edge" of the face)
    groups = [sorted_indices[i:i+3] for i in range(0, 12, 3)]

    # Now perform the rotation
    new_colors = colors.copy()

    # Left face is viewed from the left side, so the rotation directions are inverted
    # compared to how they appear in the diagram
    if direction == 'ccw':
        # For left face, we want to rotate counterclockwise when viewed from left side
        shifted_groups = [groups[1], groups[2], groups[3], groups[0]]
    else:  # cw
        # For left face, we want to rotate clockwise when viewed from left side
        shifted_groups = [groups[3], groups[0], groups[1], groups[2]]

    # Apply the rotation by moving colors between groups
    for i, (orig_group, new_group) in enumerate(zip(groups, shifted_groups)):
        for j in range(len(orig_group)):
            new_colors[orig_group[j]] = colors[new_group[j]]

    return points, new_colors

# Enhanced function to perform multiple successive moves
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
    current_points = points.copy()
    current_colors = colors.copy()
    
    for face, direction in moves:
        if face == 'U':
            current_points, current_colors = rotate_up_face(current_points, current_colors, direction)
        elif face == 'F':
            current_points, current_colors = rotate_front_face(current_points, current_colors, direction)
        elif face == 'R':
            current_points, current_colors = rotate_right_face(current_points, current_colors, direction)
        elif face == 'L':
            current_points, current_colors = rotate_left_face(current_points, current_colors, direction)
        elif face == 'D':
            current_points, current_colors = rotate_down_face(current_points, current_colors, direction)
        elif face == 'B':
            current_points, current_colors = rotate_back_face(current_points, current_colors, direction)

    return current_points, current_colors

# Test with multiple moves on different faces
initial_points, initial_colors = generate_initial_points()
# Visualize initial state
create_rubiks_diagram(initial_points, initial_colors)

# Test Right face clockwise
points_after_url, colors_after_url = perform_moves(
    initial_points, initial_colors, 
    [('R', 'cw')]*4
    )    
create_rubiks_diagram(points_after_url, colors_after_url)

create_rubiks_diagram(initial_points, initial_colors)
points_after, colors_after = rotate_left_face(initial_points, initial_colors, 'cw')
create_rubiks_diagram(points_after, colors_after)
