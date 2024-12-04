import cv2
import mediapipe as mp
import time
from pynput.mouse import Button, Controller
import math

#Below are modifiable varibles
#Feel free to modify other as well

SmouseMaxY = 1178 # max screen y in pixels + 10
SmouseMaxX = 2018 # max screen x in pixels + 10
DEADZONE = 20 #ADJUSTABLE
smoothing_factor = 0.5 #ADJUSTABLE (0 - 1)
HmouseMinX = 150 # min camera x in pixels
HmouseMaxX = 400 # max camera x in pixels
HmouseMinY = 170 # min camera y in pixels
HmouseMaxY = 400 # max camera y in pixels
clickDelay = 0.3 # check line 96
clickDistance = 15 # check line 96

print("Press 'q' to exit or end the script.")

mouse = Controller()
cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
frame_count = 0

SmouseMinX = -10
#y above
SmouseMinY = -10
#x above

HtoSmultiX = SmouseMaxX / HmouseMaxX
HtoSmultiY = SmouseMaxY / HmouseMaxY

prevClickTime = 0

prev_mouse_pos = (0, 0)

coordDict = [
    {"wrist_X": 0, "wrist_Y": 0},
    {"thumbCMC_X": 0, "thumbCMC_Y": 0},
    {"thumbMCP_X": 0, "thumbMCP_Y": 0},
    {"thumbIP_X": 0, "thumbIP_Y": 0},
    {"thumbTIP_X": 0, "thumbTIP_Y": 0},
    {"indexMCP_X": 0, "indexMCP_Y": 0},
    {"indexPIP_X": 0, "indexPIP_Y": 0},
    {"indexDIP_X": 0, "indexDIP_Y": 0},
    {"indexTIP_X": 0, "indexTIP_Y": 0},
    {"middleMCP_X": 0, "middleMCP_Y": 0},
    {"middlePIP_X": 0, "middlePIP_Y": 0},
    {"middleDIP_X": 0, "middleDIP_Y": 0},
    {"middleTIP_X": 0, "middleTIP_Y": 0},
    {"ringMCP_X": 0, "ringMCP_Y": 0},
    {"ringPIP_X": 0, "ringPIP_Y": 0},
    {"ringDIP_X": 0, "ringDIP_Y": 0},
    {"ringTIP_X": 0, "ringTIP_Y": 0},
    {"pinkyMCP_X": 0, "pinkyMCP_Y": 0},
    {"pinkyPIP_X": 0, "pinkyPIP_Y": 0},
    {"pinkyDIP_X": 0, "pinkyDIP_Y": 0},
    {"pinkyTIP_X": 0, "pinkyTIP_Y": 0}
]

def mouseController(x, y):
    global prev_mouse_pos
    
    if HmouseMinX < x < HmouseMaxX and HmouseMinY < y < HmouseMaxY:
        normalizedX = (x - HmouseMinX) / (HmouseMaxX - HmouseMinX)
        normalizedY = (y - HmouseMinY) / (HmouseMaxY - HmouseMinY)

        normalizedY = 1 - normalizedY
        normalizedX = 1 - normalizedX

        screenX = normalizedX * (SmouseMaxX - SmouseMinX) + SmouseMinX
        screenY = normalizedY * (SmouseMaxY - SmouseMinY) + SmouseMinY

        deltaX = abs(screenX - prev_mouse_pos[0])
        deltaY = abs(screenY - prev_mouse_pos[1])

        if deltaX > DEADZONE or deltaY > DEADZONE:
            smoothX = prev_mouse_pos[0] + (screenX - prev_mouse_pos[0]) * smoothing_factor
            smoothY = prev_mouse_pos[1] + (screenY - prev_mouse_pos[1]) * smoothing_factor
            mouse.position = (smoothX, smoothY)
            prev_mouse_pos = (smoothX, smoothY)

def clickCheck(x, y):
    global prevClickTime

    if HmouseMinX < x < HmouseMaxX and HmouseMinY < y < HmouseMaxY:
        index_tip = coordDict[8]
        thumb_tip = coordDict[4]

        a = math.sqrt((thumb_tip["thumbTIP_X"] - index_tip["indexTIP_X"])**2 + (thumb_tip["thumbTIP_Y"] - index_tip["indexTIP_Y"])**2)

        if a < clickDistance and time.time() > (prevClickTime + clickDelay):
            mouse.click(Button.left, 1)
            print("click")
            prevClickTime = time.time()

        print(f"Distance: {a}")

        
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            for id, lm in enumerate(handLms.landmark):

                h,w,c = img.shape
                cx,cy = int(lm. x*w), int(lm. y*h)

                if id == 0:
                    cv2.circle(img, (cx,cy), 10, (255, 255, 0), cv2.FILLED)
                    coordDict[0] = {"wrist_X": cx, "wrist_Y": cy}
                elif id == 1:
                    coordDict[1] = {"thumbCMC_X": cx, "thumbCMC_Y": cy}
                elif id == 2:
                    coordDict[2] = {"thumbMCP_X": cx, "thumbMCP_Y": cy}
                elif id == 3:
                    coordDict[3] = {"thumbIP_X": cx, "thumbIP_Y": cy}
                elif id == 4:
                    cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)
                    coordDict[4] = {"thumbTIP_X": cx, "thumbTIP_Y": cy}
                    clickCheck(cx, cy)
                elif id == 5:
                    coordDict[5] = {"indexMCP_X": cx, "indexMCP_Y": cy}
                elif id == 6:
                    coordDict[6] = {"indexPIP_X": cx, "indexPIP_Y": cy}
                elif id == 7:
                    coordDict[7] = {"indexDIP_X": cx, "indexDIP_Y": cy}
                elif id == 8:
                    cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)
                    coordDict[8] = {"indexTIP_X": cx, "indexTIP_Y": cy}
                    mouseController(cx, cy)
                    clickCheck(cx, cy)
                elif id == 9:
                    coordDict[9] = {"middleMCP_X": cx, "middleMCP_Y": cy}
                elif id == 10:
                    coordDict[10] = {"middlePIP_X": cx, "middlePIP_Y": cy}
                elif id == 11:
                    coordDict[11] = {"middleDIP_X": cx, "middleDIP_Y": cy}
                elif id == 12:
                    cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)
                    coordDict[12] = {"middleTIP_X": cx, "middleTIP_Y": cy}
                elif id == 13:
                    coordDict[13] = {"ringMCP_X": cx, "ringMCP_Y": cy}
                elif id == 14:
                    coordDict[14] = {"ringPIP_X": cx, "ringPIP_Y": cy}
                elif id == 15:
                    coordDict[15] = {"ringDIP_X": cx, "ringDIP_Y": cy}
                elif id == 16:
                    cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)
                    coordDict[16] = {"ringTIP_X": cx, "ringTIP_Y": cy}
                elif id == 17:
                    coordDict[17] = {"pinkyMCP_X": cx, "pinkyMCP_Y": cy}
                elif id == 18:
                    coordDict[18] = {"pinkyPIP_X": cx, "pinkyPIP_Y": cy}
                elif id == 19:
                    coordDict[19] = {"pinkyDIP_X": cx, "pinkyDIP_Y": cy}
                elif id == 20:
                    cv2.circle(img, (cx,cy), 10, (0, 255, 0), cv2.FILLED)
                    coordDict[20] = {"pinkyTIP_X": cx, "pinkyTIP_Y": cy}
                
            mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)

    cv2.circle(img, (HmouseMinX, HmouseMaxY), 10, (0, 255, 0), cv2.FILLED)
    cv2.circle(img, (HmouseMaxX, HmouseMinY), 10, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (HmouseMinX, HmouseMinY), (HmouseMaxX, HmouseMaxY), (255, 0, 0), 2)

    if time.time() - pTime > 1:
        fps = frame_count
        frame_count = 0
        pTime = time.time()

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()