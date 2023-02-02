"""
Simulator class as an interface to the Coppelia remote API
"""
from typing import Tuple

import numpy as np
from .zmqRemoteApi import RemoteAPIClient

# pylint: disable=no-member


class Simulator:
    """
    Simulator class as an interface to the Coppelia remote API
    """

    def __init__(self):
        self.client = RemoteAPIClient()
        self.sim = self.client.getObject("sim")

        # Fetch ids for each of the wheels
        self.steer_handle = self.sim.getObject("/Manta/steer_joint")
        self.motor_handle = self.sim.getObject("/Manta/motor_joint")
        self.wheel_handles = [
            self.sim.getObject("/Manta/br_brake_joint"),
            self.sim.getObject("/Manta/fr_brake_joint"),
            self.sim.getObject("/Manta/bl_brake_joint"),
            self.sim.getObject("/Manta/fl_brake_joint"),
        ]

        # Car parameters
        self.max_velocity = 15
        self.max_steer_angle = 0.52  # 30 degrees
        self.motor_torque = 60

        self.steer_angle = 0
        self.motor_velocity = 0

        # Fetch id for the camera
        self.camera_handle = self.sim.getObject("/Manta/Camera")
        self.camera_resolution = 640, 480

    def start(self) -> None:
        """
        Start the simulation
        """
        self.sim.startSimulation()
        self.client.setStepping(False)

    def stop(self) -> None:
        """
        Stop the simulation
        """
        self.sim.stopSimulation()

    def move_car(self, velocity: float, steering: float) -> None:
        """
        Send a command to the car

        Parameters
        ----------
        velocity : float
            Velocity of the car in m/s
        steering : float
            Steering angle of the car in radians
        """
        steering = np.clip(steering, -self.max_steer_angle, self.max_steer_angle)

        self.sim.setJointTargetPosition(self.steer_handle, steering)
        self.steer_angle = steering

        self.motor_velocity = velocity
        if self.motor_velocity > self.max_velocity:
            self.motor_velocity = self.max_velocity
        self.sim.setJointTargetForce(self.motor_handle, self.motor_torque)
        self.sim.setJointTargetVelocity(self.motor_handle, self.motor_velocity)

    def get_image(self) -> np.ndarray:
        """
        Get the image from the camera
        Returns
        -------
        np.ndarray, shape = (640, 480, 3)
            Image from the camera
        """
        image, _ = self.sim.getVisionSensorImg(self.camera_handle)
        image = np.array(list(image), dtype=np.uint8)
        image = image.reshape((self.camera_resolution[1], self.camera_resolution[0], 3))
        image = np.flip(
            image, 1
        )  # Image is reflected along the x-axis (width), so unreflected it
        return image

    def get_state(self) -> Tuple[float, float]:
        """
        Gets the current state of the car

        Returns
        -------
        current_steering : float
            Current steering angle of the car in radians
        linear_velocity : float
            Current linear velocity of the car in m/s
        """
        current_steering = self.sim.getJointPosition(self.steer_handle)

        bl_wheel_velocity = self.sim.getObjectFloatParam(
            self.wheel_handles[2], self.sim.jointfloatparam_velocity
        )
        br_wheel_velocity = self.sim.getObjectFloatParam(
            self.wheel_handles[0], self.sim.jointfloatparam_velocity
        )
        rear_wheel_velocity = (bl_wheel_velocity + br_wheel_velocity) / 2
        linear_velocity = rear_wheel_velocity * 0.09
        return current_steering, linear_velocity
