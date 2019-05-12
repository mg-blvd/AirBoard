import numpy as np
import cv2
from collections import deque
import uuid
from PIL import Image


class DrawingWindow():
    def __init__(self):
        #Flag that will allow is to close the windows
        self.close_wins = False
        # Define the upper and lower boundaries for a color to be considered "PinkishRed"
        self.redLower = np.array([170,50,220])
        self.redUpper = np.array([180,255,255])

        # Define size of brush for drawing
        self.brush_size = 2

        # Define a 5x5 kernel for erosion and dilation
        self.kernel = np.ones((5, 5), np.uint8)

        # List of layers for different point sizes and their colors
        self.points = []
        self.points_size = []
        self.colorIndexes = []

        # RGB values of Red, Blue, Green, and Yellow
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        self.colorIndex = 0


        self.width = 0
        self.height = 0

        # Load the video
        self.camera = cv2.VideoCapture(0)




        # Setup the Paint interface, values here not important, will change in the Draw function
        self.paintWindow = np.zeros((self.width,self.height,3)) + 255










    def draw(self):
        cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
        # Keep looping



        while True:
            # Grab the current paintWindow
            (self.grabbed, self.frame) = self.camera.read()
            self.frame = cv2.flip(self.frame, 1)
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)


            #Need to do a funky save image and get the size because opencv has no easy way to get resolution of video stream. Use that size of the image to set the white frame window and then replace the image with a white screen because noone wants a mugshot of themself
            if(self.width == 0):
                cv2.imwrite("images/temp.jpg", self.frame)
                im = Image.open("images/temp.jpg")
                self.width, self.height = im.size
                # Setup the Paint interface
                self.paintWindow = np.zeros((self.height,self.width,3)) + 255
                cv2.imwrite("images/temp.jpg", self.paintWindow)



            # Check to see if we have reached the end of the video
            if not self.grabbed:
                break

            # Determine which pixels fall within the red boundaries and then blur the binary image
            self.redMask = cv2.inRange(self.hsv, self.redLower, self.redUpper)
            self.redMask = cv2.erode(self.redMask, self.kernel, iterations=2)
            self.redMask = cv2.morphologyEx(self.redMask, cv2.MORPH_OPEN, self.kernel)
            self.redMask = cv2.dilate(self.redMask,self.kernel, iterations=1)

            # Find contours in the image

            # IMPORTANT: Depending on your machine, you may need 2 or 3 result parameters
            # for this function. Try (self.conts, _) or (_, self.conts, _) respectively if there is an issue.
            try:
                (_, self.cnts, _) = cv2.findContours(self.redMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            except:
                (self.cnts, _) = cv2.findContours(self.redMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)







            self.center = None

            self.setBrush(self.brush_size)
            current_index = len(self.points) - 1
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
                    self.points[current_index][0][self.colorIndexes[current_index][0]].appendleft(self.center)
                elif self.colorIndex == 1:
                    self.points[current_index][1][self.colorIndexes[current_index][1]].appendleft(self.center)
                elif self.colorIndex == 2:
                    self.points[current_index][2][self.colorIndexes[current_index][2]].appendleft(self.center)
                elif self.colorIndex == 3:
                    self.points[current_index][3][self.colorIndexes[current_index][3]].appendleft(self.center)
            # Append the next deque when no contours are detected
            else:
                self.points[current_index][0].append(deque(maxlen=512))
                self.colorIndexes[current_index][0] += 1

                self.points[current_index][1].append(deque(maxlen=512))
                self.colorIndexes[current_index][1] += 1

                self.points[current_index][2].append(deque(maxlen=512))
                self.colorIndexes[current_index][2] += 1

                self.points[current_index][3].append(deque(maxlen=512))
                self.colorIndexes[current_index][3] += 1


            # Draw lines of all the colors (Blue, Green, Red and Yellow), as well as lines of different sizes

            for l in range(len(self.points)):
                for i in range(len(self.points[l])):
                    for j in range(len(self.points[l][i])):
                        for k in range(1, len(self.points[l][i][j])):
                            if self.points[l][i][j][k - 1] is None or self.points[l][i][j][k] is None:
                                continue
                            cv2.line(self.frame, self.points[l][i][j][k - 1], self.points[l][i][j][k], self.colors[i], self.points_size[l])
                            cv2.line(self.paintWindow, self.points[l][i][j][k - 1], self.points[l][i][j][k], self.colors[i], self.points_size[l])

            # Show the frame and the paintWindow image
            cv2.imshow("Tracking", self.frame)


            # If the 'q' key is pressed, stop the loop
            if cv2.waitKey(1) & self.close_wins:
                break



        # Cleanup the camera and close any open windows
        self.camera.release()
        cv2.destroyAllWindows()

    def setBrush(self, new_size):
        # If the brush size has changed or there are no layers: add a new layer
        if self.brush_size != new_size or not self.points:
            self.brush_size = new_size
            self.points.append([[deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)]])
            self.points_size.append(self.brush_size)
            self.colorIndexes.append([0,0,0,0])

    def save1(self):
        cv2.imwrite("images/image%d.jpg" % uuid.uuid4(), self.paintWindow)

    def save2(self):
        cv2.imwrite("images/image%d.jpg" % uuid.uuid4(), self.frame)

    def clear_everything(self):
        #erase all - clears all layers
        self.points.clear()
        self.colorIndexes.clear()
        self.points_size.clear()
        self.paintWindow[67:,:,:] = 255
