import random

from strategic_voting.simple_voting_calc import SimpleVotingCalculator

from strategic_voting.calc_voting_outcome import VotingCalculator
from strategic_voting.simple_voting import (
    strategic_voting_options_in_situation,
    voting_outcome,
    get_winner,
)
from strategic_voting.situation_generator import VotingSituationGenerator
from strategic_voting.util import profiler

random.seed(42)

voting_options = ["A", "B", "C", "D", "E"]

generator = VotingSituationGenerator()
calc = VotingCalculator()
simple_calc = SimpleVotingCalculator()

generator.option = "plane"
calc.option = "borda"
simple_calc.option = "borda"

profiler.start()

voting_situation = generator.generate(5, voting_options, 1)
print(f"All voting options: {voting_options}")

true_outcome = voting_outcome(voting_situation.votes(calc))
print(f"True voting outcome:{true_outcome}")
print(f"True voting winner: {get_winner(true_outcome, voting_options)}")
voting_situation.outcome = [(o, out) for o, out in zip(voting_options, true_outcome)]
print(f"outcome: {voting_situation.outcome}")
print(f"total happiness: {voting_situation.total_happiness}")


for voter, options in strategic_voting_options_in_situation(
    voting_situation, calc
).items():
    print(voter.order)
    for o in options:
        print(f"\t{o}")


print("Tactical votes")
voter_option = {}
for voter, options in strategic_voting_options_in_situation(
    voting_situation, calc
).items():
    voter_option[voter] = (
        simple_calc.calc(random.choice(options)[0])
        if len(options) != 0
        else calc.calc(voter)
    )

tactical_outcome = voting_outcome([v for v in voter_option.values()])
print(f"Tactical voting outcome:{tactical_outcome}")
print(f"Tactical voting winner: {get_winner(tactical_outcome, voting_options)}")
voting_situation.outcome = [
    (o, out) for o, out in zip(voting_options, tactical_outcome)
]
print(voting_situation.outcome)
print(voting_situation.total_happiness)


# outcome(voting_situation)
# total_happy = voting_situation.total_happiness
# print(
#     f"happiness(measurement1): {total_happy[0]}, happiness(measurement2):{total_happy[1]}")
# print(f"winner: {voting_situation.winner}")

profiler.stop()

# profiler.show()
