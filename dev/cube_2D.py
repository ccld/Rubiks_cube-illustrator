# -*- coding: utf-8 -*-
"""

"""
import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt
from matplotlib.patches import Circle


class MagicCube:
    def __init__(self):
        self.cube = self._initialize_cube()
        
    def _initialize_cube(self):
        """Create a valid magic cube with all centers filled"""
        cube = np.empty((6, 3, 3), dtype=object)
        # Up face
        cube[0] = [['2', '7', '6'],
                  ['9', '5', '1'],
                  ['4', '3', '8']]
        # Down face
        cube[1] =[['51', '52', '47'],
                  ['46', '50', '54'],
                  ['53', '48', '49']]   
        # Front face
        cube[2] = [['26', '21', '22'],
                  ['19', '23', '27'],
                  ['24', '25', '20']]
        # Back face
        cube[3] = [['33', '34', '29'],
                  ['28', '32', '36'],
                  ['35', '30', '31']]
        # Left face
        cube[4] = [['44', '37', '42'],
                  ['39', '41', '43'],
                  ['40', '45', '38']]
        # Right face
        cube[5] = [['13', '18', '11'],
                  ['12', '14', '16'],
                  ['17', '10', '15']]
       
        return cube

    def rotate(self, face):
        """Rotate a face clockwise with full edge handling"""
        face_map = {
            'U': (0, self._rotate_up),
            #'D': (1, self._rotate_down),
            'F': (2, self._rotate_front),
            #'B': (3, self._rotate_back),
            #'L': (4, self._rotate_left),
            #'R': (5, self._rotate_right)
        }
        
        if face not in face_map:
            raise ValueError(f"Invalid face: {face}. Use U/D/F/B/L/R")
            
        face_idx, rot_func = face_map[face]
        self.cube = rot_func(self.cube, face_idx)
        
        
    def _rotate_up(self, cube, face_idx):
        """Rotate up face and adjacent edges"""
        new_cube = deepcopy(cube)
        new_cube[face_idx] = np.rot90(cube[face_idx], -1)
        
        # Save edges
        front_edge = cube[2, 0, :].copy()
        left_edge = cube[4, 0, :].copy()
        back_edge = cube[3, 0, :].copy()
        right_edge = cube[5, 0, :].copy()
        
        # Rotate edges
        new_cube[4, 0, :] = front_edge
        new_cube[3, 0, :] = left_edge
        new_cube[5, 0, :] = back_edge
        new_cube[2, 0, :] = right_edge
        
        return new_cube

    
    def _rotate_front(self, cube, face_idx):
        """Rotate front face and adjacent edges"""
        new_cube = deepcopy(cube)
        
        # Rotate the face
        new_cube[face_idx] = np.rot90(cube[face_idx], -1)
        
        # Save adjacent edges
        up_edge = cube[0, 2, :].copy()     # Up face bottom row
        left_edge = cube[4, :, 2].copy()   # Left face right column
        down_edge = cube[1, 0, :].copy()   # Down face top row
        right_edge = cube[5, :, 0].copy()  # Right face left column
        
        # Perform edge rotation
        new_cube[5, :, 0] = up_edge[::-1]    # Right <- Up (reversed)
        new_cube[1, 0, :] = right_edge       # Down <- Right
        new_cube[4, :, 2] = down_edge        # Left <- Down
        new_cube[0, 2, :] = left_edge[::-1]  # Up <- Left (reversed)
        
        return new_cube

    def rotate_face_clockwise(cube_np, face_idx):
        """Rotate a single face 90° clockwise while maintaining adjacent edges"""
        # Deep copy to avoid reference issues
        new_cube = np.copy(cube_np)
        
        # Rotate the selected face
        face = cube_np[face_idx]
        rotated_face = np.rot90(face, -1)  # -1 for clockwise
        new_cube[face_idx] = rotated_face
        
        # Handle adjacent edges (this varies by face)
        if face_idx == 2:  # Front face rotation
            # Save affected edges
            top_row = cube_np[0, 2, :].copy()     # Up face bottom row
            left_col = cube_np[4, :, 2].copy()    # Left face right column
            bottom_row = cube_np[1, 0, :].copy()  # Down face top row
            right_col = cube_np[5, :, 0].copy()   # Right face left column
            
            # Perform edge rotation
            new_cube[5, :, 0] = top_row[::-1]     # Right <- Up (reversed)
            new_cube[1, 0, :] = right_col          # Down <- Right
            new_cube[4, :, 2] = bottom_row         # Left <- Down
            new_cube[0, 2, :] = left_col[::-1]     # Up <- Left (reversed)
        
        elif face_idx == 0:  # Up face rotation
            # Similar logic for other faces...
            pass
        
        return new_cube
    
    
    def _rotate_edges(self, cube, adj_faces, clockwise):
        """Rotate the edges around a face"""
        temp = cube[adj_faces['up']].copy()
        if clockwise:
            cube[adj_faces['up']] = cube[adj_faces['left']][::-1]
            cube[adj_faces['left']] = cube[adj_faces['down']]
            cube[adj_faces['down']] = cube[adj_faces['right']][::-1]
            cube[adj_faces['right']] = temp
        else:
            # Counter-clockwise rotation
            cube[adj_faces['up']] = cube[adj_faces['right']]
            cube[adj_faces['right']] = cube[adj_faces['down']][::-1]
            cube[adj_faces['down']] = cube[adj_faces['left']]
            cube[adj_faces['left']] = temp[::-1]

    
    
    def rotate_cube_x(cube_np):
        """Rotate entire cube around X-axis (front-back axis)"""
        # Cycle Up -> Front -> Down -> Back while rotating faces
        new_cube = np.copy(cube_np)
        new_cube[0] = np.rot90(cube_np[2], 2)  # Up becomes inverted Front
        new_cube[1] = np.rot90(cube_np[3], 2)  # Down becomes inverted Back
        new_cube[2] = cube_np[1]               # Front becomes Down
        new_cube[3] = cube_np[0]               # Back becomes Up
        # Left/Right need rotation too
        new_cube[4] = np.rot90(cube_np[4], -1)
        new_cube[5] = np.rot90(cube_np[5], 1)
        return new_cube
        
def display_cube_safe(cube_np):
    fig, axs = plt.subplots(3, 4, figsize=(9, 9), layout='constrained')
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

    faces = {
        (0,1): ('Up', 0),
        (1,0): ('Left', 4),
        (1,1): ('Front', 2),
        (1,2): ('Right', 5),
        (1,3): ('Back', 3),
        (2,1): ('Down', 1)
        }
    
    for (row,col), (label, idx) in faces.items():
        ax = axs[row, col]
        face = cube_np[idx]

        try:
            center_val = int(face[1,1]) if face[1,1] is not None else '?'
            for i in range(3):
                for j in range(3):
                    val = face[i,j] if face[i,j] is not None else '?'
                    ax.add_patch(plt.Rectangle((j, 2.3-i), 1, 1, 
                                             facecolor='yellow' if i == 1 and j ==1 else 'white',
                                             edgecolor='black'))
                    ax.text(j+0.5, 2.3-i+0.5, str(val), 
                           ha='center', va='center', fontsize = 16, fontweight = 'bold')
            
            ax.set_title(f"{label}\nCenter: {center_val}")
            ax.set_xlim(-0.5,3.5)
            ax.set_ylim(-1,4)
            #ax.axis('off')
            #ax.yaxis.set_visible(False)
            #ax.xaxis.set_visible(False) 
            
        except Exception as e:
            print(f"Error displaying {label} face: {e}")
            ax.set_title(f"Error in {label}")
            ax.axis('off')
    
    plt.tight_layout() #(pad=1.08) #, h_pad = 1.08) w_pad = 0.4, rect= (1.08, 1.08, 1.08,  1.08))
    plt.savefig("F:/Users/Claude/Downloads/cube_new.png", format='png', bbox_inches='tight', pad_inches=0.0, transparent=True)
    plt.show()
    plt.close()
        
def interactive_demo():
    cube = MagicCube()
    print("Initial Cube:")
    display_cube_safe(cube.cube)
    
    while True:
        cmd = input("Rotate (U/D/F/B/L/R/x/y/z/quit): ").strip().upper()
        if cmd == 'QUIT':
            break
        elif cmd in ['U','D','F','B','L','R','X','Y','Z']:
            cube.rotate(cmd)
            display_cube_safe(cube.cube)
            if not cube.verify_integrity():
                print("Warning: Magic properties violated!")
        else:
            print("Invalid command")        
            
# Initialize and display
cube = MagicCube()
print("Initial Cube:")
display_cube_safe(cube.cube)  # Use your display function

'''
# Rotate front face
cube.rotate('F')
print("\nAfter Front rotation:")
display_cube_safe(cube.cube)

# Rotate up face
cube.rotate('U')
print("\nAfter Up rotation:")
display_cube_safe(cube.cube)
'''