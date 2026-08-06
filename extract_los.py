import glob
import re

for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Learning Outcomes section. It usually looks like:
    # <strong>Learning Outcomes</strong><br />...</div>
    match = re.search(r'<strong>Learning Outcomes</strong>(.*?)</div>', content, re.DOTALL)
    if match:
        los = match.group(1).strip()
        # Clean up HTML tags for readability in the log
        los = re.sub(r'<br\s*/?>', '\n', los)
        los = re.sub(r'</p>', '', los)
        print(f'--- {filepath} ---')
        print(los)
        print('\n')
