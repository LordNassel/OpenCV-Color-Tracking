# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments for GREEN
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# construct the argument parse and parse the arguments for RED
apRED = argparse.ArgumentParser()
apRED.add_argument("-b", "--bufferRED", type=int, default=32,
	help="max buffer size")
argsRED = vars(apRED.parse_args())



# define the lower and upper boundaries of the "GREEN" in the HSV color space
greenLower = (45, 100, 50)
greenUpper = (90, 255, 255)

# define the lower and upper boundaries of the "RED" in the HSV color space
#From the previous ColorFiltering.py code ---------------------------------
redLower = (150, 150, 50)
redUpper = (180, 255, 150)



# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"]) # deque: list-like container with fast appends and pops on either end
counter = 0
(dX, dY) = (0, 0)
direction = ""

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
ptsRED = deque(maxlen=argsRED["bufferRED"]) # deque: list-like container with fast appends and pops on either end
counterRED = 0
(dS, dR) = (0, 0)
directionRED = ""



# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
    
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
    
    
    
# keep looping... :)
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



	# construct a mask for the color "GREEN", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
    
    # construct a mask for the color "RED", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the maskRED
	maskRED = cv2.inRange(hsv, redLower, redUpper)
	maskRED = cv2.erode(maskRED, None, iterations=2)
	maskRED = cv2.dilate(maskRED, None, iterations=2)
    
    

	# find contours in the mask_GREEN and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
    
    	# find contours in the maskRED and initialize the current
	# (s, r) center of the ballRED
	cntsRED = cv2.findContours(maskRED.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	centerRED = None

#------------------------------------------------------------------------------

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			pts.appendleft(center)
            
            
    # only proceed if at least one contour was found
	if len(cntsRED) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		cRED = max(cntsRED, key=cv2.contourArea)                         
		((s, r), radiusRED) = cv2.minEnclosingCircle(cRED)
		MRED = cv2.moments(cRED)
		centerRED = (int(MRED["m10"] /MRED["m00"]), int(MRED["m01"] / MRED["m00"])) 

		# only proceed if the radius meets a minimum size
		if radiusRED > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(s), int(r)), int(radiusRED),
				(0, 255, 255), 2)
			cv2.circle(frame, centerRED, 5, (0, 0, 255), -1)
			ptsRED.appendleft(centerRED)
            
#------------------------------------------------------------------------------          

	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and len(pts) == args["buffer"]:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)



    # loop over the set of tracked points
	for w in np.arange(1, len(ptsRED)):
		# if either of the tracked points are None, ignore
		# them
		if ptsRED[w - 1] is None or ptsRED[w] is None:
			continue

		# check to see if enough points have been accumulated in
		# the buffer
		if counterRED >= 10 and w == 1 and len(ptsRED) == argsRED["bufferRED"]:
			# compute the difference between the s and r
			# coordinates and re-initialize the direction
			# text variables
			dS = ptsRED[-10][0] - ptsRED[w][0]
			dR = ptsRED[-10][1] - ptsRED[w][1]
			(dirS, dirR) = ("", "")
        
        	# otherwise, compute the thicknesRED of the line and
		# draw the connecting lines
		thicknessRED = int(np.sqrt(argsRED["bufferRED"] / float(w + 1)) * 2.5)
		cv2.line(frame, ptsRED[w - 1], ptsRED[w], (0, 0, 255), thicknessRED)


#------------------------------------------------------------------------------ 
#TEXT TO SCREEN # NO PROBLEM HERE! CHECKED TWICE! THIS SHIT WORKS in 1000% !!
    
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 255, 0), 1)
    
    	cv2.putText(frame, "ds: {}, dr: {}".format(dS, dR),
		(150, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
    
    

#------------------------------------------------------------------------------ 
#EXIT FROM SCREEN

	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

#------------------------------------------------------------------------------ 


#RELEASE PART
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()