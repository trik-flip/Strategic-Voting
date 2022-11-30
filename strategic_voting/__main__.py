from strategic_voting.calc_voting_outcome import VotingOutcome
from strategic_voting.situation_generator import VotingSituationGenerator
from strategic_voting.util import profiler

voting_options = ["A", "B", "C"]
gen = VotingSituationGenerator()
outcome = VotingOutcome()

gen.option = "plane"
outcome.option = "vote-for-two"

voting_situation = gen(5000, voting_options, 8)
outcome(voting_situation)

total_happy = voting_situation.total_happiness
print(
    f"happiness(measurement1): {total_happy[0]}, happiness(measurement2):{total_happy[1]}")
print(f"winner: {voting_situation.winner}")

profiler.show(min_time=profiler.ms)
