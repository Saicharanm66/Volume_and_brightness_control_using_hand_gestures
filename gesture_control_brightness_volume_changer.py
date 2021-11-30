import cv2
import time
import os
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from cvzone.HandTrackingModule import HandDetector
from math import hypot
import screen_brightness_control as sbc
from win10toast import ToastNotifier

class Funct():
    def __init__():
        pass
    def brightness(lmList_i,img):
        time.sleep(0.4)
        lmList_i=list_lm
        x1,y1=list_lm[4][0],list_lm[4][1]
        x2,y2 = list_lm[8][0],list_lm[8][1]
        cv2.circle (img,(x1,y1),4, (255,0,0) ,cv2.FILLED)
        cv2.circle(img,(x2,y2) ,4, (255,0,0) ,cv2.FILLED)
        cv2.line(img, (x1, y1), (x2,y2), (255,8,0), 3)
        finger_distance = hypot(x2-x1,y2-y1)
        brightness_control = np.interp(finger_distance,[40,200],[0,100])
        sbc.set_brightness(brightness_control)
    def volume(i):
        time.sleep(1)
        speaker_volume = AudioUtilities.GetSpeakers()
        interface = speaker_volume.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        #min_vol, max_vol = volume.GetVolumeRange()[:2]
        volume_control = np.interp(i,[1,2,3,4,5,6,7,8,9,10,11],[-65.25,-45,-35,-29.625,-22,-15.3125,-11,-8,-5,-2.15625,0])
        volume.SetMasterVolumeLevel(volume_control,None)
    def shutdown():
        os.system("shutdown /s /t 1")
    def notify(operat,status,duration):
        duration=float()
        toaster.show_toast(f"{operat}",
                        f"{status}",
                        duration=duration)
toaster = ToastNotifier()
cap = cv2.VideoCapture(0)
cap.set(9, 1920)
cap.set(16, 1080)
detector = HandDetector(detectionCon=0.5, maxHands=2)
i=3
a=[]
m=[]
c=5
d=5
bol=False
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        #time.sleep(0.1)
        hand1=hands[0]
        list_lm=hand1["lmList"]
        bbox1=hand1["bbox"]
        centre_p=hand1["center"]
        right_left=hand1["type"]
        fingers = detector.fingersUp(hand1)
        finger_count = fingers.count(1)
        cv2.putText(img, f'Fingers:{finger_count}', (bbox1[0] + 200, bbox1[1] - 30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        if len(hands)==2:
            hand2=hands[1]
            list_lm2=hand2["lmList"]
            bbox2=hand2["bbox"]
            centre_p2=hand2["center"]
            right_left2=hand2["type"]
            if list_lm2:
                fingers2 = detector.fingersUp(hand2)
                finger_count2 = fingers2.count(1)
                cv2.putText(img, f'Fingers:{finger_count2}', (bbox2[0] + 200, bbox2[1] - 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                if finger_count==finger_count2==c:
                    a.append(c)
                    c-=1
                    if list(reversed(sorted(list(set(a)))))==[5,4,3,2,1,0]:
                        Funct.shutdown()
        elif len(hands)==1:
            c=5
            a=[]
            if right_left=="Right":
                if finger_count==d:
                    print("yes")
                    m.append(d)
                    d-=1
                    if list(reversed(sorted(list(set(m)))))==[5,4,3,2,1,0]:
                        print("entered")
                        if bol==True:
                            bol=False
                            Funct.notify("Gestures","OFF",2)
                            print("set false")
                            m=[]
                            d=5
                        else:
                            bol=True
                            Funct.notify("Gestures","ON",2)
                            m=[]
                            d=5
            if right_left=="Left":
                if bol==True:
                    if finger_count==5:
                        Funct.brightness(list_lm,img)
                    elif finger_count==2:
                        if 0<i<12:
                            i+=1
                        elif i<1:
                            i+=1
                        Funct.volume(i)
                        #Funct.notify("Volume",f"{i}",1)
                    elif finger_count==1:
                        if 0<i<12:
                            i-=1
                        elif i>11:
                            i-=1
                        elif i<1:
                            i+=1
                        Funct.volume(i)
                        #Funct.notify("Volume",f"{i}",1)
                    
    #cv2.imshow("Image", img)
    cv2.waitKey(1)


