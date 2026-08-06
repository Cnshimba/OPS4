import os
import re
import json

notes_path = os.path.join("Week 11 - Cluster Monitoring", "Week_11_Student_Notes.html")

additional_w11_content = """
<hr />
<h2>5. Deep Dive: PromQL (Prometheus Query Language)</h2>
<p>To truly utilize Prometheus, an administrator must master its native query language, <strong>PromQL</strong>. Unlike SQL, which queries rows in tables, PromQL queries multi-dimensional time series data.</p>

<h3>5.1 Basic PromQL Queries</h3>
<ul>
    <li><strong>Instant Vector:</strong> Returns a single value for each time series. For example, <code>node_cpu_seconds_total</code> returns the total CPU time consumed since boot.</li>
    <li><strong>Range Vector:</strong> Returns a set of values over a time range. Useful for calculating rates. For example, <code>node_cpu_seconds_total[5m]</code> returns the data points collected over the last 5 minutes.</li>
</ul>

<h3>5.2 Calculating Rates (The Most Common Query)</h3>
<p>Because many metrics are <em>counters</em> (they only go up, like total bytes sent), you usually want to know the <em>rate of increase</em> per second (e.g., bandwidth). You do this using the <code>irate()</code> or <code>rate()</code> functions.</p>
<pre><code># Calculate CPU usage percentage per core over the last 5 minutes:
100 - (avg by (cpu) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)</code></pre>
<p>This query takes the rate of the "idle" mode CPU counter, averages it by CPU core, and subtracts it from 100 to get the active utilization.</p>

<hr />

<h2>6. Practical Alerting with Alertmanager</h2>
<p>Monitoring is only useful if it wakes you up when something goes wrong. Alertmanager handles grouping, inhibiting, and routing alerts.</p>

<h3>6.1 Defining Alert Rules</h3>
<p>Rules are defined in YAML format on the Prometheus server. If the PromQL expression evaluates to true for a given duration, the alert fires.</p>
<pre><code>groups:
- name: NodeAlerts
  rules:
  - alert: HighCPULoad
    expr: node_load1 > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Instance {{ $labels.instance }} under high load"</code></pre>
<p>This rule checks if the 1-minute load average (<code>node_load1</code>) exceeds 10 for 5 consecutive minutes. If so, it sends a Warning alert.</p>

<h3>6.2 Alert Routing</h3>
<p>Once Alertmanager receives the <code>HighCPULoad</code> alert, it looks at its routing tree. It might send "warning" severity alerts to a Slack channel, but "critical" alerts (like an entire rack losing power) to a PagerDuty system to wake up an on-call engineer.</p>

<hr />
"""

if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # We will inject the new content right before "<h2>5. Summary and Next Steps</h2>"
    # Actually the existing section is <h2>5. Summary and Next Steps</h2>
    # We will replace it with 7. Summary and Next Steps, and inject our sections 5 and 6 before it.
    
    html = html.replace("<h2>5. Summary and Next Steps</h2>", additional_w11_content + "\n<h2>7. Summary and Next Steps</h2>")
    
    with open(notes_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully expanded content in {notes_path}")
else:
    print(f"Could not find {notes_path}")

# Now generate the Quiz for Week 11
w11_q = [
    {
        "question": "What does the acronym RAS stand for in the context of HPC System Administration?",
        "options": ["Random Access Storage", "Reliability, Availability, Serviceability", "Remote Administration System", "Rapid Application Scaling"],
        "correct": 1,
        "explanation": "RAS (Reliability, Availability, Serviceability) represents the primary goals of maintaining an enterprise or HPC system."
    },
    {
        "question": "According to the Utilization Law (U = λ/μ), what happens to queue wait times as cluster utilization (U) approaches 100%?",
        "options": ["Wait times become zero.", "Wait times grow exponentially.", "Wait times remain constant.", "Wait times decrease."],
        "correct": 1,
        "explanation": "In queueing theory, as a system reaches 100% saturation (U=1), the length of the queue and the wait time grow towards infinity."
    },
    {
        "question": "What is a primary difference between Legacy monitoring (e.g., Nagios) and Modern monitoring (e.g., Prometheus)?",
        "options": ["Legacy focuses on 'How is it running?', Modern focuses on 'Is it up?'", "Legacy monitoring focuses on binary states (Up/Down), while modern monitoring uses Time-Series databases to track metric changes over time.", "Legacy monitoring uses graphics, Modern uses only text.", "There is no difference."],
        "correct": 1,
        "explanation": "Prometheus shifts the focus to metrics over time rather than simple ping checks, allowing for trend analysis."
    },
    {
        "question": "Prometheus utilizes a 'Pull' architecture. What does this mean?",
        "options": ["Nodes forcefully push their data to the server.", "The server wakes up at specific intervals and requests (scrapes) data from the nodes.", "The server pulls cables to restart nodes.", "Data is pulled directly from the internet."],
        "correct": 1,
        "explanation": "In a Pull model, the central server initiates the HTTP request to scrape the metrics from the node exporters."
    },
    {
        "question": "What is the role of an 'Exporter' in the Prometheus ecosystem?",
        "options": ["It exports data to a CSV file.", "It is a lightweight binary running on a node that collects local metrics and exposes them on a web endpoint for the server to scrape.", "It deletes old data to save disk space.", "It alerts users via email."],
        "correct": 1,
        "explanation": "Exporters (like node_exporter) translate local system states into the Prometheus metric format and host them via HTTP."
    },
    {
        "question": "What does TSDB stand for?",
        "options": ["Time-Series Database", "Terminal System Data Bus", "Total Storage Data Block", "Technical System Debugging Binary"],
        "correct": 0,
        "explanation": "A Time-Series Database is optimized for handling data indexed by time, tracking how values change over seconds, minutes, or days."
    },
    {
        "question": "Which tool is commonly paired with Prometheus to act as a 'Single Pane of Glass' for visualization?",
        "options": ["Warewulf", "Slurm", "Grafana", "BeeGFS"],
        "correct": 2,
        "explanation": "Grafana connects to Prometheus and turns raw time-series data into actionable dashboards with graphs, gauges, and heatmaps."
    },
    {
        "question": "What is the primary benefit of using a Heatmap visualization in an HPC cluster?",
        "options": ["To show the exact temperature of the CPU in Celsius.", "To instantly reveal outliers and distributions across hundreds of nodes (e.g., finding one node acting differently than the rest).", "To print data to paper.", "To replace the terminal interface."],
        "correct": 1,
        "explanation": "Heatmaps excel at displaying the distribution of a metric across a massive number of targets, making outliers visually obvious."
    },
    {
        "question": "What is PromQL?",
        "options": ["Prometheus Queueing Logic", "A SQL database for Prometheus.", "Prometheus Query Language, used to query multi-dimensional time series data.", "A programming language for writing CFD applications."],
        "correct": 2,
        "explanation": "PromQL allows administrators to filter, aggregate, and perform math (like calculating rates) on the metrics stored in Prometheus."
    },
    {
        "question": "In PromQL, why is the 'irate()' or 'rate()' function used on counters?",
        "options": ["To reset the counter to zero.", "Because counters only go up (like an odometer), you use rate() to calculate the speed or rate of increase per second.", "To delete the metric.", "To generate a random number."],
        "correct": 1,
        "explanation": "A counter tells you total bytes transferred since boot. Applying rate() tells you the current bandwidth in bytes per second."
    },
    {
        "question": "What is the role of the Prometheus Alertmanager?",
        "options": ["It generates graphs.", "It restarts crashed nodes automatically.", "It receives alert signals from Prometheus, groups them, and routes them to receivers like Slack, Email, or PagerDuty.", "It prevents users from logging in."],
        "correct": 2,
        "explanation": "Alertmanager handles the silencing, grouping, and routing of alerts so administrators don't suffer from alert fatigue."
    },
    {
        "question": "In a Prometheus alert rule, what does the 'for: 5m' clause do?",
        "options": ["It waits 5 months before alerting.", "It ensures the condition (e.g., high load) remains true for 5 consecutive minutes before firing the alert, preventing false positives from temporary spikes.", "It shuts the node down for 5 minutes.", "It sends the alert 5 times."],
        "correct": 1,
        "explanation": "The 'for' duration is critical to avoid spamming alerts for transient issues."
    },
    {
        "question": "What is IPMI (Intelligent Platform Management Interface)?",
        "options": ["A protocol for sending emails.", "A standard interface allowing administrators to manage and monitor hardware (like fans, voltage, power states) directly via a BMC, even if the OS is crashed or powered off.", "A file system for storing user data.", "A scheduling algorithm."],
        "correct": 1,
        "explanation": "IPMI operates Out-Of-Band via the Baseboard Management Controller (BMC), providing physical hardware control independent of the host OS."
    },
    {
        "question": "Why is a Push architecture considered risky for monitoring a massive HPC cluster?",
        "options": ["Because data gets encrypted.", "Because if 1000 nodes push their data to the server at the exact same millisecond, they can inadvertently DDoS and crash the monitoring server.", "Because it uses too much electricity.", "Because Push architecture is illegal."],
        "correct": 1,
        "explanation": "Pull architecture allows the server to dictate the pace of data ingestion, preventing overload."
    },
    {
        "question": "If you observe that cluster disk I/O spikes every time the CPU usage drops significantly, what pattern have you recognized?",
        "options": ["A network failure.", "A likely I/O bottleneck, where the CPU is sitting idle (I/O Wait) waiting for the storage system to respond.", "A perfectly optimized application.", "An IPMI alert."],
        "correct": 1,
        "explanation": "Correlating metrics allows you to diagnose bottlenecks. If CPU drops when disk usage spikes, the CPUs are starved for data."
    }
]

def create_w11_quiz():
    week = 11
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
    new_questions_str = "const questions = " + json.dumps(w11_q, indent=12) + ";"
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

create_w11_quiz()
