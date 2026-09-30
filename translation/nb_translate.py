"""Extract, check and rebuild translated notebooks.

Usage (run from anywhere):
    python translation/nb_translate.py extract [files...]
    python translation/nb_translate.py check   [files...]
    python translation/nb_translate.py build   [files...]
    python translation/nb_translate.py status

`files` are repo-relative paths; without them every md/ipynb file is used.
See translation/WORKFLOW.md for the full procedure and file format.
"""
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, 'src')
TR = os.path.join(HERE, 'tr')
os.chdir(ROOT)

CELL_RE = re.compile(r'=====CELL (\d+)=====')


def all_files():
    out = subprocess.check_output(['git', 'ls-files', '*.md', '*.ipynb']).decode().split()
    return [f for f in out if not f.endswith(('_cn.md', '_cn.ipynb')) and not f.startswith('translation/')]


def txt_name(f):
    return f.replace('/', '__') + '.txt'


def cells_of(nb):
    # nbformat 3 keeps cells under worksheets
    return nb.get('cells') or [c for w in nb.get('worksheets', []) for c in w['cells']]


def text_of(c):
    s = c.get('source', c.get('input', ''))
    return s if isinstance(s, str) else ''.join(s)


def md_cells(nb):
    return [(i, c) for i, c in enumerate(cells_of(nb))
            if c['cell_type'] in ('markdown', 'heading') and text_of(c).strip()]


def parse(path):
    d, cur, buf = {}, None, []
    for line in open(path, encoding='utf8').read().split('\n'):
        m = CELL_RE.fullmatch(line)
        if m:
            if cur is not None:
                d[cur] = '\n'.join(buf).rstrip('\n')
            cur, buf = int(m.group(1)), []
        else:
            buf.append(line)
    if cur is not None:
        d[cur] = '\n'.join(buf).rstrip('\n')
    return d


def extract(f):
    os.makedirs(SRC, exist_ok=True)
    if f.endswith('.md'):
        parts = ['=====CELL 0=====\n' + open(f, encoding='utf8').read()]
    else:
        nb = json.load(open(f, encoding='utf8'))
        parts = ['=====CELL %d=====\n%s' % (i, text_of(c)) for i, c in md_cells(nb)]
    with open(os.path.join(SRC, txt_name(f)), 'w', encoding='utf8', newline='\n') as fh:
        fh.write('\n'.join(parts) + '\n')
    return len(parts)


def fix_links(t, f):
    """Point relative md/ipynb links at the _cn copy when the target exists."""
    def sub(m):
        p = m.group(2)
        if re.match(r'(https?:|mailto:|#)', p):
            return m.group(0)
        m2 = re.match(r'^(.*?)(\.(?:ipynb|md))([#?].*)?$', p)
        if m2 and not m2.group(1).endswith('_cn'):
            tgt = os.path.normpath(os.path.join(os.path.dirname(f), m2.group(1) + m2.group(2)))
            if os.path.exists(tgt):
                p = m2.group(1) + '_cn' + m2.group(2) + (m2.group(3) or '')
        return m.group(1) + p + m.group(3)
    t = re.sub(r'(\]\()([^)\s]+)(\))', sub, t)
    return re.sub(r'(href=")([^"]+)(")', sub, t)


def urls_of(t):
    """Exclude closing markup delimiters while retaining balanced URL parentheses."""
    urls = []
    for match in re.finditer(r"https?://[A-Za-z0-9._~:/?#@!$&*+;=%()\[\]'-]+", t):
        url = match.group(0)
        stack = []
        for i, char in enumerate(url):
            if char in '([':
                stack.append(char)
            elif char in ')]':
                if not stack or stack[-1] != {')': '(', ']': '['}[char]:
                    url = url[:i]
                    break
                stack.pop()
        urls.append(url.rstrip('.,;:'))
    return sorted(urls)


def formulas_of(t):
    """Allow prose-driven formula reordering and incidental line-edge whitespace."""
    formulas = re.findall(r'(?<!\\)\$\$[\s\S]*?\$\$|(?<!\\)\$(?:\\.|[^$])*?\$', t)
    return sorted('\n'.join(line.rstrip() for line in formula.splitlines())
                  for formula in formulas)


def invariants(t):
    """Things a translation must not change."""
    return {
        'dollar': t.count('$'),
        'fence': t.count('```'),
        'urls': urls_of(t),
        'latex_cmds': sorted(re.findall(r'\\[A-Za-z]+', t)),
        'formulas': formulas_of(t),
    }


def check(f):
    sp, tp = os.path.join(SRC, txt_name(f)), os.path.join(TR, txt_name(f))
    if not os.path.exists(tp):
        return None
    src, tr = parse(sp), parse(tp)
    errs = []
    for k in tr:
        if k not in src:
            errs.append('cell %d: not in source' % k)
            continue
        a, b = invariants(src[k]), invariants(tr[k])
        for key in a:
            if a[key] != b[key]:
                errs.append('cell %d: %s changed' % (k, key))
    missing = [k for k in src if k not in tr]
    return errs, missing


def build(f):
    tp = os.path.join(TR, txt_name(f))
    base, ext = os.path.splitext(f)
    dst = base + '_cn' + ext
    if not os.path.exists(tp):
        sp = os.path.join(SRC, txt_name(f))
        if os.path.exists(sp) and not parse(sp):
            shutil.copyfile(f, dst)
            return 'copied (no text)'
        return 'skipped (no translation)'
    tr = parse(tp)
    if ext == '.md':
        with open(dst, 'w', encoding='utf8', newline='\n') as fh:
            fh.write(fix_links(tr[0], f) + '\n')
        return 'built %d cells' % len(tr)
    nb = json.load(open(f, encoding='utf8'))
    cells = cells_of(nb)
    for i, t in tr.items():
        c = cells[i]
        t = fix_links(t, f)
        if text_of(c).endswith('\n') and not t.endswith('\n'):
            t += '\n'
        c['source' if 'source' in c else 'input'] = t.splitlines(keepends=True)
    with open(dst, 'w', encoding='utf8', newline='\n') as fh:
        json.dump(nb, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    return 'built %d cells' % len(tr)


def status(f):
    sp, tp = os.path.join(SRC, txt_name(f)), os.path.join(TR, txt_name(f))
    n = len(parse(sp)) if os.path.exists(sp) else 0
    d = len(parse(tp)) if os.path.exists(tp) else 0
    return '%d/%d' % (d, n)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ('extract', 'check', 'build', 'status'):
        print(__doc__)
        return 2
    cmd, files = sys.argv[1], (sys.argv[2:] or all_files())
    bad = 0
    for f in files:
        if cmd == 'extract':
            print(f, extract(f))
        elif cmd == 'build':
            print(f, build(f))
        elif cmd == 'status':
            print(f, status(f))
        else:
            r = check(f)
            if r is None:
                continue
            errs, missing = r
            bad += len(errs)
            print(f, 'errors=%d untranslated_cells=%d' % (len(errs), len(missing)))
            for e in errs:
                print('   ', e)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
