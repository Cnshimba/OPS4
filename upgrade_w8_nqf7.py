import os
import re
import json

notes_path = os.path.join("Week 8 - Advanced Storage Concepts", "Week_8_Student_Notes.html")

new_article_content = r"""
<div class="flex items-stretch bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm mb-8 overflow-hidden">
    <div class="w-48 flex-shrink-0 flex flex-col items-center justify-center bg-gray-100 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 p-4">
        <div class="w-32 h-32 rounded-full bg-primary border-4 border-secondary flex items-center justify-center shadow-lg mb-2 overflow-hidden">
            <img src="../images/week_8_icon.png" class="h-full w-full object-contain p-4 grayscale invert mix-blend-screen" alt="Icon">
        </div>
        <span class="text-sm font-black text-slate-400 uppercase tracking-widest">Week 8</span>
    </div>
    <div class="flex-1 flex flex-col items-center justify-center p-6 text-center">
        <h1 class="text-3xl font-bold text-secondary m-0">Advanced Storage Architectures</h1>
        <span class="text-lg font-medium text-gray-500 dark:text-gray-400 mt-1">HPC & Cluster Computing</span>
    </div>
</div>

<div class="flex items-start p-4 mb-8 rounded-lg border-l-4 shadow-sm bg-[#002F6E]/10 dark:bg-[#002F6E]/20 border-[#002F6E] text-slate-700 dark:text-slate-300">
    <svg class="w-6 h-6 mr-3 flex-shrink-0 text-[#002F6E]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
    <div class="flex-1 text-sm md:text-base">
        <p><strong>Course</strong>: Operating Systems 4 (HPC)<br /><strong>Module</strong>: EIOSY4A<br /><strong>Topic</strong>: Advanced HPC Storage Architectures (NQF 7)<br /><strong>Reading Time</strong>: ~30 Minutes</p>
    </div>
</div>
<hr />
<div class="flex items-start p-4 my-4 rounded-lg border-l-4 shadow-sm bg-[#c9984a]/10 dark:bg-[#c9984a]/20 border-[#c9984a] text-slate-700 dark:text-slate-300">
    <svg class="w-6 h-6 mr-3 flex-shrink-0 text-[#c9984a]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 0 117.072 0l-.548 5.478a1 1 0 01-1.636 0L9.663 17z"></path></svg>
    <div class="flex-1 text-sm md:text-base">
        <strong>Learning Outcomes</strong><br />By the end of this week, you should be able to:<br />
        1. <strong>Critique</strong> the applications of Block, File, and Object storage paradigms within HPC environments.<br />
        2. <strong>Evaluate</strong> the multi-tiered HPC storage hierarchy using queuing theory and Amdahl's Law applied to I/O.<br />
        3. <strong>Analyze</strong> strict POSIX semantics, Distributed Lock Managers (DLM), and why they fail at Exascale.<br />
        4. <strong>Compare</strong> the architectures of BeeGFS and Lustre, focusing on Distributed Namespaces (DNE), LNET routing, and NUMA awareness.<br />
        5. <strong>Appraise</strong> emerging non-POSIX storage frameworks, specifically DAOS (Distributed Asynchronous Object Storage).
    </div>
</div>
<hr />

<h2>Overview</h2>
<p>In Exascale computing, processing power is rarely the primary bottleneck. The true grand challenge of modern High Performance Computing is moving massive volumes of data from persistent storage to the CPU cache before the processors starve. This week, we analyze advanced storage architectures at a rigorous mathematical and protocol level. We will explore the breakdown of POSIX standards at scale, evaluate Parallel File Systems (BeeGFS and Lustre) under high-contention workloads, and investigate emerging memory-driven storage models like DAOS.</p>

<hr />

<h2>1. Mathematical Modeling of the I/O Bottleneck</h2>
<p>To understand why complex parallel file systems exist, we must first model the I/O problem mathematically.</p>

<h3>1.1 Amdahl's Law Applied to I/O</h3>
<p>Amdahl's Law is typically used to predict the theoretical speedup of parallelizing computational tasks. However, its most brutal application is in I/O. If a program runs infinitely fast on an infinite number of processors, the total execution time is strictly bound by the sequential I/O time.</p>
<p>Let $f_{io}$ be the fraction of execution time a program spends reading or writing data. The maximum theoretical speedup $S_{max}$ as the number of processors $N \to \infty$ is:</p>
<p>$$ S_{max} = \frac{1}{f_{io}} $$</p>
<p><strong>Example</strong>: If a computational fluid dynamics (CFD) simulation spends just 5% of its time dumping checkpoint data to disk ($f_{io} = 0.05$), the maximum speedup of that application—even on a million-core supercomputer—is capped at $20x$. Therefore, increasing compute density without proportionally scaling I/O bandwidth leads to catastrophic inefficiency. This is known as the "I/O Wall."</p>

<h3>1.2 Little's Law in Storage Queues</h3>
<p>When thousands of compute nodes simultaneously request data from a centralized storage server, a queuing network is formed. We model this using Little's Law:</p>
<p>$$ L = \lambda \times W $$</p>
<ul>
    <li>$L$: The average number of I/O requests pending in the storage system.</li>
    <li>$\lambda$: The arrival rate of requests (IOPS generated by the compute cluster).</li>
    <li>$W$: The average response time (latency) for an I/O request.</li>
</ul>
<p>As the cluster scales ($\lambda$ increases), if the storage system's service rate $\mu$ remains static, the utilization $\rho = \frac{\lambda}{\mu}$ approaches $1$. According to standard M/M/1 queuing theory, the wait time $W$ grows exponentially as $\rho \to 1$. To prevent this, HPC architects must design <strong>Scale-Out</strong> parallel file systems where $\mu$ scales linearly with $\lambda$.</p>

<hr />

<h2>2. POSIX Consistency and Distributed Lock Managers</h2>
<p>The Portable Operating System Interface (POSIX) standard dictates how a file system must behave. A key requirement is <strong>Strict Consistency</strong>: If Node A writes a byte to a file, Node B must immediately be able to read that updated byte. Achieving this across a distributed network of 10,000 nodes is incredibly complex.</p>

<h3>2.1 The Distributed Lock Manager (DLM)</h3>
<p>To enforce POSIX semantics, Parallel File Systems use a Distributed Lock Manager. When a node wants to write to a chunk of a file, it must request an exclusive lock from the metadata server.</p>
<ol>
    <li><strong>Request:</strong> Node A sends an RPC to the MDS requesting an exclusive write lock on File X, Byte Range [0-1024].</li>
    <li><strong>Revocation:</strong> If Node B holds a read lock on that range, the MDS must send an RPC to Node B to revoke the lock and invalidate Node B's local cache.</li>
    <li><strong>Grant:</strong> The MDS grants the exclusive lock to Node A.</li>
    <li><strong>Commit:</strong> Node A writes the data.</li>
</ol>
<p><strong>The Bottleneck:</strong> In N-to-1 write patterns (thousands of MPI processes writing to a single shared file), the DLM becomes paralyzed by "lock contention." The metadata server spends more time revoking and granting locks than actual data transfer occurs. This is why strict POSIX compliance is fundamentally hostile to Exascale computing.</p>

<hr />

<h2>3. Advanced Parallel File Systems: BeeGFS</h2>
<p>BeeGFS decouples Metadata from Data to circumvent standard storage bottlenecks. At an NQF 7 level, we must look at how it is optimized at the hardware and operating system levels.</p>

<h3>3.1 NUMA Awareness in Storage Daemons</h3>
<p>Modern servers utilize a Non-Uniform Memory Access (NUMA) architecture. A dual-socket server has two physical CPUs, each with its own local memory and local PCIe lanes connected to specific NVMe drives or InfiniBand network cards. If the <code>beegfs-storage</code> daemon running on CPU 0 processes a network request arriving on a NIC attached to CPU 1, the data must traverse the UPI (Ultra Path Interconnect) bus between the sockets, adding significant latency.</p>
<p>Advanced BeeGFS tuning requires pinning the <code>beegfs-storage</code> daemon, the IRQs (Interrupt Requests) of the InfiniBand card, and the target NVMe drives to the exact same NUMA node to achieve zero-copy DMA (Direct Memory Access).</p>

<p><img class="max-w-full h-auto max-h-[400px] object-contain rounded-lg shadow-sm mx-auto block" alt="BeeGFS Architecture Interactions" src="../images/beegfs_architecture.png" />
<br /><em>Figure 1: BeeGFS Architecture Interactions highlighting the decoupling of Metadata and Object Storage.</em></p>

<h3>3.2 Underlying Storage Targets (XFS vs. ZFS)</h3>
<p>A Parallel File System does not interface directly with raw disk platters; it stores its chunks on a local POSIX file system running on the storage node. The choice of underlying filesystem drastically alters performance:</p>
<ul>
    <li><strong>XFS:</strong> The industry standard for HPC storage targets. XFS utilizes highly efficient Allocation Groups (AGs), allowing massive parallel I/O within a single volume. It is lean, CPU-efficient, and optimized for high-throughput sequential writes.</li>
    <li><strong>ZFS:</strong> A Copy-on-Write (CoW) filesystem. While it provides incredible data integrity (checksumming) and easy snapshots, the CoW overhead and heavy RAM utilization (ARC cache) often result in severe IOPS degradation under heavy HPC workloads compared to XFS.</li>
</ul>

<hr />

<h2>4. Advanced Parallel File Systems: Lustre</h2>
<p>Lustre is the dominant kernel-space parallel file system in the Top500, designed for brutal scale. Its advanced features address the bottlenecks found in smaller file systems.</p>

<h3>4.1 Distributed Namespace (DNE)</h3>
<p>Historically, the single Metadata Server (MDS) was Lustre's Achilles' heel. Creating thousands of tiny files per second would saturate the MDS CPU and network interface. <strong>DNE (Distributed Namespace)</strong> solves this.</p>
<ul>
    <li><strong>DNE Phase 1 (Remote Directories):</strong> Allows different subdirectories to be hosted on entirely different MDS nodes (e.g., `/scratch/userA` on MDS1, `/scratch/userB` on MDS2).</li>
    <li><strong>DNE Phase 2 (Striped Directories):</strong> Allows a <em>single directory</em> containing millions of files to have its metadata striped across multiple MDS nodes simultaneously, providing linear scaling for metadata IOPS (essential for massive machine learning datasets).</li>
</ul>

<p><img class="max-w-full h-auto max-h-[400px] object-contain rounded-lg shadow-sm mx-auto block" alt="Lustre Architecture" src="../images/lustre_architecture.png" />
<br /><em>Figure 2: Lustre Architecture. Notice how clients bypass the MDS entirely once the file layout is negotiated.</em></p>

<h3>4.2 Lustre Networking (LNET) and RDMA</h3>
<p>Lustre does not use standard TCP/IP sockets for data transfer. It uses <strong>LNET (Lustre Networking)</strong>, a custom abstraction layer that supports <strong>RDMA (Remote Direct Memory Access)</strong> over InfiniBand or RoCE. RDMA allows an Object Storage Server (OSS) to push data directly into the RAM of a Compute Node client without interrupting the client's CPU. This zero-copy architecture is crucial for keeping latency in the microsecond range while sustaining terabytes per second of throughput.</p>

<hr />

<h2>5. The Post-POSIX Era: DAOS</h2>
<p>As we breach the Exascale barrier (10^18 calculations per second), the POSIX standard itself is becoming obsolete. The future of HPC storage relies on abandoning strict locks and hierarchical directories.</p>

<h3>5.1 DAOS (Distributed Asynchronous Object Storage)</h3>
<p>DAOS is an open-source software-defined object store built entirely in user space, completely bypassing the Linux Kernel block layer (which is too slow for modern NVMe drives). It is designed exclusively for Storage Class Memory (SCM, like Intel Optane) and NVMe flash.</p>
<ul>
    <li><strong>Byte-Granular I/O:</strong> Instead of dealing with 4KB block sizes, DAOS allows applications to read and write arbitrary byte sizes directly to persistent memory.</li>
    <li><strong>Versioned Object Store:</strong> Rather than using a DLM for lock arbitration, DAOS uses an epoch-based versioning system. Writes do not block reads; instead, the system creates a new version of the object, completely eliminating lock contention.</li>
    <li><strong>API Native:</strong> Modern HPC applications (like AI frameworks or HDF5) interface directly with the DAOS API rather than writing to a virtual filesystem, stripping away decades of legacy POSIX overhead.</li>
</ul>

<hr />

<h2>6. Summary</h2>
<p>At an NQF 7 level, storage is no longer viewed simply as "hard drives over a network." It is a complex distributed system bound by mathematical laws (Amdahl, Little). We explored the severe limitations of POSIX compliance at scale, the necessity of Distributed Lock Managers, and the architectural solutions provided by BeeGFS (NUMA targeting, XFS) and Lustre (DNE, LNET). Finally, we recognized that the true future of HPC lies in post-POSIX architectures like DAOS, which leverage RDMA and persistent memory to sustain Exascale workloads.</p>

<div class="mt-12 p-8 bg-[#002F6E]/10 dark:bg-[#002F6E]/20 rounded-xl border border-[#002F6E] text-center">
    <h3 class="text-2xl font-bold text-slate-900 dark:text-white mb-4">Test Your Knowledge</h3>
    <p class="text-slate-600 dark:text-slate-300 mb-6">Ready to check your understanding of advanced storage protocols, mathematical limits, and DLMs? Take the NQF 7 interactive quiz now!</p>
    <a href="Week_8_Quiz.html" class="inline-block px-8 py-3 bg-[#002F6E] hover:bg-[#002355] text-white font-bold rounded-lg transition-colors shadow-md no-underline">
        Start Quiz
    </a>
</div>
"""

if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    start_tag = '<article class="prose'
    start_idx = html.find(start_tag)
    end_of_start_tag = html.find(">", start_idx) + 1
    
    end_tag = "</article>"
    end_idx = html.rfind(end_tag)
    
    if start_idx != -1 and end_idx != -1:
        new_html = html[:end_of_start_tag] + "\n" + new_article_content + "\n        " + html[end_idx:]
        with open(notes_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Successfully upgraded content to NQF 7 in {notes_path}")
    else:
        print("Could not find insertion points.")
else:
    print(f"Could not find {notes_path}")
