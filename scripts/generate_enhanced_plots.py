#!/usr/bin/env python3
"""
generate_enhanced_plots.py
Generates publication-grade performance charts for the Enhanced GPU Dataset Processing project.
Team: Joel Biju, Mehak Sayed Yusuf, Akshay Bhat, Vageesh Mathad
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# Set clean styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

output_dir = r"c:\Users\vagee\OneDrive\Desktop\pgc project\PGC-03-Enhanced-GPU-Processing\results"
os.makedirs(output_dir, exist_ok=True)

datasets = ["1M", "5M", "10M", "20M", "50M"]
elements = [1_000_000, 5_000_000, 10_000_000, 20_000_000, 50_000_000]

# Measured Timings (ms)
cpu_seq_time       = [0.967, 4.724, 8.449, 17.427, 46.177]
cpu_omp_time       = [0.358, 1.431, 2.640,  5.281, 13.993]
cuda_kernel_time   = [0.473, 0.592, 0.698,  0.930,  1.594]
cuda_vec_time      = [0.364, 0.462, 0.529,  0.710,  1.208]
cuda_sync_total    = [2.218, 8.320, 16.268, 30.652, 80.050]
cuda_pipelined     = [1.250, 4.150,  7.920, 14.850, 36.500]

# Speedup Metrics vs CPU Sequential
speedup_kernel     = [seq / k for seq, k in zip(cpu_seq_time, cuda_kernel_time)]
speedup_vec        = [seq / v for seq, v in zip(cpu_seq_time, cuda_vec_time)]
speedup_omp        = [seq / o for seq, o in zip(cpu_seq_time, cpu_omp_time)]
speedup_sync_total = [seq / s for seq, s in zip(cpu_seq_time, cuda_sync_total)]
speedup_pipelined  = [seq / p for seq, p in zip(cpu_seq_time, cuda_pipelined)]

# -----------------------------------------------------------------------------
# Chart 1: Speedup Scaling Analysis
# -----------------------------------------------------------------------------
def plot_speedup():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    ax.plot(datasets, speedup_vec, marker='^', color='#8A2BE2', linewidth=2.5, markersize=8,
            label='Vectorized float4 GPU Kernel (Compute-Only)')
    ax.plot(datasets, speedup_kernel, marker='o', color='#2E7D32', linewidth=2.5, markersize=8,
            label='Standard CUDA GPU Kernel (Compute-Only)')
    ax.plot(datasets, speedup_omp, marker='d', color='#0288D1', linewidth=2.0, linestyle='-.', markersize=7,
            label='OpenMP Multi-Core CPU (8 Threads)')
    ax.plot(datasets, speedup_pipelined, marker='*', color='#FF8F00', linewidth=2.5, markersize=9,
            label='Pipelined CUDA Streams (Overlapped End-to-End)')
    ax.plot(datasets, speedup_sync_total, marker='s', color='#C62828', linewidth=2.2, linestyle='--', markersize=7,
            label='Synchronous CUDA (Baseline End-to-End)')

    # Baseline line (1.0x)
    ax.axhline(1.0, color='#37474F', linestyle=':', linewidth=1.5, alpha=0.8, label='CPU Sequential Baseline (1.0x)')

    # Annotate key data points
    ax.annotate(f"{speedup_vec[-1]:.1f}x", (datasets[-1], speedup_vec[-1]), textcoords="offset points", xytext=(0, 8), ha='center', fontweight='bold', color='#8A2BE2')
    ax.annotate(f"{speedup_kernel[-1]:.1f}x", (datasets[-1], speedup_kernel[-1]), textcoords="offset points", xytext=(0, -15), ha='center', fontweight='bold', color='#2E7D32')
    ax.annotate(f"{speedup_pipelined[-1]:.2f}x", (datasets[-1], speedup_pipelined[-1]), textcoords="offset points", xytext=(0, 8), ha='center', fontweight='bold', color='#FF8F00')
    ax.annotate(f"{speedup_sync_total[-1]:.2f}x", (datasets[-1], speedup_sync_total[-1]), textcoords="offset points", xytext=(0, -15), ha='center', fontweight='bold', color='#C62828')

    ax.set_title("Comprehensive Speedup Scaling: CPU vs. Standard vs. Pipelined CUDA", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Dataset Size (Elements)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Speedup Relative to CPU Sequential (x)", fontsize=11, fontweight='bold')
    ax.legend(loc='upper left', frameon=True, fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    path = os.path.join(output_dir, "speedup_analysis.png")
    plt.savefig(path)
    plt.close()
    print(f"Generated: {path}")

# -----------------------------------------------------------------------------
# Chart 2: Execution Time Breakdown
# -----------------------------------------------------------------------------
def plot_execution_times():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    x = np.arange(len(datasets))
    width = 0.16

    ax.bar(x - 2*width, cpu_seq_time, width, label='CPU Sequential', color='#78909C')
    ax.bar(x - width, cpu_omp_time, width, label='CPU OpenMP (Multi-Core)', color='#42A5F5')
    ax.bar(x, cuda_kernel_time, width, label='CUDA Kernel (Compute)', color='#66BB6A')
    ax.bar(x + width, cuda_pipelined, width, label='CUDA Pipelined Streams (Total)', color='#FFA726')
    ax.bar(x + 2*width, cuda_sync_total, width, label='CUDA Synchronous (Total)', color='#EF5350')

    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontweight='bold')
    ax.set_title("Execution Time Comparison Across Implementations (ms)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Dataset Size", fontsize=11, fontweight='bold')
    ax.set_ylabel("Execution Time (Milliseconds) - Log Scale", fontsize=11, fontweight='bold')
    ax.set_yscale('log')
    ax.legend(loc='upper left', frameon=True, fontsize=10)
    ax.grid(True, which="both", ls="--", alpha=0.4)

    plt.tight_layout()
    path = os.path.join(output_dir, "execution_time_breakdown.png")
    plt.savefig(path)
    plt.close()
    print(f"Generated: {path}")

# -----------------------------------------------------------------------------
# Chart 3: Memory Bandwidth & Compute Throughput
# -----------------------------------------------------------------------------
def plot_bandwidth():
    # Bandwidth in GB/s: (2 * N * 4 bytes) / (kernel_time_seconds) / 1e9
    bw_standard = [(2.0 * n * 4.0 / (k / 1000.0)) / 1e9 for n, k in zip(elements, cuda_kernel_time)]
    bw_vec      = [(2.0 * n * 4.0 / (v / 1000.0)) / 1e9 for n, v in zip(elements, cuda_vec_time)]

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    
    ax.plot(datasets, bw_vec, marker='^', color='#8A2BE2', linewidth=2.5, markersize=8,
            label='Vectorized float4 GPU Kernel Bandwidth')
    ax.plot(datasets, bw_standard, marker='o', color='#00897B', linewidth=2.5, markersize=8,
            label='Standard CUDA GPU Kernel Bandwidth')

    # Quadro T2000 Peak Bandwidth reference line (~112 GB/s)
    ax.axhline(112.0, color='#E53935', linestyle='--', linewidth=1.5, alpha=0.8,
               label='Quadro T2000 Theoretical Peak VRAM Bandwidth (112 GB/s)')
    # PCIe 3.0 x16 Practical Peak (~12.5 GB/s)
    ax.axhline(12.5, color='#F57C00', linestyle=':', linewidth=1.5, alpha=0.8,
               label='PCIe Gen3 x16 Bus Limit (~12.5 GB/s)')

    for i, (b_std, b_v) in enumerate(zip(bw_standard, bw_vec)):
        ax.annotate(f"{b_v:.1f} GB/s", (datasets[i], b_v), textcoords="offset points", xytext=(0, 8), ha='center', fontweight='bold', color='#8A2BE2')
        ax.annotate(f"{b_std:.1f} GB/s", (datasets[i], b_std), textcoords="offset points", xytext=(0, -15), ha='center', fontweight='bold', color='#00897B')

    ax.set_title("Effective Memory Bandwidth (GB/s): Standard vs. Vectorized float4", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Dataset Size (Elements)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Effective Bandwidth (GB/s)", fontsize=11, fontweight='bold')
    ax.set_ylim(0, 125)
    ax.legend(loc='lower right', frameon=True, fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    path = os.path.join(output_dir, "memory_bandwidth_throughput.png")
    plt.savefig(path)
    plt.close()
    print(f"Generated: {path}")

# -----------------------------------------------------------------------------
# Chart 4: Stream Pipelining Timeline Diagram
# -----------------------------------------------------------------------------
def plot_pipeline_diagram():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), dpi=300)

    # Subplot 1: Synchronous Model
    ax1.set_title("Synchronous CUDA Baseline: Strict Sequential Serialization (High Idle Overhead)", fontsize=11, fontweight='bold', pad=8)
    ax1.barh(["Timeline"], [35], left=[0], color='#E57373', edgecolor='black', label='Host-to-Device Copy (PCIe)')
    ax1.barh(["Timeline"], [5], left=[35], color='#81C784', edgecolor='black', label='Kernel Execution (GPU Compute)')
    ax1.barh(["Timeline"], [35], left=[40], color='#64B5F6', edgecolor='black', label='Device-to-Host Copy (PCIe)')
    ax1.text(17.5, 0, "cudaMemcpy (H2D)\n~38 ms", ha='center', va='center', fontweight='bold', color='white')
    ax1.text(37.5, 0, "Kernel\n1.6ms", ha='center', va='center', fontweight='bold', color='black', fontsize=8)
    ax1.text(57.5, 0, "cudaMemcpy (D2H)\n~38 ms", ha='center', va='center', fontweight='bold', color='white')
    ax1.set_xlim(0, 80)
    ax1.set_xlabel("Total Execution Time: ~80 ms (GPU Compute Engine Idle ~98% of the time)", fontsize=10, fontweight='bold', color='#C62828')
    ax1.legend(loc='upper right', fontsize=8)

    # Subplot 2: Asynchronous Pipelined Model (4 Streams)
    ax2.set_title("Enhanced CUDA Streams: Overlapped Memory Transfers & Computation (Hiding PCIe Latency)", fontsize=11, fontweight='bold', pad=8)
    streams = ["Stream 4", "Stream 3", "Stream 2", "Stream 1"]
    
    # Offsets and durations for 4 streams
    h2d_duration = 9
    k_duration = 2
    d2h_duration = 9

    for s_idx, s_name in enumerate(reversed(streams)):
        start = s_idx * 7
        ax2.barh([s_name], [h2d_duration], left=[start], color='#E57373', edgecolor='black')
        ax2.barh([s_name], [k_duration], left=[start + h2d_duration], color='#81C784', edgecolor='black')
        ax2.barh([s_name], [d2h_duration], left=[start + h2d_duration + k_duration], color='#64B5F6', edgecolor='black')
        ax2.text(start + h2d_duration/2, s_idx, "H2D", ha='center', va='center', fontsize=7, color='white', fontweight='bold')
        ax2.text(start + h2d_duration + k_duration/2, s_idx, "K", ha='center', va='center', fontsize=7, color='black', fontweight='bold')
        ax2.text(start + h2d_duration + k_duration + d2h_duration/2, s_idx, "D2H", ha='center', va='center', fontsize=7, color='white', fontweight='bold')

    ax2.set_xlim(0, 80)
    ax2.set_xlabel("Total Pipelined Time: ~36.5 ms (Overlapped Execution Cuts Total Latency by > 54%!)", fontsize=10, fontweight='bold', color='#2E7D32')

    plt.tight_layout()
    path = os.path.join(output_dir, "cuda_stream_pipelining.png")
    plt.savefig(path)
    plt.close()
    print(f"Generated: {path}")

if __name__ == "__main__":
    plot_speedup()
    plot_execution_times()
    plot_bandwidth()
    plot_pipeline_diagram()
    print("All enhanced visualization charts successfully created!")
