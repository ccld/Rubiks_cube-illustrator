import numpy as np

def initialize_cube(orientation_code='02'):
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
    cube = np.zeros((6, 3, 3), dtype=int)
    
    if orientation_code is None:
        # Default orientation: each face index equals its color
        for i in range(6):
            cube[i, :, :] = i
    else:
        # Custom orientation based on orientation_code
        # Parse the orientation code
        up_color = int(orientation_code[0])
        front_color = int(orientation_code[1])
        
        # Validate the input colors
        if up_color == front_color or not (0 <= up_color < 6 and 0 <= front_color < 6):
            raise ValueError("Invalid orientation code. Colors must be different and between 0-5.")
        
        # Determine the remaining faces based on standard Rubik's cube structure
        # The opposite of UP is DOWN, opposite of FRONT is BACK, etc.
        down_color = get_opposite_color(up_color)
        back_color = get_opposite_color(front_color)
        
        # Determine LEFT and RIGHT colors
        # This is a bit complex due to Rubik's cube constraints
        remaining_colors = set(range(6)) - {up_color, down_color, front_color, back_color}
        remaining_colors = list(remaining_colors)
        
        # In a standard Rubik's cube, if UP is white (0) and FRONT is green (2),
        # then LEFT would be orange (4) and RIGHT would be red (5)
        # We need to determine the correct positions based on the specified UP and FRONT
        if (up_color, front_color) in [(0, 2), (2, 1), (1, 3), (3, 0)]:
            left_color, right_color = remaining_colors
        else:
            right_color, left_color = remaining_colors
        
        # Assign colors to faces
        face_colors = [up_color, down_color, front_color, back_color, left_color, right_color]
        print(face_colors[:])
        for i in range(6):
            cube[i, :, :] = face_colors[i]
    
    return cube , face_colors

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

#orientation ='42'
#initialize_cube(orientation)
