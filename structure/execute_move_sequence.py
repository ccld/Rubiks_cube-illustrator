def execute_move_sequence(points, colors, notation_string):
    """
    Execute a sequence of moves described by a notation string.
    
    :param points: List of intersection points
    :param colors: List of colors for the points
    :param notation_string: String like 'FLRU2Lr'
    :return: Tuple of final points and colors
    """
    moves = parse_move_notation(notation_string)
    return perform_moves(points, colors, moves)

'''
# Example usage:
initial_points, initial_colors = generate_initial_points()
# Execute the move sequence 'FLRU2Lr'
final_points, final_colors = execute_move_sequence(initial_points, initial_colors, 'FLRU2Lr')
create_rubiks_diagram(final_points, final_colors)
'''
