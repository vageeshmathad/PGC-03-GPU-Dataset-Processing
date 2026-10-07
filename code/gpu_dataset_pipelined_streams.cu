/**
 * ============================================================================
 * Project: PGC-03 GPU Dataset Processing - CUDA Streams & Pipelining
 * Team Members:
 *   - Joel Biju        (01FE24BCI021)
 *   - Mehak Sayed Yusuf(01FE24BCI012)
 *   - Akshay Bhat      (01FE24BCI024)
 *   - Vageesh Mathad   (01FE24BCI008)
 * 
 * Target Architecture: NVIDIA GPU (Turing / Quadro T2000 Max-Q)
 * Objective:
 *   Directly eliminates the 98% PCIe bus bottleneck identified in standard
 *   synchronous CUDA by overlapping Host-to-Device transfer, kernel execution,
 *   and Device-to-Host transfer using pinned host memory and asynchronous streams.
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>
#include <chrono>
#include <cmath>

#define NUM_STREAMS 4
#define BLOCK_SIZE 256

__global__ void processChunkKernel(const float *input, float *output, int n)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
    {
        output[i] = input[i] * 2.0f;
    }
}

int main(int argc, char **argv)
{
    int N = 50000000; // Default 50M
    if (argc > 1)
    {
        N = atoi(argv[1]);
        if (N <= 0) N = 50000000;
    }

    size_t totalBytes = N * sizeof(float);

    printf("================================================================\n");
    printf(" CUDA ASYNCHRONOUS STREAM PIPELINING BENCHMARK\n");
    printf(" Demonstrating PCIe Transfer Overlap & Latency Hiding\n");
    printf("================================================================\n");
    printf("Dataset Size         : %d elements (%.2f MB)\n", N, (double)totalBytes / (1024.0 * 1024.0));
    printf("Number of Streams    : %d\n", NUM_STREAMS);
    printf("Stream Chunk Size    : %d elements\n", N / NUM_STREAMS);

    // 1. Allocate PINNED (Page-Locked) Host Memory for direct DMA access
    float *h_input_pinned, *h_output_pinned;
    cudaMallocHost((void **)&h_input_pinned, totalBytes);
    cudaMallocHost((void **)&h_output_pinned, totalBytes);

    if (!h_input_pinned || !h_output_pinned)
    {
        fprintf(stderr, "Pinned host memory allocation failed!\n");
        return 1;
    }

    for (int i = 0; i < N; i++)
    {
        h_input_pinned[i] = (float)(i % 1000);
    }

    // Baseline CPU Sequential execution
    auto cpuStart = std::chrono::high_resolution_clock::now();
    float *cpu_verify = (float *)malloc(totalBytes);
    for (int i = 0; i < N; i++)
    {
        cpu_verify[i] = h_input_pinned[i] * 2.0f;
    }
    auto cpuEnd = std::chrono::high_resolution_clock::now();
    double cpuTime = std::chrono::duration<double, std::milli>(cpuEnd - cpuStart).count();

    // Device Memory
    float *d_input, *d_output;
    cudaMalloc((void **)&d_input, totalBytes);
    cudaMalloc((void **)&d_output, totalBytes);

    // Create CUDA Streams
    cudaStream_t streams[NUM_STREAMS];
    for (int s = 0; s < NUM_STREAMS; s++)
    {
        cudaStreamCreate(&streams[s]);
    }

    cudaEvent_t startEvent, stopEvent;
    cudaEventCreate(&startEvent);
    cudaEventCreate(&stopEvent);

    int chunkSize = N / NUM_STREAMS;
    size_t chunkBytes = chunkSize * sizeof(float);
    int gridChunk = (chunkSize + BLOCK_SIZE - 1) / BLOCK_SIZE;

    // ------------------------------------------------------------------------
    // Pipelined Asynchronous Execution
    // ------------------------------------------------------------------------
    cudaEventRecord(startEvent, 0);

    for (int s = 0; s < NUM_STREAMS; s++)
    {
        int offset = s * chunkSize;
        // Asynchronous H2D Transfer
        cudaMemcpyAsync(&d_input[offset], &h_input_pinned[offset], chunkBytes, 
                        cudaMemcpyHostToDevice, streams[s]);

        // Asynchronous Kernel Execution
        processChunkKernel<<<gridChunk, BLOCK_SIZE, 0, streams[s]>>>(
            &d_input[offset], &d_output[offset], chunkSize);

        // Asynchronous D2H Transfer
        cudaMemcpyAsync(&h_output_pinned[offset], &d_output[offset], chunkBytes, 
                        cudaMemcpyDeviceToHost, streams[s]);
    }

    // Wait for all streams to finish
    for (int s = 0; s < NUM_STREAMS; s++)
    {
        cudaStreamSynchronize(streams[s]);
    }

    cudaEventRecord(stopEvent, 0);
    cudaEventSynchronize(stopEvent);

    float pipelinedTime = 0.0f;
    cudaEventElapsedTime(&pipelinedTime, startEvent, stopEvent);

    // ------------------------------------------------------------------------
    // Verification
    // ------------------------------------------------------------------------
    bool passed = true;
    for (int i = 0; i < N; i++)
    {
        if (std::abs(cpu_verify[i] - h_output_pinned[i]) > 1e-4f)
        {
            passed = false;
            break;
        }
    }

    printf("\n--- Results ---\n");
    printf("CPU Baseline Time         : %.4f ms\n", cpuTime);
    printf("Pipelined Async CUDA Time : %.4f ms\n", pipelinedTime);
    printf("End-to-End Speedup        : %.2fx\n", cpuTime / pipelinedTime);
    printf("Verification Result       : %s\n", passed ? "PASSED [100% Match]" : "FAILED");
    printf("================================================================\n");

    // Clean up
    for (int s = 0; s < NUM_STREAMS; s++)
    {
        cudaStreamDestroy(streams[s]);
    }
    cudaFree(d_input);
    cudaFree(d_output);
    cudaFreeHost(h_input_pinned);
    cudaFreeHost(h_output_pinned);
    free(cpu_verify);
    cudaEventDestroy(startEvent);
    cudaEventDestroy(stopEvent);

    return 0;
}
