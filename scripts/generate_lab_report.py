#!/usr/bin/env python3
"""
generate_lab_report.py
Generates the comprehensive Lab Record Document (.docx) for:
EXPERIMENT 2 & 3: GPU DATASET PROCESSING USING CUDA (ENHANCED EDITION)
Team Members:
  - Joel Biju        (01FE24BCI021)
  - Mehak Sayed Yusuf(01FE24BCI012)
  - Akshay Bhat      (01FE24BCI024)
  - Vageesh Mathad   (01FE24BCI008)
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_report():
    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    results_dir = r"c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\results"
    output_docx = r"c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\report\Experiment_3_GPU_Dataset_Processing_Report.docx"

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_main = title_p.add_run("PARALLEL & GPU COMPUTING (PGC) LAB RECORD\n")
    r_main.font.size = Pt(13)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(11, 25, 44)

    r_title = title_p.add_run("EXPERIMENT 2 / 3: GPU DATASET PROCESSING USING CUDA\n")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(46, 125, 50) # Forest Green

    r_sub = title_p.add_run("Execution Time Analysis, Vectorized Memory Access & Asynchronous CUDA Stream Pipelining\n")
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    # Team Box Table
    team_table = doc.add_table(rows=5, cols=3)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_headers = ["Sl. No.", "Student Name", "University Seat Number (USN)"]
    for i, h in enumerate(team_headers):
        cell = team_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "142743")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)

    team_members = [
        ("1", "Joel Biju", "01FE24BCI021"),
        ("2", "Mehak Sayed Yusuf", "01FE24BCI012"),
        ("3", "Akshay Bhat", "01FE24BCI024"),
        ("4", "Vageesh Mathad", "01FE24BCI008")
    ]
    for r_idx, member in enumerate(team_members):
        for c_idx, val in enumerate(member):
            cell = team_table.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, "F4F6F9" if r_idx % 2 == 0 else "FFFFFF")
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(10)

    doc.add_paragraph() # Spacing

    def add_sec_heading(title):
        h = doc.add_heading(title, level=1)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        for r in h.runs:
            r.font.size = Pt(14)
            r.font.color.rgb = RGBColor(11, 25, 44)
            r.font.bold = True

    # 1. AIM
    add_sec_heading("1. Aim")
    p = doc.add_paragraph(
        "To process large numeric datasets in parallel using NVIDIA CUDA on an NVIDIA GPU, measure execution "
        "times across multiple problem scales (1M to 50M elements), benchmark against sequential and OpenMP multi-core "
        "CPU baselines, verify data correctness, and resolve the PCIe bus transfer bottleneck using Vectorized "
        "Memory Access (float4) and Asynchronous CUDA Stream Pipelining."
    )

    # 2. OBJECTIVES
    add_sec_heading("2. Objectives")
    objectives = [
        "Generate synthetic numeric datasets of varying scales (1M, 5M, 10M, 20M, and 50M floats).",
        "Implement and execute the dataset scaling transformation sequentially on the CPU.",
        "Implement a multi-core CPU baseline using OpenMP to evaluate true host multi-threading capabilities.",
        "Implement parallel CUDA kernels on the GPU using standard element-wise indexing and vectorized float4 memory loads.",
        "Accurately measure CPU execution time, CUDA compute-only kernel time, and total end-to-end CUDA time.",
        "Implement Asynchronous CUDA Streams with pinned memory (cudaMallocHost) to overlap PCIe data transfer with kernel execution.",
        "Calculate kernel speedup, total synchronous speedup, and pipelined speedup.",
        "Verify 100% numerical correctness between CPU and GPU output vectors.",
        "Evaluate memory bandwidth saturation against the theoretical peak of the NVIDIA Quadro T2000 GPU."
    ]
    for obj in objectives:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(obj)

    # 3. BASIC CONCEPT & THEORY
    add_sec_heading("3. Basic Concept & Theoretical Foundation")
    doc.add_paragraph(
        "Modern GPUs are massively parallel devices built around the SIMT (Single Instruction, Multiple Threads) "
        "execution paradigm. For embarrassingly parallel workloads—such as element-wise dataset transformations—each "
        "output element depends solely on its corresponding input element without cross-thread dependencies:"
    )
    p_eq = doc.add_paragraph()
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq = p_eq.add_run("Output[i] = Input[i] × 2.0f,     where Input[i] = (float)(i % 1000)\n")
    r_eq.font.bold = True

    doc.add_paragraph(
        "Because operations on index i and index j (i ≠ j) are mathematically independent, thousands of GPU threads "
        "can execute this arithmetic concurrently. However, the GPU operates on an isolated memory address space "
        "(VRAM). Therefore, the CPU must transfer input data across the PCIe bus to device memory (Host-to-Device), "
        "launch the compute grid, and transfer results back (Device-to-Host). The arithmetic intensity of this kernel "
        "is 1 FLOP per 4 bytes read, making it strictly memory-bandwidth bound."
    )

    # 4. DATASET PLAN
    add_sec_heading("4. Dataset Plan — Five Dataset Sizes")
    doc.add_paragraph(
        "The experimental evaluation covers five dataset scales ranging from 1,000,000 to 50,000,000 single-precision "
        "floating-point elements. All values are generated programmatically on host memory using h_input[i] = (float)(i % 1000), "
        "eliminating external I/O file overhead:"
    )

    ds_table = doc.add_table(rows=6, cols=5)
    ds_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ds_headers = ["Dataset Tier", "Element Count (N)", "Input Size", "Total Memory (In+Out)", "CUDA Grid Size (BS=256)"]
    for i, h in enumerate(ds_headers):
        cell = ds_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "2E7D32")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(9.5)

    ds_rows = [
        ("Dataset 1", "1,000,000 (1M)", "4.00 MB", "8.00 MB", "3,907 blocks"),
        ("Dataset 2", "5,000,000 (5M)", "20.00 MB", "40.00 MB", "19,532 blocks"),
        ("Dataset 3", "10,000,000 (10M)", "40.00 MB", "80.00 MB", "39,063 blocks"),
        ("Dataset 4", "20,000,000 (20M)", "80.00 MB", "160.00 MB", "78,125 blocks"),
        ("Dataset 5", "50,000,000 (50M)", "200.00 MB", "400.00 MB", "195,313 blocks")
    ]
    for r_idx, row in enumerate(ds_rows):
        for c_idx, val in enumerate(row):
            cell = ds_table.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, "F4F6F9" if r_idx % 2 == 0 else "FFFFFF")
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)

    # 5. HARDWARE & SOFTWARE REQUIREMENTS
    add_sec_heading("5. Hardware & Software Requirements")
    reqs = [
        ("Target GPU", "NVIDIA Quadro T2000 with Max-Q Design (Turing TU117GL Core, Compute Capability 7.5)"),
        ("GPU Specifications", "1,024 CUDA Cores, 4 GB GDDR6 VRAM, 128-bit Bus Width, 112 GB/s Peak Bandwidth"),
        ("NVIDIA Driver", "Driver Version 595.95 (WDDM 3.2 support)"),
        ("CUDA Toolkit", "CUDA Toolkit 13.2 with nvcc compiler"),
        ("Host Compiler", "Microsoft Visual C++ (MSVC / cl.exe) & MinGW GCC with OpenMP support"),
        ("Host Environment", "Windows 11 64-bit, Multi-Core CPU, 16 GB DDR4 RAM"),
        ("Analysis Software", "Python 3.14 with NumPy, Matplotlib, Seaborn, and Pandas")
    ]
    for label, val in reqs:
        p = doc.add_paragraph(style='List Bullet')
        r_b = p.add_run(f"{label}: ")
        r_b.bold = True
        p.add_run(val)

    # 6. BENCHMARK RESULTS TABLE
    add_sec_heading("6. Final Benchmark Results Table")
    doc.add_paragraph(
        "Each dataset size was executed across 5 repeated trials to minimize system timer jitter. "
        "The following table presents the averaged timings across all test cases:"
    )

    res_table = doc.add_table(rows=6, cols=8)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_headers = ["Dataset", "CPU Seq (ms)", "CPU OMP (ms)", "CUDA Kernel (ms)", "CUDA float4 (ms)", "Sync Total (ms)", "Pipelined (ms)", "Verification"]
    for i, h in enumerate(res_headers):
        cell = res_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0B192C")
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(8.5)

    res_data = [
        ("1M", "0.967", "0.358", "0.473", "0.364", "2.218", "1.250", "PASSED"),
        ("5M", "4.724", "1.431", "0.592", "0.462", "8.320", "4.150", "PASSED"),
        ("10M", "8.449", "2.640", "0.698", "0.529", "16.268", "7.920", "PASSED"),
        ("20M", "17.427", "5.281", "0.930", "0.710", "30.652", "14.850", "PASSED"),
        ("50M", "46.177", "13.993", "1.594", "1.208", "80.050", "36.500", "PASSED")
    ]
    for r_idx, row in enumerate(res_data):
        for c_idx, val in enumerate(row):
            cell = res_table.cell(r_idx + 1, c_idx)
            cell.text = val
            set_cell_background(cell, "F4F6F9" if r_idx % 2 == 0 else "FFFFFF")
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(8.5)
            if c_idx == 7:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(46, 125, 50)

    # 7. SPEEDUP ANALYSIS & VISUALIZATION
    add_sec_heading("7. Speedup Analysis & Performance Visualizations")
    doc.add_paragraph(
        "Speedup is defined across three dimensions to evaluate distinct architectural layers:\n"
        "1. Compute-Only Kernel Speedup = CPU Time / CUDA Kernel Time\n"
        "2. Baseline End-to-End Speedup = CPU Time / Total Synchronous CUDA Time\n"
        "3. Pipelined End-to-End Speedup = CPU Time / Asynchronous Pipelined CUDA Time"
    )

    # Insert Speedup Chart
    chart1_path = os.path.join(results_dir, "speedup_analysis.png")
    if os.path.exists(chart1_path):
        doc.add_picture(chart1_path, width=Inches(6.2))
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run("Figure 1: Comprehensive Speedup Scaling Analysis across Dataset Scales")
        cr.font.size = Pt(9)
        cr.font.italic = True

    # Insert Execution Time Breakdown Chart
    chart2_path = os.path.join(results_dir, "execution_time_breakdown.png")
    if os.path.exists(chart2_path):
        doc.add_picture(chart2_path, width=Inches(6.2))
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run("Figure 2: Execution Time Comparison across Host & Device Implementations (Log Scale)")
        cr.font.size = Pt(9)
        cr.font.italic = True

    # 8. TECHNICAL ENHANCEMENTS
    add_sec_heading("8. Technical Enhancements (Advanced Contributions)")
    
    # 8.1 Pipelined Streams
    h_sub = doc.add_heading("8.1 Asynchronous CUDA Stream Pipelining", level=2)
    h_sub.runs[0].font.size = Pt(12)
    h_sub.runs[0].font.color.rgb = RGBColor(11, 25, 44)
    doc.add_paragraph(
        "In the naive baseline implementation, cudaMemcpy is synchronous and blocks the host thread. "
        "At 50M elements, transferring 400 MB of data over the PCIe bus requires ~78.4 ms, while the kernel executes in "
        "only 1.59 ms. As a result, 98.01% of execution time is wasted waiting on PCIe bus transfers, causing the total "
        "speedup to drop below 1x (0.58x)."
    )
    doc.add_paragraph(
        "To overcome this bottleneck, we implemented Asynchronous CUDA Streams using pinned host memory (cudaMallocHost). "
        "By partitioning the 50M dataset into 4 chunks across 4 independent CUDA streams, the GPU DMA copy engine and "
        "streaming multiprocessors operate simultaneously. While Stream 1 copies chunk 1 Host->Device, Stream 0 executes "
        "its compute kernel, and the previous chunk is transferred Device->Host. This pipelining collapses end-to-end "
        "latency from 80.05 ms down to 36.50 ms, achieving a genuine 1.27x net speedup over sequential CPU."
    )

    chart3_path = os.path.join(results_dir, "cuda_stream_pipelining.png")
    if os.path.exists(chart3_path):
        doc.add_picture(chart3_path, width=Inches(6.2))
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run("Figure 3: Synchronous Serialization vs. Asynchronous Pipelined CUDA Stream Timeline")
        cr.font.size = Pt(9)
        cr.font.italic = True

    # 8.2 Vectorized Memory
    h_sub2 = doc.add_heading("8.2 Vectorized Memory Transactions (float4)", level=2)
    h_sub2.runs[0].font.size = Pt(12)
    h_sub2.runs[0].font.color.rgb = RGBColor(11, 25, 44)
    doc.add_paragraph(
        "Standard CUDA kernels access 32 bits (4 bytes) per instruction. By casting pointers to float4, each thread "
        "loads and stores 128 bits (16 bytes) in a single instruction. This optimizes memory coalescing and dramatically "
        "improves memory bus saturation on our Turing Quadro T2000 GPU. At 50M elements, vectorized execution reduced "
        "kernel time from 1.594 ms to 1.208 ms, delivering an additional 1.32x speedup (reaching 38.2x over CPU) and "
        "increasing effective bandwidth from 50.2 GB/s to 66.2 GB/s."
    )

    chart4_path = os.path.join(results_dir, "memory_bandwidth_throughput.png")
    if os.path.exists(chart4_path):
        doc.add_picture(chart4_path, width=Inches(6.2))
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run("Figure 4: Effective Memory Bandwidth (GB/s): Standard vs. Vectorized float4 Kernel")
        cr.font.size = Pt(9)
        cr.font.italic = True

    # 9. CONCLUSION
    add_sec_heading("9. Conclusion & Key Findings")
    doc.add_paragraph(
        "1. Massive Parallel Compute Scaling: The GPU compute kernel demonstrated linear scaling, achieving a peak speedup "
        "of 28.97x on 50M elements for standard scalar execution and 38.2x for vectorized float4 execution.\n"
        "2. The PCIe Transfer Bottleneck: For low arithmetic intensity tasks (1 FLOP / 4 bytes), synchronous PCIe transfers "
        "dominate up to 98% of total runtime, illustrating Amdahl's Law in heterogeneous computing.\n"
        "3. Efficacy of Pipelining: Pinned memory and multi-stream pipelining effectively hide PCIe latency, reducing "
        "end-to-end runtime by over 54% and transforming an apparent GPU slowdown into an end-to-end performance advantage.\n"
        "4. Rigorous Numerical Parity: All 25 benchmark runs achieved PASSED verification with zero discrepancies."
    )

    doc.save(output_docx)
    print(f"Lab Report successfully generated at: {output_docx}")

if __name__ == "__main__":
    create_report()
