import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Find all CSS variable definitions (in :root or anywhere)
var_def_pattern = re.compile(r'--([\w\-]+)\s*:')
defined_vars = set()
for m in var_def_pattern.finditer(css):
    defined_vars.add(m.group(1))

# Find all CSS variable usages
var_use_pattern = re.compile(r'var\(\s*--([\w\-]+)')
used_vars = set()
for m in var_use_pattern.finditer(css):
    used_vars.add(m.group(1))

unused_vars = defined_vars - used_vars
print('Defined CSS variables: {}'.format(len(defined_vars)))
print('Used CSS variables: {}'.format(len(used_vars)))
print('Unused CSS variables: {}'.format(len(unused_vars)))
print()
print('=== UNUSED CSS VARIABLES ===')
for v in sorted(unused_vars):
    print('  --' + v)

# Find all @keyframes definitions
kf_def_pattern = re.compile(r'@(?:-webkit-)?keyframes\s+([\w\-]+)')
defined_kfs = set()
for m in kf_def_pattern.finditer(css):
    defined_kfs.add(m.group(1))

# Find all animation usages (animation: name ... or animation-name: name)
kf_use_pattern = re.compile(r'animation(?:-name)?\s*:\s*([\w\-]+)')
used_kfs = set()
for m in kf_use_pattern.finditer(css):
    name = m.group(1)
    if name not in ('none', 'inherit', 'initial', 'unset', 'normal', 'reverse', 'alternate',
                    'infinite', 'paused', 'running', 'forwards', 'backwards', 'both'):
        used_kfs.add(name)
# Also detect animation: SHORTHAND containing keyframe name
for m in re.finditer(r'animation\s*:\s*([^;]+);', css):
    parts = m.group(1).split()
    for p in parts:
        if p in defined_kfs:
            used_kfs.add(p)

unused_kfs = defined_kfs - used_kfs
print()
print('Defined keyframes: {}'.format(len(defined_kfs)))
print('Used keyframes: {}'.format(len(used_kfs)))
print('Unused keyframes: {}'.format(len(unused_kfs)))
print()
print('=== UNUSED KEYFRAMES ===')
for k in sorted(unused_kfs):
    print('  @keyframes ' + k)
