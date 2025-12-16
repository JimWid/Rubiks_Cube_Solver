from typing import Dict, List
from collections import Counter
from twophase.solver import solve

# Cube State Representation Setup: up, right, front, down, left and back
KOCIEMBA_FACE_ORDER = ['U', 'R', 'F', 'D', 'L', 'B']

COLOR_TO_FACE = {
    "white": "U",
    "red": "R",
    "green": "F",
    "yellow": "D",
    "orange": "L",
    "blue": "B"
}

def generate_kociemba_string(state: Dict[str, List[str]]) -> str:
        
    kociemba_string = ""

    for face_character in KOCIEMBA_FACE_ORDER:
        scanned_colors = state[face_character]
        for color_name in scanned_colors:
            kociemba_string += COLOR_TO_FACE[color_name]

    if len(kociemba_string) != 54:
        raise ValueError(f"Invalid cube string lenght: {len(kociemba_string)}. Should be 54.")
    
    counts = Counter(kociemba_string)
    for face_char in "URFDLB":
        if counts[face_char] != 9:
            raise ValueError(f"Invalid cube facelet '{face_char}' appers {counts[face_char]} times instead of 9.")

    return kociemba_string

def solve_cube(face_state: Dict[str, List[str]]) -> str:
    kociemba_str = generate_kociemba_string(face_state)
    solution = solve(kociemba_str)

    return solution