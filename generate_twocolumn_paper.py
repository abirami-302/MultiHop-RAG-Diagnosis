# -*- coding: utf-8 -*-
"""
generate_twocolumn_paper.py
Rebuilds the publication-grade, human-written two-column research paper incorporating
all mentor audit corrections:
1. Removed S10 completely (Table 9 deleted, references in 3.2 and 4.9 excised).
2. Cleaned and hedged Hop-2 retrieval gain (+2.8 pp) without unverified p-values.
3. Cleaned all figures to match exact empirical tables:
   - Figure 1: Architecture diagram reflecting real code (top-2 passages, 200 chars).
   - Figure 2: Ablation bar chart (untruncated axis).
   - Figure 3: Empirical Hybrid Depth curve from Table 7.
   - Figure 4: Paired 2x2 contingency matrix (S8 vs S5_Ctrl).
   - Figure 5: Generator capacity bar chart (3B vs 7B on identical evidence).
   - Figure 6: Subgroup depth curves (Bridge vs Comparison) matching Table 7.
4. Corrected citations: Min et al. 2019 (Compositional questions), Khattab DSP, Asai Self-RAG, etc.
5. Re-framed claims: Diminishing returns beyond 70% AllSF (not 'decoupled'), underpowered EM tests,
   reader prompt explicitly stated, corpus pooling transparently documented.
6. Concisely written abstract (~210 words).
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
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

def format_row(row, bg_hex=None, bold=False, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT, color_hex="000000"):
    for cell in row.cells:
        if bg_hex:
            set_cell_shading(cell, bg_hex)
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = align
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.line_spacing = 1.05
            for r in p.runs:
                r.bold = bold
                r.font.name = "Times New Roman"
                r.font.size = Pt(font_size)
                if color_hex != "000000":
                    r.font.color.rgb = RGBColor(int(color_hex[:2], 16), int(color_hex[2:4], 16), int(color_hex[4:], 16))

def build_paper():
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(9.5)
    style_normal.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

    def add_p(text="", bold_prefix="", italic_note="", space_after=4, line_spacing=1.08, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Times New Roman'
            r_b.font.size = Pt(9.5)
        if text:
            r_t = p.add_run(text)
            r_t.font.name = 'Times New Roman'
            r_t.font.size = Pt(9.5)
        if italic_note:
            r_i = p.add_run(italic_note)
            r_i.italic = True
            r_i.font.name = 'Times New Roman'
            r_i.font.size = Pt(9)
        return p

    def add_sec_heading(title, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.bold = True
        r.font.name = 'Times New Roman'
        if level == 1:
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(0x00, 0x2B, 0x49)
        elif level == 2:
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        else:
            r.font.size = Pt(9.5)
            r.italic = True
            r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x00, 0x2B, 0x49)
        return p

    def add_table_note(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(5)
        r = p.add_run(text)
        r.italic = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        return p

    def add_image_box(img_filename, caption_text, width_inches=3.3):
        img_path = os.path.join(r"C:\Users\abira\OneDrive\Desktop\MultiHop-RAG-Diagnosis\images", img_filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            p_img.add_run().add_picture(img_path, width=Inches(width_inches))
            add_caption(caption_text)

    # =========================================================================
    # BANNER
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Diagnosing the Multi-Hop Retrieval-Generation Gap:\nA Stage-Wise Empirical Study on HotpotQA")
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(0x00, 0x2B, 0x49)

    p_aut = doc.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aut.paragraph_format.space_before = Pt(2)
    p_aut.paragraph_format.space_after = Pt(2)
    r_aut = p_aut.add_run("Abirami K   ·   Madhumitha P S\n")
    r_aut.bold = True
    r_aut.font.name = 'Times New Roman'
    r_aut.font.size = Pt(10.5)
    r_aut.font.color.rgb = RGBColor(0x00, 0x2B, 0x49)
    
    r_aff = p_aut.add_run("Department of Computer Science and Engineering\nabiramikondaiyan@gmail.com\nSeptember 2026")
    r_aff.font.name = 'Times New Roman'
    r_aff.font.size = Pt(9)
    r_aff.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(2)
    p_rep.paragraph_format.space_after = Pt(6)
    r_rep = p_rep.add_run("Code & Data Availability: Complete execution scripts, raw checkpoint outputs, and paired bootstrap logs are open-source at https://github.com/abirami-302/MultiHop-RAG-Diagnosis under the MIT License.")
    r_rep.font.name = 'Times New Roman'
    r_rep.font.size = Pt(8.5)
    r_rep.italic = True
    r_rep.font.color.rgb = RGBColor(0x00, 0x44, 0x88)

    # Boxed Abstract Table
    t_abs = doc.add_table(rows=1, cols=2)
    t_abs.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_abs, color="B0C4DE")
    c_info = t_abs.rows[0].cells[0]
    c_body = t_abs.rows[0].cells[1]
    set_cell_shading(c_info, "F0F4F8")
    set_cell_shading(c_body, "FCFDFE")
    set_cell_margins(c_info, top=80, bottom=80, left=100, right=100)
    set_cell_margins(c_body, top=80, bottom=80, left=120, right=120)

    p_inf = c_info.paragraphs[0]
    p_inf.paragraph_format.space_before = Pt(0)
    p_inf.paragraph_format.space_after = Pt(0)
    p_inf.paragraph_format.line_spacing = 1.05
    r_ih = p_inf.add_run("ARTICLE INFO\n\nKeywords:\n")
    r_ih.bold = True
    r_ih.font.name = "Times New Roman"
    r_ih.font.size = Pt(8)
    r_ik = p_inf.add_run("• Multi-hop QA\n• Retrieval-Augmented Generation\n• HotpotQA Benchmark\n• Cross-Encoder Reranking\n• Paired Bootstrap Testing\n• Reader Capacity Scaling\n• Error Budget Decomposition")
    r_ik.font.name = "Times New Roman"
    r_ik.font.size = Pt(7.5)

    p_ab = c_body.paragraphs[0]
    p_ab.paragraph_format.space_before = Pt(0)
    p_ab.paragraph_format.space_after = Pt(0)
    p_ab.paragraph_format.line_spacing = 1.05
    p_ab.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_ah = p_ab.add_run("ABSTRACT\n")
    r_ah.bold = True
    r_ah.font.name = "Times New Roman"
    r_ah.font.size = Pt(8.5)
    r_at = p_ab.add_run(
        "Multi-hop question answering requires synthesizing evidence scattered across multiple source passages. "
        "While complex iterative retrieval pipelines are frequently proposed to address this challenge, their stage-wise error "
        "mechanisms remain insufficiently understood. In this study, we present an empirical diagnostic investigation comparing "
        "thirteen retrieval and generation configurations on a 500-question evaluation benchmark drawn from HotpotQA over a pooled "
        "corpus of 19,260 passages under a unified execution protocol. Using paired bootstrap resampling (B=10,000) and McNemar's "
        "paired non-parametric tests with Holm-Bonferroni family-wise error control, we decouple the relative impact of neural reranking, "
        "iterative querying, and generator capacity. Our findings reveal that cross-encoder reranking yields the single largest retrieval "
        "gain (+15.40 pp AllSF@5), whereas iterative second-hop retrieval contributes a modest gain (+2.80 pp AllSF@5) that fails to translate "
        "into statistically detectable downstream Exact Match improvements. Decomposing the end-to-end performance deficit reveals that imperfect "
        "retrieval accounts for only 21.9% of the overall Exact Match deficit under a 3B reader, contracting to 17.1% under a 7B reader. "
        "Providing identical retrieved evidence to a 7B reader improves Exact Match by +12.20 pp (reaching 52.00%, comparable to the 3B model's "
        "gold-evidence ceiling of 53.00%). A hand-verified error audit of 60 failure cases reveals that 36.70% of downstream errors stem from "
        "surface-form metric penalties rather than factual errors. These results demonstrate that multi-hop RAG systems operating over "
        "distractor-rich corpora face severe diminishing returns from retrieval optimization and are predominantly reader-and-metric-bound."
    )
    r_at.font.name = "Times New Roman"
    r_at.font.size = Pt(8)

    # TWO-COLUMN SECTION
    sec_twocol = doc.add_section(WD_SECTION.CONTINUOUS)
    sectPr = sec_twocol._sectPr
    cols = parse_xml(f'<w:cols {nsdecls("w")} w:num="2" w:space="720"/>')
    sectPr.append(cols)

    # 1. INTRODUCTION
    add_sec_heading("1. Introduction", level=1)
    add_p(
        "Retrieval-Augmented Generation (RAG) has emerged as the standard paradigm for grounding large language models "
        "in verifiable external documentation [1, 2]. By dynamically querying non-parametric text indices at inference time, "
        "RAG systems mitigate factual hallucinations, navigate knowledge cutoff constraints, and provide inspectable citations [3]. "
        "However, multi-step queries—such as synthesizing entity relationships across separate Wikipedia passages—frequently "
        "expose acute retrieval bottlenecks [4]."
    )
    add_p(
        "The standard response in recent literature has been architectural: introducing multi-agent debate loops, iterative query reformulations, "
        "and multi-hop graph traversals, exemplified by frameworks like IRCoT [5], DSP [6], and Self-RAG [7]. These architectures proceed from "
        "the assumption that missing evidence is the primary bottleneck suppressing downstream answer accuracy."
    )
    add_p(
        "Yet evaluating multi-hop systems often conflates retrieval recall gains with answer generation improvements [8]. Many reported "
        "improvements fail to isolate whether downstream accuracy gains originate from genuinely superior multi-hop evidence capture, broader "
        "context windows, or the downstream generator's capacity to digest noisy candidate sets [9]. Without stage-wise error decomposition "
        "and paired statistical testing, practitioners risk engineering intricate retrieval workflows to resolve what might actually be a reader reasoning "
        "or metric-formatting deficiency [10]."
    )
    add_p(
        "To investigate this dynamic, we conducted an empirical diagnostic study rather than proposing a new retrieval architecture. "
        "We evaluate multi-hop RAG stage by stage on HotpotQA [4], evaluating 500 questions against a pooled corpus of 19,260 passages on dual "
        "NVIDIA Tesla T4 GPUs. We systematically isolate sparse lexical retrieval (BM25 [11]), dense semantic search (BGE-Small [12]), "
        "reciprocal rank fusion (RRF [13]), neural cross-encoder reranking [14], and iterative second-hop retrieval. Crucially, we enforce "
        "controlled baselines, including an identical-pool single-pass control (Pool-50) and a wider-context baseline (K=10), paired bootstrap "
        "resampling with Holm-Bonferroni family-wise error control [15, 16], and McNemar's tests on paired binary Exact Match outcomes [17]."
    )

    add_sec_heading("1.1 Contributions", level=2)
    add_p(
        "Our paper provides an empirical diagnostic study rather than a novel pipeline architecture. Specifically, we report three core findings:"
    )
    add_p(
        "1. Stage-Wise Error Decomposition: We quantify the exact source of end-to-end performance loss (Table 1). Under a 3B reader, imperfect "
        "retrieval accounts for only 21.9% of the overall Exact Match deficit (13.20 pp out of 60.20 pp below 100%), while reader and metric artifacts account "
        "for 78.1% (47.00 pp). When evaluating a 7B reader over the exact same evidence, retrieval's share of the deficit contracts to 17.1% (8.20 pp), establishing "
        "that stronger generators exhibit greater resilience against distractor interference [18]."
    )
    add_p(
        "2. Retrieval Lever Disambiguation: Cross-encoder reranking serves as the dominant retrieval lever, contributing +15.40 pp in all-supporting-fact "
        "retrieval coverage (AllSF@5), whereas iterative Hop-2 query augmentation adds a modest +2.80 pp. Under paired McNemar testing, this retrieval gain "
        "produces no statistically detectable improvement in downstream Exact Match (p_holm = 0.8511)."
    )
    add_p(
        "3. Qualitative Failure Taxonomy: Through a hand-verified audit of 60 error cases, we demonstrate that 36.70% of generation failures "
        "represent surface-form metric artifacts where the model extracted the correct semantic fact but failed string-matching criteria. An additional 31.70% "
        "represent logical reasoning breakdowns despite having full or partial gold evidence in context. Collectively, these results show that multi-hop QA over "
        "distractor-rich corpora is primarily reader-and-metric-bound rather than retrieval-bound [19]."
    )

    # 2. RELATED WORK
    add_sec_heading("2. Related Work", level=1)
    add_p(
        "Dense passage retrieval [2] maps questions and candidate documents into a shared continuous semantic space via dual-encoder "
        "architectures. While effective for single-fact lookups, dense retrieval frequently misses lexical exact-matches such as entity acronyms and numerical codes, "
        "leading to the resurgence of hybrid retrieval paradigms that combine dense vectors with BM25 Okapi [11] via Reciprocal Rank Fusion (RRF) [13]. "
        "Cross-encoder neural rerankers [14] further refine candidate pools by performing full token-level cross-attention over query-document pairs, yielding "
        "substantial precision gains at the cost of quadratic computational complexity."
    )
    add_p(
        "For complex questions requiring multi-hop reasoning, single-pass retrieval often fails because the second supporting fact depends on entity links "
        "uncovered only in the first fact [4]. Iterative retrieval frameworks such as IRCoT [5] and DSP [6] address this by interleaving chain-of-thought "
        "generation with iterative retrieval calls. However, as Min et al. [20] observed, many multi-hop benchmark questions contain reasoning shortcuts "
        "where partial evidence suffices for answering, raising questions about whether iterative retrieval is always necessary."
    )
    add_p(
        "Furthermore, empirical rigor and statistical testing remain inconsistently applied in recent NLP literature [21]. Studies frequently report point differences "
        "on small test sets without paired non-parametric significance testing. We adopt paired bootstrap resampling [15] and McNemar's test for binary paired outcomes [17], "
        "enforcing family-wise error rate control via the Holm-Bonferroni step-down procedure [16] to establish reproducible diagnostic baselines."
    )

    # 3. METHODOLOGY
    add_sec_heading("3. Methodology", level=1)
    add_p(
        "To perform a clean diagnostic autopsy, we evaluate thirteen distinct system configurations and controlled ablations across a single, fixed evaluation "
        "protocol. In this section, we document our corpus construction, the thirteen evaluated pipeline configurations, metric definitions, and our statistical framework."
    )

    add_sec_heading("3.1 Evaluation Benchmark and Corpus Construction", level=2)
    add_p(
        "We construct our benchmark using the HotpotQA development set (distractor split) [4]. The full development set comprises 7,405 questions, each accompanied "
        "by two gold supporting passages and eight distractor paragraphs selected by TF-IDF similarity. To evaluate under a realistic open-retrieval setting without "
        "relying on external APIs, we construct a pooled local corpus of 19,260 unique passages by aggregating all context paragraphs associated with a fixed subset of "
        "2,000 development questions (N_CORPUS = 2000, SEED = 42). Because distractor paragraphs in HotpotQA share high lexical overlap with the query entities, "
        "this pooled corpus provides an adversarial environment with severe distractor competition."
    )
    add_p(
        "From this pooled corpus, we evaluate a fixed subset of 500 questions (N=500), comprising 404 bridge questions (80.8%) and 96 comparison "
        "questions (19.2%), preserving the natural difficulty distribution of the original benchmark. Hardware execution is fixed on dual NVIDIA Tesla T4 GPUs "
        "(16 GB VRAM each) hosted in a reproducible Kaggle environment."
    )

    add_sec_heading("3.2 Evaluated System Configurations and Controlled Baselines", level=2)
    add_p(
        "We examine thirteen distinct configurations, specifically formulated to isolate each component of the retrieval and generation stack:\n"
        "• S0 (Closed-Book Floor): Parametric knowledge alone; generator receives no context passages.\n"
        "• S1 (BM25 Okapi): Lexical sparse inverted indexing, returning top-5 passages [11].\n"
        "• S2 (Dense BGE-Small): Vector search via BAAI/bge-small-en-v1.5 (384-dim) with dot-product similarity, returning top-5 passages [12].\n"
        "• S3 (Hybrid RRF Fusion): Merges top-100 BM25 and top-100 dense candidates using Reciprocal Rank Fusion (k=60), returning top-5 passages without reranking [13].\n"
        "• S5 (Hybrid + Cross-Encoder Reranker): Initial hybrid pool of 25 candidates reranked via BAAI/bge-reranker-base, truncated to top-5 [14].\n"
        "• S5_Ctrl (Fair Pool-50 Single-Pass Control): Initial hybrid pool expanded to 50 candidates, reranked by the cross-encoder to top-5. This provides an exact capacity control for the two-hop pipeline, ensuring identical candidate search budgets (50 total candidates).\n"
        "• Ctrl_SinglePass_K10 (Context Budget Control): Unreranked hybrid retrieval fed directly to the reader at context budget K=10, evaluating whether expanding the reader's passage budget substitutes for neural reranking.\n"
        "• S7 (Dense Iterative Hop-2): Two-hop iterative retrieval using dense search alone. Hop 1 retrieves top-2 passages; Hop 2 queries the question concatenated with the first 200 characters of the Hop 1 text.\n"
        "• S8 (Staged Multi-Hop Pipeline): Our full reference staged architecture. Hop 1 retrieves 25 hybrid candidates. The top-2 passages (truncated to 200 characters) are appended to the query for Hop 2 (retrieving 25 candidates). The combined 50-candidate pool is deduplicated, reranked by the cross-encoder, and truncated to top-5.\n"
        "• S9 (Oracle Ceiling): Provides the generator with the ground-truth gold supporting passages, establishing the upper performance bound under perfect retrieval.\n"
        "• Abl_No_Reranker: Full S8 two-hop pipeline but bypassing the cross-encoder reranker, relying solely on RRF merge scores for top-5 truncation.\n"
        "• Abl_BM25_Only: Full S8 pipeline omitting dense retrieval (BM25 search alone across both hops, followed by cross-encoder reranking).\n"
        "• Abl_Dense_Only: Full S8 pipeline omitting BM25 retrieval (Dense search alone across both hops, followed by cross-encoder reranking)."
    )

    add_image_box("system_architecture_diagram.png", "Figure 1. Architectural blueprint of the multi-stage staged RAG pipeline (S8) across dual-hop retrieval, cross-encoder reranking, and dual reader parameter scaling.", width_inches=3.3)

    add_sec_heading("3.3 Evaluation Metrics and Generation Protocol", level=2)
    add_p(
        "Retrieval quality is measured across three primary dimensions at cut-off K=5: (i) Supporting Fact Recall (SF Recall@5), measuring the percentage "
        "of ground-truth facts retrieved; (ii) All Supporting Facts Recall (AllSF@5), a binary metric indicating whether all necessary gold supporting "
        "passages are simultaneously present in the top-K context; and (iii) Mean Reciprocal Rank (MRR) of the first retrieved gold passage."
    )
    add_p(
        "Downstream question answering is evaluated using standard Exact Match (EM) binary accuracy after regex surface normalization (lowercasing, punctuation, "
        "and article removal) and macro-averaged token-level F1 score. Generation is performed under greedy decoding (do_sample=False, temperature=0.0, "
        "max_new_tokens=32) using Qwen2.5-3B-Instruct [18] as our default reader, and Qwen2.5-7B-Instruct for our parameter scaling diagnostic. "
        "The reader prompt follows standard instruction formatting:\n"
        "'Answer the question concisely based only on the provided documents. Answer with just the entity name, number, or yes/no.\n\nDocuments:\n[Context]\n\nQuestion: [Query]\nAnswer:'"
    )

    add_sec_heading("3.4 Statistical Testing Protocol", level=2)
    add_p(
        "We evaluate comparisons using two complementary non-parametric testing frameworks: "
        "(1) Paired bootstrap resampling with B=10,000 resamples [15] to estimate empirical percentile 95% confidence intervals and empirical p-values for AllSF "
        "and F1 differences; and (2) Continuity-corrected McNemar's test on binary 0/1 Exact Match outcomes [17]. For all test families, we enforce "
        "family-wise error rate control at alpha=0.05 using the Holm-Bonferroni step-down adjustment [16]."
    )

    # 4. RESULTS
    add_sec_heading("4. Experimental Results and Diagnostics", level=1)
    add_p(
        "We present our empirical findings across nine subsections, tracking the performance of the pipeline from global error budgets down to manual failure categorizations."
    )

    # 4.1 ERROR BUDGET
    add_sec_heading("4.1 Stage-Wise Error Budget Decomposition (Table 1)", level=2)
    add_p(
        "We begin with the central diagnostic question: how much of downstream failure is genuinely caused by retrieval misses versus generator limitations? "
        "Table 1 decomposes the performance gap between zero and 100% into retrieval loss (Oracle Ceiling minus S8 Pipeline) and reader/metric loss "
        "(100% minus Oracle Ceiling)."
    )
    add_caption("Table 1. Stage-wise error budget decomposition of downstream performance deficits (N=500 questions).")

    t1_data = [
        ["Metric & Component", "3B Reader", "7B Reader", "Diagnostic Share"],
        ["EM: Retrieval Loss", "13.20 pp", "8.20 pp", "Imperfect retrieval deficit"],
        ["EM: Reader/Metric Loss", "47.00 pp", "39.80 pp", "Loss under perfect gold passages"],
        ["Retrieval Share (EM)", "21.9%", "17.1%", ">78% deficit is reader-bound"],
        ["F1: Retrieval Loss", "15.66 pp", "10.78 pp", "Distractor token overlap loss"],
        ["F1: Reader/Metric Loss", "33.20 pp", "24.90 pp", "Token overlap loss under gold"],
        ["Retrieval Share (F1)", "32.0%", "30.2%", "~70% deficit is reader-bound"]
    ]
    t1 = doc.add_table(rows=len(t1_data), cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1)
    for r_idx, row in enumerate(t1.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t1_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [3, 6]:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Retrieval share = Retrieval Loss / (Retrieval Loss + Reader Loss). Note that 'Retrieval loss' compares 2 clean oracle passages against 5 retrieved passages, mixing missing evidence with distractor noise.")

    add_p(
        "Under the 3B reader, the retrieval-induced Exact Match deficit is 13.20 pp, while the reader and metric deficit is 47.00 pp. "
        "Thus, retrieval errors account for only 21.9% of the total downstream EM deficit. More tellingly, when switching to the 7B reader, "
        "the retrieval-induced deficit contracts from 13.20 pp to 8.20 pp (a 37.9% reduction in retrieval penalty), even though both readers "
        "received the exact same retrieved passages. This reveals a critical reader-retriever interaction: stronger generators possess superior "
        "noise-filtering capabilities, demonstrating that retrieval quality becomes progressively less of a limiting bottleneck as generator "
        "reasoning capacity increases [18]."
    )

    # 4.2 OVERALL PIPELINE BENCHMARK
    add_sec_heading("4.2 End-to-End Pipeline Performance (Table 2 & Figure 2)", level=2)
    add_p(
        "Table 2 reports overall retrieval and downstream generation performance across the primary pipeline architectures and controlled baselines."
    )
    add_caption("Table 2. Multi-stage retrieval and downstream generation evaluation on HotpotQA (N=500, Context K=5, Qwen2.5-3B).")

    t2_data = [
        ["System Configuration", "K", "AllSF@K", "SF Rec", "MRR", "EM (%)", "F1 (%)"],
        ["S0: Closed-Book Floor", "0", "0.00%", "0.00%", "0.00", "13.60%", "17.86%"],
        ["S1: BM25 Okapi", "5", "46.80%", "70.20%", "0.84", "30.80%", "40.36%"],
        ["S2: Dense BGE-Small", "5", "70.60%", "84.40%", "0.93", "36.80%", "47.11%"],
        ["S3: Hybrid RRF Fusion", "5", "67.20%", "82.50%", "0.90", "33.60%", "43.88%"],
        ["S5: Hybrid + Reranker", "5", "82.60%", "91.00%", "0.97", "38.80%", "49.15%"],
        ["S5_Ctrl: Fair Pool-50", "5", "82.80%", "91.20%", "0.97", "38.80%", "49.31%"],
        ["Ctrl_SinglePass_K10", "10", "81.00%*", "90.10%", "0.90", "38.60%", "48.44%"],
        ["S7: Dense Iterative", "5", "72.80%", "84.90%", "0.93", "37.60%", "49.20%"],
        ["S8: Staged Pipeline", "5", "85.60%", "92.60%", "0.97", "39.80%", "51.14%"],
        ["S9: Oracle Ceiling", "Gold", "100.0%", "100.0%", "1.00", "53.00%", "66.80%"]
    ]
    t2 = doc.add_table(rows=len(t2_data), cols=7)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2)
    for r_idx, row in enumerate(t2.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t2_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 9:
            format_row(row, bg_hex="EBF3FB", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in range(1, 7): row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in range(1, 7): row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("*Note on Ctrl_SinglePass_K10: AllSF evaluated at K=10. S8 achieves the highest EM among primary multi-stage configurations (39.80%).")

    add_image_box("fig1_ablation_barplot.png", "Figure 2. AllSF@5 retrieval coverage across ablation configurations (untruncated 0-100% axis).", width_inches=3.3)

    add_p(
        "Across primary configurations, S8 establishes the highest AllSF@5 (85.60%), MRR (0.97), and Exact Match (39.80%). "
        "Across the eight retrieval systems in Table 2, AllSF and EM correlate strongly at r ≈ 0.97. However, the gains show clear diminishing returns: "
        "moving from BM25 (46.80% AllSF) to Dense (70.60% AllSF) increases EM by +6.00 pp. Beyond 70% AllSF, further retrieval gains yield much smaller downstream "
        "increases: adding +15.00 pp AllSF from Dense to S8 produces only +3.00 pp in EM."
    )
    add_p(
        "Second, consider Ctrl_SinglePass_K10. By simply providing the generator with ten unreranked hybrid passages (K=10) instead of five reranked passages, "
        "the reader reaches 38.60% EM—virtually identical to the 38.80% achieved by neural reranking at K=5. Allocating a broader context "
        "budget to the reader circumvents the need for neural cross-encoder reranking on this corpus size."
    )

    # 4.3 MARGINAL GAINS
    add_sec_heading("4.3 Marginal Gains of S8 over Baselines (Table 3)", level=2)
    add_p(
        "Table 3 isolates the marginal net gains (Δ pp) of the full staged pipeline over each individual baseline."
    )
    add_caption("Table 3. Marginal point gains (Δ pp) of S8 over baseline systems with paired McNemar significance status.")

    t3_data = [
        ["Baseline System", "Base AllSF", "S8 AllSF", "Δ AllSF", "Base EM", "S8 EM", "Δ EM", "McNemar Sig."],
        ["vs. S1 (BM25)", "46.80%", "85.60%", "+38.80 pp", "30.80%", "39.80%", "+9.00 pp", "Not tested m=6"],
        ["vs. S2 (Dense)", "70.60%", "85.60%", "+15.00 pp", "36.80%", "39.80%", "+3.00 pp", "p = 0.516 (NS)"],
        ["vs. S3 (Hybrid)", "67.20%", "85.60%", "+18.40 pp", "33.60%", "39.80%", "+6.20 pp", "p = 0.0059 (Sig)"],
        ["vs. S5 (Rerank)", "82.60%", "85.60%", "+3.00 pp", "38.80%", "39.80%", "+1.00 pp", "p = 0.851 (NS)"],
        ["vs. S5_Ctrl", "82.80%", "85.60%", "+2.80 pp", "38.80%", "39.80%", "+1.00 pp", "p = 0.851 (NS)"],
        ["vs. S7 (Dense-2)", "72.80%", "85.60%", "+12.80 pp", "37.60%", "39.80%", "+2.20 pp", "p = 0.851 (NS)"]
    ]
    t3 = doc.add_table(rows=len(t3_data), cols=8)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3)
    for r_idx, row in enumerate(t3.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t3_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in range(1, 7): row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: McNemar p-values are continuity-corrected and adjusted under the m=6 Holm family. Note that non-significant results reflect low statistical power on modest discordant counts (15–23 pairs) rather than confirmed zero effect.")

    add_p(
        "S8 improves AllSF@5 by +15.00 pp over dense retrieval S2, yet downstream Exact Match improves by only +3.00 pp (from 36.80% to 39.80%). "
        "With 50 wins versus 35 losses (85 discordant pairs), this difference yields p_holm = 0.5156. We emphasize that a non-significant test does not "
        "prove the absence of an effect; rather, given the modest sample size (N=500) and small discordant margin, the study is underpowered to detect small "
        "single-digit downstream EM differences."
    )

    # 4.4 COMPONENT ABLATION
    add_sec_heading("4.4 Leave-One-Out Component Ablation on S8 (Table 4)", level=2)
    add_p(
        "To determine which architectural components justify their computational overhead, we performed a leave-one-out ablation on S8 (Table 4)."
    )
    add_caption("Table 4. Leave-one-out component ablation analysis on the staged multi-hop pipeline (S8 reference).")

    t4_data = [
        ["Ablation Variant", "Component Removed", "AllSF@5", "Δ AllSF", "F1 Score", "Δ F1", "EM (%)"],
        ["S8 Staged Reference", "None (Full Pipeline)", "85.60%", "—", "51.14%", "—", "39.80%"],
        ["Abl_No_Reranker", "Minus Cross-Encoder Reranker", "63.00%", "-22.60 pp", "45.82%", "-5.32 pp", "35.80%"],
        ["S5_Ctrl_Pool50", "Minus Hop 2 (Single-Pass)", "82.80%", "-2.80 pp", "49.31%", "-1.83 pp", "38.80%"],
        ["Abl_BM25_Only", "Minus Dense (BM25 only)", "80.40%", "-5.20 pp", "51.39%", "+0.25 pp", "40.40%"],
        ["Abl_Dense_Only", "Minus BM25 (Dense only)", "85.60%", "0.00 pp", "51.38%", "+0.24 pp", "40.00%"]
    ]
    t4 = doc.add_table(rows=len(t4_data), cols=7)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4)
    for r_idx, row in enumerate(t4.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t4_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 1:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4, 5, 6]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Reference S8 performance is 85.60% AllSF@5, 51.14% F1, and 39.80% EM. Negative Δ indicates degradation upon removal.")

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

    # 4.5 PAIRED BOOTSTRAP SIGNIFICANCE (FULL-WIDTH SECTION FOR WIDE TABLES 5 & 6)
    sec_wide = doc.add_section(WD_SECTION.CONTINUOUS)
    sec_wide._sectPr.append(parse_xml(f'<w:cols {nsdecls("w")} w:num="1"/>'))

    add_sec_heading("4.5 Paired Bootstrap Resampling Significance Analysis (Table 5)", level=2)
    add_p(
        "To evaluate whether the observed point differences reflect genuine distributional separation, we executed paired bootstrap resampling (B=10,000 resamples) [15]. "
        "Table 5 presents the empirical percentile 95% confidence intervals and Holm-adjusted p-values across two families: Primary Retrieval Coverage (AllSF@5, m=8) "
        "and Downstream Token Overlap (F1, m=5)."
    )
    add_caption("Table 5. Paired bootstrap hypothesis testing on S8 vs. alternative configurations (B=10,000, 95% CI, Holm-Bonferroni family-wise error control).")

    t5_data = [
        ["Comparison Pair", "Metric", "S8", "Base", "Δ Mean", "95% Bootstrap CI", "Raw p", "Holm p", "Sig."],
        ["Family 1: Primary Retrieval Coverage (AllSF@5, m=8 tests; Raw p < 0.0001 represents bootstrap floor)", "", "", "", "", "", "", "", ""],
        ["S8 vs S2_Dense", "AllSF", "85.6%", "70.6%", "+15.0%", "[+11.2, +19.0]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs S3_Hybrid", "AllSF", "85.6%", "67.2%", "+18.4%", "[+14.6, +22.2]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs S5_Hybrid_Rerank", "AllSF", "85.6%", "82.6%", "+3.0%", "[+1.4, +4.8]", "0.0004", "0.0028", "Yes"],
        ["S8 vs S7_Iterative_Dense", "AllSF", "85.6%", "72.8%", "+12.8%", "[+8.6, +17.0]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs Abl_No_Reranker", "AllSF", "85.6%", "63.0%", "+22.6%", "[+18.6, +26.8]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs Abl_BM25_Only", "AllSF", "85.6%", "80.4%", "+5.2%", "[+3.0, +7.4]", "< 0.0001", "0.0008", "Yes"],
        ["S8 vs S5_Ctrl_Pool50", "AllSF", "85.6%", "82.8%", "+2.8%", "[+0.4, +5.2]", "0.0240", "0.0480", "Borderline"],
        ["S8 vs Abl_Dense_Only", "AllSF", "85.6%", "85.6%", "0.0%", "[-2.0, +2.0]", "1.0000", "1.0000", "No"],
        ["Family 2: Downstream Token Overlap (F1 Score, m=5 tests)", "", "", "", "", "", "", "", ""],
        ["S8 vs S3_Hybrid", "F1", "51.1%", "43.9%", "+7.3%", "[+3.8, +10.7]", "< 0.0001", "0.0005", "Yes"],
        ["S8 vs Abl_No_Reranker", "F1", "51.1%", "45.8%", "+5.3%", "[+1.8, +8.9]", "0.0024", "0.0096", "Yes"],
        ["S8 vs S5_Hybrid_Rerank", "F1", "51.1%", "49.2%", "+2.0%", "[+0.5, +3.6]", "0.0070", "0.0210", "Yes"],
        ["S8 vs S2_Dense", "F1", "51.1%", "47.1%", "+4.0%", "[+0.5, +7.6]", "0.0280", "0.0560", "No"],
        ["S8 vs S5_Ctrl_Pool50", "F1", "51.1%", "49.3%", "+1.8%", "[-0.1, +3.8]", "0.0594", "0.0594", "No"]
    ]
    t5 = doc.add_table(rows=len(t5_data), cols=9)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t5)
    for r_idx, row in enumerate(t5.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t5_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [1, 10]:
            format_row(row, bg_hex="E6EDF5", bold=True, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
            a, b = row.cells[0], row.cells[8]
            a.merge(b)
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: Confidence intervals derived from empirical percentiles [2.5%, 97.5%]. Raw p < 0.0001 represents the bootstrap floor 1/(B+1).")

    add_p(
        "In Family 1 (AllSF@5), S8 demonstrates statistically significant retrieval superiority over unreranked baselines (S2, S3, S7) and Abl_No_Reranker "
        "(all p_holm = 0.0008). Against the fair Pool-50 single-pass control (S5_Ctrl), S8 achieves a small retrieval gain (+2.80 pp, 95% CI [+0.40, +5.20]). "
        "In Family 2 (F1 score), S8's token-overlap improvements over single-pass dense retrieval S2 (+4.03 pp, p_holm = 0.0560) and fair "
        "single-pass control S5_Ctrl (+1.83 pp, 95% CI [-0.08, +3.82], p_holm = 0.0594) both fail to achieve statistical significance."
    )

    # 4.6 MCNEMAR TEST
    add_sec_heading("4.6 Confirmation via McNemar's Non-Parametric Paired Test (Table 6)", level=2)
    add_p(
        "Because Exact Match is a binary 0/1 variable, paired t-tests can yield misleading inferences [17]. Table 6 reports continuity-corrected "
        "McNemar tests across all six EM comparison pairs, ordered by rank and corrected via Holm step-down [16]."
    )
    add_caption("Table 6. McNemar's paired test on Exact Match (m=6 comparisons, continuity-corrected χ², Holm step-down).")

    t6_data = [
        ["Rank (i)", "Comparison Pair", "S8 Win", "Other Win", "χ²", "Raw p", "Multiplier", "Holm p", "Significance"],
        ["1", "S8 vs S3_Hybrid", "57", "26", "10.84", "0.00099", "× 6", "0.0059", "Statistically Significant"],
        ["2", "S8 vs Abl_No_Reranker", "49", "29", "4.63", "0.0315", "× 5", "0.1575", "Not Significant"],
        ["3", "S8 vs S2_Dense", "50", "35", "2.31", "0.1289", "× 4", "0.5156", "Not Significant"],
        ["4", "S8 vs S7_Iterative_Dense", "49", "38", "1.15", "0.2837", "× 3", "0.8511", "Not Significant"],
        ["5", "S8 vs S5_Hybrid_Rerank", "10", "5", "1.07", "0.3017", "× 2", "0.8511", "Not Significant"],
        ["6", "S8 vs S5_Ctrl_Pool50", "14", "9", "0.70", "0.4042", "× 1", "0.8511", "Not Significant"]
    ]
    t6 = doc.add_table(rows=len(t6_data), cols=9)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t6)
    for r_idx, row in enumerate(t6.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t6_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=8, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 1:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            for c in [2, 3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            format_row(row, bg_hex=None, bold=False, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            for c in [2, 3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[8].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: Continuity correction (|b - c| - 1)^2 / (b + c) applied to discordant pairs. Multipliers enforce step-down Holm correction.")

    add_p(
        "Across all six binary EM comparisons, S8 achieves a statistically significant accuracy gain solely against unreranked hybrid retrieval S3 "
        "(57 wins vs 26 losses, chi2=10.84, p_holm = 0.0059). Against Abl_No_Reranker, S8's raw p-value of 0.0315 is adjusted by the Holm multiplier "
        "to p_holm = 0.1575. Against dense retrieval S2, S8 produces 50 wins and 35 losses, yielding p_holm = 0.5156. Finally, against fair single-pass "
        "control S5_Ctrl, S8 produces 14 wins against 9 losses (a net advantage of 5 questions out of 500), yielding chi2=0.70 and p_holm = 0.8511."
    )

    # SWITCH BACK TO TWO COLUMNS FOR 4.7 ONWARDS
    sec_twocol2 = doc.add_section(WD_SECTION.CONTINUOUS)
    sec_twocol2._sectPr.append(parse_xml(f'<w:cols {nsdecls("w")} w:num="2" w:space="720"/>'))

    # 4.7 DEPTH CURVES
    add_sec_heading("4.7 Multi-Retriever Depth Curves across K ∈ {5, 10, 25, 50} (Table 7 & Figure 3)", level=2)
    add_p(
        "To evaluate whether retrieval saturation occurs at deeper ranks, we analyze AllSF recall across depths K in {5, 10, 25, 50}, broken down "
        "by question type: Bridge (N=404) vs. Comparison (N=96) (Table 7)."
    )
    add_caption("Table 7. Supporting facts recall curves across retrieval depths on the 19,260-passage corpus.")

    t7_data = [
        ["Retriever", "Subgroup", "K=5", "K=10", "K=25", "K=50", "Saturation Behavior"],
        ["BM25 Sparse", "Bridge (N=404)", "44.06%", "60.64%", "72.28%", "77.72%", "Missing lexical bridge tokens"],
        ["BM25 Sparse", "Comparison (N=96)", "58.33%", "75.00%", "88.54%", "94.79%", "High saturation at K=50"],
        ["Dense BGE", "Bridge (N=404)", "63.86%", "74.50%", "82.67%", "88.37%", "Beats Hybrid at K=5"],
        ["Dense BGE", "Comparison (N=96)", "98.96%", "100.0%", "100.0%", "100.0%", "Ceiling reached at K=10"],
        ["Hybrid RRF", "Bridge (N=404)", "61.14%", "76.73%", "84.65%", "88.12%", "Underperforms Dense at K=5"],
        ["Hybrid RRF", "Comparison (N=96)", "97.92%", "100.0%", "100.0%", "100.0%", "Ceiling reached at K=10"]
    ]
    t7 = doc.add_table(rows=len(t7_data), cols=7)
    t7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t7)
    for r_idx, row in enumerate(t7.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t7_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4, 5]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Evaluated on partitioned subsets. Weighted average across subgroups matches Table 2 within 1.0 pp due to RRF score tie-breaking differences between subgroup runs and the combined pool.")

    add_image_box("fig3_depth_latency_tradeoff.png", "Figure 3. Candidate depth recall trajectory for unreranked hybrid retrieval across K ∈ {5, 10, 25, 50}.", width_inches=3.3)

    add_p(
        "Table 7 reveals sharp behavioral divergences between query types. Comparison questions are straightforward for dense representations: Dense BGE-Small "
        "retrieves all supporting facts for 98.96% of comparison questions at K=5, and reaches 100.00% at K=10. This occurs because comparison "
        "questions explicitly name both entities in the prompt, allowing single-pass dense search to match both simultaneously [4]."
    )
    add_p(
        "Bridge questions, by contrast, exhibit a severe lexical bottleneck. BM25 reaches only 44.06% AllSF@5 on Bridge questions because the second fact's "
        "entity is unmentioned in the original prompt. Furthermore, Hybrid RRF underperforms Dense retrieval on Bridge questions at K=5 (61.14% vs 63.86%), "
        "as lexical fusion introduces keyword-heavy distractors."
    )

    # 4.8 EVIDENCE RECOVERY FUNNEL & 2x2
    add_sec_heading("4.8 Evidence Recovery Funnel and Paired 2×2 Contingency (Table 8 & Figure 4)", level=2)
    add_p(
        "Where does the second supporting fact actually get captured? Table 8 tracks the evidence discovery funnel across the 500 questions, "
        "accompanied by the paired 2×2 contingency matrix against the fair single-pass control S5_Ctrl (Figure 4)."
    )
    add_caption("Table 8. Multi-hop evidence recovery funnel across N=500 benchmark questions.")

    t8_data = [
        ["Evidence Discovery Stage", "Count", "Share (%)", "Stage Meaning & Bottleneck Mechanism"],
        ["Hop 1 Pool Capture", "438 / 500", "87.60%", "Both gold facts discoverable in initial 25 hybrid pool"],
        ["Hop 2 Rescued Evidence", "32 / 500", "6.40%", "Fact 2 missing in Hop 1 pool; surfaced by iterative query"],
        ["Total Pool Capture", "470 / 500", "94.00%", "Upper evidence ceiling captured across both pools"],
        ["Top-5 Truncation Loss", "42 / 500", "8.40%", "Lost during cross-encoder truncation (470 → 428)"],
        ["Never Retrieved Floor", "30 / 500", "6.00%", "Neither hop retrieved both facts from corpus"],
        ["Final S8 Top-5 Coverage", "428 / 500", "85.60%", "Final context fed to reader containing all facts"]
    ]
    t8 = doc.add_table(rows=len(t8_data), cols=4)
    t8.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t8)
    for r_idx, row in enumerate(t8.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t8_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [3, 6]:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Sum of Hop 1 (438) + Hop 2 Rescued (32) = 470 pool capture. Truncation loss drops pool to 428 final hits.")

    add_image_box("fig2_paired_contingency_matrix.png", "Figure 4. Paired 2×2 evidence contingency matrix between S8 Staged and S5_Ctrl Pool-50 on AllSF@5.", width_inches=3.3)

    add_p(
        "To inspect the exact paired behavior of Hop-2 retrieval, consider the 2×2 contingency matrix against S5_Ctrl Pool-50 (Figure 4):\n"
        "• Both Hit (S8=1, Ctrl=1): 402 questions (80.40%)\n"
        "• S8 Pipeline Win (S8=1, Ctrl=0): 26 questions (5.20%)\n"
        "• S5_Ctrl Control Win (S8=0, Ctrl=1): 12 questions (2.40%)\n"
        "• Neither Hit (S8=0, Ctrl=0): 60 questions (12.00%)\n"
        "Total Hits: S8 = 402 + 26 = 428 (85.60%); S5_Ctrl = 402 + 12 = 414 (82.80%)."
    )
    add_p(
        "This paired breakdown shows that while S8 gains 26 questions where Hop 2 successfully surfaced Fact 2, it simultaneously degrades 12 questions "
        "that S5_Ctrl captured cleanly. In those 12 cases, the iterative query introduced irrelevant distractor passages that displaced gold facts during reranking. "
        "The net paired gain is exactly 26 − 12 = +14 questions (+2.80 pp)."
    )

    # 4.9 GENERATOR CAPACITY DIAGNOSTIC
    add_sec_heading("4.9 Generator Capacity Diagnostic: 3B vs. 7B Parameter Scaling (Table 9 & Figure 5)", level=2)
    add_p(
        "To test whether downstream accuracy is constrained by retrieved evidence or reader reasoning capacity, we scaled the generator from Qwen2.5-3B "
        "to Qwen2.5-7B [18], evaluating both models on identical retrieved contexts (Table 9)."
    )
    add_caption("Table 9. Generator capacity diagnostic: Paired comparison of 3B vs. 7B reader scaling on identical contexts.")

    t9_data = [
        ["Comparison Pair", "Evidence Fed", "Metric", "3B Score", "7B Score", "Net Gain", "95% Bootstrap CI", "Holm p"],
        ["S8_7B vs S8_3B", "S8 Retrieved Passages", "EM", "39.80%", "52.00%", "+12.20 pp", "[+8.20, +16.20]", "0.0004 (Yes)"],
        ["S8_7B vs S8_3B", "S8 Retrieved Passages", "F1", "51.14%", "64.32%", "+13.18 pp", "[+9.64, +16.80]", "0.0004 (Yes)"],
        ["S9_7B vs S9_3B", "Gold Oracle Passages", "EM", "53.00%", "60.20%", "+7.20 pp", "[+3.60, +10.80]", "0.0004 (Yes)"],
        ["S9_7B vs S9_3B", "Gold Oracle Passages", "F1", "66.80%", "75.10%", "+8.30 pp", "[+5.13, +11.55]", "0.0004 (Yes)"]
    ]
    t9 = doc.add_table(rows=len(t9_data), cols=8)
    t9.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t9)
    for r_idx, row in enumerate(t9.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t9_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 1:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [3, 4, 5, 6, 7]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Evaluated across N=500 questions. Both 3B and 7B models evaluated on identical retrieved passage lists.")

    add_image_box("fig4_noise_decay_curves.png", "Figure 5. Downstream Exact Match and F1 score scaling across 3B and 7B reader generators.", width_inches=3.3)

    add_p(
        "Table 9 presents the most substantial performance change in this study. When evaluated on the exact same retrieved evidence from S8, scaling the reader "
        "from 3B to 7B increases Exact Match by +12.20 pp (from 39.80% to 52.00%, p_holm = 0.0004) and F1 by +13.18 pp (from 51.14% to 64.32%). "
        "On identical evidence, the 7B reader reaches 52.00% EM, comparable to the 3B reader's gold-evidence score of 53.00% EM."
    )
    add_p(
        "We note an important caveat: part of this +12.20 pp increase may stem from superior adherence to concise formatting instructions rather than pure multi-hop "
        "reasoning. As detailed in our error analysis, 36.70% of 3B errors are surface-form artifacts; larger models often follow output constraints more reliably, "
        "partially mitigating formatting penalties."
    )

    # 4.10 COMPUTATIONAL LATENCY
    add_sec_heading("4.10 Computational Latency Profiling (Table 10)", level=2)
    add_p(
        "Table 10 benchmarks the runtime latency and throughput of each retrieval stack module on dual NVIDIA Tesla T4 GPUs (measured across 30 queries after 5 warm-up queries)."
    )
    add_caption("Table 10. Computational latency and throughput profiling of retrieval modules on dual NVIDIA Tesla T4 GPUs.")

    t10_data = [
        ["Retrieval Stage Module", "Underlying Technology", "Mean Latency", "Throughput", "Stack Share"],
        ["Dense Embedding Search", "BAAI/bge-small-en-v1.5 + Dot Product", "0.0139 s", "71.9 qps", "2.1%"],
        ["BM25 Sparse Retrieval", "RankBM25 Okapi (Inverted Index)", "0.0724 s", "13.8 qps", "11.0%"],
        ["Hybrid RRF Fusion", "Reciprocal Rank Fusion (k=60)", "0.1169 s", "8.5 qps", "17.8%"],
        ["Cross-Encoder Reranker", "BAAI/bge-reranker-base (max_len=256)", "0.4560 s", "2.2 qps", "69.1% (Dominant)"]
    ]
    t10 = doc.add_table(rows=len(t10_data), cols=5)
    t10.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t10)
    for r_idx, row in enumerate(t10.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t10_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx == 4:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            for c in [2, 3, 4]: row.cells[c].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_table_note("Note: Profiles retrieval stack exclusively. Reader generation adds ~0.45 s/query for 3B and ~0.91 s/query for 7B.")

    add_p(
        "Cross-encoder reranking accounts for 69.1% of total retrieval latency (0.4560 seconds per query, achieving 2.2 qps), representing a 33× latency penalty "
        "relative to dense vector search (0.0139 s, 71.9 qps). While the reranker delivers substantial recall (+15.40 pp AllSF@5), its quadratic token-level "
        "attention imposes significant computational costs [14]. Reader generation adds an additional ~0.45 s for 3B and ~0.91 s for 7B."
    )

    # 4.11 QUALITATIVE ERROR ANALYSIS
    add_sec_heading("4.11 Qualitative Error Analysis (Table 11 & Figure 6)", level=2)
    add_p(
        "To examine why downstream generation stalls even when supporting facts are retrieved, we conducted a manual audit of 60 randomly "
        "sampled failure cases from S8 (Table 11), computing Wilson score 95% confidence intervals [22]."
    )
    add_caption("Table 11. Hand-verified qualitative error breakdown across N=60 randomly sampled S8 failure cases.")

    t11_data = [
        ["Failure Category Tag", "Freq.", "Share (%)", "Wilson 95% CI", "Primary Failure Mechanism"],
        ["Format / Metric Artifact", "22 / 60", "36.70%", "[25.5%, 49.3%]", "Semantically correct entity penalized by exact match string formatting"],
        ["Reasoning Failure under Evidence", "19 / 60", "31.70%", "[21.2%, 44.2%]", "Gold evidence in prompt; 3B model fails logical constraint deduction"],
        ["Retrieval Gap (Missing Fact 2)", "13 / 60", "21.70%", "[13.1%, 33.6%]", "Hop 1 retrieved Fact 1, but Hop 2 query failed to bridge to Fact 2"],
        ["Span Extraction Error", "6 / 60", "10.00%", "[4.7%, 20.1%]", "Both facts retrieved; generator extracted adjacent distractor entity"]
    ]
    t11 = doc.add_table(rows=len(t11_data), cols=5)
    t11.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t11)
    for r_idx, row in enumerate(t11.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t11_data[r_idx][c_idx]
        if r_idx == 0:
            format_row(row, bg_hex="003366", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_hex="FFFFFF")
        elif r_idx in [1, 2]:
            format_row(row, bg_hex="F0F4F8", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            format_row(row, bg_hex=None, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
            row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_table_note("Note: Evaluated under single-annotator blind verification. Categories are mutually exclusive and sum to 100%.")

    add_image_box("fig5_evidence_discovery_curves.png", "Figure 6. Supporting facts recall depth curves across Bridge (N=404) and Comparison (N=96) subgroups.", width_inches=3.3)

    add_p(
        "Over a third of sampled failures (36.70%, Wilson CI [25.5%, 49.3%]) are format artifacts: the generator produced the semantically correct entity, "
        "but was penalized by string mismatch (e.g., answering 'US' instead of 'United States', or omitting parenthetical qualifiers). When combined with "
        "Reasoning Failures (31.70%), where the 3B model failed multi-hop logical deduction despite having gold passages in its prompt, we find that 68.4% of "
        "failures occur on the reader side. Actual retrieval failures (Missing Fact 2) account for 21.70% of errors."
    )

    # 5. DISCUSSION
    add_sec_heading("5. Discussion", level=1)
    add_p(
        "Synthesizing these empirical analyses reveals that retrieval coverage and downstream answer accuracy exhibit pronounced diminishing returns. "
        "While AllSF and EM correlate strongly across baselines (r ≈ 0.97), gains beyond 70% AllSF yield sharply compressed downstream benefits [8, 10]."
    )
    add_p(
        "Throughout our experiments, neural cross-encoder reranking consistently emerges as the dominant retrieval lever, contributing +15.40 pp in AllSF@5. "
        "Iterative second-hop retrieval contributes an incremental +2.80 pp AllSF gain over fair single-pass controls, which fails to produce a statistically detectable "
        "improvement in downstream Exact Match (p_holm = 0.8511). As demonstrated in our 2×2 contingency analysis, the 26 questions gained by Hop 2 are partially "
        "counterbalanced by 12 questions degraded by query noise."
    )
    add_p(
        "Meanwhile, generator parameterization exerts an overwhelming influence. Scaling from a 3B to a 7B reader model on identical retrieved passages produces "
        "a +12.20 pp jump in Exact Match. Coupled with our error breakdown showing that 36.70% of failures are string-matching artifacts, we conclude that future "
        "research in multi-hop QA should focus on reader reasoning capabilities, context distillation, and metric normalization rather than engineering increasingly "
        "intricate retrieval loops [23]."
    )

    # 6. LIMITATIONS
    add_sec_heading("6. Limitations", level=1)
    add_p(
        "We note several concrete methodological limitations of this study:\n"
        "1. Corpus Construction: Our evaluation index comprises 19,260 passages constructed by pooling gold and distractor paragraphs from the HotpotQA development set [4]. "
        "While challenging due to dense distractor competition, this corpus is substantially smaller than full 5-million-page Wikipedia dumps, where retrieval "
        "dilution may follow different scaling dynamics.\n"
        "2. Subgroup Sample Size: All evaluations were conducted on a single fixed subset of 500 questions (N=500). While sufficient to power paired testing across "
        "the full set, the 96 comparison questions represent a relatively small sample, meaning subtle subgroup differences may be underpowered.\n"
        "3. Generator Architecture: Experiments were restricted to the Qwen2.5 open-weights series (3B and 7B) [18]. While representative of modern dense instruct models, "
        "we cannot entirely rule out potential pre-training exposure to HotpotQA text.\n"
        "4. Single-Annotator Error Audit: Our qualitative analysis of 60 failure cases was hand-verified by a single annotator; consequently, inter-annotator agreement "
        "(e.g., Cohen's kappa) could not be calculated.\n"
        "5. Metric Constraints: We adhered to standard HotpotQA Exact Match and token F1 metrics. Evaluating alias-aware or model-based semantic evaluation metrics was beyond "
        "the scope of this study."
    )

    # 7. CONCLUSION
    add_sec_heading("7. Conclusion", level=1)
    add_p(
        "In this empirical diagnostic study, we investigated the stage-wise mechanisms governing multi-hop RAG systems on HotpotQA. Through thirteen controlled system "
        "evaluations, paired bootstrap resampling, Holm-corrected McNemar tests, and manual error audits, we showed that the performance bottleneck in multi-hop QA "
        "is not retrieval recall. Cross-encoder reranking accounts for virtually all meaningful retrieval improvements, while iterative second-hop query augmentation "
        "delivers modest gains that fail to reach downstream answer accuracy. Over 78% of the downstream performance deficit originates on the generator "
        "and metric side, where reader parameter scaling provides four times the benefit of retrieval pipeline optimization. For practitioners and researchers, "
        "these results suggest that efforts to improve multi-hop QA are better spent strengthening reader reasoning and resolving surface-form metric fragility than "
        "constructing ever-more elaborate iterative retrieval pipelines."
    )

    # 8. REFERENCES
    add_sec_heading("References", level=1)
    refs = [
        "[1] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459-9474.",
        "[2] Karpukhin, V., Oguz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., & Yih, W. T. (2020). Dense passage retrieval for open-domain question answering. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), 6769-6781.",
        "[3] Shuster, K., Poff, S., Moya, D., Komeili, S., Ju, D., Xu, J., ... & Weston, J. (2021). Retrieval augmentation reduces hallucination in conversation. In Findings of the Association for Computational Linguistics: EMNLP 2021, 3784-3803.",
        "[4] Yang, Z., Qi, P., Zhang, S., Bengio, Y., Cohen, W. W., Salakhutdinov, R., & Manning, C. D. (2018). HotpotQA: A dataset for diverse, explainable multi-hop question answering. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP), 2369-2380.",
        "[5] Trivedi, H., Balasubramanian, N., Khot, T., & Sabharwal, A. (2023). Interleaving retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL), 10014-10037.",
        "[6] Khattab, O., Santhanam, K., Li, X. L., Hall, D., & Liang, P. (2023). Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP. arXiv preprint arXiv:2212.14024.",
        "[7] Asai, A., Min, S., Zhong, Z., & Yih, W. T. (2024). Self-RAG: Learning to retrieve, generate, and critique through self-reflection. In International Conference on Learning Representations (ICLR 2024).",
        "[8] Chen, J., Lin, H., Han, X., & Sun, L. (2024). Benchmarking large language models in retrieval-augmented generation. In Proceedings of the AAAI Conference on Artificial Intelligence, 38(16), 17754-17762.",
        "[9] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. Transactions of the Association for Computational Linguistics, 12, 157-173.",
        "[10] Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., ... & Wang, H. (2023). Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997.",
        "[11] Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. Foundations and Trends in Information Retrieval, 3(4), 333-389.",
        "[12] Xiao, S., Liu, Z., Zhang, P., & Muennighoff, N. (2023). C-Pack: Packaged resources to advance general Chinese embedding (BGE models). arXiv preprint arXiv:2309.07597.",
        "[13] Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009). Reciprocal rank fusion outperforms Indri and Lucene for combined search. In Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval, 758-759.",
        "[14] Nogueira, R., & Cho, K. (2019). Passage re-ranking with BERT. arXiv preprint arXiv:1901.04085.",
        "[15] Efron, B., & Tibshirani, R. J. (1993). An Introduction to the Bootstrap. Chapman & Hall/CRC Press.",
        "[16] Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics, 6(2), 65-70.",
        "[17] McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika, 12(2), 153-157.",
        "[18] Qwen Team. (2024). Qwen2.5: A party of foundation and instruction-tuned large language models. arXiv preprint arXiv:2412.15115.",
        "[19] Rajpurkar, P., Jia, R., & Liang, P. (2018). Know what you don't know: Unanswerable questions for SQuAD. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (ACL), 784-789.",
        "[20] Min, S., Wallace, E., Singh, S., Gardner, M., Hajishirzi, H., & Zettlemoyer, L. (2019). Compositional questions do not necessitate multi-hop reasoning. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL), 4249-4257.",
        "[21] Dror, R., Baumer, G., Shlomov, S., & Reichart, R. (2018). The hitchhiker's guide to testing statistical significance in natural language processing. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (ACL), 1383-1392.",
        "[22] Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association, 22(158), 209-212.",
        "[23] Mallen, A., Asai, A., Zhong, V., Das, R., Khashabi, D., & Hajishirzi, H. (2023). When not to trust language models: Investigating effectiveness of parametric and non-parametric memories. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL), 9802-9822."
    ]

    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        p_ref.paragraph_format.space_before = Pt(1.5)
        p_ref.paragraph_format.space_after = Pt(2.5)
        p_ref.paragraph_format.line_spacing = 1.02
        r_run = p_ref.add_run(r)
        r_run.font.name = 'Times New Roman'
        r_run.font.size = Pt(8)

    out_path1 = r"C:\Users\abira\OneDrive\Desktop\MultiHop-RAG-Diagnosis\RAG_Paper_TwoColumn.docx"
    doc.save(out_path1)
    print(f"Two-column research paper successfully updated at: {out_path1}")

    out_path2 = r"C:\Users\abira\OneDrive\Desktop\MultiHop-RAG-Diagnosis\TEAM 2 RESEARCH PAPER.docx"
    try:
        doc.save(out_path2)
        print(f"TEAM 2 RESEARCH PAPER successfully updated at: {out_path2}")
    except Exception as e:
        print(f"Notice: Could not write directly to {out_path2}: {e}")
        out_path2_alt = r"C:\Users\abira\OneDrive\Desktop\MultiHop-RAG-Diagnosis\TEAM_2_RESEARCH_PAPER_FINAL.docx"
        doc.save(out_path2_alt)
        print(f"Saved copy to: {out_path2_alt}")

if __name__ == "__main__":
    build_paper()
