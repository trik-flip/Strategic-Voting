import numpy as np


def risk(tva):
    num_dishonest_votes = 0
    for voter in tva["voting_situation"].keys():
        if not np.array_equal(tva['voting_situation'][voter]["vote"], tva['voting_situation'][voter]["strategic_vote"]):
            num_dishonest_votes += 1
    tva["risk"] = num_dishonest_votes
    return num_dishonest_votes

def risk2(options):
    # Risk according to the sum of difference in happiness
    risk = sum(x[1] for x in options)
    return risk
