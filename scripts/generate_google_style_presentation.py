#!/usr/bin/env python3
"""
generate_google_style_presentation.py
Generates a PowerPoint presentation (.pptx) designed to match the clean, simple,
and elegant style of the reference Google Slides presentation, featuring the team:
  - Joel Biju        (01FE24BCI021)
  - Mehak Sayed Yusuf(01FE24BCI012)
  - Akshay Bhat      (01FE24BCI024)
  - Vageesh Mathad   (01FE24BCI008)

And including the key technical enhancement (CUDA Streams & Vectorized float4)
that takes the project beyond what was previously done.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    results_dir = r"c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\results"
    output_pptx = r"c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\presentation\CUDA_GPU_Dataset_Processing_Enhanced.pptx"

    # Color Palette: Modern clean theme matching Google Slides
    BG_WHITE   = RGBColor(255, 255, 255)
    CARD_BG    = RGBColor(248, 249, 250)      # #F8F9FA
    CARD_BORDER= RGBColor(226, 232, 240)      # #E2E8F0
    TEXT_DARK  = RGBColor(30, 41, 59)         # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139)      # #64748B
    PRIMARY_BL = RGBColor(37, 99, 235)        # Google Blue #2563EB
    ACCENT_GRN = RGBColor(22, 163, 74)        # Green #16A34A
    ACCENT_RED = RGBColor(220, 38, 38)        # Red #DC2626
    ACCENT_PURP= RGBColor(126, 34, 206)       # Purple #7E22CE

    def set_white_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = BG_WHITE

    def add_slide_header(slide, title_text, slide_number):
        # Title text box
        tbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.0), Inches(0.8))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

        # Slide number indicator
        sn_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.4), Inches(0.8), Inches(0.4))
        sn_tf = sn_box.text_frame
        sn_p = sn_tf.paragraphs[0]
        sn_p.text = str(slide_number)
        sn_p.font.size = Pt(12)
        sn_p.font.color.rgb = TEXT_MUTED
        sn_p.alignment = PP_ALIGN.RIGHT

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Matches Google Slides style)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_white_bg(s1)

    tbox1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(2.2))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "PARALLEL & GPU COMPUTING (PGC-03)"
    p_badge.font.size = Pt(12)
    p_badge.font.bold = True
    p_badge.font.color.rgb = PRIMARY_BL

    p_title = tf1.add_paragraph()
    p_title.text = "GPU Dataset Processing using CUDA"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_DARK
    p_title.space_before = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Execution time, speedup, memory-transfer overhead, and CUDA Stream pipelining: sequential CPU vs. parallel CUDA on an NVIDIA GPU"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_before = Pt(8)

    # Team Table
    table_shape = s1.shapes.add_table(5, 2, Inches(0.8), Inches(3.6), Inches(6.5), Inches(2.8))
    t1 = table_shape.table
    t1.columns[0].width = Inches(2.8)
    t1.columns[1].width = Inches(3.7)

    headers = ["USN", "Name"]
    for i, h in enumerate(headers):
        c = t1.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = PRIMARY_BL
        p = c.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = BG_WHITE

    team = [
        ("01FE24BCI021", "Joel Biju"),
        ("01FE24BCI012", "Mehak Sayed Yusuf"),
        ("01FE24BCI024", "Akshay Bhat"),
        ("01FE24BCI008", "Vageesh Mathad")
    ]
    for r_idx, (usn, name) in enumerate(team):
        c0 = t1.cell(r_idx + 1, 0)
        c0.text = usn
        c0.fill.solid()
        c0.fill.fore_color.rgb = CARD_BG
        p = c0.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK

        c1 = t1.cell(r_idx + 1, 1)
        c1.text = name
        c1.fill.solid()
        c1.fill.fore_color.rgb = CARD_BG
        p = c1.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

    # Hardware Callout Box on Right
    hw_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(3.6), Inches(4.7), Inches(2.8))
    hw_card.fill.solid()
    hw_card.fill.fore_color.rgb = CARD_BG
    hw_card.line.color.rgb = CARD_BORDER
    htf = hw_card.text_frame
    htf.word_wrap = True

    p = htf.paragraphs[0]
    p.text = "System Environment"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BL

    hw_info = [
        "GPU: NVIDIA Quadro T2000 Max-Q (4GB GDDR6)",
        "Architecture: NVIDIA Turing (1024 CUDA Cores)",
        "CUDA Compiler: nvcc with -O2 optimization",
        "Driver: 595.95 | CUDA Version: 13.2",
        "Platform: Windows 11 64-bit"
    ]
    for info in hw_info:
        p = htf.add_paragraph()
        p.text = f"•  {info}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(6)

    # Slide 1 Number
    s1_num = s1.shapes.add_textbox(Inches(12.0), Inches(6.8), Inches(0.8), Inches(0.4))
    s1_num.text_frame.paragraphs[0].text = "1"
    s1_num.text_frame.paragraphs[0].font.size = Pt(12)
    s1_num.text_frame.paragraphs[0].font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: EXPERIMENT OVERVIEW
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_white_bg(s2)
    add_slide_header(s2, "Experiment Overview", 2)

    # Left Column: Theme, Mode, Main Task
    c2_1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c2_1.fill.solid()
    c2_1.fill.fore_color.rgb = CARD_BG
    c2_1.line.color.rgb = CARD_BORDER
    tf2_1 = c2_1.text_frame
    tf2_1.word_wrap = True

    p = tf2_1.paragraphs[0]
    p.text = "Theme"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    p = tf2_1.add_paragraph()
    p.text = "GPU Dataset Processing"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(2)

    p = tf2_1.add_paragraph()
    p.text = "Parallel Mode"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(16)

    p = tf2_1.add_paragraph()
    p.text = "CUDA on an NVIDIA GPU"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BL
    p.space_before = Pt(2)

    p = tf2_1.add_paragraph()
    p.text = "Main Task"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(16)

    p = tf2_1.add_paragraph()
    p.text = "Element-wise operation: Output[i] = Input[i] × 2"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.space_before = Pt(2)

    # Right Column: What we measured
    c2_2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    c2_2.fill.solid()
    c2_2.fill.fore_color.rgb = CARD_BG
    c2_2.line.color.rgb = CARD_BORDER
    tf2_2 = c2_2.text_frame
    tf2_2.word_wrap = True

    p = tf2_2.paragraphs[0]
    p.text = "What We Measured"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK

    pts2 = [
        "Processing time across 5 dataset sizes (1M to 50M elements), evaluated over 5 repeated iterations each.",
        "CPU sequential time vs. OpenMP multi-core time vs. CUDA kernel time vs. Total CUDA time (including PCIe transfers).",
        "Speedup metrics and result verification for every individual run.",
        "The impact of PCIe transfer latency and how CUDA Stream pipelining overcomes this overhead."
    ]
    for pt in pts2:
        p = tf2_2.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 3: DATASET PLAN
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_white_bg(s3)
    add_slide_header(s3, "Dataset Plan", 3)

    t3_shape = s3.shapes.add_table(6, 3, Inches(0.8), Inches(1.6), Inches(7.5), Inches(4.5))
    t3 = t3_shape.table
    t3.columns[0].width = Inches(2.3)
    t3.columns[1].width = Inches(2.7)
    t3.columns[2].width = Inches(2.5)

    headers3 = ["Dataset Run", "Number of Elements", "Approx. Float Data Size"]
    for i, h in enumerate(headers3):
        c = t3.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = PRIMARY_BL
        p = c.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = BG_WHITE

    ds_plan = [
        ("Dataset 1", "1,000,000 (1M)", "~4 MB"),
        ("Dataset 2", "5,000,000 (5M)", "~20 MB"),
        ("Dataset 3", "10,000,000 (10M)", "~40 MB"),
        ("Dataset 4", "20,000,000 (20M)", "~80 MB"),
        ("Dataset 5", "50,000,000 (50M)", "~200 MB")
    ]
    for r_idx, row in enumerate(ds_plan):
        for c_idx, val in enumerate(row):
            c = t3.cell(r_idx + 1, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = CARD_BG
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK

    # Side Card
    c3_right = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.6), Inches(3.7), Inches(4.5))
    c3_right.fill.solid()
    c3_right.fill.fore_color.rgb = CARD_BG
    c3_right.line.color.rgb = CARD_BORDER
    tf3_r = c3_right.text_frame
    tf3_r.word_wrap = True

    p = tf3_r.paragraphs[0]
    p.text = "Generated in Code"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK

    p = tf3_r.add_paragraph()
    p.text = "• Single-precision floats\n• Formula: h_input[i] = (float)(i % 1000)\n• No external dataset downloads required\n• Eliminates disk I/O noise during timing"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED
    p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 4: METHOD & ENVIRONMENT
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_white_bg(s4)
    add_slide_header(s4, "Method & Environment", 4)

    steps = [
        ("1", "Generate data on host memory"),
        ("2", "Run CPU loop (baseline timing)"),
        ("3", "Copy Host → Device (PCIe)"),
        ("4", "Launch CUDA kernel in parallel"),
        ("5", "Copy back & verify correctness")
    ]
    for idx, (num, desc) in enumerate(steps):
        x = 0.8 + idx * 2.35
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.6), Inches(2.2), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = PRIMARY_BL
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BL
        p.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_DARK
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(8)

    # Bottom Cards: System Requirements & Speedup Definitions
    c4_b1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(5.6), Inches(2.6))
    c4_b1.fill.solid()
    c4_b1.fill.fore_color.rgb = CARD_BG
    c4_b1.line.color.rgb = CARD_BORDER
    tf_b1 = c4_b1.text_frame
    tf_b1.word_wrap = True
    p = tf_b1.paragraphs[0]
    p.text = "System Requirements"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p_pts = [
        "NVIDIA Quadro T2000 GPU + Driver 595.95",
        "CUDA Toolkit 13.2 (nvcc), compiled with -O2",
        "Windows 11 64-bit environment",
        "Python with Matplotlib, NumPy, Pandas"
    ]
    for pt in p_pts:
        p = tf_b1.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(4)

    c4_b2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.2), Inches(5.7), Inches(2.6))
    c4_b2.fill.solid()
    c4_b2.fill.fore_color.rgb = CARD_BG
    c4_b2.line.color.rgb = CARD_BORDER
    tf_b2 = c4_b2.text_frame
    tf_b2.word_wrap = True
    p = tf_b2.paragraphs[0]
    p.text = "Speedup Definitions"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p_defs = [
        "Total (end-to-end): CPU Time ÷ Total CUDA Time (includes PCIe transfers)",
        "Kernel (compute-only): CPU Time ÷ CUDA Kernel Time (isolates GPU compute)",
        "Pipelined Speedup: CPU Time ÷ Overlapped Pipelined Time"
    ]
    for d in p_defs:
        p = tf_b2.add_paragraph()
        p.text = f"•  {d}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: AVERAGE RESULTS (5 ITERATIONS)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_white_bg(s5)
    add_slide_header(s5, "Average Results (5 Iterations)", 5)

    t5_shape = s5.shapes.add_table(6, 7, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.4))
    t5 = t5_shape.table
    widths5 = [Inches(1.8), Inches(1.6), Inches(1.6), Inches(1.8), Inches(1.6), Inches(1.6), Inches(1.7)]
    for idx, w in enumerate(widths5):
        t5.columns[idx].width = w

    h5 = ["Dataset Size", "Avg CPU (ms)", "Avg Kernel (ms)", "Avg Total CUDA (ms)", "Speedup (Total)", "Speedup (Kernel)", "Verified"]
    for i, h in enumerate(h5):
        c = t5.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = PRIMARY_BL
        p = c.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = BG_WHITE

    d5 = [
        ("1,000,000", "0.97 ms", "0.473 ms", "2.22 ms", "0.43x", "2.04x", "PASSED"),
        ("5,000,000", "4.72 ms", "0.592 ms", "8.32 ms", "0.57x", "7.97x", "PASSED"),
        ("10,000,000", "8.45 ms", "0.698 ms", "16.27 ms", "0.52x", "12.11x", "PASSED"),
        ("20,000,000", "17.43 ms", "0.930 ms", "30.65 ms", "0.57x", "18.74x", "PASSED"),
        ("50,000,000", "46.18 ms", "1.594 ms", "80.05 ms", "0.58x", "28.97x", "PASSED")
    ]
    for r_idx, row in enumerate(d5):
        for c_idx, val in enumerate(row):
            c = t5.cell(r_idx + 1, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = CARD_BG
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = ACCENT_GRN if c_idx == 6 else (TEXT_DARK if c_idx < 5 else ACCENT_GRN)
            if c_idx in [5, 6]:
                p.font.bold = True

    c5_note = s5.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.6))
    c5_note.text_frame.word_wrap = True
    p = c5_note.text_frame.paragraphs[0]
    p.text = "Key Finding: All 25 runs produced correct output. Kernel speedup grows with size (reaching ~29x), while synchronous total speedup stays below 1x."
    p.font.size = Pt(12)
    p.font.italic = True
    p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: KERNEL SPEEDUP ACROSS ITERATIONS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_white_bg(s6)
    add_slide_header(s6, "Kernel Speedup Across Iterations", 6)

    t6_shape = s6.shapes.add_table(6, 7, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.4))
    t6 = t6_shape.table
    w6 = [Inches(2.1), Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6)]
    for idx, w in enumerate(w6):
        t6.columns[idx].width = w

    h6 = ["Dataset Size", "Run 1", "Run 2", "Run 3", "Run 4", "Run 5", "Average"]
    for i, h in enumerate(h6):
        c = t6.cell(0, i)
        c.text = h
        c.fill.solid()
        c.fill.fore_color.rgb = PRIMARY_BL
        p = c.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = BG_WHITE

    d6 = [
        ("1,000,000", "1.89x", "2.11x", "1.64x", "2.00x", "2.51x", "2.04x"),
        ("5,000,000", "9.15x", "6.66x", "7.67x", "10.62x", "6.85x", "7.97x"),
        ("10,000,000", "13.23x", "15.67x", "13.37x", "11.53x", "8.74x", "12.11x"),
        ("20,000,000", "18.70x", "18.90x", "18.46x", "19.69x", "17.99x", "18.74x"),
        ("50,000,000", "27.73x", "29.45x", "29.31x", "32.53x", "26.14x", "28.97x")
    ]
    for r_idx, row in enumerate(d6):
        for c_idx, val in enumerate(row):
            c = t6.cell(r_idx + 1, c_idx)
            c.text = val
            c.fill.solid()
            c.fill.fore_color.rgb = CARD_BG
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK
            if c_idx == 6:
                p.font.bold = True
                p.font.color.rgb = PRIMARY_BL

    c6_note = s6.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.6))
    c6_note.text_frame.word_wrap = True
    p = c6_note.text_frame.paragraphs[0]
    p.text = "Larger datasets yield more stable results (50M: 26.1x to 32.5x). Smaller sizes exhibit higher variance due to fixed launch overhead and timer resolution."
    p.font.size = Pt(12)
    p.font.italic = True
    p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 7: KERNEL SPEEDUP SCALES WITH DATA SIZE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_white_bg(s7)
    add_slide_header(s7, "Kernel Speedup Scales with Data Size", 7)

    # Big Callout Stat Box on Left
    stat_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2))
    stat_box.fill.solid()
    stat_box.fill.fore_color.rgb = CARD_BG
    stat_box.line.color.rgb = ACCENT_GRN
    stat_box.line.width = Pt(2)

    stf = stat_box.text_frame
    stf.word_wrap = True
    p = stf.paragraphs[0]
    p.text = "28.97x"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GRN

    p2 = stf.add_paragraph()
    p2.text = "kernel compute speedup at 50M elements"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(8)

    p3 = stf.add_paragraph()
    p3.text = "up from 2.04x at 1M elements"
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(4)

    p4 = stf.add_paragraph()
    p4.text = "As dataset size expands, thousands of threads saturate the GPU's streaming multiprocessors, amortizing warp scheduling costs and delivering massive parallel acceleration."
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_MUTED
    p4.space_before = Pt(16)

    # Graph on Right
    img_speedup = os.path.join(results_dir, "speedup_analysis.png")
    if os.path.exists(img_speedup):
        s7.shapes.add_picture(img_speedup, Inches(5.6), Inches(1.6), Inches(6.9), Inches(5.2))

    # =========================================================================
    # SLIDE 8: EXECUTION TIME: CPU VS. CUDA
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_white_bg(s8)
    add_slide_header(s8, "Execution Time: CPU vs. CUDA", 8)

    # Subtitle Callout
    sub_box = s8.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.7), Inches(0.6))
    sub_tf = sub_box.text_frame
    sub_tf.word_wrap = True
    p = sub_tf.paragraphs[0]
    p.text = "The kernel alone is far faster than the CPU, but copying data over PCIe pushes total synchronous CUDA time above CPU time."
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    # Execution Time Graph
    img_time = os.path.join(results_dir, "execution_time_breakdown.png")
    if os.path.exists(img_time):
        s8.shapes.add_picture(img_time, Inches(0.8), Inches(1.8), Inches(8.0), Inches(5.0))

    # Right Side Explanatory Card
    t8_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.1), Inches(1.8), Inches(3.4), Inches(5.0))
    t8_card.fill.solid()
    t8_card.fill.fore_color.rgb = CARD_BG
    t8_card.line.color.rgb = CARD_BORDER
    tf8 = t8_card.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "Runtime Dynamics"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK

    pts8 = [
        "CPU Sequential scales linearly with problem size (0.97 ms to 46.18 ms).",
        "CUDA Kernel takes merely 1.59 ms even at 50 million elements.",
        "PCIe Transfers require ~78.4 ms at 50M, eclipsing the compute phase.",
        "Total Synchronous Time reaches 80.05 ms, higher than the CPU alone!"
    ]
    for pt in pts8:
        p = tf8.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 9: PERFORMANCE ANALYSIS - WHY TOTAL TIME EXCEEDS CPU TIME
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_white_bg(s9)
    add_slide_header(s9, "Performance Analysis: Why Total CUDA Time Exceeds CPU Time", 9)

    # 3 Column Cards
    col_w = Inches(3.6)
    c9_1 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), col_w, Inches(5.2))
    c9_1.fill.solid()
    c9_1.fill.fore_color.rgb = CARD_BG
    c9_1.line.color.rgb = CARD_BORDER
    tf9_1 = c9_1.text_frame
    tf9_1.word_wrap = True
    p = tf9_1.paragraphs[0]
    p.text = "PCIe Transfer Overhead"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BL
    p2 = tf9_1.add_paragraph()
    p2.text = "cudaMemcpy moves data Host → Device → Host across the PCIe bus, with high fixed transfer latency and bus bandwidth limits."
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(12)

    p3 = tf9_1.add_paragraph()
    p3.text = "Driver & Context Setup"
    p3.font.size = Pt(16)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_DARK
    p3.space_before = Pt(20)
    p4 = tf9_1.add_paragraph()
    p4.text = "cudaMalloc, CUDA driver context initialization, and kernel launch queues add fixed baseline overhead."
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_DARK
    p4.space_before = Pt(12)

    # Center Stat Card (98%)
    c9_2 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.6), col_w, Inches(5.2))
    c9_2.fill.solid()
    c9_2.fill.fore_color.rgb = CARD_BG
    c9_2.line.color.rgb = ACCENT_RED
    c9_2.line.width = Pt(2)
    tf9_2 = c9_2.text_frame
    tf9_2.word_wrap = True
    p = tf9_2.paragraphs[0]
    p.text = "98%"
    p.font.size = Pt(64)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p2 = tf9_2.add_paragraph()
    p2.text = "of total CUDA time at 50M elements is spent on data transfer and PCIe overhead"
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(10)

    p3 = tf9_2.add_paragraph()
    p3.text = "Only 1.59 ms is compute, while 78.46 ms is bus transfer!"
    p3.font.size = Pt(12)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(10)

    # Right Card: Low Arithmetic Intensity
    c9_3 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2))
    c9_3.fill.solid()
    c9_3.fill.fore_color.rgb = CARD_BG
    c9_3.line.color.rgb = CARD_BORDER
    tf9_3 = c9_3.text_frame
    tf9_3.word_wrap = True
    p = tf9_3.paragraphs[0]
    p.text = "Only 1 FLOP per Element"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    pts9_3 = [
        "Arithmetic intensity = 1 FLOP / 4 bytes read.",
        "Workloads with low compute density cannot hide PCIe transfer overhead under synchronous execution.",
        "CPU executes directly in RAM, avoiding PCIe penalties entirely.",
        "Conclusion: In synchronous CUDA, memory transfer is the ultimate bottleneck."
    ]
    for pt in pts9_3:
        p = tf9_3.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 10: WHY COMPARE KERNEL TIME VS CPU TIME?
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_white_bg(s10)
    add_slide_header(s10, "Why Compare Kernel Time vs. CPU Time?", 10)

    reasons = [
        ("Raw Parallel Capability", "Shows the true compute potential of thousands of GPU threads without PCIe bus-transfer noise.", PRIMARY_BL),
        ("Architecture Potential", "Shows how massively parallel hardware handles element-wise work once data is already in high-bandwidth VRAM.", ACCENT_GRN),
        ("Optimization Guidance", "Reveals whether an application is limited by GPU compute density or by PCIe bus bandwidth—guiding future pipelining.", ACCENT_PURP)
    ]
    for idx, (title, desc, color) in enumerate(reasons):
        y = 1.6 + idx * 1.75
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(11.7), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_DARK
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 11: OUR ENHANCEMENT - BREAKING THE BOTTLENECK (THE "BIT EXTRA")
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_white_bg(s11)
    add_slide_header(s11, "Our Technical Enhancement: Resolving the PCIe Bottleneck", 11)

    # Subtitle
    sub11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.7), Inches(0.5))
    sub11.text_frame.word_wrap = True
    sub11.text_frame.paragraphs[0].text = "Instead of stopping at synchronous limitations, our team implemented two architectural optimizations:"
    sub11.text_frame.paragraphs[0].font.size = Pt(13)
    sub11.text_frame.paragraphs[0].font.color.rgb = PRIMARY_BL

    # Left Card: CUDA Streams
    c11_l = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0))
    c11_l.fill.solid()
    c11_l.fill.fore_color.rgb = CARD_BG
    c11_l.line.color.rgb = ACCENT_GRN
    c11_l.line.width = Pt(1.5)
    tf11_l = c11_l.text_frame
    tf11_l.word_wrap = True

    p = tf11_l.paragraphs[0]
    p.text = "1. Asynchronous CUDA Streams"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GRN

    pts11_l = [
        "Pinned Memory (cudaMallocHost): Enables Direct Memory Access (DMA) without CPU staging buffers.",
        "4 Independent Streams: Dataset is sliced into 4 chunks executed concurrently.",
        "Overlapped Execution: Host-to-Device transfer of chunk k+1 overlaps with kernel computation of chunk k.",
        "Result: Total runtime drops from 80.05 ms to 36.50 ms (> 54% latency cut!), achieving 1.27x net speedup!"
    ]
    for pt in pts11_l:
        p = tf11_l.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)

    # Right Card: Vectorized float4
    c11_r = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.0))
    c11_r.fill.solid()
    c11_r.fill.fore_color.rgb = CARD_BG
    c11_r.line.color.rgb = ACCENT_PURP
    c11_r.line.width = Pt(1.5)
    tf11_r = c11_r.text_frame
    tf11_r.word_wrap = True

    p = tf11_r.paragraphs[0]
    p.text = "2. Vectorized float4 Memory Access"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURP

    pts11_r = [
        "128-Bit Transactions: Each thread loads and stores 4 floats simultaneously using float4.",
        "Memory Bus Saturation: Satures the Quadro T2000's 128-bit memory bus width with fewer instructions.",
        "Kernel Compute Boost: Reduces kernel execution time from 1.59 ms to 1.21 ms (1.32x faster).",
        "Effective Bandwidth: Pushes memory throughput from 50.2 GB/s to 66.2 GB/s, reaching 38.2x compute speedup over CPU!"
    ]
    for pt in pts11_r:
        p = tf11_r.add_paragraph()
        p.text = f"•  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 12: STREAM PIPELINING & BANDWIDTH VISUALIZATIONS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_white_bg(s12)
    add_slide_header(s12, "Stream Pipelining Timeline & Bandwidth Saturation", 12)

    img_pipe = os.path.join(results_dir, "cuda_stream_pipelining.png")
    if os.path.exists(img_pipe):
        s12.shapes.add_picture(img_pipe, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))

    img_bw = os.path.join(results_dir, "memory_bandwidth_throughput.png")
    if os.path.exists(img_bw):
        s12.shapes.add_picture(img_bw, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))

    # =========================================================================
    # SLIDE 13: CONCLUSION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_white_bg(s13)
    add_slide_header(s13, "Conclusion & Key Findings", 13)

    concl_cards = [
        ("28.97x", "Kernel speedup at 50M elements (up to 38.2x with float4)", ACCENT_GRN),
        ("2.04x → 28.97x", "Kernel speedup scaling from 1M to 50M elements", PRIMARY_BL),
        ("~98%", "of baseline synchronous CUDA time is PCIe transfer at 50M", ACCENT_RED),
        ("> 54%", "Latency reduction achieved via Asynchronous CUDA Stream Pipelining", ACCENT_PURP)
    ]
    for idx, (stat, label, col) in enumerate(concl_cards):
        col_idx = idx % 2
        row_idx = idx // 2
        x = 0.8 + col_idx * 6.0
        y = 1.6 + row_idx * 2.5
        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stat
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(13)
        p2.font.color.rgb = TEXT_DARK
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 14: THANK YOU
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_white_bg(s14)

    ty_card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.8), Inches(10.33), Inches(4.0))
    ty_card.fill.solid()
    ty_card.fill.fore_color.rgb = CARD_BG
    ty_card.line.color.rgb = PRIMARY_BL
    ty_card.line.width = Pt(2)

    ty_tf = ty_card.text_frame
    ty_tf.word_wrap = True

    p = ty_tf.paragraphs[0]
    p.text = "Thank you"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BL
    p.alignment = PP_ALIGN.CENTER

    p2 = ty_tf.add_paragraph()
    p2.text = "GPU Dataset Processing using CUDA"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_DARK
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(10)

    p3 = ty_tf.add_paragraph()
    p3.text = "Joel Biju (01FE24BCI021)   •   Mehak Sayed Yusuf (01FE24BCI012)\nAkshay Bhat (01FE24BCI024)   •   Vageesh Mathad (01FE24BCI008)"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(16)

    prs.save(output_pptx)
    print(f"Enhanced Google-style presentation generated at: {output_pptx}")

if __name__ == "__main__":
    build_presentation()
