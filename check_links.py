import glob
import os
import re

for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
    # Remove 'Back to Course Index'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(r'<p><a href="\.\./OPS4_COURSE_STRUCTURE\.md">← Back to Course Index</a></p>', '', content)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Removed Back to Course Index from {filepath}')
    
    # Check if quiz exists
    match = re.search(r'href="(Week_\d+_Quiz\.html)"', content)
    if match:
        quiz_file = match.group(1)
        dir_name = os.path.dirname(filepath)
        quiz_path = os.path.join(dir_name, quiz_file)
        if not os.path.exists(quiz_path):
            print(f'ERROR: Quiz file missing: {quiz_path}')
        else:
            print(f'OK: Quiz found: {quiz_path}')
    else:
        print(f'WARNING: No quiz link found in {filepath}')
