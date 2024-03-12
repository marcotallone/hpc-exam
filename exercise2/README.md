# High Performance Computing Exam

### UniTs, 2023 - 2024

### March 2024

***

## Student's Info

| Name | Surname | Student ID | UniTs mail | Google mail | Master |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Marco | Tallone | SM3600002 | `marco.tallone@studenti.units.it` | `marcotallone85@gmail.com` | SDIC |

## Documentation

### Project's organization

The project is organized with the following structure:

```bash
.
├── apps # Ready-to-use scripts
│   └── main.c
├── datasets # Datasets with scaling data
├── include # Include headers
│   └── qsort.h
├── python # Python scripts for plotting and analysis
│   ├── utils
│   └── scaling.ipynb
├── report.pdf # Report of the project
├── README.md # This file
├── install.sh # Quick compilation and installation
├── mpi.job # MPI job script for Slurm
├── omp.job # OpenMP job script for Slurm
└── src # Source files
    └── qsort.c
```

### Usage

To be able to use the implemented library in a `C` script it's possible to import the `qsort.h` header file and link to the library at compilation time. Compilation details are explained below.

```c
#include "qsort.h"
```

In the `apps/` folder the `mpi_example.c` and `omp_example.c` files provide a starting point with some basic usage example of the implemented features.

### Implemented Quicksort Functions

This library implements different parallel versions of the Quicksort algorithm. The different algorithms have been implemented both in shared and distributed memory environments. Further detail about the implemented algorithm and the theory behind their implementation can be found in the provided report in the root directory of this folder.\
This file presents here the main characteristics of the implemented functions and explains their practical usage. The main implemented sorting functions are the folowing:

* `void serial_qsort(data_t *, int, int, compare_t)`: serial version of the quicksort algorithm. Takes in input the array to be sorted, the starting and ending index of the array and a comparison function to be used for sorting.

* `void omp_task_qsort(data_t *, int, int, compare_t)`: task-based parallel version using OpenMP. Takes in input the array to be sorted, the starting and ending index of the array and a comparison function to be used for sorting. This function requires to be used inside a parallel region as follows:
    ```c
    #pragma omp parallel
    {
      #pragma omp single
      {
        omp_task_qsort(array, 0, N, compare_f);
      }
    }
    ```

* `void omp_parallel_qsort(data_t *, int, int, compare_t, int)`: shared memory version of the quicksort algorithm using OpenMP. Takes in input the array to be sorted, the starting and ending index of the array, a comparison function to be used for sorting and the depth of the recursive call (First call 0). Can be normally used as any other function in the main script.

* `void omp_hyperquicksort(data_t *, int, int, compare_t, int)`: shared memory version of the hyperquicksort algorithm using OpenMP. Takes in input the array to be sorted, the starting and ending index of the array, a comparison function to be used for sorting and the depth of the recursive call (First call is 0).

* `void omp_psrs(data_t *, int, int, compare_t)`: shared memory version of the PSRS algorithm using OpenMP. Takes in input the array to be sorted, the starting and ending index of the array and a comparison function to be used for sorting.

* `void MPI_Parallel_qsort(data_t **, int *, int *, int, MPI_Comm, MPI_Datatype, compare_t)`: distributed memory version of the quicksort algorithm using MPI. This function must be called after `MPI_Initialize()` to enable communication between multiple processes. Takes in input the local array to be sorted, the size of the local array, the rank of the process, the number of processes, the MPI communicator, the MPI specific datatype of the array elements and a comparison function to be used for sorting.

* `void MPI_Hyperquicksort(data_t **, int *, int *, int, MPI_Comm, MPI_Datatype, compare_t)`: distributed memory version of the hyperquicksort algorithm using MPI. This function must be called after `MPI_Initialize()` to enable communication between multiple processes. Takes in input the local array to be sorted, the size of the local array, the rank of the process, the number of processes, the MPI communicator, the MPI specific datatype of the array elements and a comparison function to be used for sorting.

* `void MPI_PSRS(data_t **, int *, int, int, int, MPI_Datatype, compare_t)`: distributed memory version of the PSRS algorithm using MPI. This function must be called after `MPI_Initialize()` to enable communication between multiple processes. Takes in input the local array to be sorted, the size of the local array, the size of the global array, the rank of the process, the number of processes, the MPI communicator, the MPI specific datatype of the array elements and a comparison function to be used for sorting.

The serial and shared memory versions sort the input array in place directly without the need of any additional operation. The MPI versions require a the master process to initially split the input array in multiple chunks and to actually send the chunks to the different processes. The chunks are then sorted in place by the single processes. These can be merged by the master process at the end of the function execution to check for sorting correctness.
The `mpi_example.c` and `omp_example.c` script in the `apps/` folder show some usage examples.

### Compilation

Compilation of the implemented library is performed with the `cmake` system.\
By executing the following commands (and eventually specifying the correct `-DCMAKE_PREFIX_PATH` for eventual third party libraries if not found) all the `C` libraries will be compiled in the `build/` folder.

```bash
cmake -S . -B build/

make -C build/ -j<N> -D<COMPILATION_MODE>=ON
```

The library can be compiled in different modes. These includes the following:

* **serial** compilation: this will only compile the serial version of the library without any parallel algorithm.

* **openmp** compilation: this will compile the library with the OpenMP parallel algorithms, in order to enable this version compile with the option `-DOMP=ON`.

* **mpi** compilation: this will compile the complete library with the MPI parallel algorithms and also using OpenMP since these algorithm require it, in order to enable this version compile with the option `-DMPI=ON`.

All of these modes also include a debugging mode where no optimization is performed at compile time and some debugging flags are enabled. This can be enabled by adding the `-DDEBUG=ON` flag to the compilation command.
For a quick installation following this commands and `build.sh` script has been provided in the root folder. To compile more easily with this script you can pass the compile version you want as a command like argument. Accepted argument include `omp`, `mpi` or their debug versions `debug omp` and `debug mpi`.\
After compilation the executables can be found in the `build/bin/` folder. In order to add a personal executable to be compiled with the library you just need to update the `MAIN_FILES` list in the provided `CMakeLists.txt` file by directly editing the file.\
In the root directory of the project there are also 2 Slurm job to showcase how to compile and use the library on the ORFEO cluster. These will run a scaling test to asses strong and weak scalability of the implementations depending on the specified input. The results of the test will be appended on a relative `csv` file in the `datasets/` folder. It's possible to visualize the file with an editor of choice or by running the `display.c` program if compiled by the cmake system. Further details on the scaling tests can be found in the `mpi_scaling.c` and `omp_scaling.c` files.
