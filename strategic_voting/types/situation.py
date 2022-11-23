from typing import Any
from .voter import Voter


class Situation:
    voters: set[Voter]
    outcome: list[tuple[Any, int]]
    _happiness: float | None = None
    _happiness2: float | None = None

    def copy(self):
        slim_copy = Situation()
        slim_copy.voters = self.voters.copy()
        return slim_copy

    @property
    def happiness(self):
        if "outcome" not in self.__dict__ or self.outcome is None:
            raise Exception("the outcome is not yet calculated")

        if self._happiness and self._happiness2 is not None:
            return self._happiness, self._happiness2

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
        for voter_info in self.voters:
            voter_happiness_scaled = (
                voter_info.happiness - min(voter_happiness_list)
            ) / (max(voter_happiness_list) - min(voter_happiness_list))
            total_happiness += voter_happiness_scaled
            voter_happiness2_scaled = (voter_info.happiness2 - min(voter_happiness2_list)) / (max(voter_happiness2_list) - min(voter_happiness2_list))
            total_happiness2 += voter_happiness2_scaled
            voter_info.scaled_happiness = voter_happiness_scaled
            voter_info.scaled_happiness2 = voter_happiness2_scaled

        self._happiness = total_happiness
        self._happiness2 = total_happiness2
        return self._happiness, self._happiness2

    @property
    def winner(self):
        return self.outcome[0][0]

    def __init__(self) -> None:
        self.voters = set()
