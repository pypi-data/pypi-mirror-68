import cv2


class Webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def shot(self):
        ret, frame = self.cap.read()
        # print(cv2.imencode('png', frame))
        res, arr = cv2.imencode('.jpg', frame)
        return arr

    def close(self):
        self.cap.release()



def check_webcam_permissions():
    w = Webcam()
    w.shot()
    w.close()

