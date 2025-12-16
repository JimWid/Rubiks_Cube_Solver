def display_cube(cube_state):
    # Mapping from color names to single characters
    color_to_char = {
        'white': 'w',
        'red': 'r',
        'green': 'g',
        'blue': 'b',
        'orange': 'o',
        'yellow': 'y'
    }
    
    # Helper function to convert a face's list of 9 colors to three rows
    def get_face_rows(face):
        chars = [color_to_char[c] for c in cube_state[face]]
        return [' '.join(chars[i:i+3]) for i in range(0, 9, 3)]
    
    # Get rows for each face
    U_rows = get_face_rows('U')
    L_rows = get_face_rows('L')
    F_rows = get_face_rows('F')
    R_rows = get_face_rows('R')
    B_rows = get_face_rows('B')
    D_rows = get_face_rows('D')
    
    # Print Up face
    for row in U_rows:
        print("       ", row)
    
    # Print middle section: Left, Front, Right, Back
    for i in range(3):
        middle_row = ' | '.join([L_rows[i], F_rows[i], R_rows[i], B_rows[i]])
        print(middle_row)
    
    # Print Down face
    for row in D_rows:
        print("       ", row)


