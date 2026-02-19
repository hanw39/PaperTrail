# Experiment {#sec:exp}

## Setup

**Datasets.** We evaluate our agent on MLE-Bench [@chan2024mle], which consists of 75 challenging competitions from Kaggle, forming a diverse collection of tasks covering natural language processing, computer vision, and tabular data analysis.

**Environments.** We adhere to the standard MLE-Bench protocol, where agents are allocated a strict 24-hour wall-clock time budget per competition. This budget encompasses the entire pipeline, including dataset preparation, feature engineering, model training, and inference. The experiment for each agent on each competition is conducted on a standard node equipped with one NVIDIA A100 GPU (40GB), 12 vCPUs, 220 GB of RAM, and 1 TB of SSD storage. This setup simulates a realistic, resource-constrained machine learning engineering environment.

**Baselines.** We compare our method to the agents in the MLE-Bench leaderboard [^1] and two state-of-the-art open-source agents: AIDE [@aide2025] and AIRA [@toledo2025ai]. For open-source baselines, we ensure a strictly fair comparison by running them under identical environment configurations and using the same underlying LLMs.

**Metrics.** Following the standard MLE-Bench evaluation protocol, we report the mean and standard error of the mean (SEM) across three independent runs. Our evaluation focuses on three primary metrics: Above Median Rate (percentage of runs outperforming the median participant), Any Medal Rate (percentage achieving at least a Bronze medal), and Gold Medal Rate (percentage securing a Gold medal).

**Hyper-parameters for MARS.** We set the maximum number of lessons in the agent's memory to $K_m=30$ to maintain relevant context without context window overflow. We allow up to $N_d=10$ debugging actions per failure to resolve runtime errors effectively. The branching factor for valid nodes is set to $N_i=2$, balancing exploration breadth with depth. We set $w=-0.07$ in the reward function ([\[eq:reward\]](#eq:reward){reference-type="ref" reference="eq:reward"}) following [@tan2019mnasnet] to penalize excessive execution time (refer to Appendix [12.2](#app:hyperparam-w-ablation){reference-type="ref" reference="app:hyperparam-w-ablation"} for sensitivity analysis of $w$).

## Main Results

:::: table*
::: adjustbox
width=,center

+:-------------------------------------+:-----------------------+:---------------:+:--------------------------:+:--------------:+:--------------:+:--------------------------:+:--------------------------:+
| **Agent**                            | **Model**              |                 |                            |                |                |                            |                            |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **Submission**                       |                        |                 |                            |                |                |                            |                            |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **Median**                           |                        |                 |                            |                |                |                            |                            |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **Medal**                            |                        |                 |                            |                |                |                            |                            |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **Official MLE-Bench Leaderboard Results**                                                                                                                                                               |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **ML-Master [@liu2025ml]**           | Deepseek-R1            | $93.3 \pm 1.3$  | $44.9 \pm 1.2$             | $4.4 \pm 0.9$  | $7.6 \pm 0.4$  | $17.3 \pm 0.8$             | $29.3 \pm 0.8$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **R&D-Agent [@yang2025rdagent]**     | GPT-5                  | $53.3 \pm 0.0$  | $40.4 \pm 0.9$             | $6.7 \pm 1.5$  | $12.0 \pm 0.8$ | $16.4 \pm 0.9$             | $35.1 \pm 0.4$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **InternAgent [@team2025novelseek]** | Deepseek-R1            | $96.4 \pm 0.4$  | $48.4 \pm 1.2$             | $7.1 \pm 1.6$  | $10.7 \pm 0.8$ | $18.7 \pm 0.8$             | $36.4 \pm 1.2$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **Famou-Agent [@li2025fm]**          | Gemini-2.5-Pro         | $96.9 \pm 1.2$  | $51.6 \pm 1.2$             | $8.4 \pm 0.4$  | $12.4 \pm 1.9$ | $22.7 \pm 0.8$             | $43.6 \pm 0.9$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **Leeroo [@kapso2025]**              | Gemini-3-Pro-Preview   | $50.7 \pm 1.3$  | $50.7 \pm 1.3$             | $14.2 \pm 1.2$ | $15.1 \pm 0.9$ | $21.3 \pm 2.0$             | $50.7 \pm 1.3$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **ML-Master 2.0 [@zhu2026toward]**   | Deepseek-V3.2-Speciale | $95.6 \pm 1.2$  | $63.1 \pm 1.2$             | $11.1 \pm 0.4$ | $25.8 \pm 2.5$ | $19.6 \pm 0.9$             | $56.4 \pm 2.5$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **Controlled Evaluation in Our Environment**                                                                                                                                                             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **AIDE [@aide2025]**                 | Gemini-2.5-Pro         | $84.4 \pm 0.4$  | $40.0 \pm 0.8$             | $5.8 \pm 0.9$  | $4.9 \pm 1.2$  | $12.4 \pm 0.9$             | $23.1 \pm 0.4$             |
|                                      +------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
|                                      | Gemini-3-Pro-Preview   | $82.7 \pm 0.8$  | $48.0 \pm 0.0$             | $4.9 \pm 0.4$  | $11.1 \pm 1.2$ | $16.4 \pm 1.8$             | $32.4 \pm 2.5$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **AIRA-dojo [@toledo2025ai]**        | Gemini-2.5-Pro         | $83.6 \pm 2.4$  | $38.7 \pm 0.8$             | $2.7 \pm 0.8$  | $6.7 \pm 2.3$  | $15.1 \pm 1.2$             | $24.4 \pm 1.2$             |
|                                      +------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
|                                      | Gemini-3-Pro-Preview   | $98.2 \pm 1.2$  | $55.6 \pm 1.2$             | $5.8 \pm 1.9$  | $8.0 \pm 0.8$  | $24.0 \pm 1.5$             | $37.8 \pm 2.5$             |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **MARS (ours)**                      | Gemini-2.5-Pro         | $94.2 \pm 0.4$  | $52.4 \pm 0.9$             | $11.6 \pm 1.9$ | $12.4 \pm 0.9$ | $19.1 \pm 0.4$             | $43.1 \pm 1.6$             |
|                                      +------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
|                                      | Gemini-3-Pro-Preview   | $98.7 \pm 0.0$  | $\underline{65.8} \pm 1.6$ | $9.3 \pm 0.0$  | $15.6 \pm 1.2$ | $\underline{31.1} \pm 0.4$ | $\underline{56.0} \pm 1.5$ |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
| **MARS+ (ours)**                     | Gemini-3-Pro-Preview   | $100.0 \pm 0.0$ | $\textbf{74.2} \pm 0.9$    | $12.4 \pm 1.9$ | $16.4 \pm 1.2$ | $\textbf{33.8} \pm 0.4$    | $\textbf{62.7} \pm 0.8$    |
+--------------------------------------+------------------------+-----------------+----------------------------+----------------+----------------+----------------------------+----------------------------+
:::
::::

We compare MARS against state-of-the-art baselines in Table [\[tab:full-results\]](#tab:full-results){reference-type="ref" reference="tab:full-results"}. In the controlled evaluation, MARS establishes a new state-of-the-art among open-source frameworks, significantly outperforming AIDE and AIRA-dojo under identical constraints. When compared to the official leaderboard, our method remains highly competitive despite using significantly fewer resources (see Appendix [11](#app:leaderboard-setup){reference-type="ref" reference="app:leaderboard-setup"} for setup disparities). Notably, the standard MARS achieves the highest Gold Medal rate (31.1%) among all reported agents. To assess scalability, we evaluate **MARS+**, a variant configured to execute two concurrent search trees with increased compute (2$\times$H100 GPUs and 48 vCPUs). This scaled approach achieves the highest Above Median rate (74.2%), Gold Medal rate (33.8%), and Any Medal rate (62.7%), outperforming strong competitors like ML-Master 2.0. Finally, Table [1](#tab:split-results){reference-type="ref" reference="tab:split-results"} decomposes performance by task complexity, demonstrating that MARS consistently outperforms baselines across the Lite, Medium, and High splits.

::: {#tab:split-results}
+:-----------+:------------------+:--------------------------:+:--------------------------:+:--------------------------:+
| **Agent**  | **Model**         | **Any Medal**                                                                        |
|            |                   +----------------------------+----------------------------+----------------------------+
|            |                   | Lite (%)                   | Medium (%)                 | High (%)                   |
+------------+-------------------+----------------------------+----------------------------+----------------------------+
| **AIDE**   | Gemini-2.5-Pro    | $36.4 \pm 4.5$             | $18.4 \pm 2.6$             | $15.6 \pm 2.2$             |
|            +-------------------+----------------------------+----------------------------+----------------------------+
|            | Gemini-3-Pro-Prev | $53.0 \pm 6.1$             | $26.3 \pm 3.0$             | $17.8 \pm 2.2$             |
+------------+-------------------+----------------------------+----------------------------+----------------------------+
| **AIRA**   | Gemini-2.5-Pro    | $40.9 \pm 2.6$             | $16.7 \pm 3.5$             | $20.0 \pm 0.0$             |
+------------+-------------------+----------------------------+----------------------------+----------------------------+
| **-dojo**  | Gemini-3-Pro-Prev | $56.1 \pm 1.5$             | $29.8 \pm 3.8$             | $\underline{31.1} \pm 4.4$ |
+------------+-------------------+----------------------------+----------------------------+----------------------------+
| **MARS**   | Gemini-2.5-Pro    | $\underline{68.2} \pm 2.6$ | $\underline{33.3} \pm 1.8$ | $\underline{31.1} \pm 2.2$ |
+------------+-------------------+----------------------------+----------------------------+----------------------------+
| **(ours)** | Gemini-3-Pro-Prev | $\textbf{74.2} \pm 1.5$    | $\textbf{52.6} \pm 3.0$    | $\textbf{37.8} \pm 2.2$    |
+------------+-------------------+----------------------------+----------------------------+----------------------------+

: Controlled evaluation in our environment across different splits of MLE-Bench. Results are reported as mean $\pm$ SEM across three independent runs. The best performance is highlighted in **bold**, and the second-best is [underlined]{.underline}. The complete results including leaderboard results and other metrics are in Appendix [12.1](#app:complete-split-eval){reference-type="ref" reference="app:complete-split-eval"}.
:::

## Ablation Study

<figure id="fig:modular-lesson-ablation" data-latex-placement="htb">
<img src="./figures/module_lesson_ablation.png" style="width:60.0%" />
<figcaption>Impact of Modular Decomposition and Lesson Learning. </figcaption>
</figure>

<figure id="fig:tree-search-ablation" data-latex-placement="htb">
<img src="./figures/search_ablation.png" style="width:60.0%" />
<figcaption>Comparison of tree search strategies for MARS.</figcaption>
</figure>

We conduct ablation studies for MARS on the MLE-Bench Lite containing 22 competitions. Figure [3](#fig:modular-lesson-ablation){reference-type="ref" reference="fig:modular-lesson-ablation"} illustrates the performance of MARS versus variants lacking the Modular Decomposition or Lesson Learning component. The results demonstrate that both techniques significantly contribute to the agent's overall success. Figure [4](#fig:tree-search-ablation){reference-type="ref" reference="fig:tree-search-ablation"} compares different tree search algorithms for MARS. Greedy Search selects the node with the best validation metric for expansion at each step, while Vanilla MCTS is a variant of Budget-aware MCTS where $w=0$ in Eq ([\[eq:reward\]](#eq:reward){reference-type="ref" reference="eq:reward"}). The results indicate that the proposed Budget-Aware MCTS consistently yields superior performance over time compared to others, effectively balancing exploration with resource constraints.
