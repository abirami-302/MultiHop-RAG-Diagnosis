# Diagnosing the Multi-Hop Retrieval-Generation Gap

[![GitHub Pages](https://img.shields.io/badge/Live-Interactive_Tables-blue.svg)](https://abirami-302.github.io/MultiHop-RAG-Diagnosis/)
[![Benchmark](https://img.shields.io/badge/HotpotQA-N%3D500-green.svg)](#)
[![Dual GPU](https://img.shields.io/badge/Hardware-Kaggle_Dual_T4-orange.svg)](#)

> **Paper Headline:**  
> *"On HotpotQA (N=500, 19,260-passage corpus), a cross-encoder reranker yields the single largest retrieval gain (+15.4 pp AllSF@5), while iterative Hop-2 adds a modest +2.8 pp that does not translate to significant EM gains. Even with gold passages, a 3B reader reaches only 53.0% EM; scaling the reader to 7B improves EM by +12.2 pp on identical retrieved evidence, establishing that the primary performance bottleneck is reader capacity rather than multi-hop retrieval."*

---

## 🌐 Live Interactive Results Table
👉 **View the full publication-styled interactive tables live on GitHub Pages: [abirami-302.github.io/MultiHop-RAG-Diagnosis](https://abirami-302.github.io/MultiHop-RAG-Diagnosis/)**

---

## 📊 Summary of Verified Results

### 1. Stage-Wise Error Budget Decomposition (Table 0)

| Metric & Decomposition Component | Qwen-2.5-3B Architecture | Qwen-2.5-7B Architecture | Diagnostic Interpretation |
| :--- | :---: | :---: | :--- |
| **EM: Retrieval Loss** (Oracle Ceiling − S8 Pipeline) | **13.20 pp** | **8.20 pp** | Lost due to imperfect retrieval evidence |
| **EM: Reader/Metric Loss** (100.0% − Oracle Ceiling) | **47.00 pp** | **39.80 pp** | Lost despite perfect gold evidence present |
| **Retrieval Share of Total EM Deficit** | **21.9%** | **17.1%** | **>78% of downstream error is reader-side** |
| **F1: Retrieval Loss** (Oracle Ceiling − S8 Pipeline) | **15.66 pp** | **10.78 pp** | Token overlap lost due to retrieval noise |
| **F1: Reader/Metric Loss** (100.0% − Oracle Ceiling) | **33.20 pp** | **24.90 pp** | Token overlap lost under gold evidence |
| **Retrieval Share of Total F1 Deficit** | **32.0%** | **30.2%** | **~70% of F1 deficit is reader-bound** |

---

### 2. Comprehensive System Benchmark (Table 1)
*Evaluated on N=500 questions across 19,260 passages (Context budget $K=5$, Qwen-2.5-3B-Instruct)*

| System Configuration | AllSF@5 (%) | SF Recall@5 (%) | MRR | EM (%) | F1 (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **S0: Closed-Book Floor** | 0.00% | 0.00% | 0.00 | 13.60% | 17.86% |
| **S1: BM25 Okapi** | 46.80% | 70.20% | 0.84 | 30.80% | 40.36% |
| **S2: Dense BGE-Small** | 70.60% | 84.40% | 0.93 | 36.80% | 47.11% |
| **S3: Hybrid RRF Fusion** | 67.20% | 82.50% | 0.90 | 33.60% | 43.88% |
| **S5: Hybrid + Reranker (Pool=25)** | 82.60% | 91.00% | 0.97 | 38.80% | 49.15% |
| **S5_Ctrl: Fair Pool-50 Control** | 82.80% | 91.20% | 0.97 | 38.80% | 49.31% |
| **Ctrl_SinglePass_K10** | 81.00% | 90.10% | 0.90 | 38.60% | 48.44% |
| **S7: Iterative Dense Hop-2** | 72.80% | 84.90% | 0.93 | 37.60% | 49.20% |
| **S8: Staged Multi-Hop Pipeline** | **85.60%** | **92.60%** | **0.97** | **39.80%** | **51.14%** |
| **S9: Oracle Ceiling (Gold Evidence)** | **100.00%** | **100.00%** | **1.00** | **53.00%** | **66.80%** |

---

### 3. Generator Capacity Diagnostic: 3B vs 7B Scaling (Table 6)
*Paired Bootstrap $B=10,000$, Holm-Bonferroni Corrected ($m=4$)*

| Comparison Pair | Context Evidence | Metric | 3B Score | 7B Score | Net Gain | 95% Bootstrap CI | Holm $p$-value |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S8_7B vs S8_3B** | S8 Retrieved Passages | **EM** | 39.80% | **52.00%** | **+12.20 pp** | $[+8.20, +16.20]$ | **0.0004 (Yes)** |
| **S8_7B vs S8_3B** | S8 Retrieved Passages | **F1** | 51.14% | **64.32%** | **+13.18 pp** | $[+9.64, +16.80]$ | **0.0004 (Yes)** |
| **S9_7B vs S9_3B** | Gold Oracle Passages | **EM** | 53.00% | **60.20%** | **+7.20 pp** | $[+3.60, +10.80]$ | **0.0004 (Yes)** |
| **S9_7B vs S9_3B** | Gold Oracle Passages | **F1** | 66.80% | **75.10%** | **+8.30 pp** | $[+5.13, +11.55]$ | **0.0004 (Yes)** |

> **Key Diagnostic Finding:** S8 with a 7B reader (52.00% EM) matches the 3B reader under perfect gold oracle passages (53.00% EM), demonstrating that downstream accuracy is heavily gated by generator capacity rather than multi-hop retrieval.

---

## 🛠️ Repository Contents
- **`index.html`**: Complete standalone publication-ready HTML dashboard containing all 8 tables, responsive layout, styled badges, and footnotes.
- **`RAG_Research_Evaluation_Final.ipynb`**: Kaggle execution notebook containing all indexing, retrieval pipelines, generation with caching, bootstrap statistics, and McNemar test implementations.
- **`README.md`**: Executive summary and verified empirical findings.

---

## 📜 Citation & Reproduction
All experiments were conducted locally on Kaggle Dual NVIDIA Tesla T4 GPUs with zero API calls.
Corpus: HotpotQA dev set pooled distractor collection (19,260 passages, 500 evaluation questions).
Models: `BAAI/bge-small-en-v1.5`, `BAAI/bge-reranker-base`, `Qwen/Qwen2.5-3B-Instruct`, and `Qwen/Qwen2.5-7B-Instruct`.
