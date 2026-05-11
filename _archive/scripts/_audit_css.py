import re
import os

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Collect all classes USED in HTML + JS
exclude_pseudos = {'is-active', 'is-open', 'is-enter', 'is-exit', 'is-revealed',
                   'is-paused', 'is-light', 'is-hover', 'is-visible'}

used_classes = set()
for root, dirs, files in os.walk('.'):
    if '.git' in root or '_archive' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js')):
            with open(os.path.join(root, f), 'r', encoding='utf-8') as fh:
                content = fh.read()
            for m in re.finditer(r'class(?:Name|List)?\s*[=\(\.\+]?\s*["' + "'" + r']?([\w\s\-_]+)["' + "'" + r']?', content):
                for cls in m.group(1).split():
                    used_classes.add(cls)
            for m in re.finditer(r"['" + '"' + r"]([a-z][\w\-]*)['" + '"' + r"]", content):
                cls = m.group(1)
                if re.match(r'^[a-z][\w\-]*$', cls):
                    used_classes.add(cls)

print('Detected used classes (rough): {}'.format(len(used_classes)))


def parse_css_rules(css_text):
    rules = []
    i = 0
    n = len(css_text)
    while i < n:
        while i < n and css_text[i].isspace():
            i += 1
        if i >= n:
            break
        if css_text[i:i+2] == '/*':
            end = css_text.find('*/', i+2)
            if end < 0:
                break
            i = end + 2
            continue
        rule_start = i
        brace_pos = -1
        semi_pos = -1
        depth_paren = 0
        for j in range(i, n):
            ch = css_text[j]
            if ch == '(':
                depth_paren += 1
            elif ch == ')':
                depth_paren -= 1
            elif ch == '{' and depth_paren == 0:
                brace_pos = j
                break
            elif ch == ';' and depth_paren == 0:
                semi_pos = j
                break
        if brace_pos < 0:
            if semi_pos >= 0:
                i = semi_pos + 1
                continue
            break
        selector = css_text[i:brace_pos].strip()
        depth = 1
        j = brace_pos + 1
        while j < n and depth > 0:
            if css_text[j] == '{':
                depth += 1
            elif css_text[j] == '}':
                depth -= 1
            j += 1
        body = css_text[brace_pos+1:j-1]
        kind = 'rule'
        if selector.startswith('@media'):
            kind = 'media'
        elif selector.startswith('@keyframes') or selector.startswith('@-webkit-keyframes'):
            kind = 'keyframes'
        elif selector.startswith('@'):
            kind = 'at-rule'
        rules.append({
            'kind': kind,
            'selector': selector,
            'body': body,
            'body_start': brace_pos + 1,
            'body_end': j - 1,
            'start': rule_start,
            'end': j,
        })
        i = j
    return rules


rules = parse_css_rules(css)
print('Top-level rules: {}'.format(len(rules)))


def is_rule_dead(selector):
    groups = [g.strip() for g in selector.split(',')]
    for grp in groups:
        classes_in_grp = re.findall(r'\.([a-zA-Z_][\w\-]*)', grp)
        if not classes_in_grp:
            return False
        any_used = any(c in used_classes for c in classes_in_grp if c not in exclude_pseudos)
        if any_used:
            return False
        all_pseudos = all(c in exclude_pseudos for c in classes_in_grp)
        if all_pseudos:
            return False
    return True


# Process top-level rules + inside @media
output_parts = []
last_end = 0
removed_count = 0
removed_chars = 0
removed_selectors = []

for r in rules:
    if r['kind'] == 'rule':
        if is_rule_dead(r['selector']):
            output_parts.append(css[last_end:r['start']])
            removed_count += 1
            removed_chars += r['end'] - r['start']
            removed_selectors.append(r['selector'][:80])
            last_end = r['end']
    elif r['kind'] == 'media':
        inner = parse_css_rules(r['body'])
        inner_dead = [inr for inr in inner if inr['kind'] == 'rule' and is_rule_dead(inr['selector'])]
        if inner_dead:
            output_parts.append(css[last_end:r['start']])
            new_body = r['body']
            for inr in reversed(inner_dead):
                new_body = new_body[:inr['start']] + new_body[inr['end']:]
                removed_count += 1
                removed_chars += inr['end'] - inr['start']
                removed_selectors.append('  (in @media) ' + inr['selector'][:70])
            if new_body.strip():
                output_parts.append(r['selector'] + ' {' + new_body + '}')
            last_end = r['end']

output_parts.append(css[last_end:])
new_css = ''.join(output_parts)

print()
print('Rules removed: {}'.format(removed_count))
print('Characters removed: {}'.format(removed_chars))
print('Original size: {} chars / {} lines'.format(len(css), css.count(chr(10))))
print('New size: {} chars / {} lines'.format(len(new_css), new_css.count(chr(10))))
print('Reduction: {}%'.format((len(css) - len(new_css)) * 100 // len(css)))

# Show first 30 removed selectors
print()
print('=== First 30 removed selectors ===')
for s in removed_selectors[:30]:
    print('  ' + s)

# Save
with open('assets/css/style.css', 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_css)
print()
print('Wrote cleaned CSS.')
