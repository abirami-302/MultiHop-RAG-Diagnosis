# Reproducibility Guide & Data Audit Trail

This repository contains the complete empirical evaluation code, raw checkpoint data, and statistical testing scripts for:
**"Diagnosing the Multi-Hop Retrieval-Generation Gap: A Stage-Wise Empirical Study on HotpotQA"** (Abirami K, Madhumitha P S).

To guarantee full scientific integrity and independent auditability, **every number, confidence interval, and contingency count reported in the paper is deterministically re-derivable from the raw files committed in this repository.**

---

## 1. Traceability Matrix: Paper Tables to Raw Output Files

All raw evaluation files reside in the `OUT/` directory of this repository:

| Paper Table | Subject Matter | Exact Ground-Truth Source File | Key Code Execution Origin |
| :--- | :--- | :--- | :--- |
| **Table 1** | Stage-Wise Error Budget Decomposition | `OUT/results_overall.csv` | Computed from $S9\text{ (Oracle Ceiling)}$ minus $S8\text{ (Full Pipeline)}$ |
| **Table 2** | Multi-Stage Benchmark ($S0$–$S9$) | `OUT/results_overall.csv` | Notebook Step 8 & Step 10 (`summarize_df`) |
| **Table 3** | Marginal Point Gains ($\Delta\text{ pp}$) & McNemar Sig. | `OUT/results_overall.csv`, `OUT/tracker.csv` | Direct point differences; continuity-corrected McNemar tests |
| **Table 4** | Leave-One-Out Component Ablations | `OUT/results_overall.csv` (rows 10–12) | Notebook Step 9 (`Evaluating Ablations`) |
| **Table 5** | Paired Bootstrap Resampling ($B=10,000$, 95% CI) | `OUT/significance_all_sf.csv`, `OUT/significance_f1.csv` | Notebook Step 10 (`paired_bootstrap`, empirical percentiles) |
| **Table 6** | McNemar's Non-Parametric Paired Tests | `OUT/tracker.csv` | Discordant pair counts evaluated on `em` column |
| **Table 7** | Subgroup Depth Curves ($K \in \{5, 10, 25, 50\}$) | `OUT/depth_curve.csv` | Notebook Step 10 (`retrieve_bm25`, `dense`, `hybrid` over `eval_qs`) |
| **Table 8** | Multi-Hop Evidence Recovery Funnel | `OUT/tracker.csv` | Column `error_tag` (`Hop1_Pool`, `Hop2_Added`, `Never_Retrieved`) |
| **Figure 4** | Paired $2\times2$ Retrieval Contingency Matrix | `OUT/tracker.csv` | Paired cross-tabulation between $S8$ and $S5\_\text{Ctrl}$ on `all_sf` |
| **Table 9** | Generator Capacity Scaling (3B vs. 7B) | `OUT/tracker.csv` | Dual-model greedy generation over identical retrieved contexts |
| **Table 10** | Hardware Latency & Throughput Benchmark | Micro-benchmark log ($N=30$ queries) | Hardware profiling on dual NVIDIA Tesla T4 GPUs |
| **Table 11** | Hand-Verified Error Taxonomy ($N=60$) | Qualitative failure audit log | Blind hand-annotation across 60 randomly sampled $S8$ errors |

---

## 2. Experimental Specifications & Fixed Hyperparameters

To replicate exact numerical distributions, ensure the following parameters are enforced:

* **Random Seed:** `SEED = 42` (controls question sampling, corpus pooling, and initial rank shuffles).
* **Corpus Index Size:** $19,260$ unique passage titles (`pids` in `OUT/corpus.json`) drawn from $2,000$ sampled HotpotQA development set questions.
* **Evaluation Benchmark:** Fixed subset of $N=500$ questions (`OUT/eval_qs.json`):
  * Bridge queries: $n = 404$ ($80.8\%$)
  * Comparison queries: $n = 96$ ($19.2\%$)
* **Model Versions & Weights:**
  * Dense Retriever: `BAAI/bge-small-en-v1.5` (384-dimensional continuous vector embeddings, dot-product similarity).
  * Cross-Encoder Reranker: `BAAI/bge-reranker-base` (max sequence length = 256 tokens).
  * Primary Reader: `Qwen/Qwen2.5-3B-Instruct`.
  * Scaled Reader: `Qwen/Qwen2.5-7B-Instruct` (loaded in 4-bit precision via BitsAndBytes).
* **Decoding Parameters:** Greedy decoding (`do_sample=False`, `temperature=0.0`, `max_new_tokens=32`, repetition penalty = 1.0).
* **Hardware Environment:** Dual NVIDIA Tesla T4 GPUs ($2 \times 16\text{ GB}$ VRAM) on Google Cloud / Kaggle Linux container (CUDA 12.2, PyTorch 2.1+).

---

## 3. Step-by-Step Replication Protocol from Scratch

If running in a fresh Kaggle notebook or cloud GPU instance:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/abirami-302/MultiHop-RAG-Diagnosis.git
   cd MultiHop-RAG-Diagnosis
   ```

2. **Install Exact Dependencies:**
   ```bash
   pip install -q numpy pandas rank_bm25 sentence-transformers faiss-cpu tqdm torch matplotlib seaborn datasets bitsandbytes
   ```

3. **Execute Evaluation Pipeline:**
   Open `RAG_Research_Evaluation_Final.ipynb` and run Cells 1 through 10 sequentially:
   * **Step 3:** Automatically builds the 19,260-passage pooled corpus (`OUT/corpus.json`) and extracts the 500 evaluation questions (`OUT/eval_qs.json`).
   * **Step 4–6:** Precomputes the BM25 inverted index and dense FAISS index on GPU.
   * **Step 8:** Executes baseline systems $S0$ through $S9$, writing predictions and binary hits to `OUT/tracker.csv`.
   * **Step 9:** Runs leave-one-out ablations (`Abl_No_Reranker`, `Abl_Dense_Only`, `Abl_BM25_Only`).
   * **Step 10:** Runs 10,000 paired bootstrap iterations and exports `results_overall.csv`, `depth_curve.csv`, and all `significance_*.csv` files.

4. **Verify Table 2 & Table 3 Live:**
   You can verify all aggregate means by running:
   ```python
   import pandas as pd
   df = pd.read_csv('OUT/results_overall.csv')
   print(df.to_string())
   ```

---

## 4. Scientific Integrity Note: Historical Audit & S10 Removal

An earlier working draft of this repository contained an experimental configuration designated as **$S10$** (proposed as an LLM-generated sub-query reformulation baseline). 

During internal research auditing, it was discovered that:
1. System $S10$ was never formally executed on the Kaggle GPU cluster; its rows did not exist in `tracker.csv`.
2. The reported numeric values in the draft table were artificial mirror inversions of the real $S8\text{ vs. }S5$ difference row.
3. The narrative rationale claiming qualitative query drifting was unsupported by saved logs.

In accordance with strict scientific integrity standards:
* **System $S10$ was completely retracted and purged** from the manuscript, tables, and codebase.
* The paper replaced that subsection with the fully verified **3B vs. 7B Reader Scaling Diagnostic (Table 9)**, which is backed by real dual-model inference on identical retrieved contexts.
* This `REPRODUCIBILITY.md` document exists specifically to ensure that every remaining numeric claim in the manuscript maps directly to committed, re-runnable data.
