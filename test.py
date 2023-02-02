from PIL import Image
from machathon_judge import Simulator, Judge


def run_car(simulator):
    img = simulator.get_image()
    img = Image.fromarray(img)
    img.save("test.png")
    simulator.move_car(5, 0)


if __name__ == "__main__":
    judge = Judge(run_car)
    judge.run()
