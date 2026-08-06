import os
import glob
import re

def main():
    for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Reformat <blockquote><p><strong>Code Explanation</strong>: text</p></blockquote>
        def repl(match):
            text = match.group(1).strip()
            return f'<p class="text-sm text-slate-600 dark:text-slate-400 mt-2"><strong>Explanation:</strong> {text}</p>'
        
        new_content = re.sub(r'<blockquote>\s*<p><strong>Code Explanation</strong>:\s*(.*?)</p>\s*</blockquote>', repl, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Reformatted explanations in {filepath}')
            content = new_content

        # Count code blocks vs explanations
        code_blocks = len(re.findall(r'<pre><code', content))
        explanations = len(re.findall(r'<strong>Explanation:</strong>', content))
        
        if code_blocks > explanations:
            print(f'MISSING EXPLANATIONS in {filepath}: {code_blocks} blocks, {explanations} explanations')

if __name__ == "__main__":
    main()
