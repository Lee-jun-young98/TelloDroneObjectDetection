import cv2
import cvzone
from djitellopy import tello
import KeyPressModule as kp
import time

threshold = 0.6
nmsThreshold = 0.2

# cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)

classNames = []
classFile = 'Resources/coco.names'

with open(classFile, 'rt') as f:
    classNames = f.read().split("\n")
print(classNames)

configPath = 'Resources/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'Resources/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5,127.5,127.5))
net.setInputSwapRB(True)


# drone

kp.init()

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

global img
drone.streamon()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("RIGHT") : lr = speed
    elif kp.getKey("LEFT") : lr = -speed

    if kp.getKey("UP") : fb = speed
    elif kp.getKey("DOWN") : fb = -speed
    
    if kp.getKey("w") : ud = speed
    elif kp.getKey("s") : ud = -speed

    if kp.getKey("a") : yv = -speed
    elif kp.getKey("d") : yv = speed

    if kp.getKey("q") :
        drone.land()
        time.sleep(3)
  
    if kp.getKey("e") : drone.takeoff()

    if kp.getKey("z") :
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    # success, img = cap.read()
    img = drone.get_frame_read().frame
    classIds, confs, boundbox = net.detect(img, confThreshold = threshold, nmsThreshold = nmsThreshold)

    try:
        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), boundbox):
            print(classId, conf, box)
            cvzone.cornerRect(img, box) # can add  rt = 0
            cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf*100,2)}',
                        (box[0]+10, box[1]+30),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0),2)
    except:
        pass
    cv2.imshow("Image",img)
    cv2.waitKey(1)