import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from cvzone.HandTrackingModule import HandDetector
from math import hypot
import screen_brightness_control as sbc

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
detector = HandDetector(detectionCon=0.5, maxHands=1)
speaker_volume = AudioUtilities.GetSpeakers()
interface = speaker_volume.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_vol, max_vol = volume.GetVolumeRange()[:2]
i=3

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand1=hands[0]
        list_lm=hand1["lmList"]
        bbox1=hand1["bbox"]
        centre_p=hand1["center"]
        right_left=hand1["type"]
        if list_lm:
            fingers = detector.fingersUp(hand1)
            finger_count = fingers.count(1)
            cv2.putText(img, f'Fingers:{finger_count}', (bbox1[0] + 200, bbox1[1] - 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        if finger_count==5 or finger_count==4:
            x1,y1=list_lm[4][0],list_lm[4][1]
            x2,y2 = list_lm[8][0],list_lm[8][1]
            cv2.circle (img,(x1,y1),4, (255,0,0) ,cv2.FILLED)
            cv2.circle(img,(x2,y2) ,4, (255,0,0) ,cv2.FILLED)
            cv2.line(img, (x1, y1), (x2,y2), (255,8,0), 3)
            finger_distance = hypot(x2-x1,y2-y1)
            brightness_control = np.interp(finger_distance,[40,200],[0,100])
            sbc.set_brightness(brightness_control)      
        elif finger_count==1:
            if 0<i<41:
                i+=1
            elif i<1:
                i+=1
        elif finger_count==2:
            if 0<i<41:
                i-=1
            elif i>40:
                i-=1
            elif i<1:
                i+=1
        volume_control = np.interp(i,[1,40],[-65.25, 0.0])
        volume.SetMasterVolumeLevel(volume_control,None)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
