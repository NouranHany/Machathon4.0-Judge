# Machathon4.0-Judge

<p align="left">
  <a style="text-decoration:none" >
    <img src="https://img.shields.io/badge/Code-Python-blue?logo=python" alt="Website" />
  </a>
  <a style="text-decoration:none" >
    <img src="https://img.shields.io/badge/Simulator-CoppeliaSim-red" alt="Website" />
  </a>
</p>

<p align="left">
  <img src="https://user-images.githubusercontent.com/59095993/218258760-82d70b5c-56d2-4820-8644-4d5a1fb68a6b.jpg" width=400 alt="Machathon header">
</p>


The Machathon4.0 Judge repository provides all the required tools and utilities for the [Machathon4.0 Competition - self driving cars edition](https://www.facebook.com/events/1344518816336469). It features convenient wrapper functions for controlling the movement of the car and capturing images from the camera within the CoppeliaSim simulator. It also includes the judge code that evaluates the competitor's solution and updates the leader-board. 

For more information about the competition regulations, please refer to the official competition [rule book](https://drive.google.com/drive/folders/1f5tKFI4mWJoQy0Vv3YQ2X8SHJh2JxGTu)

## Installation

Clone the repositry with the following command <br>
```git clone github link```

Navigate to the repositry directory <br> ```cd Machathon4.0-judge```

Install all dependencies needed <br>
```pip install -r .\requirements.txt```


## Project Hierarchy
```
└── Machathon4.0-Judge/
    ├── machathon_judge/
    │   ├── data.py  # contains important variables that are used throughout the project
    │   ├── judge.py 
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

If you have any questions or would like to get in touch with our team, please email us at stp23.official@gmail.com or find us on [Facebook](https://www.facebook.com/STP.Organization). 

