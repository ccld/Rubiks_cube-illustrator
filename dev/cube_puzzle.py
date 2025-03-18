# -*- coding: utf-8 -*-
# =====================================================================
"""
Rubik's Cube Venn Diagram Move Simulation
"""
# =====================================================================
 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
 
# import structure
# =====================================================================

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

width = 638
height = 638
fps = 1
directory= "C://Users//HP//Downloads//"

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

def create_rubiks_diagram(points, colors, frame_number, subtext):
    """Create the Rubik's Cube Venn diagram."""
    plt.figure(figsize=(6.38, 6.38), dpi = 100)
    ax = plt.subplot(111, aspect='equal')
    
    # Draw concentric circles
    for center in centers:
        for radius in circle_radii:
            circle = Circle(center, radius, fill=False, color='gray', linestyle='-', linewidth=1)
            ax.add_patch(circle)
    
    # Draw the intersection points as colored nodes
    for point, color in zip(points, colors):
        plt.plot(point[0], point[1], 'o', markersize=15, markerfacecolor=face_colors[color], markeredgecolor='black')
        
    ax.text(-4., -5., subtext)
    # Set plot limits and remove axes
    plt.xlim(-5.5, 5.5)
    plt.ylim(-5.5, 5.5)
    plt.axis('off')
    plt.title("Rubik's Cube Venn Representation", fontsize=14)
    plt.tight_layout()
    # Save the figure to a file instead of displaying it
    filename = f'circle_frame_{frame_number:03d}.png'
    plt.savefig(filename, dpi=100)
    plt.show()
    plt.close()  # Close the figure to free memory
    
    return filename
    


def create_animation(turns, output_filename='rubiks_animation.avi', fps=1):
    # Create temporary directory for frames
    frames = []
    # Generate each frame
    n = -1 
    for x in turns:
        n = n +1
        k = turns.index(turns[n]) 
        if n == 0 :
                print(k , turns[k], n)  
                subtitle = 'Set #'+ str(n) + '  for algorithm x'
                filename = create_rubiks_diagram(initial_points, initial_colors, subtitle)
                frames.append(filename)  
                points_after, colors_after = perform_moves(
                    initial_points, initial_colors, 
                    [(turns[k])])
                subtitle = 'Set #'+ str(n+1) + '  after rotating '+ turns[1][0] + turns[1][1]
                filename = create_rubiks_diagram(points_after, colors_after, 1)
                frames.append(filename)  

        else :
            print( k, turns[k], n)
            points_after, colors_after  = perform_moves(
                                points_after, colors_after,
                                [(turns[k])])                     
            subtitle = 'Set #'+ str(n+1) + '  after rotating '+ turns[n][0] + turns[n][1]                    
            filename = create_rubiks_diagram(points_after, colors_after, n+1)
            frames.append(filename)  
# =====================================================================  
''' 
    import cv2
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter('output_name.avi', fourcc, float(fps), (width, height))
    for filename in frames:
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        video.write(img)   
        
    # Create GIF from frames
    with imageio.get_writer('output_name.gif', mode='I', fps=1) as writer:
        for filename in frames:
            image = imageio.imread(filename)
            writer.append_data(image)
    
    # Optional: Clean up temporary files
    for filename in frames:
        os.remove(filename)
'''
# =====================================================================
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
    #print(intersections)
    return  intersections, colors # 

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


# =====================================================================
# Test with multiple moves on different faces
initial_points, initial_colors = generate_initial_points()
# Visualize initial state
create_rubiks_diagram(initial_points, initial_colors,0,'start')

# Test faces 4 clockwise
points_after_url, colors_after_url = perform_moves(
    initial_points, initial_colors, 
    [('U', 'cw'),
     ('U', 'cw'),
     ('D', 'cw'),
     ('D', 'cw'),
     ('L', 'cw'),
     ('L', 'cw'),
     ('R', 'cw'),
     ('R', 'cw'),
     ('F', 'cw'),
     ('F', 'cw'),
     ('B', 'cw'),
     ('B', 'cw')]
    )
 
create_rubiks_diagram(points_after_url, colors_after_url, 0, 'checkerboard')

# =====================================================================
