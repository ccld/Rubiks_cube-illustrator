# -*- coding: utf-8 -*-
#!/usr/bin/env python
# =====================================================================
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D
import cv2

from structure import *
# =====================================================================

def get_color_map():
    """Return a mapping of color indices to RGB values."""
    return {
        0: (1.0, 1.0, 1.0),  # White
        1: (1.0, 1.0, 0.0),  # Yellow
        2: (0.0, 1.0, 0.0),  # Green
        3: (0.0, 0.0, 1.0),  # Blue
        4: (1.0, 0.5, 0.0),  # Orange
        5: (1.0, 0.0, 0.0)   # Red
    }

def display_cube(cube, orientation_code=None):
    """
    Display a 2D representation of the cube state.
    
    Args:
        cube (np.ndarray): The cube state
        orientation_code (str, optional): The orientation code used to initialize the cube
    """
    # Color map for display
    color_map = get_color_map()
    
    # Create a figure with a grid layout
    fig, axs = plt.subplots(3, 4, figsize=(8, 6))
    
    # Remove axes and set aspect ratio
    for ax in axs.flat:
        ax.set_aspect('equal')
        ax.axis('off')
    
    # Hide unused subplots
    axs[0, 0].set_visible(False)
    axs[0, 2].set_visible(False)
    axs[0, 3].set_visible(False)
    axs[2, 0].set_visible(False)
    axs[2, 2].set_visible(False)
    axs[2, 3].set_visible(False)
    
    # Display each face
    faces = {
        (0, 1): 0,  # Up
        (1, 1): 2,  # Front
        (1, 0): 4,  # Left
        (1, 2): 5,  # Right
        (1, 3): 3,  # Back
        (2, 1): 1   # Down
    }
    
    # Get face labels
    face_labels = ["Up", "Down", "Front", "Back", "Left", "Right"]
    
    # Add orientation info to title if provided
    if orientation_code:
        up_color = get_color_name(int(orientation_code[0]))
        front_color = get_color_name(int(orientation_code[1]))
        plt.suptitle(f"Cube Orientation: {orientation_code} ({up_color} UP, {front_color} FRONT)")
    
    for (row, col), face_idx in faces.items():
        ax = axs[row, col]
        face = cube[face_idx]
        
        # Draw a grid of colored squares
        for i in range(3):
            for j in range(3):
                color_idx = face[i, j]
                color = color_map.get(color_idx, (0.5, 0.5, 0.5))  # Default to gray
                ax.add_patch(plt.Rectangle((j, 2-i), 1, 1, facecolor=color, edgecolor='black'))
        
        # Set limits
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        
        # Add face label
        ax.text(1.5, -0.5, face_labels[face_idx], ha='center')
    
    plt.tight_layout()
    plt.show()

def display_cube_state(cube, title=None, orientation_code=None):
    """Display the cube with an optional title and orientation code."""
    if title:
        plt.figure(figsize=(8, 6))
        plt.suptitle(title)
    
    display_cube(cube, orientation_code)

def get_color_name(color_index):
    """Convert color index to its name."""
    colors = {
        0: "White",
        1: "Yellow",
        2: "Green",
        3: "Blue",
        4: "Orange",
        5: "Red"
    }
    return colors.get(color_index, "Unknown")

def create_rubiks_diagram(points, colors, frame_number, subtext):
    r = np.sqrt(3)/6  
    centers = []
        # Top center
        # Bottom left
        # Bottom right       
    centers = [(0,2.5),(-2,-2*r),(2,-2*r)]
    # Circle radii
    circle_radii = [2.4, 2.8, 3.2]
    face_colors = {
    'orange': '#FFA500',  # Up (U)
    'red': '#FF0000',     # Down (D)
    'green': '#00FF00',   # Left (L)
    'blue': '#0000FF',    # Right (R)
    'white': '#FFFFFF',   # Front (F)
    'yellow': '#FFFF00'   # Back (B)
        }
    
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
    ax.text(0., -3.6, 'D')
    ax.text(0., 2.3, 'U')
    ax.text(-3.8, 2.3, 'L')
    ax.text(3.6,2.3, 'B')
    ax.text(-1.74, -0.60, 'F')
    ax.text(1.54,-0.60, 'R')
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

def create_animation(fur, moves_list, twists , cleanfile= True):
    subtext = 'turn'
    fps = 1
    # Create temporary directory for frames
    frames = []
    # Generate each frame
    n = -1 
    print('anim', fur)
    cube, face_colors, corner = framesetup.initialize_cube(fur) 
    initial_points, initial_colors = framesetup.generate_initial_points(corner)
    filename = create_rubiks_diagram(initial_points, initial_colors,'', 'Initial solved state')
    for x in moves_list:
        n = n +1
        k = moves_list.index(moves_list[n]) 

        if n == 0 :
                subtitle = 'Set #' + '  for algorithm x' #+ str(n)
                filename = create_rubiks_diagram(initial_points, initial_colors,0, twists + '-')
                frames.append(filename)  
                points_after, colors_after = framesetup.perform_moves(
                    initial_points, initial_colors, 
                    [(moves_list[0])]
                    )
                filename = create_rubiks_diagram(points_after, colors_after, 1, twists + '-')
                frames.append(filename)  
                print('frame ', n)
        else :
            points_after, colors_after  = framesetup.perform_moves(
                                points_after, colors_after,
                                [(moves_list[n])]
                                )                   
            filename = create_rubiks_diagram(points_after, colors_after, str(n+1), twists + '-')
            frames.append(filename)  
            print('frame ', n)
            
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    video = cv2.VideoWriter('filename'+'.mp4', fourcc, float(fps), (638,638))
    for frame in frames:
        img_path = os.path.join(os.getcwd(), frame)
        img = cv2.imread(img_path)
        video.write(img)  
           
    # Optional: Clean up temporary files
    if cleanfile:
        for filename in frames:
            os.remove(filename)

# =====================================================================
