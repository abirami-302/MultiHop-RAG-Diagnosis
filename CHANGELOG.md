# Changelog

All notable changes, revisions, corrections, and audit milestones for the Multi-Hop RAG Diagnostic study are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.0.0] - 2026-09-30

### Expanded
- **Related Work (Section 2):** Expanded empirical context across DPR, BM25/BEIR, cross-encoder reranking, IRCoT, and Beam Retrieval. Documented explicit benchmark contrasts (full-Wikipedia open-domain scale vs. our controlled 19,260-passage pooled evaluation corpus, reader parameter sizes 3B/7B vs. 11B/Flan-T5).
- **Methodology (Section 3.3.1):** Added formal definition of Reciprocal Rank Fusion (RRF) with constant $k = 60$, exact verbatim prompt template for reader inference, and an explicit worked arithmetic example of the retrieval deficit decomposition:
  $$\text{Retrieval Share} = \frac{53.00\% - 39.80\%}{100.00\% - 39.80\%} = \frac{13.20\%}{60.20\%} \approx 21.93\% \rightarrow 21.9\%$$
- **Discussion (Section 5):** Added analytical discussion on:
  - Rapid saturation of comparison-type questions (43.8% EM on S1 to 46.9% on S8) and implications for benchmark design.
  - Potential score inflation from corpus pooling (19,260 passages vs. 5M+ full-Wikipedia articles).
  - Production latency-vs-accuracy trade-offs under fixed compute budgets.
- **Threats to Validity (Section 6.1):** Added structured subsection detailing:
  - Benchmark ceiling and annotation ambiguity artifacts (Gold EM ceiling of 53.0% / F1 of 66.8%).
  - Corpus size constraints (pooled distractor set).
  - Reader scale sensitivity (4-bit NF4 quantization on 7B reader).
  - Metric brittleness in exact match tokenization.

### Verified & Reconciled
- **EM Contingency Alignment:** Re-verified exact $2 \times 2$ contingency matrix between $S8$ and $S5\_\text{Ctrl}\_\text{Pool50}$ on the `em` column of `OUT/tracker.csv`:
  - Both Hit EM: 185 ($37.0\%$)
  - S8-Only Win EM: 14 ($2.8\%$)
  - Control-Only Win EM: 9 ($1.8\%$)
  - Neither Hit EM: 292 ($58.4\%$)
  - Total: 500 questions, net difference $+5$ questions ($+1.00\text{ pp}$).
  - Fully disentangled from retrieval AllSF contingency (26 S8-only wins vs. 12 Control-only wins, net $+14$ questions, $+2.80\text{ pp}$).
- **Retrieval Stack Latency Share:** Clarified that the $69.1\%$ reranker latency figure represents the reranker stage ($0.4560\text{ s}$) divided by cumulative stage latency across all four retrieval modules ($0.0139 + 0.0724 + 0.1169 + 0.4560 = 0.6592\text{ s} \rightarrow 69.17\%$).

---

## [1.2.0] - 2026-09-29

### Fixed
- Corrected discussion narrative that previously conflated AllSF retrieval contingency counts ($26/12$, $+14$) with Exact Match answer generation counts ($14/9$, $+5$).
- Recomputed exact cumulative latency breakdown across dual T4 GPU benchmark runs.

### Added
- Created `REPRODUCIBILITY.md` detailing end-to-end table lineage, script mapping, seed configurations, and verification steps.

---

## [1.1.0] - 2026-09-28

### Removed
- **Retraction of Exploratory System S10:** System S10 (LLM Query Formulation variant) was identified during internal review as not originating from an active row in `OUT/tracker.csv`. All references and statistical rows for S10 were formally retracted and excised from paper tables, scripts, and bootstrap families.

### Changed
- **Statistical Claim Softening:** Reframed significance claims to reflect power limits of an $N=500$ sample. Highlighted that downstream EM improvements (+1.0 pp over $S5\_\text{Ctrl}$) do not achieve statistical significance under Holm-Bonferroni correction ($p = 0.851$).
- **Layout Formatting:** Adjusted wide comparison tables (Tables 5 & 6) to span single-column layout sections to preserve typography and readability in the 2-column manuscript.
- **Author Affiliations:** Added co-author Madhumitha P S and institutional affiliations.

---

## [1.0.0] - 2026-09-25

### Initial Release
- Initial draft of research manuscript compiling HotpotQA diagnostic benchmark results across systems S0 through S9 on dual NVIDIA T4 GPUs.
- Established primary empirical finding: retrieval failure accounts for only $21.9\%$ of downstream EM deficit on Qwen-2.5-3B ($17.1\%$ on Qwen-2.5-7B), establishing the diagnostic primacy of reader capacity and metric artifacts.
