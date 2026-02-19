# Method {#sec:method}

<figure id="fig:method-overview" data-latex-placement="tb">
<embed src="./figures/MARS_teaser.pdf" />
<figcaption> Overview of the MARS Framework. MARS reformulates long-horizon coding as a search for an optimal software repository. (1) Task Preparation: The agent grounds the abstract problem (Instruction, Environment, Objective) tuple by exploratory analysis of the given dataset and metadata. (2) The MARS Loop: The agent iteratively evolves solutions through three synergistic modules: <strong>(A) Resource-Aware Planning:</strong> A Budget-Aware MCTS strategically navigates the search space by selecting actions from {Draft new architecture, Debug runtime errors, Improve a valid solution}. It optimizes an efficiency-guided reward that explicitly balances performance maximization with the penalty of high execution costs. <strong>(B) Modular Decomposition:</strong> To replace fragile monolithic scripting, the system employs a “Design-Decompose-Implement” pipeline. Specialized {Idea, Modular, Coding} agents architect the solution into independent, testable modules. This structure enables precise Diff-Based Refinement, allowing the agent to update specific logic blocks without regenerating the entire codebase. <strong>(C) Reflective Memory:</strong> This module distills raw execution logs into structured Debugging and Solution Lessons to proactively prevent error repetition and accelerate convergence in later iterations. </figcaption>
</figure>

## Overall Framework

We propose MARS, a general agent scaffolding framework designed to enable autonomous agents to solve long-horizon AI Research problems, as illustrated in Figure [2](#fig:method-overview){reference-type="ref" reference="fig:method-overview"}. Formally, we define the problem as a tuple $\mathcal{P} = (\mathcal{I}, \mathcal{E}, \mathcal{O})$, where the agent must follow the instruction $\mathcal{I}$ within an environment $\mathcal{E}$ to maximize an objective $\mathcal{O}$ under a cost budget $B$. To address the core challenges of exploration complexity, context management, and solution robustness in this setting, our framework integrates three key capabilities:

- **Modular Construction Strategy:** Instead of generating monolithic scripts, we enforce a structured, repository-level software architecture. This paradigm allows for handing complex logic with greater accuracy, efficient code reuse, and improving testability.

- **Reflective Memory:** To overcome context window limitations, we introduce a "Lesson Learning" mechanism that distills high-value insights from past interactions (both successes and failures) into a compact, retrievable knowledge base.

- **Resource-Aware Planning:** We employ a budget-aware Monte Carlo Tree Search (MCTS) algorithm to systematically explore the solution space. This allows the system to balance the exploitation of promising candidates with the exploration of novel ideas, preventing local optima, and penalize solutions that are costly.

## Modular Decomposition

A primary contribution of this work is the strategic shift from generating monolithic scripts to a Modular Implementation paradigm. This paradigm addresses several inherent limitations of LLM-based coding. First, it bypasses token output limits by distributing code across multiple files. Second, it enhances precision; by focusing on smaller logical units, the agent encounters less context noise and can handle complex logic with greater accuracy. Third, it enables efficiency via caching, as validated modules can be reused without regeneration. Finally, it significantly improves testability, as debugging is localized to specific files rather than requiring full-script diagnosis.

We define a node solution $s_n$ as a tuple comprising a set of $l$ independent modules and one orchestration script: $$\begin{align}
    s_n = \langle \{\mathcal{M}_j\}_{j=1}^l, \pi_{main} \rangle
\end{align}$$ Each module $\mathcal{M}_{j}$ encapsulates a specific sub-task (e.g., data preprocessing, configuration), while the main script $\pi_{\text{main}}$ orchestrates the end-to-end pipeline.

To instantiate this structure, we employ a three-stage "Design-Decompose-Implement" workflow:

- **Idea Generation:** An *Idea Generation Agent* articulates a comprehensive natural language plan covering various aspects of the solution.

- **Module Decomposition:** A *Modular Agent* parses the plan and decomposes the solution into logical, independent functional modules.

- **Component Implementation and Debugging:** A *Coding Agent* sequentially implements each module $\mathcal{M}_{j}$, employing a validation script to debug and verify functionality. Once validated, the agent orchestrates the modules via the main script $\pi_{\text{main}}$.

To prevent wasteful full-repository regeneration, we adopt a Diff-Based Editing mechanism. Code modifications are structured in a standardized diff format, specifying the target file, the block to replace, and the new code. This enables atomic, multi-file updates in a single inference step.

## Lesson Learning

Solving complex tasks requires long-horizon exploration, generating extensive interaction trajectories that often exceed context window constraints. More importantly, research progress is inherently iterative and opaque; when a new experiment yields improved results, isolating the specific causal factors remains a challenge. Standard memory-based agents often lack the mechanisms to solve this credit assignment problem, failing to learn effectively from past trials. To address this, we propose *Comparative Reflective Memory*, a mechanism designed to distill high-signal, causal insights from the exploration process into a compact lesson pool.

#### Solution Improvement via Comparative Reflection.

We employ a two-stage process to resolve the credit assignment problem by synthesizing lessons from valid solutions. First, an *Empirical Analysis Agent* reviews execution logs to extract objective findings (e.g., metric trends). Subsequently, a *Lesson Distillation Agent* performs a comparative reflection by analyzing the delta between the current solution and the previous best-known solution. This isolates the specific algorithmic changes driving performance shifts, resulting in a structured lesson containing: (1) The isolated causal change, (2) A comparative impact analysis, and (3) A generalized rule for future iterations.

#### Debugging Lessons.

For failed executions, a dedicated agent analyzes the buggy code, error logs, and the applied fix. It outputs a lesson confirming the fix's efficacy, explaining the failure logic, and providing guidelines to preemptively identify similar errors.

#### Lesson Management.

To maintain a high-signal lesson pool, a Review Agent evaluates new lessons against the existing pool through LLM-based reasoning, filtering out redundant insights to ensure the retrieved context remains diverse and relevant.

#### Lesson Utilization.

When executing solution improvement or debugging actions, the agent utilizes relevant knowledge from the corresponding lesson categories. We retain the $K_m$ most recent lessons in the agent's memory to manage context. To ensure interpretability, the agent is instructed to explicitly cite specific lessons whenever they are applied.

## Budget-Aware MCTS

We adopt the Monte Carlo Tree Search (MCTS) framework to explore the solution space, which iterates through four phases: Selection, Expansion, Simulation, and Backpropagation. In this section, we detail our domain-specific modifications: (1) specialized expansion operators, (2) a coherent node selection strategy, and (3) an *Efficiency-Guided Reward Function* that balances performance with cost. Appendix [9](#app:mcts){reference-type="ref" reference="app:mcts"} provides a review of standard MCTS principles.

### Actions and Expansion {#sec:mcts_expansion}

We define three distinct operators to transform a parent state $s_{parent}$ into a child solution $s_{new}$:

- **Drafting (Root Expansion):** Generates a completely new solution $s_{new}$ from scratch.

- **Improvement:** Applied to valid, executable nodes. The agent modifies the modules and the main script from $s_{parent}$ to maximize the objective $\mathcal{O}$.

- **Debugging:** Applied to nodes where execution failed. The agent inherits the solution structure from $s_{parent}$ but modifies specific modules or the orchestration script to resolve runtime errors. Buggy children enter an automatic debugging loop with up to $N_d$ debugging actions to fix the errors.

### Node Selection

We employ the Upper Confidence Bound for Trees (UCT) algorithm to navigate the solution space, balancing the exploitation of high-performing solutions with the exploration of new solutions.

The selection phase begins at the root node. In each step, we select the child node that maximizes the UCT value. This traversal continues recursively until we identify a candidate node, defined as a node that is not yet "fully expanded".

The root node is set fully expanded unless any of the follow condition occurs: (1) It does not have any children; (2) the best solution has not been improved after implementing $n_s$ valid nodes.

If the traversal reaches a leaf node that is already fully expanded (it implies that no further debugging or improvement is permitted for that branch), then the root node is re-activated to allow for new drafts.

The buggy nodes are always set fully expanded. The valid nodes are set fully expanded if they have $\ge N_i$ children (attempts to improve).

### Efficiency-Guided Reward Function

To guide the search efficiently, we design a reward function $R(v)$ that rewards performance gains and penalizes long execution time. Let $M(v)$ denote the performance metric of a node $v$, and let $t(v)$ and $L(v)$ represent its execution time and time limit, respectively. We first normalize the performance metric relative to the history of explored nodes $\mathcal{V}$. Let $M_{max} = \max_{v' \in \mathcal{V}} M(v')$ and $M_{min} = \min_{v' \in \mathcal{V}} M(v')$. We define the global normalized score $G(v)$ as:

$$\begin{align}
    G(v) := 
\begin{cases} 
0.5 \quad \text{if } M_{max} = M_{min}, \\
\frac{M(v) - M_{min}}{M_{max}-M_{min}} \quad \text{otherwise}
\end{cases}
\end{align}$$

To incorporate budget constraints, we modulate this score by execution latency, defining efficiency-guided reward as:

$$\begin{align}
    \label{eq:reward}
    R(v) := G(v) \cdot [t(v) / L(v)]^{w}
\end{align}$$

Where $w$ is a penalty weight hyperparameter. A similar function has been proposed in [@tan2019mnasnet].

## Task Specific Components {#sec:task_specific}

While MARS is a general framework, its application requires task-specific components. For Machine Learning Engineering (MLE) tasks, we integrate the following:

**Task preparation.** We employ a multi-agent system to extract task metadata, formalizing the optimization objective and preparing training, validation, and test datasets.

**Data analysis.** We employ an agent to perform Exploratory Data Analysis (EDA) to generate a report that guides downstream feature engineering.

**Curriculum-Based Exploration.** We implement a curriculum-based idea generation strategy that progressively explores simple baselines to complex methods.

Refer to the Appendix [10](#app:mars_mle_task){reference-type="ref" reference="app:mars_mle_task"} for the details.
