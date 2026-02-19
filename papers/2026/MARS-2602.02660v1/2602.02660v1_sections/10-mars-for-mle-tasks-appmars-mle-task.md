# MARS for MLE Tasks {#app:mars_mle_task}

:::: algorithm
::: algorithmic
**Input:** Task Description $I$, Raw Dataset $D$, Time Limit $T$ **Output:** Optimized solution code repository $s^*$ $d \gets \text{MetricParsing}(I)$ $\mathcal{C}_{meta} \gets \text{Preprocess}(D)$ $\mathcal{C}_{eda} \gets \text{Analyze}(I, D, \mathcal{C}_{meta})$ $\mathcal{C}_{model} \gets \text{SearchArchitectures}(I)$ $\mathcal{C} = \{ \mathcal{C}_{meta}, \mathcal{C}_{eda}, \mathcal{C}_{model} \}$ $v_{root} \gets \text{InitializeTree}()$ $v^* \gets \text{None}$ $\mathcal{L}_{solution} \gets \emptyset$ $\mathcal{L}_{debug} \gets \emptyset$ $\mathcal{Y} \gets \emptyset$ $v \gets \text{SelectNode}(v_{root})$ $Y \gets \text{ProposeIdea}(I, \mathcal{Y}, \mathcal{C}, \mathcal{L}_{solution})$ $Z \gets \text{ProposeModules}(I, Y)$ $\{\mathcal{M}_j\}_{j=1}^l \gets \text{ImplementModules}(I, Y, Z)$ $\{\mathcal{M}_j\}_{j=1}^l \gets \text{DebugModules}(I, \{\mathcal{M}_j\}_{j=1}^l)$ $\pi_{\text{main}} \gets \text{ImplementMainScript}(I, Y, \{\mathcal{M}_j\}_{j=1}^l)$ $v_{new} \gets \text{DraftNode}(\{\mathcal{M}_j\}_{j=1}^l, \pi_{\text{main}})$ $\mathcal{Y} \gets \mathcal{Y} \cup \{ Y \}$ $v_{new} \gets \text{ImproveNode}(v, \mathcal{L}_{solution})$ $k \gets 0$ $v_{new} \gets \text{DebugNode}(v_{new}, \mathcal{L}_{debug})$ $k \gets k + 1$ $r_{e} \gets \text{ExecuteAndReview}(v_{new})$ $\text{ExtractLesson}(v_{new}, r_{e}, \mathcal{L}_{solution})$ $\text{Backpropagate}(v_{new}, r_{e})$ $v^* \gets v_{new}$ $s^* \gets \text{GetRepoCode}(v^*)$ **return** $s^*$
:::
::::

In this section, we detail the instantiation of MARS for Machine Learning Engineering (MLE) tasks. The comprehensive procedure is formalized in Algorithm [\[alg:mars-mle\]](#alg:mars-mle){reference-type="ref" reference="alg:mars-mle"}. Corresponding instruction prompts for the agents involved are provided in Appendix [13](#app:agent-prompts){reference-type="ref" reference="app:agent-prompts"}.

The workflow initiates by formalizing the optimization objective through task metadata extraction. A *Metric Extraction Agent* parses the natural language task description $\mathcal{I}$ to identify the primary evaluation metric $M$ and the optimization direction $d \in \{\text{maximize}, \text{minimize}\}$.

Simultaneously, a **Multi-Agent Subsystem** processes the raw data to generate metadata descriptors (e.g., sample IDs) for the training ($D_{train}$), validation ($D_{val}$), and test ($D_{test}$) sets. These metadata descriptors are saved to files for later usage.

To ensure robust evaluation, we employ a strict protocol:

- **Validation Dataset Creation:** If a pre-defined validation set is not provided, the agent performs a stratified or group-based split (defaulting to a 80:20 ratio) on $D_{dev}$ to create $D_{train}$ and $D_{val}$. This ensures that $D_{val}$ maintains a distribution $P(D_{val}) \approx P(D_{train})$, enabling reliable proxy evaluation.

- **Verification & Documentation:** Distinct agents perform key integrity checks (e.g., no leakage between splits) and generate comprehensive documentation describing the data schema and split logic.

Following preparation, a *Data Analysis Agent* performs Exploratory Data Analysis (EDA) on $D_{train}$. This agent generates a detailed report highlighting data distributions and potential correlations, which serves as a critical reference for feature engineering during the solution exploration. Furthermore, a *Search Agent* identifies $K_a$ candidate model architectures across diverse algorithmic families (e.g., gradient-boosted trees, deep neural networks) using web search tools.

Once initialized, MARS enters an iterative Tree Search Stage. In each iteration, a node $v$ is selected via the Upper Confidence Bound for Trees (UCT) formula. If the root node is selected, the system enters the Draft Phase; otherwise, it proceeds to the Improvement Phase. Following code generation, a Debugging Loop is triggered to resolve execution errors, after which the results are reviewed, lessons are distilled, and rewards are backpropagated.

#### Drafting Phase.

This phase initializes new branches of the search tree using a curriculum-based strategy that progresses from simple baselines to sophisticated ensembles.

- **Initial Seed:** When the solution lesson pool $\mathcal{L}_{solution}$ is empty, an *Initial Idea Generation Agent* proposes a solution based on the most lightweight model from the $K_a$ candidates.

- **Evolutionary Growth:** As lessons accumulate, an *Idea Improvement Agent* formulates advanced proposals by integrating insights from $\mathcal{L}_{solution}$.

- **Modular Implementation:** A *Modular Agent* decomposes the proposed idea into independent functional units, which are implemented and unit-tested by a *Coding Agent* before being orchestrated into a final execution script $\pi_{\text{main}}$.

#### Improvement Phase.

This phase focuses on local optimization. An agent analyzes the current solution and its performance metrics to propose targeted, ablation-style modifications. By leveraging the learned lessons in $\mathcal{L}_{solution}$, the agent avoids previously identified pitfalls and focuses on high-impact refinements (e.g., hyperparameter tuning or feature engineering).

#### Debugging Phase.

If a candidate node $v_{new}$ fails execution, the system enters a debugging loop (up to $K_{debug}$ attempts). We maintain a dedicated debugging lesson pool $\mathcal{L}_{debug}$ to store error-correction patterns. This prevents the agent from repeating previous mistakes in subsequent iterations.
