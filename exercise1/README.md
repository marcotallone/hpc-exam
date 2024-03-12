# High Performance Computing Exam

### UniTs, 2023 - 2024

### March 2024

***

## Student's Info

| Name | Surname | Student ID | UniTs mail | Google mail | Master |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Marco | Tallone | SM3600002 | `marco.tallone@studenti.units.it` | `marcotallone85@gmail.com` | SDIC |


## Documentation

### Repository Structure

The repository is organized in the following way:

```bash
.
├── apps # Python apps and usage examples
│   └── examples.py
├── convert # Python scripts to convert collected data
│   └── ...
├── datasets # Collected data csv files
│   └── ...
├── jobs # Slurm job scripts
│   └── ...
├── notebooks # Jupyter notebooks for data analysis
│   └── ...
├── README.md # This file
├── report.pdf # Report document
├── setup.py # Setup file for the epyc module
└── src # Python module
```

### Contents and Features

This repository contains collected data and implemented models for the latency predictions of the `broadcast` and `reduce` MPI collective operations as part of the exam for the High Performance Computing course at the University of Trieste.\
The data are available in the `datasets/` folder and have been colected on the ORFEO cluster at AREA Science Park in Trieste using `EPYC` nodes.\
The repository then contains a Python module named `epyc` which is a collection of classes and methods that allows the user to simulate MPI core allocation on a real EPYC machine. The module, in fact, allows to create `Node` objects and to initialize a certain number of processes on them according to different mapping policies, as done by the `map-by` option of the `mpirun` command.\
The module is also able to simulate the latency of the `broadcast` and `reduce` collective operations on the `EPYC` nodes, using the data collected on the ORFEO cluster. The latency is predicted based on a point-to-point communication model. Further details on the model details are available on the report in this repository.\
The module also offers few utility functions to plot and to perform statistical analysis on the collected data collected for the latencies.\
The majority of the implemented functions and classes are documented, hence further info about inputs and usage can be obtained with the `help` function in Python.\
Some usage examples can be found in the `apps/` folder or in the Jupiter notebooks in the `notebooks/` folder.

### Installation

The module comes with a `setup.py` file in the root directory, hence it can be installed with the following command:

```bash
pip install -e .
```
from the root directory of the project.
After that, the module can be imported in any Python script or notebook with the following command:

```python
import epyc
```

Or, alternatively to also use the utilities functions one can import:

```python
from epyc import *
from utils import *
```

Alternatively the modules can be used by manually updating the `PYTHONPATH` environment before running the scripts or notebooks.

### Usage

The `example.py` script in the `apps/` folder contains some usage examples of the implemented classes and methods. The script can be run with the following command:

```bash
python apps/examples.py
```

from the root directory. Running the script will produce the following output:
    
```terminal
Now these nodes are empty:

Node 0:
┌──────────────────┐  ┌──────────────────┐
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
└──────────────────┘  └──────────────────┘

Node 1:
┌──────────────────┐  ┌──────────────────┐
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
└──────────────────┘  └──────────────────┘
Now we initialize the nodes with 2 processes each and mapby node:

Node 0:
┌──────────────────┐  ┌──────────────────┐
│ ✅⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
└──────────────────┘  └──────────────────┘

Node 1:
┌──────────────────┐  ┌──────────────────┐
│ ✅⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
│ ⬛⬛⬛⬛⬛⬛⬛⬛ │  │ ⬛⬛⬛⬛⬛⬛⬛⬛ │
└──────────────────┘  └──────────────────┘
Now we re-allocate the processes with socket mapping and going up to 132 processes
Let's see where each process is:

Node 0:
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│   0   2   4   6   8  10  12  14 │  │   1   3   5   7   9  11  13  15 │
│  16  18  20  22  24  26  28  30 │  │  17  19  21  23  25  27  29  31 │
│  32  34  36  38  40  42  44  46 │  │  33  35  37  39  41  43  45  47 │
│  48  50  52  54  56  58  60  62 │  │  49  51  53  55  57  59  61  63 │
│  64  66  68  70  72  74  76  78 │  │  65  67  69  71  73  75  77  79 │
│  80  82  84  86  88  90  92  94 │  │  81  83  85  87  89  91  93  95 │
│  96  98 100 102 104 106 108 110 │  │  97  99 101 103 105 107 109 111 │
│ 112 114 116 118 120 122 124 126 │  │ 113 115 117 119 121 123 125 127 │
└─────────────────────────────────┘  └─────────────────────────────────┘

Node 1:
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│ 128 130                         │  │ 129 131                         │
│                                 │  │                                 │
│                                 │  │                                 │
│                                 │  │                                 │
│                                 │  │                                 │
│                                 │  │                                 │
│                                 │  │                                 │
│                                 │  │                                 │
└─────────────────────────────────┘  └─────────────────────────────────┘
We now re-allocated the node filling them completely with 256 processes and mapby core
In fact here is their status:

Node 0:
┌──────────────────┐  ┌──────────────────┐
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
└──────────────────┘  └──────────────────┘
Active cores:	128 / 128
Empty cores:	0 /128
Active sockets:	2 / 2
Empty sockets:	0 / 2

Node 1:
┌──────────────────┐  ┌──────────────────┐
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
│ ✅✅✅✅✅✅✅✅ │  │ ✅✅✅✅✅✅✅✅ │
└──────────────────┘  └──────────────────┘
Active cores:	128 / 128
Empty cores:	0 /128
Active sockets:	2 / 2
Empty sockets:	0 / 2
We can simulate different collective operations seeing their latency, for instance here for a message size of 1B:
	 - linear broadcast latency: 50.573211704623475 us
	 - chain broadcast latency: 55.030291447907615 us
	 - binary broadcast latency: 11.795976127944595 us
	 - linear reduce latency: 0.29013244483611006 us
	 - chain reduce latency: 34.846116497184674 us
	 - binary reduce latency: 1.785089908861254 us
```