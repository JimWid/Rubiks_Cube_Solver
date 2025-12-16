# Rubiks Cube Solver In Real Time (Computer Vision)
This project provides a real-time Rubik's Cube detector with color recognition built using the YOLOv11 object detection framework and a custom-trained model. It utilizes your webcam feed to identify and highlight Rubik's Cubes and its color in real-time. Once all colors are detected it will give you a set of steps to solve the cube.
# Features
 - **Real-time Detection**: Detects Rubik's Cubes and its color live from your webcam feed.
 - **YOLOv11 Powered**: Leverages the efficient and accurate YOLOv11 architecture.
 - **Custom Trained Model**: Utilizes a specifically trained model (best.pt) optimized for Rubik's Cube detection.
 - **TwoPhase Solver**: Utilizes the module TwoPhaseSolver to generate a set of moves to solve the cube in **20 moves or less**.
# Getting Started
Follow these steps to get the detector up and running on your local machine.
## Prerequisites
### Before you begin, ensure you have the following:
Python 3.8+ (Recommended)
- A webcam connected to your computer
- A stable internet connection for the initial setup
- (Optional but Recommended) A NVIDIA GPU for faster inference. If you don't have one, the model will run on your CPU, which might be slower.
## 1. Clone the Repository
First, clone this project repository to your local machine:
code: 
```
git clone https://github.com/JimWid/Rubiks_Cube_Solver.git
cd Rubiks_Cube_Solver
```
## 2. Set up the Enviroment
```
python -m venv env
```
## Activate the virtual environment
### On Windows:
```
env\Scripts\activate
```
### On macOS/Linux:
```
source env/bin/activate
```
### Install the required Python packages
```
pip install -r requirements.txt
```
## 3. Run Main.py file
```
python main.py
```
- The module TwoPhaseSolver will start downloading, *this may take some time*, but only on the first time you run main.py, later it wont need to load.
- A window showing your webcam feed will open. With certain comments and intructions for the user.
- The detector will start analyzing the feed in real-time and draw bounding boxes around the most confident Rubik's Cube detected.
- Press the q key to quit the application.

# Important notes on Cube Orientation and Directions:
After some try and error I have finally found the correct sequence and orientations the faces should have at the moment of scanning. (**the sequence itself is not necessary but it helps to know the orientation**) Since the program relies on Colors, make sure to follow:
### First:
Defining Your Cube: Make sure you see your cube as:
- **White: UP**
- **Green: Front**
- **Red: Right**
- **Blue: Back**
- **Yellow: Down**
- **Orange: Left**

Once you have the center of **Green** in front of you(or the camera). **turn down** to scan **White** first, move the cube **UP** to face green again. And turn the cube **right(->)** to scan the **Red** face, then right again(->) to scan **Blue**, again to scan **Orange** and again to scan **Green**, keep Green in front of the camera and then **move up** to scan **Yellow**. [Watch Video](https://youtu.be/rkV9gtoWGrM) to see how it is.

# Known Limitations and Tips for Best Performance
#### Lighting Conditions: 
The model performs best in well-lit environments. Poor lighting, excessive shadows, or glare can reduce detection on cube and color accuracy.
#### Background Clutter: 
A plain, contrasting background behind the Rubik's Cube can improve detection reliability.
#### Object Distance and Angle: 
The model is trained on a variety of distances and angles, but extreme close-ups, far distances, or unusual orientations might sometimes be challenging. Try presenting the cube clearly in the camera's view.
#### Performance: 
On CPU, detection might be noticeably slower, leading to a lower frame rate. For real-time smooth performance, a GPU is highly recommended.
 - **Color Performance**: It is very confident and succesful with most of the colors in the right lighting, most complicated color to detect is Orange getting confused by Red (**this has improved**).
 - **Confidence Threshold**: If the detector isn't picking up cubes, you might need to adjust the CONFIDENCE_THRESHOLD variable in main.py. Lowering it could show more detections (including potential      false positives), while raising it makes detections stricter.
 - **Solver Performance**: The kociemba string is well generated, but I hypothesis that it needs to be in the right angle and orientation for the kociemba solver to actually accept it. Otherwise it        will get an error. Try to find the correct posture of every face. I'm working on this matter since its very frustrating.
