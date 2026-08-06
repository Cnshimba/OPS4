import json

log_path = r"C:\Users\carlos\.gemini\antigravity-ide\brain\fec6e410-f7ae-412d-b68e-34c8f488cc94\.system_generated\logs\transcript.jsonl"
target_file = r"c:\Users\carlos\OneDrive - Vaal University of Technology\WORK\2026\OPS4_html\Week 3 - Node Provisioning\Week_3_Student_Notes.html"

with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

view_output = None
for line in reversed(lines):
    try:
        step = json.loads(line)
        if step.get("type") == "TOOL_RESPONSE" and step.get("tool_calls"):
            for call in step.get("tool_calls", []):
                if call.get("tool_name") == "default_api:view_file":
                    output = call.get("output", "")
                    if "Total Lines: 734" in output and "Showing lines 1 to 734" in output:
                        view_output = output
                        break
        if view_output:
            break
    except Exception as e:
        pass

if view_output:
    lines = view_output.split('\n')
    reconstructed = []
    for line in lines:
        if line.strip() and ": " in line:
            parts = line.split(": ", 1)
            if parts[0].isdigit():
                reconstructed.append(parts[1])
            else:
                if len(reconstructed) > 0: reconstructed.append(line)
        elif line.strip().isdigit() and line.endswith(":"):
            reconstructed.append("")
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(reconstructed))
    print(f"Restored {len(reconstructed)} lines.")
else:
    print("Could not find the view_file output in logs.")
