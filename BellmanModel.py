from scipy.stats import norm
## because of recursion, we had too many function calls, so we used lru_cache to cache the results of previous function calls
from functools import lru_cache


dist_others=26 #assume oppenents guess exactly half right (p=0.5)
std_others=2.0 #now imagine that they may be a bit better or worse than that, so we give them a standard deviation of 2
number_others=10 #10 opponents

## our win probability can be calculated viewing the normal distribution of the other players and calculating the probability that our score C is greater than theirs
def win_probability(C):
    return norm.cdf((C - dist_others) / std_others) ** number_others 


@lru_cache(maxsize=None)
#Bellman equation, R is number of red left, B is number of blue left, C is current score
def V(R,B,C):
    if R==0 and B==0:
        return win_probability(C)
    
    total=R+B
    ##red guesses
    RG=0    
    if R>0:
        RG+= (R/total)*V(R-1,B,C+1)
    if B>0:
        RG+= (B/total)*V(R,B-1,C)

    #blue guesses
    BG=0
    if B>0:
        BG+= (B/total)*V(R,B-1,C+1)
    if R>0:
        BG+= (R/total)*V(R-1,B,C)
    #the max of RG and BG will just choose whether to guess red or blue based on which has a higher expected value.
    return max(RG,BG)


print ("Win Probability with Bellman:", V(26,26,0))