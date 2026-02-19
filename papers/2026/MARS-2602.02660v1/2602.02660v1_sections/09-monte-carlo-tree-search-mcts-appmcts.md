# Monte Carlo Tree Search (MCTS) {#app:mcts}

Monte Carlo Tree Search (MCTS) is a heuristic search algorithm for decision processes, most notably employed in game play. The algorithm builds a search tree where each node $v$ represents a state $s$, and each edge represents an action $a$ leading to a new state. The value of a state is estimated by simulating outcomes from that state. As shown in Algorithm [\[alg:mcts\]](#alg:mcts){reference-type="ref" reference="alg:mcts"}, each MCTS iteration consists of four distinct phases:

1.  **Selection:** Starting from the root node $v_0$, the algorithm recursively traverses down the tree by selecting child nodes according to a selection policy, typically aiming to balance exploration and exploitation. a common strategy is the Upper Confidence Bound for Trees (UCT) [@kocsis2006bandit]: $$\begin{align}
            a^* = \mathop{\mathrm{arg\,max}}_{a \in \mathcal{A}(s)} \left( Q(s, a) + c_{uct} \sqrt{\frac{\ln N(s)}{N(s, a)}} \right)
    \end{align}$$ where $Q(s, a)$ is the estimated value of taking action $a$ in state $s$, $N(s)$ is the total visit count of state $s$, $N(s, a)$ is the number of times action $a$ has been selected from $s$, and $c_{uct}$ is a constant controlling the exploration weight.

2.  **Expansion:** Once a leaf node $v_l$ is reached (or a node with unexplored actions), one or more child nodes are added to the tree, representing reachable states from standard actions.

3.  **Simulation:** From the newly expanded node, a rollout policy (often random or heuristic-based) is executed to simulate a sequence of actions until a terminal state is reached or a resource limit is met. This produces a reward $R$.

4.  **Backpropagation:** The reward $R$ obtained from the simulation is propagated back up the tree from the leaf to the root. For each node $(s, a)$ traversed during the selection phase, we update the visit count and value estimate as follows: $$\begin{align}
            N(s, a) &\leftarrow N(s, a) + 1 \\
            Q(s, a) &\leftarrow Q(s, a) + \frac{R - Q(s, a)}{N(s, a)}
    \end{align}$$

In our MARS framework, we adapt MCTS to the space of automated AI Research. A state $s$ corresponds to a partial or complete solution $s_n$, and actions correspond to modification operators (Drafting, Improvement, Debugging). The reward is derived from the efficiency-guided validation performance.

:::: algorithm
::: algorithmic
Task $\mathcal{P}$, Time Budget $T$. Best Solution Node $v^*$ Initialize root node $v_0$ with empty solution $v^* \leftarrow v_0$ $v_l \leftarrow \text{SELECT}(v_0)$ $v_{new} \leftarrow \text{EXPAND}(v_l)$ $R \leftarrow \text{SIMULATE}(v_{new})$ $\text{BACKPROPAGATE}(v_{new}, R)$ $v^* \leftarrow v_{new}$ **return** $v^*$
:::
::::
