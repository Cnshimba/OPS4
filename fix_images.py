import glob
import re

standard_class = 'max-w-full h-auto max-h-[400px] object-contain rounded-lg shadow-sm'

def fix_image_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def repl(match):
        img_tag = match.group(0)
        # Skip icon images
        if 'alt="Icon"' in img_tag or '_icon.png' in img_tag:
            return img_tag
        
        # Remove any existing class attribute
        img_tag = re.sub(r'\s*class="[^"]*"', '', img_tag)
        
        # Insert the standard class right after <img
        new_tag = img_tag.replace('<img', f'<img class="{standard_class}"')
        return new_tag

    new_content = re.sub(r'<img.*?>', repl, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed images in {filepath}')

for filepath in glob.glob('Week * - */Week_*_Student_Notes.html'):
    fix_image_tags(filepath)

