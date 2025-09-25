# Optimal Guessing Strategy Using Markov Decision Processes and Monte Carlo Simulation

## Problem Statement

**Quantitative Question:**  
You are playing a game against 10 opponents with a standard 52-card deck (26 red, 26 black).  
Cards are drawn one by one, and before each draw, you and your opponents guess the card's color.

- You do not know what your opponents guess.  
- You see the color of each card after it is drawn and whether your guess was correct.  
- The player with the most correct guesses wins \$1,000.  
- In case of a tie, the winner is chosen at random.

**Objective:**  
Develop a strategy that maximizes your probability of winning and estimate the success rate.

---

## Methodology

We model this sequential decision-making problem as a **Markov Decision Process (MDP)** and solve it using **dynamic programming (Bellman recursion)**.  
We then validate the approach using **Monte Carlo simulation** against probabilistic opponents.

---

## State Space and Actions

We define the state:

$$
S = (R, B, C)
$$

Where:

- $R$: number of red cards remaining  
- $B$: number of black cards remaining  
- $C$: current number of correct guesses

The possible actions are:

$$
A \in \{\text{Guess Red}, \text{Guess Black}\}
$$

---

## Transition Dynamics

The state transitions depend on the true color drawn (revealed after guessing), updating $R$, $B$, and $C$ accordingly.  
The process continues until $R + B = 0$.

---

## Bellman Optimality Equation

The Bellman value function is defined as:

$$
V(R, B, C) =
\begin{cases}
P(\text{win} \mid C) & \text{if } R + B = 0 \\
\max \{ V_{\text{red}}, V_{\text{black}} \} & \text{otherwise}
\end{cases}
$$

Where:

$$
V_{\text{red}} = \frac{R}{R + B} V(R - 1, B, C + 1) + \frac{B}{R + B} V(R, B - 1, C)
$$

$$
V_{\text{black}} = \frac{B}{R + B} V(R, B - 1, C + 1) + \frac{R}{R + B} V(R - 1, B, C)
$$

The optimal policy selects the action that maximizes $V(R, B, C)$ at every state.

---

## Opponent Modeling

Opponents are modeled as probabilistic guessers with Gaussian-distributed scores:

$$
\text{Score} \sim \mathcal{N}(28, 3^2)
$$

With 10 opponents, the expected maximum score is approximately:

$$
\mathbb{E}[\max] \approx 30.8 - 31.0
$$

---

## Monte Carlo Simulation

We simulate $100{,}000$ games under the Bellman-optimal policy:

1. Shuffle and draw cards sequentially.
2. Use the Bellman-optimal action at each state.
3. Sample opponent scores from $\mathcal{N}(28, 3^2)$.
4. Estimate the probability that our score exceeds the opponent's maximum.

---

## Results

| Metric | Value |
|--------|-------|
| Mean correct guesses (optimal policy) | ~29.0 |
| Sta
