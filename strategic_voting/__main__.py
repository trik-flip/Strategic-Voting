import random

from strategic_voting.calc_voting_outcome import VotingCalculator
from strategic_voting.simple_voting import (
    strategic_voting_options_in_situation, voting_outcome, get_winner)
from strategic_voting.situation_generator import VotingSituationGenerator
from strategic_voting.util import profiler

random.seed(42)

voting_options = ["A", "B", "C", "D", "E"]

generator = VotingSituationGenerator()
calc = VotingCalculator()

generator.option = "plane"
calc.option = "borda"

profiler.start()

# Plurality timing:
# -  500 voters, 5 options => .17s runtime
# - 1000 voters, 5 options => .4s runtime
# - 2000 voters, 5 options => 1.2s runtime
# - 4000 voters, 5 options => 4.6s runtime
# 2x bigger = 3x slower

# Anti-Plurality timing:
# -  500 voters, 5 options => .17s runtime
# - 1000 voters, 5 options => .4s runtime
# - 2000 voters, 5 options => 1.2s runtime
# - 4000 voters, 5 options => 4.6s runtime
# 2x bigger = 3x slower

# Borda timing:
# -  500 voters, 5 options => 1.3s runtime
# - 1000 voters, 5 options => 8.2s runtime
# - 2000 voters, 5 options => 42s runtime
# - 4000 voters, 5 options => 300s runtime
# 2x bigger = 5x/7x slower

# Vote-for-Two timing:
# -  500 voters, 5 options => .24s runtime
# - 1000 voters, 5 options => .66s runtime
# - 2000 voters, 5 options => 2.26s runtime
# - 4000 voters, 5 options => 10s runtime
# 2x bigger = 3x/4x slower

voting_situation = generator.generate(5, voting_options, 1)
print(f"All voting options: {voting_options}")

true_outcome = voting_outcome(voting_situation.votes(calc))
print(f"True voting outcome:{true_outcome}")
print(
    f"True voting winner: {get_winner(true_outcome, voting_options)}")
voting_situation.outcome = [(o, out)
                            for o, out in zip(voting_options, true_outcome)]
print(voting_situation.outcome)
print(voting_situation.total_happiness)


for k, v in strategic_voting_options_in_situation(voting_situation, calc).items():
    print(k.order, calc.calc(k), v)



print("Tactical votes")
voter_option = {}
for voter, options in strategic_voting_options_in_situation(voting_situation, calc).items():
    voter_option[voter] = random.choice(options) if len(
        options) != 0 else calc.calc(voter)

tactical_outcome = voting_outcome([v for v in voter_option.values()])
print(f"Tactical voting outcome:{tactical_outcome}")
print(
    f"Tactical voting winner: {get_winner(tactical_outcome, voting_options)}")
voting_situation.outcome = [(o, out)
                            for o, out in zip(voting_options, tactical_outcome)]
print(voting_situation.outcome)
print(voting_situation.total_happiness)


# outcome(voting_situation)
# total_happy = voting_situation.total_happiness
# print(
#     f"happiness(measurement1): {total_happy[0]}, happiness(measurement2):{total_happy[1]}")
# print(f"winner: {voting_situation.winner}")

profiler.stop()

# profiler.show()
