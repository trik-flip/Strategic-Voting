import numpy as np



def get_risk(tva):
    num_dishonest_votes = 0
    for voter in tva["voting_situation"].keys():
        if not np.array_equal(tva['voting_situation'][voter]["vote"], tva['voting_situation'][voter]["strategic_vote"]):
            num_dishonest_votes += 1
    tva["risk"] = num_dishonest_votes
    return num_dishonest_votes


