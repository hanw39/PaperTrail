# Prompts {#app:agent-prompts}

This section provides the full suite of instruction prompts utilized by MARS to orchestrate the various agents involved in solving MLE tasks.

::: promptbox
Metric Parsing Instruction

    ==== Task ====
    Your task is to analyze the provided problem description to identify the primary evaluation metric and determine if a lower score indicates better performance. Your response must be in a specific JSON format with the following fields:
    - metric_name (string): This field specifies the name of the primary evaluation metric.
    - lower_is_better (boolean): This field indicates whether the metric should be minimized. If a lower value of the metric represents better performance (e.g., for Mean Squared Error), set this to true. If a higher value represents better performance (e.g., for accuracy), set this to false.

    # Response Format
    Your response should be in the following JSON format in a single markdown code block (wrapped in ```):
    ```json
    {{
        "metric_name": "accuracy",
        "lower_is_better": false,
    }}
    ```
:::

::: promptbox
Metadata Generation Instruction

    ==== Task ====
    Your task is to write a Python script that generates three metadata files for the training, validation, and test datasets respectively. This metadata (e.g., sample IDs, file paths, labels) will be used by other scripts to load data efficiently.

    # Requirements
    - The script's only responsibility is to generate metadata. It should not perform any model training or inference.
    - The script must read raw data from the `./input` directory. This directory should be treated as read-only.
    - All generated metadata files (e.g., .csv, .parquet, .json) must be saved directly to the `./metadata` directory.
    - You must not copy or move the original raw data. The `./metadata` directory should only contain the newly generated metadata files.
    - All file paths stored within the metadata must be relative to the `./input` directory. Review the Dataset Information section above to identify the correct file paths and structure.
    - The metadata for the training and validation datasets must include the ground-truth labels.
    - Create a validation set by splitting the training data only if a separate validation dataset is not already available.
        - Use a fixed 80:20 ratio (80% training and 20% validation). This ratio should not be a user-configurable argument.
        - Randomly shuffle the training data before splitting. To ensure the split is reproducible, use a fixed random state (`RANDOM_STATE = 42`).
        - Apply stratified sampling or group sampling to ensure the validation dataset's distribution properly represents the original data.
            - Stratified Sampling: Use this if it's a classification task, stratifying by the target label.
            - Group Sampling: Use this if the data has inherent groups (e.g., patient IDs, user IDs) that must not be split across the train and validation sets.
    - After generating the metadata, the script must immediately load the datasets using the new metadata and perform the following checks:
        - Print summary statistics for the final training, validation, and test datasets (e.g., total number of samples, class distributions, data shapes, number of unique users, etc.).
        - If the metadata contains file paths, programmatically check 1000 relative file paths randomly selected from each of the metadata files. Calculate the ratio of paths that do not resolve to an existing file in `./input`. If this "missing file ratio" is greater than 0.5, the script must raise an error. Before raising the error, print a sample (e.g., the first five) of the non-resolving file paths to the console for debugging purposes.
        - If a new validation set was created, you must programmatically verify that it satisfies the requirements.
            - Assert that the stratification or group split was successful.
            - Raise an error (e.g., AssertionError) if these verification checks fail.

    # Implementation Guideline
    - The code should be a single-file python program that is self-contained and can be executed as-is.
    - The script must be complete and able to run from start to finish without premature termination or skipped sections.
    - Your response should only contain a single code block.
    - All validation checks must fail explicitly, either by raising an Exception or triggering an AssertionError.
    - Do not use `try ... except` blocks to suppress or ignore errors in your code examples.
    - Be aware of the running time of the code, it should complete within {exec_timeout}.
    - All the provided input data is stored in "./input" directory. There is no need to unzip any files.
:::

::: promptbox
Validation Dataset Verification Instruction

    ==== Task ====
    Analyze the provided Python script and its execution output to verify if the validation dataset was handled or created successfully.

    # Python Script
    {code}

    # Execution Output
    {term_out}

    # Requirements
    You must review the script and output based on the criteria below. Your entire response must be a single JSON code block.

    - Success Criteria: The success field must be set to True if one of the following two conditions is met. Otherwise, set it to False.
        1. Existing Validation Set: The script correctly identifies that a separate validation dataset is already available in the raw data (i.e., no new split is required).
        2. Created Validation Set: The script correctly creates a new validation set by splitting the training data. \
    Your analysis must confirm that the script's logic properly attempts to create a representative split (e.g., by using stratified or group sampling).
    - JSON Response Format: Provide your review in the following JSON format.
        - analysis (string): A concise rationale for your decision.
            - If successful: Explain which of the two success criteria was met.
            - If failed: Briefly explain why the script failed to meet either criterion (e.g., "The script split the data randomly instead of using stratification.").
        - success (bool): True if the validation dataset was handled or created successfully, False otherwise.

    # Response Format
    The review must be submitted in the following JSON format in a single markdown code block (wrapped in ```):
    ```json
    {{
        "analysis": "The validation dataset was not created successfully. The script split the training data but did not use stratified sampling, failing to create a representative sample.",,
        "success": false,
    }}
    ```
:::

::: promptbox
Metadata Documentation Instruction

    ==== Task ====
    Your task is to analyze the provided Python script and its execution output to create clear documentation for each file generated in the `./metadata` directory.

    # Python Script
    {code}

    # Execution Output
    {term_out}

    # Requirements
    For each file generated in the `./metadata` directory, provide a detailed breakdown covering:
    - Content and Purpose:
        - Describe the information or data contained within the file (e.g., "Contains image_id, file_path, and label for the training set.").
        - Explain its primary purpose (e.g., "This file is used by the data loader to find image files and match them with their correct labels.").
    - Schema / Structure: Detail the structure, such as column names, data types, and an example row if applicable.
    - Loading Method: Explain the standard method or library function required to load this file (e.g., "Load with pandas.read_csv()" or "Load with joblib.load()").
:::

::: promptbox
Exploratory Data Analysis Instruction

    ==== Task ====
    Your task is to write a robust Python script to perform an Exploratory Data Analysis (EDA) on the training dataset. The script must adapt its analysis based on the data modality (Tabular, Image, Audio, or Text). The output should act as a report to inform feature engineering and preprocessing strategies.

    # Requirements
    1. Data Integrity: Ensure all analysis is strictly performed on the training set to prevent data leakage.
    2. Target Variable Analysis
    - Distribution: Calculate the distribution of the target variable.
    - Imbalance/Skew:
        - If Classification: Calculate class balance ratios.
        - If Regression: Calculate Skewness and Kurtosis to assess normality.
    3. Input Data Analysis (Modality-Specific)
    - If Tabular Data:
        - Numerical: Report mean, std, min, max, and outlier counts (IQR method).
        - Categorical: Report cardinality; flag columns with > 50 categories or rare labels (< 1 percent frequency).
        - Missing Values: Report count/percentage of NaNs per column.
    - If Image Data:
        - Dimensions: Analyze distributions of Image Widths, Heights, and Aspect Ratios.
        - Channels: Report the distribution of channel counts (e.g., Grayscale vs. RGB).
        - Pixel Stats: Calculate the global mean and standard deviation of pixel values (for normalization).
    - If Audio Data:
        - Signal: Analyze distributions of Duration (seconds), Sampling Rates, and Bit Depths.
        - Channels: Check for mono vs. stereo inconsistency.
    - If Text Data:
        - Lengths: Analyze distribution of sequence lengths (character and word counts).
        - Vocabulary: Report unique vocabulary size and OOV (Out of Vocabulary) potential.
    4. Feature/Signal Relationships
    - Structured (Tabular) Relationships:
        - Correlation: Pearson/Spearman for numerical; Mutual Information for categorical.
        - Importance: Train a lightweight Random Forest and report top 5 features.
        - Redundancy: Report collinear pairs (Correlation > 0.90).
    - Unstructured (Meta-Feature) Relationships: Analyze the relationship between metadata and the target (e.g., "Do longer audio files correlate with specific classes?", "Are larger images associated with higher regression targets?").
    5. Formatting & Output
    - Organize the output into distinct, capitalized sections.
    - Use f-strings to format floats to 4 decimal places for readability.
:::

::: promptbox
Model Architecture Search Instruction

    ==== Task ====
    Your task is to propose {num_model_candidates} distinct model architectures to solve the problem. **Action:** Use Google Search to research state-of-the-art and efficient architectures relevant to this domain.

    # Requirements
    - **Broad Diversity:** The candidates must represent different algorithmic families. Do not propose multiple variations of the same underlying method (e.g., do not suggest two different ResNets). Aim for a mix of:
        * Instance-Based / Kernel Methods (e.g., k-NN, SVM)
        * Tree-Based Ensembles (e.g., LightGBM, XGBoost, CatBoost)
        * Deep Learning (e.g., CNN, MLP, Transformers, RNNs)
    - **Problem Alignment:** Architectures must be specifically tailored to the data modality (e.g., tabular, image, time-series) and input structure.
    - **Hybridization:** Incorporate hybrid or ensemble designs if they offer a clear advantage for heterogeneous data.
    - **Efficiency First:** Prioritize "lightweight" designs. For each family, choose the architecture that offers the best trade-off between low computational cost (fast training/inference) and high performance.
    - **Data Constraints:** If the training data is limited, explicitly address regularization or low-complexity designs to prevent overfitting.
    - For each model, create a JSON object with the following two keys:
        - `reasoning`: Justification for why this architecture fits the constraints (efficiency, data size, and why it was chosen over others in its category).
        - `description`: A technical description of the architecture and design philosophy.

    # Response Format
    Your response should be in the following JSON format in a single markdown code block (wrapped in ```):
    ```json
    [
        {{"reasoning": "k-NN is small and efficient...", "description": "We can use K-NN for this task..."}},
        {{"reasoning": "CNN is effective and efficient...", "description": "We can use CNN for this task..."}},
        {{"reasoning": "GBMs is an effective model...", "description": "We can use GBMs for this task..."}},
    ]
    ```
:::

::: promptbox
Initial Idea Proposal Instruction

    ==== Model Architectures ====
    {model_arch_desc}

    ==== Previous Ideas ====
    {previous_ideas}

    ==== Task ====
    Your task is to propose a highly efficient **baseline approach** to solve the problem. 

    # Requirements
    - Novelty: The proposed solution must remain strictly distinct from the approaches listed in Previous Ideas.
    - Model Design: Synthesize a simple and lightweight architecture using the provided Model Architectures as a conceptual foundation. Ensure the design is unique and has not been suggested in the Previous Ideas.
    - Philosophy: Prioritize speed and simplicity over maximum accuracy. Exclude resource-intensive techniques, such as heavy augmentations or ensembles, to establish a reliable performance baseline.

    # Response Format
    Your solution must be outlined in natural language without using code or specific implementation details. Your response should cover the following aspects:
    - Model: Describe the model architecture's design and key components.
    - Data: Describe the necessary steps to preprocess data for both training and evaluation.
    - Training: Outline the training procedure, including key techniques (e.g., loss functions, optimizers, or training strategies).
    - Evaluation: Describe the process for generating predictions on the test data.
:::

::: promptbox
Idea Improvement Instruction

    ==== Previous Ideas ====
    {previous_ideas}

    ==== Lessons ====
    {lessons}

    ==== Task ====
    Using the insights from the lessons learned during solution development, your task is to propose an optimized strategy to solve the problem more effectively. You must synthesize the provided "Lessons" to propose a structural evolution of the "Previous Ideas".

    # Requirements
    - Structural Innovation (Exploration): Do not propose trivial hyperparameter tuning. You must introduce a fundamental change (e.g., a new backbone architecture, a multi-stage pipeline, or a distinct feature engineering paradigm) to address identified weaknesses.
    - Strategic Retention (Exploitation): Explicitly preserve components identified as successful in the "Lessons". Do not discard what is already working.
    - Computational Budget: The solution is allowed to be moderately heavier than previous ideas (e.g., using a stronger backbone), but it must remain feasible for standard training environments.
    - Citation: Whenever you apply a specific concept or solution from these lessons, you must immediately reference it by appending "Cite {{lesson_id}}" to the relevant statement.

    # Response Format
    Your solution must be outlined in natural language without using code or specific implementation details. Your response should cover the following aspects:
    - Model: Describe the model architecture's design and key components.
    - Data: Describe the necessary steps to preprocess data for both training and evaluation.
    - Training: Outline the training procedure, including key techniques (e.g., loss functions, optimizers, or training strategies).
    - Evaluation: Describe the process for generating predictions on the test data.
:::

::: promptbox
Modular Decomposition Instruction

    ==== Idea ====
    {idea}

    ==== Task ====
    Your task is to design a modular repository structure to implement the given idea. Do not generate the full code yet; focus on the natural description of the **architectural logic**.

    # Requirements
    - **Modularity:** Break the solution into logical modules based on functionality (e.g., data handling, core training and evaluation logic, utilities).
    - **Entry Point:** You must include a `main` module that acts as the entry point to execute the end-to-end pipeline.
    - **Detail:** For each module, the description must include:
        - The purpose of the module.
        - The names of specific classes or functions to be implemented.
        - A brief description of the implementation logic.
        - A brief explanation of how this module interacts with others.
    - **Ordering:** The JSON output must be ordered topologically (dependencies first, dependent modules last).

    # Response Format
    Provide the output strictly as a JSON object in a single markdown code block. The keys should be the module names and the values should be the detailed descriptions. The module name must not include the `.py` extension.

    Example Format:
    ```json
    {{
        "module_name": "Implements [Specific Class] to handle [Specific Task]. includes functions like [func_a] and [func_b].",
        "main": "Orchestrates the workflow. Imports DataLoader from the data module and Model from the model module to run the pipeline."
    }}
    ```
:::

::: promptbox
Module Implementation Instruction

    ==== Idea ====
    {idea}

    ==== Python Files ====
    The following Python files are already provided. Do not modify them.
    {library_files}

    ==== Target File Description ({file_name}) ====
    {file_description}

    ==== Task ====
    Your task is to implement the `{file_name}` module based on the description above.

    # Requirements
    - Import the functions or classes from the given Python files instead of re-implementing them.
    - Only implement the module class/functions. DO NOT include an if `__name__ == "__main__":` block. DO NOT implement the end-to-end pipeline.
    - Ensure functions accept arguments for flexibility. You must include hyperparameters to control dataset size (for debugging) and training steps/epochs.
    - When printing validation metrics, please print the full precision without any rounding or formatting.
    - If loading raw data, use the metadata in `./metadata` to identify the correct train/val/test splits.
    - If this module performs deterministic data processing, you must implement a caching mechanism strictly following this logic:
        - **Function Signature:** The processing function must accept a `load_cached_data: bool` argument.
        - **Directory Safety:** Ensure the directory `./working/{dir_name}/` exists (use `os.makedirs(..., exist_ok=True)`).
        - **Prohibited:** Do NOT use `pickle`. Use `parquet` (via pandas) or `npy` (via numpy).
        - **Logic Flow:**
            1. IF `load_cached_data` is True: Try to load the file.
            2. IF loading fails (file missing or corrupt) OR `load_cached_data` is False:
                - Compute/process the data from scratch.
                - Save the result to the cache directory `./working/{dir_name}/` for future runs.
            3. Return the data.
    - If this module handles model training:
        - **Metrics:** Print key training and validation metrics during training process.
        - **Optimization:** Implement Early Stopping to prevent overfitting and reduce runtime.
    - If this module handles submission generation:
        - Generate predictions for the entire test set. Save the final predictions to `./submission/submission.csv`.
        - Refer to the sample submission file (e.g., `./input/sample_submission.csv` or `./input/sampleSubmission.csv`) for the correct formatting required by the competition.
:::

::: promptbox
Module Testing Instruction

    ==== Python Files ====
    The following Python files are already provided. Do not modify them.
    {library_files}

    ==== Task ====
    Your task is to write code examples demonstrating how to instantiate and utilize the classes or functions from the provided Python files.

    # Requirements
    - Optimize for Speed: Limit hyperparameters (e.g., reduce the number of epochs/steps, use a smaller dataset subset) to ensure the demonstration executes quickly.
    - Verify Logic: Include assertions or validation steps to confirm the correctness of complex classes and functions. \
    You may skip verification for trivial components, such as configuration classes.
:::

::: promptbox
Solution Drafting Instruction

    ==== Idea ====
    {idea}

    ==== Python Files ====
    The following Python files are already provided. Do not modify them.
    {library_files}

    ==== Target File Description (`runfile.py`) ====
    {file_description}

    ==== Task ====
    Your task is to implement the end-to-end orchestration script `runfile.py`. This script serves as a **fast baseline** to verify the idea. It must train the model, validate performance, perform failure analysis, and generate a submission.

    # Requirements
    - Import the functions or classes from the given Python files instead of re-implementing them.
    - Make the model training fast.
        - Limit maximum number of training samples and training steps/epochs to ensure a quick baseline execution.
        - Set appropriate batch sizes to prevent CUDA out-of-memory errors.
    - After training is complete, you must execute validation assessment, failure analysis, and submission generation.
        - You must load the hold-out validation dataset using the metadata located in the `./metadata` directory.
        - You must print the final validation metric computed on the entire hold-out validation set in this format `Final Validation Metric: <value>`. Without this metric, the solution cannot be evaluated, rendering the entire code invalid. You must use the validation metric defined in the Task Description. Please print the full precision of the validation metric without any rounding or formatting.
        - You must perform failure analysis on the trained model. You must perform failure analysis on the validation set to identify systematic error patterns. Calculate and print the correlation between the model's error magnitude and the input features to reveal which variables are most associated with poor performance.
        - You must generate predictions for the entire test set and create the submission file{submission_cond}. Save the final predictions to `./submission/submission.csv`. Refer to the sample submission file (e.g., `./input/sample_submission.csv` or `./input/sampleSubmission.csv`) for the correct formatting required by the competition.
    - Optimize the validation inference speed.
        - Ensure the model is in evaluation mode for this inference.
        - Your code must automatically detect and utilize an available GPU for inference. Ensure the model and all data batches are moved to the correct device (GPU or CPU).
        - During inference, you don't need to compute gradients. Disabling this process reduces memory consumption and speeds up computation.
    - Call data loading functions with `load_cached_data=True` (if applicable) to utilize preprocessed data in the `./working` directory.
:::

::: promptbox
Solution Improvement Instruction

    ==== Lessons ====
    {lessons}

    ==== Previous Solution ====
    {previous_solution}

    ==== Task ====
    Your task is to modify the Python files from the previous solution to optimize performance.

    # Requirements
    - Modifications must be targeted and specific (ablation-style). Do not rewrite the entire solution; focus on isolating and improving specific aspects.
    - You should apply the relevant knowledge provided in the Lessons section to support your optimization strategy. Whenever you apply a specific concept or solution from these lessons, you must immediately reference it by appending "Cite {{lesson_id}}" to the relevant statement.
    - Optimize hyperparameter settings (e.g., training steps, learning rate, batch size) to strike the best balance between predictive performance and execution speed.
    - **Do not remove** the following core logic from the original `runfile.py` script:
        - Print the final validation metric computed on the entire hold-out validation set.
        - Perform failure analysis on the trained model.
        - Generate predictions for the entire test set and create the submission file{submission_cond}.
:::

::: promptbox
Bug Analysis Instruction

    ==== Debug Lessons ====
    {lessons}

    ==== Python Files ====
    The following Python files are already provided.
    {files}

    ==== Task ====
    You are tasked with debugging a script failure. You should summarize the execution traceback and explain the root cause of the errors. You should apply the relevant knowledge provided in the Debug Lessons section to support your diagnosis. Whenever you apply a specific concept or solution from these lessons, you must immediately reference it by appending "Cite {{lesson_id}}" to the relevant statement. You can use Google Search as needed for debugging.

    Execution Traceback (`python runfile.py`):
    {exec_result}
:::

::: promptbox
Debugging Instruction

    ==== Debug Lessons ====
    {lessons}

    ==== Python Files ====
    The following Python files are already provided. Do not modify them.
    {files}

    ==== Task ====
    We ran this command (`python runfile.py`) and got some errors.

    Execution Traceback:
    {exec_result}

    Error analysis:
    {error_analysis}

    Your task is to revise the given Python files to fix the errors based on the provided error analysis. You can use Google Search as needed for debugging.

    # Requirements
    - You should write a brief natural language description of what the issue in the previous implementation is and how the issue can be fixed.
    - The fix must be targeted. Do not change the core logic or intended functionality of the original code; only correct the specific implementation error shown in the Execution Traceback.
    - You should apply the relevant knowledge provided in the Debug Lessons section to guide your fixes. Whenever you apply a specific concept or solution from these lessons, you must immediately reference it by appending "Cite {{lesson_id}}" to the relevant statement.
    - Do not use `try...except` blocks to catch, suppress, or ignore the original error. The fix must address the root cause of the problem.
:::

::: promptbox
Debugging Lesson Distillation Instruction

    You are an expert Python debugger and instructor. Your task is to analyze a debugging attempt and distill a high-value "Lesson Learned".

    # Input
    Initial State:
    {source_files}

    Initial Execution Traceback:
    {source_exec_result}

    Initial Error analysis:
    {source_error_analysis}

    Attempted Fix (Diff):
    {diff}

    Execution Traceback after applying the fix:
    {final_exec_result}

    # Guidelines
    - Determine if the Attempted Fix resolved the Initial Error based on the Result of Fix.
    - If the fix SUCCEEDED: Explain the root cause of the initial error and why this specific fix was the correct solution.
    - If the fix FAILED: Explain why the attempted fix was insufficient, incorrect, or introduced new issues. The lesson must focus on avoiding this specific pitfall.

    # Response Format
    - Title: A concise, imperative, and memorable summary of the lesson.
    - Explanation: A clear paragraph synthesizing the error context. Describe the specific mechanism of the failure and the logic required to fix it.
    - Detection: How to identify this issue in the future. List specific signals, such as particular Exception types, stack trace patterns, or code smells.
:::

::: promptbox
Execution Result Review Instruction

    ==== Python Files ====
    The following Python files are already provided.
    {library_files}

    ==== Task ====
    Your task is to evaluate the output of the code execution for the provided code and report the empirical findings. The review must be submitted in a specific JSON format with the following fields:
    - summary (string): In this field, provide a brief summary describing the empirical findings. This must include:
        - The training loss trend (e.g., did it converge/minimize?).
        - Failure analysis.
        - The final validation metric.
        - The reasoning for your `valid_metric` assessment (e.g., "The final validation metric is valid," or "The final validation metric is invalid due to validation data leakage...").
    - metric (number or null): Report the value of the validation metric here. You must convert percentages to decimals (e.g., 95% -> 0.95). This should be null if the metric cannot be found or determined.
    - valid_metric (boolean): Set to `true` if the final validation metric is valid. Set to `false` if any of the following conditions are met:
        - The computed final validation metric does not match the one defined in the Task Description.
        - The final validation metric is calculated incorrectly.
        - The final validation metric is not computed on the entire hold-out validation set.
        - There are signs of validation data leakage (e.g., the validation set was used in training).

    Code:
    ```
    {code}
    ```

    Execution Output:
    {term_out}

    # Response Format
    The review must be submitted in the following JSON format in a single markdown code block (wrapped in ```):
    ```json
    {{
        "summary": "The code trains a model to solve the task... The final validation metric is ...",
        "metric": 0.99,
        "valid_metric": true,
    }}
    ```
:::

::: promptbox
Solution Lesson Distillation Instruction

    ==== Current Best Solution ====
    {best_solution}

    ==== New Solution ====
    {new_solution}

    ==== Task ====
    Your task is to analyze the provided solutions to distill a high-value "Lesson Learned".

    # Guidelines
    - **Check Context:**
       - If *Current Best Solution* exists: Comparative Analysis. Contrast the algorithmic approach of the New vs. Current. Explain precisely *why* the New Solution improves or degrades performance based on the execution results.
       - If *Current Best Solution* is missing: Empirical Analysis. Summarize the findings and effectiveness of the New Solution based on its execution results.
    - **Logic over Syntax:** Focus on algorithmic choices, data structures, and architectural decisions. Ignore minor syntactic sugar unless it affects performance.
    - **Causal Chain:** Trace the logic to prove exactly how the new approach resolves the specific bottleneck.
    - **Generalizability:** The final lesson must be abstract enough to apply to similar problems in the future, not just this specific snippet.

    # Response Format
    - Title: A clear, memorable title for the lesson.
    - Summary: A brief, high-level overview of the methods or algorithmic changes applied in the New Solution.
    - Empirical Findings: Analysis of the execution results. If comparing, highlight the delta in performance (validation metric and execution time) and the specific trade-offs observed.
    - Key Lesson: A standalone, actionable principle. Write this as a heuristic or rule of thumb (e.g., "When handling sparse matrices, prefer X over Y because..."). If a developer reads *only* this paragraph, they should learn a technique to apply in their own work.
:::

::: promptbox
Lesson Deduplication Instruction

    You are a Machine Learning Engineer responsible for maintaining a knowledge base of technical lessons.

    ==== Existing Lessons ====
    {existing_lessons}

    ==== New Lesson ====
    {new_lesson}

    ==== Task ====
    Your task is to determine if the **New Lesson** is semantically equivalent to any of the **Existing Lessons**.

    ### Guidelines
    - **Semantic Overlap:** A lesson is a duplicate if the core insight, principle, or actionable advice is effectively the same, even if the wording differs.
    - **Subsets:** If the **New Lesson** is fully covered by a broader existing lesson, count it as a duplicate.
    - **Novelty:** If the **New Lesson** provides a specific nuance, edge case, or context not covered by existing lessons, it is **not** a duplicate.

    # Response Format
    Provide your analysis in a single valid JSON object inside a single markdown code block (wrapped in ```).

    **Fields:**
    - `reasoning` (string): Briefly explain your decision. If a duplicate exists, explicitly quote or summarize the specific existing lesson that overlaps.
    - `duplicate` (boolean): Use `true` if it is a duplicate, `false` otherwise.

    **Example Output:**
    ```json
    {{
        "reasoning": "The lesson is the same as one of the existing lessons.",
        "duplicate": true
    }}
    ```
:::
