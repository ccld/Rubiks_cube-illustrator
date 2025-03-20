# -*- coding: utf-8 -*-
#!/usr/bin/env python
# ==================================================================================

import numpy as np

# ==================================================================================

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
        
