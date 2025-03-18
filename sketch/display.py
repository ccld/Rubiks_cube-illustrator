import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
