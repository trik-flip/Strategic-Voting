"""To calculate the happiness of a voter, we need to know the voter's true preference,
the outcome of strategic voting. With these two elements, we can compare the position of any
candidate in the voter's true preference and that position in outcome. If the difference between
two positions is small, then the happiness of the voter would be high."""

voting_situation = {1:{"order":["A","B","C"], "weight":[3,2,1]},
                    2:{"order":["C","B","A"],"weight":[2,1,1]},
                    3:{"order":["C","A","B"],"weight":[2,1,1]}
                    }
voting_outcome = ["B","A","C"]

def CalcTotalHappiness(voting_outcome, voting_situation):
    total_happiness = 0
    voter_happiness_list = []

    for voter in range(len(voting_situation.keys())):
        voter_preference = voting_situation[voter+1]["order"]
        voter_happiness = CalcVoterHappiness(voter, voting_outcome, voter_preference,voting_situation)
        voter_happiness_list.append(voter_happiness)
        voting_situation[voter+1]["happiness"] = voter_happiness

    for voter in range(len(voting_situation.keys())):
        voter_happiness_scaled = (voting_situation[voter+1]["happiness"] - min(voter_happiness_list)) / (
                max(voter_happiness_list) - min(voter_happiness_list))
        total_happiness += voter_happiness_scaled
        voting_situation[voter + 1]["scaled_happiness"] = voter_happiness_scaled

    return total_happiness, voting_situation

def CalcVoterHappiness(voter, voting_outcome, voter_preference, voting_situation):
    weight_outcome = list(range(len(voting_outcome)))
    weight_outcome.reverse()
    voter_happiness = 0

    for candidate in range(len(voter_preference)):
        # Based on the order of candidates in voter preference,
        # find their positions in outcome indexing from the end
        index_candidate_outcome = len(voting_outcome) - voting_outcome.index(
            voter_preference[candidate])
        happiness_outcome = weight_outcome[voting_outcome.index(voter_preference[candidate])]*index_candidate_outcome
        happiness_preference = voting_situation[voter+1]["weight"][candidate]*candidate
        voter_happiness += happiness_outcome - happiness_preference

    return voter_happiness

print(CalcTotalHappiness(voting_outcome, voting_situation))