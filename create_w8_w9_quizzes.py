import os
import json
import shutil
import re

w8_q = [
    {
        "question": "What is the primary difference between Block storage and File storage?",
        "options": ["Block storage is accessed over the internet, File storage is local.", "Block storage provides raw storage volumes without a filesystem, while File storage presents data organized in directories and files.", "Block storage is only for Windows, File storage is for Linux.", "There is no difference."],
        "correct": 1,
        "explanation": "Block storage is low-level and accessed by the OS as a raw drive. File storage adds a filesystem layer (like NFS or SMB) so users see files and folders."
    },
    {
        "question": "Why does standard NFS often become a severe bottleneck in HPC environments?",
        "options": ["It does not support Linux.", "It is a single-server architecture, meaning all data requests from thousands of compute nodes hit one machine, overwhelming its network and disk I/O.", "It encrypts data too heavily.", "It cannot store files larger than 4GB."],
        "correct": 1,
        "explanation": "Standard NFS funnels all cluster I/O through a single server. In HPC, concurrent access from many nodes quickly saturates the NFS server's bandwidth."
    },
    {
        "question": "What does POSIX compliance mean for a file system?",
        "options": ["It is free and open-source.", "It adheres to a standard set of OS interfaces (like open, read, write, close) ensuring compatibility with standard Linux utilities and applications.", "It guarantees data encryption.", "It means the file system is specifically designed for GPUs."],
        "correct": 1,
        "explanation": "POSIX defines standard system calls. If a Parallel File System is POSIX compliant, standard commands like 'ls' or 'cp' work without modification."
    },
    {
        "question": "What is the primary architectural advantage of a Parallel File System (PFS) like Lustre or BeeGFS?",
        "options": ["It compresses files more efficiently.", "It strips data across multiple independent storage servers, allowing clients to read/write fragments in parallel, vastly increasing total bandwidth.", "It automatically translates code from C to Python.", "It uses less electricity."],
        "correct": 1,
        "explanation": "By breaking large files into chunks and distributing them across many servers (striping), a PFS allows massive parallel I/O, bypassing single-server bottlenecks."
    },
    {
        "question": "In a Parallel File System, what is the difference between Metadata and Data?",
        "options": ["Metadata is the file contents; Data is the filename.", "Metadata includes file attributes (name, size, permissions, physical location of stripes); Data is the actual file content.", "Metadata is for administrators; Data is for users.", "Metadata is stored in the cloud."],
        "correct": 1,
        "explanation": "Metadata servers manage the directory structure and tell clients where the pieces of a file are located. Storage servers hold the actual bits."
    },
    {
        "question": "In Lustre architecture, what does MDS stand for?",
        "options": ["Main Data Storage", "Metadata Server", "Multiple Disk System", "Memory Direct Sync"],
        "correct": 1,
        "explanation": "The MDS (Metadata Server) manages the namespace and permissions. It stores this metadata on an MDT (Metadata Target)."
    },
    {
        "question": "In Lustre architecture, what is an OSS?",
        "options": ["Open Source Software", "Object Storage Server", "Operational State System", "Optical Storage Switch"],
        "correct": 1,
        "explanation": "The OSS (Object Storage Server) provides file I/O service, storing file data chunks on OSTs (Object Storage Targets)."
    },
    {
        "question": "BeeGFS is known for its modular architecture. Which of the following is NOT one of its core services?",
        "options": ["Management Service", "Metadata Service", "Storage Service", "Rendering Service"],
        "correct": 3,
        "explanation": "BeeGFS consists of the Management, Metadata, Storage, and Client services. Rendering is unrelated to storage."
    },
    {
        "question": "What does 'Striping' refer to in advanced storage concepts?",
        "options": ["Painting lines on the server room floor.", "Distributing consecutive segments of a file across multiple storage targets to enable parallel I/O.", "Removing metadata from a file.", "Compressing a file to save space."],
        "correct": 1,
        "explanation": "Striping splits a file into chunks (e.g., 1MB each) and writes them across different servers, multiplying the read/write performance."
    },
    {
        "question": "Why is NVMe (Flash) storage heavily preferred for Metadata Servers?",
        "options": ["It is cheaper than HDD.", "Metadata operations involve millions of tiny, random reads and writes (IOPS), which flash handles exponentially better than spinning disks.", "It looks cooler in the server rack.", "It is required for POSIX compliance."],
        "correct": 1,
        "explanation": "Metadata workloads are highly random and IOPS-intensive (e.g., checking permissions, listing directories), making the low latency of NVMe critical."
    },
    {
        "question": "What is Object Storage (like Amazon S3)?",
        "options": ["A hierarchical file system.", "A flat storage architecture where data is managed as objects, each with a unique identifier and rich metadata, accessed via an API.", "Storage designed specifically for object-oriented programming.", "A type of local hard drive."],
        "correct": 1,
        "explanation": "Unlike File storage (hierarchical) or Block storage (raw sectors), Object storage uses a flat namespace and HTTP APIs (REST) to store and retrieve data."
    },
    {
        "question": "What is the difference between Throughput and IOPS?",
        "options": ["Throughput measures data volume per second (MB/s); IOPS measures the number of distinct read/write operations per second.", "They are the exact same thing.", "Throughput is for CPUs; IOPS is for storage.", "Throughput measures latency; IOPS measures capacity."],
        "correct": 0,
        "explanation": "Throughput (Bandwidth) is critical for large sequential files (video, big data). IOPS is critical for small, random access (databases, metadata)."
    },
    {
        "question": "How is High Availability (HA) typically achieved in HPC storage?",
        "options": ["By asking users not to delete files.", "By deploying redundant servers (e.g., Active-Passive pairs) connected to shared dual-ported drives so one can take over if the other fails.", "By backing everything up to a USB drive nightly.", "By running the servers at a lower temperature."],
        "correct": 1,
        "explanation": "HA ensures that if an OSS or MDS hardware fails, its partner node immediately takes over its IP address and storage targets without dropping client connections."
    },
    {
        "question": "What is a 'Quota' in cluster storage?",
        "options": ["The maximum number of users allowed to log in.", "A hard or soft limit enforced by the file system on how much disk space or how many files (inodes) a user or group can consume.", "The physical speed limit of the network.", "A daily backup schedule."],
        "correct": 1,
        "explanation": "Quotas prevent a single runaway job or careless user from filling up the entire multi-petabyte shared file system and crashing the cluster."
    },
    {
        "question": "Why is network bandwidth critical for Parallel File Systems?",
        "options": ["Because they run on the public internet.", "Because the compute nodes must send massive amounts of data over the network to reach the distributed storage servers.", "Because it downloads software updates.", "It isn't; CPU speed is more important."],
        "correct": 1,
        "explanation": "In a PFS, the storage is entirely network-attached. The maximum read/write speed of a node is directly limited by its network connection (e.g., Infiniband) to the storage servers."
    }
]

w9_q = [
    {
        "question": "What is the fundamental architectural difference between a CPU and a GPU?",
        "options": ["CPUs are designed for high throughput; GPUs are designed for low latency.", "CPUs optimize for low-latency sequential execution using complex logic; GPUs optimize for massive throughput using thousands of simple cores.", "CPUs use memory; GPUs do not.", "There is no difference; they are interchangeable."],
        "correct": 1,
        "explanation": "CPUs use a few large, complex cores with deep caches to execute single threads very fast. GPUs use thousands of tiny cores to execute thousands of threads simultaneously."
    },
    {
        "question": "What does CUDA stand for, and what is it?",
        "options": ["Compute Unified Device Architecture; NVIDIA's parallel computing platform and programming model.", "Central Unit for Data Analysis; a new type of processor.", "Computer Understanding of Deep Algorithms; an AI software.", "C++ Universal Data Array; a data structure."],
        "correct": 0,
        "explanation": "CUDA is the proprietary software layer and API created by NVIDIA that allows developers to write C/C++ code that executes directly on NVIDIA GPUs."
    },
    {
        "question": "In NVIDIA architecture, what is an SM (Streaming Multiprocessor)?",
        "options": ["A video streaming card.", "The core building block of a GPU, containing a group of CUDA cores, shared memory, and schedulers.", "The main CPU of the host machine.", "A network interface."],
        "correct": 1,
        "explanation": "A GPU is made up of multiple SMs. Each SM operates somewhat independently, scheduling and executing blocks of threads on its own set of internal cores."
    },
    {
        "question": "What is a 'Warp' in CUDA terminology?",
        "options": ["A bug that crashes the GPU.", "A group of 32 threads that are executed simultaneously in lockstep on an SM.", "A memory leak.", "A physical cable connecting two GPUs."],
        "correct": 1,
        "explanation": "NVIDIA GPUs group threads into Warps of 32. All 32 threads in a warp must execute the exact same instruction at the same time (SIMT architecture)."
    },
    {
        "question": "What happens if threads within the same Warp take different paths in an `if-else` statement (Warp Divergence)?",
        "options": ["The GPU crashes.", "The SM must execute each branch sequentially, disabling the threads not on the current branch, which severely degrades performance.", "The GPU automatically spawns a new SM.", "Nothing, it runs at full speed."],
        "correct": 1,
        "explanation": "Because a Warp shares a single instruction fetch unit, divergent branches force the hardware to serialize the execution of the `if` and the `else`, halving performance."
    },
    {
        "question": "What is the difference between 'Host' and 'Device' in GPU programming?",
        "options": ["Host is the network; Device is the hard drive.", "Host is the user; Device is the software.", "Host refers to the CPU and its memory; Device refers to the GPU and its memory.", "Host is the GPU; Device is the CPU."],
        "correct": 2,
        "explanation": "In heterogeneous computing, the Host (CPU) orchestrates the program and offloads heavy parallel tasks to the Device (GPU)."
    },
    {
        "question": "What is typically the most significant bottleneck in GPU-accelerated applications?",
        "options": ["The clock speed of the GPU.", "Transferring data back and forth between the Host memory and Device memory over the PCIe bus.", "The size of the L1 cache.", "The speed of the monitor."],
        "correct": 1,
        "explanation": "The PCIe bus is vastly slower than the GPU's internal memory bandwidth. If an application constantly copies data to/from the GPU, it will lose all performance gains."
    },
    {
        "question": "What is 'Shared Memory' on a GPU?",
        "options": ["Memory shared with other users on the internet.", "A very fast, user-managed scratchpad memory located on the SM, shared among all threads in a Block.", "The main VRAM of the GPU.", "Memory shared over the PCIe bus."],
        "correct": 1,
        "explanation": "Shared memory is an explicit, on-chip cache. Threads in a block can use it to cooperate and share data locally at speeds much faster than reaching out to global VRAM."
    },
    {
        "question": "In CUDA, what is a 'Thread Block'?",
        "options": ["A firewall rule.", "A logical grouping of threads that execute together on the same SM and can synchronize and share memory.", "A physical chunk of silicon.", "A section of the hard drive."],
        "correct": 1,
        "explanation": "When you launch a GPU kernel, you organize millions of threads into Blocks. The GPU hardware schedules each entire Block onto a single SM."
    },
    {
        "question": "What is OpenACC?",
        "options": ["An open-source GPU manufacturer.", "A directive-based programming model (like OpenMP) that allows developers to add pragmas to C/Fortran code to automatically offload loops to the GPU.", "A database management system.", "A Linux kernel module."],
        "correct": 1,
        "explanation": "OpenACC (and OpenMP offloading) provides a higher-level, easier alternative to writing raw CUDA code, letting the compiler handle the complex GPU memory management and threading."
    },
    {
        "question": "What does SIMT stand for?",
        "options": ["Single Instruction, Multiple Threads", "System Integrated Memory Transfer", "Synchronous Iteration, Multiple Tasks", "Shared Internet Multi-Tenancy"],
        "correct": 0,
        "explanation": "SIMT (Single Instruction, Multiple Threads) is NVIDIA's term for their architecture, where a single instruction is broadcast to multiple threads (a Warp) executing on different data."
    },
    {
        "question": "What is 'Occupancy' in GPU profiling?",
        "options": ["The physical space the GPU takes in the rack.", "The ratio of active warps on an SM to the maximum possible number of active warps.", "The percentage of hard drive used.", "The number of users logged in."],
        "correct": 1,
        "explanation": "High occupancy means the SM has plenty of warps to switch between when one warp stalls (e.g., waiting for memory), allowing the GPU to hide latency effectively."
    },
    {
        "question": "What is the advantage of CUDA 'Unified Memory'?",
        "options": ["It makes the GPU run faster.", "It creates a single virtual memory space accessible by both the CPU and GPU, automatically migrating data pages on demand without explicit copy commands.", "It combines the RAM of multiple compute nodes.", "It prevents race conditions."],
        "correct": 1,
        "explanation": "Unified Memory simplifies programming by eliminating the need to write complex `cudaMemcpy` commands; the driver moves data across the PCIe bus behind the scenes."
    },
    {
        "question": "What is NVLink?",
        "options": ["A website for downloading drivers.", "A proprietary high-speed interconnect developed by NVIDIA that allows GPUs to communicate directly with each other much faster than PCIe.", "A type of fiber optic cable.", "A programming language."],
        "correct": 1,
        "explanation": "NVLink provides massive bandwidth (hundreds of GB/s) directly between multiple GPUs within a node, bypassing the CPU and PCIe bottleneck for multi-GPU training."
    },
    {
        "question": "What are Tensor Cores?",
        "options": ["Cores that stretch the silicon.", "Specialized execution units on modern GPUs specifically designed to dramatically accelerate mixed-precision matrix multiply-accumulate operations used in Deep Learning.", "The main power supply of the GPU.", "Software libraries for text analysis."],
        "correct": 1,
        "explanation": "Unlike standard CUDA cores that do generalized math, Tensor Cores perform large matrix operations (like 4x4 matrix multiplication) in a single clock cycle, fueling the AI boom."
    }
]

def create_quiz(week, questions):
    # Determine the folder for the week
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and f.startswith(f"Week {week} - ")]
    if not folders:
        print(f"Skipping week {week}, folder not found")
        return
    folder = folders[0]
    
    # Use Week 2 Quiz as template
    template_path = os.path.join("Week 2 - System Design and Memory", "Week_2_Quiz.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace titles and specific text
    new_html = template.replace("Week 2 Quiz: System Design and Memory", f"Week {week} Quiz")
    new_html = new_html.replace("Week 2 Quiz", f"Week {week} Quiz")
    new_html = new_html.replace("Test your understanding of System Design, Topologies, and Memory Hierarchies", f"Test your understanding of Week {week} concepts")
    new_html = new_html.replace("Week_2_Student_Notes.html", f"Week_{week}_Student_Notes.html")
    
    # Replace the questions array
    pattern = r"const questions\s*=\s*\[.*?(?:\}\s*\];|\}\s*\]\];)"
    new_questions_str = "const questions = " + json.dumps(questions, indent=12) + ";"
    repl_str = new_questions_str.replace('\\', '\\\\')
    
    new_html, count = re.subn(pattern, repl_str, new_html, flags=re.DOTALL)
    
    if count == 0:
        print(f"Failed to replace questions via regex for week {week}")
    
    out_path = os.path.join(folder, f"Week_{week}_Quiz.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Created {out_path}")

    # Now add the link to the Student Notes
    notes_path = os.path.join(folder, f"Week_{week}_Student_Notes.html")
    if os.path.exists(notes_path):
        with open(notes_path, 'r', encoding='utf-8') as f:
            notes_content = f.read()
        
        # Check if quiz is already linked
        if f"Week_{week}_Quiz.html" not in notes_content:
            # We want to insert the styled div right before </article>
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
        else:
            print(f"Quiz already linked in {notes_path}")


create_quiz(8, w8_q)
create_quiz(9, w9_q)
