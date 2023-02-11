"""
Example code using the judge module
"""
# pylint: disable=import-error
import cv2
import keyboard

from machathon_judge import Simulator, Judge

def run_car(simulator: Simulator) -> None:
    """
    Function to control the car using keyboard

    Parameters
    ----------
    simulator : Simulator
        The simulator object to control the car
        The only functions that should be used are:
        - get_image()
        - set_car_steering()
        - set_car_velocity()
        - get_state()
    """
    # Get the image and show it
    img = simulator.get_image()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("image", img)
    cv2.waitKey(1)

    # Control the car using keyboard
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

    simulator.set_car_steering(steering * simulator.max_steer_angle / 1.7)
    simulator.set_car_velocity(throttle * 25)


if __name__ == "__main__":
    # Initialize any variables needed
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)

    # You should modify the value of the parameters to the judge constructor
    # according to your team's info
    judge = Judge(team_name="TeamX", team_code=12345, code_file_paths=['test.py'])

    # Pass your main solution function to the judge
    judge.set_run_hook(run_car)

    # Start the judge and simulation
    judge.run(send_score=True)
