import time
import requests
from .simulator import Simulator
import random

TIMEOUT_DURATION = 1000
TEAM_CODE = 101010
LEADERBOARD_ENDPOINT = 'https://stp-org.com/stp23/leader_board/back-end/saveData.php'
FORWARD = 0
BACKWARD = 1

class Judge:
    def __init__(self, hook_img):
        self.hook = hook_img

    def publish_score(self, forward_laptime, backward_laptime, verbose=True):
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
        
        data = {
            'code': TEAM_CODE,
            'score': str(forward_laptime) + '_' + str(backward_laptime)
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}

        # sending post request to STP's leaderboard
        response = requests.post(url = LEADERBOARD_ENDPOINT, data = data, headers = headers)

        # extracting response status code 
        if(verbose):
            if response.status_code == 200 :
                print("Your score have been published on the leaderboard successfully!")
            else:
                print("Something went wrong while sending your score... \nPlease check your internet connection or contact the technical organizers.")

    def run_track(self, simulator):
        next_ckpt_id = 0
        tic = time.monotonic()
        start_time = 0

        while (time.monotonic() - tic) < TIMEOUT_DURATION:
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
            #self.hook(simulator)

        # return the time taken to complete 1 lap through the track
        return finish_time-start_time

    def run(self):
        simulator = Simulator()

        simulator.start()
        
        # choosing the orientation of the track randomly
        # your code should run autonomously, either by starting the track from its forward or backward direction
        track_orientation = random.randint(0,1)
        
        # position the car at the start of the track
        # lap_time1 = self.run_track(simulator)
        
        # re-position the car to start the track with the opposite direction
        # lap_time2 = self.run_track(simulator)

        # publish the score of the 2 runs to the leaderboard
        # self.publish_score(lap_time1, lap_time2)
        
        simulator.stop()
