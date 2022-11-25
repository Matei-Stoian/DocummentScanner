import cv2
import numpy as np

def biggets_countour(countours):
    bigget = np.array([])
    max_area = 0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            peri = cv2.arcLength(cnt,closed=True)
            approx = cv2.approxPolyDP(cnt,0.015*peri,closed=True)
            if area > max_area and len(approx) == 4:
                max_area = area
                bigget = approx
    return bigget
def main():
    img = cv2.imread("1.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    img_canny = cv2.Canny(img_blur, 50, 250)
    countours, _ = cv2.findContours(
        img_canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    countours = sorted(countours, key=cv2.contourArea, reverse=True)[:10]
    big = biggets_countour(countours)
    cv2.drawContours(img,[big],-1,(0,255,0),4)
    cv2.imshow('',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
