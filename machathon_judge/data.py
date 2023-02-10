from dataclasses import dataclass
import math

@dataclass
class Data:
    LEADERBOARD_ENDPOINT = 'https://stp-org.com/stp23/leader_board/back-end/saveData.php'
    
    FORWARD_TRACK = 0
    BACKWARD_TRACK = 1

    FTRACK_STARTING_POSITION = [-1, -1, 0.2]
    FTRACK_STARTING_ORIENTATION = [0, 0, 0]

    BTRACK_STARTING_POSITION = [1.5, 1, 0.2]
    BTRACK_STARTING_ORIENTATION = [0, 0, math.pi]

    TIMEOUT_DURATION = 1000
