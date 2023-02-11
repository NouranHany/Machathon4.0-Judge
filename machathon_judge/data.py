from dataclasses import dataclass
import math

@dataclass
class Data:
    LEADERBOARD_ENDPOINT = 'https://stp-org.com/stp23/leader_board/back-end/saveData.php'
    
    FORWARD_TRACK = 0
    BACKWARD_TRACK = 1

    FTRACK_STARTING_POSITION = [3.75, 30,2, -13.9]
    FTRACK_STARTING_ORIENTATION = [0, 0, -165*math.pi/180]

    BTRACK_STARTING_POSITION = [3.75, 30,2, -13.9]
    BTRACK_STARTING_ORIENTATION = [0, 0, 15*math.pi/180]

    TIMEOUT_DURATION = 900 # 15 minutes
