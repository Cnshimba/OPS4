import os
import re
import json

folder = "Week 10 - HPC Applications"
quiz_path = os.path.join(folder, "Week_10_Quiz.html")

# Fresh 15 questions incorporating the new domains
w10_q = [
    {
        "question": "Which of the following scientific domains primarily uses OpenFOAM?",
        "options": ["Bioinformatics", "Computational Fluid Dynamics (CFD)", "Electronic Design Automation (EDA)", "Cyber Security"],
        "correct": 1,
        "explanation": "OpenFOAM is the premier open-source toolbox for simulating fluid flows and solving Navier-Stokes equations."
    },
    {
        "question": "Why does CFD require an extremely low-latency network like InfiniBand?",
        "options": ["To download data from the internet.", "Because it uses Domain Decomposition, meaning nodes must constantly exchange boundary data.", "Because the output files are small.", "Because it runs exclusively on GPUs."],
        "correct": 1,
        "explanation": "CFD is tightly coupled. If the network is slow, nodes waste CPU cycles waiting for adjacent boundary data."
    },
    {
        "question": "In Bioinformatics, what is the primary function of BLAST?",
        "options": ["To simulate weather.", "To compare unknown genetic sequences against massive databases to find matches.", "To perform crash simulations.", "To crack passwords."],
        "correct": 1,
        "explanation": "BLAST is used to find regions of similarity between biological sequences."
    },
    {
        "question": "What is the hardware profile of a node designed for de novo Genome Assembly (Bioinformatics)?",
        "options": ["Massive GPU density.", "A 'Fat Node' with massive amounts of RAM (1TB to 4TB+).", "A node with thousands of network interfaces.", "A node with a slow CPU."],
        "correct": 1,
        "explanation": "De novo genome assembly requires holding massive sequence graphs entirely in memory."
    },
    {
        "question": "Which hardware component provides the most significant performance boost for Molecular Dynamics (MD) simulations like GROMACS?",
        "options": ["High-capacity HDDs.", "GPUs (Accelerators).", "Faster Ethernet.", "More CPU RAM."],
        "correct": 1,
        "explanation": "Calculating inter-atomic forces is highly repetitive, making GPUs the dominant hardware for MD."
    },
    {
        "question": "What does WRF (Weather Research and Forecasting) require due to its long simulation run times?",
        "options": ["Massive high-speed storage for frequent Checkpointing.", "No storage at all.", "Single-core processors.", "Quantum networking."],
        "correct": 0,
        "explanation": "WRF runs for a long time and must dump its exact state (checkpointing) to massive, fast storage arrays to prevent data loss."
    },
    {
        "question": "What is the role of 'Burst Buffers' in Deep Learning training on HPC clusters?",
        "options": ["To slow down the GPUs.", "To act as an ultra-fast NVMe flash storage layer that feeds training data to the GPUs.", "To cool the processors.", "To encrypt network traffic."],
        "correct": 1,
        "explanation": "Standard hard drives cannot read training data fast enough, causing GPUs to starve. Burst buffers solve this I/O bottleneck."
    },
    {
        "question": "In structural engineering, what type of software is LS-DYNA?",
        "options": ["A genome sequencer.", "A Finite Element Analysis (FEA) tool used for crash simulations.", "A network sniffer.", "A password cracker."],
        "correct": 1,
        "explanation": "LS-DYNA simulates how materials deform and break upon impact by breaking them into a finite element mesh."
    },
    {
        "question": "How does the workload profile of FEA (Crash Simulation) differ from CFD (Fluid Dynamics)?",
        "options": ["FEA requires less CPU power.", "FEA does not use MPI.", "FEA meshes become highly distorted during a crash, requiring complex dynamic load balancing across the cluster.", "FEA uses only GPUs."],
        "correct": 2,
        "explanation": "Because a car chassis crumples, the computational load shifts dramatically, requiring advanced dynamic load balancing."
    },
    {
        "question": "What is the primary HPC hardware requirement for password cracking software like Hashcat?",
        "options": ["Massive RAM.", "High-speed InfiniBand.", "Extreme GPU Density (e.g., 8 to 10 GPUs per node).", "Large hard drives."],
        "correct": 2,
        "explanation": "Brute-forcing hashes is an embarrassingly parallel mathematical task that maps perfectly to the thousands of ALUs on GPUs."
    },
    {
        "question": "Why is password cracking considered an 'Embarrassingly Parallel' workload?",
        "options": ["Because the user forgot their password.", "Because no nodes need to talk to each other; they independently try different combinations without communication.", "Because it requires InfiniBand.", "Because it uses MPI."],
        "correct": 1,
        "explanation": "The tasks are completely independent, requiring zero node-to-node communication."
    },
    {
        "question": "In Computer Systems Engineering, what does EDA stand for?",
        "options": ["Electronic Design Automation", "Engineering Data Analytics", "Encrypted Data Array", "Extended Domain Analysis"],
        "correct": 0,
        "explanation": "EDA tools are used to simulate the electrical logic and timing of silicon chips before fabrication."
    },
    {
        "question": "Why are Electronic Design Automation (EDA) workloads difficult to parallelize across multiple nodes?",
        "options": ["Because they are open-source.", "Because a chip's logic is highly interconnected, so splitting it across a network causes massive latency.", "Because they only run on Windows.", "Because they don't require much CPU."],
        "correct": 1,
        "explanation": "Unlike fluids, silicon logic is heavily interdependent. EDA workloads generally require Scale-Up 'Fat Nodes' rather than Scale-Out clusters."
    },
    {
        "question": "Which workload is heavily reliant on 'Scale-Up' (Single massive server) rather than 'Scale-Out' (Many smaller servers)?",
        "options": ["Password Cracking (Hashcat)", "Electronic Design Automation (EDA)", "Molecular Dynamics (MD)", "Web Scraping"],
        "correct": 1,
        "explanation": "EDA requires massive RAM and high single-thread performance on a single machine due to the difficulty of parallelizing logic simulation."
    },
    {
        "question": "Why is 'one size fits all' a poor philosophy when building a supercomputer?",
        "options": ["Because different scientific domains have fundamentally conflicting hardware requirements (e.g., EDA needs RAM, Cyber needs GPUs, CFD needs InfiniBand).", "Because all software is identical.", "Because computers are too expensive.", "Because it is required by law."],
        "correct": 0,
        "explanation": "An HPC architect must understand the specific scientific workload before buying hardware, as optimizing for one domain often penalizes another."
    }
]

if os.path.exists(quiz_path):
    with open(quiz_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    pattern = r"const questions\s*=\s*\[.*?(?:\}\s*\];|\}\s*\]\];)"
    new_questions_str = "const questions = " + json.dumps(w10_q, indent=12) + ";"
    repl_str = new_questions_str.replace('\\', '\\\\')
    
    new_html, count = re.subn(pattern, repl_str, html, flags=re.DOTALL)
    
    with open(quiz_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Successfully updated quiz questions in {quiz_path}")
else:
    print(f"Could not find {quiz_path}")
