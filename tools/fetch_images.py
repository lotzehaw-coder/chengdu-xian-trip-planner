"""Find one Wikimedia Commons photo per place, save a 960px JPEG to ../img/<id>.jpg and record the credit in credits.json.
Re-run safe: skips ids already present unless --force. Override a bad pick with PIN = {id: 'File:Exact name.jpg'}."""
import requests, json, os, sys, io, re, time
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, '..', 'img'); os.makedirs(IMG, exist_ok=True)
API = 'https://commons.wikimedia.org/w/api.php'; S = requests.Session(); S.headers['User-Agent'] = 'chengdu-xian-trip-planner/1.0 (family trip planner; lotzehaw@users.noreply.github.com)'
Q = json.load(open(os.path.join(HERE, 'image_queries.json'), encoding='utf-8'))
CRED_P = os.path.join(HERE, 'credits.json'); CRED = json.load(open(CRED_P, encoding='utf-8')) if os.path.exists(CRED_P) else {}
force = '--force' in sys.argv; only = [a for a in sys.argv[1:] if not a.startswith('--')]
BAD = re.compile(r'map|logo|diagram|plan|flag|coat|seal|icon|svg|locator|chart|sign|ticket|menu|panorama', re.I)
def strip(h): return re.sub(r'<[^>]+>', '', h or '').strip()
def candidates(q):
    r = S.get(API, params={'action':'query','format':'json','generator':'search','gsrnamespace':6,'gsrsearch':q+' filetype:bitmap','gsrlimit':25,
        'prop':'imageinfo','iiprop':'url|size|extmetadata|mime','iiurlwidth':960}, timeout=40).json()
    pages = sorted((r.get('query') or {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    out = []
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]; t = p['title']
        if ii.get('mime') not in ('image/jpeg','image/png') or BAD.search(t): continue
        w, h = ii.get('width',0), ii.get('height',0)
        if w < 1000 or h < 600 or w/h < 1.15 or w/h > 2.1: continue
        out.append((t, ii))
    return out
def pinned(title):
    r = S.get(API, params={'action':'query','format':'json','titles':title,'prop':'imageinfo','iiprop':'url|size|extmetadata|mime','iiurlwidth':960}, timeout=40).json()
    p = list(r['query']['pages'].values())[0]; return [(p['title'], p['imageinfo'][0])]
for pid, spec in Q.items():
    if only and pid not in only: continue
    dst = os.path.join(IMG, pid + '.jpg')
    if os.path.exists(dst) and not force: continue
    try:
        cands = pinned(spec['pin']) if spec.get('pin') else []
        for q in ([] if cands else spec['q']):
            cands = candidates(q)
            if cands: break
        if not cands: print('NONE ', pid); continue
        t, ii = cands[spec.get('pick', 0) if len(cands) > spec.get('pick', 0) else 0]
        data = S.get(ii['thumburl'], timeout=60).content
        im = Image.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((960, 720)); im.save(dst, 'JPEG', quality=74, optimize=True, progressive=True)
        md = ii.get('extmetadata', {})
        CRED[pid] = {'file': t, 'page': ii.get('descriptionurl'), 'author': strip(md.get('Artist', {}).get('value'))[:80], 'license': strip(md.get('LicenseShortName', {}).get('value'))}
        print('ok   ', pid, '<-', t[:70], '|', CRED[pid]['license'], os.path.getsize(dst)//1024, 'KB')
        time.sleep(0.4)
    except Exception as e:
        print('ERR  ', pid, e)
json.dump(CRED, open(CRED_P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
