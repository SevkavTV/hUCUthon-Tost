# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def aaaa(buf):
    aa = np.fromstring(
        buf, dtype=np.uint8)
    print(aa)
    image = cv2.imdecode(aa, cv2.IMREAD_ANYCOLOR)
    if image.shape[0] > 1000:
        scale_percent = 1000.0 / image.shape[0]
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)
        image = cv2.resize(image, dim)
    print(image.shape[1], image.shape[0])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cv2.imshow("Blured", edged)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print(len(cnts))
    docCnt = None
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                print("find")
                docCnt = approx
                break

    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))

    thresh = cv2.threshold(warped, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cv2.imshow("thresh", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    questionCnts = []

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if w * h >= 100 and ar >= 0.7 and ar <= 1.3 and len(approx) == 4:
            questionCnts.append(c)

    for c in questionCnts:
        color = (0, 0, 255)
        cv2.drawContours(paper, [c], -1, color, 3)
    cv2.imshow("Final", paper)
    cv2.waitKey(0)
