import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

unused_vars = [
    '--duration-lg', '--fs-h1', '--fs-h3', '--fs-small', '--fs-stat-num',
    '--highlight', '--shadow-hover', '--shadow-soft', '--space-hairline', '--space-tight'
]

# Remove each CSS variable declaration line
# Pattern: optional whitespace + var: value; + optional comment + newline
for var in unused_vars:
    # Match: leading whitespace + --varname : ... ; + optional same-line comment + newline
    pattern = re.compile(r'^[ \t]*' + re.escape(var) + r'\s*:[^;]+;[^\n]*\n', re.MULTILINE)
    new_css = pattern.sub('', css)
    if new_css == css:
        # Try multi-line value
        pattern2 = re.compile(r'^[ \t]*' + re.escape(var) + r'\s*:.*?;\s*\n', re.MULTILINE | re.DOTALL)
        new_css = pattern2.sub('', css)
    if new_css != css:
        css = new_css
        print('Removed:', var)
    else:
        print('NOT FOUND:', var)

# Remove @keyframes scroll-cue-pulse
kf_pattern = re.compile(r'@(?:-webkit-)?keyframes\s+scroll-cue-pulse\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\s*', re.DOTALL)
new_css = kf_pattern.sub('', css)
if new_css != css:
    css = new_css
    print('Removed: @keyframes scroll-cue-pulse')

with open('assets/css/style.css', 'w', encoding='utf-8', newline='\n') as f:
    f.write(css)

print()
print('New size: {} chars / {} lines'.format(len(css), css.count(chr(10))))
