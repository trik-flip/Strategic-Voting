from strategic_voting.calc_voting_outcome import VotingOutcome
from strategic_voting.types.situation import Situation

"""

I can't make anything great now without some of the parts that need to be written still. :(
This is a more "advanced" way, easier would be to count dishonest voters.

The idea is as follows:
1. calculate for each voter the happiness of the true voting outcome and the strategic vote outcome (either best or all whatever you prefer)
2. compute the average difference of the happiness (or overall happiness) between all voters and true voting outcome vs. strategic outcome
3. the average would be the rate of a voting situation (overall happiness) being susceptical to strategic voting

"""
def risk_calculation(voting: Situation, VotingOutcome, StrategicVotingOutcome):

    for v in voting.happiness:
        v += v
    
    for s in StrategicVotingOutcome.happiness:    # I'm not sure how to refer to the strategicvotingoutcome yet because it is not added yet but imagine going through all happiness of each strategic vote
        s += s

    av_happiness = v - s / len(voting.voters)
