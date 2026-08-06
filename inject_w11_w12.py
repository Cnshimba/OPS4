import os
import re

new_los = {
    '11': """<div class="flex items-start p-4 my-4 rounded-lg border-l-4 shadow-sm bg-[#c9984a]/10 dark:bg-[#c9984a]/20 border-[#c9984a] text-slate-700 dark:text-slate-300"><svg class="w-6 h-6 mr-3 flex-shrink-0 text-[#c9984a]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 0 117.072 0l-.548 5.478a1 1 0 01-1.636 0L9.663 17z"></path></svg><div class="flex-1 text-sm md:text-base"><strong>Learning Outcomes</strong><br />By the end of this week, you should be able to:<br />
1. <strong>Evaluate</strong> the importance of cluster monitoring in maintaining high availability and performance.<br />
2. <strong>Analyze</strong> the architecture of Prometheus and its time-series data collection mechanisms.<br />
3. <strong>Design</strong> comprehensive Grafana dashboards to visualize cluster health metrics.<br />
4. <strong>Formulate</strong> alerting rules to proactively manage system anomalies.<br />
5. <strong>Critique</strong> different monitoring tools and justify their selection for specific operational needs.</div></div>""",

    '12': """<div class="flex items-start p-4 my-4 rounded-lg border-l-4 shadow-sm bg-[#c9984a]/10 dark:bg-[#c9984a]/20 border-[#c9984a] text-slate-700 dark:text-slate-300"><svg class="w-6 h-6 mr-3 flex-shrink-0 text-[#c9984a]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 0 117.072 0l-.548 5.478a1 1 0 01-1.636 0L9.663 17z"></path></svg><div class="flex-1 text-sm md:text-base"><strong>Learning Outcomes</strong><br />By the end of this week, you should be able to:<br />
1. <strong>Synthesize</strong> concepts from provisioning, resource management, and parallel programming into a unified cluster architecture.<br />
2. <strong>Design and deploy</strong> a fully functional HPC cluster from bare metal to a working batch scheduler.<br />
3. <strong>Evaluate</strong> the performance of the deployed cluster using standard benchmarking suites.<br />
4. <strong>Formulate</strong> troubleshooting strategies to resolve complex integration issues.<br />
5. <strong>Critique</strong> your architectural decisions and present a final technical report defending your design.</div></div>"""
}

assessment_text = """<div class="flex items-start p-4 my-4 rounded-lg border-l-4 shadow-sm bg-[#002F6E]/10 dark:bg-[#002F6E]/20 border-[#002F6E] text-slate-700 dark:text-slate-300"><svg class="w-6 h-6 mr-3 flex-shrink-0 text-[#002F6E]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg><div class="flex-1 text-sm md:text-base"><strong>Week Goal</strong><br />
Welcome to this week! 
<br /><br /><strong>Assessment Alignment:</strong> The weekly quiz and practical assignments for this module specifically evaluate the Learning Outcomes listed below, verifying your ability to operate at an NQF Level 7 standard of analysis and synthesis.</div></div>"""

def inject(week_num, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "Assessment Alignment:" in content:
        print(f"Already injected in {filepath}")
        return

    # Replace <hr />\n<h2>Overview</h2> with the blocks
    replacement = f"{assessment_text}\n{new_los[week_num]}\n<hr />\n<h2>Overview</h2>"
    content = content.replace("<hr />\n<h2>Overview</h2>", replacement)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Injected into {filepath}")

inject('11', 'Week 11 - Cluster Monitoring/Week_11_Student_Notes.html')
inject('12', 'Week 12 - Capstone Project/Week_12_Student_Notes.html')
