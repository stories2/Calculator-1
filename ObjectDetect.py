import cv2
import numpy as np
import unittest2 as unittest
from matplotlib import pyplot as plt
import ColorDetect

def Show(image,key=0):
    cnt = len(image)
    print cnt
    for k in range(cnt):
        string = 'image' + str(k)
        cv2.imshow(string, image[k])
    cv2.waitKey(key)

def DetectObjectFromImage(beforeImage, afterImage):
    beforeGrayImage = cv2.imread(beforeImage, 0)
    # beforeGrayImage = cv2.cvtColor(beforeImage, cv2.COLOR_BGR2GRAY)

    afterGrayImage = cv2.imread(afterImage, 0)
    # afterGrayImage = cv2.cvtColor(afterImage, cv2.COLOR_BGR2GRAY)

    mask = ColorDetect.ColorDetectFromImage(beforeImage)

    # plt.imshow(afterGrayImage)

    kernel = np.ones((7, 7), np.uint8)
    beforeGrayImage = cv2.morphologyEx(beforeGrayImage,cv2.MORPH_OPEN,kernel)
    afterGrayImage = cv2.morphologyEx(afterGrayImage,cv2.MORPH_OPEN,kernel)
    Show([beforeGrayImage,afterGrayImage])

    differenceBetweenLoadedImages = cv2.absdiff(beforeGrayImage, afterGrayImage)

    differenceBetweenLoadedImages[differenceBetweenLoadedImages > 30] = 255

    cv2.imwrite("Resources/testcase5/result_absdiff.jpg", differenceBetweenLoadedImages)

    blurKernel = cv2.GaussianBlur(differenceBetweenLoadedImages, (3, 3), 0)

    differenceBetweenLoadedImages = cv2.adaptiveThreshold(differenceBetweenLoadedImages, 255,
                                                          cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 10)

    imageEdgesDetected = cv2.Canny(differenceBetweenLoadedImages, 0, 255)

    _, contours, hierarchy = cv2.findContours(imageEdgesDetected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    maxContoursArea = 0
    calculatedContourArea = 0
    maxContoursIndex = []
    for contoursIndex in contours:
        calculatedContourArea = cv2.contourArea(contoursIndex)
        if maxContoursArea < calculatedContourArea:
            maxContoursArea = calculatedContourArea
            maxContoursIndex = contoursIndex

    cv2.drawContours(beforeGrayImage, contours, 0, 255, 3)

    (positionX, positionY, width, height) = cv2.boundingRect(maxContoursIndex)

    cv2.rectangle(beforeGrayImage, (positionX, positionY), (positionX + width, positionY + height), 255, 2)

    cv2.imwrite("Resources/testcase5/result_canny.jpg", imageEdgesDetected)
    # cv2.imwrite("Resources/testcase2/result.jpg", beforeGrayImage)

def Detecting():
    beforeGrayImage = cv2.imread('Resources/testcase5/before.jpg', 0)
    #beforeGrayImage = cv2.cvtColor(beforeImage, cv2.COLOR_BGR2GRAY)

    afterGrayImage = cv2.imread('Resources/testcase5/after.jpg', 0)
    #afterGrayImage = cv2.cvtColor(afterImage, cv2.COLOR_BGR2GRAY)

    #plt.imshow(afterGrayImage)

    differenceBetweenLoadedImages = cv2.absdiff(beforeGrayImage, afterGrayImage)

    differenceBetweenLoadedImages[differenceBetweenLoadedImages > 30] = 255

    cv2.imwrite("Resources/testcase5/result_absdiff.jpg", differenceBetweenLoadedImages)

    blurKernel = cv2.GaussianBlur(differenceBetweenLoadedImages, (3, 3), 0)

    differenceBetweenLoadedImages = cv2.adaptiveThreshold(differenceBetweenLoadedImages, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 10)

    imageEdgesDetected = cv2.Canny(differenceBetweenLoadedImages, 0, 255)

    _, contours, hierarchy = cv2.findContours(imageEdgesDetected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    maxContoursArea = 0
    calculatedContourArea = 0
    maxContoursIndex = []
    for contoursIndex in contours:
        calculatedContourArea = cv2.contourArea(contoursIndex)
        if maxContoursArea < calculatedContourArea:
            maxContoursArea = calculatedContourArea
            maxContoursIndex = contoursIndex

    cv2.drawContours(beforeGrayImage, contours, 0, 255, 3)

    (positionX, positionY, width, height) = cv2.boundingRect(maxContoursIndex)

    cv2.rectangle(beforeGrayImage, (positionX, positionY), (positionX + width, positionY + height), 255, 2)


    cv2.imwrite("Resources/testcase5/result_canny.jpg", imageEdgesDetected)
    #cv2.imwrite("Resources/testcase2/result.jpg", beforeGrayImage)