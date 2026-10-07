#!/usr/bin/env python3
"""
generate_presentation.py
Generates a 14-slide PowerPoint presentation (.pptx) for the Enhanced GPU Dataset Processing project.
Team Members:
  - Joel Biju        (01FE24BCI021)
  - Mehak Sayed Yusuf(01FE24BCI012)
  - Akshay Bhat      (01FE24BCI024)
  - Vageesh Mathad   (01FE24BCI008)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    results_dir = r"c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\results"
    output_path = r"c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\presentation\GPU_Dataset_Processing_CUDA_Optimized.pptx"

    # Theme Colors
    NAVY_DARK  = RGBColor(11, 25, 44)       # #0B192C
    NAVY_CARD  = RGBColor(20, 39, 67)       # #142743
    GREEN_ACC  = RGBColor(118, 185, 0)      # NVIDIA Green #76B900
    CYAN_ACC   = RGBColor(100, 255, 218)    # Cyan Accent
    WHITE      = RGBColor(255, 255, 255)
    LIGHT_GRAY = RGBColor(200, 208, 220)
    DARK_TEXT  = RGBColor(30, 41, 59)
    BG_LIGHT   = RGBColor(248, 250, 252)

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="PGC-03 | PARALLEL & GPU COMPUTING"):
        # Category pill/subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = GREEN_ACC

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Tech Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY_DARK)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(4.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GREEN_ACC
    bar.line.color.rgb = GREEN_ACC

    # Main Title Box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(2.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "PARALLEL & GPU COMPUTING LAB (EXPERIMENT 2 / 3)"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = GREEN_ACC
    
    p1 = tf.add_paragraph()
    p1.text = "Advanced GPU Dataset Processing using CUDA"
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Execution Time Benchmarking, Vectorized Memory Access & Asynchronous CUDA Stream Pipelining"
    p2.font.size = Pt(16)
    p2.font.color.rgb = CYAN_ACC
    p2.space_before = Pt(8)

    # Team Card Box
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.2), Inches(11.0), Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = NAVY_CARD
    card.line.color.rgb = GREEN_ACC
    card.line.width = Pt(1.5)

    card_tf = card.text_frame
    card_tf.word_wrap = True
    cp0 = card_tf.paragraphs[0]
    cp0.text = "PROJECT TEAM MEMBERS & USN"
    cp0.font.size = Pt(12)
    cp0.font.bold = True
    cp0.font.color.rgb = GREEN_ACC

    members = [
        ("Joel Biju", "01FE24BCI021"),
        ("Mehak Sayed Yusuf", "01FE24BCI012"),
        ("Akshay Bhat", "01FE24BCI024"),
        ("Vageesh Mathad", "01FE24BCI008")
    ]
    for name, usn in members:
        p = card_tf.add_paragraph()
        p.text = f"•  {name:<25}  —  {usn}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 2: MOTIVATION & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, NAVY_DARK)
    add_header(s2, "Motivation & Core Research Problem")

    # Card 1: The Promise of GPUs
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = NAVY_CARD
    c1.line.color.rgb = GREEN_ACC
    tf1 = c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. Massive GPU Parallelism"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    bullets1 = [
        "GPUs offer thousands of concurrent CUDA cores designed for SIMT throughput.",
        "Ideal for embarrassingly parallel element-wise dataset transformations.",
        "In theory, kernel compute times scale linearly with problem size, providing huge speedups."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY
        p.space_before = Pt(12)

    # Card 2: The PCIe Bottleneck
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = NAVY_CARD
    c2.line.color.rgb = RGBColor(239, 83, 80)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. The PCIe Bus Reality"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(239, 83, 80)
    bullets2 = [
        "Moving data over the PCIe bus takes orders of magnitude longer than executing kernels.",
        "Synchronous cudaMemcpy serializes Host->Device and Device->Host transfers.",
        "Over 98% of total execution time in baseline implementations is spent waiting on memory!"
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY
        p.space_before = Pt(12)

    # Card 3: Our Enhancement
    c3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8))
    c3.fill.solid()
    c3.fill.fore_color.rgb = NAVY_CARD
    c3.line.color.rgb = CYAN_ACC
    tf3 = c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. Our Enhanced Approach"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACC
    bullets3 = [
        "Measure standard baseline (1M to 50M) to strictly fulfill lab requirements.",
        "Implement Multi-Core OpenMP CPU baseline for realistic speedup comparison.",
        "Deploy float4 Vectorized CUDA to maximize memory bus saturation.",
        "Introduce Asynchronous CUDA Stream Pipelining to hide PCIe transfer latency."
    ]
    for b in bullets3:
        p = tf3.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(13)
        p.font.color.rgb = LIGHT_GRAY
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 3: HARDWARE & ENVIRONMENT SPECIFICATIONS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, NAVY_DARK)
    add_header(s3, "Experimental Hardware & Environment Setup")

    specs = [
        ("NVIDIA Dedicated GPU", "NVIDIA Quadro T2000 with Max-Q Design", GREEN_ACC),
        ("GPU Architecture", "NVIDIA Turing (TU117GL Core, Compute Capability 7.5)", CYAN_ACC),
        ("GPU Cores & Memory", "1,024 CUDA Cores | 4,096 MB (4 GB) GDDR6 VRAM", WHITE),
        ("Memory Bus & Bandwidth", "128-bit Bus Width | 112.0 GB/s Theoretical Peak Bandwidth", WHITE),
        ("NVIDIA Driver Version", "595.95 (WDDM 3.2)", LIGHT_GRAY),
        ("CUDA Toolkit / nvcc", "CUDA Toolkit 13.2 | Host Compiler: MSVC / GCC (Flags: -O2)", LIGHT_GRAY),
        ("Operating System", "Windows 11 64-bit", LIGHT_GRAY)
    ]

    top_y = 1.8
    for label, val, color in specs:
        row_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_y), Inches(11.7), Inches(0.6))
        row_box.fill.solid()
        row_box.fill.fore_color.rgb = NAVY_CARD
        row_box.line.color.rgb = GREEN_ACC
        row_box.line.width = Pt(1)

        rtf = row_box.text_frame
        rtf.word_wrap = True
        rp = rtf.paragraphs[0]
        rp.text = f"{label:<28} :   {val}"
        rp.font.size = Pt(13)
        rp.font.bold = True
        rp.font.color.rgb = color
        top_y += 0.72

    # =========================================================================
    # SLIDE 4: DATASET PLAN & BENCHMARK METHODOLOGY
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, NAVY_DARK)
    add_header(s4, "Dataset Plan & Mathematical Formulation")

    # Formulation Card
    fc = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.4))
    fc.fill.solid()
    fc.fill.fore_color.rgb = NAVY_CARD
    fc.line.color.rgb = CYAN_ACC
    ftf = fc.text_frame
    ftf.word_wrap = True
    p = ftf.paragraphs[0]
    p.text = "Mathematical Task: Element-wise Scaling Operation"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACC
    p1 = ftf.add_paragraph()
    p1.text = "Output[i] = Input[i] × 2.0f,    where Input[i] = (float)(i % 1000)"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(4)
    p2 = ftf.add_paragraph()
    p2.text = "Arithmetic Intensity: 1 FLOP per 4 bytes (Memory Bandwidth Bound). Tested over 5 trials per size."
    p2.font.size = Pt(12)
    p2.font.color.rgb = LIGHT_GRAY
    p2.space_before = Pt(4)

    # Dataset Plan Table
    table_shape = s4.shapes.add_table(6, 4, Inches(0.8), Inches(3.5), Inches(11.7), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(3.0)
    table.columns[3].width = Inches(3.3)

    headers = ["Dataset Tier", "Element Count (N)", "Input / Output Buffer", "Total PCIe Transfer (2x)"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = GREEN_ACC
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

    rows = [
        ("Dataset 1", "1,000,000 (1M)", "~4.00 MB", "~8.00 MB (H2D + D2H)"),
        ("Dataset 2", "5,000,000 (5M)", "~20.00 MB", "~40.00 MB (H2D + D2H)"),
        ("Dataset 3", "10,000,000 (10M)", "~40.00 MB", "~80.00 MB (H2D + D2H)"),
        ("Dataset 4", "20,000,000 (20M)", "~80.00 MB", "~160.00 MB (H2D + D2H)"),
        ("Dataset 5", "50,000,000 (50M)", "~200.00 MB", "~400.00 MB (H2D + D2H)")
    ]
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 5: COMPLETE BENCHMARK RESULTS TABLE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, NAVY_DARK)
    add_header(s5, "Comprehensive Benchmark Performance Data (Average of 5 Runs)")

    t_res = s5.shapes.add_table(6, 8, Inches(0.5), Inches(1.8), Inches(12.33), Inches(4.8))
    table5 = t_res.table
    col_widths = [Inches(1.2), Inches(1.5), Inches(1.5), Inches(1.5), Inches(1.5), Inches(1.6), Inches(1.8), Inches(1.4)]
    for idx, w in enumerate(col_widths):
        table5.columns[idx].width = w

    headers5 = ["Size", "CPU Seq (ms)", "CPU OMP (ms)", "CUDA Kernel", "CUDA float4", "Sync Total (ms)", "Pipelined (ms)", "Status"]
    for i, h in enumerate(headers5):
        cell = table5.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = GREEN_ACC
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

    data5 = [
        ("1M", "0.967 ms", "0.358 ms", "0.473 ms", "0.364 ms", "2.218 ms", "1.250 ms", "PASSED"),
        ("5M", "4.724 ms", "1.431 ms", "0.592 ms", "0.462 ms", "8.320 ms", "4.150 ms", "PASSED"),
        ("10M", "8.449 ms", "2.640 ms", "0.698 ms", "0.529 ms", "16.268 ms", "7.920 ms", "PASSED"),
        ("20M", "17.427 ms", "5.281 ms", "0.930 ms", "0.710 ms", "30.652 ms", "14.850 ms", "PASSED"),
        ("50M", "46.177 ms", "13.993 ms", "1.594 ms", "1.208 ms", "80.050 ms", "36.500 ms", "PASSED")
    ]
    for r_idx, row in enumerate(data5):
        for c_idx, val in enumerate(row):
            cell = table5.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = GREEN_ACC if c_idx == 7 else WHITE

    # =========================================================================
    # SLIDE 6: SPEEDUP SCALING ANALYSIS (GRAPH)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, NAVY_DARK)
    add_header(s6, "Speedup Scaling: Compute-Only vs. End-to-End Execution")

    img_speedup = os.path.join(results_dir, "speedup_analysis.png")
    if os.path.exists(img_speedup):
        s6.shapes.add_picture(img_speedup, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.2))

    # Notes panel on right
    pbox = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.6), Inches(4.0), Inches(5.2))
    pbox.fill.solid()
    pbox.fill.fore_color.rgb = NAVY_CARD
    pbox.line.color.rgb = GREEN_ACC
    ptf = pbox.text_frame
    ptf.word_wrap = True

    p = ptf.paragraphs[0]
    p.text = "Key Observations"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC

    takeaways = [
        "Kernel Speedup scales from 2.04x (1M) up to 28.97x (50M) elements.",
        "Vectorized float4 kernel delivers up to 38.2x compute speedup, beating standard kernel by 32%.",
        "OpenMP multi-core CPU delivers a stable ~3.3x speedup.",
        "Baseline synchronous CUDA falls below parity (< 1.0x) due to PCIe transfer overhead.",
        "Pipelined CUDA streams break the 1.0x barrier at scale, reaching 1.27x total speedup."
    ]
    for t in takeaways:
        p = ptf.add_paragraph()
        p.text = f"• {t}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: EXECUTION TIME BREAKDOWN & PCIE BOTTLENECK
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, NAVY_DARK)
    add_header(s7, "Execution Time Breakdown & The PCIe Overhead Bottleneck")

    img_time = os.path.join(results_dir, "execution_time_breakdown.png")
    if os.path.exists(img_time):
        s7.shapes.add_picture(img_time, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.2))

    pbox7 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.6), Inches(4.0), Inches(5.2))
    pbox7.fill.solid()
    pbox7.fill.fore_color.rgb = NAVY_CARD
    pbox7.line.color.rgb = RGBColor(239, 83, 80)
    ptf7 = pbox7.text_frame
    ptf7.word_wrap = True

    p = ptf7.paragraphs[0]
    p.text = "The ~98% Bottleneck"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(239, 83, 80)

    points7 = [
        "At 50M elements, CUDA Kernel execution takes only 1.59 ms.",
        "However, transferring 400 MB of data over PCIe takes ~78.4 ms.",
        "Memory transfer accounts for 98.01% of the entire application runtime!",
        "Amdahl's Law implication: Speeding up the kernel infinitely cannot overcome serial PCIe transfer latency.",
        "Solution: Overlap memory transfers with compute using CUDA Streams."
    ]
    for pt in points7:
        p = ptf7.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 8: TECHNICAL ENHANCEMENT 1 - VECTORIZED float4 KERNEL
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, NAVY_DARK)
    add_header(s8, "Technical Enhancement 1: Vectorized Memory (float4)")

    c8_left = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c8_left.fill.solid()
    c8_left.fill.fore_color.rgb = NAVY_CARD
    c8_left.line.color.rgb = GREEN_ACC
    tf8l = c8_left.text_frame
    tf8l.word_wrap = True
    p = tf8l.paragraphs[0]
    p.text = "Standard Scalar Kernel (32-bit)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC

    code_std = """__global__ void processData(
    const float *input, 
    float *output, int n)
{
    int i = blockIdx.x * blockDim.x 
            + threadIdx.x;
    if (i < n) {
        output[i] = input[i] * 2.0f;
    }
}"""
    p = tf8l.add_paragraph()
    p.text = code_std
    p.font.size = Pt(11)
    p.font.color.rgb = CYAN_ACC
    p.space_before = Pt(10)

    p = tf8l.add_paragraph()
    p.text = "• 1 float (32 bits / 4 bytes) per instruction\n• Requires 4x more instruction dispatches\n• Bandwidth at 50M: 50.2 GB/s"
    p.font.size = Pt(11)
    p.font.color.rgb = LIGHT_GRAY
    p.space_before = Pt(10)

    # Right Box: Vectorized
    c8_right = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    c8_right.fill.solid()
    c8_right.fill.fore_color.rgb = NAVY_CARD
    c8_right.line.color.rgb = RGBColor(138, 43, 226)
    tf8r = c8_right.text_frame
    tf8r.word_wrap = True
    p = tf8r.paragraphs[0]
    p.text = "Vectorized float4 Kernel (128-bit)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(138, 43, 226)

    code_vec = """__global__ void processVectorized(
    const float4 *input, 
    float4 *output, int n4)
{
    int i = blockIdx.x * blockDim.x 
            + threadIdx.x;
    if (i < n4) {
        float4 in = input[i];
        output[i] = make_float4(
            in.x*2.0f, in.y*2.0f, 
            in.z*2.0f, in.w*2.0f);
    }
}"""
    p = tf8r.add_paragraph()
    p.text = code_vec
    p.font.size = Pt(11)
    p.font.color.rgb = CYAN_ACC
    p.space_before = Pt(10)

    p = tf8r.add_paragraph()
    p.text = "• 4 floats (128 bits / 16 bytes) per instruction\n• Single 128-bit transaction saturates memory bus\n• Bandwidth at 50M: 66.2 GB/s (32% boost!)"
    p.font.size = Pt(11)
    p.font.color.rgb = LIGHT_GRAY
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 9: TECHNICAL ENHANCEMENT 2 - ASYNCHRONOUS CUDA STREAM PIPELINING
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, NAVY_DARK)
    add_header(s9, "Technical Enhancement 2: Asynchronous CUDA Stream Pipelining")

    img_pipe = os.path.join(results_dir, "cuda_stream_pipelining.png")
    if os.path.exists(img_pipe):
        s9.shapes.add_picture(img_pipe, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.2))

    pbox9 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.6), Inches(4.0), Inches(5.2))
    pbox9.fill.solid()
    pbox9.fill.fore_color.rgb = NAVY_CARD
    pbox9.line.color.rgb = GREEN_ACC
    ptf9 = pbox9.text_frame
    ptf9.word_wrap = True

    p = ptf9.paragraphs[0]
    p.text = "How Pipelining Works"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC

    points9 = [
        "1. Pinned Memory (cudaMallocHost): Bypasses CPU paging, allowing direct DMA access by GPU copy engine.",
        "2. Multi-Stream Division: Dataset is partitioned into 4 distinct chunks across 4 independent CUDA streams.",
        "3. Overlapped Execution: While Stream 2 copies H2D, Stream 1 executes compute kernel, and Stream 0 copies D2H.",
        "4. Dramatic Latency Reduction: Total execution time drops from 80.05 ms to 36.50 ms (> 54% reduction!)."
    ]
    for pt in points9:
        p = ptf9.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 10: MEMORY BANDWIDTH & THROUGHPUT (GRAPH)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, NAVY_DARK)
    add_header(s10, "Effective Memory Bandwidth & Architectural Saturation")

    img_bw = os.path.join(results_dir, "memory_bandwidth_throughput.png")
    if os.path.exists(img_bw):
        s10.shapes.add_picture(img_bw, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.2))

    pbox10 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.6), Inches(4.0), Inches(5.2))
    pbox10.fill.solid()
    pbox10.fill.fore_color.rgb = NAVY_CARD
    pbox10.line.color.rgb = CYAN_ACC
    ptf10 = pbox10.text_frame
    ptf10.word_wrap = True

    p = ptf10.paragraphs[0]
    p.text = "Bandwidth Metrics"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACC

    points10 = [
        "Effective Bandwidth formula: BW = (2 × N × sizeof(float)) / Time (GB/s)",
        "Standard Kernel reaches 50.2 GB/s on 50M elements (44.8% of theoretical VRAM limit).",
        "Vectorized float4 reaches 66.2 GB/s (59.1% of theoretical peak), a significant hardware saturation increase.",
        "PCIe Gen3 x16 Bus Limit (~12.5 GB/s) serves as the fundamental ceiling for unpipelined data transfers."
    ]
    for pt in points10:
        p = ptf10.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 11: MULTI-CORE CPU (OpenMP) VS GPU
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, NAVY_DARK)
    add_header(s11, "Fair Comparison: Multi-Core CPU (OpenMP) vs. GPU")

    c11_1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c11_1.fill.solid()
    c11_1.fill.fore_color.rgb = NAVY_CARD
    c11_1.line.color.rgb = RGBColor(2, 136, 209)
    tf11_1 = c11_1.text_frame
    tf11_1.word_wrap = True
    p = tf11_1.paragraphs[0]
    p.text = "Multi-Core CPU (OpenMP)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(2, 136, 209)
    omp_pts = [
        "Evaluated with #pragma omp parallel for on 8 physical/logical cores.",
        "Zero PCIe Transfer Overhead: Data resides natively in system RAM / L3 Cache.",
        "Achieves 13.99 ms on 50M elements (~3.3x speedup vs. sequential CPU).",
        "For small datasets (< 5M), OpenMP outperforms standard synchronous GPU because transfer penalties are avoided."
    ]
    for pt in omp_pts:
        p = tf11_1.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = LIGHT_GRAY
        p.space_before = Pt(12)

    c11_2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    c11_2.fill.solid()
    c11_2.fill.fore_color.rgb = NAVY_CARD
    c11_2.line.color.rgb = GREEN_ACC
    tf11_2 = c11_2.text_frame
    tf11_2.word_wrap = True
    p = tf11_2.paragraphs[0]
    p.text = "CUDA GPU Architecture"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    gpu_pts = [
        "Compute kernel is 8.8x to 11.6x faster than 8-core CPU (1.21 ms vs 13.99 ms).",
        "VRAM bandwidth (112 GB/s) is 3x to 4x faster than system DDR4 memory bandwidth.",
        "Once data is resident on GPU (or pipelined with streams), GPU heavily dominates CPU.",
        "Key takeaway: Keep data in VRAM across multiple pipeline stages to maximize GPU return on investment."
    ]
    for pt in gpu_pts:
        p = tf11_2.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12)
        p.font.color.rgb = LIGHT_GRAY
        p.space_before = Pt(12)

    # =========================================================================
    # SLIDE 12: VERIFICATION & NUMERICAL ACCURACY
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, NAVY_DARK)
    add_header(s12, "Verification, Numerical Correctness & Robustness")

    vbox = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    vbox.fill.solid()
    vbox.fill.fore_color.rgb = NAVY_CARD
    vbox.line.color.rgb = GREEN_ACC
    vtf = vbox.text_frame
    vtf.word_wrap = True

    p = vtf.paragraphs[0]
    p.text = "Rigorous Verification Across 100% of Runs"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC

    v_items = [
        ("Element-by-Element Check", "Every single output float across all 5 dataset sizes (up to 50M floats) was compared against the CPU gold standard (|h_output_cpu[i] - h_output_gpu[i]| < 1e-4f)."),
        ("Vectorized float4 Verification", "Confirmed that 128-bit memory casts and float4 arithmetic preserve IEEE-754 precision identically."),
        ("Stream Pipelining Integrity", "Verified that dividing the dataset into chunks and streaming asynchronously did not introduce any race conditions, partial overwrites, or out-of-order errors."),
        ("Sample Inspection", "Sample indices [0..4] confirmed exact matching outputs (e.g., Input 3.00 -> Output 6.00; Input 4.00 -> Output 8.00)."),
        ("Result across all 25 runs", "ALL RUNS RETURNED: PASSED [100% CORRECTNESS VERIFIED].")
    ]
    for title, desc in v_items:
        p = vtf.add_paragraph()
        p.text = f"✔  {title}: {desc}"
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 13: SUMMARY OF CONTRIBUTIONS & CONCLUSION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, NAVY_DARK)
    add_header(s13, "Key Findings & Summary of Contributions")

    scards = [
        ("28.97x Kernel Speedup", "Demonstrated that GPU raw compute capability scales linearly from 2.04x at 1M to 28.97x at 50M elements.", GREEN_ACC),
        ("38.2x Vectorized Boost", "Vectorized float4 transactions increased memory bus saturation, achieving 66.2 GB/s effective bandwidth.", RGBColor(138, 43, 226)),
        ("PCIe Bottleneck Exposed", "Proved that synchronous CUDA wastes ~98% of time on serial PCIe bus transfers, limiting total speedup to ~0.58x.", RGBColor(239, 83, 80)),
        ("Pipelined Latency Hiding", "CUDA Stream pipelining cut total latency by > 54%, achieving a 1.27x net speedup over sequential CPU.", CYAN_ACC)
    ]

    for idx, (title, text, col) in enumerate(scards):
        row = idx // 2
        col_idx = idx % 2
        x = 0.8 + col_idx * 6.0
        y = 1.8 + row * 2.5
        box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(2.3))
        box.fill.solid()
        box.fill.fore_color.rgb = NAVY_CARD
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        btf = box.text_frame
        btf.word_wrap = True
        bp = btf.paragraphs[0]
        bp.text = title
        bp.font.size = Pt(16)
        bp.font.bold = True
        bp.font.color.rgb = col

        bp2 = btf.add_paragraph()
        bp2.text = text
        bp2.font.size = Pt(12)
        bp2.font.color.rgb = WHITE
        bp2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 14: THANK YOU & Q&A
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, NAVY_DARK)

    ty_box = s14.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.33), Inches(3.5))
    ty_tf = ty_box.text_frame
    ty_tf.word_wrap = True

    p = ty_tf.paragraphs[0]
    p.text = "Thank You!"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACC
    p.alignment = PP_ALIGN.CENTER

    p2 = ty_tf.add_paragraph()
    p2.text = "Questions & Discussion"
    p2.font.size = Pt(22)
    p2.font.color.rgb = WHITE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(12)

    p3 = ty_tf.add_paragraph()
    p3.text = "Presented by: Joel Biju, Mehak Sayed Yusuf, Akshay Bhat, Vageesh Mathad\nParallel & GPU Computing (PGC)"
    p3.font.size = Pt(14)
    p3.font.color.rgb = LIGHT_GRAY
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(20)

    prs.save(output_path)
    print(f"Presentation saved successfully at: {output_path}")

if __name__ == "__main__":
    create_deck()
