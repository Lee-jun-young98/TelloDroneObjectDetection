import KeyPressModule as kp
import time

kp.init()


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT") : lr = -speed
    elif kp.getKey("RIGHT") : lr = speed

    if kp.getKey("UP") : fb = speed
    elif kp.getKey("DOWN") : fb = -speed
    
    if kp.getKey("w") : ud = speed
    elif kp.getKey("s") : ud = -speed

    if kp.getKey("a") : yv = -speed
    elif kp.getKey("d") : yv = speed

    if kp.getKey("q") : print("ZZ")
    if kp.getKey("e") : print("TT")

    if kp.getKey("z") : print("Capture")

    return [lr, fb, ud, yv]    


while True:
    vals = getKeyboardInput()
    print(vals)