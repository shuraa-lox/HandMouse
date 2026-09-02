
from colorama import Fore, Style, init

import cv2
import mediapipe as mp
import time, pyautogui
import math

def pix2coord(frame, landmark):
	h, w, _ = frame.shape
	cx, cy = int(landmark.x * w), int(landmark.y * h)
	return cx, cy

def getDistance(x1, y1, x2, y2):
	return math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2)) #Distance formula matematika


init()

cap = cv2.VideoCapture(0) # cumera

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

enabled = False #Mouse tracking switcher
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

RMB_RANGE = 30 # range from index(ukazatelni) to thumb finger which will trigger right mouse buttton
LMB_RANGE = 25 # from index to mid finger left mouse button
MMB_RANGE1 = 130 # range from index finger to wrist which will trigger the mid mouse button (if second condition will work)
MMB_RANGE2 = 120 # same for mid fing

with mp_hands.Hands(
    model_complexity=1, # 0 - speed 1 - uverenost
    max_num_hands=1,  
    min_detection_confidence=0.5, # hand detect uverenost
    min_tracking_confidence=0.5   # finger detect uverennnost
) as hands:

	print("ESC - exit. Enable '='")
	print(f"""{Fore.YELLOW}		{10 * "*"}  MOUSE CONTROL INSTRUCTION  {10 * "*"}
Move mouse - move ur index finger
Right mouse button - Bring your thumb and index(ukazatelnii) fingers together.
Left mouse button - Bring your mid and index fingers together.
Mid mouse button(kolosiko) - Bring mid and index finger to ur wrist
u can just show ur fist(facing top) to the cumera, like \"SOS\" gesture.
	""")

	print(Style.RESET_ALL)

	while cap.isOpened():
		_, frame = cap.read()

		frame = cv2.flip(frame, 1) #flip for mp
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #rgb for mp

		results = hands.process(rgb_frame) #hand detection

        # Если не найдены руки найдены
		if results.multi_hand_landmarks:

			for hand_landmarks in results.multi_hand_landmarks:
	
				mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) # hand skeleton
	
				if not enabled:
					continue  
	
				index_finger_tip = hand_landmarks.landmark[8] #index fing(ukazatalnii)
				ind_x, ind_y = pix2coord(frame, index_finger_tip)
				cv2.circle(frame, (ind_x, ind_y), 10, (0, 255, 0), cv2.FILLED) # green point
	
				cursor_x = int(index_finger_tip.x * screen_width)
				cursor_y = int(index_finger_tip.y * screen_height)
				pyautogui.moveTo(cursor_x, cursor_y)
	
				middle_finger_tip = hand_landmarks.landmark[12] #mid fing
				mid_x, mid_y = pix2coord(frame, middle_finger_tip)
				cv2.circle(frame, (mid_x, mid_y), 10, (255, 0, 0), cv2.FILLED) # red point
	
				thumb_finger_tip = hand_landmarks.landmark[4] #thumb fing(bolshoi)
				thumb_x, thumb_y = pix2coord(frame, thumb_finger_tip)
				cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 0, 255), cv2.FILLED) # blue point
	
				wrist = hand_landmarks.landmark[0] #wrist
				wrist_x, wrist_y = pix2coord(frame, wrist)
				cv2.circle(frame, (wrist_x, wrist_y), 10, (157, 55, 191), cv2.FILLED) # purp point
	
				if getDistance(ind_x, ind_y, wrist_x, wrist_y) <= MMB_RANGE1 and getDistance(mid_x, mid_y, wrist_x, wrist_y) <= MMB_RANGE2:
					pyautogui.mouseUp(button="right")
					pyautogui.mouseUp(button="left")
	
					pyautogui.mouseDown(button="middle")
					print("Holding middle...")
				else:
					pyautogui.mouseUp(button="middle")
	
					if getDistance(ind_x, ind_y, mid_x, mid_y) <= LMB_RANGE:
						pyautogui.mouseUp(button="right")
						pyautogui.mouseUp(button="middle")

						pyautogui.mouseDown(button="left")
						print("Holding left...")
					else:
						pyautogui.mouseUp(button="left")
	
					if getDistance(thumb_x, thumb_y, ind_x, ind_y) <= RMB_RANGE: 
						pyautogui.mouseUp(button="left")
						pyautogui.mouseUp(button="middle")

						pyautogui.mouseDown(button="right")
						print("Holding right...")
					else:
						pyautogui.mouseUp(button="right")

		cv2.imshow('Cumera', frame)

        # Exit & switcher
		key = cv2.waitKey(5) & 0xFF

		if key == 27:
			break
		if key == ord('='): #ord - unicode code
			enabled = not enabled
			print("Status: " + str(enabled))
cap.release()
cv2.destroyAllWindows()
