# Push-Up Counter and Calorie Burner using OpenCV and Pose Detection

## Introduction

This Python script utilizes the OpenCV library and Pose Detection to count push-ups and estimate calories burned during a push-up workout. The code processes a video input (e.g., from a webcam or a pre-recorded video), detects the person's body pose, calculates push-up angles, and tracks push-up counts and calorie expenditure. It also provides visual feedback to guide the user on when to move up or down during a push-up.

## Requirements

- Python: Make sure you have Python installed on your system. You can download it from the official Python website.

- Python Libraries: Install the required Python libraries using pip:


## Installation

1. Download the `vid1.mp4` video file (or use your own video) to use as input. Place it in the same directory as the Python script.

## Usage

1. Run the script using the following command:

2. A window will open displaying the video with real-time push-up counting and calorie estimation. The script will also create an output video named `output.avi` in the same directory.

3. To quit the application, press the 'q' key in the display window.

## Features

- Counts push-ups based on the user's body pose and the predefined angles.
- Estimates calories burned per minute using the MET (Metabolic Equivalent of Task) value, user weight, and time.
- Provides visual guidance with an arrow indicating when to move up or down during a push-up.
- Displays real-time push-up counts and calorie expenditure on the video frame.

## Configuration

- You can adjust the MET value and user weight by modifying the `MET_value` and `weight_kg` variables in the code.
- You can fine-tune the angle thresholds and steady threshold to match your specific push-up form and requirements.

## Limitations

- The accuracy of the push-up count and calorie estimation depends on a lot of things. I used MET to count calories, but a proper calorie burn counter would require more precise details  and the user's adherence to the proper push-up form.

## Author

- [Tanim Ahmed]



## Acknowledgments

- This project was inspired by the desire to create a fun and interactive way to track push-up progress and encourage physical activity.
