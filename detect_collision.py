from PIL import Image
from machathon_judge import Simulator, Judge


def run_car(simulator):
    carHandle = simulator.sim.getObject('/Manta')
    cuboidHandle = simulator.sim.getObject('/Cuboid')
    result, _ = simulator.sim.checkCollision(carHandle,cuboidHandle)
    print(result)
    simulator.move_car(10, 0)



if __name__ == "__main__":
    judge = Judge(run_car)
    judge.run()
