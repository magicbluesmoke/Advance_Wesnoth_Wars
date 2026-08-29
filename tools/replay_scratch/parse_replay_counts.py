import glob, os, re
from statistics import mean

WML_FILES = sorted(glob.glob('C:/src/Advance_Wesnoth_Wars/tools/replay_scratch/*.wml'))

def replay_block_lines(text):
    m = re.search(r'\[replay(?:_start)?\]', text)
    if not m:
        return []
    start = text[:m.start()].count('\n')
    return text.splitlines()[start:]

results = []
for path in WML_FILES:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    lines = replay_block_lines(text)
    attacks = sum(1 for line in lines if line.strip() == '[attack]')
    captures = sum(1 for line in lines if line.strip() == '[capture_village]')
    buffer = 0
    i = 0
    while i < len(lines):
        if lines[i].strip() == '[attack]':
            j = i + 1
            while j < len(lines) and lines[j].strip() != '[/attack]':
                j += 1
            chunk = '\n'.join(lines[i+1:j]).lower()
            if any(k in chunk for k in ['slow=yes','slowed','poison=yes','poisoned','petrify=yes','petrified']):
                buffer += 1
            i = j + 1
            continue
        i += 1
    results.append({
        'file': os.path.basename(path),
        'attacks': attacks,
        'captures': captures,
        'buffer': buffer,
    })

print('Parsed counts:')
for r in results:
    print(r)
attacks = [r['attacks'] for r in results]
captures = [r['captures'] for r in results]
buffers = [r['buffer'] for r in results]
print('attacks mean', round(mean(attacks),2), 'range', min(attacks), max(attacks))
print('captures mean', round(mean(captures),2), 'range', min(captures), max(captures))
print('buffer mean', round(mean(buffers),2), 'range', min(buffers), max(buffers))
