"""Automated checks for the trip planner. The reviewer agent runs this first, then does the judgement calls (photo relevance, plan sense).

    python check_site.py            # local checks: build freshness, JS syntax, images, credits, map data, plan sanity
    python check_site.py --links    # + every external link (hotel pages, photo credit pages)
    python check_site.py --live     # + the published GitHub Pages site and every image on it

Exit code 1 if anything is an ERROR. WARN lines are for a human to judge."""
import json, os, sys, re, subprocess, hashlib, urllib.parse, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
LIVE = 'https://lotzehaw-coder.github.io/chengdu-xian-trip-planner/'
errors, warns, oks = [], [], []
def E(m): errors.append(m)
def W(m): warns.append(m)
def OK(m): oks.append(m)

seed = json.load(open(os.path.join(HERE, 'seed.json'), encoding='utf-8'))
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

# 1. build is up to date with seed.json + template.html
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
raw = open(os.path.join(HERE, 'seed.json'), encoding='utf-8').read()
expect = tpl.replace('__SEED__', raw.replace('</script', r'<\/script'))
(OK if expect == html else E)('index.html matches template.html + seed.json' if expect == html else 'index.html is stale: run python seed.py && python build.py')

# 2. JS syntax
js = re.search(r'<script>(.*)</script>', html, re.S).group(1); tmp = os.path.join(HERE, '_check.js'); open(tmp, 'w', encoding='utf-8').write(js)
node = r'C:\Program Files\nodejs\node.exe' if os.name == 'nt' else 'node'
try:
    r = subprocess.run([node, '--check', tmp], capture_output=True, text=True)
    (OK('JS syntax OK') if r.returncode == 0 else E('JS syntax error: ' + r.stderr[:300]))
except FileNotFoundError:
    W('node not found; JS syntax not checked')
finally:
    os.remove(tmp)

# 3. images referenced exist, are credited, galleries have no duplicates
refs = {}
def ref(src, where):
    if src: refs.setdefault(src, []).append(where)
for i in seed['items']:
    ref(i['img'], i['id'])
    for g in i.get('gallery', []): ref(g, i['id'])
    if len(i.get('gallery', [])) != len(set(i.get('gallery', []))): E(f"duplicate photo inside gallery of {i['id']}")
for d in seed['decisions']:
    for o in d['options']:
        ref(o['img'], f"{d['id']}:{o['id']}")
        for g in o.get('gallery', []): ref(g, f"{d['id']}:{o['id']}")
for city, st in seed['hotels'].items():
    for h in st['options']:
        caps = [g.get('cap') for g in h['gallery']]
        if not all(caps): E(f'hotel {h["id"]} has a photo without a caption')
        if len({g['src'] for g in h['gallery']}) != len(h['gallery']): E(f'duplicate photo in hotel {h["id"]} carousel')
        if len(h['gallery']) < 3: W(f'hotel {h["id"]} carousel has only {len(h["gallery"])} photos')
        for g in h['gallery']: ref(g['src'], 'hotel:' + h['id'])
missing = [s for s in refs if not os.path.exists(os.path.join(ROOT, s))]
for s in missing: E(f'missing image {s} (used by {refs[s][0]})')
on_disk = {os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/') for dp, _, fs in os.walk(os.path.join(ROOT, 'img')) for f in fs if f.endswith('.jpg')}
unused = sorted(on_disk - set(refs) - {'img/chengduhero.jpg', 'img/xianhero.jpg', 'img/panda.jpg'})
if unused: W(f'{len(unused)} image files on disk not used: {unused[:8]}')
cred = seed['credits']
uncredited = [s for s in refs if s[4:-4] not in cred]
for s in uncredited: E(f'no photo credit for {s}')
for k, c in cred.items():
    if not c.get('license') or not c.get('page'): E(f'credit for {k} lacks a license or source page')
    if c.get('license') and not re.search(r'CC0|CC BY|Public domain|PD', c['license'], re.I): W(f'credit for {k} has an unusual license: {c["license"]}')
# the same Commons file used as two different ids looks like repetition
by_file = {}
for k, c in cred.items(): by_file.setdefault(c['file'], []).append(k)
for f, ks in by_file.items():
    if len(ks) > 1: W(f'same photo saved twice as {ks}')
OK(f'{len(refs)} images referenced, {len(missing)} missing, {len(uncredited)} uncredited')

# 4. map data: every real place has a search term; URLs build cleanly
for i in seed['items']:
    rest = i['category'] == 'Rest' or not re.search(r'[㐀-鿿]', i['name'] + i.get('mapq', ''))
    if not i.get('mapq') and not rest: W(f"no map search for {i['id']} ({i['name']})")
    if i.get('mapq') and not i.get('mapen'): W(f"no English Google search for {i['id']}")
    if i.get('mapq') and not re.search(r'[㐀-鿿]', i['mapq']): W(f"map search for {i['id']} is not Chinese: {i['mapq']}")
    if i.get('lat') and not (28 < i['lat'] < 36 and 102 < i['lng'] < 111): E(f"coordinates for {i['id']} are outside Sichuan/Shaanxi: {i['lat']},{i['lng']}")
for b in seed['blocks']:
    if b['type'] in ('train', 'flight') and b['type'] == 'train' and not b.get('mapq'): W(f"train block {b['id']} has no station search")
    q = b.get('mapq')
    if q: urllib.parse.quote(q)
for city, st in seed['hotels'].items():
    for h in st['options']:
        if not re.search(r'[㐀-鿿]', h['cn']): E(f'hotel {h["id"]} has no Chinese name for the map search')
OK('map search terms checked')

# 5. plan sanity
days = [d['d'] for d in seed['days']]
dec = {d['id']: d for d in seed['decisions']}
def mins(t): h, m = map(int, t.split(':')); return h*60 + m
for d in days:
    its = [i for i in seed['items'] if i['day'] == d and i['status'] == 'scheduled' and not i['opt'] and i['time'] and i['end']]
    its.sort(key=lambda i: i['time'])
    for a, b in zip(its, its[1:]):
        if mins(b['time']) < mins(a['end']): E(f"{d}: {a['name']} ({a['time']}-{a['end']}) overlaps {b['name']} ({b['time']})")
    wd = time.strptime(d, '%Y-%m-%d').tm_wday
    for i in [i for i in seed['items'] if i['day'] == d and i['status'] == 'scheduled' or (i['opt'] and i['day'] == d)]:
        if wd == 0 and re.search(r'museum|terracotta', i['name'], re.I): W(f"{d} is a Monday and '{i['name']}' may be closed on Mondays")
    for x in [x for x in seed['decisions'] if x['day'] == d]:
        for o in x['options']:
            opts = [i for i in seed['items'] if i['id'] in o['items']]
            if not opts: E(f"vote {x['id']} option {o['id']} has no stops")
for i in seed['items']:
    if i['opt']:
        did, oid = i['opt'].split(':')
        if did not in dec or i['id'] not in next((o['items'] for o in dec[did]['options'] if o['id'] == oid), []): E(f"{i['id']} points at vote {i['opt']} that doesn't list it")
    if i['day'] and i['day'] not in days: E(f"{i['id']} is on {i['day']}, outside the trip")
OK('plan sanity checked')

# 6. external links
def fetch(url, method='HEAD'):
    import urllib.request
    req = urllib.request.Request(url, method=method, headers={'User-Agent': 'Mozilla/5.0 (trip-planner link check)'})
    try:
        with urllib.request.urlopen(req, timeout=25) as r: return r.status
    except Exception as e:
        return getattr(e, 'code', None) or str(e)[:60]
if '--links' in sys.argv:
    urls = [(h['url'], 'hotel ' + h['id']) for st in seed['hotels'].values() for h in st['options']] + [(c['page'], 'credit ' + k) for k, c in cred.items()]
    for u, what in urls:
        st = fetch(u) if 'marriott.com' not in u and 'ritzcarlton.com' not in u else fetch(u, 'GET')
        if st == 200: continue
        if st in (403, 405, 429) and ('marriott.com' in u or 'ritzcarlton.com' in u): W(f'{what}: {u} answered {st} to a script (Marriott blocks bots); open it in a browser to confirm')
        elif st in (403, 405, 429): W(f'{what}: {u} answered {st}')
        else: E(f'{what}: {u} -> {st}')
        time.sleep(0.2)
    OK(f'{len(urls)} external links checked')

# 7. live site
if '--live' in sys.argv:
    import urllib.request
    try:
        live = urllib.request.urlopen(urllib.request.Request(LIVE + '?check=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8')
        (OK('live site matches local index.html') if hashlib.sha1(live.encode()).hexdigest() == hashlib.sha1(html.encode()).hexdigest()
         else W('live site differs from local index.html (not pushed yet, or Pages still building)'))
    except Exception as e:
        E(f'live site unreachable: {e}')
    bad = [s for s in refs if fetch(LIVE + s) != 200]
    for s in bad: E(f'live image not served: {LIVE + s}')
    OK(f'{len(refs)} live images checked, {len(bad)} failed')

for m in oks: print('OK    ', m)
for m in warns: print('WARN  ', m)
for m in errors: print('ERROR ', m)
print(f'\n{len(errors)} errors, {len(warns)} warnings')
sys.exit(1 if errors else 0)
