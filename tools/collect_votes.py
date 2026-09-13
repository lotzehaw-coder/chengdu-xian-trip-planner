"""Collect family votes from WhatsApp into votes.json, then publish it with the site.

People tap "Send my votes on WhatsApp" and post the message (with its #v=CX1.<code> link) into any chat Tze is in.
Tze's WhatsApp bridge logs every chat he's in to messages.db, so this script can read those links without anyone
tapping them. The page loads votes.json and shows live results to everyone.

    python collect_votes.py            # read, write ../votes.json, commit + push if anything changed
    python collect_votes.py --dry      # read and print, write nothing

Reads a COPY of the bridge database (never the live file). Only vote links for THIS site count.
votes.json holds only the name each person typed and their picks; no phone numbers or chat names."""
import base64, json, os, re, shutil, sqlite3, subprocess, sys, tempfile, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
DB = os.environ.get('WA_MESSAGES_DB', r'C:\Users\User\wa-probe\store\messages.db')
seed = json.load(open(os.path.join(HERE, 'seed.json'), encoding='utf-8'))
SITE = seed['trip']['site'].rstrip('/')
PATH = re.sub(r'^https?://', '', SITE)                     # lotzehaw-coder.github.io/chengdu-xian-trip-planner
DEC = {d['id']: {o['id'] for o in d['options']} for d in seed['decisions']}
ITEMS = {i['id'] for i in seed['items']}
OUT = os.path.join(ROOT, 'votes.json')

def decode(code):
    b = code.replace('-', '+').replace('_', '/'); b += '=' * (-len(b) % 4)
    return json.loads(base64.b64decode(b).decode('utf-8'))

def read_codes():
    tmp = os.path.join(tempfile.gettempdir(), 'votes_messages_copy.db')
    shutil.copy2(DB, tmp)
    c = sqlite3.connect(tmp)
    rows = c.execute("select timestamp, content from messages where content like '%#v=CX1.%' order by timestamp").fetchall()
    c.close()
    out = []
    for ts, content in rows:
        for m in re.finditer(r'(\S*?)#v=CX1\.([A-Za-z0-9_-]+)', content or ''):
            if PATH not in m.group(1): continue                # a vote link for another trip's page
            out.append((ts, m.group(2)))
    return out

def tally():
    ballots = {}; seen = 0; bad = 0
    for ts, code in read_codes():
        seen += 1
        try:
            o = decode(code)
            name = str(o.get('n', '')).strip()[:40]
            if not name: raise ValueError('no name')
            picks = {d: v for d, v in (o.get('p') or {}).items() if d in DEC and v in DEC[d]}
            hearts = [('p:' + str(h)) for h in (o.get('h') or []) if ('p:' + str(h)) in ITEMS]
            t = int(o.get('t') or 0)
        except Exception:
            bad += 1; continue
        cur = ballots.get(name)
        if not cur or t >= cur['t']:                            # a person's latest message wins
            ballots[name] = {'picks': picks, 'hearts': hearts, 't': t}
    return ballots, seen, bad

def main():
    ballots, seen, bad = tally()
    data = {'updated': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='minutes'),
            'count': len(ballots), 'ballots': dict(sorted(ballots.items()))}
    print(f'{seen} vote links found, {bad} unreadable, {len(ballots)} people: {", ".join(ballots) or "-"}')
    if '--dry' in sys.argv:
        print(json.dumps(data, ensure_ascii=False, indent=1)); return
    old = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    if old.get('ballots') == data['ballots']:
        print('no change'); return
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    git = lambda *a: subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True)
    git('add', 'votes.json')
    r = git('commit', '-m', f'Votes: {len(ballots)} people ({data["updated"]})')
    if r.returncode: print('commit failed:', r.stdout[-300:], r.stderr[-300:]); sys.exit(1)
    r = git('push', '-q')
    if r.returncode: print('push failed:', r.stderr[-400:]); sys.exit(1)
    print('published votes.json')

if __name__ == '__main__':
    main()
