# -*- coding: utf_8 -*-

import cv2
import cv
import numpy as np
from matplotlib import pyplot as plt

# пример для захвата камер и опт.потока и глупого построения disparity map.

cv.NamedWindow("Camera 1")
cv.NamedWindow("Camera 2")
cv.NamedWindow("Opt")

# еще нужно fps установить. ато при большем разрещении буфер переполняется.
video1 = cv.CaptureFromCAM(1)
cv.SetCaptureProperty(video1, cv.CV_CAP_PROP_FRAME_WIDTH, 352)
cv.SetCaptureProperty(video1, cv.CV_CAP_PROP_FRAME_HEIGHT, 288)

video2 = cv.CaptureFromCAM(2)
cv.SetCaptureProperty(video2, cv.CV_CAP_PROP_FRAME_WIDTH, 352)
cv.SetCaptureProperty(video2, cv.CV_CAP_PROP_FRAME_HEIGHT, 288)

# вместо второй строчки метода нужно триангулировать.
# если бы камеры были идеально на одной прямой, то мы имели бы 
# правильную карту сдвигов (сейчас не правильная, но показательная), а для нее триангуляция простая
# но имеем кучу ошибок + камеры не получается ровно поставить.
# так что честная триангуляция. нужны матрицы камер. 
def disparity_map(img1, img2):
    flow = cv2.calcOpticalFlowFarneback(img1, img2, 0.5, 3, 20, 10, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    return mag

while (True):
    frame1 = cv.QueryFrame(video2)
    gray1 = cv.CreateImage(cv.GetSize(frame1), frame1.depth, 1)
    cv.CvtColor(frame1, gray1, cv.CV_RGB2GRAY)
    mat1 = cv.GetMat(gray1)
    frame2 = cv.QueryFrame(video1)
    gray2 = cv.CreateImage(cv.GetSize(frame2), frame2.depth, 1)
    cv.CvtColor(frame2, gray2, cv.CV_RGB2GRAY)
    mat2 = cv.GetMat(gray2)
    optflow = disparity_map(np.asarray(mat1), np.asarray(mat2))
    
    cv.ShowImage("Camera 1", frame1)
    cv.ShowImage("Camera 2", frame2)
    cv.ShowImage("Opt", cv.fromarray(optflow))
    
    char = cv.WaitKey(100)
    
    

cv.DestroyWindow("Camera 1")
cv.DestroyWindow("Camera 2")
cv.DestroyWindow("Opt")

