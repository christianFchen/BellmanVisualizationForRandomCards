from scipy.stats import norm
## because of recursion, we had too many function calls, so we used lru_cache to cache the results of previous function calls
from functools import lru_cache
import random
import matplotlib.pyplot as plt
import numpy as np
import os
os.makedirs("figures", exist_ok=True)


dist_others=28 #assume oppenents guess stronger than purely probability that uses bayesian
std_others=3 #now imagine that they may be a bit better or worse than that, so we give them a +- 3 cards from 28
number_others=10 #10 opponents
n=100000 #100,000 simulations

## our win probability can be calculated viewing the normal distribution of the other players and calculating the probability that our score C is greater than theirs
def win_probability(C):
    prob_beat_one=norm.cdf((C - dist_others) / std_others) #probability of beating one opponent
    return prob_beat_one ** number_others  #normal cdf gives the probability that a random variable from a normal distribution is less than a certain value. we want the probability that our score C is greater than theirs, so we use (C - dist_others) / std_others to standardize our score and then raise it to the power of number_others to get the probability that we beat all of them.

@lru_cache(maxsize=None)
#Bellman equation, R is number of red left, B is number of blue left, C is current score
def V(R,B,C):
    if R==0 and B==0:
        return win_probability(C)
    
    total=R+B
    ##red guesses
    RG=0    
    if R>0:
        RG+= (R/total)*V(R-1,B,C+1) # recursively calls V with one less red card and one more correct guess
    if B>0:
        RG+= (B/total)*V(R,B-1,C) # recursively calls V with one less blue card and same correct guesses

    #blue guesses
    BG=0
    if B>0:
        BG+= (B/total)*V(R,B-1,C+1) # recursively calls V with one less blue card and one more correct guess
    if R>0:
        BG+= (R/total)*V(R-1,B,C) # recursively calls V with one less red card and same correct guesses

    #the max of RG and BG will just choose whether to guess red or blue based on which has a higher expected value.
    return max(RG,BG)




def best_action(R, B, C):
    # exacft same as V but returns the action instead of the value
    if R == 0 and B == 0:
        return None

    total=R+B
    ##red guesses
    RG=0    
    if R>0:
        RG+= (R/total)*V(R-1,B,C+1) # recursively calls V with one less red card and one more correct guess
    if B>0:
        RG+= (B/total)*V(R,B-1,C) # recursively calls V with one less blue card and same correct guesses

    #blue guesses
    BG=0
    if B>0:
        BG+= (B/total)*V(R,B-1,C+1) # recursively calls V with one less blue card and one more correct guess
    if R>0:
        BG+= (R/total)*V(R-1,B,C) # recursively calls V with one less red card and same correct guesses

    return "R" if RG > BG else "B"


def simulation():
    #simulate with a shuffled deck of 26 red and 26 black cards
    deck = ['R'] * 26 + ['B'] * 26
    random.shuffle(deck)
    R,B=26,26
    C=0
    for card in deck:
        action=best_action(R, B, C)
        if action==card:
            C+=1
        if card=='R':
            R-=1
        else:
            B-=1   
    
    opponents = norm.rvs(loc=dist_others, scale=std_others, size=number_others)
    top = opponents.max()
    win=0
    if C > top:
        win= 1
    elif C == top:
        if random.random() < 1 / (1 + (opponents == top).sum()):
            win= 1
        else:
            win= 0
    return C,win


def runsimulation():
    my_scores = []

    wins=0
    for i in range(n):
        C, win = simulation()
        my_scores.append(C)
        wins += win
    win_rate = wins / n
    print(f"Monte Carlo win probability: {win_rate:.4f}")
    print(f"Mean score: {np.mean(my_scores):.2f}, Std: {np.std(my_scores):.2f}")


def plot_histogram(my_scores):
    plt.figure(figsize=(10,6))
    #plot my scores with bellman policy
    plt.hist(my_scores, bins=20, density=True, alpha=0.7, color='red', label='Bellman Policy Scores')
    #plot opponent mean and max as vertical lines (inputted at start, calculated beforehand through implementing opponent as guessing with probability)
    plt.axvline(28, color='blue', linestyle='--', label='Opponent mean (~28)')
    plt.axvline(31, color='black', linestyle='--', label='Opponent max (~31)')
    plt.xlabel("Correct guesses")
    plt.ylabel("Outcome Weight")
    plt.title("Monte Carlo Distribution of Final Scores (Bellman Policy)")
    plt.legend()
    plt.grid(True)
    plt.savefig("figures/bellman_histogram_opponent.png", dpi=300, bbox_inches="tight")
    plt.show()
def plotVsOpponentMax(my_scores): #plots bellman against opponent max distribution
    opp_max_scores = norm.rvs(loc=28, scale=3, size=(100_000, 10)).max(axis=1)
    plt.figure(figsize=(10, 6))

    # plot bellman distribution
    plt.hist(my_scores, bins=20, density=True, alpha=0.6, color='red', label='Your score distribution')

    # plot opponent max distribution
    plt.hist(opp_max_scores, bins=20, density=True, alpha=0.6, color='blue', label='Max opponent distribution')

    # vertical line of the means of opponent max and my average
    plt.axvline(np.mean(my_scores), color='red', linestyle='--', label=f"Your mean ≈ {np.mean(my_scores):.2f}")
    plt.axvline(np.mean(opp_max_scores), color='blue', linestyle='--', label=f"Opponent max mean ≈ {np.mean(opp_max_scores):.2f}")

    plt.title("Your Score Distribution vs. Opponent Max Distribution")
    plt.xlabel("Correct guesses")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.savefig("figures/bellman_hist_vs_opponentMax.png", dpi=300, bbox_inches="tight")
    plt.show()
def simulateBestPolicy():

    R_values = range(0, 27)   
    B_values = range(0, 27)
    grid = np.zeros((27, 27))
    for R in R_values:
        for B in B_values:
            if R + B == 0:
                continue
            action = best_action(R, B, 0)
            grid[R, B] = 1 if action == "R" else 0
    return grid
   
   
def heatMapOfBellman(grid):
    plt.figure(figsize=(8, 6))
    plt.imshow(grid, origin='lower', cmap='RdBu_r', extent=[0, 26, 0, 26])  #ibverted color map so red cards with red, black cards with blue
    plt.colorbar(label='Optimal Guess (0 = Black, 1 = Red)')
    plt.xlabel('Black cards remaining (B)')
    plt.ylabel('Red cards remaining (R)')
    plt.title('Bellman-Optimal Guess Policy')

    # decision boundary line to see where the bellman policy switches
    plt.contour(grid, levels=[0.5], colors='k', linewidths=2, extent=[0, 26, 0, 26])
    plt.savefig("figures/bellman_heatmap.png", dpi=300, bbox_inches="tight")
    plt.show()



print ("Win Probability with Bellman:", V(26,26,0)) #calculated via vectorized bellman equation

runsimulation()
my_scores = [simulation()[0] for i in range(n)]
plot_histogram(my_scores)
plotVsOpponentMax(my_scores)
grid=simulateBestPolicy()
heatMapOfBellman(grid)
