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

generator.option = "random"
calc.option = "borda"
simple_calc.option = "borda"
num_voters = 10

profiler.start()

voting_situation = generator.generate(num_voters, voting_options, 1)
print(f"All voting options: {voting_options}")

print("True votes")
true_outcome = voting_outcome(voting_situation.votes(calc))
print(f"True voting outcome:{true_outcome}")
print(f"True voting winner: {get_winner(true_outcome, voting_options)}")
voting_situation.outcome = [(o, out) for o, out in zip(voting_options, true_outcome)]
print(f"Outcome: {voting_situation.outcome}")
print(f"Total happiness: {(voting_situation.total_happiness[0]/num_voters)*100, (voting_situation.total_happiness[1]/num_voters)*100}") # (weighted based, distance based)

mean_happiness_gain_total = 0
for i, (voter, options) in enumerate(
    strategic_voting_options_in_situation(voting_situation, calc).items()
):
    print(f"===== Voter {i+1:2} =====")
    print(f"True preferrence: \t\t{voter.order}")
    print(f"True happiness: \t\t{voter.happiness}")
    print(f"Tactical voting options: \t{len(options)}")
    print()
    mean_happiness_gain_voter = 0
    for o_index, option in enumerate(options):
        happiness_gain = option[2]-option[3]
        mean_happiness_gain_voter += happiness_gain
        print(f"--- Tactical voting option {o_index+1:2} ---")
        print(f"New voter preferrence: \t\t{option[0]}")
        print(f"New outcome: \t\t\t{option[1]}")
        print(f"New happiness: \t\t\t{option[2]}")
        print(f"Gain in happiness: \t\t{happiness_gain}")
        print(f"New overall happiness: \t\t{option[4]}")
        print(f"Old overall happiness: \t\t{option[5]}")
    print("=" * 50)
    print()
    mean_happiness_gain_total += mean_happiness_gain_voter


print("Tactical votes")
voter_option = {}
risk = 0
for voter, options in strategic_voting_options_in_situation(
    voting_situation, calc
).items():
    voter_option[voter] = (
        simple_calc.calc(random.choice(options)[0])
        if len(options) != 0
        else calc.calc(voter)
    )
    risk = risk + len(options)

tactical_outcome = voting_outcome([v for v in voter_option.values()])
print(f"Tactical voting outcome:{tactical_outcome}")
print(f"Tactical voting winner: {get_winner(tactical_outcome, voting_options)}")
voting_situation.outcome = [
    (o, out) for o, out in zip(voting_options, tactical_outcome)
]
print(f"Outcome: {voting_situation.outcome}")
print(f"Total happiness: {(voting_situation.total_happiness[0]/num_voters)*100, (voting_situation.total_happiness[1]/num_voters)*100}")



print("\nRisk analysis")
"""
The risk functions are implemented here.

Function 1: 
Divides the sum of the number of tactical voting options of all voters (line 76) by the number of voters.
Returns an average number of tactical voting options per voter.

Function 2:
Sums the total happiness gain for all voters (lines40, 51, 52 and 62) and divides this number by the number of voters.
Returns an average happiness gain per voter.
"""

risk = risk / num_voters
risk1 = (mean_happiness_gain_total)/num_voters

print(f"Risk based on tactical vote options: ", risk)
print("Risk based on average happiness gain per voter: ", risk1)



# outcome(voting_situation)
# total_happy = voting_situation.total_happiness
# print(
#     f"happiness(measurement1): {total_happy[0]}, happiness(measurement2):{total_happy[1]}")
# print(f"winner: {voting_situation.winner}")

profiler.stop()

# profiler.show()
