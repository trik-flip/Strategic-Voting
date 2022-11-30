from typing import Any, Callable

from strategic_voting.types.situation import Situation
from strategic_voting.types.voter import Voter
from strategic_voting.util import Singleton, profiler, cache


VotingFunc = Callable[[Voter], dict[Any, int]]


@profiler.profile
def to_simple_list(votes: dict[Any, int]):
    return tuple(votes[x] for x in sorted(votes))


class VotingCalculator(metaclass=Singleton):
    _voting_systems: dict[str, VotingFunc] = {}
    option: str = "plurality"

    @staticmethod
    def register(name: str):
        def outer_func(func: VotingFunc):
            def inner_func(voter: Voter):
                return func(voter)
            instance = VotingCalculator()
            instance._voting_systems[name] = func
            return inner_func
        return outer_func

    @cache
    @profiler.profile
    def calc(self, voter: Voter):
        return to_simple_list(self._voting_systems[self.option](voter))


@profiler.profile
@VotingCalculator.register("plurality")
def plurality_vote(voter: Voter):
    pref = {option: 0 for option in voter.order}
    pref[voter.order[0]] = 1
    return pref


@profiler.profile
@VotingCalculator.register("borda")
def borda_vote(voter: Voter):
    max_score = len(voter.order) - 1
    pref = {option: max_score -
            voter.order.index(option) for option in voter.order}
    return pref


@profiler.profile
@VotingCalculator.register("anti-plurality")
def anti_plurality_vote(voter: Voter):
    pref = {option: 1 for option in voter.order}
    pref[voter.order[-1]] = 0
    return pref


@profiler.profile
@VotingCalculator.register("vote-for-two")
def best_two_vote(voter: Voter):
    pref = {option: 0 for option in voter.order}
    for o in voter.order[:2]:
        pref[o] = 1
    return pref
