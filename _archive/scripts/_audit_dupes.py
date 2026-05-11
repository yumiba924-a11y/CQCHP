import re
from collections import defaultdict

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()


def parse_top_rules(text):
    rules = []
    i = 0
    n = len(text)
    while i < n:
        while i < n and text[i].isspace():
            i += 1
        if i >= n:
            break
        if text[i:i+2] == '/*':
            end = text.find('*/', i+2)
            if end < 0:
                break
            i = end + 2
            continue
        rule_start = i
        brace_pos = -1
        depth_paren = 0
        for j in range(i, n):
            ch = text[j]
            if ch == '(':
                depth_paren += 1
            elif ch == ')':
                depth_paren -= 1
            elif ch == '{' and depth_paren == 0:
                brace_pos = j
                break
            elif ch == ';' and depth_paren == 0:
                i = j + 1
                brace_pos = -2
                break
        if brace_pos < 0:
            if brace_pos == -2:
                continue
            break
        selector = text[i:brace_pos].strip()
        depth = 1
        j = brace_pos + 1
        while j < n and depth > 0:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
            j += 1
        body = text[brace_pos+1:j-1]
        rules.append({'selector': selector, 'body': body, 'start': rule_start, 'end': j})
        i = j
    return rules


rules = parse_top_rules(css)
print('Total top-level rules: {}'.format(len(rules)))

# Find selectors that appear in multiple rules
selector_count = defaultdict(list)
for idx, r in enumerate(rules):
    # Skip @media, @keyframes, @supports etc — they can have duplicates
    if r['selector'].startswith('@'):
        continue
    sel_normalized = re.sub(r'\s+', ' ', r['selector']).strip()
    selector_count[sel_normalized].append(idx)

# Report duplicates
print()
print('=== DUPLICATE SELECTORS (>1 rule with same selector) ===')
total_dupes = 0
for sel, idxs in selector_count.items():
    if len(idxs) > 1:
        total_dupes += len(idxs) - 1
        print('  ({} times) {}'.format(len(idxs), sel[:100]))

print()
print('Total duplicate rules (excess): {}'.format(total_dupes))
