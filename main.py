import cv2
import numpy as np

def biggets_countour(countours):
    bigget = np.array([])
    max_area = 0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            peri = cv2.arcLength(cnt, closed=True)
            approx = cv2.approxPolyDP(cnt, 0.015*peri, closed=True)
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
    big = biggets_countour(countours=countours)

    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class Scanner:
    def __init__(self, path):
        self.original = cv2.imread(path)
        self.scan()
        self.display()

    def biggets_countour(self,countours):
        bigget = np.array([])
        max_area = 0
        for cnt in countours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                peri = cv2.arcLength(cnt, closed=True)
                approx = cv2.approxPolyDP(cnt, 0.015*peri, closed=True)
            if area > max_area and len(approx) == 4:
                max_area = area
                bigget = approx
        return bigget
    def display(self):
        cv2.imshow('',self.output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def scan(self):
        gray = cv2.cvtColor(self.original,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        canny = cv2.Canny(blur,50,250)
        conturs, _ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        conturs = sorted(conturs,key=cv2.contourArea,reverse=True)[:10]
        big = self.biggets_countour(countours=conturs)
        points = big.reshape(4,2)
        input_arr = np.zeros((4,2),dtype="float32")
        spoints = points.sum(axis = 1)
        input_arr[0] = points[np.argmin(spoints)]
        input_arr[3] = points[np.argmax(spoints)]
        dpoints = np.diff(points,axis=1)
        input_arr[1] = points[np.argmin(dpoints)]
        input_arr[2] = points[np.argmax(dpoints)]
        (tl,tr,bl,br) = input_arr
        b_width = np.sqrt(((br[0]-bl[0]) ** 2) + ((br[1]-bl[1])**2))
        t_width = np.sqrt(((tr[0]-tl[0]) ** 2) + ((tr[1]-tl[1])**2))
        r_height = np.sqrt(((tr[0]-br[0]) ** 2) + ((tr[1]-br[1])**2))
        l_height = np.sqrt(((tl[0]-bl[0]) ** 2) + ((tl[1]-bl[1])**2))
        mwidth = max(int(b_width),int(t_width))
        mheight = max(int(r_height),int(l_height))
        converted_paints = np.float32([[0,0],[mwidth,0],[0,mheight],[mwidth,mheight]])
        matrix = cv2.getPerspectiveTransform(input_arr,converted_paints)
        self.output = cv2.warpPerspective(self.original,matrix,(mwidth,mheight))
        


if __name__ == '__main__':
    s = Scanner("2.jpg")
    
