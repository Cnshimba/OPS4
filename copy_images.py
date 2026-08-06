import os
import shutil
import glob

artifacts_dir = r"C:\Users\carlos\.gemini\antigravity-ide\brain\b8ec1968-b802-4654-9e4c-1dacb89a27b7"
target_dir = r"c:\Users\carlos\OneDrive - Vaal University of Technology\WORK\2026\OPS4_html\images"

files_to_copy = [
    "divide_conquer_tree",
    "manager_worker_diagram",
    "halo_exchange_diagram",
    "cannons_algorithm_diagram",
    "bfs_frontier_diagram",
    "beegfs_architecture",
    "lustre_architecture",
    "prometheus_architecture",
    "grafana_dashboard",
    "capstone_architecture_v2"
]

for base_name in files_to_copy:
    # Find the most recently generated file matching the base name
    pattern = os.path.join(artifacts_dir, f"{base_name}_*.png")
    matches = glob.glob(pattern)
    if matches:
        # Sort by modification time to get the newest one if multiple exist
        matches.sort(key=os.path.getmtime, reverse=True)
        newest_file = matches[0]
        
        target_path = os.path.join(target_dir, f"{base_name}.png")
        shutil.copy2(newest_file, target_path)
        print(f"Copied {os.path.basename(newest_file)} -> {target_path}")
    else:
        print(f"WARNING: Could not find artifact for {base_name}")
