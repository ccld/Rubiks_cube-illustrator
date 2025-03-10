#!/usr/bin/env python
"""
Script that allows for face rotations

The rotation follows the color progression:
Clockwise: white → green → yellow → blue → white
Counterclockwise: white → blue → yellow → green → white


"""

# =====================================================================
# function to handle UP face rotation
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

# -------------------------------------------------------------------
# function to handle RIGHT face rotation
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
    
    if direction == 'cw':
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

# -------------------------------------------------------------------
# function to handle FRONT face rotation
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

# -------------------------------------------------------------------
# function to handle LEFT face rotation
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

# -------------------------------------------------------------------
# function to handle DOWN face rotation
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

# -------------------------------------------------------------------
# function to handle BACK face rotation
def rotate_back_face(points, colors, direction='ccw'):
    """
    Perform a rotation of the BACK (B) face by rotating colors at the 12 intersection points.    
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

# =====================================================================
