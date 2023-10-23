# Motion Detection System with OpenCV

This README provides a comprehensive explanation of a Python script that captures video frames from a camera and detects motion using OpenCV. The script allows you to toggle an alarm mode, triggers an alarm when motion is detected, and stops the alarm. Each part of the code will be explained in detail.

## Table of Contents
- [Motion Detection System with OpenCV](#motion-detection-system-with-opencv)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Code Explanation](#code-explanation)
    - [Import Libraries](#import-libraries)
    - [Global Variables](#global-variables)
    - [beep\_alarm Function](#beep_alarm-function)
    - [Main Function](#main-function)
      - [Camera Configuration](#camera-configuration)
      - [Initial Frame Capture](#initial-frame-capture)
      - [Main Loop](#main-loop)
      - [Alarm Mode Handling](#alarm-mode-handling)
      - [Displaying Frames](#displaying-frames)
      - [Key Handling](#key-handling)
      - [Exception Handling](#exception-handling)
    - [Cleanup](#cleanup)

## Introduction
This Python script uses OpenCV to capture video frames from a camera, processes the frames, and detects motion. When motion is detected, it triggers an alarm by beeping the computer's speaker. The alarm mode can be toggled, and the alarm can be stopped using specific keypresses. Color frames are displayed when the alarm mode is off, and black and white frames are displayed when the alarm mode is on.

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- `imutils` library
- `winsound` library (for audio alerts)

To install the required libraries, you can use `pip`:

```bash
pip install opencv-python imutils
```

## Usage
1. Make sure your camera is connected and functional.
2. Run the Python script by executing it in your terminal or code editor.

## Code Explanation

### Import Libraries
The script begins by importing the necessary libraries, including `cv2` for OpenCV, `imutils` for image processing, and `winsound` for audio alerts.

```python
import threading
import cv2
import imutils
import winsound
```

### Global Variables
Global variables are declared to manage the alarm system. These variables track the alarm state, alarm mode, and the number of frames with detected motion.

```python
alarm = False
alarm_mode = False
alarm_counter = 0
```

### beep_alarm Function
The `beep_alarm` function is responsible for triggering the alarm. It beeps the computer's speaker by calling `winsound.Beep` five times. It checks if `alarm_mode` is still active to stop the beeping if the alarm mode is turned off.

```python
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("[+] ALARM")
        # winsound.Beep(1000, 1000)
    alarm = False
```

### Main Function
The `main` function is the core of the script. It captures video frames, processes them, and handles alarm-related functionality.

```python
def main():
    global alarm_counter
    global alarm_mode
    global alarm
    try:
        vid = cv2.VideoCapture(1)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        print("[+] CAMERA CONFIGURED")
        
        # ... (explained below)
        
    except KeyboardInterrupt:
        print("[+] OPERATION CANCELLED ❌")
    except Exception as ex:
        print("[+] SOMETHING WENT WRONG ❌")
        print(str(ex))
```

#### Camera Configuration
The script initializes the video capture from the camera (in this case, camera index 1) and sets the frame width and height. It prints a message indicating that the camera is configured.

```python
vid = cv2.VideoCapture(1)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
print("[+] CAMERA CONFIGURED")
```

#### Initial Frame Capture
The first frame is captured and stored as `start_frame`. This frame is resized to 500 pixels in width, converted to grayscale for motion detection, and smoothed using Gaussian blur to reduce noise.

```python
ret, start_frame = vid.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
```

#### Main Loop
The script enters a continuous loop to capture and process frames from the camera.

```python
while True:
    _, frame = vid.read()
    frame = imutils.resize(frame, width=500)
```

#### Alarm Mode Handling
If `alarm_mode` is active, the script processes frames for motion detection:

```python
if alarm_mode:
    frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
    difference = cv2.absdiff(frame_bw, start_frame)
    threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
    start_frame = frame_bw
```

- `frame_bw` is created by converting the current frame to grayscale and applying Gaussian blur for noise reduction.
- `difference` is calculated as the absolute difference between `frame_bw` and the `start_frame`.
- `threshold` is created by applying a binary threshold to the difference image, identifying areas with motion.
- The `start_frame` is updated to the current frame for future comparisons.

#### Displaying Frames
If `alarm_mode` is active and motion is detected, the black and white thresholded frame is displayed.

```python
if threshold.sum() > 300:
    alarm_counter += 1
else:
    if alarm_counter > 0:
        alarm_counter -= 1
if alarm_counter >= 10:
    if not alarm:
        alarm = True
        beep_alarm()
cv2.imshow("[+] Cam", threshold)
```

- The sum of pixel values in the thresholded image is used to determine if motion is detected.
- `alarm_counter` is incremented if motion is detected, or decremented if no motion is detected.
- If `alarm_counter` reaches a threshold (set to 10), and the alarm is not active, it triggers the alarm using the `beep_alarm` function.
- The black and white thresholded frame is displayed.
- This part of the code is responsible for motion detection and the handling of alarm-related functionality when `alarm_mode` is active. Let's break it down step by step:

1. `if alarm_mode:`: This condition checks if the `alarm_mode` is active. If it's not, this block of code is skipped, and the program continues to display the regular color frames.

2. `frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`: Here, the current frame is converted to grayscale using the `cv2.COLOR_BGR2GRAY` color conversion. This is done to simplify motion detection since it's easier to work with grayscale images.

3. `frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)`: Gaussian blur is applied to the grayscale frame. This step smooths the image and reduces noise, making it easier to detect significant changes between frames.

4. `difference = cv2.absdiff(frame_bw, start_frame)`: This line calculates the absolute difference between the current grayscale frame (`frame_bw`) and the initial frame (`start_frame`). The result is an image that highlights the areas where motion is occurring.

5. `threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]`: A binary threshold is applied to the difference image. This means that any pixel in the difference image with a value greater than 25 is set to 255 (white), and all other pixels are set to 0 (black). This results in a black and white image where white areas represent motion.

6. `start_frame = frame_bw`: The `start_frame` is updated to the current grayscale frame. This ensures that the next frame will be compared to the most recent frame.

7. `if threshold.sum() > 300:`: The code calculates the sum of all pixel values in the thresholded image. If the sum is greater than 300, it suggests that a significant amount of motion is detected in the frame.

8. `alarm_counter += 1`: If motion is detected, the `alarm_counter` is incremented, indicating that motion is ongoing.

9. `else:`: If no motion is detected, this block is executed.

10. `if alarm_counter > 0:`: If `alarm_counter` is greater than 0, it means that motion was detected in previous frames, but it has now stopped.

11. `alarm_counter -= 1`: In this case, `alarm_counter` is decremented to reduce the count of motion events.

12. `if alarm_counter >= 100:`: If `alarm_counter` reaches or exceeds a threshold (set to 100 in this example), it indicates that motion has been consistently detected over a period.

13. `if not alarm:`: The alarm is only triggered if it is not already active.

14. `alarm = True`: This line activates the alarm.

15. `beep_alarm()`: The `beep_alarm` function is called to trigger the alarm.

16. `cv2.imshow("[+] Cam", threshold)`: Finally, if `alarm_mode` is active and motion is detected, the black and white image (thresholded image) is displayed with the window title "[+] Cam." This allows you to visualize the areas with detected motion.

In summary, this section of the code processes frames in black and white, identifies areas with significant changes (motion), and triggers an alarm when motion is detected and sustained. The threshold values (300 and 100) can be adjusted based on your specific requirements.

#### Key Handling
The script checks for keypresses during each iteration. Keypresses are used to control alarm modes and stop the alarm.

```python
key = cv2.waitKey(1)
if key & 0xFF == 27:  # Press 'Esc' key to exit the program
    print("[+] Exiting the alarm")
    break
if key == ord('t'):  # Press 'A' key to toggle alarm mode
    alarm_mode = not alarm_mode


    print(f"[+] Alarm mode is {'on' if alarm_mode else 'off'}")
elif key == ord('s'):  # Press 'S' key to stop the alarm
    alarm = False
```

- The 'Esc' key (key code 27) is used to exit the program.
- The 'A' key (key code 't') toggles the alarm mode on and off.
- The 'S' key (key code 's') is used to stop the alarm if it's currently active.

#### Exception Handling
The script includes exception handling for KeyboardInterrupt (Ctrl+C to stop the program) and generic exceptions. It provides feedback in case of errors.

```python
except KeyboardInterrupt:
    print("[+] OPERATION CANCELLED ❌")
except Exception as ex:
    print("[+] SOMETHING WENT WRONG ❌")
    print(str(ex))
```

### Cleanup
After exiting the main loop, the script releases the video capture and closes all OpenCV windows.

In summary, this script continuously captures frames from a camera, processes them to detect motion, and triggers an alarm when motion is detected. Users can toggle the alarm mode, stop the alarm, and exit the program using keypresses. The frames displayed in the window are either black and white (motion detection mode) or color (normal mode) based on the value of `alarm_mode`.