#!/usr/bin/env python

import rospy
import ros_numpy
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
import cv2
from matplotlib import pyplot as plt
import time
import os

def callback(data):

    # raw image data in
    img_rgb = ros_numpy.numpify(data)
    # converts to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # applies gaussian blur filter
    img_blurred = cv2.GaussianBlur(img_gray,(5,5),0)

    # reads template data
    a = os.environ['ROS_PACKAGE_PATH'].split(':')
    os.chdir(a[0] + '/template_match_camera')
    #print os.getcwd()
    template = cv2.imread('template.png',0)
    # print error if no template is found
    if not template.any():
        print "No template found"
    # blurs template, (5,5) is GaussianBlur kernel, 0 sets sigma to default for selected kernel.
    template_blurred = cv2.GaussianBlur(template,(5,5),0)
    w, h = template.shape[::-1]

    # matches pattern against image data, creates a intensity map of match confidence
    res = cv2.matchTemplate(img_blurred,template_blurred,cv2.TM_CCOEFF_NORMED)

    # threshold value for matching 0-1, should be as high as possible
    threshold = 0.3

    # locate each point in res that is above threshold value
    loc = np.where( res >= threshold)
    coords = zip(*loc[::-1])

    # draw ractangle at every match
    for point in coords:
        cv2.rectangle(img_rgb, point, (point[0] + w, point[1] + h), (0,0,255), 2)

    # draws image
    cv2.imshow("res", img_rgb)
    cv2.waitKey(1)

    # check if no coords are found and publish to publisher
    pub = rospy.Publisher('/object_status', Bool, queue_size=10)

    if not coords:
        pub.publish(False)
    else:
        pub.publish(True)


    # sets display frequency
    time.sleep(0.01)



# main code,
def listener():

    rospy.init_node('templatematch')

    rospy.Subscriber("/usb_cam/image_raw", Image, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
