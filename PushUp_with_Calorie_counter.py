import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector
import math
import time

counter = 0
pushup_state = "up"  # Start in the "up" state

cap = cv2.VideoCapture('vid1.mp4')
pd = PoseDetector(trackCon=0.70, detectionCon=0.70)

arrow_x = 100
arrow_y = 250
text_x = 50
text_y = 40  # Vertical position for text

# MET value for push-ups
MET_value = 8

# Weight of the person in kilograms
weight_kg = 180 / 2.20462

# Start time
start_time = time.time()

# Variables to store the previous push-up state and time
prev_pushup_state = "up"
prev_time = start_time

# Variable to store the current calorie count
current_calories = 0.0

# Variables to store the previous angles
prev_left_angle = None
prev_right_angle = None

# Threshold to determine if the person is steady
steady_threshold = 1.0  # Adjust this value as needed

# Font settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.6
font_color = (0, 255, 255)
font_thickness = 1

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_rate = int(cap.get(5))

# Define the codec and create a VideoWriter object for MP4
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 25, (frame_width, frame_height))

def calculate_angle(point1, point2, point3):
    angle = math.degrees(
        math.atan2(point3[1] - point2[1], point3[0] - point2[0]) -
        math.atan2(point1[1] - point2[1], point1[0] - point2[0])
    )
    return angle

def are_angles_steady(left_angle, right_angle):
    global prev_left_angle, prev_right_angle

    if prev_left_angle is not None and prev_right_angle is not None:
        left_angle_diff = abs(left_angle - prev_left_angle)
        right_angle_diff = abs(right_angle - prev_right_angle)

        if left_angle_diff < steady_threshold and right_angle_diff < steady_threshold:
            return True

    prev_left_angle = left_angle
    prev_right_angle = right_angle
    return False

def draw_arrow(img):
    global pushup_state

    # Define the arrow size
    arrow_size = 100

    # Define the arrow color and thickness
    arrow_color = (255, 255, 255)
    arrow_thickness = 8

    # Draw the arrow
    if pushup_state == "down":
        arrow_points = np.array([[arrow_x, arrow_y],
                                 [arrow_x - 20, arrow_y],
                                 [arrow_x, arrow_y - 60],
                                 [arrow_x + 20, arrow_y]],
                                np.int32)
        cv2.fillPoly(img, [arrow_points], arrow_color)
        text = "Go Down"
        text_position = (text_x, arrow_y - arrow_size - 10)
        text_color = (0, 255, 255)
        text_thickness = 1
        cv2.putText(img, text, (60,180), cv2.FONT_HERSHEY_TRIPLEX,.8, (5,255,255), 1)
    else:
        arrow_points = np.array([[arrow_x, arrow_y],
                                 [arrow_x - 20, arrow_y],
                                 [arrow_x, arrow_y + 60],
                                 [arrow_x + 20, arrow_y]],
                                np.int32)
        cv2.fillPoly(img, [arrow_points], (0,255,0))
        text = "Move Up"
        text_position = (text_x, arrow_y + arrow_size + 10)
        text_color = (255, 255, 0)
        text_thickness = 1
        cv2.putText(img, text, (60,350), cv2.FONT_HERSHEY_TRIPLEX, .7, text_color, text_thickness)

    # Add instructional text

    #cv2.putText(img, text, text_position, cv2.FONT_HERSHEY_TRIPLEX, font_scale, text_color, text_thickness)

def draw_angles(img, lmlist):
    global counter
    global pushup_state
    global prev_pushup_state
    global prev_time
    global current_calories

    if len(lmlist) != 0:
        # Define keypoints and their labels
        keypoints = [(11, 'L. Shoulder'), (13, 'L. Elbow'), (15, 'L. Wrist'),
                     (12, 'R. Shoulder'), (14, 'R. Elbow'), (16, 'R. Wrist')]

        for i, (kp_index, kp_label) in enumerate(keypoints):
            x, y, _ = lmlist[kp_index]
            cv2.circle(img, (x, y), 5, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, kp_label, (x - 20, y - 10), font, font_scale, font_color, font_thickness)

        for p1, p2, p3 in [(11, 13, 15)]:
            angle = calculate_angle(lmlist[p1], lmlist[p2], lmlist[p3])

            # Correct angles for both sides to be positive
            if angle < 0:
                angle += 360

            angle_text = f"{int(angle)} degrees"
            x, y, _ = lmlist[p2]
            cv2.putText(img, angle_text, (x - 40, y + 30),cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, (255,0,255), font_thickness)
            cv2.line(img, tuple(lmlist[p1][:2]), tuple(lmlist[p2][:2]), (255, 255, 0), 1)
            cv2.line(img, tuple(lmlist[p2][:2]), tuple(lmlist[p3][:2]), (255, 255, 0), 1)
        for p1, p2, p3 in [(12, 14, 16)]:
            angle2 = calculate_angle(lmlist[p1], lmlist[p2], lmlist[p3])

            # Correct angles for both sides to be positive
            if angle2 < 0:
                angle2 += 360

            angle_text = f"{int(angle2)} degrees"
            x, y, _ = lmlist[p2]
            cv2.putText(img, angle_text, (x - 40, y + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, (0,0,255), font_thickness)
            cv2.line(img, tuple(lmlist[p1][:2]), tuple(lmlist[p2][:2]), (255, 255, 255), 1)
            cv2.line(img, tuple(lmlist[p2][:2]), tuple(lmlist[p3][:2]), (255, 255, 255), 1)
        right_angle = angle2
        left_angle = angle

        # Calculate calories burned per minute based on MET value, weight, and time
        current_time = time.time()
        elapsed_time = current_time - prev_time

        # Determine if the person is steady in any position
        if are_angles_steady(left_angle, right_angle):
            calorie_counting_speed = 0.2
        else:
            calorie_counting_speed = 1.0

        calories_burned_per_minute = (MET_value * weight_kg * 0.0175 * elapsed_time / 60.0) * calorie_counting_speed

        if pushup_state == "up" and right_angle >= 165 and left_angle <= 200:
            pushup_state = "down"
        elif pushup_state == "down" and right_angle <= 50 and left_angle >= 300:
            pushup_state = "half"
        elif pushup_state == "half" and right_angle >= 165 and left_angle <= 200:
            pushup_state = "up"
            counter += 1

        draw_arrow(img)

        # Display the push-up counter and calories burned on the video frame
        cv2.rectangle(img, (30, 10), (300,90), (0, 0, 0), -1)
        cv2.putText(img, f"Push-Ups: ", (text_x, text_y), font, font_scale, (0, 255, 0), font_thickness)
        cv2.putText(img, f"{int(counter)}", (text_x+120, text_y), cv2.FONT_HERSHEY_TRIPLEX,.7, (0, 0, 255), 1)
        current_calories += calories_burned_per_minute
        cv2.putText(img, f"Calories Burned:", (text_x-10, text_y + 30), cv2.FONT_HERSHEY_TRIPLEX, .6, (255, 255, 255), font_thickness)
        cv2.putText(img, f" {current_calories:.2f} kcal", (text_x+155, text_y+30), font, .6, (255, 255, 0), 2)
        prev_pushup_state = pushup_state
        prev_time = current_time

while True:
    ret, img = cap.read()
    if not ret:
        cap = cv2.VideoCapture('vid1.mp4')
        continue

    img = cv2.resize(img, (1000, 500))
    cv2.putText(img, 'Calculating Push-Ups', (400, 60), cv2.FONT_HERSHEY_COMPLEX, 1.4, (255,56,200), 2)
    pd.findPose(img, draw=False)
    lmlist, _ = pd.findPosition(img, draw=False)

    draw_angles(img, lmlist)

    cv2.imshow('frame', img)
    frame2 = cv2.resize(img, (frame_width, frame_height), cv2.INTER_LANCZOS4)

    out.write(frame2)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
