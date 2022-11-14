from typing import Any
from .voter import Voter


class Situation:
    voters: set[Voter]
    outcome: list[tuple[Any, int]]
    _happiness: float | None = None

    def copy(self):
        slim_copy = Situation()
        slim_copy.voters = self.voters.copy()
        return slim_copy

    @property
    def happiness(self):
        if "outcome" not in self.__dict__ or self.outcome is None:
            raise Exception("the outcome is not yet calculated")

        if self._happiness is not None:
            return self._happiness

        total_happiness = 0
        voter_happiness_list = []

        for voter_info in self.voters:
            voter_info.happiness = self.winner
            voter_happiness_list.append(voter_info.happiness)

        # Why is it scaled?
        for voter_info in self.voters:
            voter_happiness_scaled = (
                voter_info.happiness - min(voter_happiness_list)
            ) / (max(voter_happiness_list) - min(voter_happiness_list))
            total_happiness += voter_happiness_scaled
            voter_info.scaled_happiness = voter_happiness_scaled

        self._happiness = total_happiness
        return self._happiness

    @property
    def winner(self):
        return self.outcome[0][0]

    def __init__(self) -> None:
        self.voters = set()
