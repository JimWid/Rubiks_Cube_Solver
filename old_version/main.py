import cv2
import sys
import numpy as np
from backend.app.twophase import solve
from ultralytics import YOLO

from display_cube import display_cube
from funcs import *

# Path to the trained model
CUSTOM_MODEL_PATH = "frontend/public/models/yolo11n.onnx"
CONFIDENCE_THRESHOLD = 0.80

# Loading Custom Trained Model YOLOv11n
try:
    print("Loading YOLOv11n custom model...")
    model = YOLO(CUSTOM_MODEL_PATH)
    print("YOLOv11n model loaded successfully!\n")

except Exception as e:
    print(f"An error occurred during model loading: {e}")
    sys.exit()

# Setting up Cube State
cube_state = {face : [None] * 9 for face in KOCIEMBA_FACE_ORDER}
current_face_state = []
scanned_faces = []
already_printed = False

print(f"Using confidence threshold: {CONFIDENCE_THRESHOLD}\n")
print("Scan: 1. White, 2. Red, 3. Blue, 4. Orange, 5. Green, 6. Yellow\n")

# Camera Setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera D:")
    sys.exit()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break
    
    #frame = cv2.flip(frame, 1)
    display_frame = frame.copy()

    # Converting frame to RGB for the model YOLOv5   
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(img_rgb, conf=CONFIDENCE_THRESHOLD, verbose=False) # Passing the RGB frame to the model
    detections_df = results[0].boxes.data.cpu().numpy()

    # Now we are only detecting the cube with the highest confidence %
    if len(detections_df) > 0 and len(scanned_faces) != 6:
        row = detections_df[detections_df[:, 4].argmax()]
        x1, y1, x2, y2, conf, cls = row
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(display_frame, f"Confidence: {conf*100:.2f}%", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # Sticker Region Calculation (Aprox.)
        box_width = x2 - x1
        box_height = y2 - y1

        # Calculation ROI: Region Of Interest
        # For every sticker in a 3x3 grid + adding a padding to avoid black borders between stickers
        padding_x = int((box_width * 0.1) / 3)
        padding_y = int((box_height * 0.1) / 3)

        # sticker sizes (width uses box_width, height uses box_height)
        sticker_width = max(1, (box_width - 2 * padding_x * 3) // 3)
        sticker_height = max(1, (box_height - 2 * padding_y * 3) // 3)

        detected_face_colors = []

        for r in range(3): # Row of 3
            for c in range(3): # Column of 3
                sticker_x1 = x1 + c * (sticker_width + 2 * padding_x) + padding_x
                sticker_y1 = y1 + r * (sticker_height + 2 * padding_y) + padding_y
                sticker_x2 = sticker_x1 + sticker_width
                sticker_y2 = sticker_y1 + sticker_height

                # Clip coordinates to frame bounds
                sticker_x1_clipped = max(0, min(sticker_x1, frame.shape[1] - 1))
                sticker_y1_clipped = max(0, min(sticker_y1, frame.shape[0] - 1))
                sticker_x2_clipped = max(0, min(sticker_x2, frame.shape[1]))
                sticker_y2_clipped = max(0, min(sticker_y2, frame.shape[0]))

                # ROI = Region Of Interest
                if sticker_y2_clipped > sticker_y1_clipped and sticker_x2_clipped > sticker_x1_clipped:
                    sticker_roi = frame[sticker_y1_clipped:sticker_y2_clipped, sticker_x1_clipped:sticker_x2_clipped]
                else:
                    sticker_roi = np.array([])

                if sticker_roi.size > 0:
                    # Converting ROI to HSV
                    hsv_roi = cv2.cvtColor(sticker_roi, cv2.COLOR_BGR2HSV)

                    # Calculating the median HSV value of the ROI
                    h, s, v = np.median(hsv_roi.reshape(-1, 3), axis=0).astype(int)

                    # Getting color names
                    color_name = get_color_name(h, s, v)
                    detected_face_colors.append(color_name)

                    # Drawing feedback on display frame (grid drawn inside the detection loop)
                    cv2.rectangle(display_frame, (sticker_x1_clipped, sticker_y1_clipped), (sticker_x2_clipped, sticker_y2_clipped), (255, 0, 0), 1)
                    if color_name:
                        text_color = (0, 0, 0) if color_name in ["white", "yellow"] else (255, 255, 255)
                        cv2.putText(display_frame, color_name[0].upper(), (sticker_x1_clipped + 5, sticker_y1_clipped + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
                else:
                    detected_face_colors.append(None) # Append None if ROI is empty (should not happen)

        current_face_state = detected_face_colors

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # Map: Key to Face:
    key_to_face = {'w': 'U', 'r': 'R', 'g': 'F', 'y': 'D', 'o': 'L', 'b': 'B'}

    if chr(key) in key_to_face:
        face_char = key_to_face[chr(key)]

        if current_face_state and len(current_face_state) == 9 and None not in current_face_state:
            cube_state[face_char] = current_face_state
            print(f"Scanned Face: '{face_char}': {current_face_state}")

    if key == ord('c'):
        cube_state = {face: [None] * 9 for face in KOCIEMBA_FACE_ORDER}
        current_face_state = []
        scanned_faces = []
        already_printed = False
        print("\n--- All scanned data cleared. ---\n")

    # Displaying Instructions and Status
    y_offset = 30
    scanned_faces = [face for face, colors in cube_state.items() if colors[0] is not None]
    cv2.putText(display_frame, "Press key for the face's CENTER color:", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    y_offset += 25
    cv2.putText(display_frame, "w:white r:red g:green y:yellow o:orange b:blue", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    y_offset += 30
    cv2.putText(display_frame, f"Scanned Faces: {scanned_faces}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Checking if all faces are scanned and generating the final string
    if len(scanned_faces) == 6:
        y_offset += 30
        k_string = generate_kociemba_string(cube_state)
        cv2.putText(display_frame, "All faces scanned! Press 'c' to clear.", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        y_offset += 25

        # Showing Kociemba String, Cube State and Steps
        if k_string and not already_printed:
            #print(f"\nCube State: {cube_state}")
            print(f"\nKociemba String: {k_string}.\n")
            print("Your 2D cube representation:\n", display_cube(cube_state))

            print("\n---------Steps To Follow---------")
            solution = solve(k_string)
            print(solution)

            # Intructions and Reminders
            print("\nRemember:\n1) Faces: U = Up, R = Right, F = Front, D = Down, L = Left, and B = Back.")
            print("U, R, F, D, L and B denote the Up, Right, Front, Down, Left and Back faces of the cube." \
            "1, 2, and 3 denote a 90°, 180° and 270° clockwise rotation of the corresponding face.")
            already_printed = True

        cv2.putText(display_frame, f"Steps: {solution}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 0), 2)
        cv2.putText(display_frame, solution, (10, y_offset + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 0), 2)

    cv2.imshow("Rubiks Cube Scanner!!!", display_frame)

cap.release()
cv2.destroyAllWindows()
