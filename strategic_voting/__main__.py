from strategic_voting.situation_generator import VotingSituationGenerator
from strategic_voting.calc_voting_outcome import VotingOutcome

voting_options = ["A", "B", "C"]

gen = VotingSituationGenerator()
outcome = VotingOutcome()

gen.option = "plane"
outcome.option = "vote-for-two"

voting_situation = gen(7, voting_options, 3)

outcome(voting_situation)

print(f"happiness: {voting_situation.happiness}")
print(f"winner: {voting_situation.winner}")
