import os

notes_path = os.path.join("Week 10 - HPC Applications", "Week_10_Student_Notes.html")

additional_w10_content = """
<hr />

<h2>6. Engineering and Finite Element Analysis (FEA)</h2>
<p>Beyond fluids (CFD), HPC is heavily utilized in structural engineering and manufacturing. Before a physical car is ever built, it is crashed thousands of times in a supercomputer.</p>

<h3>6.1 Crash Simulations (LS-DYNA)</h3>
<p>Finite Element Analysis (FEA) breaks a solid object (like a car chassis) into a mesh of finite elements. Software like <strong>LS-DYNA</strong> simulates how these elements deform, transfer energy, and break upon impact over milliseconds.</p>

<h3>6.2 HPC Workload Profile for FEA</h3>
<ul>
    <li><strong>Parallel Model:</strong> MPI for domain decomposition (distributing parts of the car to different nodes).</li>
    <li><strong>Hardware Demands:</strong> Highly reliant on high CPU clock speeds and low-latency networking. Unlike CFD, structural meshes can become highly distorted during a crash, requiring complex dynamic load balancing across the cluster.</li>
</ul>

<hr />

<h2>7. Cyber Security and Cryptography</h2>
<p>HPC plays a dual role in Cyber Security: acting as the ultimate weapon to break encryption, and the ultimate shield to analyze massive streams of network traffic.</p>

<h3>7.1 Cryptanalysis and Password Cracking (Hashcat)</h3>
<p>Brute-forcing encryption keys or cracking hashed passwords involves performing the same mathematical hash function (e.g., SHA-256) billions of times per second.</p>
<ul>
    <li><strong>Parallel Model:</strong> Purely Embarrassingly Parallel. No nodes need to talk to each other; they just need to try different combinations.</li>
    <li><strong>Hardware Demands:</strong> <strong>Extreme GPU Density</strong>. Tools like <em>Hashcat</em> leverage the thousands of ALUs in GPUs. A specialized password-cracking cluster will often feature 8 to 10 GPUs per node with minimal RAM or networking infrastructure.</li>
</ul>

<h3>7.2 Large-Scale Network Anomaly Detection</h3>
<p>National security agencies and large ISPs capture petabytes of network flow data. Using frameworks like Apache Spark or Hadoop on HPC clusters, they apply machine learning algorithms to detect subtle anomalies indicative of advanced persistent threats (APTs).</p>

<hr />

<h2>8. Computer Systems Engineering (EDA)</h2>
<p>How do you design a new CPU like an Apple M3 or NVIDIA H100 that has 80 billion transistors? You use a supercomputer to simulate the supercomputer you are building.</p>

<h3>8.1 Electronic Design Automation (EDA)</h3>
<p>EDA tools simulate the electrical timing, logic gates, and thermal properties of a silicon chip before it is sent to a fabrication plant. This process is called RTL (Register-Transfer Level) Simulation.</p>

<h3>8.2 HPC Workload Profile for EDA</h3>
<ul>
    <li><strong>Hardware Demands:</strong> <strong>Massive RAM and Fast Storage</strong>. Unlike many other physics simulations, EDA workloads are notoriously difficult to parallelize across multiple nodes because a chip's logic is highly interconnected. Therefore, EDA heavily relies on <em>Scale-Up</em> servers (Fat Nodes) with extremely high single-thread CPU performance and massive amounts of RAM (2TB+) to hold the entire chip design in memory.</li>
    <li><strong>Storage:</strong> High IOPS (Input/Output Operations Per Second) are required for reading massive standard cell libraries.</li>
</ul>
"""

if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # We want to replace "<h2>6. Summary</h2>" with our new sections and shift summary to 9
    
    # Fix the existing Summary heading if it exists
    html = html.replace("<h2>6. Summary</h2>", additional_w10_content + "\n<h2>9. Summary</h2>")
    
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully added more content to {notes_path}")
else:
    print(f"Could not find {notes_path}")
