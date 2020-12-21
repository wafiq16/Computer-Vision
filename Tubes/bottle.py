import numpy as np
import cv2

cap = cv2.VideoCapture('botolkuha.mp4') #Open video file

width = int(cap.get(3))
height = int(cap.get(4))

batasKiri   = int( 1*width/6)
bataskanan  = int( 5*width/6)
batasAtas   = int( 1*height/6)
batasBawah  = int( 5*height/6)

batasColor = (255,255,255)

myImage = cv2.imread("hsv_table.png",1)
cv2.namedWindow('image')

bottleCount = 0;
def nothing(x):
    pass
# create trackbars for color change
cv2.createTrackbar('H_LOW','image',0,180,nothing)
cv2.createTrackbar('S_LOW','image',0,255,nothing)
cv2.createTrackbar('V_LOW','image',0,255,nothing)
cv2.createTrackbar('H_HIGH','image',0,180,nothing)
cv2.createTrackbar('S_HIGH','image',0,255,nothing)
cv2.createTrackbar('V_HIGH','image',0,255,nothing)
cv2.createTrackbar('param1','image',1,200,nothing)
cv2.createTrackbar('param2','image',10,200,nothing)
cv2.createTrackbar('MIN_RAD','image',50,100,nothing)
cv2.createTrackbar('MAX_RAD','image',50,100,nothing)
# cv2.createTrackbar('CANNY_LOW','image',100,200,nothing)
# cv2.createTrackbar('CANNY_HIGH','image',150,200,nothing)

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

kernelLow = np.ones((1,1),np.uint16)
kernelHigh = np.ones((3,3),np.uint16)

cv2.imshow('panduan',myImage)

while(cap.isOpened()):
    
    ret, frame = cap.read()

    # hsv = frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    hLTreshold = cv2.getTrackbarPos('H_LOW','image')
    sLTreshold = cv2.getTrackbarPos('S_LOW','image')
    vLTreshold = cv2.getTrackbarPos('V_LOW','image')
    hHTreshold = cv2.getTrackbarPos('H_HIGH','image')
    sHTreshold = cv2.getTrackbarPos('S_HIGH','image')
    vHTreshold = cv2.getTrackbarPos('V_HIGH','image')
    param1 = cv2.getTrackbarPos('param1','image')
    param2 = cv2.getTrackbarPos('param2','image')
    minRadius = cv2.getTrackbarPos('MIN_RAD','image')
    maxRadius = cv2.getTrackbarPos('MAX_RAD','image')
    # cannL = cv2.getTrackbarPos('CANNY_LOW','image')
    # cannH = cv2.getTrackbarPos('CANNY_HIGH','image')
    s = cv2.getTrackbarPos(switch,'image')

    # if s == 0:
        # frame[:] = 0 
    mask = cv2.inRange(hsv, (hLTreshold, sLTreshold, vLTreshold), (hHTreshold, sHTreshold, vHTreshold))
    # mask = cv2.medianBlur(hsv,5)
    # mask = cv2.Canny(mask,cannL,cannH)
    mask = cv2.erode(mask,kernelHigh,iterations = 3)
    # mask = cv2.dilate(mask,kernelLow,iterations = 3)
    # mask = cv2.bitwise_not(mask)
    ## slice the green
    # mask3C = np.zeros_like(frame)
    

    # imask = mask>0
    # myColor = np.zeros_like(frame, np.uint16)
    # myColor[imask] = frame[imask]

    circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,10,
                            param1,param2,minRadius,maxRadius)

    circles = np.uint16(np.around(circles))

    cimg = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    j = 0
    if circles is not None and circles[0][0].ndim == 1:
        bottleCount = 0
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
            print(i[1])
            print("width = " + str(width) + "heigh = " + str(height) + "\n")
            
            if j == 2 :
                j = 0 
            if s == 1:
                bottleCount += 1
            j += 1

    # frame = cv2.line(frame, (batasKiri,batasAtas) , (batasKiri, batasBawah), batasColor, thickness=2)
    # frame = cv2.line(frame, (bataskanan,batasAtas) , (bataskanan, batasBawah), batasColor, thickness=2)
    # frame = cv2.line(frame, (bataskanan,batasAtas) , (batasKiri, batasAtas), batasColor, thickness=2)
    # frame = cv2.line(frame, (bataskanan,batasBawah) , (batasKiri, batasBawah), batasColor, thickness=2)
    str_bootle = 'Jumlah Botol: '+ str(bottleCount)
    cv2.putText(cimg, str_bootle ,(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2,cv2.LINE_AA)
    cv2.imshow("myFrame",cimg)
    cv2.imshow("mask",mask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()