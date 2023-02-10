from PIL import Image
import cv2
from machathon_judge import Simulator, Judge

import keyboard
import time
import matplotlib.pyplot as plt

count = 0
start = None


def run_car(simulator: Simulator):
    global count, start
    if start is None:
        start = time.monotonic()
    else:
        total = time.monotonic()
        print(count / (total - start))
        if count > 100:
            count = 0
            start = None
    count += 1
    img = simulator.get_image()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("image", img)
    cv2.waitKey(1)
    steering = 0
    if keyboard.is_pressed("a"):
        steering = 1
    elif keyboard.is_pressed("d"):
        steering = -1

    throttle = 0
    if keyboard.is_pressed("w"):
        throttle = 1
    elif keyboard.is_pressed("s"):
        throttle = -1

    simulator.move_car(throttle * 15, steering * simulator.max_steer_angle / 1.7)


if __name__ == "__main__":
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    judge = Judge(run_car)
    judge.run(send_score=True)
