"""seed.json + template.html -> ../index.html

The template is trip-agnostic: everything specific to a trip is in seed.json ('trip' block, days, stops, votes, hotels).
Text that must be in the HTML before any script runs (tab title, link-preview tags, welcome sheet) is filled from
SEED.trip via {{placeholders}}; the rest is rendered in the browser."""
import re, os, sys, json, html as _html, subprocess
here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(here, '..', 'index.html')

def render():
    t = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
    seed = open(os.path.join(here, 'seed.json'), encoding='utf-8').read()
    assert t.count('__SEED__') == 1
    trip = json.loads(seed)['trip']
    fill = {'title': trip['title'], 'og_title': trip['og_title'], 'og_desc': trip['og_desc'], 'brand': trip['brand'], 'brand_sub': trip['brand_sub'],
            'welcome_title': trip['welcome']['title'], 'welcome_text': trip['welcome']['text'], 'welcome_img': trip['welcome']['img'], 'welcome_alt': trip['welcome']['alt']}
    head, script = t.split('<script>', 1)
    for k, v in fill.items(): head = head.replace('{{' + k + '}}', _html.escape(v, quote=True))
    left = re.findall(r'\{\{\w+\}\}', head)
    assert not left, f'unfilled placeholders: {left}'
    return head + '<script>' + script.replace('__SEED__', seed.replace('</script', r'<\/script'))

def js_ok(html):
    js = re.search(r'<script>(.*)</script>', html, re.S).group(1)
    node = r'C:\Program Files\nodejs\node.exe' if os.name == 'nt' else 'node'
    tmp = os.path.join(here, '_app.js'); open(tmp, 'w', encoding='utf-8').write(js)
    try:
        r = subprocess.run([node, '--check', tmp], capture_output=True, text=True)
        return (r.returncode == 0, r.stderr[:800])
    except FileNotFoundError:
        return (None, 'node not found')
    finally:
        os.remove(tmp)

if __name__ == '__main__':
    html = render()
    ok, err = js_ok(html)
    if ok is False: print(err); sys.exit(1)
    open(OUT, 'w', encoding='utf-8').write(html)
    print('syntax OK |' if ok else '(node not found, syntax not checked) |', 'wrote', os.path.abspath(OUT), os.path.getsize(OUT), 'bytes')
