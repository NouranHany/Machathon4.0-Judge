# Machathon4.0-Judge

<p align="center">
  <a style="text-decoration:none" >
    <img src="https://img.shields.io/badge/Code-Python-blue?logo=python" alt="Website" />
  </a>
  <a style="text-decoration:none" >
    <img src="https://img.shields.io/badge/Track Design-Blender-orange?logo=Blender" alt="Website" />
  </a>
  <a style="text-decoration:none" >
    <img src="https://img.shields.io/badge/Simulator-CoppeliaSim-red" alt="Website" />
  </a>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/59095993/218258760-82d70b5c-56d2-4820-8644-4d5a1fb68a6b.jpg" width=400 alt="Machathon header">
</p>


The Machathon4.0 Judge repository provides all the required tools and utilities for the [Machathon4.0 Competition - self driving cars edition](https://www.facebook.com/events/1344518816336469). It features convenient wrapper functions for controlling the movement of the car and capturing images from the camera within the CoppeliaSim simulator. It also includes the judge code that evaluates the competitor's solution and updates the leader-board. 

For more information about the competition regulations, please refer to the Official Competition [Rules Book](https://drive.google.com/drive/folders/1f5tKFI4mWJoQy0Vv3YQ2X8SHJh2JxGTu?usp=sharing).
## Installation

1. Clone the repositry <br>
```git clone https://github.com/NouranHany/Machathon4.0-Judge.git```

2. Navigate to the repository directory <br> ```cd Machathon4.0-Judge```

3. Install all dependencies needed <br>
```pip install -r requirements.txt```

## Preparation for running the code
Before running your code, it's important to make sure you have opened the `filteration_scene.ttt` in CoppeliaSim. Here are the steps to follow:

1. Open CoppeliaSim.
2. Load the `filteration_scene.ttt` file by going to File > Open Scene > Browse, then navigating to the location where the scene file is stored.

## How to Use the Judge?

1. Create an instance of the Judge class and provide your team information, including the team code(consists of 9 digits), and the path to a zip containing your code. <br>
```python
judge = Judge(team_code="your_new_team_code", zip_file_path="your_solution.zip")
```

2. Pass the function where you have written your main solution to the judge. For example, if your solution is in a function named run_car, use the following code: <br>
```python
judge.set_run_hook(run_car)
```

3. Call the judge to run your code. The judge will call your code twice and calculate the lap time for each run. If you choose to publish the lap time to the leaderboard, set the `send_score` parameter to `True`. <br>
```python
judge.run(send_score=True)
```
The provided `test.py` file demonstrates how to use the Judge class. Note: don't submit your solution using this script as it uses the keyboard to manually control the car which is against the rules.

### Note for Ubuntu users
The test.py script uses the keyboard library which requires running "sudo", so replace "pip3" with "sudo pip3" and "python3" with "sudo python3". This is only needed for the test.py

## Project Hierarchy
```
└── Machathon4.0-Judge/
    ├── machathon_judge/
    │   ├── data.py  # contains important variables that are used throughout the project
    │   ├── judge.py # Module containing the Judge class to run the competition's tracks and publish the scores to the leaderboard
    |   ├── collision_manager.py # Module containing the CollisionManager class to manage the collision events
    │   ├── simulator.py  # Wrapper for the API that connects CoppeliaSim and Python
    │   └── filteration_scene.ttt  # The competition environment in CoppeliaSim, which includes the track and the vehicle
    ├── test.py  # Demonstrates how to utilize the competition judge and simulator classes
    └── requirements.txt
```

## Attribution
<p align="center">
  <img src="https://user-images.githubusercontent.com/59095993/218258481-82b37fcf-10ad-4a2f-99d0-555e5610b6f2.png" width=100 height=100 alt="STP logo">
</p>
This code was developed and maintained by Step Towards Progress STP, a non-profit organization focuses on developing youth in various fields personally and technically through academic programs, projects, and events. You can find more information about STP at https://stp-org.com/ 

<br>If you have any questions or would like to get in touch with our team, please email us at stp23.official@gmail.com or find us on [Facebook](https://www.facebook.com/STP.Organization). 

