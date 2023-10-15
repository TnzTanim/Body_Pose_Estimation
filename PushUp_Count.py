import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector
import math

counter = 0
pushup_state = "down"

cap = cv2.VideoCapture('vid1.mp4')
pd = PoseDetector(trackCon=0.70, detectionCon=0.70)

def calculate_angle(point1, point2, point3):
    angle = math.degrees(
        math.atan2(point3[1] - point2[1], point3[0] - point2[0]) -
        math.atan2(point1[1] - point2[1], point1[0] - point2[0])
    )
    return angle
 
def draw_angles(img, lmlist):
    global counter
    global pushup_state

    if len(lmlist) != 0:
        # Define keypoints and their labels
        keypoints = [(11, 'Left Shoulder'), (13, 'Left Elbow'), (15, 'Left Wrist'),
                     (12, 'Right Shoulder'), (14, 'Right Elbow'), (16, 'Right Wrist')]
        
        for i, (kp_index, kp_label) in enumerate(keypoints):
            x, y, _ = lmlist[kp_index]
            cv2.circle(img, (x, y), 10, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, kp_label, (x - 20, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
        for p1, p2, p3 in [(11, 13, 15)]:
            angle = calculate_angle(lmlist[p1], lmlist[p2], lmlist[p3])
            
            # Correct angles for both sides to be positive
            if angle < 0:
                angle += 360
            
            angle_text = f"{int(angle)} degrees"
            x, y, _ = lmlist[p2]
            cv2.putText(img, angle_text, (x - 40, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            # Draw lines connecting keypoints
            cv2.line(img, tuple(lmlist[p1][:2]), tuple(lmlist[p2][:2]), (0, 255, 0), 2)
            cv2.line(img, tuple(lmlist[p2][:2]), tuple(lmlist[p3][:2]), (0, 255, 0), 2)
        for p1, p2, p3 in [ (12, 14, 16)]:
            angle2 = calculate_angle(lmlist[p1], lmlist[p2], lmlist[p3])
            
            # Correct angles for both sides to be positive
            if angle2 < 0:
                angle2 += 360
            
            angle_text = f"{int(angle2)} degrees"
            x, y, _ = lmlist[p2]
            cv2.putText(img, angle_text, (x - 40, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            # Draw lines connecting keypoints
            cv2.line(img, tuple(lmlist[p1][:2]), tuple(lmlist[p2][:2]), (0, 255, 0), 2)
            cv2.line(img, tuple(lmlist[p2][:2]), tuple(lmlist[p3][:2]), (0, 255, 0), 2)
        
        # Calculate angles for right and left sides
        right_angle = angle2
        left_angle = angle
        
        if pushup_state == "down" and right_angle >= 165 and left_angle <= 200:
            pushup_state = "up"
        elif pushup_state == "up" and right_angle <= 50 and left_angle >= 300:
            pushup_state = "half"
        elif pushup_state == "half" and right_angle >= 165 and left_angle <= 200:
            pushup_state = "down"
            counter += 1
        
        # Display the push-up count on the video frame
        cv2.rectangle(img, (0, 0), (120, 120), (255, 0, 0), -1)
        cv2.putText(img, str(int(counter)), (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

while True:
    ret, img = cap.read()
    if not ret:
        cap = cv2.VideoCapture('vid1.mp4')
        continue

    img = cv2.resize(img, (1000, 500))
    cv2.putText(img, 'AI Push Up Counter', (345, 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    pd.findPose(img, draw=False)
    lmlist, _ = pd.findPosition(img, draw=False)

    draw_angles(img, lmlist)

    cv2.imshow('frame', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
