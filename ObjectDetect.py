# -*- coding: utf-8 -*-
import cv2
import numpy as np
import unittest2 as unittest
from matplotlib import pyplot as plt
import ColorDetect

def Show(image, title = [], key=0):
    cv2.destroyAllWindows()
    cnt = len(image)
    for k in range(cnt):
        string = ''
        if len(title) < k + 1:
            string = 'image' + str(k)
        else:
            string = title[k]
        cv2.imshow(string, image[k])
    cv2.waitKey(key)

def CropImageFromSquareData(canvas, squareContourData):
    '''
    minx = 99999
    miny = 99999
    maxx = 0
    maxy = 0
    for i in squareContourData:
        x, y = i.ravel()
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        if x > maxx :
            maxx = x
        if y > maxy :
            maxy = y
    w = maxx - minx
    h = maxy - miny
    croppedImage = canvas[miny:maxy, minx:maxx]
    return croppedImage
    '''
    topLeft = squareContourData[0][0]
    topRight = squareContourData[3][0]
    bottomRight = squareContourData[2][0]
    bottomLeft = squareContourData[1][0]

    pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

    w1 = abs(bottomRight[0] - bottomLeft[0])
    w2 = abs(topRight[0] - topLeft[0])
    h1 = abs(topRight[1] - bottomRight[1])
    h2 = abs(topLeft[1] - bottomLeft[1])
    minWidth = min([w1, w2])
    minHeight = min([h1, h2])

    pts2 = np.float32([[0,0], [minWidth-1,0],
                      [minWidth-1,minHeight-1], [0,minHeight-1]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    result = cv2.warpPerspective(canvas, M, (int(minWidth), int(minHeight)))
    return result

def GrayImage(before,after):
    #before :  Resources/testcase5/before.JPG
    #after : Resources/testcase5/after.JPG

    MORPHOLOGY_MASK_SIZE = 5
    BLUR_MASK_SIZE = 1
    EACH_IMAGE_DIFFERENCE_THRESHOLD = 30
    SET_IMAGE_WHITE_COLOR = 255
    NEIGHBORHOOD_MASK_SIZE = 7
    CANNY_MINIMUM_THRESHOLD = 0
    CANNY_MAXIMUM_THRESHOLD = 255
    GET_MAXIMUM_AREA_SIZE = 5
    SQUARE_CORNER_NUM = 4
    IMAGE_WIDTH = 294.0

    lineImage = before
    # Line detect image

    grayImage = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    # Change color to gray

    kernel = np.ones((MORPHOLOGY_MASK_SIZE, MORPHOLOGY_MASK_SIZE), np.uint8)
    grayImage = cv2.morphologyEx(grayImage, cv2.MORPH_OPEN, kernel)
    # Reduce image noise

    '''
    splitImage = []
    splitImage = cv2.split(beforeGray)

    for color in splitImage:
        color = cv2.GaussianBlur(color, (3,3), 0)
        color = cv2.adaptiveThreshold(color, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 10)
        _, c, h = cv2.findContours(color, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for count in c:
            approx = cv2.approxPolyDP(count, 0.1 * cv2.arcLength(count, True), True)
            if len(approx) == 5 :
                print "pentagon"
                cv2.drawContours(lineImage, [count], 0, (255, 0, 0), -1)
            elif len(approx) == 3 :
                print "triangle"
                cv2.drawContours(lineImage, [count], 0, (0, 255, 0), -1)
            elif len(approx) == 4 :
                print approx
                cv2.drawContours(lineImage, [count], 0, (0, 0, 255), -1)  # square
                for i in approx:
                    x, y = i.ravel()
                    cv2.circle(lineImage, (x, y), 1, (0, 255, 0), -1)
    '''

    #blurImage = cv2.GaussianBlur(beforeGray, (BLUR_MASK_SIZE, BLUR_MASK_SIZE), 0)
    # Reduce image noise, 0 : border type (idk)

    blurImage = cv2.adaptiveThreshold(grayImage, SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, NEIGHBORHOOD_MASK_SIZE, 10)
    # Get small size of block's threshold value

    edges = cv2.Canny(blurImage, CANNY_MINIMUM_THRESHOLD, CANNY_MAXIMUM_THRESHOLD, apertureSize = 5)
    cv2.imwrite("cannyEdgeDetectedImage.jpg", edges)
    # Edge detect from bulr processed image
    (_, contours, h) = cv2.findContours(blurImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Get image contour

    foundedMaxAreaSizeContours = sorted(contours, key=cv2.contourArea, reverse=True)[:GET_MAXIMUM_AREA_SIZE]

    squareContourData = []

    for indexOfContour in foundedMaxAreaSizeContours:
        peri = cv2.arcLength(indexOfContour, True)
        approx = cv2.approxPolyDP(indexOfContour, 0.02 * peri, True)

        if len(approx) == SQUARE_CORNER_NUM:
            squareContourData = approx
            print "contour data"
            print squareContourData
            break

    beforeBack = before[:]

    #cv2.drawContours(beforeBack, [squareContourData], 0, 255, -1)
    #cv2.drawContours(before, squareContourData, 0, (0, 255, 0), 2)
    croppedBefore = CropImageFromSquareData(before, squareContourData)
    croppedAfter = CropImageFromSquareData(after, squareContourData)

    height, width = croppedBefore.shape[:2]
    rate = IMAGE_WIDTH / width
    resizeBefore = cv2.resize(croppedBefore, (int(IMAGE_WIDTH),int(rate * height)))
    height, width = croppedAfter.shape[:2]
    rate = IMAGE_WIDTH / width
    resizeAfter = cv2.resize(croppedAfter, (int(IMAGE_WIDTH),int(rate * height)))
    # Resize Image

    beforeGray = resizeBefore
    afterGray = resizeAfter
    beforeGray = cv2.cvtColor(resizeBefore, cv2.COLOR_BGR2GRAY)
    afterGray = cv2.cvtColor(resizeAfter, cv2.COLOR_BGR2GRAY)
    # Change color to gray

    kernel = np.ones((MORPHOLOGY_MASK_SIZE + 1, MORPHOLOGY_MASK_SIZE + 1), np.uint8)
    beforeGray = cv2.morphologyEx(beforeGray, cv2.MORPH_OPEN, kernel)
    afterGray = cv2.morphologyEx(afterGray, cv2.MORPH_OPEN, kernel)
    # Reduce image noise

    Show([beforeGray,afterGray], ['before','after'])

    difference = cv2.absdiff(beforeGray, afterGray)
    difference[difference > EACH_IMAGE_DIFFERENCE_THRESHOLD] = SET_IMAGE_WHITE_COLOR
    # Detect each image difference

    Show([resizeBefore, resizeAfter, difference], ['before','after','difference'])

    for count in contours:
        approx = cv2.approxPolyDP(count, 0.1 * cv2.arcLength(count, True), True)
        if len(approx) == 5 :
            # find pentagon
            cv2.drawContours(lineImage, [count], 0, (255, 0, 0), -1)
        elif len(approx) == 3 :
            # find triangle
            cv2.drawContours(lineImage, [count], 0, (0, 255, 0), -1)
        elif len(approx) == 4 :
            # find square
            cv2.drawContours(lineImage, [count], 0, (0, 0, 255), -1)  # square
            for i in approx:
                x, y = i.ravel()
                cv2.circle(lineImage, (x, y), 1, (0, 255, 0), -1)

    #Show([lineImage])
    return  resizeBefore, resizeAfter, difference

def DetectObjectFromImage(testcase):
    beforeImage = cv2.imread(testcase + "before.jpg")

    afterImage = cv2.imread(testcase + "after.jpg")

    mask = ColorDetect.ColorDetectFromImage(testcase + "before.jpg")

    # plt.imshow(afterGrayImage)

    GrayImage(beforeImage, afterImage)

    differenceBetweenLoadedImages = cv2.absdiff(beforeImage, afterImage)

    diff = afterImage - beforeImage

    differenceBetweenLoadedImages[differenceBetweenLoadedImages > 40] = 255

    differenceBetweenLoadedImages = cv2.cvtColor(differenceBetweenLoadedImages, cv2.COLOR_BGR2GRAY)

    last_result = differenceBetweenLoadedImages - mask

    cv2.imwrite((testcase + "result_absdiff.jpg"), differenceBetweenLoadedImages)

    cv2.imwrite((testcase + "result_mask.jpg"), mask)

    cv2.imwrite((testcase + "result_diff2.jpg"), last_result)

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

    cv2.drawContours(beforeImage, contours, 0, 255, 3)

    (positionX, positionY, width, height) = cv2.boundingRect(maxContoursIndex)

    cv2.rectangle(beforeImage, (positionX, positionY), (positionX + width, positionY + height), 255, 2)

    # cv2.imwrite("Resources/testcase2/result.jpg", beforeGrayImage)