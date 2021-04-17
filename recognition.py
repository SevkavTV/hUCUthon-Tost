# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import random
import firebase.database as db


def get_result(buf, columns, raw_answers):
    answers = list(map(int, raw_answers.split(',')))
    sizes = list(map(int, [columns] * len(answers)))

    print(answers, sizes)

    raw_image = np.fromstring(buf, dtype=np.uint8)
    image = cv2.imdecode(raw_image, cv2.IMREAD_ANYCOLOR)
    if image.shape[0] > 1000:
        scale_percent = 1000.0 / image.shape[0]
        width = int(image.shape[1] * scale_percent)
        height = int(image.shape[0] * scale_percent)
        dim = (width, height)
        image = cv2.resize(image, dim)
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    edged = cv2.Canny(gray, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    docCnt = None
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                docCnt = approx
                break

    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))
    thresh = cv2.threshold(warped, 0, 255,
                           cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    questionCnts = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        s = cv2.contourArea(c) / (w * h)
        ar = w / float(h)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if w * h >= 100 and ar >= 0.7 and ar <= 1.3 and s >= 0.8 and s <= 1.2:
            questionCnts.append(c)
    questionCnts = contours.sort_contours(questionCnts,
                                          method="top-to-bottom")[0]
    correct = 0

    lastUnusedQuestion = 0
    for (q, size) in enumerate(sizes):
        cnts = contours.sort_contours(
            questionCnts[lastUnusedQuestion:lastUnusedQuestion + size])[0]
        lastUnusedQuestion += size
        bubbled = None
        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)
        color = (0, 0, 255)
        k = answers[q]
        if k == bubbled[1]:
            color = (0, 255, 0)
            correct += 1
        cv2.drawContours(paper, [cnts[k]], -1, color, 3)

    score = (1.0 * correct / len(answers)) * 100
    print("[INFO] score: {:.2f}%".format(score))
    cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    photo_path = './results/'
    photo_name = 'photo_' + str(random.randint(1, 1000000000)) + '.png'
    cv2.imwrite(photo_path + photo_name, paper)
    link = db.save_photo(photo_path, photo_name)
    return (link, score)
