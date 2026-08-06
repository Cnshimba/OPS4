import glob
import re

for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace('src="images/', 'src="../images/')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed image paths in {filepath}')
