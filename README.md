# Diagnosing the Multi-Hop Retrieval-Generation Gap

[![GitHub Pages](https://img.shields.io/badge/Live-Interactive_Diagnostic_Dashboard-blue.svg)](https://abirami-302.github.io/MultiHop-RAG-Diagnosis/)
[![Benchmark](https://img.shields.io/badge/HotpotQA-N%3D500-green.svg)](#)
[![Dual GPU](https://img.shields.io/badge/Hardware-Kaggle_Dual_T4-orange.svg)](#)

> **Paper Headline:**  
> *"On HotpotQA (N=500, 19,260-passage corpus), a cross-encoder reranker yields the single largest retrieval gain (+15.4 pp AllSF@5), while iterative Hop-2 adds a modest +2.8 pp that does not translate to significant EM gains. Even with gold passages, a 3B reader reaches only 53.0% EM; scaling the reader to 7B improves EM by +12.2 pp on identical retrieved evidence, establishing that the downstream system is primarily reader-and-metric-bound rather than retrieval-bound."*

---

## 🌐 Live Interactive Diagnostic Website
👉 **View the complete publication tables on GitHub Pages: [abirami-302.github.io/MultiHop-RAG-Diagnosis](https://abirami-302.github.io/MultiHop-RAG-Diagnosis/)**

---

# Empirical Diagnostic Evaluation Suite

---

## 1. Central Diagnostic: Stage-Wise Error Budget Decomposition (Table 0)
*Decomposition of loss against a theoretical 100.0% ceiling across N=500 questions*

| Metric & Decomposition Component | Qwen-2.5-3B Architecture | Qwen-2.5-7B Architecture | Diagnostic Interpretation |
| :--- | :---: | :---: | :--- |
| **EM: Retrieval Loss** (Oracle Ceiling − S8 Pipeline) | **13.20 pp** | **8.20 pp** | Deficit attributable to missing evidence in retrieved context |
| **EM: Reader & Metric Loss** (100.0% − Oracle Ceiling) | **47.00 pp** | **39.80 pp** | Deficit under gold evidence (reasoning failure + surface-form artifacts) |
| **Retrieval Share of Total EM Deficit** | **21.9%** | **17.1%** | **>78% of downstream failure is reader-and-metric-bound** |
| **F1: Retrieval Loss** (Oracle Ceiling − S8 Pipeline) | **15.66 pp** | **10.78 pp** | Token-level overlap lost due to distractor noise |
| **F1: Reader & Metric Loss** (100.0% − Oracle Ceiling) | **33.20 pp** | **24.90 pp** | Token-level overlap lost under perfect gold passages |
| **Retrieval Share of Total F1 Deficit** | **32.0%** | **30.2%** | **~70% of F1 deficit is reader-bound or metric artifact** |

> **Key Finding on Reader-Retriever Interaction:** The retrieval-induced loss contracts from 13.20 pp on 3B to 8.20 pp on 7B. A stronger reader model is more robust to distractor noise, indicating that retrieval quality becomes less of a limiting factor as reader parameterization increases.

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

*\*Note: Ctrl_SinglePass_K10 evaluates unreranked Hybrid retrieval at context depth K=10, explaining its MRR of 0.90 vs reranked S5/S8 (0.97).*

---

## 3. Component Ablation Analysis on S8 (Table 2)
*Reference S8 = 85.60% AllSF@5 | 51.14% F1 | 39.80% EM*

| Ablation Variant | Component Removed | AllSF@5 (%) | Δ AllSF (pp) | F1 Score (%) | Δ F1 (pp) | EM (%) | Diagnostic Finding |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **S8 Staged Pipeline** | None (Full Pipeline) | **85.60%** | — | **51.14%** | — | **39.80%** | Full staged architecture reference |
| **Abl_No_Reranker** | Minus Cross-Encoder Reranker | 63.00% | **-22.60 pp** | 45.82% | **-5.32 pp** | 35.80% | **Reranker is the linchpin ($p < 0.001$)** |
| **S5_Ctrl_Pool50** | Minus Hop 2 (Single-Pass) | 82.80% | **-2.80 pp** | 49.31% | **-1.83 pp** | 38.80% | Hop-2 adds modest +2.8 pp AllSF ($p = 0.004$) |
| **Abl_BM25_Only** | Minus Dense (BM25 only) | 80.40% | **-5.20 pp** | 51.39% | **+0.25 pp** | 40.40% | Improves all-facts recall; no downstream gain |
| **Abl_Dense_Only** | Minus BM25 (Dense only) | 85.60% | **0.00 pp** | 51.38% | **+0.24 pp** | 40.00% | **Dense matches S8 ($p = 1.0$)**; BM25 redundant |

---

## 4. Paired Bootstrap Statistical Significance (Table 3a)
*B=10,000 resamples | 95% Confidence Intervals | Explicit Family-Wise Error Rate Control via Holm-Bonferroni*

| Comparison Pair | Target Metric | S8 Score | Baseline Score | Mean Diff (%) | 95% Bootstrap CI | Raw $p$ | Holm $p$ | Significant (α=0.05)? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Family 1: Primary Retrieval Coverage (AllSF@5, m=8 tests; Raw p < 0.0001 represents bootstrap floor 1/(B+1))** | | | | | | | | |
| **S8 vs S2_Dense** | AllSF@5 | 85.60% | 70.60% | **+15.00%** | $[+11.20, +19.00]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs S3_Hybrid** | AllSF@5 | 85.60% | 67.20% | **+18.40%** | $[+14.60, +22.20]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs S5_Hybrid_Rerank** | AllSF@5 | 85.60% | 82.60% | **+3.00%** | $[+1.40, +4.80]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs S5_Ctrl_Pool50** | AllSF@5 | 85.60% | 82.80% | **+2.80%** | $[+1.00, +4.60]$ | 0.0020 | **0.0040** | **Yes** |
| **S8 vs S7_Iterative_Dense** | AllSF@5 | 85.60% | 72.80% | **+12.80%** | $[+8.60, +17.00]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs Abl_No_Reranker** | AllSF@5 | 85.60% | 63.00% | **+22.60%** | $[+18.60, +26.80]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs Abl_BM25_Only** | AllSF@5 | 85.60% | 80.40% | **+5.20%** | $[+3.00, +7.40]$ | < 0.0001 | **0.0008** | **Yes** |
| **S8 vs Abl_Dense_Only** | AllSF@5 | 85.60% | 85.60% | **0.00%** | $[-2.00, +2.00]$ | 1.0000 | **1.0000** | **No** |
| **Family 2: Downstream Generation Overlap (F1, m=5 tests)** | | | | | | | | |
| **S8 vs S3_Hybrid** | F1 | 51.14% | 43.88% | **+7.26%** | $[+3.82, +10.73]$ | < 0.0001 | **0.0005** | **Yes** |
| **S8 vs Abl_No_Reranker** | F1 | 51.14% | 45.82% | **+5.32%** | $[+1.78, +8.92]$ | 0.0024 | **0.0096** | **Yes** |
| **S8 vs S5_Hybrid_Rerank** | F1 | 51.14% | 49.15% | **+1.98%** | $[+0.50, +3.59]$ | 0.0070 | **0.0210** | **Yes** |
| **S8 vs S2_Dense** | F1 | 51.14% | 47.11% | **+4.03%** | $[+0.45, +7.58]$ | 0.0280 | **0.0560** | **No** |
| **S8 vs S5_Ctrl_Pool50** | F1 | 51.14% | 49.31% | **+1.83%** | $[-0.08, +3.82]$ | 0.0594 | **0.0594** | **No** |

---

## 5. McNemar's Paired Non-Parametric Test on Exact Match (Table 3b)
*Continuity-corrected χ² | Holm-Bonferroni Step-Down Adjusted ($m=6$)*

| Comparison Pair | S8 Win (S8=1, Other=0) | Other Win (S8=0, Other=1) | Continuity χ² | Raw $p$ | Corrected Holm $p$ | Significant (α=0.05)? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S8 vs S3_Hybrid** | 57 | 26 | **10.8434** | 0.00099 | **0.0059** | **Yes** |
| **S8 vs Abl_No_Reranker** | 49 | 29 | 4.6282 | 0.0315 | **0.1575** | **No** |
| **S8 vs S2_Dense** | 50 | 35 | 2.3059 | 0.1289 | **0.5156** | **No** |
| **S8 vs S7_Iterative_Dense** | 49 | 38 | 1.1494 | 0.2837 | **0.8511** | **No** |
| **S8 vs S5_Hybrid_Rerank** | 10 | 5 | 1.0667 | 0.3017 | **0.8511** | **No** |
| **S8 vs S5_Ctrl_Pool50** | 14 | 9 | 0.6957 | 0.4042 | **0.8511** | **No** |

> **Statistical Implication:** Under rigorous Holm step-down control, the staged pipeline S8 produces statistically significant exact-match improvements only against unreranked Hybrid S3. Differences against Dense (S2), Hybrid+Rerank (S5), and fair Pool-50 (S5_Ctrl) do not reach statistical significance.

---

## 6. Generator Capacity Diagnostic: 3B vs 7B Scaling (Table 6)
*Paired Bootstrap $B=10,000$, Holm-Bonferroni Corrected ($m=4$)*

| Comparison Pair | Context Evidence Fed | Metric | 3B Score | 7B Score | Net Gain (Δ pp) | 95% Bootstrap CI | Holm $p$-value |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S8_7B vs S8_3B** | S8 Retrieved Passages | **EM** | 39.80% | **52.00%** | **+12.20 pp** | $[+8.20, +16.20]$ | **0.0004 (Yes)** |
| **S8_7B vs S8_3B** | S8 Retrieved Passages | **F1** | 51.14% | **64.32%** | **+13.18 pp** | $[+9.64, +16.80]$ | **0.0004 (Yes)** |
| **S9_7B vs S9_3B** | Gold Oracle Passages | **EM** | 53.00% | **60.20%** | **+7.20 pp** | $[+3.60, +10.80]$ | **0.0004 (Yes)** |
| **S9_7B vs S9_3B** | Gold Oracle Passages | **F1** | 66.80% | **75.10%** | **+8.30 pp** | $[+5.13, +11.55]$ | **0.0004 (Yes)** |

> **Diagnostic Finding:** On identical retrieved evidence, scaling the generator from 3B to 7B yields +12.20 pp EM (comparable to the 3B Oracle ceiling of 53.00%), confirming that reader extraction capacity represents the primary constraint on downstream answering.

---

## 7. Evidence Discovery & Hop-2 Accounting (Table 4b)

| Stage | Questions Count | Share (%) | Accounting & Mechanism |
| :--- | :---: | :---: | :--- |
| **Hop 1 Pool Capture** | 438 / 500 | **87.60%** | Both gold facts discoverable in initial 25-candidate hybrid pool |
| **Hop 2 Rescued Evidence** | 32 / 500 | **6.40%** | Fact 2 missing in Hop 1 pool; rescued by iterative evidence query |
| **Hop 2 Query Degradation** | 18 / 500 | **3.60%** | Questions where Hop 2 query introduced distractor noise, displacing gold evidence |
| **Net Hop-2 Gain over Pool-50** | **14 / 500** | **+2.80%** | Net retrieval gain (32 rescued − 18 degraded = 14 net gain) |
| **Reranking Truncation Loss** | 42 / 500 | **8.40%** | Questions present in pool (470) but lost upon top-5 cross-encoder truncation (428) |
| **Never Retrieved Floor** | 30 / 500 | **6.00%** | Neither hop surfaced all facts from the 19,260-passage corpus |

---

## 8. Qualitative Error Breakdown (Table 4c, N=60 Hand-Verified Failures)
*Single-annotator verification on randomized stratified error sample with Wilson score 95% CIs*

| Mutually Exclusive Failure Tag | Frequency | Share (%) | Wilson 95% CI | Failure Mechanism |
| :--- | :---: | :---: | :---: | :--- |
| **Granularity / Format Artifact** | 22 / 60 | **36.70%** | $[25.5\%, 49.3\%]$ | Semantically correct answer penalized by exact match string formatting |
| **Reasoning Failure under Evidence** | 19 / 60 | **31.70%** | $[21.2\%, 44.2\%]$ | Partial/full gold evidence in prompt; reader failed multi-hop synthesis |
| **Retrieval Gap (Missing Fact 2)** | 13 / 60 | **21.70%** | $[13.1\%, 33.6\%]$ | Hop 1 retrieved Fact 1, but Hop 2 failed to bridge to Fact 2 |
| **Span Extraction Error** | 6 / 60 | **10.00%** | $[4.7\%, 20.1\%]$ | Both facts retrieved; generator extracted adjacent distractor entity |

---

## 9. Computational Latency Benchmark on Dual T4 (Table 5)

| Retrieval Stage Module | Underlying Technology | Mean Latency (s/query) | Throughput (qps) | Retrieval Stack Share (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Dense Embedding Retrieval** | BAAI/bge-small-en-v1.5 + Dot Product | **0.0139 s** | **71.9 qps** | **2.1%** |
| **BM25 Sparse Retrieval** | RankBM25 Okapi (Inverted Index) | 0.0724 s | 13.8 qps | 11.0% |
| **Hybrid RRF Fusion** | Reciprocal Rank Fusion ($k=60$) | 0.1169 s | 8.5 qps | 17.8% |
| **Cross-Encoder Reranker** | BAAI/bge-reranker-base ($L=256$) | **0.4560 s** | **2.2 qps** | **69.1% (Dominant Cost)** |

---

## 🛠️ Repository Contents
- **`index.html`**: Standalone publication-ready HTML dashboard containing all diagnostic tables with color-coding and footnotes.
- **`RAG_Research_Evaluation_Final.ipynb`**: Complete execution notebook containing all pipelines, indexing, evaluation loops, bootstrap testing, and McNemar test implementations.
- **`README.md`**: Master diagnostic documentation and empirical findings.

---

## 📜 Limitations & Experimental Scope
- **Corpus Scope:** Evaluated over a 19,260-passage distractor corpus constructed from the HotpotQA development set (not the full-Wikipedia multi-million index).
- **Subsample Size:** N=500 questions evaluated across 13 systems (6,500 inference passes).
- **Generator Families:** Evaluated on Qwen-2.5 instruction-tuned series (3B and 7B). Potential pretraining exposure to HotpotQA text cannot be fully ruled out.
