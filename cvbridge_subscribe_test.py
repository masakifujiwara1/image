#!/usr/bin/env python
# coding: UTF-8

import numpy as np
import rospy
import cv2
from cv_bridge import CvBridge
import os
from sensor_msgs.msg import Image

def start_node():

    rospy.init_node('opencv')
    rospy.loginfo('opencv node started')
    rospy.Subscriber("camera/color/image_raw", Image, process_image)
    rospy.spin()

def process_image(msg):

    try:
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(msg, "bgr8")
        #W = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        #H = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_rate = 20.0 # フレームレート
        size1 = (1080, 720) # 動画の画面サイズ                                                                      

        count=0


       # frame=cv2.medianBlur(frame,5)
       # frame=cv2.GaussianBlur(frame,(5,5),0)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hue = cv2.extractChannel(hsv, 0)
        hue = cv2.inRange(hue, 4, 20)
       # hue = cv2.GaussianBlur(hue,(5,5), 0)
       # frame=cv2.medianBlur(frame,5)
        hue = cv2.medianBlur(hue, 9)
       # output = hue[ 0 : frame.shape[0], 0 : frame.shape[1]]
        #cv2.imshow('mark', frame)

        kernel = np.ones((5,5), np.uint8)
        hue = cv2.erode(hue, kernel, iterations=1)

    #輪郭を検出
        contours, hierarchy = cv2.findContours(hue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #最大輪郭検出準備
        ci, max_area = -1, 0
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
    #最大の輪郭を見つける
            if area > max_area:
                max_area=area
                ci=i
        cnt = contours[ci]

    #輪郭の凸包（convex hull）を求める
        hull = cv2.convexHull(cnt)

    #物体検出    
        n, img_label, data, center = cv2.connectedComponentsWithStats(hue)

    #    tr_x = lambda x : x * 150 / 500 # X軸 画像座標→実座標 
    #    tr_y = lambda y : y * 150 / 500 # Y軸 　〃
        img_trans_marked = frame.copy()
        for i in range(1,n):
            x, y, w, h, size = data[i]
            if size < 30000 : # 面積300px未満は無視
                continue
          #  detected_obj.append( dict( x = tr_x(x),
          #                        y = tr_y(y),
           #                       w = tr_x(w),
        #                      h = tr_y(h),
        #                      cx = tr_x(center[i][0]),
         #                     cy = tr_y(center[i][1])))  
      # 確認
                w_size=w/2
                w_size=int(w_size)
                h_size=h/2
                h_size=int(h_size)
                z_size=(h_size+w_size)/2
                z_size=int(z_size)
                img_trans_marked = cv2.rectangle(img_trans_marked, (x,y), (x+w,y+h),(0,255,0),2)
                img_trans_marked = cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),5,(0,0,255),-1)
                img_trans_marked = cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),w_size,(0,0,255),5)
    #        img_trans_marked = cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),h_size,(0,0,255),5)
                img_trans_marked = cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),z_size,(0,0,255),5)
    #        img_trans_marked = cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),600,(0,0,255),5)
     #       img_trans_marked = cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),700,(0,0,255),5)

    #最大の輪郭と凸包を描画
        img_trans_marked = cv2.drawContours(img_trans_marked, [cnt], -1, (255,0,0), 3)
    #        img_trans_marked = cv2.drawContours(img_trans_marked, [hull], -1, (0,255,0), 3)

    #凹状欠損（convexity defects）の検出
        cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        hull = cv2.convexHull(cnt, returnPoints=False)

    #凹状欠損の点を描画
        defects = cv2.convexityDefects(cnt, hull)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
    #            dist = cv2.pointPolygonTest(hull2,far,True)
    #            print(d)
            if d > 45000:
                count+=1




            cv2.line(img_trans_marked, start, end, [0, 255, 0], 2)
    #            cv2.line(img_trans_marked, avr, far, [0, 255, 0], 2)

           # u = start-far
           # numpy.linalg.norm(u)


            cv2.circle(img_trans_marked, far, 5, [0, 255, 0], -1) 


    #    print(count)
        if count == 3:
            cv2.putText(img_trans_marked, 'choki', (0, 100), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 5, cv2.LINE_AA)
        if count <= 2:
            cv2.putText(img_trans_marked, 'gu', (0, 100), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 5, cv2.LINE_AA)

        if count >= 4:
            cv2.putText(img_trans_marked, 'pa', (0, 100), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 5, cv2.LINE_AA) 

        cv2.imshow('trans',img_trans_marked)
      #  if cv2.waitKey(10) & 0xFF == ord('q'):
     #       break

        #bridge = CvBridge()
           # msg = bridge.cv2_to_imgmsg(img_trans_marked, encoding = "bgr8")

            #rate=rospy.Rate(1)
          #  while not rospy.is_shutdown():
            #pub.publish(msg)
           # rate.sleep()
        cv2.waitKey(10)

    except Exception as err:
        print(err)


   # cv2.destroyAllWindows()

if __name__=='__main__':
    try:
        start_node()
    except rospy.ROSinterruptException: pass
