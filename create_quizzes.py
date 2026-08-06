import os
import json

template_path = 'Week 2 - System Design and Memory/Week_2_Quiz.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

def create_quiz(week_num, week_dir, topic, questions):
    # Fix titles
    content = template.replace('Week 2 Quiz: System Design and Networking', f'Week {week_num} Quiz: {topic}')
    content = content.replace('Week 2 Quiz</h1>', f'Week {week_num} Quiz</h1>')
    content = content.replace('Test your understanding of System Design and Networking', f'Test your understanding of {topic}')
    content = content.replace('Week_2_Student_Notes.html', f'Week_{week_num}_Student_Notes.html')
    
    start_str = "const questions = ["
    end_str = "];\n\n        let score = 0;"
    
    parts1 = content.split(start_str)
    parts2 = parts1[1].split(end_str)
    
    new_questions = json.dumps(questions, indent=12)
    
    new_content = parts1[0] + "const questions = " + new_questions + end_str + parts2[1]
    
    out_path = os.path.join(week_dir, f'Week_{week_num}_Quiz.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Created {out_path}')

w1_q = [
    {
        "question": "What is the primary characteristic of the Von Neumann Architecture?",
        "options": ["Separate memory spaces for data and instructions.", "A single shared memory space for both data and instructions.", "A decentralized memory model without a central processing unit.", "Execution of multiple instruction streams simultaneously (MIMD)."],
        "correct": 1,
        "explanation": "Von Neumann architecture stores both the program instructions and the data in a single, unified memory space."
    },
    {
        "question": "What does the 'Memory Wall' refer to?",
        "options": ["The physical limit of how much RAM can be installed on a motherboard.", "The growing disparity between CPU speed and memory access latency.", "A firewall mechanism protecting system memory from unauthorized access.", "The maximum bandwidth limit of a PCIe bus."],
        "correct": 1,
        "explanation": "The Memory Wall describes the phenomenon where processor speeds increased much faster than memory access times, causing CPUs to frequently idle while waiting for data."
    },
    {
        "question": "In Flynn's Taxonomy, which category best describes modern GPUs?",
        "options": ["SISD", "SIMD", "MISD", "MIMD"],
        "correct": 1,
        "explanation": "GPUs are essentially SIMD (Single Instruction, Multiple Data) machines, executing the exact same mathematical operation simultaneously across thousands of data points."
    }
]

create_quiz(1, 'Week 1 - HPC Introduction and Architectures', 'HPC Introduction and Architectures', w1_q)

w5_q = [
    {
        "question": "What is the purpose of the High Performance Linpack (HPL) benchmark?",
        "options": ["To measure memory bandwidth.", "To measure disk I/O performance.", "To measure the peak floating-point computing power of a cluster.", "To test network latency."],
        "correct": 2,
        "explanation": "HPL solves a dense linear system of equations to measure the floating-point execution rate (FLOPs) of a cluster, and is the standard used for the Top500 list."
    },
    {
        "question": "What does STREAM benchmark specifically measure?",
        "options": ["Sustainable memory bandwidth.", "CPU clock speed.", "Storage read/write speeds.", "Network bisection bandwidth."],
        "correct": 0,
        "explanation": "STREAM is the industry standard for measuring sustained memory bandwidth (in GB/s) for simple vector kernels."
    },
    {
        "question": "Why is profiling important before attempting to optimize code?",
        "options": ["It increases the compilation speed.", "It identifies the 'hotspots' where the program spends the most time.", "It automatically parallelizes the code.", "It reduces the memory footprint."],
        "correct": 1,
        "explanation": "Profiling reveals where the application actually spends its time, allowing you to focus optimization efforts on the bottlenecks that matter most (Amdahl's Law)."
    }
]

create_quiz(5, 'Week 5 - Benchmarking and Tuning', 'Benchmarking and Tuning', w5_q)

w6_q = [
    {
        "question": "Which programming model relies on explicit message passing between distributed memory nodes?",
        "options": ["OpenMP", "CUDA", "MPI", "Pthreads"],
        "correct": 2,
        "explanation": "MPI (Message Passing Interface) is the standard for distributed memory systems, requiring explicit send and receive commands to move data between nodes."
    },
    {
        "question": "What does a 'Reduction' operation do in parallel programming?",
        "options": ["It reduces the number of threads to save power.", "It combines partial results from multiple processes into a single global result (e.g., sum, max).", "It compresses the data before sending it over the network.", "It reduces the precision of floating-point numbers to speed up calculation."],
        "correct": 1,
        "explanation": "A reduction takes an array of elements (distributed across processes) and combines them into a single value using a specific operation, like MPI_Reduce or OpenMP's reduction clause."
    },
    {
        "question": "What is the main difference between OpenMP and MPI?",
        "options": ["OpenMP is for distributed memory (across nodes), MPI is for shared memory (single node).", "OpenMP is for shared memory (single node), MPI is for distributed memory (across nodes).", "OpenMP is written in Python, MPI is written in C.", "OpenMP only works on GPUs."],
        "correct": 1,
        "explanation": "OpenMP uses threads within a single shared-memory node, while MPI uses independent processes that communicate over a network across distributed nodes."
    }
]

create_quiz(6, 'Week 6 - Parallel Programming', 'Parallel Programming', w6_q)
