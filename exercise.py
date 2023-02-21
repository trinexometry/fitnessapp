import cv2 
import mediapipe as md

md_drawing = md.solutions.drawing_utils
md_drawing_styles = md.solutions.drawing_styles
md_pose = md.solutions.pose

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

cap = cv2.VideoCapture(0)

def pushup():
    count = 0
    change_res(256, 256)
    position = None
    with md_pose.Pose(min_detection_confidence = 0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            success,image = cap.read()
            if not success:
                print("empty camera")
                break
            image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
            result = pose.process(image)

            imlist = []

            if result.pose_landmarks:
                md_drawing.draw_landmarks(
                    image,result.pose_landmarks,md_pose.POSE_CONNECTIONS)
                for id, im in enumerate(result.pose_landmarks.landmark):
                    h,W,_ = image.shape 
                    X,Y = int(im.x*W), int(im.y*h)
                    imlist.append([id, X,Y])
            if len(imlist) != 0:
                if ((imlist[12][2] - imlist[14][2])>=15 and (imlist[11][2] - imlist[13][2])>=15):
                    position = "down"
                if ((imlist[12][2] - imlist[14][2])<=5 and (imlist[11][2] - imlist[13][2])<=5) and position == "down":
                    position = "up"
                    count +=1 
                    print(count)

            cv2.imshow("push-up counter", cv2.flip(image, 1))
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    cap.release()

pushup()
        

