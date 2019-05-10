import numpy as np
import cv2
from collections import deque
import uuid

class DrawingWindow():
    def __init__(self):
        
        # Define the upper and lower boundaries for a color to be considered "PinkishRed"
        self.redLower = np.array([170,50,220])
        self.redUpper = np.array([180,255,255])

        # Define size of brush for drawing
        self.brush_size = 2

        # Define a 5x5 kernel for erosion and dilation
        self.kernel = np.ones((5, 5), np.uint8)


        # Setup deques to store separate colors in separate arrays
        self.bpoints = [deque(maxlen=512)]
        self.gpoints = [deque(maxlen=512)]
        self.rpoints = [deque(maxlen=512)]
        self.ypoints = [deque(maxlen=512)]

        self.bindex = 0
        self.gindex = 0
        self.rindex = 0
        self.yindex = 0

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        self.colorIndex = 0

        # Setup the Paint interface
        self.paintWindow = np.zeros((1000,2000,3)) + 255


        # Load the video
        self.camera = cv2.VideoCapture(0)



    def draw(self):
        cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
        # Keep looping
        while True:
            # Grab the current paintWindow
            (self.grabbed, self.frame) = self.camera.read()
            self.frame = cv2.flip(self.frame, 1)
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            # Check to see if we have reached the end of the video
            if not self.grabbed:
                break

            # Determine which pixels fall within the red boundaries and then blur the binary image
            self.redMask = cv2.inRange(self.hsv, self.redLower, self.redUpper)
            self.redMask = cv2.erode(self.redMask, self.kernel, iterations=2)
            self.redMask = cv2.morphologyEx(self.redMask, cv2.MORPH_OPEN, self.kernel)
            self.redMask = cv2.dilate(self.redMask,self.kernel, iterations=1)

            # Find contours in the image
            (_, self.cnts, _) = cv2.findContours(self.redMask.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
            self.center = None

            # Check to see if any contours were found
            if len(self.cnts) > 0:
                # Sort the contours and find the largest one
                self.cnt = sorted(self.cnts, key = cv2.contourArea, reverse = True)[0]
                # Get the radius of the enclosing circle around the found contour
                ((self.x, self.y), self.radius) = cv2.minEnclosingCircle(self.cnt)
                # Draw the circle around the contour
                cv2.circle(self.frame, (int(self.x), int(self.y)), int(self.radius), (0, 255, 255), 2)
                # Get the moments to calculate the center of the contour (in this case Circle)
                self.M = cv2.moments(self.cnt)
                self.center = (int(self.M['m10'] / self.M['m00']), int(self.M['m01'] / self.M['m00']))

                if self.colorIndex == 0:
                    self.bpoints[self.bindex].appendleft(self.center)
                elif self.colorIndex == 1:
                    self.gpoints[self.gindex].appendleft(self.center)
                elif self.colorIndex == 2:
                    self.rpoints[self.rindex].appendleft(self.center)
                elif self.colorIndex == 3:
                    self.ypoints[self.yindex].appendleft(self.center)
            # Append the next deque when no contours are detected
            else:
                self.bpoints.append(deque(maxlen=512))
                self.bindex += 1
                self.gpoints.append(deque(maxlen=512))
                self.gindex += 1
                self.rpoints.append(deque(maxlen=512))
                self.rindex += 1
                self.ypoints.append(deque(maxlen=512))
                self.yindex += 1


            # Draw lines of all the colors (Blue, Green, Red and Yellow)
            self.points = [self.bpoints, self.gpoints, self.rpoints, self.ypoints]
            for i in range(len(self.points)):
                for j in range(len(self.points[i])):
                    for k in range(1, len(self.points[i][j])):
                        if self.points[i][j][k - 1] is None or self.points[i][j][k] is None:
                            continue
                        cv2.line(self.frame, self.points[i][j][k - 1], self.points[i][j][k], self.colors[i], self.brush_size)
                        cv2.line(self.paintWindow, self.points[i][j][k - 1], self.points[i][j][k], self.colors[i], self.brush_size)

            # Show the frame and the paintWindow image
            cv2.imshow("Tracking", self.frame)


            #cv2.imshow("Paint", self.paintWindow)

            # If the 'q' key is pressed, stop the loop
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    

        # Cleanup the camera and close any open windows
        self.camera.release()
        cv2.destroyAllWindows()

    def setBrush(self, new_size):
        self.brush_size = new_size

    def save1(self):
        cv2.imwrite("images/image%d.jpg" % uuid.uuid4(), self.paintWindow)

    def save2(self):
        cv2.imwrite("images/image%d.jpg" % uuid.uuid4(), self.frame)

    def clear_everything(self):
        #erase all
        self.bpoints = [deque(maxlen=512)]
        self.gpoints = [deque(maxlen=512)]
        self.rpoints = [deque(maxlen=512)]
        self.ypoints = [deque(maxlen=512)]

        self.bindex = 0
        self.gindex = 0
        self.rindex = 0
        self.yindex = 0

        self.paintWindow[67:,:,:] = 255
