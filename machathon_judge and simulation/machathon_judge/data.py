"""
Module containing the Data class to store all the data required for judge to run the simulation
"""
from dataclasses import dataclass
import math


@dataclass
class Data:
    """
    Contains all the data required for judge to run the simulation
    """

    LEADERBOARD_ENDPOINT = (
        "https://stp-org.com/stp23/leader_board/back-end/saveData.php"
    )

    FORWARD_TRACK = 0
    BACKWARD_TRACK = 1

    FTRACK_STARTING_POSITION = [2.25, 33.5, -13.5]
    FTRACK_STARTING_ORIENTATION = [0, 0, -150 * math.pi / 180]

    BTRACK_STARTING_POSITION = [3.5, 31, -13.5]
    BTRACK_STARTING_ORIENTATION = [0, 0, 30 * math.pi / 180]

    TIMEOUT_DURATION = 900  # 15 minutes
