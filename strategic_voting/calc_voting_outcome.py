from typing import Any, Callable

from strategic_voting.types.situation import Situation


def select_winning_options(options: dict[Any, int]):
    sorted_options = [(k, v) for k, v in options.items()]
    sorted_options.sort(key=lambda x: x[1], reverse=True)
    return sorted_options


def plurality_voting(voting: Situation):
    options: dict[Any, int] = {}

    for v in voting.voters:
        for option in v.order[:1]:
            if option not in options:
                options[option] = 0
            options[option] += 1

    voting.outcome = select_winning_options(options)
    return voting.outcome


def borda_voting(voting: Situation):
    options: dict[Any, int] = {}

    for v in voting.voters:
        for i, option in enumerate(v.order):
            if option not in options:
                options[option] = 0
            options[option] += len(v.order) - i - 1

    voting.outcome = select_winning_options(options)
    return voting.outcome


def anti_plurality_voting(voting: Situation):
    options: dict[Any, int] = {}

    for v in voting.voters:
        for option in v.order[:-1]:
            if option not in options:
                options[option] = 0
            options[option] += 1

    voting.outcome = select_winning_options(options)
    return voting.outcome


def best_two_voting(voting: Situation):
    options: dict[Any, int] = {}

    for v in voting.voters:
        for option in enumerate(v.order[:2]):
            if option not in options:
                options[option] = 0
            options[option] += 1
    voting.outcome = select_winning_options(options)
    return voting.outcome


class VotingOutcome:
    _voting_systems: dict[str, Callable[[Situation], list[Any]]] = {
        "plurality": plurality_voting,
        "borda": borda_voting,
        "anti-plurality": anti_plurality_voting,
        "vote-for-two": best_two_voting,
    }
    _option: str = "plurality"

    @property
    def option(self) -> str:
        return self._option

    @option.setter
    def option(self, val: str):
        if val in self._voting_systems:
            self._option = val

    def __call__(self, situation: Situation):
        return self._voting_systems[self._option](situation)
