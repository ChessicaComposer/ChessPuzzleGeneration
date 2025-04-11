from genetic.crossover.singlepoint import SinglePoint
from .. chromosome import IntBoard
import random

class TwoPoint(SinglePoint):
    def __init__(self):
        super().__init__()

    def _mate(self, parent1: IntBoard, parent2: IntBoard) -> list[IntBoard]:
        max_len = len(parent1.body)
        point1 = 0
        point2 = 0
        while point1 == point2:
            point1 = random.randint(0, max_len)
            point2 = random.randint(0, max_len)
            if point1 < point2:
                return [IntBoard(parent1.body[:point1] + parent2.body[point1:point2] + parent1.body[point2: max_len]),
                IntBoard(parent2.body[:point1] + parent1.body[point1:point2] + parent2.body[point2: max_len])]
            else:
                return [IntBoard(parent1.body[:point2] + parent2.body[point2:point1] + parent1.body[point1: max_len]),
                IntBoard(parent2.body[:point2] + parent1.body[point2:point1] + parent2.body[point1: max_len])]