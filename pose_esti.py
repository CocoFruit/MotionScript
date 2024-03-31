import cv2
import mediapipe as mp
import time
import motionScript
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import random as rand
import string


def right_arm_up(landmarks,mpPose):
    shoulder_threshold = 0.1  # You can adjust this threshold as needed
    elbow_threshold = -0.1  # You can adjust this threshold as needed
    
    right_shoulder_y = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER].y
    right_elbow_y = landmarks[mpPose.PoseLandmark.RIGHT_ELBOW].y
    right_wrist_y = landmarks[mpPose.PoseLandmark.RIGHT_WRIST].y
    right_shoulder_x = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER].x
    right_wrist_x = landmarks[mpPose.PoseLandmark.RIGHT_WRIST].x
    
    if (right_shoulder_y - right_elbow_y > elbow_threshold and
        right_wrist_y - right_shoulder_y > elbow_threshold and
        right_wrist_y - right_shoulder_y < shoulder_threshold and
        right_wrist_x < right_shoulder_x):
        
        return True
    return False

def left_arm_up(landmarks,mpPose):
    shoulder_threshold = 0.1  # You can adjust this threshold as needed
    elbow_threshold = -0.1  # You can adjust this threshold as needed
    
    left_shoulder_y = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER].y
    left_elbow_y = landmarks[mpPose.PoseLandmark.LEFT_ELBOW].y
    left_wrist_y = landmarks[mpPose.PoseLandmark.LEFT_WRIST].y
    left_shoulder_x = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER].x
    left_wrist_x = landmarks[mpPose.PoseLandmark.LEFT_WRIST].x
    
    if (left_shoulder_y - left_elbow_y > elbow_threshold and
        left_wrist_y - left_shoulder_y > elbow_threshold and
        left_wrist_y - left_shoulder_y < shoulder_threshold and
        left_wrist_x > left_shoulder_x):
        
        return True
    
    return False

def left_leg_up(landmarks,mpPose):
    # check if left ankle is higher than the right ankle by a certain threshold
    threshold = 0.1  # You can adjust this threshold as needed

    left_ankle_y = landmarks[mpPose.PoseLandmark.LEFT_ANKLE].y
    right_ankle_y = landmarks[mpPose.PoseLandmark.RIGHT_ANKLE].y

    if left_ankle_y < right_ankle_y - threshold:
        return True
    return False

def right_leg_up(landmarks,mpPose):
    # check if right ankle is higher than the left ankle by a certain threshold

    threshold = 0.1  # You can adjust this threshold as needed

    left_ankle_y = landmarks[mpPose.PoseLandmark.LEFT_ANKLE].y
    right_ankle_y = landmarks[mpPose.PoseLandmark.RIGHT_ANKLE].y

    if right_ankle_y < left_ankle_y - threshold:
        return True
    
    return False

def both_arms_straight_up(landmarks,mpPose):

    # get angle between shoulders and elbows
    right_shoulder = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER]
    right_elbow = landmarks[mpPose.PoseLandmark.RIGHT_ELBOW]

    left_shoulder = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER]
    left_elbow = landmarks[mpPose.PoseLandmark.LEFT_ELBOW]

    right_angle = np.arctan2(right_elbow.y - right_shoulder.y, right_elbow.x - right_shoulder.x)
    left_angle = np.arctan2(left_elbow.y - left_shoulder.y, left_elbow.x - left_shoulder.x)

    right_angle = np.degrees(right_angle)
    left_angle = np.degrees(left_angle)
    
    if right_angle < -20 and left_angle < -20:
        return True
    
    return False

def straddling(landmarks,mpPose):
    # get angle between hip and knees
    right_hip = landmarks[mpPose.PoseLandmark.RIGHT_HIP]
    right_knee = landmarks[mpPose.PoseLandmark.RIGHT_KNEE]

    left_hip = landmarks[mpPose.PoseLandmark.LEFT_HIP]
    left_knee = landmarks[mpPose.PoseLandmark.LEFT_KNEE]

    right_angle = np.arctan2(right_knee.y - right_hip.y, right_knee.x - right_hip.x)
    left_angle = np.arctan2(left_knee.y - left_hip.y, left_knee.x - left_hip.x)

    right_angle = np.degrees(right_angle)
    left_angle = np.degrees(left_angle)

    if right_angle > 93 and left_angle < 77:
        return True
    
    return False


def is_t_posing(landmarks,mpPose):
    if (right_arm_up(landmarks,mpPose) and left_arm_up(landmarks,mpPose)):
        return True

# mpDraw = mp.solutions.drawing_utils
# mpPose = mp.solutions.pose

def start_watching(pose,mpDraw,mpPose,timer,target,random=False,diff=None,m=0,h=0):

    if random and diff:
        target = ""

        for i in range(diff):
            target+=rand.choice(string.ascii_letters[m:h])

        

    # pose = mpPose.Pose()

    # Set up video capture
    cap = cv2.VideoCapture(1)
    
    
    # Set desired resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # make it fullscreen
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


    pTime = 0
    r = 0 # right arm up counter
    l = 0 # left arm up counter
    t = 0 # t pose counter
    u = 0 # both arms up counter
    ll = 0 # left leg up counter
    rl = 0 # right leg up counter
    s = 0 # straddling counter

    frame_cutoff = 15

    prev_hip_y = None
    prev_knee_y = None
    jump_threshold = 0.04  # You can adjust this threshold as needed
    jump_timer_duration = .9  # Adjust the duration of the jump timer in seconds

    jump_timer = time.time() - jump_timer_duration


    current_code = ""

    ms = motionScript.MotionScriptInterpreter()

    memory_font = ImageFont.truetype("Ubuntu_Mono/UbuntuMono-Regular.ttf", size=60)  # Adjust size as needed
    code_font = ImageFont.truetype("Ubuntu_Mono/UbuntuMono-Regular.ttf", size=50)  # Adjust size as needed
    output_font = ImageFont.truetype("Ubuntu_Mono/UbuntuMono-Regular.ttf", size=70)  # Adjust size as needed

    start_time = time.time()

    while time.time()-start_time < timer:
        current_time = time.time()
        success, img = cap.read()
        if not success:
            print("NOT SUCCESSFULLL")
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark
            for id, lm in enumerate(landmarks):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

            if current_time - jump_timer >= jump_timer_duration and s==0: # check for jump

                # Extract hip landmark indices
                left_hip_index = mpPose.PoseLandmark.LEFT_HIP.value
                right_hip_index = mpPose.PoseLandmark.RIGHT_HIP.value

                left_hip = landmarks[left_hip_index]
                right_hip = landmarks[right_hip_index]

                # get knee landmarks
                left_knee = landmarks[mpPose.PoseLandmark.LEFT_KNEE.value]
                right_knee = landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value]

                # Get the vertical position of the hips
                hip_y = (left_hip.y + right_hip.y) / 2
                knee_y = (left_knee.y + right_knee.y) / 2

                # Check for jump
                if prev_hip_y is not None:
                    if prev_knee_y is not None:
                        hip_diff = hip_y - prev_hip_y
                        knee_diff = knee_y - prev_knee_y
                        if hip_diff > jump_threshold and knee_diff > jump_threshold:
                            current_code += "+"
                            jump_timer = current_time

                # Update previous hip position
                prev_hip_y = hip_y
                prev_knee_y = knee_y

            # check for right arm up -- >
            if right_arm_up(landmarks,mpPose) and t== 0:
                r += 1
            else:
                r = 0

            if left_arm_up(landmarks,mpPose) and t== 0:
                l += 1
            else:
                l = 0
            
            # check for t pose
            if is_t_posing(landmarks,mpPose):
                t += 1
            else:
                t = 0

            if straddling(landmarks,mpPose):
                s += 1
            else:
                s = 0

            # check for left leg up
            if left_leg_up(landmarks,mpPose) and t== 0:
                ll += 1
            else:
                ll = 0

            # check for right leg up
            if right_leg_up(landmarks,mpPose) and t== 0:
                rl += 1
            else:
                rl = 0

            if both_arms_straight_up(landmarks,mpPose) and t== 0:
                u += 1
            else:
                u = 0

        # flip image
        img = cv2.flip(img, 1)

        if r > frame_cutoff: 
            current_code += ">"
            r = 0
        
        if l > frame_cutoff: 
            current_code += "<"
            l = 0

        if t > frame_cutoff:
            current_code += "."
            t = 0

        if u > frame_cutoff: 
            try:
                ms.interpret(current_code)
                if ms.output_buffer == target:
                    cap.release()
                    cv2.destroyAllWindows()
                    print("destorying")
                    return True
            except:
                print("error")
            current_code = ""
            u = 0

        if s > frame_cutoff:
            current_code += "-"
            s = 0

        if ll > frame_cutoff-2:
            current_code += "["
            ll = 0
        
        if rl > frame_cutoff-2:
            current_code += "]"
            rl = 0

        # Create a blank image with a black box for text
        img_pil = Image.fromarray(img)
        # Load a monospace font

        draw = ImageDraw.Draw(img_pil)

        # draw a black rectangle
        draw.rectangle([0, 0, 1900, 170], fill=(0, 0, 0,100)) # for memory

        # Render the text
        draw.text((40, 10), str(ms.get_memory()), fill=(50, 255, 0), font=memory_font) # show memory
        draw.text((40, 70), str(ms.get_prointer()), fill=(150, 255, 0), font=memory_font) # show pointer
        draw.text((40, 110), "CURRENT CODE:"+current_code, fill=(50, 255, 0), font=code_font) # show code
        draw.text((40, 600), "OUTPUT:"+ms.output_buffer, fill=(50, 255, 0), font=output_font) # show output buffer
        draw.text((900, 10), "TIMER:"+str(round(timer-(current_time-start_time),2)), fill=(50, 255, 0), font=code_font)
        if random:
            draw.text((900, 70), "CURRENT CODE:"+target, fill=(50, 255, 0), font=code_font) # show code

        # Convert the PIL image 
        img = np.array(img_pil)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        # Resize image to fit screen
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    cap.release()
    # kill cv2 
    cv2.destroyAllWindows()
    # pose.close()
    print(ms.output_buffer,target,ms.output_buffer==target)

    return False

if __name__ == "__main__":
    
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    print("starting")
    start_watching(pose,mpDraw,mpPose,600,"hack")
    cv2.destroyAllWindows()

