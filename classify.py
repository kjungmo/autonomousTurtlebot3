#!/usr/bin/env python

'''libraries'''
import time
import numpy as np
import rospy
import roslib
import cv2
import tensorflow as tf
import keras
import numpy as np


from geometry_msgs.msg import Twist
from sensor_msgs.msg import CompressedImage
from tf.transformations import euler_from_quaternion, quaternion_from_euler

global LSD
LSD = cv2.createLineSegmentDetector(0) # 이미지의 contour 추출

''' class '''
class robot():
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.img_subscriber = rospy.Subscriber('/raspicam_node/image/compressed',CompressedImage,self.callback_img)

    def callback_img(self,data):
        np_arr = np.fromstring(data.data, np.uint8) 
        self.image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV 3.3.1
        

    def imageupdate(self):
        image=self.image_np
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image,hsv
        
turtle=robot()
time.sleep(1.2)
model = tf.keras.models.load_model('/home/pi/4layer_3class_aug.h5') # remote PC에서 훈련시킨 모델 사용


if __name__=='__main__':
    while 1:
        try:
            img,hsv = turtle.imageupdate()
            
            time.sleep(0.5)
            
            detect = hsv
            detect = cv2.resize(detect, (320, 320))        
            detect = np.expand_dims(detect, axis=0)

            pred = np.argmax(model.predict(detect), axis=1)

            index = pred[0]
            label = ['Stop', 'Straight', 'Corner']   # datagenerator에서의 라벨값을 넣어준다 
            print(label[index])

        except :
           print('error error')