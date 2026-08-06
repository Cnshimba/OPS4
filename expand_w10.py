import os
import re
import json

notes_path = os.path.join("Week 10 - HPC Applications", "Week_10_Student_Notes.html")

new_content = """<h2>Overview</h2>
<p>We have spent 9 weeks building the infrastructure (Warewulf), scheduling capability (Slurm), programming models (MPI), and storage (BeeGFS). Now, what do people actually <em>do</em> with these supercomputers? In this week, we pivot from system administration to application science. We will explore the major scientific domains that rely on HPC, analyze their unique computational profiles, and understand why cluster hardware must be carefully tailored to the specific workloads it will run.</p>

<hr />

<h2>1. Computational Fluid Dynamics (CFD)</h2>
<p>CFD is the simulation of fluid flow—whether that is airflow over a Formula 1 car, water flowing through a dam, or blood pumping through a human heart. It relies on solving the Navier-Stokes equations numerically across a discretized physical space.</p>

<h3>1.1 OpenFOAM and Mesh Generation</h3>
<p><strong>OpenFOAM</strong> (Open Field Operation and Manipulation) is the premier open-source CFD toolbox. The CFD process generally involves:</p>
<ol>
    <li><strong>Meshing:</strong> The physical volume is divided into millions (or billions) of tiny geometric cells forming a "mesh".</li>
    <li><strong>Solving:</strong> The physics equations (pressure, velocity, temperature) are solved iteratively for every single cell, stepping forward in time.</li>
    <li><strong>Post-Processing:</strong> Visualizing the massive output datasets (often using tools like ParaView).</li>
</ol>

<h3>1.2 HPC Workload Profile for CFD</h3>
<p>CFD is the quintessential <strong>Tightly Coupled</strong> workload. Because the fluid in one cell directly affects the fluid in the adjacent cells, processors must constantly communicate with their neighbors.</p>
<ul>
    <li><strong>Parallel Model:</strong> MPI (Message Passing Interface) using Domain Decomposition (splitting the mesh geometrically).</li>
    <li><strong>Hardware Demands:</strong> Requires an extremely low-latency network (e.g., <strong>InfiniBand</strong>). If the network is slow, processors waste cycles waiting for boundary data (Halo Exchange) from their neighbors.</li>
    <li><strong>CPU Focus:</strong> High clock speeds and large CPU caches are critical. GPUs are notoriously difficult to apply to unstructured CFD meshes due to branching and scattered memory access.</li>
</ul>

<hr />

<h2>2. Bioinformatics and Genomics</h2>
<p>Bioinformatics applies computational science to biological data. The most common HPC task in this domain is genomic sequence analysis—reading the DNA or RNA of an organism, assembling it, and comparing it to known databases to find mutations or similarities.</p>

<h3>2.1 Common Pipelines: BLAST and GATK</h3>
<ul>
    <li><strong>BLAST (Basic Local Alignment Search Tool):</strong> Compares an unknown sequence against massive biological databases to find matches.</li>
    <li><strong>GATK (Genome Analysis Toolkit):</strong> The industry standard for identifying SNPs (Single Nucleotide Polymorphisms) and indels in DNA and RNA sequence data.</li>
</ul>

<h3>2.2 HPC Workload Profile for Bioinformatics</h3>
<p>Unlike CFD, genomic workloads are generally <strong>Loosely Coupled</strong> or <strong>Embarrassingly Parallel</strong>.</p>
<ul>
    <li><strong>Parallel Model:</strong> Often involves running thousands of independent tasks simultaneously (Task Farms/Manager-Worker).</li>
    <li><strong>Hardware Demands:</strong> Highly <strong>I/O Bound</strong>. Genomic databases are massive (terabytes). The cluster requires a robust Parallel File System (like BeeGFS or Lustre) capable of sustaining massive read throughput from thousands of nodes at once.</li>
    <li><strong>Memory Focus:</strong> Certain tasks, like <em>de novo</em> genome assembly, require "Fat Nodes"—servers with immense amounts of RAM (1TB to 4TB+ per node) to hold the entire sequence graph in memory.</li>
</ul>

<hr />

<h2>3. Molecular Dynamics (MD)</h2>
<p>Molecular Dynamics simulates the physical movements of atoms and molecules. It is heavily used in drug discovery to simulate how a potential medicine binds to a target protein (like a virus spike) at the atomic level.</p>

<h3>3.1 GROMACS, NAMD, and LAMMPS</h3>
<p>These are the dominant open-source MD engines. They calculate the electrostatic and van der Waals forces between every pair of atoms in a system for millions of microscopic time steps (femtoseconds).</p>

<h3>3.2 HPC Workload Profile for MD</h3>
<p>MD is highly floating-point math intensive and predictable.</p>
<ul>
    <li><strong>Parallel Model:</strong> Hybrid MPI (across nodes) and OpenMP/CUDA (within nodes).</li>
    <li><strong>Hardware Demands:</strong> <strong>GPUs (Accelerators)</strong> are the absolute king here. Because calculating forces between atoms is highly repetitive and uniform, it maps perfectly to the thousands of cores on an NVIDIA GPU. A single GPU node can often outperform 20 standard CPU nodes for MD workloads.</li>
</ul>

<hr />

<h2>4. Weather Forecasting and Climate Modeling</h2>
<p>Predicting the weather is one of the oldest and most vital uses of supercomputing.</p>

<h3>4.1 WRF (Weather Research and Forecasting)</h3>
<p>WRF divides the atmosphere into a 3D grid, calculating thermodynamics, solar radiation, and moisture transport. Weather forecasting operates on strict deadlines—a 24-hour forecast must compute in just an hour to be useful.</p>

<h3>4.2 HPC Workload Profile for Weather</h3>
<ul>
    <li><strong>I/O Demands:</strong> Generates massive amounts of checkpoint data. Because WRF models run for days, they must constantly dump their state to disk so the run can be resumed if a node crashes.</li>
    <li><strong>Network Demands:</strong> Highly sensitive to network latency, similar to CFD.</li>
</ul>

<hr />

<h2>5. Artificial Intelligence and Machine Learning (AI/ML)</h2>
<p>The explosive growth of Deep Learning and Large Language Models (LLMs) has fundamentally altered HPC architecture.</p>

<h3>5.1 Distributed Training</h3>
<p>Training a model like GPT-4 requires thousands of GPUs working together for months. Frameworks like PyTorch and TensorFlow use specialized communication backends (like NVIDIA NCCL) to synchronize neural network weights across the cluster.</p>

<h3>5.2 HPC Workload Profile for AI</h3>
<ul>
    <li><strong>Hardware Demands:</strong> Dense GPU nodes (e.g., 4 to 8 GPUs per node) interconnected by proprietary high-speed links like NVLink.</li>
    <li><strong>Storage Demands:</strong> "Burst Buffers" (NVMe flash arrays) are used to feed training data (images, text) into the GPUs as fast as possible to keep them from sitting idle.</li>
</ul>

<hr />

<h2>6. Summary</h2>
<p>Understanding these workloads is critical for an HPC administrator. If your university specializes in Genomics, you must spend your budget on massive storage arrays and high-RAM nodes. If they specialize in Deep Learning, every cent should go into GPUs. There is no "one size fits all" supercomputer.</p>

<h3>Preparing for Week 11</h3>
<p>Next week, we will tackle <strong>System Administration and Monitoring</strong>. How do we know if these massive applications are actually using the hardware efficiently? We will deploy <strong>Prometheus</strong> and <strong>Grafana</strong> to visualize the heartbeat of our supercomputer.</p>"""

if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # We want to replace everything from <h2>Overview</h2> down to </ul> right before </article>
    # Since regex can be tricky with HTML, we'll do a string slice.
    start_tag = "<h2>Overview</h2>"
    end_tag = "</article>"
    
    start_idx = html.find(start_tag)
    end_idx = html.rfind(end_tag)
    
    if start_idx != -1 and end_idx != -1:
        new_html = html[:start_idx] + new_content + "\n        " + html[end_idx:]
        with open(notes_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Successfully expanded content in {notes_path}")
    else:
        print("Could not find insertion points.")
else:
    print(f"Could not find {notes_path}")


# Now generate the Quiz for Week 10
w10_q = [
    {
        "question": "Which of the following scientific domains primarily uses OpenFOAM?",
        "options": ["Bioinformatics", "Computational Fluid Dynamics (CFD)", "Molecular Dynamics", "Natural Language Processing"],
        "correct": 1,
        "explanation": "OpenFOAM (Open Field Operation and Manipulation) is the premier open-source toolbox for simulating fluid flows and solving Navier-Stokes equations."
    },
    {
        "question": "Why does CFD (like OpenFOAM) require an extremely low-latency network like InfiniBand?",
        "options": ["Because fluid dynamic equations are downloaded from the internet.", "Because it uses Domain Decomposition, meaning compute nodes must constantly exchange boundary (halo) data with their neighbors after every time step.", "Because the output files are very small.", "Because it runs exclusively on GPUs."],
        "correct": 1,
        "explanation": "CFD is tightly coupled. If the network is slow, nodes waste CPU cycles waiting for adjacent boundary data to arrive before they can compute the next step."
    },
    {
        "question": "In Bioinformatics, what is the primary function of BLAST?",
        "options": ["To simulate weather patterns.", "To compare unknown genetic sequences (DNA/RNA/Proteins) against massive known databases to find matches.", "To render 3D graphics.", "To schedule jobs on a cluster."],
        "correct": 1,
        "explanation": "BLAST (Basic Local Alignment Search Tool) is used to find regions of similarity between biological sequences."
    },
    {
        "question": "Which of the following best describes the workload profile of most Bioinformatics pipelines (e.g., sequence alignment)?",
        "options": ["Tightly coupled, requiring constant node-to-node communication.", "Embarrassingly parallel and highly I/O bound (Data Heavy).", "Requires low-latency InfiniBand to function.", "Only runs efficiently on Quantum Computers."],
        "correct": 1,
        "explanation": "Sequence searches can often be split into thousands of independent tasks that do not need to communicate with each other, making them embarrassingly parallel. However, they read terabytes of database files."
    },
    {
        "question": "What is a 'Fat Node' in HPC?",
        "options": ["A node with a physically large chassis.", "A compute node equipped with massive amounts of RAM (e.g., 1TB to 4TB+), often used for genome assembly.", "A node that consumes too much electricity.", "A node running Windows."],
        "correct": 1,
        "explanation": "De novo genome assembly requires holding massive sequence graphs entirely in memory, necessitating specialized 'Fat Nodes' with huge RAM capacities."
    },
    {
        "question": "What is the primary purpose of Molecular Dynamics (MD) software like GROMACS or NAMD?",
        "options": ["To predict the weather.", "To simulate the physical movements and electrostatic forces of atoms and molecules over time.", "To assemble genomes.", "To monitor network traffic."],
        "correct": 1,
        "explanation": "MD simulates molecular interactions at the atomic level, which is critical for drug discovery and material science."
    },
    {
        "question": "Which hardware component provides the most significant performance boost for Molecular Dynamics (MD) simulations?",
        "options": ["High-capacity HDD arrays.", "GPUs (Accelerators).", "Faster Ethernet cables.", "More CPU cores."],
        "correct": 1,
        "explanation": "Because calculating inter-atomic forces is highly repetitive and uniform, it maps perfectly to the thousands of cores on an NVIDIA GPU, making GPUs the dominant hardware for MD."
    },
    {
        "question": "What does WRF stand for in HPC?",
        "options": ["Weather Research and Forecasting", "Worldwide Routing Framework", "Web Resource Fetcher", "Wireless Radio Frequency"],
        "correct": 0,
        "explanation": "WRF is a next-generation mesoscale numerical weather prediction system designed for both atmospheric research and operational forecasting."
    },
    {
        "question": "Why is high-performance storage critical for Weather Modeling (WRF)?",
        "options": ["Weather models don't use storage.", "Because weather models generate massive amounts of Checkpoint data that must be dumped to disk rapidly to ensure the multi-day run isn't lost if a node crashes.", "Because it streams live video from satellites.", "Because weather changes too fast."],
        "correct": 1,
        "explanation": "WRF models run for a long time. Checkpointing (saving the exact state of the simulation) requires writing massive files to disk simultaneously from all nodes."
    },
    {
        "question": "In the context of AI and Deep Learning training on HPC, what is the role of 'Burst Buffers'?",
        "options": ["To slow down the GPUs.", "To act as an ultra-fast NVMe flash storage layer that feeds training data (like images) into the GPUs fast enough to keep them from sitting idle.", "To buffer network packets.", "To cool the processors."],
        "correct": 1,
        "explanation": "GPUs process data incredibly fast. Standard hard drives cannot read training data fast enough, causing the expensive GPUs to wait (starve). Burst buffers solve this I/O bottleneck."
    },
    {
        "question": "Which HPC workload is generally considered 'Tightly Coupled'?",
        "options": ["Bioinformatics sequence searching", "Image rendering farm", "Computational Fluid Dynamics (CFD)", "Web scraping"],
        "correct": 2,
        "explanation": "CFD requires processors to constantly exchange data with each other at every time step, meaning they are tightly bound together by the network."
    },
    {
        "question": "Which communication library is heavily used by PyTorch and TensorFlow for distributed GPU training?",
        "options": ["OpenMP", "NVIDIA NCCL (Nickel)", "SLURM", "POSIX"],
        "correct": 1,
        "explanation": "NCCL (NVIDIA Collective Communication Library) is optimized specifically for multi-GPU and multi-node communication, utilizing NVLink and InfiniBand efficiently."
    },
    {
        "question": "If an HPC center's primary mission is Deep Learning and AI, what should be the bulk of their hardware budget?",
        "options": ["Massive slow storage arrays", "High-density GPU nodes", "Thousands of low-power ARM CPUs", "Fat nodes with 4TB RAM but no GPUs"],
        "correct": 1,
        "explanation": "AI workloads are almost entirely dependent on GPU acceleration (Tensor Cores)."
    },
    {
        "question": "What is 'Domain Decomposition' in the context of CFD?",
        "options": ["Breaking down a URL into parts.", "Geometrically splitting the physical simulation mesh into smaller chunks, assigning each chunk to a different CPU core.", "Compressing data to save space.", "Translating code from C++ to Python."],
        "correct": 1,
        "explanation": "Domain decomposition is how tightly coupled physical simulations achieve parallelism—by dividing the 3D space among processors."
    },
    {
        "question": "Why is 'one size fits all' a poor philosophy when building a supercomputer?",
        "options": ["Because all scientists use the exact same software.", "Because different scientific domains have fundamentally conflicting hardware requirements (e.g., Genomics needs I/O and RAM; AI needs GPUs; CFD needs low-latency networking).", "Because computers are too expensive.", "Because it is required by law."],
        "correct": 1,
        "explanation": "A cluster optimized for bioinformatics will perform poorly on CFD, and vice versa. An HPC architect must understand the specific scientific workload before buying hardware."
    }
]

def create_w10_quiz():
    week = 10
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and f.startswith(f"Week {week} - ")]
    if not folders:
        print("Folder not found")
        return
    folder = folders[0]
    
    template_path = os.path.join("Week 2 - System Design and Memory", "Week_2_Quiz.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    new_html = template.replace("Week 2 Quiz: System Design and Memory", f"Week {week} Quiz")
    new_html = new_html.replace("Week 2 Quiz", f"Week {week} Quiz")
    new_html = new_html.replace("Test your understanding of System Design, Topologies, and Memory Hierarchies", f"Test your understanding of Week {week} concepts")
    new_html = new_html.replace("Week_2_Student_Notes.html", f"Week_{week}_Student_Notes.html")
    
    pattern = r"const questions\s*=\s*\[.*?(?:\}\s*\];|\}\s*\]\];)"
    new_questions_str = "const questions = " + json.dumps(w10_q, indent=12) + ";"
    repl_str = new_questions_str.replace('\\', '\\\\')
    
    new_html, count = re.subn(pattern, repl_str, new_html, flags=re.DOTALL)
    
    out_path = os.path.join(folder, f"Week_{week}_Quiz.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Created {out_path}")

    # Add link
    notes_path = os.path.join(folder, f"Week_{week}_Student_Notes.html")
    with open(notes_path, 'r', encoding='utf-8') as f:
        notes_content = f.read()
    
    if f"Week_{week}_Quiz.html" not in notes_content:
        quiz_div = f'''
<div class="mt-12 p-8 bg-[#002F6E]/10 dark:bg-[#002F6E]/20 rounded-xl border border-[#002F6E] text-center">
    <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Test Your Knowledge</h3>
    <p class="text-slate-600 dark:text-slate-300 mb-6">Ready to check your understanding of this week's material? Take the interactive quiz now!</p>
    <a href="Week_{week}_Quiz.html" class="inline-block px-8 py-3 bg-[#002F6E] hover:bg-[#002355] text-white font-bold rounded-lg transition-colors shadow-md no-underline">
        Start Quiz
    </a>
</div>
'''
        new_notes = notes_content.replace("</article>", quiz_div + "\n        </article>")
        with open(notes_path, 'w', encoding='utf-8') as f:
            f.write(new_notes)
        print(f"Linked quiz in {notes_path}")

create_w10_quiz()
