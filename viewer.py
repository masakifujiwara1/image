#!/usr/bin/env python
#encoding: UTF-8

import rospy
import cv2

from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def process_image(msg):
    try:
        bridge = CvBridge()
        orig = bridge.imgmsg_to_cv2(msg, encoding = "bgr8")
        cv2.imshow('img', orig)
        cv2.waitKey(10)
    except Exception as err:
        print err

def start_node():
    rospy.init_node('viewer')
    rospy.loginfo('viewer node started')
    rospy.Subscriber("image_data", Image, process_image)
    rospy.spin()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass
