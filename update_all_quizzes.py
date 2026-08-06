import os
import json
import re

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
    },
    {
        "question": "Which of the following best defines Moore's Law?",
        "options": ["The speed of light is the ultimate limit for data transmission.", "The number of transistors on a microchip doubles approximately every two years.", "The power consumption of a processor halves every 18 months.", "Software speed decreases as hardware speed increases."],
        "correct": 1,
        "explanation": "Moore's Law is the observation that the number of transistors in a dense integrated circuit doubles about every two years."
    },
    {
        "question": "What was Dennard Scaling?",
        "options": ["As transistors get smaller, their power density remains constant.", "The speed of a processor scales linearly with the number of cores.", "The network bandwidth must scale with the processor speed.", "Memory size must double every two years."],
        "correct": 0,
        "explanation": "Dennard Scaling stated that as transistors shrink, their power density stays constant, meaning performance per watt increases. Its breakdown led to the multi-core era."
    },
    {
        "question": "According to Amdahl's Law, what limits the maximum speedup of a parallel program?",
        "options": ["The number of processors.", "The speed of the network interconnect.", "The fraction of the code that is strictly serial.", "The amount of available RAM."],
        "correct": 2,
        "explanation": "Amdahl's Law states that the theoretical maximum speedup is strictly limited by the serial portion of the program."
    },
    {
        "question": "What does SISD stand for in Flynn's Taxonomy?",
        "options": ["Single Instruction, Single Data", "Standard Instruction, Shared Data", "Synchronous Instruction, Single Data", "Systematic Instruction, Shared Data"],
        "correct": 0,
        "explanation": "SISD stands for Single Instruction, Single Data, which characterizes a traditional uniprocessor system."
    },
    {
        "question": "What does MIMD stand for in Flynn's Taxonomy?",
        "options": ["Multiple Instruction, Multiple Data", "Memory Instruction, Memory Data", "Main Instruction, Main Data", "Multiple Iteration, Multiple Data"],
        "correct": 0,
        "explanation": "MIMD stands for Multiple Instruction, Multiple Data, typical of modern multi-core processors and HPC clusters."
    },
    {
        "question": "Which of the following is a key characteristic of a computing cluster?",
        "options": ["It consists of a single massive processor.", "It connects multiple independent computers via a network to act as a single system.", "It runs only single-threaded applications.", "It shares a single continuous block of physical memory across all nodes."],
        "correct": 1,
        "explanation": "A cluster connects multiple standalone machines (nodes) via a high-speed network to work collaboratively on computational tasks."
    },
    {
        "question": "What was the main driver for the shift to multi-core processors?",
        "options": ["The inability to manufacture larger silicon wafers.", "The breakdown of Dennard Scaling and the 'power wall'.", "A shortage of memory bandwidth.", "The invention of GPUs."],
        "correct": 1,
        "explanation": "When Dennard Scaling broke down, increasing clock speeds led to excessive heat (the power wall), forcing manufacturers to use multiple slower cores instead."
    },
    {
        "question": "In a Distributed Memory architecture, how do processors access each other's memory?",
        "options": ["Directly via the memory bus.", "Through explicit message passing over a network.", "Via a shared Level 3 cache.", "By reading and writing to a central shared hard drive."],
        "correct": 1,
        "explanation": "In distributed memory systems (like a cluster), nodes cannot access each other's RAM directly; they must send and receive data explicitly over a network."
    },
    {
        "question": "What is the primary role of a high-speed interconnect in an HPC cluster?",
        "options": ["To connect the cluster to the internet.", "To provide power to the compute nodes.", "To facilitate fast, low-latency communication between compute nodes.", "To connect the monitor and keyboard to the head node."],
        "correct": 2,
        "explanation": "Interconnects like Infiniband are designed for extremely high bandwidth and low latency communication between nodes, essential for parallel applications."
    },
    {
        "question": "What constitutes a 'compute node' in a cluster?",
        "options": ["A specialized hard drive.", "An individual server containing CPUs, memory, and a network interface.", "The software that schedules jobs.", "The main switch that routes traffic."],
        "correct": 1,
        "explanation": "A compute node is essentially a standalone server that acts as a single worker unit within the larger cluster."
    },
    {
        "question": "What is the primary difference between a CPU and a GPU?",
        "options": ["CPUs have more cores than GPUs.", "GPUs are optimized for serial execution, while CPUs are optimized for parallel execution.", "CPUs are optimized for low latency and complex logic, while GPUs are optimized for high throughput and parallel data processing.", "CPUs only process integers, while GPUs process floating-point numbers."],
        "correct": 2,
        "explanation": "CPUs use complex cores for fast sequential processing, whereas GPUs use thousands of simpler cores for massive data parallelism."
    },
    {
        "question": "How is Peak FLOPS typically calculated for a processor?",
        "options": ["Cores x Clock Frequency x FLOPs per Cycle", "Memory Bandwidth x Clock Frequency", "Number of Transistors x Power Consumption", "Network Latency x Number of Nodes"],
        "correct": 0,
        "explanation": "Theoretical peak performance is calculated by multiplying the number of cores, the clock speed, and the number of floating-point operations the core can execute per cycle."
    }
]

w2_q = [
    {
        "question": "What is the primary metric used to rank systems on the Top500 list?",
        "options": ["Total storage capacity", "Peak memory bandwidth", "Maximum sustained floating-point performance (Linpack)", "Lowest network latency"],
        "correct": 2,
        "explanation": "The Top500 list ranks the world's fastest supercomputers based on their Rmax score (sustained performance) achieved running the High Performance Linpack (HPL) benchmark."
    },
    {
        "question": "What is the function of a PCIe bus in a modern compute node?",
        "options": ["It connects the CPU to the L1 cache.", "It provides a high-speed interface for connecting peripherals like GPUs and network cards to the CPU.", "It routes data between different compute nodes in the cluster.", "It is the primary power supply line for the motherboard."],
        "correct": 1,
        "explanation": "Peripheral Component Interconnect Express (PCIe) is the high-speed serial computer expansion bus standard used to attach hardware devices to a computer."
    },
    {
        "question": "What does RDMA stand for, and what is its primary advantage?",
        "options": ["Remote Direct Memory Access; it allows data transfer between nodes without involving the remote CPU.", "Rapid Disk Management Architecture; it speeds up hard drive reads.", "Remote Data Mapping Algorithm; it compresses data over the network.", "Random Direct Memory Allocation; it prevents memory leaks."],
        "correct": 0,
        "explanation": "RDMA allows a network card to transfer data directly to or from the application memory on a remote node, bypassing the CPU and operating system for ultra-low latency."
    },
    {
        "question": "Why is InfiniBand often preferred over standard Ethernet in HPC environments?",
        "options": ["It uses cheaper cables.", "It offers significantly lower latency and natively supports RDMA.", "It operates wirelessly.", "It is natively compatible with Windows without drivers."],
        "correct": 1,
        "explanation": "InfiniBand is designed specifically for HPC, offering extreme bandwidth, microsecond latency, and native RDMA, which are critical for tight parallel coupling."
    },
    {
        "question": "What is NUMA?",
        "options": ["Non-Uniform Memory Access: memory access time depends on the memory location relative to the processor.", "Network User Management API: a tool for managing cluster users.", "New Unified Memory Architecture: a system where all memory is exactly the same distance from all CPUs.", "Node Utilization Metric Analysis: a benchmarking tool."],
        "correct": 0,
        "explanation": "In NUMA systems, a CPU can access its own local memory faster than memory attached to another CPU on the same motherboard."
    },
    {
        "question": "What is the purpose of cache coherence protocols in multi-core processors?",
        "options": ["To increase the size of the L3 cache.", "To ensure that all cores see a consistent view of memory, even if they have local cached copies.", "To compress data before storing it in cache.", "To clear the cache automatically when a program crashes."],
        "correct": 1,
        "explanation": "Cache coherence ensures that if one core modifies a variable in its local cache, other cores will not read stale, outdated versions of that variable."
    },
    {
        "question": "What is a Baseboard Management Controller (BMC)?",
        "options": ["The primary CPU of the compute node.", "A specialized microcontroller that manages the interface between system-management software and platform hardware.", "The network switch connecting the cluster.", "A software program for managing MPI jobs."],
        "correct": 1,
        "explanation": "The BMC provides out-of-band management, allowing administrators to monitor hardware health, power cycle the node, and access the console remotely, even if the OS is unresponsive."
    },
    {
        "question": "What is the primary role of a 'Head Node' (or Login Node)?",
        "options": ["To perform the heaviest computational tasks.", "To provide a secure entry point for users to compile code and submit jobs to the compute nodes.", "To store all the backup data for the cluster.", "To regulate the cooling system of the server racks."],
        "correct": 1,
        "explanation": "The head node acts as the gateway to the cluster. Users log in here to edit files, compile software, and submit jobs to the batch scheduler, rather than running computations on it directly."
    },
    {
        "question": "In rack-mounted server hardware, what does '1U' denote?",
        "options": ["1 User", "1 Unit of processing power", "1 Rack Unit of height (1.75 inches)", "1 Uninterruptible power supply"],
        "correct": 2,
        "explanation": "A Rack Unit (U) is a unit of measure describing the height of equipment designed to mount in a 19-inch rack. 1U equals 1.75 inches (44.45 mm)."
    },
    {
        "question": "Why do enterprise servers often have redundant Power Supply Units (PSUs)?",
        "options": ["To double the clock speed of the processors.", "To ensure the server remains operational if one power supply fails or loses its power source.", "To generate more heat for the cooling system to process.", "To separate power for the CPU and the RAM."],
        "correct": 1,
        "explanation": "Redundancy ensures high availability. If one PSU fails, the other can handle the full load, preventing the server from crashing."
    },
    {
        "question": "Which of the following represents the correct order of the memory hierarchy, from fastest/smallest to slowest/largest?",
        "options": ["RAM, L1 Cache, Registers, NVMe Storage", "Registers, L1 Cache, RAM, NVMe Storage", "NVMe Storage, RAM, L1 Cache, Registers", "L1 Cache, Registers, NVMe Storage, RAM"],
        "correct": 1,
        "explanation": "Registers are the fastest and smallest, followed by cache (L1, L2, L3), then main memory (RAM), and finally persistent storage (like NVMe SSDs)."
    },
    {
        "question": "What does 'network oversubscription' mean in cluster design?",
        "options": ["Paying for more bandwidth than you need.", "Having more downlink bandwidth to the nodes than uplink bandwidth between switches.", "Having too many users logged into the head node.", "Running network cables that are too long."],
        "correct": 1,
        "explanation": "Oversubscription occurs when a switch has more bandwidth connected to its local nodes than it has bandwidth to send traffic to other switches, creating a potential bottleneck."
    },
    {
        "question": "What is IPMI used for?",
        "options": ["Internet Protocol for Message Passing Interface.", "Intelligent Platform Management Interface, used for remote, out-of-band management of servers.", "Internal Processor Memory Interface.", "Integrated Parallel Management Instructions."],
        "correct": 1,
        "explanation": "IPMI is the standardized protocol used by the BMC to allow remote monitoring, power control, and console access to a server."
    },
    {
        "question": "Why is efficient cooling critical in HPC data centers?",
        "options": ["Because CPUs run faster at room temperature.", "Because high-density compute nodes generate massive amounts of heat, which can cause thermal throttling or hardware failure.", "Because hard drives require low temperatures to spin.", "Because network cables degrade in heat."],
        "correct": 1,
        "explanation": "HPC clusters pack immense computing power into small physical spaces, generating significant heat. Without adequate cooling, components will overheat and either slow down (throttle) or fail."
    },
    {
        "question": "What is the function of a network topology like a 'Fat Tree'?",
        "options": ["To connect nodes in a single straight line.", "To provide multiple paths and high bisection bandwidth between any two nodes in the cluster.", "To organize files on the hard drive.", "To visualize the execution flow of a program."],
        "correct": 1,
        "explanation": "A Fat Tree topology ensures that communication between nodes in different parts of the cluster has sufficient bandwidth, often providing non-blocking communication."
    }
]

w3_q = [
    {
        "question": "What does PXE stand for?",
        "options": ["Preboot Execution Environment", "Parallel XML Extractor", "Primary X Server Environment", "Processor Execution Engine"],
        "correct": 0,
        "explanation": "PXE (Preboot Execution Environment) is an industry standard that allows computers to boot an operating system directly from the network instead of a local disk."
    },
    {
        "question": "What is the role of DHCP in the network boot process?",
        "options": ["It transfers the operating system files.", "It provides the booting node with an IP address and the location of the boot server.", "It encrypts the boot image.", "It formats the local hard drive."],
        "correct": 1,
        "explanation": "DHCP (Dynamic Host Configuration Protocol) assigns an IP address to the node and provides the 'next-server' and boot filename required to start the PXE process."
    },
    {
        "question": "Which protocol is typically used to transfer the initial bootloader (like pxelinux or iPXE) during a network boot?",
        "options": ["HTTP", "FTP", "TFTP", "SSH"],
        "correct": 2,
        "explanation": "TFTP (Trivial File Transfer Protocol) is a simple, UDP-based protocol used to transfer the small initial bootloader because it requires minimal implementation in the network card's firmware."
    },
    {
        "question": "What is a 'stateless' compute node?",
        "options": ["A node that does not have an IP address.", "A node that boots its OS entirely into RAM from the network, maintaining no persistent local OS state.", "A node that cannot run MPI jobs.", "A node that is powered off."],
        "correct": 1,
        "explanation": "Stateless nodes run their OS from a RAM disk. Any changes made to the OS are lost upon reboot, ensuring the node always starts in a known, clean state."
    },
    {
        "question": "What is the primary function of Warewulf?",
        "options": ["To compile parallel code.", "To schedule jobs on a cluster.", "To provision and manage operating system images across a cluster of compute nodes.", "To monitor network traffic."],
        "correct": 2,
        "explanation": "Warewulf is an open-source cluster provisioning system that builds OS images and distributes them to compute nodes over the network."
    },
    {
        "question": "What is a VNFS in the context of Warewulf?",
        "options": ["Virtual Network Firewall System", "Virtual Node File System - the encapsulated OS image deployed to nodes.", "Volatile Node Failure State", "Verified Network File Share"],
        "correct": 1,
        "explanation": "The VNFS is the root filesystem image that Warewulf constructs and serves to the compute nodes during the boot process."
    },
    {
        "question": "What is the purpose of a 'chroot' environment when building cluster images?",
        "options": ["To change the root password.", "To create an isolated directory tree that acts as a separate root filesystem, allowing you to install and configure software for the nodes without affecting the head node.", "To compress the filesystem.", "To encrypt the hard drive."],
        "correct": 1,
        "explanation": "A chroot (change root) allows administrators to build and modify the OS image (the VNFS) in an isolated space on the head node before deploying it."
    },
    {
        "question": "Why is iPXE often used instead of standard PXE?",
        "options": ["It is older and more compatible.", "It supports booting over HTTP, which is much faster and more reliable than TFTP.", "It requires no DHCP server.", "It only works on wireless networks."],
        "correct": 1,
        "explanation": "iPXE extends traditional PXE capabilities, notably adding support for HTTP, which vastly speeds up the transfer of the large OS image compared to TFTP."
    },
    {
        "question": "What is a major advantage of diskless booting (stateless provisioning)?",
        "options": ["Nodes use more power.", "Every node is guaranteed to run the exact same, synchronized software image.", "It requires a hard drive in every node.", "It is immune to network failures."],
        "correct": 1,
        "explanation": "Because all nodes pull their OS from the same master image on the head node, software consistency across the cluster is absolutely guaranteed."
    },
    {
        "question": "In a Warewulf cluster, what generates the `/etc/hosts` file on the compute nodes?",
        "options": ["The user must manually write it on every node.", "Warewulf dynamically generates it based on its internal node database.", "It is downloaded from the internet.", "It is copied from the Windows domain controller."],
        "correct": 1,
        "explanation": "Warewulf acts as the source of truth and automatically generates cluster-wide configuration files like /etc/hosts using templates and its node database."
    },
    {
        "question": "What does the kernel payload do in the Warewulf boot process?",
        "options": ["It compiles C code.", "It provides the Linux kernel and initial RAM disk (initramfs) necessary to start the OS and mount the VNFS.", "It schedules jobs.", "It manages user passwords."],
        "correct": 1,
        "explanation": "The kernel payload is the first piece of Linux executed by the bootloader; it initializes hardware and pulls down the rest of the OS image."
    },
    {
        "question": "How does Warewulf handle node-specific configurations (like hostnames or IP addresses) if all nodes use the same image?",
        "options": ["It relies on users to set them after booting.", "It uses 'Overlays'—small, dynamically generated file archives applied over the base image at boot time.", "It creates a completely separate 10GB image for every single node.", "It doesn't; all nodes have the same hostname."],
        "correct": 1,
        "explanation": "Warewulf uses overlays to inject node-specific files (like network configs or hostnames) into the stateless image right as the node boots."
    },
    {
        "question": "What is the primary identifier used by the DHCP server to recognize a specific bare-metal compute node?",
        "options": ["Its CPU model.", "Its MAC address.", "Its hard drive serial number.", "Its BIOS version."],
        "correct": 1,
        "explanation": "The MAC address is a unique hardware identifier on the network card, used by DHCP and Warewulf to identify the node and assign its specific IP and image."
    },
    {
        "question": "If a stateless compute node reboots, what happens to temporary files written to `/tmp`?",
        "options": ["They are saved to the head node.", "They are preserved on the local hard drive.", "They are permanently lost because the filesystem exists only in RAM.", "They are emailed to the administrator."],
        "correct": 2,
        "explanation": "Stateless nodes run in a RAM disk (tmpfs). A reboot wipes the memory, destroying any local modifications or temporary files."
    },
    {
        "question": "Why must the head node have two network interfaces in a standard cluster design?",
        "options": ["To double the internet speed.", "One for the public external network, and one for the private internal cluster network.", "One for Windows and one for Linux.", "To provide a backup if one cable breaks."],
        "correct": 1,
        "explanation": "The head node bridges the outside world (public IP) and the isolated compute nodes (private network), acting as a gateway and NAT router."
    }
]

w4_q = [
    {
        "question": "What is the primary purpose of a resource manager/job scheduler like Slurm?",
        "options": ["To provision operating systems.", "To compile C code automatically.", "To arbitrate access to cluster resources, ensuring fair usage and efficient packing of jobs.", "To manage user passwords."],
        "correct": 2,
        "explanation": "Slurm manages the queue of user jobs, allocating compute nodes and starting tasks based on policies, priorities, and resource availability."
    },
    {
        "question": "What does a 'Partition' represent in Slurm?",
        "options": ["A division of a hard drive.", "A logical grouping of compute nodes, often functioning as a specific queue with distinct limits and access controls.", "A segmented network VLAN.", "A slice of a CPU core."],
        "correct": 1,
        "explanation": "Partitions in Slurm group nodes together (e.g., 'debug', 'gpu', 'batch') and define job limits like maximum runtime or node count."
    },
    {
        "question": "Which command is used to submit a batch script to Slurm?",
        "options": ["srun", "sbatch", "squeue", "sinfo"],
        "correct": 1,
        "explanation": "The 'sbatch' command parses a submission script, allocates resources, and runs the script in the background when resources become available."
    },
    {
        "question": "How does 'srun' differ from 'sbatch'?",
        "options": ["srun is used for compiling, sbatch is for running.", "srun submits a background job, sbatch runs interactively.", "srun executes a command in real-time, often interactively or as a step within a batch script, while sbatch submits a script for later execution.", "There is no difference."],
        "correct": 2,
        "explanation": "srun launches parallel tasks in real-time across allocated resources, whereas sbatch puts a script into the queue to run unattended."
    },
    {
        "question": "What command allows you to view the status of jobs in the Slurm queue?",
        "options": ["sview", "squeue", "sinfo", "sstat"],
        "correct": 1,
        "explanation": "The 'squeue' command lists the jobs currently running or waiting in the Slurm scheduling queue."
    },
    {
        "question": "If you submit a job by mistake, how do you stop it in Slurm?",
        "options": ["kill -9", "scancel <jobid>", "sstop <jobid>", "srm <jobid>"],
        "correct": 1,
        "explanation": "The 'scancel' command followed by the job ID will terminate a running or pending job."
    },
    {
        "question": "What is 'Fairshare' scheduling?",
        "options": ["A policy that gives all users exactly equal CPU time every day.", "An algorithm that adjusts job priority based on a user's historical resource usage compared to their allocated share.", "A system that shares memory between nodes.", "A licensing agreement for HPC software."],
        "correct": 1,
        "explanation": "Fairshare ensures long-term fairness. If a user has recently consumed a lot of resources, their priority drops, allowing users who haven't run jobs recently to move up the queue."
    },
    {
        "question": "What is the purpose of 'Backfill' scheduling?",
        "options": ["To fill empty hard drive space with random data.", "To allow smaller, shorter jobs to run immediately in the gaps left while the system waits for resources to free up for a massive job.", "To restart failed jobs automatically.", "To copy data from compute nodes back to the head node."],
        "correct": 1,
        "explanation": "Backfill drastically improves cluster utilization by fitting small jobs into idle nodes, provided they will finish before the nodes are needed for the next high-priority large job."
    },
    {
        "question": "Why must users accurately estimate the Wall Time (`--time`) for their jobs?",
        "options": ["If they underestimate, the job is killed; if they overestimate, it may delay backfill scheduling.", "Because Slurm charges them real money per hour.", "Because the CPU clock speed depends on the wall time.", "Because Slurm will randomly pause the job."],
        "correct": 0,
        "explanation": "Slurm strictly enforces the time limit (killing jobs that exceed it), but overestimating prevents the backfill scheduler from fitting the job into gaps, leaving it pending longer."
    },
    {
        "question": "What does the `sinfo` command display?",
        "options": ["Information about the user's account.", "The status and configuration of nodes and partitions in the cluster.", "The memory usage of a running job.", "The version of Slurm installed."],
        "correct": 1,
        "explanation": "The 'sinfo' command gives a high-level view of cluster state, showing which nodes are allocated, idle, or down, grouped by partition."
    },
    {
        "question": "What does the '#SBATCH' directive do in a script?",
        "options": ["It is a comment ignored by Slurm.", "It instructs the bash shell to execute the line.", "It provides resource requests and configuration flags to the Slurm scheduler.", "It defines a variable in Python."],
        "correct": 2,
        "explanation": "Slurm parses lines starting with #SBATCH to understand how many nodes, cores, and hours the job requires."
    },
    {
        "question": "What does a node state of 'drain' indicate in Slurm?",
        "options": ["The node is actively running jobs.", "The node is physically leaking coolant.", "The node is marked to accept no new jobs, usually pending maintenance or investigation of a hardware issue.", "The node is booting up."],
        "correct": 2,
        "explanation": "Draining a node prevents Slurm from scheduling new jobs on it, allowing current jobs to finish so the node can be safely taken offline."
    },
    {
        "question": "What is the role of the `slurmctld` daemon?",
        "options": ["It runs on compute nodes to launch tasks.", "It is the central controller running on the head node that manages state, queues, and allocations.", "It manages the database backend.", "It provides a web interface for users."],
        "correct": 1,
        "explanation": "The slurmctld (Slurm Control Daemon) is the brain of Slurm, managing the entire cluster's scheduling and state."
    },
    {
        "question": "What is the role of the `slurmd` daemon?",
        "options": ["It runs on compute nodes, awaiting instructions from the controller to launch tasks and monitor resources.", "It is the central controller.", "It generates billing reports.", "It provisions the operating system."],
        "correct": 0,
        "explanation": "slurmd runs on every compute node, acting as the worker daemon that executes tasks assigned by slurmctld."
    },
    {
        "question": "What is 'Exclusive' allocation in Slurm?",
        "options": ["A job that requires a special license to run.", "A job that is granted entire compute nodes, preventing any other user's jobs from sharing those nodes.", "A job that runs only on weekends.", "A job that uses all nodes in the cluster."],
        "correct": 1,
        "explanation": "Exclusive mode gives a job dedicated access to whole nodes, preventing performance interference from other users' processes."
    }
]

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
    },
    {
        "question": "What is the difference between GFLOPS and TFLOPS?",
        "options": ["GFLOPS is memory speed, TFLOPS is disk speed.", "GFLOPS is billions of FLOPs, TFLOPS is trillions of FLOPs.", "GFLOPS is for CPUs, TFLOPS is for GPUs.", "There is no difference."],
        "correct": 1,
        "explanation": "GigaFLOPS (10^9) represents billions of operations per second, while TeraFLOPS (10^12) represents trillions."
    },
    {
        "question": "What is 'Strong Scaling'?",
        "options": ["Increasing the problem size while keeping the number of processors constant.", "Keeping the overall problem size fixed while increasing the number of processors.", "Using stronger, faster processors.", "Scaling the network bandwidth."],
        "correct": 1,
        "explanation": "Strong scaling measures how the time to solve a fixed-size problem decreases as more processors are added."
    },
    {
        "question": "What is 'Weak Scaling'?",
        "options": ["Using older, slower processors.", "Keeping the problem size fixed while reducing processors.", "Increasing the problem size proportionally as the number of processors increases.", "Decreasing the memory bandwidth."],
        "correct": 2,
        "explanation": "Weak scaling measures efficiency when the workload per processor is kept constant, meaning the total problem size grows as you add nodes."
    },
    {
        "question": "According to Amdahl's Law, if 10% of a program is serial, what is the maximum theoretical speedup regardless of how many cores you use?",
        "options": ["10x", "100x", "Infinite", "2x"],
        "correct": 0,
        "explanation": "Amdahl's Law states Speedup = 1 / (Serial Fraction). 1 / 0.10 = 10. You can never achieve more than a 10x speedup."
    },
    {
        "question": "How does Gustafson's Law change the perspective of Amdahl's Law?",
        "options": ["It proves Amdahl wrong.", "It argues that as we get more processors, we don't solve the same problem faster; we solve a much larger problem in the same amount of time.", "It states that serial code doesn't exist.", "It focuses purely on GPU acceleration."],
        "correct": 1,
        "explanation": "Gustafson's Law relates to weak scaling, recognizing that researchers scale up the size of their simulations when given more computing power, reducing the impact of the serial portion."
    },
    {
        "question": "What is the primary cause of a 'cache miss'?",
        "options": ["The CPU clock speed is too fast.", "The data the CPU needs is not in the fast cache, forcing it to wait for a fetch from slower main memory.", "The program has a syntax error.", "The network cable is unplugged."],
        "correct": 1,
        "explanation": "Cache misses occur when data is not found in the L1/L2/L3 cache, resulting in significant CPU stall times while data is retrieved from RAM."
    },
    {
        "question": "What does a compiler optimization flag like `-O3` do?",
        "options": ["It deletes the source code.", "It applies aggressive automatic optimizations (like loop unrolling and vectorization) to make the executable run faster.", "It forces the code to run sequentially.", "It turns off all warnings."],
        "correct": 1,
        "explanation": "Compiler optimization flags instruct the compiler to spend more time analyzing the code to generate highly optimized, faster machine code."
    },
    {
        "question": "What is the 'Roofline Model'?",
        "options": ["A model for cluster cooling efficiency.", "A visual performance model that relates processor performance to off-chip memory traffic.", "A method for physical server rack layout.", "A pricing model for cloud HPC."],
        "correct": 1,
        "explanation": "The Roofline model shows whether an application is compute-bound (limited by the CPU's peak FLOPS) or memory-bound (limited by memory bandwidth)."
    },
    {
        "question": "What is HPCG (High Performance Conjugate Gradients)?",
        "options": ["A new type of graphics card.", "A benchmark designed to complement HPL by measuring memory bandwidth and irregular data access, which better represents modern scientific codes.", "A compiler flag.", "A file system."],
        "correct": 1,
        "explanation": "HPCG is a modern benchmark that stresses memory and network latency, providing a more realistic performance metric for memory-bound applications than HPL."
    },
    {
        "question": "What is 'OS Jitter' (or OS Noise) in HPC?",
        "options": ["Vibrations in the server rack.", "Small interruptions caused by background operating system tasks that can severely desynchronize tightly coupled parallel applications.", "Static on the network cables.", "Random crashes of the Slurm daemon."],
        "correct": 1,
        "explanation": "OS Jitter refers to the microsecond delays caused by OS interrupts (like cron jobs or network polling). In a cluster with thousands of nodes, these tiny delays compound and drastically reduce performance."
    },
    {
        "question": "What does it mean if an application is 'Memory Bound'?",
        "options": ["It uses too much hard drive space.", "Its performance is limited by how fast data can be delivered from RAM to the CPU, not by the CPU's calculating speed.", "It has a memory leak and will crash.", "It can only run on a single node."],
        "correct": 1,
        "explanation": "A memory-bound application spends most of its time waiting for data to arrive from memory because the CPU processes data faster than the RAM can supply it."
    },
    {
        "question": "What does it mean if an application is 'Compute Bound'?",
        "options": ["It is tied to a specific computer.", "Its performance is limited by the speed of the CPU's arithmetic logic units (FLOPS), not by memory delivery.", "It requires a calculator.", "It cannot use GPUs."],
        "correct": 1,
        "explanation": "A compute-bound application has plenty of data available in cache/registers and is purely limited by how fast the CPU can crunch the numbers."
    }
]

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
    },
    {
        "question": "What does `MPI_Bcast` do?",
        "options": ["Sends a message to a single specific node.", "Broadcasts a message from one 'root' process to all other processes in the communicator.", "Calculates the sum of arrays across all nodes.", "Closes the MPI environment."],
        "correct": 1,
        "explanation": "MPI_Bcast takes data from a root rank and efficiently copies it to all other ranks."
    },
    {
        "question": "What is a 'Race Condition' in shared memory programming?",
        "options": ["Two programs trying to finish first.", "A bug where the output depends on the unpredictable timing of threads accessing shared variables simultaneously without synchronization.", "The process of accelerating network traffic.", "A compiler optimization."],
        "correct": 1,
        "explanation": "Race conditions occur when multiple threads read and write to the same memory location concurrently, leading to corrupted or unpredictable results."
    },
    {
        "question": "What does `#pragma omp parallel for` do in C/C++?",
        "options": ["It runs the loop on a GPU.", "It tells the compiler to automatically divide the iterations of the following loop among a team of threads.", "It prevents the loop from running.", "It sends the loop over the network using MPI."],
        "correct": 1,
        "explanation": "This OpenMP directive is the easiest way to parallelize a standard loop in shared memory, handling thread creation, work distribution, and joining automatically."
    },
    {
        "question": "What is the difference between a blocking (`MPI_Send`) and non-blocking (`MPI_Isend`) call?",
        "options": ["Blocking stops the whole cluster; non-blocking stops one node.", "Blocking waits until the data is safely copied out of the send buffer; non-blocking returns immediately, allowing computation to overlap with communication.", "Blocking is for integers; non-blocking is for floats.", "Blocking requires a password."],
        "correct": 1,
        "explanation": "Non-blocking communication allows a program to initiate a data transfer and immediately continue crunching numbers, hiding network latency."
    },
    {
        "question": "What does `MPI_Scatter` do?",
        "options": ["It randomizes the data array.", "It takes a large array on the root node and slices it into equal chunks, sending one chunk to each process.", "It gathers data from all nodes into a single array.", "It deletes data to free up memory."],
        "correct": 1,
        "explanation": "Scatter is a collective operation used for data distribution, dealing out pieces of a master array to worker nodes."
    },
    {
        "question": "What does `MPI_Gather` do?",
        "options": ["It collects smaller arrays from all processes and concatenates them into a single large array on the root process.", "It scatters data to all nodes.", "It downloads data from the internet.", "It collects log files."],
        "correct": 0,
        "explanation": "Gather is the inverse of Scatter. It brings distributed results back together onto a single node for final processing or output."
    },
    {
        "question": "In MPI terminology, what is a 'Communicator' (e.g., `MPI_COMM_WORLD`)?",
        "options": ["The network cable.", "A group of processes that are allowed to communicate with each other.", "The router.", "A specialized hardware component."],
        "correct": 1,
        "explanation": "A communicator defines the context and the group of processes. MPI_COMM_WORLD includes all processes launched by the job."
    },
    {
        "question": "What do `MPI_Comm_rank` and `MPI_Comm_size` represent?",
        "options": ["Rank is the network speed; Size is the memory size.", "Rank is the unique ID (0 to N-1) of a process; Size is the total number of processes in the communicator.", "Rank is the CPU model; Size is the hard drive capacity.", "Rank is the priority; Size is the file size."],
        "correct": 1,
        "explanation": "Rank identifies 'who am I', and Size identifies 'how many of us are there'. These are fundamental to determining how work is divided."
    },
    {
        "question": "What is 'Deadlock' in message passing?",
        "options": ["When the server loses power.", "A situation where two or more processes are stuck forever, each waiting for a message from the other that will never arrive.", "When the hard drive is full.", "A security lock on a file."],
        "correct": 1,
        "explanation": "Deadlock is a critical parallel programming bug caused by mismatched sends and receives, bringing the execution to a permanent halt."
    },
    {
        "question": "Why use highly optimized numerical libraries like Intel MKL or BLAS instead of writing your own loops?",
        "options": ["They are easier to read.", "Hand-written loops rarely utilize processor features like vector instructions and cache hierarchies effectively, whereas libraries approach peak hardware performance.", "They use less memory.", "They don't require a compiler."],
        "correct": 1,
        "explanation": "Vendors spend years optimizing libraries (like BLAS for matrix math) at the assembly level to exploit specific cache sizes and SIMD registers."
    },
    {
        "question": "What is the FFTW library used for?",
        "options": ["Fast File Transfer over Wide-area networks.", "Computing discrete Fast Fourier Transforms efficiently.", "Formatting text output.", "Finding files on the filesystem."],
        "correct": 1,
        "explanation": "FFTW (Fastest Fourier Transform in the West) is the gold standard C subroutine library for computing the discrete Fourier transform (DFT)."
    },
    {
        "question": "What is a 'Barrier' in parallel programming?",
        "options": ["A firewall protecting the cluster.", "A synchronization point where all threads/processes must stop and wait until everyone has reached the barrier before anyone can proceed.", "A physical wall between server racks.", "A limit on memory usage."],
        "correct": 1,
        "explanation": "Barriers ensure that a specific phase of computation is completely finished by all workers before moving to the next phase."
    }
]

w7_q = [
    {
        "question": "What is the main advantage of 2D (Block) Decomposition over 1D (Slab) Decomposition in large parallel problems?",
        "options": ["It requires less memory per node.", "It minimizes the Surface-to-Volume ratio, thereby reducing communication overhead.", "It is easier to implement using 1D arrays.", "It eliminates the need for synchronization barriers."],
        "correct": 1,
        "explanation": "2D decomposition generally scales better because a block has a smaller perimeter-to-area (surface-to-volume) ratio, minimizing the amount of boundary data that must be communicated between processors."
    },
    {
        "question": "Which parallel motif is characterized by a central node dynamically distributing tasks to a pool of available nodes?",
        "options": ["Fork-Join", "Halo Exchange", "Manager-Worker (Task Farm)", "Divide and Conquer"],
        "correct": 2,
        "explanation": "In the Manager-Worker pattern, a single Manager maintains a pool of work and distributes tasks to Workers, providing excellent dynamic load balancing."
    },
    {
        "question": "In structured grid problems like CFD, what is the purpose of a 'Halo Exchange'?",
        "options": ["To offload computations to a GPU accelerator.", "To exchange boundary ghost cells with neighboring processors before the next compute step.", "To dynamically balance the load among unevenly matched workers.", "To divide a large matrix into smaller sub-matrices."],
        "correct": 1,
        "explanation": "Halo Exchange is used to synchronize boundary data (halos or ghost cells) between adjacent processors in grid-based simulations so they can compute their local updates."
    },
    {
        "question": "What does the 'Surface-to-Volume Ratio' represent in parallel algorithm design?",
        "options": ["The physical size of the CPU.", "The ratio of Communication (surface) to Computation (volume).", "The ratio of RAM to Hard Drive space.", "The ratio of network cables to server racks."],
        "correct": 1,
        "explanation": "Volume represents the useful computation done inside a data block, while Surface represents the overhead of communicating the boundaries. We want to maximize volume and minimize surface."
    },
    {
        "question": "What is Cannon's Algorithm used for?",
        "options": ["Sorting lists.", "Memory-efficient dense matrix multiplication on a 2D processor grid.", "Solving differential equations.", "Routing network packets."],
        "correct": 1,
        "explanation": "Cannon's algorithm avoids broadcasting large matrices by using a structured shift-and-multiply data flow across a grid of processors."
    },
    {
        "question": "How does the 'Divide and Conquer' parallel pattern work?",
        "options": ["It fires the manager.", "It recursively breaks a large problem into smaller sub-problems, solves them in parallel, and merges the results.", "It separates data from instructions.", "It puts half the CPUs to sleep to save power."],
        "correct": 1,
        "explanation": "Divide and conquer creates a dynamic tree of tasks, naturally exposing massive parallelism as the problem is recursively bisected."
    },
    {
        "question": "What is the 'Fork-Join' pattern?",
        "options": ["A method for eating pasta.", "A model where a main thread executes sequentially, spawns multiple worker threads for a parallel region, and then waits for them to finish.", "A way to combine two clusters.", "A network routing protocol."],
        "correct": 1,
        "explanation": "Fork-Join is the foundational pattern of OpenMP. The main thread forks to parallelize a loop or task, and joins at a barrier when the work is done."
    },
    {
        "question": "What does it mean if a problem is 'Embarrassingly Parallel'?",
        "options": ["The code is poorly written.", "The tasks are completely independent of each other and require zero communication to execute.", "The algorithm is too complex to understand.", "It requires a supercomputer to run."],
        "correct": 1,
        "explanation": "Embarrassingly parallel workloads (like Monte Carlo simulations or ray tracing) scale perfectly because workers never have to talk to each other."
    },
    {
        "question": "What is 'Load Balancing'?",
        "options": ["Ensuring physical servers weigh the same.", "Distributing work evenly across all processors so that no processor is sitting idle waiting for others to finish.", "Balancing network traffic across two cables.", "Distributing RAM evenly."],
        "correct": 1,
        "explanation": "Poor load balancing leads to idleness. The execution time of a parallel program is dictated by the slowest (most heavily loaded) processor."
    },
    {
        "question": "In Parallel Breadth-First Search (BFS), what is the 'Frontier'?",
        "options": ["The final result.", "The set of currently active nodes that are exploring their unvisited neighbors in parallel.", "The boundary of the cluster.", "The root node."],
        "correct": 1,
        "explanation": "Graph algorithms often proceed level-by-level. The frontier represents the active boundary of the search, expanding iteratively."
    },
    {
        "question": "What is 'Granularity' in parallel computing?",
        "options": ["The size of the hard drive platters.", "The ratio of computation to communication; i.e., how much work a task does before needing to communicate.", "The resolution of the monitor.", "The speed of the CPU clock."],
        "correct": 1,
        "explanation": "Fine-grained parallelism involves frequent communication of small data amounts, while coarse-grained parallelism involves infrequent communication of large chunks."
    },
    {
        "question": "Why might fine-grained parallelism perform poorly on a cluster?",
        "options": ["It uses too much RAM.", "The latency overhead of sending frequent, tiny messages over the network dominates the execution time.", "The CPUs get too hot.", "It requires specialized GPUs."],
        "correct": 1,
        "explanation": "Network latency is high compared to CPU speed. If tasks are too fine-grained, the CPUs spend more time waiting for the network than actually computing."
    },
    {
        "question": "What are 'Ghost Cells' (or Halos)?",
        "options": ["Deleted files.", "Extra memory allocated around a local grid block to hold copies of neighboring processors' boundary data.", "Hidden processes running in the background.", "Corrupted memory segments."],
        "correct": 1,
        "explanation": "Ghost cells allow a processor to compute a stencil operation (which requires neighbor data) locally without communicating for every single calculation."
    },
    {
        "question": "What is a 'Superlinear Speedup'?",
        "options": ["When an application crashes really fast.", "When a program runs more than N times faster on N processors, often due to the problem now fitting entirely into the combined L1/L2 caches.", "A marketing term for fast CPUs.", "When the network exceeds the speed of light."],
        "correct": 1,
        "explanation": "While rare, superlinear speedup occurs when dividing the problem shrinks the local data size so much that it fits entirely in ultra-fast CPU cache, bypassing RAM access penalties."
    },
    {
        "question": "What is the difference between Data Parallelism and Task Parallelism?",
        "options": ["Data parallelism is for hard drives, task parallelism is for CPUs.", "Data parallelism executes the same operation on different pieces of data; Task parallelism executes different operations concurrently.", "They are the same thing.", "Task parallelism is only used in Python."],
        "correct": 1,
        "explanation": "Applying a filter to every pixel in an image is Data Parallel. Having one thread read a file, another compress data, and a third write to disk is Task Parallel."
    }
]


# Combine all into a dictionary
all_quizzes = {
    1: w1_q,
    2: w2_q,
    3: w3_q,
    4: w4_q,
    5: w5_q,
    6: w6_q,
    7: w7_q
}

for week, questions in all_quizzes.items():
    file_path = f"Week {week} - "
    # Resolve exact folder name
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and f.startswith(f"Week {week} - ")]
    if not folders:
        print(f"Skipping week {week}, folder not found")
        continue
    folder = folders[0]
    html_file = os.path.join(folder, f"Week_{week}_Quiz.html")
    
    if not os.path.exists(html_file):
        print(f"File {html_file} not found.")
        continue
        
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We need to replace the content of `const questions = [ ... ];`
    # Let's use regex to find the block
    pattern = r"const questions\s*=\s*\[.*?(?:\}\s*\];|\}\s*\]\];)"
    
    new_questions_str = "const questions = " + json.dumps(questions, indent=12) + ";"
    
    # Escape backslashes for re.subn
    repl_str = new_questions_str.replace('\\', '\\\\')
    
    # Using re.sub with DOTALL
    new_content, count = re.subn(pattern, repl_str, content, flags=re.DOTALL)
    
    if count == 0:
        # Fallback if regex fails, which it might due to double brackets or formatting
        print(f"Regex failed for {html_file}. Trying split method.")
        try:
            parts1 = content.split("const questions = [")
            # the end of the array is usually followed by `let score = 0;`
            parts2 = parts1[1].split("let score = 0;")
            
            # parts2[0] ends with `];\n\n        ` or similar
            new_content = parts1[0] + "const questions = " + json.dumps(questions, indent=12) + ";\n\n        let score = 0;" + parts2[1]
        except Exception as e:
            print(f"Split method failed for {html_file}: {e}")
            continue
            
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Successfully updated {html_file} with {len(questions)} questions.")

