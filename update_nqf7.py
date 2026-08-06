import glob
import re
import os

new_los = {
    '1': """<br />By the end of this week, you should be able to:<br />
1. <strong>Critique</strong> the definition of High Performance Computing relative to standard IT infrastructure in complex environments.<br />
2. <strong>Evaluate</strong> the role and impact of the South African HPC ecosystem (CHPC, DIRISA, SANReN) on regional research.<br />
3. <strong>Analyze</strong> cluster performance using FLOPS and interpret top-tier benchmarking standards (Top500).<br />
4. <strong>Contrast and evaluate</strong> the Von Neumann and Harvard architectures in the context of modern supercomputing.<br />
5. <strong>Formulate</strong> strategies to mitigate the Memory Wall problem using advanced cache hierarchies.<br />
6. <strong>Classify</strong> parallel computing systems critically using Flynn's Taxonomy.<br />
7. <strong>Apply and analyze</strong> Amdahl's Law and Gustafson's Law to predict parallel speedup bounds.</p>""",

    '2': """<br />By the end of this week, you should be able to:<br />
1. <strong>Analyze</strong> the "Beowulf" approach to cluster design and its economic viability.<br />
2. <strong>Evaluate and compare</strong> high-performance network topologies (Fat Tree vs. Torus) for specific computational workloads.<br />
3. <strong>Critique</strong> the OpenHPC Reference Architecture for modern data center deployments.<br />
4. <strong>Design</strong> the integration of core cluster services required for diskless operations.</p>""",

    '3': """<br />By the end of this week, you should be able to:<br />
1. <strong>Evaluate</strong> the benefits and architectural implications of stateless provisioning in enterprise HPC clusters.<br />
2. <strong>Analyze</strong> Warewulf 4's architecture and its integration with OCI-standard containers.<br />
3. <strong>Deploy and configure</strong> complex nodes, profiles, and overlays using the wwctl command-line tool.<br />
4. <strong>Design</strong> dynamic, per-node customizations of generic container images using system overlays.</p>""",

    '4': """<br />By the end of this week, you should be able to:<br />
1. <strong>Justify</strong> the necessity of advanced workload managers in multi-tenant, shared HPC environments.<br />
2. <strong>Analyze</strong> the architectural components and daemon interactions within Slurm.<br />
3. <strong>Manage</strong> job lifecycles by submitting, monitoring, and debugging complex batch scripts.<br />
4. <strong>Formulate</strong> optimized <code>sbatch</code> scripts with precise resource allocation directives.<br />
5. <strong>Evaluate</strong> how Slurm partitions, Quality of Service (QOS), and priority algorithms influence job scheduling fairness.</p>""",

    '5': """<br />By the end of this week, you should be able to:<br />
1. <strong>Analyze</strong> key HPC performance constraints including FLOPs, memory bandwidth, and network latency.<br />
2. <strong>Apply</strong> the Roofline Model to diagnose and classify computational codes as compute-bound or memory-bound.<br />
3. <strong>Execute and evaluate</strong> the HPL benchmark, interpreting its practical results against theoretical Rpeak.<br />
4. <strong>Critique</strong> memory bandwidth limitations by analyzing STREAM benchmark outputs.<br />
5. <strong>Formulate</strong> basic code optimization strategies utilizing compiler flags and specialized numerical libraries.</p>""",

    '6': """<br />By the end of this week, you should be able to:<br />
1. <strong>Evaluate</strong> the architectural trade-offs between Shared Memory (OpenMP) and Distributed Memory (MPI) paradigms.<br />
2. <strong>Predict and analyze</strong> the upper theoretical limits of parallel scaling using Amdahl's Law.<br />
3. <strong>Implement</strong> OpenMP directives (parallel for, reduction, critical) to parallelize serial code blocks.<br />
4. <strong>Design</strong> distributed memory applications using the MPI SPMD model, communicators, and point-to-point operations.<br />
5. <strong>Diagnose and resolve</strong> complex concurrent programming flaws, including race conditions and deadlocks.</p>""",

    '7': """<br />By the end of this week, you should be able to:<br />
1. <strong>Analyze</strong> parallel algorithms based on Work, Span, and Cost Optimality metrics.<br />
2. <strong>Design</strong> parallel solutions by applying rigorous Domain and Functional Decomposition strategies.<br />
3. <strong>Evaluate</strong> the suitability of Fork-Join, Divide-and-Conquer, and Manager-Worker patterns for various workloads.<br />
4. <strong>Optimize</strong> communication overhead by applying the surface-to-volume ratio principle.<br />
5. <strong>Trace and critique</strong> the execution flows of advanced algorithms (Halo Exchange, Cannon's Algorithm, BFS).</p>""",

    '8': """<br />By the end of this week, you should be able to:<br />
1. <strong>Critique</strong> the applications of Block, File, and Object storage paradigms within HPC environments.<br />
2. <strong>Evaluate</strong> the multi-tiered HPC storage hierarchy, from NVMe burst buffers to deep archive.<br />
3. <strong>Configure</strong> NFS exports and analyze its scalability limitations in massively parallel systems.<br />
4. <strong>Analyze</strong> the architectures of BeeGFS and Lustre, focusing on striping mechanics and metadata separation.<br />
5. <strong>Select and execute</strong> appropriate benchmarking tools (IOR vs mdtest) to evaluate throughput and IOPS.</p>""",

    '9': """<br />By the end of this week, you should be able to:<br />
1. <strong>Evaluate</strong> Heterogeneous Computing models and justify the use of GPUs for massively parallel workloads.<br />
2. <strong>Analyze</strong> deep GPU architectural features including Streaming Multiprocessors, the SIMT model, and warp scheduling.<br />
3. <strong>Design</strong> parallel kernels using the CUDA programming model, mapping threads, blocks, and grids.<br />
4. <strong>Critique</strong> the specific HPC use cases for FPGAs and specialized ASICs versus general-purpose GPUs.<br />
5. <strong>Analyze</strong> the PCIe data transfer bottleneck and formulate strategies to minimize host-to-device latency.</p>""",

    '10': """<br />By the end of this week, you should be able to:<br />
1. <strong>Analyze</strong> the computational requirements and HPC resource utilization of Computational Fluid Dynamics (CFD) applications.<br />
2. <strong>Evaluate</strong> the role and integration of bioinformatics pipelines (e.g., BLAST, GATK) in genomic research.<br />
3. <strong>Contrast</strong> the architectural demands of modern AI/ML workloads (PyTorch, TensorFlow) against traditional HPC simulations.<br />
4. <strong>Design</strong> multi-step scientific pipelines using advanced workflow managers.<br />
5. <strong>Select and justify</strong> specific scheduler directives and software tools tailored to distinct scientific domains.</p>""",

    '11': """<br />By the end of this week, you should be able to:<br />
1. <strong>Evaluate</strong> the importance of cluster monitoring in maintaining high availability and performance.<br />
2. <strong>Analyze</strong> the architecture of Prometheus and its time-series data collection mechanisms.<br />
3. <strong>Design</strong> comprehensive Grafana dashboards to visualize cluster health metrics.<br />
4. <strong>Formulate</strong> alerting rules to proactively manage system anomalies.<br />
5. <strong>Critique</strong> different monitoring tools and justify their selection for specific operational needs.</p>""",

    '12': """<br />By the end of this week, you should be able to:<br />
1. <strong>Synthesize</strong> concepts from provisioning, resource management, and parallel programming into a unified cluster architecture.<br />
2. <strong>Design and deploy</strong> a fully functional HPC cluster from bare metal to a working batch scheduler.<br />
3. <strong>Evaluate</strong> the performance of the deployed cluster using standard benchmarking suites.<br />
4. <strong>Formulate</strong> troubleshooting strategies to resolve complex integration issues.<br />
5. <strong>Critique</strong> your architectural decisions and present a final technical report defending your design.</p>"""
}

# The assessment text
assessment_text = "<br /><br /><strong>Assessment Alignment:</strong> The weekly quiz and practical assignments for this module specifically evaluate the Learning Outcomes listed below, verifying your ability to operate at an NQF Level 7 standard of analysis and synthesis."

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine week number from filename (e.g. Week_1_Student_Notes.html)
    match = re.search(r'Week_(\d+)_Student_Notes', filepath)
    if not match: return
    week_num = match.group(1)
    
    if week_num not in new_los: return
    
    modified = False

    # 1. Update Learning Outcomes
    # Search for the block starting with <strong>Learning Outcomes</strong><br />
    lo_match = re.search(r'(<strong>Learning Outcomes</strong>)(.*?)(</div>)', content, re.DOTALL)
    if lo_match:
        old_lo = lo_match.group(2)
        content = content.replace(old_lo, new_los[week_num])
        modified = True
    else:
        # If Week 11 or 12 don't have it, we need to inject the whole block
        # We'll inject it right after the Week Goal block
        goal_match = re.search(r'<strong>Week Goal</strong>.*?</div></div>', content, re.DOTALL)
        if goal_match:
            lo_block = f"""
<div class="flex items-start p-4 my-4 rounded-lg border-l-4 shadow-sm bg-[#c9984a]/10 dark:bg-[#c9984a]/20 border-[#c9984a] text-slate-700 dark:text-slate-300"><svg class="w-6 h-6 mr-3 flex-shrink-0 text-[#c9984a]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 0 117.072 0l-.548 5.478a1 1 0 01-1.636 0L9.663 17z"></path></svg><div class="flex-1 text-sm md:text-base"><strong>Learning Outcomes</strong>{new_los[week_num]}</div></div>
"""
            content = content.replace(goal_match.group(0), lo_block + goal_match.group(0))
            modified = True

    # 2. Inject Assessment Alignment into Week Goal
    # Find the Week Goal div ending
    goal_match = re.search(r'(<strong>Week Goal</strong>.*?)(</div></div>)', content, re.DOTALL)
    if goal_match:
        # Avoid duplicate injections
        if "Assessment Alignment" not in goal_match.group(1):
            content = content.replace(goal_match.group(0), goal_match.group(1) + assessment_text + goal_match.group(2))
            modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {filepath}')

for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
    process_file(filepath)
