import serial
from cvzone.HandTrackingModule import HandDetector
import cv2

port = "/dev/ttyACM0"
baud = 115200
ser = serial.Serial(port,baud)
ser.flushInput()

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.5, maxHands=1)
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)
        
        fingers_list = (list(map(int,fingers1)))
        count = 0
        for i in fingers_list:
            count = count+i
        print(count)
        ser.write(str(count).encode())
        ser.write("\n".encode())


    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
