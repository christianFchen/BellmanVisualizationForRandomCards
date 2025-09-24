# BellmanVisualizationForRandomCards
Given a deck of 26 red and 26 black cards, what would be an optimal way of guessing cards against 10 other players to win (have more than them)?

I have modeled the Bellman equation in this scenario (without a discounted factor because it does not apply) and calculated our expected value of winning. I chose not to do a Monte Carlo simulation with hypothetical guesses and other outliers for opponents' guesses because this seemed like a more concrete way to represent my strategy.
