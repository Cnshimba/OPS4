import os
import glob
import re

html_files = glob.glob('Week * - */Week_*_Student_Notes.html')

print(f"Found {len(html_files)} files.")

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Count code blocks
    code_blocks = len(re.findall(r'<pre><code', content))
    
    # Check for malformed tags
    heads = content.count('</head>')
    bodies = content.count('<body')
    navs = content.count('<nav')
    
    print(f"{f}: {code_blocks} code blocks, heads={heads}, bodies={bodies}, navs={navs}")
