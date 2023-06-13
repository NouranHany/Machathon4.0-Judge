"""
Module containing the Judge class to run the competition's tracks and
publish the scores to the leaderboard
"""
import time
import random
from typing import Callable, List

# pylint: disable=import-error
import requests
from requests.exceptions import ConnectionError
from .data import Data
from .simulator import Simulator
from .collision_manager import CollisionManager


class Judge:
    """
    Class to run the competition's tracks and publish the scores to the leaderboard

    Parameters
    ----------
    team_code: string
        The new 9-digit team code
    zip_file_path: string
        Path to a zip file containing all your code files that represent your solution. e.g. "mysolution.zip"
    """

    def __init__(self, team_code: str, zip_file_path: str):
        self.data = Data()
        self.team_code = team_code
        self.zip_file_path = zip_file_path
        self.track_starting_position = None
        self.track_starting_orientation = None
        self.simulator = None
        self.collision_manager = None
        self.hook = None

    def set_run_hook(self, hook_func: Callable) -> None:
        """
        Set a hook function.
        Parameters
        ----------
        hook_func: Callable
            A function to be called each time step of the simulation
            This is the function provided by the competitors that represents their solution.
        """
        self.hook = hook_func

    def clean_up(self) -> None:
        """
        Closes the simulator and collision manager object.
        """
        if self.collision_manager is not None:
            self.collision_manager.close()

        if self.simulator is not None:
            self.simulator.stop()

    def publish_score(
        self, forward_laptime: float, backward_laptime: float, verbose: bool = True
    ) -> None:
        """
        Send the current submission score to the competition's leaderboard

        Parameters
        ----------
        forward_laptime : float
            Time taken to finish the track by moving in the track's forward direction.
        backward_laptime : float
            Time taken to finish the track by moving in the track's backward direction.
        verbose : boolean, default True
            Flag to print messages about the submission status.
        """

        file = [("solution_code", open(self.zip_file_path, "rb"))]

        data = {
            "team_9digit_code": self.team_code,
            "forward_laptime": forward_laptime,
            "backward_laptime": backward_laptime,
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; \
                            rv:55.0) Gecko/20100101 Firefox/55.0"
        }

        # sending post request to STP's leaderboard
        response = requests.post(
            url=self.data.LEADERBOARD_ENDPOINT,
            files=file,
            data=data,
            headers=headers,
            timeout=1000,
        )

        # extracting response status code
        if verbose:
            if response.status_code == 200:
                print("Your score has been published on the leaderboard successfully!")
            else:
                print("Submission Failure, ", response.text)

    def run_track(self, simulator: Simulator) -> float:
        """
        This function runs the competitor's code and calculates the lap time taken to complete
        a single lap of the track. A lap is considered completed when the vehicle crosses the
        starting checkpoint twice.

        Parameters:
        ----------
        simulator: Simulator
            The simulation environment object.
            Refer to the rule book to see which functions you're allowed to use on this object.

        Returns:
        -------
        float
            The lap time taken to complete a single lap of the track in seconds.
        """
        next_ckpt_id = 0
        tic = time.monotonic()
        start_time = 0

        self.collision_manager = CollisionManager()

        while (time.monotonic() - tic) < self.data.TIMEOUT_DURATION:
            # calculate the start and finish time when the vehicle crosses the starting checkpoint
            if self.collision_manager.ckpts_collided[next_ckpt_id]:
                if start_time == 0:
                    start_time = time.monotonic()
                elif next_ckpt_id == 0:
                    finish_time = time.monotonic()
                    self.collision_manager.close()

                    # return the time taken to complete 1 lap through the track
                    return finish_time - start_time
                # switch between the starting checkpoint and the middle-track checkpoint
                next_ckpt_id = 1 - next_ckpt_id
            # Calling the competitior's code
            self.hook(simulator)

        self.clean_up()
        raise TimeoutError("Simulation timeout exceeded!")

    def run_unsafe(self, send_score: bool = True, verbose: bool = True) -> None:
        """
        This function calls the competitor's code twice. It then caluclates the laptime taken
        for each run and, if specified, publishes the laptime to the leaderboard.

        Parameters
        ----------
        send_score : bool, optional
            Determine whether send the score to the leaderboard, default is True.
        verbose: bool, optional
            Flag to print messages about the lap time values, default is True.
        """
        self.simulator = Simulator()

        self.simulator.stop()
        time.sleep(0.5)  # Ensure the simulator has stopped
        self.simulator.start()
        time.sleep(2)  # Ensure the websockets have started

        # Randomly choosing which direction of the track to start the navigation with
        # Your code should run autonomously given any track
        # This is why the process of choosing the starting direction of the track is done randomly,
        # so you don't control flow your code on a specific track.
        track_id = random.randint(0, 1)
        self.track_starting_orientation = (
            self.data.FTRACK_STARTING_ORIENTATION
            if track_id == self.data.FORWARD_TRACK
            else self.data.BTRACK_STARTING_ORIENTATION
        )
        self.track_starting_position = (
            self.data.FTRACK_STARTING_POSITION
            if track_id == self.data.FORWARD_TRACK
            else self.data.BTRACK_STARTING_POSITION
        )

        # position the car at the start of the track
        self.simulator.reset_car_pose(
            self.track_starting_position, self.track_starting_orientation
        )

        # execute the competitor's code on the track first direction
        lap_time1 = self.run_track(self.simulator)
        # re-position the car to start the track with the opposite direction
        self.track_starting_orientation = (
            self.data.BTRACK_STARTING_ORIENTATION
            if track_id == self.data.FORWARD_TRACK
            else self.data.FTRACK_STARTING_ORIENTATION
        )
        self.track_starting_position = (
            self.data.BTRACK_STARTING_POSITION
            if track_id == self.data.FORWARD_TRACK
            else self.data.FTRACK_STARTING_POSITION
        )
        self.simulator.reset_car_pose(
            self.track_starting_position, self.track_starting_orientation
        )

        # execute the competitor's code on the track's opposite direction
        lap_time2 = self.run_track(self.simulator)

        # publish the laptime of the 2 runs to the leaderboard
        forward_laptime, backward_laptime = (
            (lap_time1, lap_time2)
            if track_id == self.data.FORWARD_TRACK
            else (lap_time2, lap_time1)
        )

        if verbose:
            print(
                "Time taken to finish the track starting from its forward orientation: ",
                forward_laptime,
            )
            print(
                "Time taken to finish the track starting from its backward orientation: ",
                backward_laptime,
            )

        if send_score:
            self.publish_score(forward_laptime, backward_laptime, verbose)

        self.simulator.stop()

    def run(self, send_score: bool = True, verbose: bool = True) -> None:
        """
        This function is a wrapper for the run_unsafe function

        Parameters
        ----------
        send_score : bool, optional
            Determine whether send the score to the leaderboard, default is True.
        verbose: bool, optional
            Flag to print messages about the lap time values, default is True.
        """
        # The following try-except block handles any keyboard interruptions
        # that occur during the run, such as pressing "ctrl+c" in the terminal.
        # It closes any opened collision manager and simulator objects.
        try:
            self.run_unsafe(send_score, verbose)
        except KeyboardInterrupt:
            print(
                "The program has received a keyboard interrupt. Shutting down safely...."
            )
            self.clean_up()
        except ConnectionError:
            print(
                "Something went wrong! \nYour score hasn't been submitted, please check your internet connection."
            )
            self.clean_up()
