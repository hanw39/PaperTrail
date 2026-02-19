# Discussions {#sec:discussion}

#### How does Modular Decomposition impact solution complexity?

We investigate whether Modular Decomposition facilitates the construction of complex solutions for each task. Table [2](#tab:modular-decomposition-analysis){reference-type="ref" reference="tab:modular-decomposition-analysis"} compares the repository statistics of MARS with and without modular decomposition for the best solution. The results show that the modular approach encourages the generation of more extensive and structured codebases (measured by lines of code and number of files in the best solution). To illustrate this structural adaptability, Table [\[tab:competition-modules\]](#tab:competition-modules){reference-type="ref" reference="tab:competition-modules"} enumerates the specific modules synthesized for five representative competitions. The diversity of these modules -- tailored to specific sub-tasks such as preprocessing and model architecture -- demonstrates the agent's ability to decompose intricate problems into logical components. This capacity to architect organized, repository-level solutions closely mirrors professional software engineering workflows.

::: {#tab:modular-decomposition-analysis}
  **Metric**         **MARS without Modular**       **MARS**
  ----------------- -------------------------- -------------------
  Lines of Code          $474.8 \pm 13.5$       $1103.9 \pm 35.9$
  Number of Files         $1.0 \pm 0.0$           $6.7 \pm 0.1$

  : Comparison of repository statistics between MARS and the variant without Modular Decomposition on MLE-Bench Lite.
:::

:::: table*
::: adjustbox
width=,center

  **Competition**                                                                     **Modules**
  ----------------------------------------------- ------------------------------------------------------------------------------------
  aptos2019-blindness-detection                                        dataset.py, engine.py, model.py, utils.py
  jigsaw-toxic-comment-classification-challenge          data_processing.py, model_definitions.py, training_engine.py, utils.py
  us-patent-phrase-to-phrase-matching                 config.py, cpc_utils.py, dataset.py, engine.py, loss.py, model.py, utils.py
  h-and-m-personalized-fashion-recommendations       config.py, data_factory.py, embedder.py, features.py, ranker.py, retrieval.py
  multi-modal-gesture-recognition                  config.py, data_loader.py, inference.py, losses.py, model.py, trainer.py, utils.py
:::
::::

<figure id="fig:reward-example" data-latex-placement="htb">
<embed src="./figures/reward-example.pdf" style="width:60.0%" />
<figcaption>Reward modulation: Budget-aware MCTS assigns higher rewards to faster candidates when performance is comparable.</figcaption>
</figure>

#### Does Budget-aware MCTS improve exploration?

We examine whether Budget-aware MCTS discovers high-quality solutions more frequently than the Vanilla MCTS. We define the effective solution rate as the proportion of explored solutions that improve upon the current best validation metric per task. Empirically, Budget-aware MCTS achieves an effective solution rate of $19.5\% \pm 1.5\%$, notably higher than the $16.1\% \pm 1.3\%$ observed with Vanilla MCTS. This suggests that the latency penalty acts as a heuristic to prune inefficient trajectories. As illustrated in Figure [5](#fig:reward-example){reference-type="ref" reference="fig:reward-example"}, when the agent encounters solutions with comparable accuracy but differing costs, our efficiency-guided reward favors the faster candidate. This bias directs computational resources toward efficient nodes, accelerating the discovery of optimal solutions within the time limit.

#### How lessons guide the evolution process?

We examine the role of Lesson Learning in guiding the agent's solution exploration. Figure [1](#fig:aha-moment){reference-type="ref" reference="fig:aha-moment"} illustrates an example where the agent formulates lessons from early failures or partial successes and applies them to refine subsequent solutions. To quantify this behavior, we introduce two metrics: the lesson-utilization rate (the proportion of solutions that incorporate existing lessons) and the lesson-transfer rate (the proportion of utilized solution lessons originating from a different tree branch). MARS achieves a lesson-utilization rate of $65.8\% \pm 1.1\%$ and a lesson-transfer rate of $63.0\% \pm 1.8\%$ on MLE-Bench. These results demonstrate that the agent actively leverages learned knowledge and cross-branch transfer to steer the search toward high-quality strategies.

<figure id="fig:plagiarism-detection" data-latex-placement="htb">
<img src="./figures/similarity_scores_distribution.png" style="width:60.0%" />
<figcaption>Distribution of maximum code similarity scores for medal-winning submissions from AIRA-dojo and MARS, compared against top public Kaggle notebooks.</figcaption>
</figure>

#### Does MARS follow the MLE-Bench rules?

To verify compliance, we employ the official MLE-Bench log analysis tool, which utilizes gpt-4.1-mini to audit the logs and code outputs of all medal-winning submissions. The evaluation confirms that MARS strictly adheres to the protocol, registering a 0% violation rate across all monitored dimensions, including "Tried to access unauthorized resources", "Tried to call external LLM API service", and "Manually-written submission". Furthermore, we assess code originality using the provided plagiarism detection tool based on Dolos [@maertens2024discovering]. We calculate the maximum similarity score between our agent's code -- concatenated into a single file for multi-module repositories -- and the top public notebooks for each competition. As shown in Figure [6](#fig:plagiarism-detection){reference-type="ref" reference="fig:plagiarism-detection"}, the similarity distribution of MARS mirrors that of the baseline AIRA-dojo. Crucially, no submission exceeds a 60% similarity threshold, demonstrating that MARS generates distinct, original solutions rather than reproducing existing public code.

#### Cost Analysis.

As detailed in Appendix [12.3](#app:cost-analysis){reference-type="ref" reference="app:cost-analysis"}, MARS incurs a higher cost per task due to the maintenance of a comprehensive memory context (\$39.0 for AIRA-dojo vs \$60.5 for MARS). However, this investment yields substantial returns: the Any Medal Rate nearly doubles from $24.4\%$ for AIRA-dojo to $43.1\%$ for MARS, justifying the expense through superior efficacy.
