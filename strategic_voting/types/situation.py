from typing import Any

from strategic_voting.types.voter import Voter
from strategic_voting.util import profiler


class Situation:

    voters: list[Voter]
    outcome: list[tuple[Any, int]]
    _happiness: float = None
    _happiness2: float = None

    @profiler.profile
    def votes(self, voting_calc):
        return [voting_calc.calc(v) for v in self.voters]

    @profiler.profile
    def copy(self):
        slim_copy = Situation()
        slim_copy.voters = self.voters.copy()
        return slim_copy

    @property
    @profiler.profile
    def total_happiness(self):
        if "outcome" not in self.__dict__ or self.outcome is None:
            raise Exception("the outcome is not yet calculated")

        total_happiness = 0
        total_happiness2 = 0
        voter_happiness_list = []
        voter_happiness2_list = []

        for voter_info in self.voters:
            voter_info.happiness = self.winner
            voter_info.happiness2 = self.winner
            voter_happiness_list.append(voter_info.happiness)
            voter_happiness2_list.append(voter_info.happiness2)

        # Why is it scaled?
        min_voter_happiness_list = min(voter_happiness_list)
        max_voter_happiness_list = max(voter_happiness_list)

        min_voter_happiness2_list = min(voter_happiness2_list)
        max_voter_happiness2_list = max(voter_happiness2_list)

        for voter_info in self.voters:
            voter_happiness_scaled = (
                voter_info.happiness - min_voter_happiness_list
            ) / (max_voter_happiness_list - min_voter_happiness_list)

            total_happiness += voter_happiness_scaled

            voter_happiness2_scaled = (
                voter_info.happiness2 - min_voter_happiness2_list
            ) / (max_voter_happiness2_list - min_voter_happiness2_list)

            total_happiness2 += voter_happiness2_scaled

            voter_info.scaled_happiness = voter_happiness_scaled
            voter_info.scaled_happiness2 = voter_happiness2_scaled

        self._happiness = total_happiness
        self._happiness2 = total_happiness2
        return self._happiness, self._happiness2

    @property
    @profiler.profile
    def winner(self):
        return sorted(self.outcome, key=lambda x: x[1], reverse=True)[0][0]

    def __init__(self) -> None:
        self.voters = []
