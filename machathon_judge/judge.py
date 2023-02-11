import time
import random
import requests
from .simulator import Simulator

from .data import Data

TEAM_CODE = 101010
TEAM_NAME = 'TEAMX'

class Judge:
    def __init__(self, hook_img):
        self.hook = hook_img
        self.data = Data()
        self.track_starting_position = None
        self.track_starting_orientation = None

    def publish_score(self, forward_laptime: float, backward_laptime: float, verbose=True) -> None:
        """
        Send the current submission score to the compeition's leaderboard.
        Parameters
        ----------
        forward_laptime : float
            Time taken by the vehicle to finish the track by moving in the track's forward direction.
        backward_laptime : float
            Time taken by the vehicle to finish the track by moving in the track's backward direction.
        verbose : boolean  
            Flag to print messages about the submission status. default True.
        """
        
        # data = {
        #     'team_7digit_code': TEAM_CODE,
        #     'solution_code': None,
        #     'team_name': TEAM_NAME,
        #     'forward_laptime': str(forward_laptime),
        #     'backward_laptime': str(backward_laptime)
        # }

        data = {
            'code': TEAM_CODE,
            'score': str(forward_laptime) + '_' + str(backward_laptime)
        }

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}

        # sending post request to STP's leaderboard
        response = requests.post(url = self.data.LEADERBOARD_ENDPOINT, data = data, headers = headers)

        # extracting response status code 
        if(verbose):
            if response.status_code == 200 :
                print("Your score have been published on the leaderboard successfully!")
            else:
                print("Something went wrong while sending your score... \nPlease check your internet connection or contact the technical organizers.")

    def run_track(self, simulator: Simulator) -> float:
        """
        This function runs the competitor's code and calculates the lap time taken to complete a single lap of the track.
        A lap is considered completed when the vehicle crosses the starting checkpoint twice.

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

        while (time.monotonic() - tic) < self.data.TIMEOUT_DURATION:
            # calculate the start and finish time whenever the vehicle crosses the starting checkpoint
            if(simulator.is_collision(next_ckpt_id)):
                if(start_time == 0):
                    start_time = time.monotonic()
                elif next_ckpt_id==0:
                    finish_time = time.monotonic()
                    break
                # switch between the starting checkpoint and the middle-track checkpoint
                next_ckpt_id = 1 - next_ckpt_id
            
            # Calling the competitior's code
            self.hook(simulator)

        # return the time taken to complete 1 lap through the track
        return finish_time-start_time

    def run(self, send_score: bool=True, verbose: bool=True) -> None:
        """
        This function calls the competitor's code twice. It then caluclates the laptime taken for each run
        and, if specified, publishes the laptime to the leaderboard.

        Parameters
        ----------
        send_score : bool, optional
            Determine whether send the score to the leaderboard, default is True.
        verbose: bool, optional
            Flag to print messages about the lap time values, default is True.
        """
        simulator = Simulator()

        simulator.start()
        
        # Randomly choosing which direction of the track to start the navigation with
        # Your code should run autonomously given any track
        # This is why the process of choosing the starting direction of the track is done randomly,
        # so you don't control flow your code on a specific track.
        track_id = random.randint(0,1)
        self.track_starting_orientation = self.data.FTRACK_STARTING_ORIENTATION if track_id == self.data.FORWARD_TRACK else self.data.BTRACK_STARTING_ORIENTATION
        self.track_starting_position = self.data.FTRACK_STARTING_POSITION if track_id == self.data.FORWARD_TRACK else self.data.BTRACK_STARTING_POSITION            
        
        # position the car at the start of the track
        simulator.reset_car_pose(self.track_starting_position, self.track_starting_orientation)

        # execute the competitor's code on the track first direction
        lap_time1 = self.run_track(simulator)
        # re-position the car to start the track with the opposite direction
        self.track_starting_orientation = self.data.BTRACK_STARTING_ORIENTATION if track_id == self.data.FORWARD_TRACK else self.data.FTRACK_STARTING_ORIENTATION
        self.track_starting_position = self.data.BTRACK_STARTING_POSITION if track_id == self.data.FORWARD_TRACK else self.data.FTRACK_STARTING_POSITION
        simulator.reset_car_pose(self.track_starting_position, self.track_starting_orientation)

        # execute the competitor's code on the track's opposite direction
        lap_time2 = self.run_track(simulator)

        # publish the laptime of the 2 runs to the leaderboard
        forward_laptime, backward_laptime = (lap_time1, lap_time2) if track_id == self.data.FORWARD_TRACK else (lap_time2, lap_time1)
        
        if verbose:
            print("Time taken to finish the track starting from its forward orientation: ", forward_laptime)
            print("Time taken to finish the track starting from its backward orientation: ", backward_laptime)
        
        if send_score:
            self.publish_score(forward_laptime, backward_laptime, verbose)
    
        simulator.stop()
