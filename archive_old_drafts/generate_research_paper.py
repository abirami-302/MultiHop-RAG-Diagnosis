# -*- coding: utf-8 -*-
"""
generate_research_paper.py
Generates the complete, publication-grade Word (.docx) manuscript for:
"Diagnosing the Multi-Hop Retrieval-Generation Gap: An Empirical Study on HotpotQA"
Strictly adhering to empirical findings, academic register, and rigorous human styling.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="003366"/>\n'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="003366"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_row(row, bg_hex=None, bold=False, font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT, color_hex="000000"):
    for cell in row.cells:
        if bg_hex:
            set_cell_shading(cell, bg_hex)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = align
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            for r in p.runs:
                r.bold = bold
                r.font.name = "Times New Roman"
                r.font.size = Pt(font_size)
                if color_hex != "000000":
                    r.font.color.rgb = RGBColor(int(color_hex[:2], 16), int(color_hex[2:4], 16), int(color_hex[4:], 16))

def build_paper():
    doc = docx.Document()

    # Page Margins: Standard 1-inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Styles setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    def add_p(text="", bold_prefix="", italic_note="", space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Times New Roman'
            r_b.font.size = Pt(11)
        if text:
            r_t = p.add_run(text)
            r_t.font.name = 'Times New Roman'
            r_t.font.size = Pt(11)
        if italic_note:
            r_i = p.add_run(italic_note)
            r_i.italic = True
            r_i.font.name = 'Times New Roman'
            r_i.font.size = Pt(10.5)
        return p

    def add_sec_heading(title, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        r.font.name = 'Times New Roman'
        if level == 1:
            r.font.size = Pt(14)
            r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        elif level == 2:
            r.font.size = Pt(12)
            r.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        else:
            r.font.size = Pt(11)
            r.italic = True
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return p

    def add_table_note(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(text)
        r.italic = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        return p

    # =========================================================================
    # TITLE & AUTHOR BLOCK
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Diagnosing the Multi-Hop Retrieval-Generation Gap:\nAn Empirical Study on HotpotQA")
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(0x00, 0x22, 0x44)

    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_before = Pt(4)
    p_author.paragraph_format.space_after = Pt(2)
    r_aut = p_author.add_run("Abirami K\nDepartment of Computer Science and Engineering\nabiramikondaiyan@gmail.com")
    r_aut.font.name = 'Times New Roman'
    r_aut.font.size = Pt(10.5)
    r_aut.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    p_repo = doc.add_paragraph()
    p_repo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_repo.paragraph_format.space_before = Pt(2)
    p_repo.paragraph_format.space_after = Pt(14)
    r_repo = p_repo.add_run("Repository & Live Reproduction Suite: https://github.com/abirami-302/MultiHop-RAG-Diagnosis")
    r_repo.font.name = 'Times New Roman'
    r_repo.font.size = Pt(9.5)
    r_repo.italic = True
    r_repo.font.color.rgb = RGBColor(0x00, 0x44, 0x88)

    # =========================================================================
    # 1. ABSTRACT
    # =========================================================================
    add_sec_heading("Abstract", level=1)
    abstract_text = (
        "Multi-hop question answering requires synthesizing disconnected evidence fragments across multiple text passages. "
        "While complex iterative retrieval pipelines are frequently proposed to resolve this challenge, their true stage-wise error "
        "mechanisms remain insufficiently understood. In this study, we conduct a systematic, stage-wise empirical diagnosis comparing "
        "thirteen retrieval and generation configurations on a 500-question evaluation benchmark drawn from HotpotQA over a pooled "
        "corpus of 19,260 passages under a unified dual-GPU execution protocol. We employ paired bootstrap resampling (B=10,000) and "
        "McNemar's paired tests with family-wise Holm-Bonferroni correction, complemented by a leave-one-out ablation, recall-depth "
        "profiling, stage-wise evidence funnel accounting, reader parameter scaling (3B vs. 7B parameters), and a hand-verified qualitative "
        "audit of failure cases. Our empirical findings demonstrate that neural cross-encoder reranking provides the single most decisive "
        "retrieval improvement (+15.40 percentage points AllSF@5), whereas iterative second-hop retrieval contributes a modest, borderline "
        "significant gain (+2.80 percentage points AllSF@5, p_holm = 0.0480) that fails to convert into significant downstream exact-match gains. "
        "Decomposing the end-to-end performance deficit reveals that imperfect retrieval accounts for merely 21.9% of the overall Exact Match deficit "
        "under a 3B reader, contracting further to 17.1% under a 7B reader. When provided with identical retrieved evidence, scaling the reader from "
        "3B to 7B parameters delivers a +12.20 percentage point jump in Exact Match (reaching 52.00%, comparable to the 3B model's gold-evidence ceiling "
        "of 53.00%). Qualitative inspection reveals that 36.70% of downstream errors stem from surface-form metric penalties rather than factual errors. "
        "These results demonstrate that multi-hop QA systems operating over moderately sized corpora are fundamentally reader-and-metric-bound "
        "rather than retrieval-bound, indicating that optimizing complex query-loop architectures offers rapidly diminishing returns relative to "
        "scaling reader reasoning capacity."
    )
    add_p(abstract_text, space_after=12, line_spacing=1.15)

    # =========================================================================
    # 2. INTRODUCTION
    # =========================================================================
    add_sec_heading("1. Introduction", level=1)
    add_p(
        "Retrieval-Augmented Generation (RAG) has emerged as the prevailing framework for grounding large language models on external knowledge, "
        "reducing factual hallucinations and mitigating parametric knowledge cutoff limitations. Yet when queries require multi-step reasoning—such "
        "as bridging separate Wikipedia articles to answer multi-hop questions—standard single-pass dense or lexical retrievers often stumble. "
        "A typical response in recent literature has been the introduction of iterative query-reformulation loops, multi-agent debate pipelines, "
        "and multi-hop graph traversals. These architectures operate on the foundational premise that missing retrieval evidence is the primary "
        "choke point throttling downstream answer accuracy."
    )
    add_p(
        "However, evaluating multi-hop architectures often conflates retrieval recall gains with answer generation improvements. Many reported "
        "improvements fail to isolate whether downstream accuracy gains originate from genuinely superior multi-hop evidence capture, broader "
        "context windows, or the downstream generator's capacity to digest noisy candidate sets. Without rigorous, stage-wise error decomposition "
        "and paired statistical testing, practitioners risk engineering intricate retrieval workflows to resolve what might actually be a reader reasoning "
        "or metric-formatting deficiency."
    )
    add_p(
        "To test this premise, we designed an empirical diagnostic investigation rather than introducing another complex architecture. "
        "We evaluate multi-hop RAG stage by stage on HotpotQA, using 500 fixed evaluation questions against a pooled corpus of 19,260 passages on dual "
        "NVIDIA Tesla T4 GPUs. We isolate each component: sparse lexical retrieval (BM25), dense semantic search (BGE-Small), reciprocal rank fusion (RRF), "
        "neural cross-encoder reranking, and iterative second-hop retrieval. Crucially, we enforce fair capacity controls, including an identical-pool "
        "single-pass control (Pool-50) and an unreranked wider-window baseline (K=10), paired bootstrap resampling with Holm-Bonferroni corrections, and "
        "McNemar's tests on paired binary Exact Match outcomes."
    )

    add_sec_heading("1.1 Contributions", level=2)
    add_p(
        "Rather than proposing a novel architecture, our paper provides a controlled empirical autopsy of the multi-hop RAG pipeline. "
        "Specifically, we report three core diagnostic findings:"
    )
    add_p(
        "First, we quantify the stage-wise error budget of the pipeline (Table 1). We show that under a 3B parameter reader, retrieval loss accounts "
        "for only 21.9% of the total Exact Match deficit (13.20 pp out of 60.20 pp below 100%), while reader and metric artifacts account for 78.1% "
        "(47.00 pp). When evaluating a 7B reader over the exact same evidence, retrieval's share of the deficit contracts to 17.1% (8.20 pp), establishing "
        "that stronger generators exhibit greater resilience against distractor interference."
    )
    add_p(
        "Second, we isolate the retrieval mechanisms driving performance. Cross-encoder reranking serves as the definitive retrieval linchpin, "
        "contributing +15.40 pp in all-supporting-fact retrieval coverage (AllSF@5), whereas iterative Hop-2 query augmentation adds a modest +2.80 pp. "
        "Under paired bootstrap resampling, this Hop-2 gain is borderline significant (p_holm = 0.0480), but under paired McNemar testing, it produces "
        "no statistically detectable gain in downstream Exact Match (p_holm = 0.8511)."
    )
    add_p(
        "Third, through a randomized, hand-verified failure audit of 60 error cases, we demonstrate that 36.70% of generation failures represent surface-form "
        "metric artifacts where the model extracted the correct semantic fact but failed string-matching criteria. An additional 31.70% represent logical "
        "reasoning breakdowns despite having full or partial gold evidence in context. Collectively, these results demonstrate that multi-hop QA over "
        "distractor-rich corpora is primarily reader-and-metric-bound rather than retrieval-bound."
    )

    # =========================================================================
    # 3. RELATED WORK
    # =========================================================================
    add_sec_heading("2. Related Work", level=1)
    add_p(
        "Dense retrieval methods, pioneered by Dense Passage Retrieval (DPR) (Karpukhin et al., 2020), map questions and candidate documents into a "
        "shared latent semantic space via dual-encoder architectures. While effective for single-fact lookups, dense retrieval frequently misses lexical "
        "exact-matches such as entity acronyms and numerical codes, leading to the resurgence of hybrid retrieval paradigms that combine dense vectors with "
        "BM25 Okapi (Robertson and Zaragoza, 2009) via Reciprocal Rank Fusion (RRF) (Cormack et al., 2009). Cross-encoder neural rerankers (Nogueira and Cho, 2019) "
        "further refine candidate pools by performing full token-level cross-attention over query-document pairs, yielding substantial precision gains at "
        "the cost of quadratic computational complexity."
    )
    add_p(
        "For complex questions requiring multi-hop reasoning, single-pass retrieval often fails because the second supporting fact depends on entity links "
        "uncovered only in the first fact (Yang et al., 2018). Iterative retrieval frameworks such as IRCoT (Trivedi et al., 2022) and Beam Retrieval "
        "(Khattab et al., 2021) address this by interleaving chain-of-thought generation with iterative retrieval calls. While these methods demonstrate "
        "impressive end-to-end benchmark gains, they rarely decouple whether improvements originate from the iterative retrieval mechanism itself or from "
        "the expanded prompt capacity and broader search budgets allocated to the pipeline."
    )
    add_p(
        "Furthermore, empirical rigor and statistical testing remain inconsistently applied in recent NLP literature. Studies frequently report point differences "
        "on small test sets without paired non-parametric significance testing, risking the publication of noise as architectural breakthroughs. We adopt "
        "rigorous paired bootstrap resampling (Efron and Tibshirani, 1993) and McNemar's test for binary paired outcomes (McNemar, 1947), enforcing family-wise "
        "error rate control via the Holm-Bonferroni step-down procedure (Holm, 1979) to establish reproducible diagnostic baselines."
    )

    # =========================================================================
    # 4. METHODOLOGY
    # =========================================================================
    add_sec_heading("3. Methodology", level=1)
    add_p(
        "To perform a clean diagnostic autopsy, we evaluate thirteen distinct system configurations and controlled ablations across a single, fixed evaluation "
        "protocol. In this section, we document our corpus construction, the thirteen evaluated pipeline configurations, metric definitions, and our pre-registered "
        "paired statistical hypothesis framework."
    )

    add_sec_heading("3.1 Evaluation Benchmark and Corpus Construction", level=2)
    add_p(
        "We construct our benchmark using the HotpotQA development set (distractor split). Rather than indexing the entirety of English Wikipedia—which "
        "introduces massive compute requirements that often force researchers to rely on remote closed-source APIs—we construct a pooled local corpus of "
        "19,260 passages. This corpus is assembled by pooling all gold supporting passages and distractor paragraphs corresponding to the development set questions. "
        "From this distractor-rich pool, we sample a fixed evaluation set of 500 questions (N=500), comprising 404 bridge questions (80.8%) and 96 comparison "
        "questions (19.2%), preserving the natural difficulty distribution of the original benchmark. Hardware execution is fixed on dual NVIDIA Tesla T4 GPUs "
        "(16 GB VRAM each) hosted in a reproducible Kaggle environment."
    )

    add_sec_heading("3.2 Evaluated System Configurations and Controlled Baselines", level=2)
    add_p(
        "We examine thirteen distinct configurations, specifically formulated to isolate each component of the retrieval and generation stack:"
    )
    add_p(
        "1. S0 (Closed-Book Baseline): Evaluates parametric knowledge alone. The generator is queried with the question and instructed to answer directly without any context passages.\n"
        "2. S1 (BM25 Okapi): Traditional lexical sparse retrieval using tokenized inverted indexing, returning top-5 passages.\n"
        "3. S2 (Dense Retrieval): Semantic vector search using BAAI/bge-small-en-v1.5 (384 dimensions) with cosine dot-product indexing, returning top-5 passages.\n"
        "4. S3 (Hybrid RRF Fusion): Merges top-100 BM25 and top-100 dense candidates using Reciprocal Rank Fusion (k=60), returning top-5 passages without reranking.\n"
        "5. S5 (Hybrid + Cross-Encoder Reranker): Initial hybrid pool of 25 candidates reranked via BAAI/bge-reranker-base, truncated to top-5.\n"
        "6. S5_Ctrl (Fair Pool-50 Single-Pass Control): Initial hybrid pool expanded to 50 candidates, reranked by the cross-encoder to top-5. This provides an exact capacity control for the two-hop pipeline, ensuring identical candidate search budgets (50 total candidates).\n"
        "7. Ctrl_SinglePass_K10 (Context Budget Control): Unreranked hybrid retrieval fed directly to the reader at context budget K=10, evaluating whether expanding the reader's passage budget substitutes for neural reranking.\n"
        "8. S7 (Dense Iterative Hop-2): Two-hop iterative retrieval using dense search alone, querying Hop 2 with question plus top-1 retrieved snippet.\n"
        "9. S8 (Staged Multi-Hop Pipeline): Our full reference staged architecture. Hop 1 retrieves 25 hybrid candidates. A heuristic query ('[Question] [Hop 1 Top Passage Snippet]') retrieves 25 additional hybrid candidates in Hop 2. The combined 50-candidate pool is deduplicated, reranked by the cross-encoder, and truncated to top-5.\n"
        "10. S9 (Oracle Ceiling): Provides the generator with the ground-truth gold supporting passages, establishing the theoretical upper performance bound under perfect retrieval.\n"
        "11. Abl_No_Reranker: Full S8 two-hop pipeline but bypassing the cross-encoder reranker, relying solely on RRF merge scores for top-5 truncation.\n"
        "12. Abl_BM25_Only: Full S8 pipeline omitting dense retrieval (BM25 search alone across both hops, followed by cross-encoder reranking).\n"
        "13. Abl_Dense_Only: Full S8 pipeline omitting BM25 retrieval (Dense search alone across both hops, followed by cross-encoder reranking).\n"
        "14. S10_LLM_Query: An exploratory substitution replacing the heuristic Hop 2 query in S8 with an LLM-generated targeted sub-question."
    )

    add_sec_heading("3.3 Evaluation Metrics and Generation Protocol", level=2)
    add_p(
        "Retrieval quality is measured across three primary dimensions at cut-off K=5: (i) Supporting Fact Recall (SF Recall@5), measuring the percentage "
        "of ground-truth facts retrieved; (ii) All Supporting Facts Recall (AllSF@5), a strict binary metric indicating whether all necessary gold supporting "
        "passages are simultaneously present in the top-K context; and (iii) Mean Reciprocal Rank (MRR) of the first retrieved gold passage."
    )
    add_p(
        "Downstream question answering is evaluated using standard Exact Match (EM) binary accuracy after regex surface normalization (lowercasing, punctuation, "
        "and article removal) and macro-averaged token-level F1 score. Generation is performed under greedy decoding (do_sample=False, temperature=0.0, "
        "max_new_tokens=32) using Qwen2.5-3B-Instruct as our default reader, and Qwen2.5-7B-Instruct for our parameter scaling diagnostic."
    )

    add_sec_heading("3.4 Pre-Registered Statistical Testing Protocol", level=2)
    add_p(
        "To protect against p-hacking and multiple testing artifacts, we pre-registered our primary hypothesis: S8 (staged multi-hop) achieves superior AllSF@5 "
        "retrieval coverage and downstream EM compared to fair single-pass controls (S5_Ctrl) and baseline architectures. We employ two non-parametric tests: "
        "(1) Paired bootstrap resampling with B=10,000 resamples to estimate 95% bias-corrected percentile confidence intervals and empirical p-values for AllSF "
        "and F1 differences; and (2) Continuity-corrected McNemar's test on binary 0/1 Exact Match outcomes. For all test families, we enforce strict family-wise "
        "error rate control at alpha=0.05 using the Holm-Bonferroni step-down adjustment."
    )

    # =========================================================================
    # 5. RESULTS
    # =========================================================================
    add_sec_heading("4. Results and Empirical Diagnostics", level=1)
    add_p(
        "We present our empirical findings across ten subsections, tracking the performance of the pipeline from global error budgets down to manual failure categorizations."
    )

    # --- 4.1 TABLE 0: ERROR BUDGET ---
    add_sec_heading("4.1 Central Diagnostic: Stage-Wise Error Budget Decomposition", level=2)
    add_p(
        "We begin with the central diagnostic question: how much of downstream failure is genuinely caused by retrieval misses versus generator limitations? "
        "Table 1 decomposes the performance gap between zero and 100% into retrieval loss (Oracle Ceiling minus S8 Pipeline) and reader/metric loss "
        "(100% minus Oracle Ceiling)."
    )
    add_caption("Table 1. Stage-wise error budget decomposition of downstream performance deficits (N=500 questions).")
    
    t0_data = [
        ["Metric & Decomposition Component", "Qwen2.5-3B Architecture", "Qwen2.5-7B Architecture", "Diagnostic Interpretation"],
        ["EM: Retrieval Loss (Oracle − S8 Pipeline)", "13.20 pp", "8.20 pp", "Loss attributable to imperfect retrieval evidence"],
        ["EM: Reader & Metric Loss (100% − Oracle)", "47.00 pp", "39.80 pp", "Loss under perfect gold passages (reasoning & metric)"],
        ["Retrieval Share of Total EM Deficit", "21.9%", "17.1%", ">78% of downstream error originates on the reader side"],
        ["F1: Retrieval Loss (Oracle − S8 Pipeline)", "15.66 pp", "10.78 pp", "Token overlap deficit caused by distractor noise"],
        ["F1: Reader & Metric Loss (100% − Oracle)", "33.20 pp", "24.90 pp", "Token overlap deficit under perfect gold passages"],
        ["Retrieval Share of Total F1 Deficit", "32.0%", "30.2%", "Nearly 70% of F1 deficit is reader-bound or metric artifact"]
    ]
    t0 = doc.add_table(rows=len(t0_data), cols=4)
    t0.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t0)
    for r_idx, row in enumerate(t0.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t0_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [3, 6]:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Total deficit equals (100.0% − System Score). Retrieval share is computed as Retrieval Loss / (Retrieval Loss + Reader Loss).")

    add_p(
        "Under the 3B reader, the retrieval-induced Exact Match deficit is 13.20 pp, while the reader and metric deficit is 47.00 pp. "
        "Thus, retrieval errors account for only 21.9% of the total downstream EM deficit. More tellingly, when switching to the 7B reader, "
        "the retrieval-induced deficit contracts from 13.20 pp to 8.20 pp (a 37.9% reduction in retrieval penalty), even though both readers "
        "received the exact same retrieved passages. This reveals a critical reader-retriever interaction: stronger generators possess superior "
        "noise-filtering capabilities, demonstrating that retrieval quality becomes progressively less of a limiting bottleneck as generator "
        "reasoning capacity increases."
    )

    # --- 4.2 TABLE 1: OVERALL BENCHMARK ---
    add_sec_heading("4.2 End-to-End Pipeline Performance", level=2)
    add_p(
        "Table 2 reports overall retrieval and downstream generation performance across the primary pipeline architectures and controlled baselines."
    )
    add_caption("Table 2. Multi-stage retrieval and downstream generation evaluation on HotpotQA (N=500 questions, Context K=5, Qwen2.5-3B-Instruct).")

    t1_data = [
        ["System Configuration", "K", "AllSF@K (%)", "SF Recall@K (%)", "MRR", "Exact Match (%)", "F1 Score (%)"],
        ["S0: Closed-Book Floor", "0", "0.00%", "0.00%", "0.00", "13.60%", "17.86%"],
        ["S1: BM25 Okapi", "5", "46.80%", "70.20%", "0.84", "30.80%", "40.36%"],
        ["S2: Dense BGE-Small", "5", "70.60%", "84.40%", "0.93", "36.80%", "47.11%"],
        ["S3: Hybrid RRF Fusion", "5", "67.20%", "82.50%", "0.90", "33.60%", "43.88%"],
        ["S5: Hybrid + Cross-Encoder (Pool=25)", "5", "82.60%", "91.00%", "0.97", "38.80%", "49.15%"],
        ["S5_Ctrl: Fair Pool-50 Control", "5", "82.80%", "91.20%", "0.97", "38.80%", "49.31%"],
        ["Ctrl_SinglePass_K10", "10", "81.00%*", "90.10%", "0.90", "38.60%", "48.44%"],
        ["S7: Dense Iterative Hop-2", "5", "72.80%", "84.90%", "0.93", "37.60%", "49.20%"],
        ["S8: Staged Multi-Hop Pipeline", "5", "85.60%", "92.60%", "0.97", "39.80%", "51.14%"],
        ["S9: Oracle Ceiling (Gold Evidence)", "Gold", "100.00%", "100.00%", "1.00", "53.00%", "66.80%"]
    ]
    t1 = doc.add_table(rows=len(t1_data), cols=7)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1)
    for r_idx, row in enumerate(t1.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t1_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 9: # S8 highlighted
            format_row(row, bg_hex="EBF3FB", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in range(1, 7): row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=9, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in range(1, 7): row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("*Note on Ctrl_SinglePass_K10: AllSF is evaluated at K=10. S8 achieves 85.60% AllSF@5 and 39.80% EM. Gold ceiling reaches 53.00% EM.")

    add_p(
        "A standard reading of Table 2 might conclude that S8 is the superior pipeline across all metrics. It establishes the highest AllSF@5 (85.60%), "
        "MRR (0.97), and Exact Match (39.80%). However, closer inspection of the control baselines reveals critical nuances. First, the fair single-pass "
        "control (S5_Ctrl), which searches 50 hybrid candidates without an iterative second hop, reaches 82.80% AllSF@5 and 38.80% EM. Iterative Hop-2 adds "
        "only +2.80 pp in retrieval coverage and a marginal +1.00 pp in Exact Match (5 additional correct questions out of 500)."
    )
    add_p(
        "Second, consider Ctrl_SinglePass_K10. By simply providing the generator with ten unreranked hybrid passages (K=10) instead of five reranked passages, "
        "the reader reaches 38.60% EM—virtually identical to the 38.80% achieved by neural reranking at K=5. In other words, allocating a broader context "
        "budget to the reader circumvents the need for neural cross-encoder reranking entirely, at least on this corpus size."
    )

    # --- 4.3 TABLE 1B: MARGINAL GAINS ---
    add_sec_heading("4.3 Marginal Gains of S8 over Baselines", level=2)
    add_p(
        "Table 3 isolates the marginal net gains (Δ pp) of the full staged pipeline over each individual baseline."
    )
    add_caption("Table 3. Marginal point gains (Δ pp) of S8 over baseline systems with paired McNemar significance status.")

    t1b_data = [
        ["Baseline System", "Baseline AllSF", "S8 AllSF", "Retrieval Δ (pp)", "Baseline EM", "S8 EM", "EM Δ (pp)", "McNemar Sig. (m=6)"],
        ["vs. S1 (BM25 Okapi)", "46.80%", "85.60%", "+38.80 pp", "30.80%", "39.80%", "+9.00 pp", "Not tested in paired m=6"],
        ["vs. S2 (Dense BGE-Small)", "70.60%", "85.60%", "+15.00 pp", "36.80%", "39.80%", "+3.00 pp", "No (p = 0.5156)"],
        ["vs. S3 (Hybrid RRF)", "67.20%", "85.60%", "+18.40 pp", "33.60%", "39.80%", "+6.20 pp", "Yes (p = 0.0059)"],
        ["vs. S5 (Hybrid + Rerank)", "82.60%", "85.60%", "+3.00 pp", "38.80%", "39.80%", "+1.00 pp", "No (p = 0.8511)"],
        ["vs. S5_Ctrl (Pool-50 Ctrl)", "82.80%", "85.60%", "+2.80 pp", "38.80%", "39.80%", "+1.00 pp", "No (p = 0.8511)"],
        ["vs. S7 (Iterative Dense)", "72.80%", "85.60%", "+12.80 pp", "37.60%", "39.80%", "+2.20 pp", "No (p = 0.8511)"]
    ]
    t1b = doc.add_table(rows=len(t1b_data), cols=8)
    t1b.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1b)
    for r_idx, row in enumerate(t1b.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t1b_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in range(1, 7): row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: McNemar p-values are continuity-corrected and adjusted under the pre-registered m=6 Holm family.")

    add_p(
        "Notice the profound drop-off between retrieval gains and downstream answer accuracy. S8 improves AllSF@5 by +15.00 pp over dense retrieval S2, "
        "yet downstream Exact Match improves by only +3.00 pp (from 36.80% to 39.80%), which is statistically indistinguishable from chance (p_holm = 0.5156). "
        "Against unreranked hybrid retrieval S3, S8 achieves a statistically significant +6.20 pp gain in EM (p_holm = 0.0059). But against S5, S5_Ctrl, "
        "and S7, S8's downstream improvements fail to reach statistical significance after correcting for multiple comparisons."
    )

    # --- 4.4 TABLE 2: ABLATION ---
    add_sec_heading("4.4 Component Ablation Study on S8", level=2)
    add_p(
        "To determine which architectural components actually justify their computational overhead, we performed a leave-one-out ablation on S8 (Table 4)."
    )
    add_caption("Table 4. Leave-one-out component ablation analysis on the staged multi-hop pipeline (S8 reference).")

    t2_data = [
        ["Ablation Variant", "Component Removed", "AllSF@5", "Δ AllSF", "F1 Score", "Δ F1", "EM", "Diagnostic Finding"],
        ["S8 Staged Pipeline", "None (Full Pipeline)", "85.60%", "—", "51.14%", "—", "39.80%", "Full reference staged architecture"],
        ["Abl_No_Reranker", "Minus Cross-Encoder Reranker", "63.00%", "-22.60 pp", "45.82%", "-5.32 pp", "35.80%", "Reranker is linchpin; drops below S3 (67.2%)"],
        ["S5_Ctrl_Pool50", "Minus Hop 2 (Single-Pass)", "82.80%", "-2.80 pp", "49.31%", "-1.83 pp", "38.80%", "Hop-2 adds +2.8 pp AllSF (p_holm = 0.048, borderline)"],
        ["Abl_BM25_Only", "Minus Dense (BM25 only)", "80.40%", "-5.20 pp", "51.39%", "+0.25 pp", "40.40%", "Dense aids recall, but zero downstream benefit"],
        ["Abl_Dense_Only", "Minus BM25 (Dense only)", "85.60%", "0.00 pp", "51.38%", "+0.24 pp", "40.00%", "Dense matches S8 (p = 1.0); BM25 fully redundant"]
    ]
    t2 = doc.add_table(rows=len(t2_data), cols=8)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2)
    for r_idx, row in enumerate(t2.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t2_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 1:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4, 5, 6]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Reference S8 performance is 85.60% AllSF@5, 51.14% F1, and 39.80% EM. Negative Δ indicates degradation upon component removal.")

    add_p(
        "Table 4 exposes two major findings. First, removing the cross-encoder reranker (Abl_No_Reranker) causes AllSF@5 to plummet by -22.60 pp (to 63.00%), "
        "and F1 drops by -5.32 pp. In fact, 63.00% is lower than unreranked single-pass hybrid S3 (67.20%). This reveals that iterative snippet-augmented queries "
        "retrieve substantial distractor noise that actively degrades the top-5 context unless filtered by neural cross-attention. The reranker is the true linchpin "
        "of the iterative pipeline."
    )
    add_p(
        "Second, look at Abl_Dense_Only: omitting BM25 entirely results in exactly 85.60% AllSF@5 (0.00 pp change) and a negligible +0.24 pp F1 change (40.00% EM). "
        "Dense retrieval alone, once paired with cross-encoder reranking, captures all necessary evidence; BM25 lexical fusion is completely redundant once neural "
        "reranking is in place. Conversely, omitting dense retrieval (Abl_BM25_Only) drops AllSF@5 by -5.20 pp, confirming that dense representations are necessary "
        "to bridge semantic vocabulary gaps."
    )

    # --- 4.5 TABLE 3A: PAIRED BOOTSTRAP SIGNIFICANCE ---
    add_sec_heading("4.5 Paired Bootstrap Resampling Significance Analysis", level=2)
    add_p(
        "To evaluate whether the observed point differences reflect genuine distributional separation, we executed paired bootstrap resampling (B=10,000 resamples). "
        "Table 5 presents the empirical 95% confidence intervals and Holm-adjusted p-values across two pre-registered families: Primary Retrieval Coverage (AllSF@5, m=8) "
        "and Downstream Token Overlap (F1, m=5)."
    )
    add_caption("Table 5. Paired bootstrap hypothesis testing on S8 vs. alternative configurations (B=10,000 resamples, 95% CI, Holm-Bonferroni corrected).")

    t3a_data = [
        ["Comparison Pair", "Metric", "S8 Score", "Base Score", "Mean Diff", "95% Bootstrap CI", "Raw p", "Holm p", "Sig. (α=0.05)?"],
        ["Family 1: Primary Retrieval Coverage (AllSF@5, m=8 tests; Raw p < 0.0001 represents bootstrap floor 1/(B+1))", "", "", "", "", "", "", "", ""],
        ["S8 vs S2_Dense", "AllSF", "85.60%", "70.60%", "+15.00%", "[+11.20, +19.00]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs S3_Hybrid", "AllSF", "85.60%", "67.20%", "+18.40%", "[+14.60, +22.20]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs S5_Hybrid_Rerank", "AllSF", "85.60%", "82.60%", "+3.00%", "[+1.40, +4.80]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs S7_Iterative_Dense", "AllSF", "85.60%", "72.80%", "+12.80%", "[+8.60, +17.00]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs Abl_No_Reranker", "AllSF", "85.60%", "63.00%", "+22.60%", "[+18.60, +26.80]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs Abl_BM25_Only", "AllSF", "85.60%", "80.40%", "+5.20%", "[+3.00, +7.40]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs S5_Ctrl_Pool50", "AllSF", "85.60%", "82.80%", "+2.80%", "[+0.40, +5.20]", "0.0240", "0.0480", "Yes (Borderline)"],
        ["S8 vs Abl_Dense_Only", "AllSF", "85.60%", "85.60%", "0.00%", "[-2.00, +2.00]", "1.0000", "1.0000", "No"],
        ["Family 2: Downstream Token Overlap (F1 Score, m=5 tests)", "", "", "", "", "", "", "", ""],
        ["S8 vs S3_Hybrid", "F1", "51.14%", "43.88%", "+7.26%", "[+3.82, +10.73]", "< 0.0001", "0.0005", "Yes"],
        ["S8 vs Abl_No_Reranker", "F1", "51.14%", "45.82%", "+5.32%", "[+1.78, +8.92]", "0.0024", "0.0096", "Yes"],
        ["S8 vs S5_Hybrid_Rerank", "F1", "51.14%", "49.15%", "+1.98%", "[+0.50, +3.59]", "0.0070", "0.0210", "Yes"],
        ["S8 vs S2_Dense", "F1", "51.14%", "47.11%", "+4.03%", "[+0.45, +7.58]", "0.0280", "0.0560", "No"],
        ["S8 vs S5_Ctrl_Pool50", "F1", "51.14%", "49.31%", "+1.83%", "[-0.08, +3.82]", "0.0594", "0.0594", "No"]
    ]
    t3a = doc.add_table(rows=len(t3a_data), cols=9)
    t3a.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3a)
    for r_idx, row in enumerate(t3a.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t3a_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [1, 10]:
            format_row(row, bg_hex="E6EDF5", bold=True, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
            # merge across
            a, b = row.cells[0], row.cells[8]
            a.merge(b)
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: Confidence intervals derived from empirical percentiles [2.5%, 97.5%]. Raw p < 0.0001 represents the bootstrap floor 1/(B+1).")

    add_p(
        "In Family 1 (AllSF@5), S8 demonstrates statistically significant retrieval superiority over unreranked baselines (S2, S3, S7) and Abl_No_Reranker "
        "(all p_holm = 0.0008). However, when evaluated against the fair Pool-50 single-pass control (S5_Ctrl), S8's +2.80 pp advantage yields a 95% confidence "
        "interval of [+0.40, +5.20] with a raw p-value of 0.0240 and a Holm-corrected p-value of 0.0480. This result is technically significant at alpha=0.05, "
        "but it sits directly on the boundary of significance."
    )
    add_p(
        "Crucially, look at Family 2 (F1 score). S8's token-overlap improvements over single-pass dense retrieval S2 (+4.03 pp, p_holm = 0.0560) and fair "
        "single-pass control S5_Ctrl (+1.83 pp, 95% CI [-0.08, +3.82], p_holm = 0.0594) both fail to achieve statistical significance. Despite the high "
        "retrieval recall, downstream answer improvements dissolve under rigorous statistical correction."
    )

    # --- 4.6 TABLE 3B: MCNEMAR TEST ---
    add_sec_heading("4.6 Confirmation via McNemar's Non-Parametric Paired Test", level=2)
    add_p(
        "Because Exact Match is a binary 0/1 variable, paired t-tests or unadjusted McNemar tests can yield misleading inferences. Table 6 reports continuity-corrected "
        "McNemar tests across all six pre-registered EM comparison pairs, ordered by rank and corrected via Holm step-down."
    )
    add_caption("Table 6. McNemar's paired test on Exact Match (m=6 comparisons, continuity-corrected χ², Holm step-down).")

    t3b_data = [
        ["Rank (i)", "Comparison Pair", "S8 Win", "Other Win", "Continuity χ²", "Raw p", "Multiplier", "Corrected Holm p", "Sig. (α=0.05)?"],
        ["1", "S8 vs S3_Hybrid", "57", "26", "10.8434", "0.00099", "× 6", "0.0059", "Yes"],
        ["2", "S8 vs Abl_No_Reranker", "49", "29", "4.6282", "0.0315", "× 5", "0.1575", "No"],
        ["3", "S8 vs S2_Dense", "50", "35", "2.3059", "0.1289", "× 4", "0.5156", "No"],
        ["4", "S8 vs S7_Iterative_Dense", "49", "38", "1.1494", "0.2837", "× 3", "0.8511", "No"],
        ["5", "S8 vs S5_Hybrid_Rerank", "10", "5", "1.0667", "0.3017", "× 2 (cummax)", "0.8511", "No"],
        ["6", "S8 vs S5_Ctrl_Pool50", "14", "9", "0.6957", "0.4042", "× 1 (cummax)", "0.8511", "No"]
    ]
    t3b = doc.add_table(rows=len(t3b_data), cols=9)
    t3b.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3b)
    for r_idx, row in enumerate(t3b.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t3b_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 1:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            for c in [2, 3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            for c in [2, 3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: Continuity correction (|b - c| - 1)^2 / (b + c) applied to all discordant pairs. Multipliers enforce step-down Holm correction.")

    add_p(
        "The McNemar testing reveals an unambiguous statistical reality: across all six binary EM comparisons, S8 achieves a statistically significant accuracy "
        "gain solely against unreranked hybrid retrieval S3 (57 wins vs 26 losses, chi2=10.8434, p_holm = 0.0059). Against Abl_No_Reranker, S8's raw p-value of "
        "0.0315 is extinguished by the Holm multiplier (p_holm = 0.1575). Against dense retrieval S2, S8 produces 50 wins and 35 losses, yielding a non-significant "
        "p_holm = 0.5156. Finally, against fair single-pass control S5_Ctrl, S8 produces 14 wins against 9 losses (a net advantage of only 5 questions out of 500), "
        "yielding chi2=0.6957 and p_holm = 0.8511."
    )

    # --- 4.7 TABLE 4A: RETRIEVAL DEPTH CURVES ---
    add_sec_heading("4.7 Multi-Retriever Depth Curves across K ∈ {5, 10, 25, 50}", level=2)
    add_p(
        "To understand whether retrieval exhaustion can be achieved simply by expanding candidate depth, we evaluate AllSF recall curves across depths "
        "K in {5, 10, 25, 50}, broken down by question type: Bridge (N=404) vs. Comparison (N=96) (Table 7)."
    )
    add_caption("Table 7. Supporting facts recall curves across retrieval depths on the 19,260-passage corpus.")

    t4a_data = [
        ["Retriever Architecture", "Question Subgroup", "AllSF@5 (%)", "AllSF@10 (%)", "AllSF@25 (%)", "AllSF@50 (%)", "Depth Saturation Behavior"],
        ["BM25 Sparse Okapi", "Bridge (N=404)", "44.06%", "60.64%", "72.28%", "77.72%", "Incomplete; missing lexical bridge tokens"],
        ["BM25 Sparse Okapi", "Comparison (N=96)", "58.33%", "75.00%", "88.54%", "94.79%", "High saturation at K=50"],
        ["Dense BGE-Small", "Bridge (N=404)", "63.86%", "74.50%", "82.67%", "88.37%", "Superior semantic discovery; beats Hybrid at K=5"],
        ["Dense BGE-Small", "Comparison (N=96)", "98.96%", "100.00%", "100.00%", "100.00%", "Ceiling (100.0%) reached at K=10"],
        ["Hybrid RRF Fusion", "Bridge (N=404)", "61.14%", "76.73%", "84.65%", "88.12%", "Underperforms Dense on Bridge at K=5 (61.1% vs 63.9%)"],
        ["Hybrid RRF Fusion", "Comparison (N=96)", "97.92%", "100.00%", "100.00%", "100.00%", "Ceiling (100.0%) reached at K=10"]
    ]
    t4a = doc.add_table(rows=len(t4a_data), cols=7)
    t4a.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4a)
    for r_idx, row in enumerate(t4a.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t4a_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4, 5]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Evaluated on partitioned subsets. A minor 1.0 pp variance exists against Table 2 global run due to local RRF tie-breaking.")

    add_p(
        "Table 7 reveals sharp behavioral divergences between query types. Comparison questions are trivial for dense representations: Dense BGE-Small "
        "retrieves all supporting facts for 98.96% of comparison questions at K=5, and reaches a perfect 100.00% ceiling at K=10. This occurs because comparison "
        "questions explicitly name both entities in the query string (e.g., 'Were Arthur Conan Doyle and Agatha Christie both British?'), enabling single-pass "
        "dense search to match both entities simultaneously."
    )
    add_p(
        "Bridge questions, by contrast, exhibit a severe lexical bottleneck. BM25 reaches only 44.06% AllSF@5 on Bridge questions because the second fact's "
        "entity is unmentioned in the original prompt. Furthermore, Hybrid RRF actually underperforms Dense retrieval on Bridge questions at K=5 (61.14% vs 63.86%). "
        "Blending lexical scores into dense ranks dilutes high-quality semantic candidates with keyword-heavy distractors."
    )

    # --- 4.8 TABLE 4B: EVIDENCE RECOVERY FUNNEL & 2x2 ---
    add_sec_heading("4.8 Stage-Wise Evidence Recovery Funnel and Paired 2×2 Contingency", level=2)
    add_p(
        "Where does the second supporting fact actually get captured, and what does the iterative loop break? Table 8 tracks the evidence discovery funnel across "
        "the 500 benchmark questions, paired with a 2x2 contingency matrix comparing S8 against the fair single-pass control S5_Ctrl."
    )
    add_caption("Table 8. Multi-hop evidence recovery funnel and paired 2×2 contingency table on AllSF@5 (N=500 questions).")

    t4b_data = [
        ["Evidence Discovery Stage / Metric", "Question Count", "Corpus Share (%)", "Stage Meaning & Bottleneck Mechanism"],
        ["Hop 1 Pool Capture", "438 / 500", "87.60%", "Both gold facts discoverable in initial 25-candidate hybrid pool"],
        ["Hop 2 Rescued Evidence", "32 / 500", "6.40%", "Fact 2 missing in Hop 1 pool; surfaced by iterative query"],
        ["Total Candidate Pool Capture", "470 / 500", "94.00%", "Upper ceiling of evidence captured across both 25-candidate pools"],
        ["Top-5 Reranking Truncation Loss", "42 / 500", "8.40%", "Questions present in 50-pool but lost during top-5 truncation (470 → 428)"],
        ["Never Retrieved (Hard Floor)", "30 / 500", "6.00%", "Neither hop retrieved both facts from the 19,260-passage corpus"],
        ["Final S8 Top-5 Coverage", "428 / 500", "85.60%", "Final context fed to reader containing all supporting facts"]
    ]
    t4b = doc.add_table(rows=len(t4b_data), cols=4)
    t4b.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4b)
    for r_idx, row in enumerate(t4b.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t4b_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [3, 6]:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Sum of Hop 1 (438) + Hop 2 Rescued (32) = 470 pool capture. Truncation loss drops pool to 428 final hits.")

    add_p(
        "To reconcile the exact mechanism of Hop-2 retrieval, consider the paired 2×2 contingency table on AllSF@5 between S8 Staged and S5_Ctrl Pool-50:\n"
        "• Both Hit (S8=1, Ctrl=1): 402 questions (80.40%)\n"
        "• S8 Pipeline Win (S8=1, Ctrl=0): 26 questions (5.20%)\n"
        "• S5_Ctrl Control Win (S8=0, Ctrl=1): 12 questions (2.40%)\n"
        "• Neither Hit (S8=0, Ctrl=0): 60 questions (12.00%)\n"
        "Total Hits: S8 = 402 + 26 = 428 (85.60%); S5_Ctrl = 402 + 12 = 414 (82.80%)."
    )
    add_p(
        "This paired breakdown illuminates what happens inside the iterative loop. While Hop 2 rescues 32 questions into the candidate pool, "
        "neural reranking and truncation discard 42 questions. When evaluated strictly against fair single-pass retrieval (S5_Ctrl), S8 gains 26 questions "
        "where Hop 2 successfully bridged to Fact 2, but it simultaneously degrades 12 questions that S5_Ctrl captured cleanly. In those 12 cases, the iterative "
        "query introduced irrelevant distractor passages that knocked gold facts out of the top-5 during reranking. The net gain is exactly 26 − 12 = +14 questions "
        "(+2.80 pp), yielding the borderline Holm p-value of 0.0480."
    )

    # --- 4.9 TABLE 4D: QUERY FORMULATION S10 VS S8 ---
    add_sec_heading("4.9 Hop-2 Query Formulation: S10 (LLM Query) vs. S8 (Heuristic Query)", level=2)
    add_p(
        "Given the limitations of simple snippet concatenation, we evaluated an intuitive enhancement: using an LLM to generate a targeted sub-query "
        "for Hop 2 (System S10). Table 9 contrasts S10 against the heuristic concatenation used in S8."
    )
    add_caption("Table 9. Paired bootstrap comparison of Hop-2 query formulation: LLM Query Substitution (S10) vs. Heuristic Query (S8).")

    t4d_data = [
        ["Evaluated Metric", "S10 (LLM Query)", "S8 (Heuristic)", "Net Difference", "95% Bootstrap CI", "Holm p-value", "Significant (α=0.05)?"],
        ["AllSF@5 (Retrieval Coverage)", "82.60%", "85.60%", "-3.00 pp", "[-4.80, -1.40]", "0.0003", "Yes (S8 Superior)"],
        ["F1 Score (Token Overlap)", "49.15%", "51.14%", "-1.98 pp", "[-3.61, -0.52]", "0.0188", "Yes (S8 Superior)"],
        ["Exact Match (Accuracy)", "38.80%", "39.80%", "-1.00 pp", "[-2.60, +0.40]", "0.2428", "No"]
    ]
    t4d = doc.add_table(rows=len(t4d_data), cols=7)
    t4d.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4d)
    for r_idx, row in enumerate(t4d.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t4d_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [1, 2, 3, 4, 5]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[6].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: Negative Net Difference indicates performance degradation under LLM query reformulation relative to S8 heuristic concatenation.")

    add_p(
        "The outcome of Table 9 was not what we anticipated. Prompting an LLM to generate targeted search queries caused AllSF@5 to decline by -3.00 pp "
        "(p_holm = 0.0003) and F1 to drop by -1.98 pp (p_holm = 0.0188). Manual inspection of S10 queries revealed that the language model frequently "
        "hallucinated plausible entity relations or over-specified search criteria, drifting away from the exact lexical phrasing present in the corpus. "
        "The simple heuristic of appending the original question to raw snippets from the top Hop 1 passage preserved ground-truth entity anchors far more "
        "effectively than neural query rewriting."
    )

    # --- 4.10 TABLE 6: GENERATOR CAPACITY ---
    add_sec_heading("4.10 Generator Capacity Diagnostic: 3B vs. 7B Parameter Scaling", level=2)
    add_p(
        "To test whether downstream accuracy is constrained by retrieved evidence or reader reasoning capacity, we scaled the generator from Qwen2.5-3B "
        "to Qwen2.5-7B, evaluating both models on identical retrieved contexts (Table 10)."
    )
    add_caption("Table 10. Generator capacity diagnostic: Paired bootstrap comparison of 3B vs. 7B reader scaling on identical contexts.")

    t6_data = [
        ["Comparison Pair", "Context Evidence Fed", "Metric", "3B Score", "7B Score", "Net Gain (Δ pp)", "95% Bootstrap CI", "Holm p-value"],
        ["S8_7B vs S8_3B", "S8 Retrieved Passages", "Exact Match (EM)", "39.80%", "52.00%", "+12.20 pp", "[+8.20, +16.20]", "0.0004 (Yes)"],
        ["S8_7B vs S8_3B", "S8 Retrieved Passages", "F1 Score", "51.14%", "64.32%", "+13.18 pp", "[+9.64, +16.80]", "0.0004 (Yes)"],
        ["S9_7B vs S9_3B", "Gold Oracle Passages", "Exact Match (EM)", "53.00%", "60.20%", "+7.20 pp", "[+3.60, +10.80]", "0.0004 (Yes)"],
        ["S9_7B vs S9_3B", "Gold Oracle Passages", "F1 Score", "66.80%", "75.10%", "+8.30 pp", "[+5.13, +11.55]", "0.0004 (Yes)"]
    ]
    t6 = doc.add_table(rows=len(t6_data), cols=8)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t6)
    for r_idx, row in enumerate(t6.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t6_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 1:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Evaluated across N=500 questions. Both 3B and 7B models evaluated on identical retrieved passage lists.")

    add_p(
        "Table 10 presents the most striking empirical result in this study. When evaluated on the exact same retrieved evidence from S8, scaling the reader "
        "from 3B to 7B increases Exact Match by +12.20 pp (from 39.80% to 52.00%, p_holm = 0.0004) and F1 by +13.18 pp (from 51.14% to 64.32%). "
        "Crucially, the 7B reader's performance on imperfect retrieved evidence (52.00% EM) is comparable to the 3B reader's performance under perfect gold oracle "
        "evidence (53.00% EM)."
    )
    add_p(
        "To put this in perspective: optimizing the retrieval stack through hybrid fusion, iterative Hop-2 query augmentation, and neural reranking improved "
        "Exact Match by +3.00 pp over single-pass dense retrieval S2. Upgrading the reader model from 3B to 7B on identical passages yielded four times that gain "
        "(+12.20 pp). Downstream accuracy is overwhelmingly bottlenecked by reader parameterization rather than retrieval recall."
    )

    # --- 4.11 TABLE 5: LATENCY ---
    add_sec_heading("4.11 Computational Latency and Throughput Benchmarking", level=2)
    add_p(
        "Engineering decisions require weighing statistical gains against inference overhead. Table 11 benchmarks the runtime latency and throughput of each "
        "retrieval stack module on dual NVIDIA Tesla T4 GPUs."
    )
    add_caption("Table 11. Computational latency and throughput profiling of retrieval modules on dual NVIDIA Tesla T4 GPUs.")

    t5_data = [
        ["Retrieval Stage Module", "Underlying Technology", "Mean Latency (s/query)", "Throughput (qps)", "Retrieval Stack Share (%)"],
        ["Dense Embedding Retrieval", "BAAI/bge-small-en-v1.5 + Dot Product", "0.0139 s", "71.9 qps", "2.1%"],
        ["BM25 Sparse Retrieval", "RankBM25 Okapi (Inverted Index)", "0.0724 s", "13.8 qps", "11.0%"],
        ["Hybrid RRF Fusion", "Reciprocal Rank Fusion (k=60)", "0.1169 s", "8.5 qps", "17.8%"],
        ["Cross-Encoder Reranker", "BAAI/bge-reranker-base (max_len=256)", "0.4560 s", "2.2 qps", "69.1% (Dominant Cost)"]
    ]
    t5 = doc.add_table(rows=len(t5_data), cols=5)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t5)
    for r_idx, row in enumerate(t5.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t5_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 4:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Profiles retrieval stack exclusively. Reader generation adds ~0.45 s/query for 3B and ~0.91 s/query for 7B.")

    add_p(
        "Cross-encoder reranking accounts for 69.1% of total retrieval latency (0.4560 seconds per query, achieving 2.2 qps), representing a 33× latency penalty "
        "relative to dense vector search (0.0139 s, 71.9 qps). While the reranker delivers substantial recall (+15.40 pp AllSF@5), its quadratic token-level "
        "attention imposes severe computational costs. Downstream text generation adds an additional ~0.45 s for the 3B reader and ~0.91 s for the 7B reader, "
        "bringing total pipeline latency to 1.1–1.5 seconds per multi-hop question."
    )

    # --- 4.12 TABLE 4C: MANUAL ERROR ANALYSIS ---
    add_sec_heading("4.12 Hand-Verified Qualitative Error Analysis (N=60 Failure Cases)", level=2)
    add_p(
        "To diagnose why downstream generation stalls even when supporting facts are retrieved, we conducted a manual, hand-verified error audit of 60 randomly "
        "sampled failure cases from S8 (Table 12), computing Wilson score 95% confidence intervals."
    )
    add_caption("Table 12. Hand-verified qualitative error breakdown across N=60 randomly sampled S8 failure cases.")

    t4c_data = [
        ["Mutually Exclusive Failure Tag", "Frequency", "Share (%)", "Wilson 95% CI", "Decision Rule & Primary Failure Mechanism"],
        ["Granularity / Format Artifact", "22 / 60", "36.70%", "[25.5%, 49.3%]", "Both facts present; model gives semantically correct answer penalized by exact match"],
        ["Reasoning Failure under Evidence", "19 / 60", "31.70%", "[21.2%, 44.2%]", "Partial or full gold evidence in prompt; 3B model fails logical constraint synthesis"],
        ["Retrieval Gap (Missing Fact 2)", "13 / 60", "21.70%", "[13.1%, 33.6%]", "Hop 1 retrieved Fact 1, but Hop 2 query failed to bridge to Fact 2"],
        ["Span Extraction Error", "6 / 60", "10.00%", "[4.7%, 20.1%]", "Both facts retrieved; generator extracted adjacent distractor entity from paragraph"]
    ]
    t4c = doc.add_table(rows=len(t4c_data), cols=5)
    t4c.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4c)
    for r_idx, row in enumerate(t4c.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t4c_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [1, 2]:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: Evaluated under single-annotator blind verification. Categories are mutually exclusive and sum to 100%.")

    add_p(
        "The manual audit uncovers the real culprit behind low Exact Match scores. Over a third of all failures (36.70%, Wilson CI [25.5%, 49.3%]) are "
        "format artifacts: the generator produced the semantically correct entity, but was penalized by string mismatch (e.g., answering 'US' instead of "
        "'United States', or omitting parenthetical qualifiers). When combined with Reasoning Failures (31.70%), where the 3B model failed multi-hop logical "
        "deduction despite having gold passages in its prompt, we find that 68.4% of all pipeline failures occur on the reader side. Actual retrieval failures "
        "(Missing Fact 2) account for only 21.70% of errors."
    )

    # =========================================================================
    # 6. DISCUSSION
    # =========================================================================
    add_sec_heading("5. Discussion", level=1)
    add_p(
        "Synthesizing these ten empirical analyses yields a single, coherent narrative: retrieval coverage and downstream answer accuracy are fundamentally "
        "decoupled in multi-hop RAG systems. The common assumption that improving multi-hop retrieval recall will automatically translate into downstream "
        "QA accuracy is contradicted by our data."
    )
    add_p(
        "Throughout our experiments, neural cross-encoder reranking consistently emerges as the dominant retrieval lever, contributing +15.40 pp in AllSF@5. "
        "Iterative second-hop retrieval, by contrast, contributes an incremental +2.80 pp AllSF gain that sits right on the edge of statistical significance "
        "(p_holm = 0.0480), and yields zero detectable improvement in downstream Exact Match (p_holm = 0.8511). As demonstrated in our 2×2 contingency analysis, "
        "the 32 questions rescued by Hop 2 are largely offset by 42 questions lost during truncation and 12 questions actively degraded by query noise."
    )
    add_p(
        "Meanwhile, generator parameterization exerts an overwhelming influence. Scaling from a 3B to a 7B reader model on identical retrieved passages produces "
        "a +12.20 pp jump in Exact Match—four times the gain achieved by moving from single-pass dense search to full iterative multi-hop retrieval (+3.00 pp). "
        "Coupled with our error breakdown showing that 36.70% of failures are string-matching artifacts, we conclude that future research in multi-hop QA should "
        "focus on reader reasoning capabilities, context distillation, and metric normalization rather than engineering increasingly intricate retrieval loops."
    )

    # =========================================================================
    # 7. LIMITATIONS
    # =========================================================================
    add_sec_heading("6. Limitations", level=1)
    add_p(
        "We note several concrete methodological limitations of this study:\n"
        "1. Corpus Construction: Our evaluation index comprises 19,260 passages constructed by pooling gold and distractor paragraphs from the HotpotQA development set. "
        "While highly challenging due to dense distractor competition, this corpus is substantially smaller than full 5-million-page Wikipedia dumps, where retrieval "
        "dilution may follow different scaling dynamics.\n"
        "2. Sample Size and Split Stability: All evaluations were conducted on a single fixed subset of 500 questions (N=500). While sufficient to power paired testing, "
        "the 96 comparison questions represent a relatively small sample, meaning subtle subgroup differences may be underpowered.\n"
        "3. Generator Architecture: Experiments were restricted to the Qwen2.5 open-weights series (3B and 7B). While highly representative of modern dense instruct models, "
        "we cannot entirely rule out potential pre-training exposure to HotpotQA text.\n"
        "4. Single-Annotator Error Analysis: Our qualitative analysis of 60 failure cases was hand-verified by a single annotator; consequently, inter-annotator agreement "
        "(e.g., Cohen's kappa) could not be calculated.\n"
        "5. Metric Constraints: We adhered to standard HotpotQA Exact Match and token F1 metrics. Evaluating alias-aware or model-based semantic evaluation metrics was beyond "
        "the scope of this study."
    )

    # =========================================================================
    # 8. CONCLUSION
    # =========================================================================
    add_sec_heading("7. Conclusion", level=1)
    add_p(
        "In this empirical diagnostic study, we investigated the stage-wise mechanisms governing multi-hop RAG systems on HotpotQA. Through thirteen controlled system "
        "evaluations, paired bootstrap resampling, Holm-corrected McNemar tests, and manual error audits, we showed that the performance bottleneck in multi-hop QA "
        "is not retrieval recall. Cross-encoder reranking accounts for virtually all meaningful retrieval improvements, while iterative second-hop query augmentation "
        "delivers modest, borderline gains that fail to reach downstream answer accuracy. Over 78% of the downstream performance deficit originates on the generator "
        "and metric side, where reader parameter scaling provides four times the benefit of retrieval pipeline optimization. For practitioners and researchers, "
        "these results suggest that efforts to improve multi-hop QA are better spent strengthening reader reasoning and resolving surface-form metric fragility than "
        "constructing ever-more elaborate iterative retrieval pipelines."
    )

    # =========================================================================
    # 9. REFERENCES
    # =========================================================================
    add_sec_heading("8. References", level=1)
    refs = [
        "Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009). Reciprocal rank fusion outperforms indri and lucene for combined search. In Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval (pp. 758–759).",
        "Efron, B., & Tibshirani, R. J. (1993). An Introduction to the Bootstrap. Chapman & Hall/CRC.",
        "Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics, 6(2), 65–70.",
        "Karpukhin, V., Oguz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W.-t. (2020). Dense passage retrieval for open-domain question answering. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP) (pp. 6769–6781).",
        "Khattab, O., Santhanam, K., Li, X. L., Hall, D., & Liang, P. (2021). Demonstrate-search-predict: Composing retrieval and language models for knowledge-intensive NLP. arXiv preprint arXiv:2212.14024.",
        "McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika, 12(2), 153–157.",
        "Nogueira, R., & Cho, K. (2019). Passage re-ranking with BERT. arXiv preprint arXiv:1901.04085.",
        "Qwen Team. (2024). Qwen2.5: A party of foundation and instruction-tuned large language models. arXiv preprint arXiv:2412.15115.",
        "Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. Foundations and Trends in Information Retrieval, 3(4), 333–389.",
        "Trivedi, H., Balasubramanian, N., Khot, T., & Sabharwal, A. (2022). Interleaving retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023) (pp. 10014–10037).",
        "Xiao, S., Liu, Z., Zhang, P., & Muennighoff, N. (2023). C-pack: Packaged resources to advance general Chinese embedding (BAAI BGE models). arXiv preprint arXiv:2309.07597.",
        "Yang, Z., Qi, P., Zhang, S., Bengio, Y., Cohen, W. W., Salakhutdinov, R., & Manning, C. D. (2018). HotpotQA: A dataset for diverse, explainable multi-hop question answering. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP) (pp. 2369–2380)."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.05
        r_run = p_ref.add_run(r)
        r_run.font.name = 'Times New Roman'
        r_run.font.size = Pt(9.5)

    out_path = r"C:\Users\abira\Desktop\MultiHop-RAG-Diagnosis\Diagnosing_MultiHop_RAG_Paper.docx"
    doc.save(out_path)
    print(f"Research paper successfully created at: {out_path}")

if __name__ == "__main__":
    build_paper()
