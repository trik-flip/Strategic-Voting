from typing import Any


class Voter:
    order: tuple[Any, ...]
    weights: tuple[float, ...]
    _happiness: float
    _happiness2: float
    scaled_happiness: float

    @property
    def happiness(self):
        return self._happiness
    @property
    def happiness2(self):
        return self._happiness2

    @happiness.setter
    def happiness(self, value):
        if value in self.order:
            self._happiness = self.weights[self.order.index(value)]
    @happiness2.setter
    def happiness2(self,value):
        if value in self.order:
            weighted_outcome = len(value)**2
            weighted_preference = self.weights[self.order.index(value)]*(len(self.order))
            self._happiness2 = 1/(1+abs(weighted_outcome - weighted_preference))
    def __init__(self, order, weight) -> None:
        self.order = order
        self.weights = weight
