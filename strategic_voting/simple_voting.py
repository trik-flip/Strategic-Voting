from itertools import permutations
from typing import Any
from strategic_voting.types.voter import Voter

from strategic_voting.util import profiler


def nested_strategic_voting_options(all_votes, voters, voting_options, calc, known_voters=None):
    if known_voters is None:
        known_voters = set()
    true_outcome = voting_outcome(all_votes)

    options: dict[Voter, list[tuple[int, ...]]] = {}
    for i, voter in enumerate(voters):

        options[voter] = []

        if get_winner(true_outcome, voting_options)[1] == voter.order[0]:
            # If first prefference is winner, we don't do anything
            continue

        voter.happiness = get_winner(true_outcome, voting_options)[1]
        true_voter_happiness = voter.happiness

        for option in alternative_voting_options(calc.calc(voter)):

            temp = all_votes[i]
            all_votes[i] = option
            for v in voters:
                if v not in known_voters:
                    nested_strategic_voting_options(
                        all_votes, voters, voting_options, calc, known_voters | {v})

            outcome = voting_outcome(all_votes)
            all_votes[i] = temp

            voter.happiness = get_winner(outcome, voting_options)[1]
            if voter.happiness > true_voter_happiness:
                options[voter].append(option)


@profiler.profile
def tied(outcome: list[int]):
    return outcome.count(max(outcome)) != 1


@profiler.profile
def alternative_voting_options(vote: tuple[int]):
    all_options = permutations(vote)
    filtered_options = set(all_options) - {vote}
    for a in sorted(filtered_options):
        yield a


@profiler.profile
def get_winner(outcome: list[int], options: list[Any]):
    return max(zip(outcome, options), key=lambda z: z[0])


@profiler.profile
def voting_outcome(votes: list[tuple[int, ...]]):
    return [sum(x) for x in zip(*votes)]


@profiler.profile
def strategic_voting_options_in_situation(situation, calc):
    all_votes = situation.votes(calc)
    true_outcome = voting_outcome(all_votes)

    voting_options = sorted(situation.voters[0].order)

    options: dict[Voter, list[tuple[int, ...]]] = {}
    for i, voter in enumerate(situation.voters):

        options[voter] = []

        if get_winner(true_outcome, voting_options)[1] == voter.order[0]:
            # If first prefference is winner, we don't do anything
            continue

        voter.happiness = get_winner(true_outcome, voting_options)[1]
        true_voter_happiness = voter.happiness

        for option in alternative_voting_options(calc.calc(voter)):

            temp = all_votes[i]
            all_votes[i] = option
            outcome = voting_outcome(all_votes)
            all_votes[i] = temp

            voter.happiness = get_winner(outcome, voting_options)[1]
            if voter.happiness > true_voter_happiness:
                options[voter].append(option)

    return options
    