from typing import Any

from strategic_voting.util import profiler


class Voter:
    order: tuple[Any, ...]
    weights: tuple[float, ...]
    _happiness:  float
    _happiness_cache: dict[Any, float]
    _happiness2: float
    scaled_happiness: float

    @property
    @profiler.profile
    def happiness(self):
        return self._happiness

    @happiness.setter
    @profiler.profile
    def happiness(self, value):
        if value not in self._happiness_cache:
            self._happiness_cache[value] = self.weights[self.order.index(
                value)]

        self._happiness = self._happiness_cache[value]

    @property
    @profiler.profile
    def happiness2(self):
        return self._happiness2

    @happiness2.setter
    @profiler.profile
    def happiness2(self, value):
        if value in self.order:
            weighted_outcome = len(value)**2
            weighted_preference = self.weights[self.order.index(
                value)]*(len(self.order)-self.order.index(value))
            self._happiness2 = 1 / \
                (1+abs(weighted_outcome - weighted_preference))

    def __init__(self, order, weight) -> None:
        self.order = order
        self.weights = weight
        self._happiness_cache = {}
