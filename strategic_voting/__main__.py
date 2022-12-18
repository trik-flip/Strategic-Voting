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
calc.option = "plurality"
simple_calc.option = "plurality"
num_voters = 10

profiler.start()

voting_situation = generator.generate(num_voters, voting_options, 1)
print(f"All voting options: {voting_options}")

true_outcome = voting_outcome(voting_situation.votes(calc))
print(f"True voting outcome:{true_outcome}")
print(f"True voting winner: {get_winner(true_outcome, voting_options)}")
voting_situation.outcome = [(o, out) for o, out in zip(voting_options, true_outcome)]
print(f"outcome: {voting_situation.outcome}")
print(f"total happiness: {voting_situation.total_happiness}")

mean_happiness_gain_total = 0
for i, (voter, options) in enumerate(
    strategic_voting_options_in_situation(voting_situation, calc).items()
):
    print(f"===== Voter {i+1:2} =====")
    print(f"True preferrence: \t\t{voter.order}")
    print(f"True happiness: \t\t{voter.happiness}")
    print(f"Tactical voting option: \t{len(options)}")
    print()
    mean_happiness_gain_voter = 0
    for o_index, option in enumerate(options):
        happiness_gain = option[2]-option[3]
        mean_happiness_gain_voter += happiness_gain
        print(f"--- Tactical voting option {o_index+1:2} ---")
        print(f"New voter preferrence: \t\t{option[0]}")
        print(f"New outcome: \t\t\t{option[1]}")
        print(f"New happiness: \t\t\t{option[2]}")
        print(f"gain in happiness: \t\t{happiness_gain}")
        print(f"New overall happiness: \t\t{option[4]}")
        print(f"old overall happiness: \t\t{option[5]}")
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
    risk = risk + (len(options) / num_voters)

tactical_outcome = voting_outcome([v for v in voter_option.values()])
print(f"Tactical voting outcome:{tactical_outcome}")
print(f"Tactical voting winner: {get_winner(tactical_outcome, voting_options)}")
voting_situation.outcome = [
    (o, out) for o, out in zip(voting_options, tactical_outcome)
]
print(voting_situation.outcome)
print(voting_situation.total_happiness)



print("\nRisk analysis")

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
