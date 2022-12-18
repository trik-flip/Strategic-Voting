from typing import Any, Callable

from strategic_voting.util import Singleton, profiler


VotingOrder = tuple[Any, ...]
VotingFunc = Callable[[VotingOrder], dict[Any, int]]


@profiler.profile
def to_simple_list(votes: dict[Any, int]):
    return tuple(votes[x] for x in sorted(votes))


class SimpleVotingCalculator(metaclass=Singleton):
    _voting_systems: dict[str, VotingFunc] = {}
    option: str = "plurality"

    @staticmethod
    def register(name: str):
        def outer_func(func: VotingFunc):
            def inner_func(order: VotingOrder):
                return func(order)

            instance = SimpleVotingCalculator()
            instance._voting_systems[name] = func
            return inner_func

        return outer_func

    @profiler.profile
    def calc(self, order: VotingOrder):
        return to_simple_list(self._voting_systems[self.option](order))


@profiler.profile
@SimpleVotingCalculator.register("plurality")
def plurality_vote(order: VotingOrder):
    pref = {option: 0 for option in order}
    pref[order[0]] = 1
    return pref


@profiler.profile
@SimpleVotingCalculator.register("borda")
def borda_vote(order: VotingOrder):
    max_score = len(order) - 1
    pref = {option: max_score - order.index(option) for option in order}
    return pref


@profiler.profile
@SimpleVotingCalculator.register("anti-plurality")
def anti_plurality_vote(order: VotingOrder):
    pref = {option: 1 for option in order}
    pref[order[-1]] = 0
    return pref


@profiler.profile
@SimpleVotingCalculator.register("vote-for-two")
def best_two_vote(order: VotingOrder):
    pref = {option: 0 for option in order}
    for o in order[:2]:
        pref[o] = 1
    return pref
