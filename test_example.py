import cv2
import numpy as np
import pygame
import sys

pygame.init()

bindcolor=[0,255,0]
print_1=(0,0)
point_2=(0,0)
center=(0,0)

window=pygame.display.set_mode((640,480))

element = cv2.getStructuringElement (cv2.MORPH_CROSS, (3,3))

blue_low=np.array([105,75,0],np.unint8)

blue_hi = np.array([135,255,255], np.uint8)

arlimit_l = 500
arlimit_h = 10000
asp_1=0.33
asp_h=2.33

cap=cv2.VideoCapture()

def preprocess(frame):
	imblur=cv2.medianBlur(frame,3)
	imhsv=cv2.cvtColor(imblur,cv2.COLOR_BGR2HSV)

	thresholded = cv2.inRange(imhsv,blue_low,blue_hi)
	eroded = cv2.erode(thresholded,element)
	return eroded
def segment(frT):
	contours, hierarchy = cv2.findContours(frT.copy(), 	
									cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	for i,cnt in enumerate(contours):
		x,y,w,h=cv2.boundingRect(cnt)
		cont_area=w*h
		if cont_area>arlimit_1 and cont_area<arlimit_h:
			aspect=float(w)/float(h)
			if aspect>asp_1 and aspect<asp_h:
				cv2.rectangle(frame,(x,y),(x+w,y+h), bindcolor,2)
				global center
				center=(x+(w/2),y+(h/2))
				break
	return frame,center

def draw_path(point_2):
	global point_1
	if point_2 == None:
		return
	pygame.draw.line(window,(0,255,0),point_1,point_2)
	point_1=point_2
	pygame.display.flip()
	return
while(True):
	f,o_frame=cap.read()
	ch=cv2.waitKey(50)
	try:
		o_frame = cv2.resize(o_frame,(640,480))
		frame=cv2.flip(o_frame,1)
		eroded=preprocess(frame)
		cv2.imshow('Eroded', eroded)
		frame,center=segment(eroded)
		cv2.imshow('Video',frame)
		draw_path(center)
		ch=cv2.waitKey(50)
	except Exception as e:
		print(str(e))



	if ch==27:
		break
cap.release()
cv2.destroyAllWindows()