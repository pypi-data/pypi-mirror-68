#define CUDA_API_PER_THREAD_DEFAULT_STREAM

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdio.h>
#include <iostream>
#include <assert.h>
#include <chrono>  // for high_resolution_clock

#include "cpu_solver.h"
#include "gpu_solver.cuh"
#include "utils.h"

void dry_run(int N){

        std::cout << "######################################################" << std::endl;
        std::cout << "A quick test to evaluate overall functionality and performance" << std::endl;
        std::cout << "######################################################" << std::endl;

        int testruns = 10;

        float *A, *B, *C, *D, *E;
        float *min;

        // host malloc

        checkCuda(cudaMallocHost((void**)&A, N * sizeof(float))); // host pinned
        checkCuda(cudaMallocHost((void**)&B, N * sizeof(float))); // host pinned
        checkCuda(cudaMallocHost((void**)&C, N * sizeof(float))); // host pinned
        checkCuda(cudaMallocHost((void**)&D, N * sizeof(float))); // host pinned
        checkCuda(cudaMallocHost((void**)&E, N * sizeof(float))); // host pinned

        checkCuda(cudaMallocHost((void**)&min, N * sizeof(float))); // host pinned

        memset(min, 0, N * sizeof(float));

        std::cout << "generating data..." << std::endl;

        generate_data(N, -100, 100, A);
        generate_data(N, -100, 100, B);
        generate_data(N, -100, 100, C);
        generate_data(N, -100, 100, D);
        generate_data(N, -100, 100, E);

        for (int i = 0; i < N; i++) {
                if (A[i] == 0) { A[i] = 1; } // done to avoid undefined behaviour in solver when A=0
        }

        std::cout << "done!" << std::endl;

        float dur = 0;
        float milliseconds = 0;
        float avg_cpu = 0;
        float avg = 0;

        std::cout << "####################### CPU ##########################" << std::endl;
        std::cout << "######################################################" << std::endl;
        std::cout << "######################################################" << std::endl;

        for (int k = 0; k < testruns; ++k) {
                auto pstart = std::chrono::high_resolution_clock::now();

                QuarticMinimumCPU(N, A, B, C, D, E, min);

                auto finish = std::chrono::high_resolution_clock::now();
                std::chrono::duration<float> elapsed = finish - pstart;
                dur = elapsed.count() * 1000;
                printf("Time (ms): %f\n", dur);
                avg_cpu += dur;
        }

        printf("min[0]: %f \n",min[0]);
        printf("avgTime (ms): %f\n", avg_cpu / testruns);

        memset(min, 0, N * sizeof(float));

        avg = 0;

        std::cout << "####################### GPU (no streams) #############" << std::endl;
        std::cout << "######################################################" << std::endl;
        std::cout << "######################################################" << std::endl;

        cudaEvent_t start, stop;
        cudaEventCreate(&start);
        cudaEventCreate(&stop);

        for (int k = 0; k < testruns; ++k) {

                cudaEventRecord(start);

                QuarticMinimumGPU(N, A, B, C, D, E, min);

                cudaEventRecord(stop);

                cudaEventSynchronize(stop);
                milliseconds = 0;
                cudaEventElapsedTime(&milliseconds, start, stop);
                printf("Time (ms): %f\n", milliseconds);
                avg += milliseconds;
        }

        printf("min[0]: %f \n",min[0]);
        printf("avgTime (ms): %f\n", avg / testruns);

        avg = 0;

        std::cout << "####################### GPU (streams) ################" << std::endl;
        std::cout << "######################################################" << std::endl;
        std::cout << "######################################################" << std::endl;

        cudaEventCreate(&start);
        cudaEventCreate(&stop);

        for (int k = 0; k < testruns; ++k) {

                cudaEventRecord(start);

                QuarticMinimumGPUStreams(N, A, B, C, D, E, min);

                cudaEventRecord(stop);

                cudaEventSynchronize(stop);
                milliseconds = 0;
                cudaEventElapsedTime(&milliseconds, start, stop);
                printf("Time (ms): %f\n", milliseconds);
                avg += milliseconds;
        }

        printf("min[0]: %f \n",min[0]);
        printf("avgTime (ms): %f\n", avg / testruns);

        std::cout << "######################################################" << std::endl;
        std::cout << "######################################################" << std::endl;

        printf("Speedup Tcpu/Tgpu: %f \n", avg_cpu / avg);
}


int main(void)
{
        int N = (1 << 20);
        std::cout << "N = " << N << std::endl;
        dry_run(N);

}
