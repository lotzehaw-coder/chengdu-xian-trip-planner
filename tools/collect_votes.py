"""Keep a permanent copy of the family's votes in GitHub (votes.json).

People vote on the website; each tap is posted to TRIP.voteRelay (an ntfy.sh topic: free, no account, append-only).
ntfy keeps messages for about 12 hours, so this script runs every 30 minutes (Windows Task Scheduler,
"Trip planner - collect votes"), merges everything into ../votes.json (each person's latest vote wins),
and pushes it. The page reads votes.json + the relay's recent messages, so results survive the 12-hour window.

    python collect_votes.py          # merge, write, commit + push if anything changed
    python collect_votes.py --dry    # print only

votes.json holds only the name each person typed and their picks."""
import json, os, ssl, subprocess, sys, urllib.request, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
seed = json.load(open(os.path.join(HERE, 'seed.json'), encoding='utf-8'))
RELAY = seed['trip'].get('voteRelay')
DEC = {d['id']: {o['id'] for o in d['options']} for d in seed['decisions']}
ITEMS = {i['id'] for i in seed['items']}
OUT = os.path.join(ROOT, 'votes.json')
try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

def clean(o):
    name = str(o.get('n', '')).strip()[:40]
    if not name: return None, None
    picks = {d: v for d, v in (o.get('p') or o.get('picks') or {}).items() if d in DEC and v in DEC[d]}
    hearts = []
    for h in (o.get('h') or o.get('hearts') or []):
        h = str(h); h = h if h.startswith('p:') else 'p:' + h
        if h in ITEMS: hearts.append(h)
    if not picks and not hearts: return None, None      # blank/test submissions don't count
    return name, {'picks': picks, 'hearts': hearts, 't': int(o.get('t') or 0)}

def relay_messages():
    if not RELAY: return []
    req = urllib.request.Request(RELAY + '/json?poll=1&since=all', headers={'User-Agent': 'trip-planner-collector'})
    out = []
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        for line in r.read().decode('utf-8').splitlines():
            if not line.strip(): continue
            m = json.loads(line)
            if m.get('event') == 'message':
                try: out.append(json.loads(m['message']))
                except Exception: pass
    return out

def main():
    old = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    ballots = {}
    for n, b in (old.get('ballots') or {}).items():
        name, clean_b = clean(dict(b, n=n))
        if name: ballots[name] = clean_b
    msgs = relay_messages(); taken = 0
    for o in msgs:
        name, b = clean(o)
        if not name: continue
        if name not in ballots or b['t'] > ballots[name]['t']:
            ballots[name] = b; taken += 1
    print(f'{len(msgs)} relay messages, {taken} newer votes, {len(ballots)} people: {", ".join(sorted(ballots)) or "-"}')
    data = {'updated': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(timespec='minutes'),
            'count': len(ballots), 'ballots': dict(sorted(ballots.items()))}
    if '--dry' in sys.argv:
        print(json.dumps(data, ensure_ascii=False, indent=1)); return
    if old.get('ballots') == data['ballots']:
        print('no change'); return
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    git = lambda *a: subprocess.run(['git', '-C', ROOT, *a], capture_output=True, text=True)
    git('add', 'votes.json')
    n = len(ballots)
    r = git('commit', '-m', f'Votes: {n} {"person" if n == 1 else "people"} ({data["updated"]})')
    if r.returncode: print('commit failed:', r.stdout[-300:], r.stderr[-300:]); sys.exit(1)
    r = git('pull', '--rebase', '-q')
    r = git('push', '-q')
    if r.returncode: print('push failed:', r.stderr[-400:]); sys.exit(1)
    print('published votes.json')

if __name__ == '__main__':
    main()
