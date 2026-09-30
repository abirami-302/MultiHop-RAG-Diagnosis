# Diagnosing the Multi-Hop Retrieval-Generation Gap

[![GitHub Pages](https://img.shields.io/badge/Live-Interactive_Dashboard-blue.svg)](https://abirami-302.github.io/MultiHop-RAG-Diagnosis/)
[![Benchmark](https://img.shields.io/badge/HotpotQA-N%3D500-green.svg)](#)
[![Dual GPU](https://img.shields.io/badge/Hardware-Kaggle_Dual_T4-orange.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Paper Headline:**  
> *"On HotpotQA (N=500, 19,260-passage corpus), a cross-encoder reranker yields the single largest retrieval gain (+15.4 pp AllSF@5), while iterative Hop-2 adds a modest +2.8 pp that is borderline significant on retrieval and does not translate to significant EM gains. Even with gold passages, a 3B reader reaches only 53.0% EM; scaling the reader to 7B improves EM by +12.2 pp on identical retrieved evidence, establishing that the downstream system is primarily reader-and-metric-bound rather than retrieval-bound."*

---

## 🌐 Live Interactive Results Dashboard
👉 **View the complete interactive tables with color-coding and filters on GitHub Pages: [abirami-302.github.io/MultiHop-RAG-Diagnosis](https://abirami-302.github.io/MultiHop-RAG-Diagnosis/)**

## 🔬 Reproducibility & Audit Trail
- **[REPRODUCIBILITY.md](REPRODUCIBILITY.md)**: Full verification guide mapping every paper table directly to raw output files in `OUT/` (`tracker.csv`, `results_overall.csv`, `depth_curve.csv`), exact hyperparameter specs, Kaggle dual-T4 replication instructions, and formal data integrity audit notes.
- **[CHANGELOG.md](CHANGELOG.md)**: Transparent revision history and audit record (including the formal retraction and removal of the unverified S10 exploratory trial).
- **Raw Execution Outputs**: All 500-question itemized logs and prediction records are preserved in `OUT/tracker.csv`, making every percentage and statistical claim in the paper directly and independently auditable.

---

# Empirical Diagnostic Evaluation Suite

---

## 1. Central Diagnostic: Stage-Wise Error Budget Decomposition (Table 0)
*Decomposition of performance deficit against a theoretical 100.0% ceiling across N=500 questions*

| Metric & Decomposition Component | Qwen-2.5-3B Architecture | Qwen-2.5-7B Architecture | Diagnostic Interpretation |
| :--- | :---: | :---: | :--- |
| **EM: Retrieval Loss** (Oracle Ceiling − S8 Pipeline) | **13.20 pp** | **8.20 pp** | Deficit attributable to missing evidence in retrieved context |
| **EM: Reader & Metric Loss** (100.0% − Oracle Ceiling) | **47.00 pp** | **39.80 pp** | Deficit under gold evidence (reasoning failure + surface-form artifacts) |
| **Retrieval Share of Total EM Deficit** | **21.9%** | **17.1%** | **>78% of downstream failure is reader-and-metric-bound** |
| **F1: Retrieval Loss** (Oracle Ceiling − S8 Pipeline) | **15.66 pp** | **10.78 pp** | Token-level overlap lost due to distractor noise |
| **F1: Reader & Metric Loss** (100.0% − Oracle Ceiling) | **33.20 pp** | **24.90 pp** | Token-level overlap lost under perfect gold passages |
| **Retrieval Share of Total F1 Deficit** | **32.0%** | **30.2%** | **~70% of F1 deficit is reader-bound or metric artifact** |

> **Key Finding on Reader-Retriever Interaction:** The retrieval-induced loss contracts from 13.20 pp on 3B to 8.20 pp on 7B. A stronger reader model is more robust to distractor noise, demonstrating that retrieval quality becomes less of a limiting factor as reader parameterization increases.

---

## 2. Multi-Stage Pipeline Architecture Evaluation (Table 1)
*Evaluated on N=500 questions across 19,260 passages (Context budget $K=5$, unless noted; Qwen-2.5-3B-Instruct)*

| System Configuration | Context ($K$) | AllSF@K (%) | SF Recall@K (%) | MRR | Exact Match EM (%) | F1 Score (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S0: Closed-Book Floor** | 0 | 0.00% | 0.00% | 0.00 | 13.60% | 17.86% |
| **S1: BM25 Okapi** | 5 | 46.80% | 70.20% | 0.84 | 30.80% | 40.36% |
| **S2: Dense BGE-Small** | 5 | 70.60% | 84.40% | 0.93 | 36.80% | 47.11% |
| **S3: Hybrid RRF Fusion** | 5 | 67.20% | 82.50% | 0.90 | 33.60% | 43.88% |
| **S5: Hybrid + Cross-Encoder Reranker (Pool=25)** | 5 | 82.60% | 91.00% | 0.97 | 38.80% | 49.15% |
| **S5_Ctrl: Fair Pool-50 Control** | 5 | 82.80% | 91.20% | 0.97 | 38.80% | 49.31% |
| **Ctrl_SinglePass_K10** | 10 | 81.00%* | 90.10% | 0.90 | 38.60% | 48.44% |
| **S7: Dense Iterative Hop-2** | 5 | 72.80% | 84.90% | 0.93 | 37.60% | 49.20% |
| **S8: Staged Multi-Hop Pipeline** | **5** | **85.60%** | **92.60%** | **0.97** | **39.80%** | **51.14%** |
| **S9: Oracle Ceiling (Gold Evidence)** | **Gold** | **100.00%** | **100.00%** | **1.00** | **53.00%** | **66.80%** |

*\*Note on Ctrl_SinglePass_K10 and Context Budget:* Unreranked hybrid at a context budget of K=10 achieves 38.60% EM, essentially matching reranked K=5 (38.80%), versus 33.60% for unreranked hybrid at K=5. This demonstrates that giving the reader twice the passage window (10 vs 5 passages) yields similar downstream gains to neural reranking. A reranked K=10 configuration was not evaluated. Its MRR of 0.90 reflects unreranked candidate positioning vs 0.97 for cross-encoder reranked stages.

*Note on System IDs:* S4, S6, and S10 represent exploratory experimental variants (intermediate pool trials and LLM query reformulation substitution) evaluated in scratch trajectories and omitted from primary benchmark rows to maintain clean pipeline progression.

---

## 3. Marginal Gains of Staged Pipeline (S8) over Baselines (Table 1b)
*Direct Point Differences (Δ pp) across retrieval and answer accuracy*

| Baseline System | Baseline AllSF@5 | S8 AllSF@5 | Retrieval Gain (Δ pp) | Baseline EM | S8 EM | EM Gain (Δ pp) | McNemar Sig. (Holm) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **vs. S1 (BM25 Okapi)** | 46.80% | **85.60%** | **+38.80 pp** | 30.80% | **39.80%** | **+9.00 pp** | *Not tested in paired m=6* |
| **vs. S2 (Dense BGE-Small)** | 70.60% | **85.60%** | **+15.00 pp** | 36.80% | **39.80%** | **+3.00 pp** | **No (p = 0.516)** |
| **vs. S3 (Hybrid RRF)** | 67.20% | **85.60%** | **+18.40 pp** | 33.60% | **39.80%** | **+6.20 pp** | **Yes (p = 0.0059)** |
| **vs. S5 (Hybrid + Rerank)** | 82.60% | **85.60%** | **+3.00 pp** | 38.80% | **39.80%** | **+1.00 pp** | **No (p = 0.851)** |
| **vs. S5_Ctrl (Pool-50 Ctrl)**| 82.80% | **85.60%** | **+2.80 pp** | 38.80% | **39.80%** | **+1.00 pp** | **No (p = 0.851)** |
| **vs. S7 (Iterative Dense)** | 72.80% | **85.60%** | **+12.80 pp** | 37.60% | **39.80%** | **+2.20 pp** | **No (p = 0.851)** |

---

## 4. Component Ablation on S8 (Table 2)
*Leave-one-out component removals (Reference S8 = 85.60% AllSF@5 | 51.14% F1 | 39.80% EM)*

| Ablation Variant | Component Removed | AllSF@5 (%) | Δ AllSF (pp) | F1 Score (%) | Δ F1 (pp) | EM (%) | Diagnostic Finding |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **S8 Staged Pipeline** | None (Full Pipeline) | **85.60%** | — | **51.14%** | — | **39.80%** | Full staged architecture reference |
| **Abl_No_Reranker** | Minus Cross-Encoder Reranker | 63.00% | **-22.60 pp** | 45.82% | **-5.32 pp** | 35.80% | **Reranker is linchpin ($p < 0.001$)**; drops below single-pass hybrid (67.2%) |
| **S5_Ctrl_Pool50** | Minus Hop 2 (Single-Pass) | 82.80% | **-2.80 pp** | 49.31% | **-1.83 pp** | 38.80% | Hop-2 adds modest +2.8 pp AllSF ($p_{\text{holm}} = 0.048$, borderline) |
| **Abl_BM25_Only** | Minus Dense (BM25 only) | 80.40% | **-5.20 pp** | 51.39% | **+0.25 pp** | 40.40% | Dense improves all-facts recall; no downstream benefit |
| **Abl_Dense_Only** | Minus BM25 (Dense only) | 85.60% | **0.00 pp** | 51.38% | **+0.24 pp** | 40.00% | **Dense matches S8 ($p = 1.0$)**; BM25 redundant once reranked |

> **Finding on Abl_No_Reranker:** Without a cross-encoder reranker, S8 drops to 63.00% AllSF@5, which is *below* unreranked single-pass hybrid S3 (67.20%). This observation is consistent with distractor noise introduced by snippet-augmented iterative queries when left unfiltered by neural reranking.

---

## 5. Paired Bootstrap Statistical Significance (Table 3a)
*B=10,000 resamples | 95% Confidence Intervals | Explicit Family-Wise Error Rate Control via Holm-Bonferroni*

| Comparison Pair | Target Metric | S8 Score | Baseline Score | Mean Diff (%) | 95% Bootstrap CI | Raw $p$ | Holm $p$ | Significant (α=0.05)? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Family 1: Primary Retrieval Coverage (AllSF@5, m=8 tests; Raw p < 0.0001 represents bootstrap floor 1/(B+1))** | | | | | | | | |
| **S8 vs S2_Dense** | AllSF@5 | 85.60% | 70.60% | **+15.00%** | $[+11.20, +19.00]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs S3_Hybrid** | AllSF@5 | 85.60% | 67.20% | **+18.40%** | $[+14.60, +22.20]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs S5_Hybrid_Rerank** | AllSF@5 | 85.60% | 82.60% | **+3.00%** | $[+1.40, +4.80]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs S7_Iterative_Dense** | AllSF@5 | 85.60% | 72.80% | **+12.80%** | $[+8.60, +17.00]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs Abl_No_Reranker** | AllSF@5 | 85.60% | 63.00% | **+22.60%** | $[+18.60, +26.80]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs Abl_BM25_Only** | AllSF@5 | 85.60% | 80.40% | **+5.20%** | $[+3.00, +7.40]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs S5_Ctrl_Pool50** | AllSF@5 | 85.60% | 82.80% | **+2.80%** | $[+0.40, +5.20]$ | 0.0240 | **0.0480** | **Yes (Borderline)** |
| **S8 vs Abl_Dense_Only** | AllSF@5 | 85.60% | 85.60% | **0.00%** | $[-2.00, +2.00]$ | 1.0000 | **1.0000** | **No** |
| **Family 2: Downstream Generation Overlap (F1, m=5 tests)** | | | | | | | | |
| **S8 vs S3_Hybrid** | F1 | 51.14% | 43.88% | **+7.26%** | $[+3.82, +10.73]$ | < 0.0001 | **0.0005** | **Yes** |
| **S8 vs Abl_No_Reranker** | F1 | 51.14% | 45.82% | **+5.32%** | $[+1.78, +8.92]$ | 0.0024 | **0.0096** | **Yes** |
| **S8 vs S5_Hybrid_Rerank** | F1 | 51.14% | 49.15% | **+1.98%** | $[+0.50, +3.59]$ | 0.0070 | **0.0210** | **Yes** |
| **S8 vs S2_Dense** | F1 | 51.14% | 47.11% | **+4.03%** | $[+0.45, +7.58]$ | 0.0280 | **0.0560** | **No** |
| **S8 vs S5_Ctrl_Pool50** | F1 | 51.14% | 49.31% | **+1.83%** | $[-0.08, +3.82]$ | 0.0594 | **0.0594** | **No** |

---

## 6. McNemar's Paired Non-Parametric Test on Exact Match (Table 3b)
*Continuity-corrected χ² | Explicit Holm Step-Down Adjustment across m=6 tests*

| Rank ($i$) | Comparison Pair | S8 Win | Other Win | Continuity χ² | Raw $p$ | Multiplier ($m-i+1$) | Corrected Holm $p$ | Significant (α=0.05)? |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **S8 vs S3_Hybrid** | 57 | 26 | **10.8434** | 0.00099 | × 6 | **0.0059** | **Yes** |
| 2 | **S8 vs Abl_No_Reranker** | 49 | 29 | 4.6282 | 0.0315 | × 5 | **0.1575** | **No** |
| 3 | **S8 vs S2_Dense** | 50 | 35 | 2.3059 | 0.1289 | × 4 | **0.5156** | **No** |
| 4 | **S8 vs S7_Iterative_Dense** | 49 | 38 | 1.1494 | 0.2837 | × 3 | **0.8511** | **No** |
| 5 | **S8 vs S5_Hybrid_Rerank** | 10 | 5 | 1.0667 | 0.3017 | × 2 (cummax) | **0.8511** | **No** |
| 6 | **S8 vs S5_Ctrl_Pool50** | 14 | 9 | 0.6957 | 0.4042 | × 1 (cummax) | **0.8511** | **No** |

> **Statistical Implication:** Across all 6 binary EM comparisons, S8 achieves statistically significant accuracy gains solely against unreranked Hybrid S3. Differences against Dense (S2), Hybrid+Rerank (S5), and fair Pool-50 (S5_Ctrl) do not reach statistical significance.

---

## 7. Generator Capacity Diagnostic: 3B vs 7B Scaling (Table 6)
*Paired Bootstrap $B=10,000$, Holm-Bonferroni Corrected ($m=4$)*

| Comparison Pair | Context Evidence Fed | Metric | 3B Score | 7B Score | Net Gain (Δ pp) | 95% Bootstrap CI | Holm $p$-value |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S8_7B vs S8_3B** | S8 Retrieved Passages | **EM** | 39.80% | **52.00%** | **+12.20 pp** | $[+8.20, +16.20]$ | **0.0004 (Yes)** |
| **S8_7B vs S8_3B** | S8 Retrieved Passages | **F1** | 51.14% | **64.32%** | **+13.18 pp** | $[+9.64, +16.80]$ | **0.0004 (Yes)** |
| **S9_7B vs S9_3B** | Gold Oracle Passages | **EM** | 53.00% | **60.20%** | **+7.20 pp** | $[+3.60, +10.80]$ | **0.0004 (Yes)** |
| **S9_7B vs S9_3B** | Gold Oracle Passages | **F1** | 66.80% | **75.10%** | **+8.30 pp** | $[+5.13, +11.55]$ | **0.0004 (Yes)** |

> **Diagnostic Finding:** On identical retrieved evidence, the 7B reader reaches 52.00% EM, comparable to the 3B reader's gold-evidence score of 53.00% EM. Reader capacity is a major constraint on downstream accuracy; the share attributable to metric artifacts remains unquantified (see Limitations).

---

## 8. Multi-Retriever Depth Curves across Depths K∈{5,10,25,50} (Table 4a)

| Retriever Architecture | Question Subgroup | AllSF@5 (%) | AllSF@10 (%) | AllSF@25 (%) | AllSF@50 (%) | Depth Saturation Behavior |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **BM25 Sparse Okapi** | Bridge ($N=404$) | 44.06% | 60.64% | 72.28% | 77.72% | Incomplete (Missing lexical bridge) |
| **BM25 Sparse Okapi** | Comparison ($N=96$) | 58.33% | 75.00% | 88.54% | 94.79% | High saturation |
| **Dense BGE-Small** | Bridge ($N=404$) | 63.86% | 74.50% | 82.67% | 88.37% | Superior semantic discovery; beats Hybrid on Bridge at K=5 and K=50 |
| **Dense BGE-Small** | Comparison ($N=96$) | 98.96% | **100.00%** | **100.00%** | **100.00%** | 100% ceiling reached at K=10 |
| **Hybrid RRF Fusion** | Bridge ($N=404$) | 61.14% | 76.73% | 84.65% | 88.12% | Underperforms Dense on Bridge at K=5 (61.14% vs 63.86%) |
| **Hybrid RRF Fusion** | Comparison ($N=96$) | 97.92% | **100.00%** | **100.00%** | **100.00%** | 100% ceiling reached at K=10 |

*Reconciliation Note on Hybrid Depth vs Main Benchmark:* Table 4a depth curves were computed in separate subgroup evaluation batches (Bridge N=404, Comparison N=96), where RRF score ties were resolved with local index ordering. This produced a minor 5-question (1.0 pp) variance against Table 1's global combined-pool run (68.20% vs 67.20% AllSF@5, and 81.20% vs 81.00% at K=10).

---

## 9. Evidence Discovery & Hop-2 Paired Accounting (Table 4b)

### 9.1 Funnel Breakdown across Pipeline Stages (N=500)
- **Hop 1 Initial Pool Capture:** 438 / 500 (87.60%) — Both gold facts discoverable in initial 25-candidate hybrid pool.
- **Hop 2 Rescued Evidence:** 32 / 500 (6.40%) — Fact 2 missing in Hop 1 pool; surfaced by iterative augmented query.
- **Top-5 Reranking Truncation Loss:** 42 / 500 (8.40%) — Questions present in candidate pool (470 total) but lost upon top-5 cross-encoder truncation (428).
- **Never Retrieved Floor:** 30 / 500 (6.00%) — Neither hop located all facts within the 19,260-passage corpus.

### 9.2 Paired 2×2 Contingency: S8 Staged vs. S5_Ctrl Pool-50 on AllSF@5
| Condition | S5_Ctrl Pool-50 Hit (1) | S5_Ctrl Pool-50 Miss (0) | Total S8 Status |
| :--- | :---: | :---: | :---: |
| **S8 Pipeline Hit (1)** | 402 (Both hit) | **26 (S8 only)** | 428 (85.60%) |
| **S8 Pipeline Miss (0)** | **12 (Ctrl only)** | 60 (Neither hit) | 72 (14.40%) |
| **Total S5_Ctrl Status** | 414 (82.80%) | 86 (17.20%) | 500 (100.0%) |

$$\text{Net Hop-2 Gain} = (\text{S8 only}) - (\text{Ctrl only}) = 26 - 12 = \mathbf{+14 \text{ questions (+2.80 pp)}} \quad (p_{\text{holm}} = 0.048)$$

---

## 10. Qualitative Error Breakdown (Table 4c, N=60 Hand-Verified Failures)
*Single-annotator verification on randomized stratified error sample with Wilson score 95% CIs. Note: Single-annotator categorization has no inter-annotator agreement estimate.*

| Mutually Exclusive Failure Tag | Frequency | Share (%) | Wilson 95% CI | Decision Rule & Failure Mechanism |
| :--- | :---: | :---: | :---: | :--- |
| **Granularity / Format Artifact** | 22 / 60 | **36.70%** | $[25.5\%, 49.3\%]$ | Both gold facts present; generated answer is semantically accurate but fails exact string match (e.g., abbreviation, missing title prefix). |
| **Reasoning Failure under Evidence** | 19 / 60 | **31.70%** | $[21.2\%, 44.2\%]$ | Partial or full gold evidence retrieved in prompt; reader fails logical synthesis across entity constraints. |
| **Retrieval Gap (Missing Fact 2)** | 13 / 60 | **21.70%** | $[13.1\%, 33.6\%]$ | Hop 1 retrieved Fact 1, but Hop 2 query failed to bridge to Fact 2 (evidence missing from prompt). |
| **Span Extraction Error** | 6 / 60 | **10.00%** | $[4.7\%, 20.1\%]$ | Both facts retrieved; generator extracted adjacent distractor entity from the correct paragraph. |

---

## 11. Computational Latency Benchmark on Dual T4 (Table 5)

| Retrieval Stage Module | Underlying Technology | Mean Latency (s/query) | Throughput (qps) | Retrieval Stack Share (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Dense Embedding Retrieval** | BAAI/bge-small-en-v1.5 + Dot Product | **0.0139 s** | **71.9 qps** | **2.1%** |
| **BM25 Sparse Retrieval** | RankBM25 Okapi (Inverted Index) | 0.0724 s | 13.8 qps | 11.0% |
| **Hybrid RRF Fusion** | Reciprocal Rank Fusion ($k=60$) | 0.1169 s | 8.5 qps | 17.8% |
| **Cross-Encoder Reranker** | BAAI/bge-reranker-base ($L=256$) | **0.4560 s** | **2.2 qps** | **69.1% (Dominant Cost)** |

---

## 🛠️ Reproduction & Artifacts
- **`index.html`**: Standalone publication-ready HTML dashboard containing all diagnostic tables with color-coding and footnotes.
- **`RAG_Research_Evaluation_Final.ipynb`**: Complete execution notebook containing all pipelines, indexing, evaluation loops, bootstrap testing, and McNemar test implementations.
- **Decoding Hyperparameters:** Greedy decoding (`do_sample=False`), temperature = 0.0, max_new_tokens = 32, repetition_penalty = 1.0. Seed = 42 for all bootstrap resamples.
- **Hardware:** Dual NVIDIA Tesla T4 GPUs (16 GB VRAM each), Kaggle environment.

---

## 📜 Experimental Scope & Methodological Limitations
- **Corpus Construction:** The evaluation index consists of 19,260 passages constructed by pooling all gold supporting passages and distractors from the HotpotQA development set (distractor split). Numbers are not directly comparable to open-domain full-Wikipedia indexes.
- **Subsample Size:** N=500 questions evaluated across primary baselines (6,500 inference passes under 3B, plus 1,000 passes under 7B scaling diagnostic). Single subset evaluated; multi-split variance remains unquantified.
- **Generator Families:** Evaluated on Qwen-2.5 instruction-tuned series (3B and 7B). Potential pretraining exposure to HotpotQA text cannot be fully ruled out.
- **Metric Artifacts:** Exact Match understates system efficacy due to strict surface-form constraints (36.7% of errors); alias-aware EM was not evaluated.
- **Latency Scope:** Table 5 benchmarks the retrieval stack exclusively; downstream reader generation adds ~0.45 s/query (3B) and ~0.91 s/query (7B).
