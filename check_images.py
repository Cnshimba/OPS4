import glob
import re

for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    images = re.findall(r'<img.*?>', content)
    diagrams = [img for img in images if 'alt="Icon"' not in img]
    if diagrams:
        print(f'--- {filepath} ---')
        for img in diagrams:
            print(img)
