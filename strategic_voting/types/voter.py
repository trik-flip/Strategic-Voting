from typing import Any


class Voter:
    order: tuple[Any]
    weights: tuple[float]

    @property
    def happiness(self):
        return self._happiness

    @happiness.setter
    def happiness(self, value):
        if value in self.order:
            self._happiness = self.weights[self.order.index(value)]

    _happiness: float
    scaled_happiness: float

    def __init__(self, order, weight) -> None:
        self.order = order
        self.weights = weight
