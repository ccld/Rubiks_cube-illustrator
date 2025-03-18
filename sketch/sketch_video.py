import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sketch.display import display_cube, get_color_map
from structure.moves import execute_move

def create_frame(cube, fig):
    """Create a single frame for the animation."""
    # Clear the figure
    fig.clf()
    
    # Create axes with the same layout as display_cube
    axs = fig.subplots(3, 4)
    
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
    color_map = get_color_map()
    faces = {
        (0, 1): 0,  # Up
        (1, 1): 2,  # Front
        (1, 0): 4,  # Left
        (1, 2): 5,  # Right
        (1, 3): 3,  # Back
        (2, 1): 1   # Down
    }
    
    for (row, col), face_idx in faces.items():
        ax = axs[row, col]
        face = cube[face_idx]
        
        # Draw a grid of colored squares
        for i in range(3):
            for j in range(3):
                color_idx = face[i, j]
                color = color_map.get(color_idx, (0.5, 0.5, 0.5))
                ax.add_patch(plt.Rectangle((j, 2-i), 1, 1, facecolor=color, edgecolor='black'))
        
        # Set limits
        ax.set_xlim(