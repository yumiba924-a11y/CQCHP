import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Collapse 3+ consecutive blank lines into max 2
css_new = re.sub(r'\n{4,}', '\n\n\n', css)
# Also collapse 2 consecutive blank lines following a "}" into 1 (within sections)
# More conservatively: just collapse 3+ → 2 (one blank between rules is OK)
css_new = re.sub(r'\n\n\n+', '\n\n', css_new)

with open('assets/css/style.css', 'w', encoding='utf-8', newline='\n') as f:
    f.write(css_new)

print('Before: {} chars / {} lines'.format(len(css), css.count(chr(10))))
print('After:  {} chars / {} lines'.format(len(css_new), css_new.count(chr(10))))
print('Removed: {} blank lines'.format(css.count(chr(10)) - css_new.count(chr(10))))
