import time
from .simulator import Simulator


class Judge:
    def __init__(self, hook_img):
        self.hook = hook_img

    def run(self):
        simulator = Simulator()

        simulator.start()

        tic = time.time()

        while (time.time() - tic) < 2:
            self.hook(simulator)

        simulator.stop()
