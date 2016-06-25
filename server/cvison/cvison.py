import numpy as np
import cv2

import datetime
import time

# NOTE: Capturing camera at 11 FPS

class cvision:
    def record(self):
        # self.fourcc = cv2.cv.CV_FOURCC(*'mp4v'); #cv2.VideoWriter_fourcc(*'XVID')
        self.camera = cv2.VideoCapture(0)
        # self.video = cv2.VideoWriter('video.mp4',self.fourcc,11,(1280,720))

        self.sum = 0;

        # time.sleep(2)

        for t in range(1,96):
            start = datetime.datetime.now()

            f,img = self.camera.read()
            # self.video.write(img)
            # cv2.imshow("webcam",img)
            # time.sleep(1/24)

            cv2.imwrite('%03d.png'%t, img)

            end = datetime.datetime.now()

            # print (end.time().time-start.time().time)

        # self.video.release()

v = cvision()
v.record()
