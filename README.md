# Rubiks Cube Solver In Real Time (Computer Vision)
A full-stack Rubik's Cube Dectetor using Computer Vision, integrating a **fine-tuned** YOLOv11n to detect physical cubes via webcam in real time. Future steps are to add the backend to handle the logic to generate an optimal solution (in 20 moves or less) to solve the cube.


The project is designed as a production-style ML system, combining frontend inference, model deployment, and a backend solver.
## Features (Implemented)
- Real-time Rubik’s Cube detection using webcam input.
- Model YOLOv11n.onnx object detection running fully in the browser.
- ONNX Runtime Web for fast client-side inference.
- Webcame draws bounding boxes, and displays confidence + FPS.
- Can either do **live detection** or **take a pic of the frame** to detect.
- Deployed frontend using Vercel

## What is to come!
- Cube state extraction (face colors → cube notation)
- FastAPI backend for solving logic
- Two-Phase Solver for optimal cube solutions
- Dockerized backend deployment
- Frontend ↔ Backend API integration

## Architecture
```
Frontend / src
 ├── app/
 │    └── page.tsx           # Main page (calling Yolo component)
 │
 ├── components/
 │    ├── Yolo.tsx           # Yolo (adding both components)
 │    ├── runModel.tsx       # Calling Model
 │    └── videoDetector.tsx  # Webcame Component
 │
 └── lib/
      └── api.js             # Api handleling

Backend                      # Still not in use
 ├── app/
 ├── Dockerfile
 └── requirements.txt

old_version                  # This is the older version already with Detection + Solver but only on Python.
 ├── display_cube.py 
 ├── funcs.py
 └── main.py
```
## Model Details
- Model: YOLOv11n.onnx (fined-tuned to detect rubik's cube)
- Input: Live webcam frames
- Output: Bounding Boxes + class confidence
- Postprocessing:
  - Confidence thresholding
  - Non-Maximum Suppression (NMS)
  - Canvas rendering
    
## Live Demo!
You can try it right here!
### Live Site:
[rubiks-cube-solver.vercel.app](http://rubiks-cube-solver-xi.vercel.app/)

## Tech Stack:
### Frontend
- Next.js
- TypeScript
- ONNX Runtime Web

### Backend
- FastAPI
- Python
- Two-Phase Rubik’s Cube Solver
- Docker

## Acknowledgements and Credits
The frontend develepment and logic from this project was highly inspired and took reference from an existing open-source work in the computer vision and object detection community!

I would like to give special thanks to the original author whose work served as a strong fundation for this project.

Special thanks and credits to **[Juan Sebastian (@juanjaho)](https://github.com/juanjaho)**
### Repo I took inspiration from:
https://github.com/juanjaho/real-time-object-detection-web-app

# License
This project includes code adapted from GPL-licensed open-source work.
In accordance with the GPL, this repository is released under the same license.

All original authors retain credit for their respective contributions.

```
This project is licensed under the GNU General Public License v3.0 (GPL-3.0) or any later version.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```
For more info read [LICENSE](LICENSE) here.
