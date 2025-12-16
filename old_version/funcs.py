from collections import Counter

# Color Detection Setup - HSV = HUE, SATURATION, VALUE
HSV_RANGES = {
    'red':    [[0, 130, 100], [8, 255, 255]], # Also covers a bit of the 0-10 range in the get_color_name function
    'orange': [[6, 130, 100], [22, 255, 255]],
    'yellow': [[26, 100, 100], [40, 255, 255]],
    'green':  [[41, 80, 80], [85, 255, 255]],
    'blue':   [[86, 100, 100], [130, 255, 255]],
    'white':  [[0, 0, 160], [131, 60, 255]] # White has low saturation and high value
    }
        
# Cube State Representation Setup: up, right, front, down, left and back
KOCIEMBA_FACE_ORDER = ['U', 'R', 'F', 'D', 'L', 'B']

# Each letter reprents a color, we are using the standar color scheme
COLOR_TO_FACE_MAP = {
    'white':  'U',
    'red':    'R',
    'green':  'F',
    'yellow': 'D',
    'orange': 'L',
    'blue':   'B'
    }

# Utility Functions:
# Getting the name for each color
def get_color_name(h, s, v): # HUE, SATURATION, VALUE

    # Checking for white first, since its HUE can be anything but sarutation is low.
    if HSV_RANGES["white"][0][1] <= s <= HSV_RANGES["white"][1][1] and \
       HSV_RANGES["white"][0][2] <= v <= HSV_RANGES["white"][1][2]:
       return 'white'
        
    # Cheking for Red, which HUE is close to 180 / highest
    if (165 <= h <= 179) and s > 120 and v > 100:
        return "red"
        
    # For Loop to iterate HSV_Ranges and return the color
    for color, (lower, upper) in HSV_RANGES.items():
        if color in ["red", "white"]: # Skiping these two since we handled them already
            continue

        if lower[0] <= h <= upper[0] and lower[1] <= s <= upper[1] and lower[2] <= v <= upper[2]:
            return color

    return None

# Generating the kociemba string
def generate_kociemba_string(state):
        
    if any(None in face_colors for face_colors in state.values()):
        return "Error: not all faces have been scanned"
        
    kociemba_string = ""

    for face_character in KOCIEMBA_FACE_ORDER:
        scanned_colors = state[face_character]
        for color_name in scanned_colors:
            kociemba_string += COLOR_TO_FACE_MAP[color_name]

    if len(kociemba_string) != 54:
        raise ValueError(f"Invalid cube string lenght: {len(kociemba_string)}. Should be 54.")
    
    counts = Counter(kociemba_string)
    for face_char in "URFDLB":
        if counts[face_char] != 9:
            raise ValueError(f"Invalid cube facelet '{face_char}' appers {counts[face_char]} times instead of 9.")

    return kociemba_string