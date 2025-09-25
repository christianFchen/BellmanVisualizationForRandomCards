\documentclass[12pt]{article}
\usepackage{amsmath, amssymb, graphicx, hyperref, geometry}
\geometry{margin=1in}

\title{Optimal Guessing Strategy Using Markov Decision Processes and Monte Carlo Simulation}
\author{Quantitative Strategy Project}
\date{\today}

\begin{document}
\maketitle

\section*{Problem Statement}

\textbf{Quantitative Question:}  
Suppose you are playing a game against ten other opponents with a standard deck of 52 cards (26 red, 26 black).  
Cards are drawn one by one, and before each draw, you and your opponents guess the card's color.  

\begin{itemize}
    \item You do not know what your opponents guess.
    \item You see the color of each card after it is drawn and know if your guess was correct.
    \item The player with the most correct guesses wins \$1,000. 
    \item If multiple players tie for the highest score, the winner is chosen randomly.
\end{itemize}

\textbf{Objective:} Develop a strategy that maximizes your probability of winning and estimate the success rate of that strategy.

\section*{Methodology}

We model this sequential decision-making problem as a \textbf{Markov Decision Process (MDP)} and solve it using \textbf{dynamic programming (Bellman recursion)}. The approach is then validated through \textbf{Monte Carlo simulation} against probabilistic opponents.

\subsection*{State Space and Actions}

We define the state as:
\[
S = (R, B, C)
\]
where:
\begin{itemize}
    \item $R$: number of red cards remaining
    \item $B$: number of black cards remaining
    \item $C$: current number of correct guesses
\end{itemize}

The possible actions are:
\[
A \in \{\text{Guess Red}, \text{Guess Black}\}
\]

\subsection*{Transition Dynamics}

The state transitions depend on the true color drawn (revealed only after guessing), updating $R$, $B$, and $C$ accordingly. The process continues until $R + B = 0$ (i.e., the deck is exhausted).

\section*{Bellman Optimality Equation}

The Bellman value function is defined as:

\[
V(R, B, C) = 
\begin{cases}
P(\text{win} \mid C) & \text{if } R + B = 0 \\
\max \{ V_{\text{red}}, V_{\text{black}} \} & \text{otherwise}
\end{cases}
\]

Where:

\[
V_{\text{red}} = \frac{R}{R + B} V(R-1, B, C + 1) + \frac{B}{R + B} V(R, B - 1, C)
\]
\[
V_{\text{black}} = \frac{B}{R + B} V(R, B - 1, C + 1) + \frac{R}{R + B} V(R - 1, B, C)
\]

The optimal policy chooses the action that maximizes expected winning probability at each state.

\section*{Opponent Modeling}

Opponents are modeled as probabilistic guessers with approximately Gaussian-distributed scores:
\[
\text{Score} \sim \mathcal{N}(28, 3^2)
\]
With 10 opponents, the expected maximum score is approximately:
\[
E[\max] \approx 30.8 - 31.0
\]

\section*{Monte Carlo Simulation}

We run $100,000$ simulations of the game under the Bellman-optimal policy:

\begin{enumerate}
    \item Randomize the deck order and simulate guesses using the optimal policy.
    \item Generate opponent scores from $\mathcal{N}(28, 3^2)$.
    \item Compute the probability of beating the highest opponent score.
\end{enumerate}

\section*{Results}

\begin{table}[h]
\centering
\begin{tabular}{l|c}
\textbf{Metric} & \textbf{Value} \\
\hline
Mean correct guesses (optimal policy) & $\approx 29.0$ \\
Standard deviation & $\approx 2.2$ \\
Monte Carlo win probability & $\approx 0.17 - 0.20$ \\
Expected opponent max score & $\approx 30.8 - 31.0$ \\
\end{tabular}
\end{table}

\textbf{Interpretation:}  
Even with optimal play, variance dominates the outcome. However, the Bellman policy improves win probability from roughly 10–12\% (random guessing) to 17–20\%.

\section*{Strategy Breakdown}

\begin{itemize}
    \item \textbf{Early Game:} Induce variance by occasionally guessing the minority color to diverge from common strategies.
    \item \textbf{Mid Game:} Guess based on conditional probabilities to maximize expected correct guesses.
    \item \textbf{End Game:} 
    \begin{itemize}
        \item If ahead: Play conservatively, following the majority probability.
        \item If behind: Increase variance by consistently guessing the minority color.
    \end{itemize}
\end{itemize}

\section*{Results and Visualizations}

\subsection*{1. Monte Carlo Score Distribution}

The histogram below shows the distribution of total correct guesses across 100,000 Monte Carlo simulations under the Bellman-optimal policy. The dashed vertical lines indicate the expected opponent mean (~28) and the approximate expected maximum score (~31) among 10 competitors.

\begin{figure}[h!]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/bellman_hist_vs_opponentMax.png}
    \caption{Monte Carlo distribution of total correct guesses under the Bellman-optimal policy.}
    \label{fig:histogram}
\end{figure}

\clearpage

\subsection*{2. Score Distribution vs. Opponent Maximum}

This plot compares the distribution of our final scores (red) to the distribution of the maximum opponent score (blue). Although our optimized policy shifts the mean score upward, the heavy right tail of the opponent distribution highlights the inherent variance-driven nature of this problem.

\begin{figure}[h!]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/bellman_histogram_opponent.png}
    \caption{Comparison of our score distribution (red) with the distribution of the maximum opponent score (blue).}
    \label{fig:opponent}
\end{figure}

\clearpage

\subsection*{3. Bellman-Optimal Policy Heatmap}

The heatmap below illustrates the decision boundary of the Bellman-optimal policy. Each cell corresponds to a state defined by the number of red ($R$) and black ($B$) cards remaining. 
Red regions indicate that guessing red maximizes expected value, while blue regions indicate that guessing black is optimal.

\begin{figure}[h!]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/bellman_heatmap.png}
    \caption{Decision boundary of the Bellman-optimal policy. Red indicates an optimal red guess; blue indicates an optimal black guess.}
    \label{fig:heatmap}
\end{figure}

\section*{Conclusion}

This project demonstrates how Markov Decision Processes and Bellman dynamic programming can be used to solve a high-variance, competitive guessing game. Despite the stochastic nature of the problem, an optimal decision policy significantly increases the probability of winning against probabilistic opponents.

\section*{Code and Resources}

All source code, visualizations, and simulation results are available in the GitHub repository. Plots and data are generated automatically and stored in the \texttt{figures/} directory.

\section*{Dependencies}

The project requires the following Python packages:
\begin{verbatim}
numpy
scipy
matplotlib
yfinance
\end{verbatim}

\end{document}
