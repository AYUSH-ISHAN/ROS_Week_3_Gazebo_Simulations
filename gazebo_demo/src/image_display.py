#!/usr/bin/env python
from __future__ import print_function
   
#from std_msg.msg import Float64   
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String, Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
#from geometry_msgs.msg import Twist

class image_converter:
  
    def __init__(self):
        
        self.image_sub = rospy.Subscriber("/gazebo_demo/camera/image_raw",Image,self.callback)
        self.bridge = CvBridge()
        self.car_centroid_x__pub = rospy.Publisher("/car_centroid_x", Float64, queue_size = 10)
        self.car_centroid_y__pub = rospy.Publisher("/car_centroid_y", Float64, queue_size = 10)

        #self.image_pub = rospy.Publisher("/car_masking",Image)

    def callback(self,data):
        try:
          cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
          print(e)
   
        rows,cols,channels = cv_image.shape
        # hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        ## there was a hsv convertor part take a look

        lower_red=np.array([0,0,100])          #([70,48,255])
        upper_red=np.array([100,185,255])       #([50,28,245])

        ## blurring the image - no_need           

        ##  thresholding
        mask = cv2.inRange(cv_image, lower_red, upper_red)
        ##  getting the centroid of the car

        m = cv2.moments(mask, False)
        try:
          cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
          cy, cx = rows/2, cols/2
        print("Coordinates of Centroid is : ")
        print(cx, cy)

        cv2.imshow("mask", mask)
        cv2.imshow("real_image", cv_image)
        cv2.waitKey(3)

        try:
          #self.image_pub.publish(self.bridge.cv2_to_imgmsg(mask, "bgr8"))
          self.car_centroid_x__pub.publish(cx)
          self.car_centroid_y__pub.publish(cy)
        except CvBridgeError as e:
          print(e)


        # try:
        #   error_x = cx;
        #   speed = Twist();
        #   speed.linear.x = cx*2;

        #   self.car_speed_pub(speed);

        # try:
        #   error_y = cy;
        #   speed = Twist();
        #   speed.linear.y = cy*2;

        #   self.car_speed_pub(speed);

          


        # if cols > 60 and rows > 60 :
        #   cv2.circle(cv_image, (50,50), 10, 255)
   
        # cv2.imshow("Image window", cv_image)
        # cv2.waitKey(3)
   
        # try:
        #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        # except CvBridgeError as e:
        #   print(e)
   
def main(args):
      ###  if got some error then put line 2 in line 1
      ic = image_converter()
      rospy.init_node('image_converter', anonymous=True)

      try:
        rospy.spin()
      except KeyboardInterrupt:
        print("Shutting down")
      cv2.destroyAllWindows()
    
if __name__ == '__main__':
          main(sys.argv)
