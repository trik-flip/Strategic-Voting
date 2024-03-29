from random import random, shuffle
from typing import Any, Callable

from strategic_voting.types.situation import Situation
from strategic_voting.types.voter import Voter
from strategic_voting.util import profiler, Singleton
Position = tuple[float, ...]

SituationGen = Callable[[int, list[Any], Any], Situation]


class VotingSituationGenerator(metaclass=Singleton):
    """Order and use generator functions"""

    _generator_options: dict[str, SituationGen] = {}

    option: str = "random"

    @staticmethod
    def register(name: str):
        def outer_func(func: SituationGen):
            def inner_func(*args, **kwargs):
                return func(*args, **kwargs)
            instance = VotingSituationGenerator()
            instance._generator_options[name] = inner_func
            return inner_func
        return outer_func

    @profiler.profile
    def generate(self, *args: Any):
        situation = self._generator_options[self.option](*args)
        situation.voters = sorted(situation.voters, key=lambda v: v.order)
        return situation


@profiler.profile
def calculate_distance_between(self: Position, other: Position) -> float:
    total: float = 0
    for x, y in zip(self, other):
        total += (x - y) ** 2
    return total**0.5


@profiler.profile
def generate_position(n: int) -> Position:
    """Create a random position for n dimentions
    # Example
    >>> x = generate_position(1)
    >>> x
    (0.42,)
    >>> y = generate_position(3)
    >>> y
    (0.42, 0.79, 0.28)
    """
    return tuple([random() for _ in range(n)])


@profiler.profile
@VotingSituationGenerator.register("random")
def totally_random(voters: int, options: list[Any], *_) -> Situation:
    """Create voters which are totally random, there is no logic in the order of options

    # Example
    >>> voting_options = ["A", "B", "C"]

    >>> s1 = totally_random(4, voting_options)
    >>> s1
    {
        0:{"weight":(1,1,1), "order":("A","C","B")},
        1:{"weight":(1,1,1), "order":("B","C","A")},
        2:{"weight":(1,1,1), "order":("A","B","C")},
        3:{"weight":(1,1,1), "order":("C","A","B")}
    }

    >>> s2 = totally_random(2, voting_options)
    >>> s2
    {
        0:{"weight":(1,1,1), "order":("C","B","A")},
        1:{"weight":(1,1,1), "order":("B","A","C")},
    }
    """
    situation = Situation()
    for _ in range(voters):
        own_options = options[:]
        shuffle(own_options)

        weights = [random() for _ in options]
        weights.sort(reverse=True)

        voter = Voter(tuple(own_options), tuple(weights))
        situation.voters.append(voter)
    return situation


@profiler.profile
@VotingSituationGenerator.register("plane")
def from_random_plane(voters: int, options: list[Any], n: int = 1) -> Situation:
    """This function tries to mimic the logic used when choosing a option

    The function creates a n-dimensional plane
    Then it will position all the options on the plane
    Then it will postion all the voters on the plane

    Based on the distance from a voter to a plane,
    a voter will have a given preference and weight to a certain option

    The weight will be the max - there distance.
    Thus if a options is further away, a option has a lower weight()

    # Example
    >>> voting_options = ["A", "B", "C"]

    >>> s1 = from_random_plane(4, voting_options)
    >>> s1
    {
        0: {'order': ('C', 'B', 'A'), 'weight': (0.90, 0.75, 0.44)},
        1: {'order': ('A', 'C', 'B'), 'weight': (0.80, 0.73, 0.39)},
        2: {'order': ('A', 'C', 'B'), 'weight': (0.99, 0.54, 0.20)},
        3: {'order': ('C', 'B', 'A'), 'weight': (0.91, 0.74, 0.45)}
    }

    >>> s2 = from_random_plane(2, voting_options, 1)
    >>> s2
    {
        0: {'order': ('B', 'C', 'A'), 'weight': (0.97, 0.46, 0.40)},
        1: {'order': ('B', 'C', 'A'), 'weight': (0.96, 0.45, 0.40)}
    }
    >>> s3 = from_random_plane(3, voting_options, 4)
    >>> s3
    {
        0: {'order': ('C', 'B', 'A'), 'weight': (1.48, 1.44, 1.22)},
        1: {'order': ('C', 'A', 'B'), 'weight': (1.58, 1.31, 1.24)},
        2: {'order': ('C', 'B', 'A'), 'weight': (1.49, 1.33, 1.06)}
    }
    """
    max_of_n: float = n**0.5
    options_positions: dict[Any, Position] = {}
    situation = Situation()

    for option in options:
        options_positions[option] = generate_position(n)

    for _ in range(voters):
        distances: dict[Any, float] = {}
        pos = generate_position(n)

        for option in options:
            distance = calculate_distance_between(
                pos, options_positions[option])
            distances[option] = distance

        sorting: list[tuple[Any, float]] = [
            (k, v) for k, v in distances.items()]
        # smallest distance first, biggest last
        sorting.sort(key=lambda x: x[1])

        order = tuple([x[0] for x in sorting])
        weight = tuple([(max_of_n - x[1]) / max_of_n for x in sorting])

        voter = Voter(order, weight)
        situation.voters.append(voter)
    return situation
