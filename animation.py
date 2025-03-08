import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import imageio.v2 as imageio
import os
import numpy as np

def create_diagram(center, radius, frame_number):
    # Create figure
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, aspect='equal')
    
    # Draw circle
    circle = Circle(center, radius, fill=False, color='blue', linestyle='-', linewidth=2)
    ax.add_patch(circle)
    
    # Set plot limits and remove axes
    plt.xlim(-5.5, 5.5)
    plt.ylim(-5.5, 5.5)
    plt.axis('off')
    plt.title(f"Circle with radius {radius}", fontsize=14)
    plt.tight_layout()
    
    # Save the figure to a file instead of displaying it
    filename = f'circle_frame_{frame_number:03d}.png'
    plt.savefig(filename, dpi=100)
    plt.close()  # Close the figure to free memory
    
    return filename

def create_animation(radii, output_filename='circle_animation.gif', fps=2):
    # Create temporary directory for frames
    frames = []
    
    # Generate each frame
    for i, radius in enumerate(radii):
        filename = create_diagram((0, 0), radius, i)
        frames.append(filename)
    
    # Create GIF from frames
    with imageio.get_writer(output_filename, mode='I', duration=1000/fps) as writer:
        for filename in frames:
            image = imageio.imread(filename)
            writer.append_data(image)
    
    # Optional: Clean up temporary files
    for filename in frames:
        os.remove(filename)
    
    print(f"Animation saved as {output_filename}")

# Example usage:
# Simple increasing radius
radii = [1, 2, 3, 4]
create_animation(radii, 'circle_growing.gif', fps=1)

# More frames for smoother animation
smooth_radii = np.linspace(0.5, 4, 20)
create_animation(smooth_radii, 'smooth_circle_growing.gif', fps=10)

# Create pulsing animation
pulsing_radii = np.concatenate([np.linspace(0.5, 4, 15), np.linspace(4, 0.5, 15)])
create_animation(pulsing_radii, 'pulsing_circle.gif', fps=15)
