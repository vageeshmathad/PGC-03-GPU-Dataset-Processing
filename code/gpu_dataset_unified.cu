/**
 * ============================================================================
 * Project: PGC-03 GPU Dataset Processing using CUDA (Enhanced Edition)
 * Team Members:
 *   - Joel Biju        (01FE24BCI021)
 *   - Mehak Sayed Yusuf(01FE24BCI012)
 *   - Akshay Bhat      (01FE24BCI024)
 *   - Vageesh Mathad   (01FE24BCI008)
 * 
 * Target Architecture: NVIDIA GPU (Turing / Quadro T2000 Max-Q)
 * Description:
 *   Comprehensive benchmark comparing:
 *     1. Sequential CPU execution
 *     2. OpenMP Multi-threaded CPU execution
 *     3. Standard CUDA Kernel execution
 *     4. Vectorized float4 CUDA Kernel execution
 *   Includes end-to-end PCIe transfer timings, verification, and effective bandwidth.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <chrono>
#include <cmath>

#ifndef DATA_SIZE
#define DATA_SIZE 10000000 // Default 10M elements if not specified
#endif

#define BLOCK_SIZE 256

// ----------------------------------------------------------------------------
// 1. Standard Element-wise CUDA Kernel
// ----------------------------------------------------------------------------
__global__ void processDataStandard(const float *input, float *output, int n)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
    {
        output[i] = input[i] * 2.0f;
    }
}

// ----------------------------------------------------------------------------
// 2. Vectorized float4 CUDA Kernel (Loads/stores 128 bits per thread)
// ----------------------------------------------------------------------------
__global__ void processDataVectorized(const float4 *input, float4 *output, int numFloat4)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < numFloat4)
    {
        float4 in = input[i];
        float4 out;
        out.x = in.x * 2.0f;
        out.y = in.y * 2.0f;
        out.z = in.z * 2.0f;
        out.w = in.w * 2.0f;
        output[i] = out;
    }
}

int main(int argc, char **argv)
{
    int N = DATA_SIZE;
    if (argc > 1)
    {
        N = atoi(argv[1]);
        if (N <= 0) N = DATA_SIZE;
    }

    size_t size = N * sizeof(float);

    printf("================================================================\n");
    printf(" PGC-03: ADVANCED GPU DATASET PROCESSING USING CUDA\n");
    printf(" Team: Joel Biju, Mehak Sayed Yusuf, Akshay Bhat, Vageesh Mathad\n");
    printf("================================================================\n");
    printf("Dataset Size         : %d elements (%.2f MB)\n", N, (double)size / (1024.0 * 1024.0));
    printf("CUDA Block Size      : %d threads\n", BLOCK_SIZE);

    // Host memory allocation
    float *h_input       = (float *)malloc(size);
    float *h_output_seq  = (float *)malloc(size);
    float *h_output_omp  = (float *)malloc(size);
    float *h_output_gpu  = (float *)malloc(size);
    float *h_output_vec  = (float *)malloc(size);

    if (!h_input || !h_output_seq || !h_output_omp || !h_output_gpu || !h_output_vec)
    {
        fprintf(stderr, "Host memory allocation failed!\n");
        return 1;
    }

    // Dataset generation
    for (int i = 0; i < N; i++)
    {
        h_input[i] = (float)(i % 1000);
    }

    // ------------------------------------------------------------------------
    // Benchmark 1: Sequential CPU Processing
    // ------------------------------------------------------------------------
    auto cpuSeqStart = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; i++)
    {
        h_output_seq[i] = h_input[i] * 2.0f;
    }
    auto cpuSeqEnd = std::chrono::high_resolution_clock::now();
    double cpuSeqTime = std::chrono::duration<double, std::milli>(cpuSeqEnd - cpuSeqStart).count();

    // ------------------------------------------------------------------------
    // Benchmark 2: OpenMP Multi-threaded CPU Processing
    // ------------------------------------------------------------------------
    auto cpuOmpStart = std::chrono::high_resolution_clock::now();
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < N; i++)
    {
        h_output_omp[i] = h_input[i] * 2.0f;
    }
    auto cpuOmpEnd = std::chrono::high_resolution_clock::now();
    double cpuOmpTime = std::chrono::duration<double, std::milli>(cpuOmpEnd - cpuOmpStart).count();

    // ------------------------------------------------------------------------
    // Benchmark 3: Standard CUDA Execution
    // ------------------------------------------------------------------------
    float *d_input, *d_output;
    cudaMalloc((void **)&d_input, size);
    cudaMalloc((void **)&d_output, size);

    cudaEvent_t totalStart, totalStop, kernelStart, kernelStop;
    cudaEventCreate(&totalStart);
    cudaEventCreate(&totalStop);
    cudaEventCreate(&kernelStart);
    cudaEventCreate(&kernelStop);

    cudaEventRecord(totalStart);

    // Host -> Device transfer
    cudaMemcpy(d_input, h_input, size, cudaMemcpyHostToDevice);

    int gridSize = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;

    // Kernel execution
    cudaEventRecord(kernelStart);
    processDataStandard<<<gridSize, BLOCK_SIZE>>>(d_input, d_output, N);
    cudaEventRecord(kernelStop);
    cudaEventSynchronize(kernelStop);

    float kernelTime = 0.0f;
    cudaEventElapsedTime(&kernelTime, kernelStart, kernelStop);

    // Device -> Host transfer
    cudaMemcpy(h_output_gpu, d_output, size, cudaMemcpyDeviceToHost);

    cudaEventRecord(totalStop);
    cudaEventSynchronize(totalStop);

    float totalCudaTime = 0.0f;
    cudaEventElapsedTime(&totalCudaTime, totalStart, totalStop);

    // ------------------------------------------------------------------------
    // Benchmark 4: Vectorized float4 CUDA Execution
    // ------------------------------------------------------------------------
    float vecKernelTime = 0.0f;
    if (N % 4 == 0)
    {
        int numFloat4 = N / 4;
        int vecGridSize = (numFloat4 + BLOCK_SIZE - 1) / BLOCK_SIZE;

        cudaEventRecord(kernelStart);
        processDataVectorized<<<vecGridSize, BLOCK_SIZE>>>(
            (const float4 *)d_input, (float4 *)d_output, numFloat4);
        cudaEventRecord(kernelStop);
        cudaEventSynchronize(kernelStop);
        cudaEventElapsedTime(&vecKernelTime, kernelStart, kernelStop);

        cudaMemcpy(h_output_vec, d_output, size, cudaMemcpyDeviceToHost);
    }

    // ------------------------------------------------------------------------
    // Verification
    // ------------------------------------------------------------------------
    bool passedStandard = true;
    bool passedVectorized = (N % 4 == 0);

    for (int i = 0; i < N; i++)
    {
        if (std::abs(h_output_seq[i] - h_output_gpu[i]) > 1e-4f)
        {
            passedStandard = false;
            break;
        }
        if (passedVectorized && std::abs(h_output_seq[i] - h_output_vec[i]) > 1e-4f)
        {
            passedVectorized = false;
        }
    }

    // Bandwidth calculation (Read + Write = 2 * size in bytes)
    double transferBytes = 2.0 * size;
    double kernelBandwidthGBs = (transferBytes / (kernelTime / 1000.0)) / 1e9;
    double vecBandwidthGBs = (transferBytes / (vecKernelTime / 1000.0)) / 1e9;

    printf("\n--- Performance Timings ---\n");
    printf("1. CPU Sequential Time    : %.4f ms\n", cpuSeqTime);
    printf("2. CPU OpenMP Multi-core  : %.4f ms (%.2fx vs Sequential)\n", cpuOmpTime, cpuSeqTime / cpuOmpTime);
    printf("3. CUDA Kernel Time       : %.4f ms\n", kernelTime);
    printf("4. Total CUDA Time        : %.4f ms (PCIe overhead: %.2f%%)\n", 
           totalCudaTime, ((totalCudaTime - kernelTime) / totalCudaTime) * 100.0);
    if (N % 4 == 0)
    {
        printf("5. Vectorized float4 Time : %.4f ms\n", vecKernelTime);
    }

    printf("\n--- Speedup Metrics ---\n");
    printf("Kernel Speedup (Compute)  : %.2fx\n", cpuSeqTime / kernelTime);
    printf("Total Speedup (End-to-End): %.2fx\n", cpuSeqTime / totalCudaTime);
    if (N % 4 == 0)
    {
        printf("Vectorized vs Standard K. : %.2fx speedup\n", kernelTime / vecKernelTime);
    }

    printf("\n--- Memory Throughput ---\n");
    printf("Effective Kernel Bandwidth: %.2f GB/s\n", kernelBandwidthGBs);
    if (N % 4 == 0)
    {
        printf("Vectorized float4 Bandw.  : %.2f GB/s\n", vecBandwidthGBs);
    }

    printf("\n--- Correctness Verification ---\n");
    printf("Standard CUDA Result      : %s\n", passedStandard ? "PASSED [OK]" : "FAILED [ERROR]");
    if (N % 4 == 0)
    {
        printf("Vectorized CUDA Result    : %s\n", passedVectorized ? "PASSED [OK]" : "FAILED [ERROR]");
    }

    printf("\nSample Outputs:\n");
    for (int i = 0; i < 5; i++)
    {
        printf("  Input[%d] = %6.2f | GPU Standard[%d] = %6.2f\n", 
               i, h_input[i], i, h_output_gpu[i]);
    }
    printf("================================================================\n");

    // Clean up
    cudaFree(d_input);
    cudaFree(d_output);
    free(h_input);
    free(h_output_seq);
    free(h_output_omp);
    free(h_output_gpu);
    free(h_output_vec);
    cudaEventDestroy(totalStart);
    cudaEventDestroy(totalStop);
    cudaEventDestroy(kernelStart);
    cudaEventDestroy(kernelStop);

    return (passedStandard ? 0 : 1);
}
