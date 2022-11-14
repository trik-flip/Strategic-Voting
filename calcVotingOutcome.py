# TODO: change hardcoded 4 candidates to variable num of candidates
import numpy as np

def calcVotingOutcome(TVA):
    outcome = np.array([0,0,0,0])

    if TVA['scheme'] == 'plurality':
        for voter in TVA["voting_situation"].keys():
            vote = np.array([0, 0, 0, 0])
            candidate = TVA["voting_situation"][voter]["preference"][0] - 1
            vote[candidate] = 1
            TVA["voting_situation"][voter]["vote"] = vote
            outcome = np.add(outcome, vote)

    if TVA['scheme'] == 'borda':
        for voter in TVA['voting_situation'].keys():
            vote = np.array([0,0,0,0])
            max_vote = len(TVA['voting_situation'][voter]["preference"])
            for pos in range(max_vote):
                candidate = TVA['voting_situation'][voter]["preference"][pos]
                vote[candidate] = max_vote - pos + 1
                TVA['voting_situation'][voter]['vote'] = vote
                outcome = np.add(outcome, vote)

    if TVA['scheme'] == 'anti-plurality':
        size = len(TVA["voting_situation"][voter]["preference"])
        for voter in TVA["voting_situation"].keys():
            vote = np.array([1, 1, 1, 1])
            candidate = TVA["voting_situation"][voter]["preference"][size - 1]
            vote[candidate] = 0
            TVA["voting_situation"][voter]["vote"] = vote
            outcome = np.add(outcome, vote)

    if TVA['scheme'] == 'vote-for-two':
        for voter in TVA["voting_situation"].keys():
            vote = np.array([0, 0, 0, 0])
            candidate1 = TVA["voting_situation"][voter]["preference"][0] - 1
            candidate2 = TVA["voting_situation"][voter]["preference"][1] - 1
            vote[candidate1], vote[candidate2] = 1
            TVA["voting_situation"][voter]["vote"] = vote
            outcome = np.add(outcome, vote)

    TVA["total_outcome"] = outcome
    TVA["normalized_outcome"] = np.divide(outcome, len(TVA["voting_situation"].keys()))
    return TVA["normalized_outcome"]
