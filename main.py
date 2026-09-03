
from colorama import Fore, Style, init

import gestures

import cv2
import mediapipe as mp
import pyautogui
import math

buttons = { #Dict with mouse buttons status
	"left" : False,
	"right" : False,
	"middle" : False 
}

def hold(button): #Hold function, which will release all buttons except given
	if not buttons[button]: 
		for btn in buttons.keys():
			if btn != button:
				buttons[btn] = False
				pyautogui.mouseUp(button=btn)

		print("Holded " + button)

		buttons[button] = True
		pyautogui.mouseDown(button=button)

def release(button = None): 
	if button is None:
		for btn in buttons.keys():
			buttons[btn] = False
			pyautogui.mouseUp(button=btn)

		return

	buttons[button] = False
	pyautogui.mouseUp(button=button)


init()

cap = cv2.VideoCapture(0) # cumera

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

enabled = False #Mouse tracking switcher
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0


with mp_hands.Hands(
    model_complexity=0, # 0 - speed 1 - uverenost
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

        # if hand finded
		if results.multi_hand_landmarks:

			for hand_landmarks in results.multi_hand_landmarks:
	
				mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) # hand skeleton
	
				if not enabled:
					continue  
	
				index_finger_tip = hand_landmarks.landmark[8] #index fing(ukazatalnii)
				cursor_x = int(index_finger_tip.x * screen_width)
				cursor_y = int(index_finger_tip.y * screen_height)
				pyautogui.moveTo(cursor_x, cursor_y)
	
				middle_finger_tip = hand_landmarks.landmark[12] #mid fing
				thumb_finger_tip = hand_landmarks.landmark[4] #thumb fing(bolshoi)
				wrist = hand_landmarks.landmark[0] #wrist

				LM_gesture = gestures.LeftMouseGesture(frame, index_finger_tip, middle_finger_tip)
				RM_gesture = gestures.RightMouseGesture(frame, index_finger_tip, thumb_finger_tip)
				MM_gesture = gestures.MiddleMouseGesture(frame, index_finger_tip, middle_finger_tip, wrist)

				if MM_gesture.check():
					hold("middle")
				else:
					release("middle")

					if LM_gesture.check():
						hold("left")
					else:
						release("left")

					if RM_gesture.check(): 
						hold("right")
					else:
						release("right")
					
		else:
			release()

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
