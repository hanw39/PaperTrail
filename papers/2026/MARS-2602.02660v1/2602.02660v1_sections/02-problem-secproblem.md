# Problem {#sec:problem}

We first formalize the general problem of *Long-Horizon Agentic Problem Solving*, where an autonomous agent is tasked with constructing a complex artifacts (e.g., a software system) to satisfy a set of requirements within a constrained budget. Let $\mathcal{P}$ denote a problem instance defined by the tuple $\mathcal{P} = (\mathcal{I}, \mathcal{E}, \mathcal{O})$, where: (1) $\mathcal{I}$ represents the *Instruction* or requirements provided in natural language. (2) $\mathcal{E}$ denotes the *Environment* with which the agent interacts to validate its solutions. This can be a compiler, a simulator, or a dataset depending on the task scenario. (3) $\mathcal{O}$ is the *Objective* function that quantifies the quality of the solution.

The goal is to find a solution $s^*$ that maximizes $\mathcal{O}$ by interacting with $\mathcal{E}$, subject to a cost constraint $B$ (e.g., time budget or monetary cost): $$\begin{align}
    s^* = \mathop{\mathrm{arg\,max}}_{s} \quad \mathcal{O}(s, \mathcal{E}), \quad s.t. \quad \text{Cost}(s) \leq B
\end{align}$$ where the search space for $s$ is often vast and unstructured (e.g., the space of all possible Python programs).

#### MLE Task Scenario.

Machine Learning Engineering (MLE) is a representative and challenging instantiation of this general problem class. MLE requires the agent to engineer a full pipeline that processes data, trains models, and validates results. In this scenario, $\mathcal{E}$ consists of the provided datasets while $\mathcal{O}$ is the performance metric (e.g. accuracy) on the held-out test set. Refer to Appendix [8](#app:mle-task){reference-type="ref" reference="app:mle-task"} for details.
