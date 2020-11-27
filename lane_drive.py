#!/usr/bin/env python

'''libraries'''
import time
import numpy as np
import rospy
import roslib
import cv2


from geometry_msgs.msg import Twist
from sensor_msgs.msg import CompressedImage
from tf.transformations import euler_from_quaternion, quaternion_from_euler

global LSD
LSD = cv2.createLineSegmentDetector(0)  # 이미지의 contour 추출

''' class '''
class robot():
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.img_subscriber = rospy.Subscriber('/raspicam_node/image/compressed',CompressedImage,self.callback_img)

    def callback_img(self,data):
        np_arr = np.fromstring(data.data, np.uint8) 
        self.image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV 3.3.1
        
    def keeping(self,hsv):
        global LSD
        vel_msg=Twist()
        crop_L=hsv[400:460,160:280]
        crop_R=hsv[400:460,400:520]
        crop_S=hsv[180:300,260:380]
        L_mask = cv2.inRange(crop_L,(21,50,100),(36,255,255)) # 왼쪽 노란선
        R_mask = cv2.inRange(crop_R,(40,0,180),(130,30,255)) # 오른쪽 흰선
        S_mask=cv2.inRange(crop_S,(165,0,193),(179,255,255)) # 정지 표지판
      
        yello_line = LSD.detect(L_mask)
        white_line = LSD.detect(R_mask)
        stop_sign = LSD.detect(S_mask)
        
        if stop_sign[0] is not None:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            print('direction : STOP')
        elif yello_line[0] is None :
            vel_msg.linear.x = 0.08
            vel_msg.angular.z = 0.25
            print('direction : LEFT')
        elif white_line[0] is None :
            vel_msg.linear.x = 0.08
            vel_msg.angular.z = -0.25
            print('direction : RIGHT')
        else :
            vel_msg.linear.x = 0.12
            vel_msg.angular.z = 0
            print('direction : STRAIGHT')
        self.velocity_publisher.publish(vel_msg)

    def imageupdate(self):
        image=self.image_np
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image,hsv
        
turtle=robot()
time.sleep(1.2)

if __name__=='__main__':
    while 1:
        try:
            img,hsv=turtle.imageupdate()
            turtle.keeping(hsv)
            time.sleep(0.5) 
        except :
           print('error error')