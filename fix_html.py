import os
import glob
import re

def fix_h1_and_head(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix duplicate </head>
    content = content.replace('</head>\n</head>', '</head>')

    # Fix H1: <h1 ...>Week X: Topic - Student Notes</h1> -> <h1 ...>Topic</h1>
    def h1_repl(match):
        prefix = match.group(1) # <h1 class="...">
        title = match.group(2)
        # remove "Week X: " and " - Student Notes"
        title = re.sub(r'^Week \d+:\s+', '', title)
        title = title.replace(' - Student Notes', '')
        return f'{prefix}{title}</h1>'
        
    content = re.sub(r'(<h1[^>]*>)(.*?)</h1>', h1_repl, content)

    # In Week 6, there are markdown code blocks inside HTML code blocks like:
    # <pre><code class="language-c">...
    # ```c
    # ...
    # </code></pre>
    # We need to clean this up. Basically, if there's ```c or ```python inside a <pre><code> block, we remove it.
    content = re.sub(r'```[a-z]*\n', '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
    fix_h1_and_head(filepath)
    print(f'Fixed {filepath}')

