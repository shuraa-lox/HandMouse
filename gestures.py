import math

RMB_RANGE = 30 # range from index(ukazatelni) to thumb finger which will trigger right mouse buttton
LMB_RANGE = 30 # from index to mid finger left mouse button
MMB_RANGE1 = 130 # range from index finger to wrist which will trigger the mid mouse button (if second condition will work)
MMB_RANGE2 = 120 # same for mid fing


def pix2coord(frame, landmark):
	h, w, _ = frame.shape
	cx, cy = int(landmark.x * w), int(landmark.y * h)
	return cx, cy

def getDistance(landmark1, landmark2, frame):

	x1, y1 = pix2coord(frame, landmark1)
	x2, y2 = pix2coord(frame, landmark2)

	return math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))



class Gesture:
	def __init__(self, frame, index_finger):
		self.frame = frame
		self.index_finger = index_finger


class LeftMouseGesture(Gesture):
	def __init__(self, frame, index_finger, middle_finger):
		super().__init__(frame, index_finger)
		self.middle_finger = middle_finger

	def check(self):
		if getDistance(self.index_finger, self.middle_finger, self.frame) <= LMB_RANGE:
			return True
		return False


class RightMouseGesture(Gesture):
	def __init__(self, frame, index_finger, thumb_finger):
		super().__init__(frame, index_finger)
		self.thumb_finger = thumb_finger

	def check(self):
		if getDistance(self.index_finger, self.thumb_finger, self.frame) <= RMB_RANGE:
			return True
		return False


class MiddleMouseGesture(Gesture):
	def __init__(self, frame, index_finger, middle_finger, wrist):
		super().__init__(frame, index_finger)
		self.middle_finger = middle_finger
		self.wrist = wrist

	def check(self):
		if getDistance(self.index_finger, self.wrist, self.frame) <= MMB_RANGE1 \
		and getDistance(self.middle_finger, self.wrist, self.frame) <= MMB_RANGE2:
			return True
		return False
