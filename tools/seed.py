"""The whole plan lives here. python seed.py -> seed.json; python build.py -> ../index.html"""
import json, math, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- coordinates: WGS-84 (Wikipedia where it has them) -> GCJ-02 for Amap / Apple Maps China ----------
_a, _ee = 6378245.0, 0.00669342162296594323
def _tlat(x, y):
    r = -100 + 2*x + 3*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
    r += (20*math.sin(6*x*math.pi) + 20*math.sin(2*x*math.pi)) * 2/3
    r += (20*math.sin(y*math.pi) + 40*math.sin(y/3*math.pi)) * 2/3
    r += (160*math.sin(y/12*math.pi) + 320*math.sin(y*math.pi/30)) * 2/3
    return r
def _tlon(x, y):
    r = 300 + x + 2*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
    r += (20*math.sin(6*x*math.pi) + 20*math.sin(2*x*math.pi)) * 2/3
    r += (20*math.sin(x*math.pi) + 40*math.sin(x/3*math.pi)) * 2/3
    r += (150*math.sin(x/12*math.pi) + 300*math.sin(x/30*math.pi)) * 2/3
    return r
def gcj(lat, lon):
    dlat, dlon = _tlat(lon-105, lat-35), _tlon(lon-105, lat-35)
    rl = lat/180*math.pi; m = math.sin(rl); m = 1 - _ee*m*m; sm = math.sqrt(m)
    dlat = (dlat*180) / ((_a*(1-_ee)) / (m*sm) * math.pi); dlon = (dlon*180) / (_a/sm*math.cos(rl)*math.pi)
    return round(lat+dlat, 6), round(lon+dlon, 6)
W = {k: v for k, v in json.load(open(os.path.join(HERE, 'wiki_coords.json'))).items() if v}
W.update({'kuanzhai': (30.6692, 104.0560), 'jinli': (30.6461, 104.0490), 'taikooli': (30.6555, 104.0826), 'wenshu': (30.6746, 104.0726),
          'datang': (34.2130, 108.9600), 'muslimquarter': (34.2640, 108.9395), 'xianmuseum': W.get('smallgoose')})
def at(k):
    v = W.get(k); return gcj(*v) if v else (None, None)

IMG = set(f[:-4] for f in os.listdir(os.path.join(HERE, '..', 'img')) if f.endswith('.jpg'))
def img(k): return f'img/{k}.jpg' if k in IMG else ''
import glob, re
REST = ['img/g/rest-1.jpg']
def gal(k):
    """main photo first, then the carousel extras img/g/<k>-<n>.jpg in number order. A list is taken as-is."""
    if isinstance(k, list): return k
    extra = sorted(glob.glob(os.path.join(HERE, '..', 'img', 'g', f'{k}-*.jpg')), key=lambda f: int(re.search(r'-(\d+)\.jpg$', f).group(1)))
    return [x for x in [img(k)] if x] + ['img/g/' + os.path.basename(f) for f in extra]
# what to search for in Amap / Apple / Google so the place card (photos, reviews) opens. No entry + no Chinese in the name = no Map button.
MAPQ = {'lunch-mapo': '陈麻婆豆腐', 'peoplespark': '鹤鸣茶社', 'kuanzhai': '宽窄巷子', 'panda': '成都大熊猫繁育研究基地',
  'lunch-longchaoshou': '龙抄手 春熙路', 'wildgoose': '大雁塔', 'dinner-dapaidang': '长安大牌档', 'datang': '大唐不夜城',
  'terracotta': '秦始皇帝陵博物院', 'dinner-defachang': '德发长', 'shaanximuseum': '陕西历史博物馆', 'lunch-noodles': '樊记腊汁肉夹馍', 'citywall': '永宁门',
  'belltower': '西安钟楼', 'night-d6': '春熙路', 'lunch-zhong': '钟水饺', 'opera': '蜀风雅韵', 'jinli-eve': '锦里古街', 'taikooli': '成都远洋太古里',
  'wuhou': '成都武侯祠', 'huaqing': '华清宫', 'muslimquarter': '回民街', 'tangshow': '唐乐宫', 'yongxingfang': '永兴坊', 'hanfu': '大雁塔',
  'smallgoose': '小雁塔', 'leshan-train': '成都东站', 'leshan': '乐山大佛', 'dujiangyan': '都江堰景区', 'dufu': '杜甫草堂', 'sichuanmuseum': '四川博物院',
  'naturalhistory': '成都自然博物馆', 'wenshu': '文殊院', 'shopping': '成都国际金融中心', 'tianfu-idea': '天府广场', 'jinsha': '金沙遗址博物馆',
  'qingcheng': '青城山', 'tangparadise': '大唐芙蓉园', 'paomo': '老孙家泡馍', 'drumtower-in': '西安鼓楼', 'leshan-back': '乐山站', 'pandatower': '天府熊猫塔', 'dongjiao': '东郊记忆', 'qianguqing': '西安千古情景区', 'gongyan': '大明宫宴 笃臣路', 'changan12': '长安十二时辰主题街区', 'emei': '只有峨眉山戏剧幻城', 'everlasting': '华清宫', 'tuoling': '驼铃传奇', 'daqin': '赳赳大秦', 'juntuan': '复活的军团', 'xianincident': '华清宫 瑶光阁剧院', 'mengchangan': '西安城墙永宁门', 'tangdream': '大唐芙蓉园', 'menghui': '凤鸣九天剧院'}
# English search for Google Maps (pre-trip reviews in English)
MAPEN = {'lunch-mapo': 'Chen Mapo Tofu', 'peoplespark': "People's Park Chengdu", 'kuanzhai': 'Kuanzhai Alley', 
  'panda': 'Chengdu Research Base of Giant Panda Breeding', 'lunch-longchaoshou': 'Long Chao Shou Chunxi Road', 
  'wildgoose': 'Big Wild Goose Pagoda', 'dinner-dapaidang': "Chang'an Da Pai Dang", 'datang': 'Great Tang All Day Mall', 'terracotta': 'Terracotta Army Museum',
  'dinner-defachang': 'De Fa Chang dumpling restaurant', 'shaanximuseum': 'Shaanxi History Museum', 'lunch-noodles': 'Fanji Roujiamo', 'citywall': "Yongningmen South Gate Xi'an City Wall",
  'belltower': "Bell Tower Xi'an", 'night-d6': 'Chunxi Road', 'lunch-zhong': 'Zhong Shui Jiao', 'opera': 'Shufeng Yayun Sichuan Opera', 'jinli-eve': 'Jinli Ancient Street',
  'taikooli': 'Sino-Ocean Taikoo Li Chengdu', 'wuhou': 'Wuhou Shrine', 'huaqing': 'Huaqing Palace', 'muslimquarter': "Muslim Quarter Xi'an", 'tangshow': 'Tang Dynasty Show Theater',
  'yongxingfang': 'Yongxingfang', 'hanfu': 'Big Wild Goose Pagoda', 'smallgoose': 'Small Wild Goose Pagoda', 'leshan-train': 'Chengdu East Railway Station',
  'leshan': 'Leshan Giant Buddha', 'dujiangyan': 'Dujiangyan Irrigation System', 'dufu': 'Du Fu Thatched Cottage', 'sichuanmuseum': 'Sichuan Museum',
  'naturalhistory': 'Chengdu Natural History Museum', 'wenshu': 'Wenshu Monastery', 'shopping': 'Chengdu IFS', 'tianfu-idea': 'Tianfu Square', 'jinsha': 'Jinsha Site Museum',
  'qingcheng': 'Mount Qingcheng', 'tangparadise': 'Tang Paradise', 'paomo': 'Lao Sun Jia Paomo', 'drumtower-in': "Drum Tower Xi'an", 'leshan-back': 'Leshan Railway Station', 'pandatower': 'Tianfu Panda Tower Chengdu', 'dongjiao': 'Eastern Suburb Memory Chengdu', 'qianguqing': "Xi'an Romance Park", 'gongyan': 'Da Ming Gong Yan Tang banquet Xian', 'changan12': "Chang'an Twelve Hours Xi'an", 'emei': 'Only Emei Mountain Drama Fantasy City', 'everlasting': 'Huaqing Palace', 'tuoling': 'Huaxia Wenlv Grand Theatre Xian', 'daqin': "Jiujiu Daqin Theatre Xi'an", 'juntuan': 'Daqin Theatre Lintong Xian', 'xianincident': 'Huaqing Palace Xian', 'mengchangan': "Yongningmen South Gate Xi'an City Wall", 'tangdream': 'Tang Paradise', 'menghui': 'Tang Paradise'}

LANDS = {"chengdu": "<path d=\"M2 58h156M4 58c6-12 16-12 22 0M26 58c6-12 16-12 22 0M48 58c6-12 16-12 22 0M2 46h70M8 46l4-6h52l4 6M36 40v-4M30 36h12l-6-5z\"/><path d=\"M128 58V8M140 58V14M128 20h2M128 34h2M140 28h2M140 44h2M128 20c8-6 14-6 20-4M140 28c-8-8-16-8-24-4M128 34c-6 2-12 8-14 12\"/><circle cx=\"98\" cy=\"42\" r=\"12\"/><circle cx=\"88\" cy=\"31\" r=\"4\"/><circle cx=\"108\" cy=\"31\" r=\"4\"/><path d=\"M92 41c1-3 4-3 5 0M99 41c1-3 4-3 5 0M96 48c1 1 3 1 4 0\"/>", "xian": "<path d=\"M2 58h156M2 58V40h8v-6h8v6h8v-6h8v6h8v-6h8v6h8v-6h8v6h4v18M24 58v-8c0-7 14-7 14 0v8M104 58V22h22v36M100 50h30M101 42h28M102 34h26M103 27h24M107 22v-6h16v6M111 16l4-7 4 7M115 9V4M112 58v-6h6v6M140 58V46M136 46h8l-4-5z\"/>"}   # landmark line drawings for the day headers / hero (SVG path markup, 160x64)
# ---------- the trip itself: everything the page shows that is specific to THIS trip ----------
TRIP = {
    'name': "Chengdu · Xi'an family trip", 'dates': '13–22 Dec 2026',
    'app': 'chengdu-xian-trip-planner', 'key': 'cdxa',                 # key: localStorage prefix + map source id. NEVER change once shared (it holds everyone's votes)
    'site': 'https://lotzehaw-coder.github.io/chengdu-xian-trip-planner/',
    'nightsFoot': ['✈ land ~00:15 Mon 14 (13th night booked)', 'Mon 21: rooms to the evening · ✈ 01:05'],   # the two ends of the Hotels-tab nights bar
    'title': "Chengdu · Xi'an Family Trip", 'brand': "Chengdu · Xi'an", 'brand_sub': '13–22 Dec 2026 · family of 10',
    'subtitle': '13–22 Dec 2026 · family of 10 · pandas, warriors & dumplings',
    'og_title': "Chengdu · Xi'an family trip — 13–22 Dec 2026", 'og_desc': 'Vote on where we go. Pandas, the Terracotta Army, hot pot and dumplings.',
    'welcome': {'title': "Chengdu & Xi'an, 13–22 Dec", 'text': 'Help plan the family trip: pandas, the Terracotta Army, hot pot and dumplings.', 'img': 'img/panda.jpg', 'alt': 'A giant panda'},
    'start': '2026-12-13T19:00:00+08:00', 'utcOffset': 8, 'amap': True,   # amap: China trips get 高德 Amap in the map menu
    'cities': [
        {'name': 'Chengdu', 'local': '成都', 'color': '#2f7a55', 'tint': 'rgba(18,52,38,.94)', 'hero': 'img/chengduhero.jpg', 'hotelDec': 'h-chengdu', 'land': LANDS['chengdu']},
        {'name': "Xi'an", 'local': '西安', 'color': '#a3432a', 'tint': 'rgba(92,32,18,.94)', 'hero': 'img/xianhero.jpg', 'hotelDec': 'h-xian', 'land': LANDS['xian']},
    ],
    'mapCities': {'Leshan': '乐山', 'Dujiangyan': '都江堰'},   # day-trip towns, so map searches land in the right city
    'bbox': [28, 102, 36, 111],   # sanity box for coordinates (Sichuan + Shaanxi)
    'voteRelay': 'https://ntfy.sh/cdxa-votes-667bb654d090f8a0',   # votes are posted here from the page; tools/collect_votes.py copies them into votes.json every 30 min
    'country': 'China', 'hotelLinkLabel': 'Marriott',
    'hotelsIntro': 'All Marriott Bonvoy. Ranked for this family: how likely a Titanium/Platinum member is to get a suite (from Flyert 飞客, SMZDM, Trip.com, TripAdvisor and FlyerTalk reports), how new the hotel is, and the location. Vote for a hotel for each stay (Chengdu has two stays, so you can try two hotels).',
    'hotelsTip': "Rooms for 10: plan on 4–5 rooms, with connecting rooms for each family and a room near the lift for the grandparents. Hotels in China often limit rooms to 2 adults + 1 child, so confirm the cot, extra bed and kids' breakfast rules when you book.",
    'about': 'Flights MH526 / MH527 are booked; exact times are on the e-ticket. Trains, vans and hotels are not booked yet and are marked tentative. Map opens the place in 高德地图 Amap, Google Maps or Apple Maps. Votes are saved online under the name you type (no accounts); your notes and plan changes stay on this phone.',
}

# ---------- days ----------
DAYS = [
 ('2026-12-13', 'Travel',  'KL → Chengdu, landing after midnight'),
 ('2026-12-14', 'Chengdu', 'Slow start · teahouse & old alleys'),
 ('2026-12-15', 'Chengdu', 'Pandas in the morning'),
 ('2026-12-16', "Xi'an",   'Train north · pagoda by night'),
 ('2026-12-17', "Xi'an",   'Terracotta Army'),
 ('2026-12-18', "Xi'an",   'Museum, city wall & Muslim Quarter'),
 ('2026-12-19', 'Chengdu', 'Train back to Chengdu'),
 ('2026-12-20', 'Chengdu', "Family's pick: day trip or city"),
 ('2026-12-21', 'Chengdu', 'Last day · fly home after midnight'),
]
days = [{'d': d, 'city': c, 'label': l} for d, c, l in DAYS]
D = [d for d, _, _ in DAYS]

# fam tags: stroller = pram-friendly, easy = little walking, stairs = many steps, cold = outdoors in winter,
#           indoor, book = book ahead, spicy = watch the chilli, rest = downtime
items = []; order = {}
MAPCITY = {'leshan': 'Leshan', 'leshan-back': 'Leshan', 'dujiangyan': 'Dujiangyan', 'qingcheng': 'Dujiangyan', 'emei': 'Emeishan'}
def I(id, day, name, city, cat, time='', end='', info='', fam=(), tags=(), key=None, pic=None, opt='', book=''):
    n = order.get(day, 0) + 1; order[day] = n
    lat, lng = at(key or id)
    items.append({'id': 'p:' + id, 'name': name, 'city': city, 'category': cat, 'time': time, 'end': end, 'info': info,
                  'fam': list(fam), 'tags': list(tags), 'img': (gal(pic or id) or [''])[0], 'gallery': gal(pic or id), 'mapq': MAPQ.get(id, ''), 'mapen': MAPEN.get(id, ''), 'mapcity': MAPCITY.get(id, city), 'lat': lat, 'lng': lng, 'address': '', 'book': book,
                  'day': day, 'suggestedDay': day, 'status': 'scheduled' if day and not opt else 'wishlist', 'opt': opt, 'order': n})

# Day 1 — Mon 14 Dec
I('peoplespark', D[1], "People's Park & Heming Teahouse 人民公园 · 鹤鸣茶社", 'Chengdu', 'Sight', '14:00', '15:30',
  'Chengdu at its most relaxed: bamboo chairs by the lake, a pot of jasmine tea, ear-cleaners doing the rounds, grandparents dancing. Flat paths all the way round.', ('stroller', 'easy'), ('must-see',))
I('kuanzhai', D[1], 'Kuanzhai Alley 宽窄巷子', 'Chengdu', 'Sight', '16:00', '17:30',
  'Three restored Qing-era lanes of courtyard houses, snacks and tea shops. Flat and pram-friendly; busy after 5pm, so hold small hands.', ('stroller', 'easy'))
# Day 2 — Tue 15 Dec
I('panda', D[2], 'Giant Panda Base 成都大熊猫繁育研究基地', 'Chengdu', 'Sight', '08:00', '11:30',
  'Go at opening: pandas are most active in the cool morning. Use the ¥10 park shuttle bus between enclosures to save little and older legs. The nurseries with cubs are the highlight.',
  ('stroller', 'cold', 'book'), ('must-see',), book="Tickets open 14 days ahead (from Tue 1 Dec) on Trip.com or the base's WeChat mini-program; passport for each person. Book the shuttle bus at the same time.")
I('rest-d2', D[2], 'Back to the hotel — nap & rest', 'Chengdu', 'Rest', '13:30', '15:45',
  'Early start and a long walk: nap time for the baby and a rest for the elderly before the evening.', ('rest',), pic=REST)
# Day 3 — Wed 16 Dec
I('lunch-train', D[3], 'Lunch on the train', 'Travel', 'Food', '12:15', '13:00',
  'Buy buns and snacks at Chengdu East before boarding, or order a hot meal to your seat when booking on Trip.com / 铁路12306. Hot water taps in every carriage for baby bottles.', ('easy',), pic='hsr')
I('wildgoose', D[3], 'Big Wild Goose Pagoda 大雁塔', "Xi'an", 'Sight', '17:15', '18:15',
  'The 7th-century Tang pagoda, beautifully lit at dusk (sunset about 17:39). The squares around it are free and flat; the temple grounds close 17:30 in winter, so this is the squares and the lights.', ('stroller', 'easy', 'cold'), ('must-see',))
I('datang', D[3], 'Great Tang All Day Mall night walk 大唐不夜城', "Xi'an", 'Night', '19:45', '21:00',
  'A long pedestrian boulevard of Tang-dynasty light sculptures and street performers running south from the pagoda. Flat and wide, fine for strollers and wheelchairs. Very cold after dark in December. The fountain on the pagoda North Square runs about 20:30–21:00 on weekdays (confirm on the 曲江新区 account), so finish the walk there. If you stay at the Ritz, one van takes the grandparents and the baby back after dinner. The street is car-free: meet the vans at 曲江大悦城 south side. Rain or snow: stay in 曲江大悦城 mall.', ('stroller', 'easy', 'cold'), ('must-see',))
# Day 4 — Thu 17 Dec
I('terracotta', D[4], 'Terracotta Army 秦始皇兵马俑', "Xi'an", 'Sight', '09:30', '12:30',
  "Start at Pit 1 (the famous rows of 2,000-year-old warriors), then Pits 3 and 2. It's a long walk from the car park to the pits, so pace it for the elderly and bring the baby carrier as well as the stroller. The halls are big and cold in winter.",
  ('stroller', 'cold', 'book'), ('must-see',), book='Online only on the official WeChat, time-slotted, 7 days ahead (from Thu 10 Dec; retry 11 Dec); passport for each person. Take the 09:30 slot. Private van for the day: about 1h each way, 1h15–1h30 from the Ritz. Car park to gate is a 5-min walk, then 1 km between gates: take the ¥5 electric cart for the grandparents and pram. If the morning runs late, 后宫园林 on 秦唐大道 is on the way for lunch.')
# Day 5 — Fri 18 Dec
I('shaanximuseum', D[5], 'Shaanxi History Museum 陕西历史博物馆', "Xi'an", 'Sight', '09:00', '11:30',
  "One of China's great museums: Tang gold and silver, murals, Zhou bronzes. Warm and indoor, a good morning for everyone after yesterday's walking.",
  ('stroller', 'indoor', 'book'), ('must-see',), book="Free, but tickets are a sprint: released 5 days ahead at 17:00 China time, only on the 陕西历史博物馆 WeChat account, real-name, gone in seconds. For Fri 18 Dec that is Sun 13 Dec 17:00 (at KLIA before the flight). If Friday sells out, 14 Dec 17:00 releases Sat 19 Dec: take that and swap it with Saturday's photoshoot. Pre-enter every passport first. Under-6s (or under 1.4 m) and over-65s need no ticket. Winter 09:00–17:30, last entry 16:00, closed Mondays. Plan B if it fails: Small Wild Goose Pagoda + Xi'an Museum (free) this morning.")
I('citywall', D[5], 'City Wall at South Gate 永宁门', "Xi'an", 'Sight', '14:00', '15:45',
  'The most complete old city wall in China, about 14km round and wide enough to cycle. Bikes for the energetic; everyone else strolls a short stretch for the view. South Gate is stairs only, so go up as one group by the lift at 含光门 (inside the Hanguang Gate museum, family toilets on top), stroll a short stretch, come down the same lift and have the vans meet you there. It is about 1.5 km along the wall to South Gate, too far there and back for the grandparents. Winter 08:00–19:00, last entry 18:00.', ('stairs', 'cold'), ('must-see',))
I('belltower', D[5], 'Bell & Drum Towers 钟楼 · 鼓楼', "Xi'an", 'Sight', '16:15', '17:15',
  'The two Ming towers at the heart of the old city, lit up at dusk. Winter 08:30–18:00, last entry 17:30. Entry is through the underpass (metro exit C has a lift) and the tower is spiral stairs, so the grandparents enjoy it from the free square. No stopping at the roundabout: meet the vans on 西大街 by De Fa Chang.', ('easy', 'cold'))
# Day 6 — Sat 19 Dec
I('lunch-d6', D[6], 'Lunch on the train', 'Travel', 'Food', '14:30', '15:15', "No time for a sit-down lunch at the station: buy buns and roujiamo at Xi'an North, or order a hot meal to your seat when booking on Trip.com / 铁路12306. Hot water taps in every carriage.", ('easy', 'indoor'), pic=[])
# Day 7 — Sun 20 Dec
# Day 8 — Mon 21 Dec (most Chengdu museums close on Mondays)
I('rest-d8', D[8], 'Rest, showers & pack (keep the rooms)', 'Chengdu', 'Rest', '14:00', '17:30',
  'The flight leaves after midnight. Keep the rooms until evening (late check-out, or book the night of 21 Dec) so the baby naps and everyone showers before the airport.', ('rest',), pic=REST)

# ---------- decisions: the family votes; the organiser locks the winner ----------
decisions = []
def DEC(id, day, time, title, question, options, kind='activity'):
    decisions.append({'id': id, 'day': day, 'time': time, 'title': title, 'question': question, 'kind': kind, 'options': options})
def O(id, name, city, blurb, fam=(), pic=None, its=()):
    return {'id': id, 'name': name, 'city': city, 'blurb': blurb, 'fam': list(fam), 'img': (gal(pic or id) or [''])[0], 'gallery': gal(pic or id), 'items': ['p:' + x for x in its]}

I('opera', D[1], 'Sichuan Opera face-changing show 蜀风雅韵', 'Chengdu', 'Show', '20:00', '21:30',
  "Chengdu's classic evening show in a teahouse theatre: face-changing, fire-spitting, shadow puppets, comic sketches. Seats with tea. Closer to the JW Marriott: 锦江剧场 Jinjiang Theatre's 《川剧秀·传奇变脸》, nightly 20:00 (weekends 20:30).", ('indoor', 'book'), opt='d-d1eve:opera', pic='sichuanopera', book='Book 1–2 days ahead on Trip.com.')
I('jinli-eve', D[1], 'Jinli Street lanterns 锦里', 'Chengdu', 'Night', '20:15', '21:15', 'Red lanterns reflected in the ponds, snack stalls, next to Wuhou Shrine. Pretty and short.', ('stroller', 'cold'), opt='d-d1eve:jinli', pic='jinli', key='jinli')
I('earlynight', D[1], 'Early night: jet-lag recovery', 'Chengdu', 'Rest', '20:15', '', 'We landed after midnight. Bath, bed.', ('rest',), opt='d-d1eve:rest', pic=REST)
I('pandatower', D[1], 'Panda Tower night view 天府熊猫塔', 'Chengdu', 'Night', '20:00', '21:00',
  "The 339m TV tower, now 'Tianfu Panda Tower': a 1-minute lift to the 230m deck for Chengdu's best night view, with the Mengzhuiwan riverside bars below. Indoor deck, warm in December.", ('easy', 'indoor', 'book'),
  opt='d-d1eve:tower', pic=['img/g/pandatower-1.jpg', 'img/g/mengzhuiwan-1.jpg'],
  book='Tickets about ¥80 (standard lift) or ¥100 (sightseeing lift); under 1.2m free, discounts for 1.2–1.4m children and over-60s. Winter hours 10:00–21:00; confirm last entry and prices on its official account before going.')
DEC('d-d1eve', D[1], '20:00', 'Monday evening', 'After dinner on the first night, what next?', [
  O('opera', 'Sichuan Opera face-changing', 'Chengdu', 'The masks that change in a flash. 1.5h, seats with tea. Late-ish for the baby.', ('indoor', 'book'), 'sichuanopera', ['opera']),
  O('jinli', 'Jinli lanterns stroll', 'Chengdu', 'Short, pretty, lantern-lit old street. About 1 hour.', ('stroller', 'cold'), 'jinli', ['jinli-eve']),
  O('rest', 'Early night', 'Chengdu', 'We land after midnight the night before. Sleep wins.', ('rest',), REST, ['earlynight']),
  O('tower', 'Panda Tower night view', 'Chengdu', "Lift up the 339m tower for Chengdu's best city-lights view. About ¥80–100, under 1.2m free.", ('easy', 'indoor', 'book'), ['img/g/pandatower-1.jpg', 'img/g/mengzhuiwan-1.jpg'], ['pandatower'])])

I('taikooli', D[2], 'Taikoo Li, Daci Temple & the IFS panda 太古里 · 大慈寺', 'Chengdu', 'Shop', '16:00', '18:30',
  'Low-rise open-air shopping streets around a Buddhist temple, then the giant panda climbing the side of IFS. Christmas lights in December.', ('stroller', 'easy'), opt='d-d2pm:taikoo')
I('wuhou', D[2], 'Wuhou Shrine & Jinli 武侯祠 · 锦里', 'Chengdu', 'Sight', '16:00', '18:30',
  'Memorial temple to the Three Kingdoms heroes (Zhuge Liang, Liu Bei) with red walls and bamboo, then the lantern street next door.', ('stroller', 'easy'), opt='d-d2pm:wuhou')
I('pool-d2', D[2], 'Hotel pool, lounge & free time', 'Chengdu', 'Rest', '16:00', '18:30', "Swim, tea, naps. Save energy for Xi'an.", ('rest',), opt='d-d2pm:rest', pic=REST)
I('dongjiao', D[2], 'Eastern Suburb Memory 东郊记忆', 'Chengdu', 'Shop', '16:00', '18:30',
  "A 1950s electronics factory turned art and music park: red-brick halls, old chimneys, cafés, and the red 'Chengdu wall' that fills Xiaohongshu. Free, open all day, flat paths.", ('stroller', 'easy', 'cold'),
  opt='d-d2pm:dongjiao', pic=['img/g/dongjiao-1.jpg'])
DEC('d-d2pm', D[2], '16:00', 'Tuesday late afternoon', 'After the pandas and a nap:', [
  O('taikoo', 'Taikoo Li + IFS panda', 'Chengdu', 'Shopping streets around an old temple, Christmas lights, the famous climbing panda.', ('stroller', 'easy'), 'taikooli', ['taikooli']),
  O('wuhou', 'Wuhou Shrine + Jinli', 'Chengdu', 'Three Kingdoms temple and bamboo gardens, then the lantern street.', ('stroller', 'easy'), 'wuhou', ['wuhou']),
  O('rest', 'Pool & lounge', 'Chengdu', 'A quiet afternoon at the hotel.', ('rest',), REST, ['pool-d2']),
  O('dongjiao', 'Eastern Suburb Memory', 'Chengdu', 'Old factory art park with the famous red Chengdu wall. Free.', ('stroller', 'easy'), ['img/g/dongjiao-1.jpg'], ['dongjiao'])])

I('huaqing', D[4], 'Huaqing Palace 华清宫', "Xi'an", 'Sight', '14:00', '16:00',
  "Tang emperors' hot-spring palace at the foot of Mount Li, next to the Terracotta Army. Gardens and pavilions by a lake. Winter 07:30–18:00, ¥80; entry only via 望京门 (Wangjing Gate).", ('stroller', 'cold'), opt='d-d4pm:huaqing')
I('rest-d4', D[4], 'Back to the hotel to rest', "Xi'an", 'Rest', '14:00', '17:30', 'The Terracotta Army is a long morning on foot. Warm up and nap.', ('rest',), opt='d-d4pm:rest', pic=REST)
I('qianguqing', D[4], "Xi'an Romance show 西安千古情", "Xi'an", 'Show', '15:30', '16:45',
  "A big indoor song-and-dance spectacle (Songcheng) about Xi'an's history: rain on stage, flying sets and horses, at the Expo Park in Chanba, a short detour on the drive back from the Terracotta Army. Allow a ~20 min walk from the gate to the theatre, and note it makes a long day with no rest before dinner.", ('indoor', 'easy', 'book'),
  opt='d-d4pm:qgq', pic=['img/g/qianguqing-1.jpg'],
  book='Tickets ¥278 / ¥328 / ¥580; under 1.2m or under 6 free without a seat (one per adult). Shows usually 13:00 / 15:30 / 17:30 / 19:00, but low season often drops afternoon shows: confirm the Thursday 15:30 exists before choosing this. Similar indoor show in the same area: 驼铃传奇 Camel Bell Legend (see Ideas).')
DEC('d-d4pm', D[4], '14:00', 'Thursday afternoon', 'After the Terracotta Army:', [
  O('huaqing', 'Huaqing Palace', "Xi'an", 'Imperial hot-spring gardens nearby, no extra long drive.', ('stroller', 'cold'), 'huaqing', ['huaqing']),
  O('rest', 'Hotel & rest', "Xi'an", 'Head back, warm up and nap before dinner.', ('rest',), REST, ['rest-d4']),
  O('qgq', "Xi'an Romance show", "Xi'an", 'Big indoor spectacle, short detour on the drive back. From ¥278, little ones free.', ('indoor', 'easy', 'book'), ['img/g/qianguqing-1.jpg'], ['qianguqing'])])

I('juntuan', D[4], 'Resurrected Legion 复活的军团', "Xi'an", 'Show', '14:10', '15:20',
  "An indoor walk-through war epic about the Qin army, at 大秦剧场 (临潼区秦陵北路166号) — the theatre next door to the Terracotta Army, so it needs no extra drive on a day you are already there. Four acts over 70 minutes with 360° projection; ⚠ it is 行进式: you are on your feet for the whole 70 minutes and the theatre does not allocate seats (剧场不对号入座) — straight after three hours walking the Terracotta pits. Some guides mention a separate route for elderly and children; the theatre does not publish one, so do not count on it. Loud battle sound and vibration effects. Several sessions between about 11:30 and 17:00, set day by day — published listings disagree, so confirm for your date.",
  ('indoor', 'book'), opt='d-xashow:juntuan', pic=[],
  book='From ¥268; under 1.2 m free without a seat; real-name tickets, maximum 6 per order. Confirm the session times for your date when booking — they are set day by day. Check it is 《复活的军团》 and not 《永生的军团》, which has used the same theatre.')

I('everlasting', D[4], 'Everlasting Regret show 长恨歌', "Xi'an", 'Show', '18:30', '19:40',
  "Xi'an's most famous show: an outdoor dance-drama on the real lake at Huaqing Palace, Mount Li behind it, telling the story of Emperor Xuanzong and Yang Guifei. It is in Lintong, next to the Terracotta Army, so it follows straight on from the day there. ⚠ It normally pauses for winter (November to about February). A heated-seat winter edition (冰火长恨歌) ran 1 Dec–28 Feb in 2024–25 with sessions at 18:30 / 19:55 / 21:20 / 22:45. Whether it ran last winter, and whether it runs in 2026, is not announced — we would only know in November.",
  ('cold', 'book'), opt='d-xashow:changhen', pic=['https://drive.xile.eu.org/d/inf-xtt/images/2026/05/1779419507854.webp', 'https://drive.xile.eu.org/d/inf-xtt/images/2026/05/1779419729912.webp', 'https://drive.xile.eu.org/d/inf-xtt/images/2026/05/1779419863063.webp'] + gal('huaqing'),
  book='Only if a December run is confirmed: tickets open 5 days ahead at 09:30 China time, from ¥249. The show ticket does NOT include daytime entry to Huaqing Palace.')
I('daqin', D[4], 'Majestic Qin 赳赳大秦', "Xi'an", 'Show', '19:45', '21:05',
  "A big indoor 'epic fantasy' production about the rise of Qin (made by 陕文投, not the 长恨歌 company): moving seats, projection and stage effects rather than a traditional theatre show. 80 minutes, no interval. At Fengdong New City in the west of the city (沣东大道 × 天台路), about 30–40 min from the Bell Tower — the opposite side of town from the Terracotta Army, so this is a drive back in and out again. ⚠ Under-5s are refused outright, so the baby cannot go in. Every seat has a safety belt, and the venue advises against it for anyone 75 or over, pregnant, claustrophobic, or with high blood pressure or heart disease. No re-entry once it starts, and a 10-seat order may not be seated together.",
  ('indoor', 'book'), opt='d-xashow:daqin', pic=['https://jjdq.changhenge.cn/skin/8154/static/picture/project-d1.jpg', 'https://jjdq.changhenge.cn/skin/8154/static/picture/project-d2.jpg', 'https://jjdq.changhenge.cn/skin/8154/static/picture/details01.jpg'],
  book='Shows 14:45 / 16:45 / 19:45 daily; book 10–15 days ahead on 大麦/猫眼 or the official site. Children 5+ pay the adult price.')
I('tuoling', D[4], 'Camel Bell Legend 驼铃传奇', "Xi'an", 'Show', '19:00', '20:10',
  "Indoor Silk Road epic at 华夏大剧院 (灞桥区华文路1518号): real camels and horses on stage, an avalanche, a sandstorm and fire. It sits between Lintong and the city, about 30 min from the Terracotta Army, so it works as a stop on the drive back. ⚠ The auditorium itself rotates to face each scene, and the operator's own notice warns off anyone with heart disease, high blood pressure or difficulty walking. Loud and startling for a baby (free on a lap, but not really suitable). ⚠ Sessions change weekly and the theatre takes an annual maintenance break that fell on 2–20 December in 2024 — check the dates before buying.",
  ('indoor', 'book'), opt='d-xashow:tuoling', pic=[],
  book='¥288–458 by tier; under 1.2 m free on a lap, one per adult. Mostly non-refundable once issued. Confirm the December session times on the 华夏文旅西安度假区 WeChat the week before.')

I('muslimquarter', D[5], 'Muslim Quarter street food 回民街', "Xi'an", 'Food', '17:30', '19:30',
  'The old Hui neighbourhood behind the Drum Tower: lamb skewers, persimmon cakes, sticky rice cake, pomegranate juice. Very crowded, so bring the baby carrier rather than the stroller.', ('cold',), opt='d-d5eve:muslim')
I('tangshow', D[5], 'Tang Dynasty dinner & show 唐乐宫', "Xi'an", 'Show', '18:50', '20:40',
  "Seated dinner from 18:50, then the costumed Tang-court show 《大唐女皇》 19:30–20:40 (19:00 / 20:30 on double-show days). Warm, comfortable, no walking, and done by 20:40 for the baby. 长安北路75号, 10 min from the Bell Tower.", ('indoor', 'easy', 'book'), opt='d-d5eve:tang', book='Dinner packages ¥350 (dumpling banquet) / ¥550 (palace banquet). Winter shows run on demand, so book several days ahead on Trip.com.')
I('gongyan', D[5], 'Tang palace banquet 大明宫宴', "Xi'an", 'Show', '18:15', '21:30',
  "The Xiaohongshu-famous 'go to the palace for dinner': a banquet of Tang palace dishes while a 90-minute show of dance, aerial acts and light plays out on a revolving stage around the tables. Optional Tang costume and make-up before. In the old city's north, near Xi'an Railway Station (新城区笃臣路6号), about 15 min from the Bell Tower. (Photo: a similar Tang performance, not the venue.)", ('indoor', 'book'),
  opt='d-d5eve:gongyan', pic=['img/g/datang-4.jpg'],
  book='Doors 17:30, evening show 19:00 (lunch 12:00): arrive 30 min early, or 1 h (18:00) with costumes. From about ¥263 per person with the meal; children pay the adult price; costume styling costs extra. Book 1–2 days ahead (Qunar / Trip.com or its mini-program, tel 400-009-6616) and ask for seats together for 10.')
I('changan12', D[5], "Chang'an Twelve Hours Tang street 长安十二时辰", "Xi'an", 'Show', '18:00', '21:00',
  "An indoor Tang-dynasty market street in 曼蒂广场, on the east side of the Great Tang All Day Mall: costumed performers, snack stalls, costume rental and photo corners, plus the 乐宴·盛唐 banquet show inside. Warm and indoor; about 30 min from the Bell Tower in Friday traffic. (Photo: the Great Tang All Day Mall next door, not the street itself.)", ('indoor', 'stroller', 'book'),
  opt='d-d5eve:c12', pic=['img/g/datang-1.jpg'],
  book='Entry ¥128 adult / ¥68 child, under 1.2m free; open 10:00–22:00. The 乐宴·盛唐 banquet inside is booked separately.')
I('yongxingfang', '', 'Yongxingfang food street 永兴坊', "Xi'an", 'Food', '', '',
  'A calmer, tidier food street by the city wall, with snacks from all over Shaanxi.', ('stroller', 'cold'))
I('eve-free', D[4], 'No show — dinner in town and an early night', "Xi'an", 'Rest', '18:30', '20:30',
  'Your Thursday dinner pick near the Bell Tower, then bed after a long day on foot.', ('rest',), opt='d-xashow:none', pic=REST)
DEC('d-xashow', D[4], '', 'Which show shall we book?', 'We can realistically fit ONE show, maybe two. Pick the one you most want to see and we will build the day around it. Everything below is confirmed to run in December — except 长恨歌, which is marked. ⚠ = something to read before you pick. Note there are other shows on the Thursday-afternoon and Friday-evening votes too: one big production is plenty for this family, with a baby and two grandparents, so if you pick one here, pick the quiet option there.', [
  O('juntuan', '复活的军团 Resurrected Legion', "Xi'an", '¥268 · 70 min · indoor. Qin war epic in the theatre right next to the Terracotta Army, so it costs no extra driving on Thursday. ⚠ You are on your feet the whole 70 min with no allocated seats, straight after the Terracotta pits. Loud battle effects.', ('indoor', 'book'), [], ['juntuan']),
  O('menghui', '梦回大唐 Dream Back to the Tang', "Xi'an", '¥298–518 · about 1h · indoor, park entry included. Tang court dance in a seated theatre. The easiest on Ah Ma and Ah Gong: sit down, warm, no walking. Free park entry for over-65s. ⚠ Start time unconfirmed — 17:00 or 19:30.', ('indoor', 'easy', 'book'), 'tangparadise', ['menghui']),
  O('qgq', '西安千古情 Romance of Xi\'an', "Xi'an", 'From ¥278 · 60 min · indoor. Big song-and-dance spectacle with rain, flying sets and horses on stage, at Chanba — a short detour on the drive back from the Terracotta Army. Little ones free. (It is also on the Thursday-afternoon vote.)', ('indoor', 'easy', 'book'), ['img/g/qianguqing-1.jpg'], ['qianguqing']),
  O('daqin', '赳赳大秦 Majestic Qin', "Xi'an", 'From ¥338 · 80 min · indoor · 19:45, west of the city. The one locals rank top: moving seats, projection and stage machinery, more ride than play. ⚠ Under-5s are refused, so the baby cannot come, and it is advised against for 75+, high blood pressure, heart disease or pregnancy — so part of the family would stay behind. Dinner would have to be early.', ('indoor', 'book'), ['https://jjdq.changhenge.cn/skin/8154/static/picture/project-d1.jpg', 'https://jjdq.changhenge.cn/skin/8154/static/picture/project-d2.jpg'], ['daqin']),
  O('tuoling', '驼铃传奇 Camel Bell Legend', "Xi'an", '¥288–458 · 70 min · indoor. Silk Road epic with real camels and horses, between Lintong and the city so it fits the drive back. ⚠ The seating bank rotates, and the operator warns off heart, blood-pressure and walking trouble; loud for the baby. Its yearly maintenance break fell on 2–20 December in 2024 — check before booking.', ('indoor', 'book'), [], ['tuoling']),
  O('changhen', '长恨歌 Everlasting Regret', "Xi'an", 'From ¥249 · 70 min · OUTDOORS at Huaqing Palace, next to the Terracotta Army. The famous one. ⚠ It normally shuts for winter (November to about February). A heated-seat December edition has run some years but did NOT run last winter and is not announced for 2026 — we would only know in November. Pick it if you want it if it happens.', ('cold', 'book'), ['https://drive.xile.eu.org/d/inf-xtt/images/2026/05/1779419507854.webp', 'https://drive.xile.eu.org/d/inf-xtt/images/2026/05/1779419729912.webp'], ['everlasting']),
  O('none', 'No show — keep the evenings free', "Xi'an", 'Skip it. The Terracotta day is already long on foot, and the Muslim Quarter, the Great Tang night walk and the Tang banquet on Friday are evenings in themselves.', ('rest',), REST, ['eve-free'])])
DEC('d-d5eve', D[5], '17:30', 'Friday evening', "Last night in Xi'an:", [
  O('muslim', 'Muslim Quarter food crawl', "Xi'an", 'The famous one: loud, crowded, delicious.', ('cold',), 'muslimquarter', ['muslimquarter']),
  O('tang', 'Tang Dynasty dinner show', "Xi'an", 'Sit-down dinner with a big costumed show. Easiest for the grandparents.', ('indoor', 'easy', 'book'), 'tangshow', ['tangshow']),
  O('gongyan', 'Tang palace banquet', "Xi'an", 'Dinner of Tang palace dishes with a 90-min show around the table. From ¥263 each, 19:00.', ('indoor', 'book'), ['img/g/datang-4.jpg'], ['gongyan']),
  O('c12', "Chang'an Twelve Hours street", "Xi'an", 'Indoor Tang market street: performers (极乐之宴 among them), snacks, costumes. ¥68 entry.', ('indoor', 'stroller', 'book'), ['img/g/datang-1.jpg'], ['changan12'])])

I('hanfu', D[6], 'Tang costume family photoshoot 唐装 · 汉服', "Xi'an", 'Show', '08:00', '11:00',
  "Rent Tang-style robes near the Big Wild Goose Pagoda and take family portraits. Hair and make-up take about 45 min a head, so two stylists from 08:00 manage about 5 people by 11:00: choose who gets styled (the kids plus 1–2 adults). Pack before you go; back at the hotel about 11:40 to change and load for the 12:15 vans. Eat a proper breakfast and carry snacks: lunch is on the 14:06 train. If Friday's museum tickets fail and you get Saturday's, swap this to Friday morning.", ('easy', 'book'), opt='d-d6am:hanfu', pic=['img/g/datang-4.jpg', 'img/g/datang-3.jpg'], book='Book two stylists for 08:00, 1–2 days ahead (studios normally open ~10:00). Make-up ¥100–300 a head.')
I('smallgoose', D[6], "Small Wild Goose Pagoda & Xi'an Museum 小雁塔 · 西安博物院", "Xi'an", 'Sight', '09:30', '11:30',
  'Quiet temple garden with a slender Tang pagoda, and a free city museum in the same grounds. Calm and flat.', ('stroller', 'easy'), opt='d-d6am:goose')
I('slow-d6', D[6], 'Slow morning, brunch & pack', "Xi'an", 'Rest', '09:30', '11:30', 'Lie-in before the train.', ('rest',), opt='d-d6am:slow', pic=REST)
DEC('d-d6am', D[6], '08:00', 'Saturday morning', 'Before the afternoon train back to Chengdu:', [
  O('hanfu', 'Tang costume family photos', "Xi'an", 'Tang robes for portraits by the pagoda: about 5 people styled (kids + 1–2 adults), two stylists from 08:00.', ('easy', 'book'), ['img/g/datang-4.jpg', 'img/g/datang-3.jpg'], ['hanfu']),
  O('goose', 'Small Wild Goose Pagoda', "Xi'an", 'Peaceful garden and free museum.', ('stroller', 'easy'), 'smallgoose', ['smallgoose']),
  O('slow', 'Slow morning', "Xi'an", 'Sleep in, brunch, pack.', ('rest',), REST, ['slow-d6'])])

I('leshan-train', D[7], 'G-train Chengdu East → Leshan 乐山', 'Chengdu', 'Travel', '08:30', '09:40', 'About 1 hour, then 30 min by van to the river pier.', ('book',), opt='d-d7:leshan', pic='hsr', key='cdeast',
  book='Train tickets open 15 days ahead counting the travel day: Sun 6 Dec for both the outbound and return trains.')
I('leshan', D[7], 'Leshan Giant Buddha by boat 乐山大佛', 'Chengdu', 'Sight', '10:30', '12:30',
  'The 71m Buddha carved into a riverside cliff 1,200 years ago. The river boat shows the whole figure with no steps, which is best for the baby and grandparents. The path down beside the Buddha is hundreds of steep steps with long queues; optional for the fit. The boat pier has moved recently (嘉州渡码头 opened July 2025, then a November 2025 notice suspended it), so check where boats board nearer the date.', ('cold',), opt='d-d7:leshan')
I('leshan-back', D[7], 'G-train Leshan → Chengdu East', 'Chengdu', 'Travel', '15:00', '16:10', 'Taxi or van back to Leshan station after lunch, then about 1 hour to Chengdu East.', ('book',), opt='d-d7:leshan', pic='hsr', key='leshanstn')
I('dujiangyan', D[7], 'Dujiangyan irrigation system 都江堰', 'Chengdu', 'Sight', '09:30', '14:30',
  'A 2,200-year-old river engineering wonder that still waters the Chengdu plain: rushing water, suspension bridges and hillside temples, about 1h by van. Some slopes and steps.', ('stairs', 'cold'), opt='d-d7:djy')
I('dufu', D[7], 'Du Fu Thatched Cottage 杜甫草堂', 'Chengdu', 'Sight', '09:30', '11:30',
  "Bamboo groves, streams and the poet Du Fu's cottage in a large, calm garden. Flat paths.", ('stroller', 'easy'), opt='d-d7:city')
I('sichuanmuseum', D[7], 'Sichuan Museum 四川博物院', 'Chengdu', 'Sight', '14:00', '16:00',
  "Right by Du Fu's cottage: Sichuan bronzes, Han pottery, Buddhist sculpture. Free and indoor. Closed Mondays, so Sunday is its day.", ('stroller', 'indoor', 'book'), opt='d-d7:city',
  book='Free with passport; reserve on its WeChat a few days ahead.')
I('naturalhistory', D[7], 'Chengdu Natural History Museum (dinosaurs) 成都自然博物馆', 'Chengdu', 'Sight', '10:00', '13:00',
  'A huge hall of dinosaur skeletons found in Sichuan, plus minerals and animals. Indoor and warm, made for the kids.', ('stroller', 'indoor', 'book'), opt='d-d7:dino', book='Reserve on its WeChat a few days ahead; closed Mondays.')
I('tea-d7', D[7], "Afternoon tea & rest", 'Chengdu', 'Rest', '14:00', '17:00', "Back to the hotel, or a second round of tea in People's Park.", ('rest',), opt='d-d7:dino', pic='peoplespark', key='peoplespark')
DEC('d-d7', D[7], '09:00', 'Sunday: the big one', 'Pick the whole day:', [
  O('leshan', 'Leshan Giant Buddha', 'Chengdu', 'Day trip by 1h fast train. See the 71m cliff Buddha from a boat, no stairs needed.', ('cold', 'book'), 'leshan', ['leshan-train', 'leshan', 'leshan-back']),
  O('djy', 'Dujiangyan', 'Chengdu', 'Ancient waterworks, bridges and temples in green hills. 1h by van, some steps.', ('stairs', 'cold'), 'dujiangyan', ['dujiangyan']),
  O('city', 'Du Fu Cottage + Sichuan Museum', 'Chengdu', 'Stay in town: bamboo garden in the morning, museum next door after lunch.', ('stroller', 'easy'), 'dufu', ['dufu', 'sichuanmuseum']),
  O('dino', 'Dinosaur museum + easy afternoon', 'Chengdu', "Kids' pick: giant Sichuan dinosaurs, then tea and rest.", ('stroller', 'indoor'), 'naturalhistory', ['naturalhistory', 'tea-d7'])])

I('wenshu', D[8], 'Wenshu Monastery 文殊院', 'Chengdu', 'Sight', '10:30', '12:30',
  "Chengdu's busiest Buddhist temple: incense and quiet courtyards. Its well-known vegetarian restaurant can replace lunch if you prefer.", ('stroller', 'easy'), opt='d-d8am:wenshu')
I('shopping', D[8], 'Last-minute shopping: IFS & Chunxi Road', 'Chengdu', 'Shop', '10:30', '12:30', 'Panda souvenirs, Sichuan pepper and tea to take home.', ('stroller', 'easy', 'indoor'), opt='d-d8am:shop', pic='ifspanda', key='ifs')
I('pool-d8', D[8], 'Pool & slow morning', 'Chengdu', 'Rest', '10:30', '12:30', 'Rest up before the overnight flight.', ('rest',), opt='d-d8am:rest', pic=REST)
DEC('d-d8am', D[8], '10:30', 'Monday morning', 'Last morning (most museums are closed on Mondays):', [
  O('wenshu', 'Wenshu Monastery', 'Chengdu', 'Temple courtyards, incense and ginkgo trees.', ('stroller', 'easy'), 'wenshu', ['wenshu']),
  O('shop', 'Shopping at IFS & Chunxi Rd', 'Chengdu', 'Souvenirs, tea, Sichuan pepper.', ('stroller', 'indoor'), 'ifspanda', ['shopping']),
  O('rest', 'Pool & slow morning', 'Chengdu', 'Save energy for the 1am flight.', ('rest',), REST, ['pool-d8'])])


# ---------- meals: 3–4 places per lunch/dinner, every restaurant used ONCE in the trip ----------
# Tze 14 Sep: "some are too spicy ... accommodate 10 pax"; 14 Sep: affordable, one or two memorable;
# 15 Sep: "You keep repeating the options. Don't show me repeated options. Give me more options."
# check_site.py fails the build if one brand appears in two meal votes.
# Checked 14–15 Sep 2026 on Ctrip / Trip.com / Qunar / 本地宝 / news. 大众点评 blocks scripts, so seating for 10
# is rarely confirmed: every card says to confirm when booking.
MEAL_DET = {}
DISH = 'Photos show the dish, not this restaurant. Tap 小红书 or 大众点评 for the place itself.'
def MO(oid, id, name, short, blurb, info, fam, pic, when, price, getting, kids='', elderly='', book='', watch='', cat='Food', mapcity=None, time=None, end=None, en=None, pp='', special=False, brand=''):
    return dict(oid=oid, id=id, name=name, short=short, blurb=blurb, info=info, fam=fam, pic=pic, book=book, cat=cat, mapcity=mapcity, time=time, end=end, en=en, pp=pp, special=special, brand=brand,
                det={'when': when, 'price': price, 'getting': getting, 'kids': kids, 'elderly': elderly, 'watch': watch, 'photo': DISH if pic else 'No photos yet: tap 小红书 or 大众点评.'})
def MEAL(did, day, time, end, title, question, *opts):
    city = next(c for d, c, _ in DAYS if d == day)
    out = []
    for o in opts:
        if o['mapcity']: MAPCITY[o['id']] = o['mapcity']
        if o['det'].get('watch'):
            MAPQ[o['id']] = re.sub(r'^(成都|西安|乐山) ', '', o['det']['watch'])
            en = o['en'] or re.sub(r'\s+', ' ', re.sub(r'[㐀-鿿·]+', '', o['name'].split('— ', 1)[-1])).strip()
            MAPEN[o['id']] = en
        I(o['id'], day, o['name'], city, o['cat'], o['time'] or time, o['end'] or end, o['info'], o['fam'], pic=o['pic'], opt=f"{did}:{o['oid']}", book=o['book'])
        MEAL_DET['p:' + o['id']] = {k: v for k, v in o['det'].items() if v}
        items[-1]['brand'] = o['brand'] or re.sub(r'^(成都|西安|乐山) ', '', o['det'].get('watch') or o['name']).split(' ')[0]
        out.append(dict(O(o['oid'], o['short'], city, o['blurb'], o['fam'], o['pic'] or [], [o['id']]), pp=o['pp'], special=o['special']))
    DEC(did, day, time, title, question, out, kind='meal')

CONFIRM = ' Confirm a table or room for 10 when you book.'
# --- Chengdu, Mon 14 Dec ---
MEAL('m-d1lunch', D[1], '12:00', '13:15', 'Monday lunch', "Before People's Park:",
  MO('mapo', 'lunch-mapo', 'Lunch — Chen Mapo Tofu 陈麻婆豆腐 (flagship)', 'Chen Mapo Tofu', 'The famous mapo tofu house. Spicy, with 不辣 dishes for the kids.',
     "The flagship of the famous mapo tofu house. Spicy by nature: order mapo tofu 微辣 (mild) for the adults, and 不辣 (no chilli) dishes such as 宫保鸡丁 kung pao chicken and 鸡丝面 chicken noodles for the kids and elderly.",
     ('easy', 'spicy'), 'mapotofu', 'Opens 11:00; closed mid-afternoon', 'About ¥50–70 per person', "青羊区东华门街51号 (富力中心B座), a short drive from People's Park",
     kids='Order the 不辣 dishes; most of the menu has chilli', elderly='Several floors: ask for the lift', book='Private rooms have had a minimum spend (about ¥800 in older reviews); confirm when booking.', watch='成都 陈麻婆豆腐 总店', pp='¥50–70'),
  MO('zsj', 'zsj-d1', 'Lunch — Zhong Shui Jiao 钟水饺 (inside the park)', 'Zhong dumplings (in the park)', 'The 1893 dumpling house, in its own pavilion inside the park. Cheap and mild.',
     "The 1893 dumpling house has its own two-storey pavilion (紫薇阁) inside People's Park, so lunch and the park are the same stop. Ask for 清汤 (clear soup) rather than 红油 (chilli oil): 清汤水饺 and 抄手 wontons, 叶儿粑 rice-leaf cakes, 蛋烘糕 egg cakes, 银耳羹 white fungus soup.",
     ('stroller', 'easy', 'indoor'), 'dumplings', '08:30–20:00', 'About ¥32–41 per person', '青羊区少城路12号 人民公园内紫薇阁',
     kids='Mild if you ask for 清汤; sweet snacks', elderly='In the park, no extra walking', book='Ground floor is walk-in; the upstairs room does set menus. Call 028-86130521 to ask for 10 together.' + CONFIRM, watch='成都 钟水饺 人民公园总店', pp='¥35'),
  MO('pss', 'pss-d1', 'Lunch — Pan Sun Shi braised meats 盘飧市', 'Pan Sun Shi (braised, mild)', 'A century-old braised-meat house. Mild and cheap, with rooms.',
     "A century-old Chengdu 卤味 house for soy-braised meats, generally mild: 卤猪蹄 braised pig trotters, 卤肉锅盔 braised-pork flatbread, 糖醋排骨 sweet-and-sour ribs, 卤鸭舌 duck tongues. Its famous 卤肉包子 buns are only sold from 15:30. Reported to have private rooms (the largest seats 14–16, with a room fee).",
     ('easy', 'indoor', 'book'), ['img/g/food-luwei-3.jpg', 'img/g/food-luwei-2.jpg'], 'Confirm hours when booking', 'About ¥60–80 per person', "锦江区华兴街62-63号, near 王府井; about 8 min by taxi from People's Park",
     kids='Mild braised meats', elderly='Rooms on an upper floor: ask about the lift', book='Book a room for 10 on 028-86750609 (room details come from an undated source).', watch='成都 盘飧市 华兴街', en='Pan Sun Shi Chengdu', pp='¥70'),
  MO('lmt', 'lmt-d1', 'Lunch — Liao Lao Ma pig trotter soup 廖老妈蹄花', 'Liao Lao Ma trotter soup', 'Milky trotter-and-bean soup: genuinely not spicy, and very cheap.',
     "Chengdu's comfort food: pork trotters stewed white with butter beans until they fall apart, with a chilli dip on the side that you can skip. Simple, soft food that suits the grandparents and the kids; open around the clock.",
     ('easy', 'indoor'), [], '24 hours', 'About ¥55 per person', '青羊区东城根南街7号',
     kids='Soft, mild; skip the dip', elderly='Very easy to eat', book='Small local place: go early or call ahead.' + CONFIRM, watch='成都 廖老妈蹄花 东城根南街', en='Liao Lao Ma Ti Hua', pp='¥55'))
MEAL('m-d1din', D[1], '18:00', '19:30', 'Monday dinner', 'Before the evening out (the opera starts at 20:00):',
  MO('tx', 'tx-d1', 'Dinner — Tingxiang old-mansion Sichuan 听香·老公馆 (Kuanzhai Alley)', 'Tingxiang (mild Sichuan)', 'Old-mansion Sichuan that plays down the chilli. Big tables and rooms. About ¥82.',
     "A restored old mansion at the east end of Kuanzhai Alley whose cooking deliberately plays down the chilli: 蜜汁包公鸭 honey duck, 山楂酒香东坡肉 pork belly with hawthorn, 皇菇煨土鸡 mushroom chicken soup, 上汤娃娃菜 cabbage in broth, 熊猫汤圆 panda rice balls (skip 毛血旺 and 夫妻肺片). Courtyard plus two floors with private rooms; big tables for 10+, baby chairs and an English menu. About 8 min by taxi to the opera.",
     ('easy', 'indoor', 'book'), ['img/g/food-teaduck-1.jpg', 'img/g/food-kaishui-2.jpg'], '11:00–21:00', 'About ¥82 per person', '青羊区宽巷子6号 (east plaza of Kuanzhai Alley)',
     kids='Mild by design; baby chairs', elderly='Courtyard seating; ask for a ground-floor room', book='Book at least half a day ahead: 028-86639558 / 18086832900.', watch='成都 听香 老公馆 宽巷子', en='Tingxiang Restaurant Kuanzhai', pp='¥82'),
  MO('tlk', 'tlk-d1', 'Dinner — Taolin Sichuan home cooking 饕林餐厅 (Kuixinglou St)', 'Taolin (Sichuan, ask for 不辣)', 'Good-value Sichuan near Kuanzhai Alley. The famous dishes are spicy: order 不辣.',
     "The Kuixinglou Street branch of a popular, good-value Chengdu home-cooking restaurant, a short walk from Kuanzhai Alley and 10–12 min by taxi to the opera. Its best-known dishes are spicy; milder picks: 高压锅牛肉 pressure-cooked beef, 锅边馍, 石磨黑豆花 black-bean tofu pudding, and the free 红豆薏米粥 porridge at the end; ask for 白肉 with the sauce on the side. Private dining and high chairs listed.",
     ('indoor', 'spicy', 'book'), ['img/g/sichuandishes-1.jpg'], 'Dinner 17:00–21:30 (lunch hours listed differently; confirm)', 'About ¥65 per person', '青羊区奎星楼街16号附9号',
     kids='Order the mild dishes; high chairs', elderly='Ask for a table near the entrance', book='Book on 19113267235 and ask for a room or big table for 10.', watch='成都 饕林餐厅 奎星楼店', en='Taolin Restaurant Kuixinglou', pp='¥65'),
  MO('dn', 'dn-d1', 'Dinner — Douniu Chaoshan beef hot pot 斗牛潮汕牛肉火锅', 'Chaoshan beef hot pot (clear broth)', 'Clear-broth beef hot pot by Kuanzhai Alley. Not spicy.',
     "Chaoshan-style hot pot: fresh-cut beef cooked for seconds in a clear beef broth, so nothing is spicy unless you add the chilli dip: 吊龙 and 匙仁 beef cuts, 手打牛肉丸 hand-beaten beef balls, vegetables. Right by Kuanzhai Alley, 10 min by taxi to the opera.",
     ('easy', 'indoor', 'book'), ['img/g/food-beefhotpot-1.jpg', 'img/g/food-beefhotpot-2.jpg', 'img/g/food-beefhotpot-3.jpg'], 'Confirm hours when booking', 'About ¥85 per person', '青羊区西二道街18号附18号, by Kuanzhai Alley',
     kids='Clear broth; beef balls are a hit', elderly='Soft, freshly cooked beef', book='Call 028-86639260 to book, and check it is still open (no recent review found).', watch='成都 斗牛潮汕牛肉火锅 宽窄巷子', en='Douniu Chaoshan Beef Hot Pot Kuanzhai', pp='¥85'),
  MO('sh', 'sh-d1', 'Dinner — Suihe family banquet 随和家宴 (Qingyang Temple)', 'Suihe family banquet', 'Banquet restaurant with many private rooms, a 10-minute walk from the opera.',
     "A family-banquet restaurant a 10-minute walk from the opera theatre, with a banquet hall and a whole floor of private rooms. Mild dishes: 松茸土鸡汤 matsutake chicken soup, 花胶山药焖蹄筋, 鲍鱼红烧肉 braised pork with abalone, 煲仔焗山药 baked yam, 桃胶椰子冻 coconut jelly (avoid 沸腾鱼 and 泡椒乌鱼片). Big tables for 10+, baby chairs and free parking.",
     ('easy', 'indoor', 'book'), [], '10:00–14:00, 16:30–21:00', 'About ¥105 per person: the priciest here', '青羊区一环路西一段166号',
     kids='Mild banquet dishes; baby chairs', elderly='Private room, no queue, short walk to the opera', book='Book a private room: 028-87742388 / 87786338.', watch='成都 随和家宴 青羊宫', en='Suihe Jiayan Chengdu', pp='¥105'))
# --- Chengdu, Tue 15 Dec ---
MEAL('m-d2lunch', D[2], '12:15', '13:15', 'Tuesday lunch', 'After the pandas, on the way back for a nap:',
  MO('zy', 'zy-d2', 'Lunch — Zhuyun bamboo restaurant 竹韵餐厅 (inside the Panda Base)', 'Zhuyun (inside the panda base)', 'Bamboo-shoot cooking inside the base itself: 7 private rooms, no travel.',
     "The Panda Base's own restaurant, about 300 m from the entrance, serving a bamboo menu: 笋子蛋汤 bamboo-shoot egg soup, 竹荪汤 bamboo fungus soup, 竹燕窝蒸蛋 steamed egg, 竹筒饭 bamboo rice, 鲜笋炒肉丝 pork with bamboo shoots, 熊猫汤圆 panda rice balls (skip 水煮肉片 and 麻婆豆腐). Seven private rooms over two floors. Eat at 11:30 straight after the visit, before leaving the ticketed area, and you are back for the nap sooner.",
     ('stroller', 'easy', 'indoor', 'book'), ['img/g/food-bamboo-1.jpg'], '09:00–17:30', 'About ¥60 per person', '成华区外北熊猫大道1375号, inside the Panda Base',
     kids='Mild bamboo dishes; panda rice balls', elderly='No travel after the morning walk', book='Book a room: 17311072681 / 028-83533916.', watch='成都 竹韵餐厅 熊猫基地', en='Zhuyun Restaurant Panda Base', pp='¥60', time='11:30', end='12:30'),
  MO('lcs', 'lunch-longchaoshou', 'Lunch — Long Chao Shou wontons 龙抄手', 'Long Chao Shou wontons', 'Cheap, mild Chengdu snacks near the hotel. Canteen style.',
     "A Chengdu snack institution near Chunxi Road: 鸡汤抄手 wontons in chicken soup, 赖汤圆 glutinous rice balls, 蛋烘糕 egg cakes, 银耳羹 white fungus soup. Mostly mild. Canteen style: order at the counter, no private rooms, so 10 people may need two tables.",
     ('easy', 'indoor'), ['img/g/food-wontonsoup-1.jpg', 'img/g/food-wontonsoup-2.jpg'], 'About 09:00–21:30 (older data)', 'About ¥30 per person', '锦江区城守街63号 (近中山广场)',
     kids='Mild food; red-oil wontons are the spicy ones', elderly='Seating is downstairs: stairs', watch='成都 龙抄手 春熙路总店', en='Long Chao Shou Chunxi Road', pp='¥30'),
  MO('ddd', 'ddd-d2', 'Lunch — Dian Dou De dim sum 点都德 (Longfor Paradise Walk)', 'Dian Dou De dim sum', "Guangzhou dim sum in a mall on the way back. Not spicy.",
     "Guangzhou's dim sum chain, in the 龙湖上城天街 mall on the ring road between the Panda Base and the city: 虾饺皇 har gow, 金沙红米肠 rice rolls, 流沙包 custard buns, 艇仔粥 congee. Not spicy; tables for 8–10.",
     ('stroller', 'easy', 'indoor'), ['img/g/food-dimsum-1.jpg', 'img/g/food-charsiubao-1.jpg'], '10:00–21:30', 'About ¥85 per person', '金牛区一环路北二段 龙湖上城天街 4F',
     kids='Nothing spicy', elderly='Mall lift', watch='成都 点都德 上城天街', pp='¥85'),
  MO('gj', 'gj-d2', 'Lunch — Gangjiu Hong Kong café 港久茶餐厅 (MixC mall)', 'Gangjiu HK café', 'Hong Kong café food, nothing spicy, on the way back into town.',
     "A Hong Kong cha chaan teng in the MixC mall, 25–30 min from the Panda Base toward the centre: 烧腊双拼 roast meats, 干炒牛河 beef ho fun, 例汤 and congee, 菠萝油 pineapple bun, 蒸凤爪 steamed chicken feet. Nothing spicy.",
     ('stroller', 'easy', 'indoor'), ['img/g/food-beefhofun-1.jpg', 'img/g/food-pineapplebun-1.jpg'], '11:00–21:30', 'About ¥48–88 per person', '成华区双庆路8号 万象城二期 D馆 4F',
     kids='Familiar Cantonese food', elderly='Mall lift', book='No private room: ask them to join tables. 028-62310517.', watch='成都 港久茶餐厅 万象城', en='Gangjiu Cha Chaan Teng MixC Chengdu', pp='¥48–88'))
MEAL('m-d2din', D[2], '19:00', '20:30', 'Tuesday dinner', 'After the afternoon out:',
  MO('hdl', 'hdl-d2', 'Dinner — Haidilao hot pot 海底捞 (Qunguang Plaza)', 'Haidilao (tomato / mushroom broth)', 'Hot pot without the heat, 1 km from Taikoo Li. Great with kids.',
     "Hot pot without the heat: pick 番茄 tomato or 菌汤 mushroom broth. Known for looking after families (baby chairs, the noodle-pulling show). About 1 km from Taikoo Li on Chunxi Road.",
     ('easy', 'indoor'), ['img/g/food-tomatohotpot-1.jpg', 'img/g/food-haidilao-1.jpg'], '11:00–03:00', 'Roughly ¥90–110 per person', '锦江区春熙路南段8号 群光广场 9F',
     kids='Baby chairs (usual at Haidilao; confirm for this branch)', elderly='Mall lift', book='Book in the Haidilao app or on 028-65000088.', watch='成都 海底捞 群光广场', pp='¥90–110'),
  MO('ls', 'ls-d2', 'Dinner — Loushang Cantonese dai pai dong 楼上大排档 (Taikoo Li)', 'Loushang (Cantonese)', 'Cantonese roast meats and claypots, 10 min from Taikoo Li. Mostly mild.',
     "A Cantonese 大排档 near Taikoo Li: 明炉烧鹅 roast goose, 苦瓜排骨汤 bitter-melon pork-rib soup, 干炒牛河 beef ho fun, seafood congee. Mostly mild — avoid the 辣啫 chilli claypots. Open very late.",
     ('easy', 'indoor', 'book'), ['img/g/food-roastgoose-1.jpg', 'img/g/food-roastgoose-2.jpg'], '11:30–14:30, 17:00–03:00', 'About ¥101 per person', '锦江区下东大街段169号 晶融汇二期 2F',
     kids='Roast meats and congee', elderly='Mall building, lift', book='Call 19113239505.' + CONFIRM, watch='成都 楼上大排档 太古里', en='Loushang Dai Pai Dong Chengdu', pp='¥101'),
  MO('sdx', 'sdx-d2', 'Dinner — Shudaxia hot pot 蜀大侠 (Chunxi Road)', 'Shudaxia hot pot, split pot', 'Big-name Chengdu hot pot with private rooms. Split pot with a mushroom side.',
     "A big-name Chengdu hot pot chain at the south end of Chunxi Road, over two floors with private rooms and tables for 8–10. Order a 鸳鸯锅 split pot with the 菌汤 mushroom side for the kids and elderly (confirm this branch offers it): 虾滑 shrimp paste, 酥肉 crispy pork, 肥牛 beef, 红糖糍粑 brown-sugar rice cakes.",
     ('spicy', 'indoor', 'book'), ['img/hotpot.jpg', 'img/g/hotpot-1.jpg'], '11:00–01:00', 'About ¥90 per person', '锦江区上东大街6号 春南商场 2F',
     kids='Keep them on the mushroom side; high chairs', elderly='2nd floor; ask for the lift', book='Book a room: 028-87666679 (confirm the room and any minimum spend).', watch='成都 蜀大侠火锅 春熙店', en='Shudaxia Hot Pot Chunxi', pp='¥90'))
# --- Xi'an, Wed 16 Dec ---
MEAL('m-d3din', D[3], '18:30', '19:45', 'Wednesday dinner', 'By the Big Wild Goose Pagoda, before the night walk:',
  MO('dpd', 'dinner-dapaidang', "Dinner — Chang'an Da Pai Dang 长安大牌档 (Joy City)", "Chang'an Da Pai Dang", 'Lively themed Shaanxi restaurant, kids love it. Mild dishes available.',
     "A lively Journey-to-the-West themed Shaanxi restaurant in 曲江大悦城, a short walk from the Great Tang All Day Mall. Mild picks: 葫芦鸡 crispy gourd chicken, 妃子笑 shrimp balls, 毛笔酥 brush-shaped pastries, 醪糟冰淇淋 rice-wine ice cream. Skip the 油泼 chilli-oil noodles for the kids.",
     ('indoor', 'book'), 'biangbiang', 'From 11:00', 'About ¥50 per person', '雁塔区慈恩西路777号 曲江大悦城 3F',
     kids='Staff in costume; order the mild dishes', elderly='Mall lift; busy and loud', book='Private rooms go fast: book several days ahead on 029-65658866. The main hall is queue-only.', watch='西安 长安大牌档 西游漫记 大悦城', pp='¥50'),
  MO('xafz', 'xafz-d3', "Dinner — Xi'an Fanzhuang 西安饭庄 (Great Tang All Day Mall)", "Xi'an Fanzhuang (Shaanxi, mild)", "Xi'an's best-known old restaurant, on the night-walk street. Not spicy.",
     "Xi'an's best-known old restaurant (since 1929), with a branch on the Great Tang All Day Mall itself: 金牌葫芦鸡 gourd chicken, 锅贴 potstickers, 糖醋小排 sweet-and-sour ribs, 桂花凉糕 osmanthus rice cake, mini roujiamo. Not spicy.",
     ('easy', 'indoor', 'book'), ['img/g/food-guotie-1.jpg'], '11:00–24:00', 'About ¥75–100 per person', '雁塔区雁塔南路518号 大唐不夜城 A6-F区',
     kids='Nothing spicy on the classics', elderly='Private room, no queue', book='Book a private room for 10.', watch='西安饭庄 大唐不夜城', pp='¥75–100'),
  MO('bpb', 'bpb-d3', "Dinner — Benpaoba Shaanxi 奔跑吧陕菜·雁塔长安", 'Benpaoba (Shaanxi, top-rated)', "Top-rated Shaanxi restaurant by the pagoda, about ¥58. Mixed spice.",
     "Rated top of the 大雁塔 food list (4.8): 长安葫芦鸡 gourd chicken, 长安的荔枝 shrimp balls, 贵妃凉糕 sweet rice cake, 腊汁肉夹馍 roujiamo. Its 富平油泼辣子鱼 fish is hot, so order around it. Packed at mealtimes; the dining room is built for photos.",
     ('easy', 'indoor', 'book'), ['img/g/food-tangcu-1.jpg'], 'Confirm hours when booking', 'About ¥58 per person', '雁塔区芙蓉东路6-1号 大雁塔北广场E座 1F',
     kids='Order the mild dishes', elderly='5 min by van to the night walk', book='Book on 大众点评 (no phone listed).' + CONFIRM, watch='西安 奔跑吧陕菜 雁塔长安', en='Benpaoba Shaanxi Restaurant Xian', pp='¥58'),
  MO('lct', 'lct-d3', 'Dinner — Green Tea Restaurant 绿茶餐厅 (Joy City)', 'Green Tea (Hangzhou, mild)', 'Hangzhou cooking, genuinely mild, in the mall by the pagoda.',
     "The Hangzhou chain, mild by default: 绿茶烤鸡 roast chicken, 石锅鸡汤豆腐 chicken-soup tofu, 面包诱惑 bread with ice cream, 绿茶饼 green-tea cakes. Avoid the 麻婆豆腐. The mall is a 10-minute walk from the pagoda's north square.",
     ('stroller', 'easy', 'indoor'), [], 'Mall hours, about 11:00–21:30', 'About ¥60–100 per person (listings differ)', '雁塔区慈恩路777号 曲江大悦城 L3-03',
     kids='Mild, familiar food; high chairs', elderly='Mall lift', book='Call 029-85720261. Large groups usually queue through the app; no dated review found, so confirm it is open.', watch='西安 绿茶餐厅 大悦城', en='Green Tea Restaurant Xian Joy City', pp='¥60–100'))
# --- Xi'an, Thu 17 Dec ---
MEAL('m-d4lunch', D[4], '12:45', '13:45', 'Thursday lunch', 'In Lintong, after the Terracotta Army:',
  MO('lty', 'lty-d4', 'Lunch — Lintong Yinxiang Shaanxi home cooking 临潼印象', 'Lintong Yinxiang (Shaanxi)', 'Local favourite in Lintong town: rooms, high chairs, about ¥50–70.',
     "A well-rated local Shaanxi restaurant in Lintong town, 12–15 min by van from the Terracotta Army and about 5 min from Huaqing Palace. Mild picks: 印象葫芦鸡 gourd chicken, 糖醋里脊 sweet-and-sour pork, 姥姥的油饼 grandma's fried bread, 西红柿泡馍 tomato paomo, 蒜蓉西兰花 garlic broccoli, 醪糟煮甑糕 sweet rice cake. Some dishes are spicy, so order around them.",
     ('easy', 'indoor', 'book'), ['img/g/food-tangcu-1.jpg'], '11:00–21:00', 'About ¥40–53 listed; groups say ¥50–70', '临潼区骊山街道秦陵南路35号 2F',
     kids='Order the mild dishes; high chairs', elderly='2nd floor: ask about stairs', book='Busy at mealtimes: book a private room on 029-83819988.', watch='临潼印象 特色陕菜', en='Lintong Yinxiang restaurant', pp='¥50–70'),
  MO('ysy', 'ysy-d4', 'Lunch — Yunshuiyao Yunnan mushroom hot pot 云水肴 (Lintong)', 'Yunshuiyao (mushroom hot pot)', 'Yunnan mushroom hot pot: the broth is mild, the chilli is a side dip.',
     "Yunnan mushroom hot pot in Lintong: 菌汤锅底 a mushroom broth that is not spicy, 过桥米线 crossing-the-bridge noodles, 烤包浆豆腐 grilled tofu, 野生菌拼盘 mushroom platter. The chilli comes as a dipping sauce, so the pot itself stays mild. Warm after the cold pits.",
     ('easy', 'indoor', 'book'), ['img/g/food-mushroomhotpot-1.jpg', 'img/g/food-crossbridge-1.jpg'], '10:00–22:00 (listings differ; confirm)', 'About ¥68 per person', '临潼区桃园路2号 骊景天下 1F',
     kids='Mild broth; noodles', elderly='Warm and soft food', book='Private rooms are listed: call 029-83999908.' + CONFIRM, watch='临潼 云水肴 云南菜', en='Yunshuiyao Yunnan Restaurant Lintong', pp='¥68', brand='云水肴'),
  MO('hg', 'hg-d4', 'Lunch — Hougong garden restaurant 后宫园林餐厅 (Lintong)', 'Hougong garden (home cooking)', 'Guanzhong farmhouse cooking in a garden, about 10 min from the pits.',
     "A garden restaurant on 秦唐大道, about 10 min from either site, cooking Guanzhong country food: 特色一锅炖 a one-pot stew, 农家焖土鸡 and 天麻炖土鸡 chicken stews, 核桃饼 walnut cakes. Mostly mild — avoid 油泼辣子蒜瓣鱼. Private rooms are mentioned in listings.",
     ('easy', 'indoor', 'book'), [], 'Confirm hours when booking', 'About ¥67 per person', '临潼区秦唐大道中',
     kids='Stews and chicken; mild', elderly='Garden setting, quiet', book='Call 029-83435678 (number unconfirmed) and ask for a room for 10.', watch='临潼 后宫园林餐厅', en='Hougong Garden Restaurant Lintong', pp='¥67', brand='后宫园林'))
MEAL('m-d4din', D[4], '18:30', '20:00', 'Thursday dinner', 'Back in the city, near the Bell Tower. ✨ The De Fa Chang dumpling banquet is the special one:',
  MO('dfc', 'dinner-defachang', 'Dinner — De Fa Chang dumpling banquet 德发长饺子宴', 'De Fa Chang dumpling banquet', 'A banquet of dumplings in many shapes. Soft, not spicy. 30+ private rooms.',
     "A long-established restaurant by the Bell Tower serving a banquet of dumplings in many shapes and fillings. Soft, not spicy, fun for kids and grandparents alike. Over 30 private rooms.",
     ('indoor', 'easy', 'book'), 'dumplings', '10:30–21:00', 'Dumpling banquets ¥138 / ¥188 / ¥268 per person; about ¥70 à la carte', '莲湖区西大街3号, by the Bell Tower',
     kids='Dumplings in animal shapes; nothing spicy', elderly='Private room', book='Book a room and a set banquet a few days ahead.', watch='西安 德发长 钟楼', pp='¥70–138+', special=True),
  MO('kyd', 'kyd-d4', "Dinner — Xi'an Roast Duck 西安烤鸭店 (Yisu quarter)", "Xi'an Roast Duck", 'The old state-run roast duck house, 5 min from the Bell Tower. Mild.',
     "A long-running Xi'an roast duck house in the Yisu theatre quarter, 5 min walk from the Bell Tower: 酥不腻烤鸭 crisp roast duck with pancakes, 鸭汤 duck soup, 桂花糕 osmanthus cake, plus Shaanxi dishes. Mild. Two floors, banquet style.",
     ('easy', 'indoor', 'book'), ['img/g/food-roastduck-1.jpg', 'img/g/food-roastduck-2.jpg'], 'Confirm hours when booking', 'About ¥72 per person', '碑林区案板街26号 易俗社文化街区 2–3F',
     kids='Duck pancakes are easy for kids', elderly='Lift to the upper floors', book='Call 029-86398999 and ask for a room for 10 (branch not confirmed).', watch='西安烤鸭店 易俗社', en="Xi'an Roast Duck Restaurant Yisu", pp='¥72'),
  MO('tsx', 'tsx-d4', 'Dinner — Tong Sheng Xiang paomo 同盛祥 (Bell Tower)', 'Tong Sheng Xiang (paomo, halal)', "Xi'an's classic bread-in-soup. Kids enjoy breaking the bread. Halal.",
     "Xi'an's classic 泡馍: you break flatbread into small pieces and it comes back in rich beef or lamb soup (kids like the breaking). Also 酱牛肉 braised beef and 蜂蜜凉粽 honey rice cake. Halal, so no pork. Next door to De Fa Chang.",
     ('easy', 'indoor', 'book'), ['img/paomo.jpg', 'img/g/paomo-1.jpg'], '10:30–21:00', 'About ¥35–50 per person', '莲湖区西大街5号, by the Bell Tower',
     kids='Mild; ask for 凉皮 without chilli', elderly='Rooms are on the 2nd floor (ground floor is a snack hall)', book='Book the 2nd-floor restaurant: 029-87218711.', watch='西安 同盛祥 钟楼店', pp='¥35–50'),
  MO('dy', 'dy-d4', 'Dinner — Dongya Shanghai restaurant 东亚饭店 (Bell Tower)', 'Dongya (Shanghainese, mild)', 'Shanghai cooking, mild and slightly sweet, 3 min from the Bell Tower.',
     "A Shanghai restaurant three minutes from the Bell Tower, mild and slightly sweet: 狮子头 lion's-head meatballs, 蟹粉豆腐 crab-roe tofu, 腌笃鲜 pork and bamboo soup, 南翔小笼 soup dumplings and 生煎 pan-fried buns. Private rooms and baby chairs are listed.",
     ('easy', 'indoor', 'book'), ['img/g/food-xiaolongbao-1.jpg', 'img/g/food-lionshead-1.jpg'], '11:00–21:00', 'About ¥110 per person: the priciest here', '莲湖区西大街3号 (by the Bell Tower)',
     kids='Soup dumplings; nothing spicy', elderly='Private room', book='Book a private room: 029-87346688.', watch='西安 东亚饭店 钟楼', en='Dongya Restaurant Xian', pp='¥110'))
# --- Xi'an, Fri 18 Dec ---
MEAL('m-d5lunch', D[5], '12:00', '13:30', 'Friday lunch', 'After the museum, before the City Wall:',
  MO('zxz', 'zxz-d5', "Lunch — Zhaixiangzi Shaanxi 窄巷子陕菜馆 (Big Wild Goose Pagoda)", 'Zhaixiangzi (Shaanxi, mild)', 'Shaanxi cooking described as not spicy and not oily. About ¥60.',
     "A Shaanxi restaurant 5 min by van from the museum, described in reviews as 不辣不油 (not spicy, not oily) and good for kids and grandparents: 葫芦鸡 gourd chicken, 山楂鲜山药 hawthorn and yam, and the usual Shaanxi staples.",
     ('easy', 'indoor', 'book'), ['img/g/food-guotie-1.jpg'], '11:00–14:30, 17:00–21:30', 'About ¥60 per person', '雁塔区雁塔西路6号',
     kids='Mild dishes', elderly='Ground floor', book='Call 029-85225738 / 17316625827.' + CONFIRM, watch='西安 窄巷子陕菜馆 大雁塔', en='Zhaixiangzi Shaanxi Restaurant Xian', pp='¥60'),
  MO('xb', 'xb-d5', 'Lunch — Xibei oat noodle village 西贝莜面村 (SEG)', 'Xibei (northwest, family chain)', 'The northwest chain built for families: bibs, colouring, mostly mild.',
     "The well-known northwest chain in SEG mall, 700 m from the museum: 莜面 oat noodles, 蒙古牛大骨 beef bones, 黄米凉糕 millet cake, 草原酸奶 yoghurt. Mostly mild — avoid 辣皮子牛肉. Set up for families, with bibs and colouring paper for the kids.",
     ('stroller', 'easy', 'indoor'), ['img/g/food-youmian-2.jpg', 'img/g/food-youmian-1.jpg'], '10:30–21:00', 'About ¥65 per person', '雁塔区长安中路123号 赛格国际购物中心 7F',
     kids='Made for kids', elderly='Mall lift', book='Queue-number system; ask them to join tables. Xibei closed some branches from Oct 2025, so confirm this one is open.', watch='西安 西贝莜面村 赛格', en='Xibei Youmian Village SEG Xian', pp='¥65'),
  MO('dfx', 'dfx-d5', 'Lunch — Defaxing HK café 德发兴茶冰厅 (South Gate)', 'Defaxing HK café (by the City Wall)', 'Hong Kong café food right by the South Gate, so no rush for the wall. About ¥50.',
     "A Hong Kong-style café right by the South Gate, about 15 min by van from the museum and a short walk to the 14:00 City Wall: 烧腊三件套 roast meat platter, 干炒牛河 beef ho fun, 冰火菠萝油 pineapple bun with butter, 虾球捞面 prawn noodles. Nothing spicy.",
     ('stroller', 'easy', 'indoor'), ['img/g/food-beefhofun-2.jpg', 'img/g/food-pineapplebun-1.jpg'], 'Confirm hours when booking', 'About ¥50 per person', '碑林区环城南路东段334号, by the South Gate 永宁门',
     kids='Familiar Cantonese food', elderly='Mall lift', book='Call ahead and confirm a table for 10.', watch='西安 德发兴茶冰厅 南门店', en='Defaxing Cha Bing Teng South Gate Xian', pp='¥50'))
# --- Chengdu, Sat 19 Dec ---
MEAL('m-d6din', D[6], '19:30', '21:00', 'Saturday dinner', 'Back in Chengdu after the train:',
  MO('walk', 'night-d6', 'Dinner & Chunxi Road by night 春熙路', 'Chunxi Road snack walk', 'Christmas lights and street snacks, no booking. Mostly mild.',
     'Walk to the shopping streets for Christmas lights and street snacks: 钟水饺 Zhong dumplings, 糖油果子 sugar-fried dough balls, 冰粉 ice jelly.',
     ('stroller', 'easy'), 'chunxi', 'Evening', 'Pay as you go', 'Chunxi Road: walkable from the JW / Ritz area, 25–35 min by car from the W', cat='Night', pp='¥30–50', brand='春熙路'),
  MO('tdc', 'tdc-d6', 'Dinner — Tao De claypot 陶德砂锅 (Chunxi Road)', 'Tao De claypot (mild)', 'Good-value claypot cooking, mild to medium, opposite Wangfujing.',
     "A well-reviewed Suining claypot restaurant on 总府路, opposite Wangfujing: 蒜蓉虾 garlic prawns, 野山菌鸡汤 wild mushroom chicken soup, 砂锅丸子 meatball claypot, 番茄炒蛋 tomato and egg, 红糖糍粑 brown-sugar rice cakes. Mild to medium; a 2025 reviewer's son who can't eat chilli ate well. Floors 2–5.",
     ('easy', 'indoor', 'book'), [], '10:00–22:30', 'About ¥56–63 per person', '锦江区总府路8号 鸿德春熙中心 2F, opposite 王府井',
     kids='Mild claypots; high chairs', elderly='Upstairs: ask for the lift', book='Book or pre-queue by phone: 028-85096669.' + CONFIRM, watch='成都 陶德砂锅 春熙路店', en='Tao De Claypot Chunxi Road', pp='¥60'),
  MO('zt', 'zt-d6', 'Dinner — Zhang Taipo trotter soup 张太婆老妈蹄花 (Taikoo Li)', 'Zhang Taipo trotter soup', 'Milky pig-trotter soup, mild and very cheap. Open late.',
     "Chengdu's late-night comfort food, 8 min walk from Taikoo Li: pork trotters stewed white with butter beans, mild unless you use the dip. Cheap and quick after the train. A small local place — skip the stir-fries, which are spicy.",
     ('easy', 'indoor'), [], '11:00–06:00', 'About ¥40 per person', '锦江区耿家巷46号 / 红石柱横街27号 (basement of the Xinwanli hotel)',
     kids='Soft and mild', elderly='Simple, warm food', book='Small place: 10 people should call ahead or go early.', watch='成都 张太婆老妈蹄花 太古里', en='Zhang Taipo Pig Trotter Soup Chengdu', pp='¥40'),
  MO('xlk', 'xlk-d6', 'Dinner — Xiaolongkan hot pot 小龙坎 (Chunxi Road)', 'Xiaolongkan hot pot, split pot', 'For the chilli fans: Chengdu hot pot with a clear side. Open late.',
     "One of Chengdu's big hot pot names. Order a 鸳鸯锅 split pot so the kids and elderly eat from the clear side: 虾滑 shrimp paste, 牛肉 beef, 红糖糍粑 brown-sugar rice cakes to finish. Open until 2am.",
     ('spicy', 'indoor'), ['img/g/hotpot-1.jpg', 'img/hotpot.jpg'], '11:00–02:00', 'About ¥90–100 per person', '锦江区下东大街36号 郁金香广场 2F',
     kids='Keep them on the clear side', elderly='2nd floor; ask for the lift', watch='成都 小龙坎 春熙店', pp='¥90–100'))
# --- Chengdu / Leshan, Sun 20 Dec ---
MEAL('m-d7lunch', D[7], '12:45', '13:45', 'Sunday lunch (Leshan day only)', 'If the family picks Leshan: lunch between the boat and the 15:00 train. Leshan beef soup is mild:',
  MO('fsn', 'fsn-d7', 'Lunch — Feng Si Niang Leshan beef soup 冯四孃跷脚牛肉', 'Feng Si Niang beef soup', "Leshan's famous clear beef soup, chilli dip on the side. Top-rated.",
     "Leshan's signature 跷脚牛肉: beef simmered in a clear herbal broth, with the chilli dip on the side, so it is mild unless you dip. Also 甜皮鸭 sweet-skin duck and 红糖饼 brown-sugar cakes. Banquet hall; top-rated on Ctrip.",
     ('easy', 'indoor'), ['img/g/food-qiaojiao-1.jpg'], '10:00–21:00', 'About ¥45 per person', '乐山市中区嘉兴路289–293号',
     kids='Clear soup; keep the chilli dip away', elderly='Soft beef in soup', watch='乐山 冯四孃跷脚牛肉 嘉兴路', mapcity='Leshan', pp='¥45'),
  MO('xlw', 'xlw-d7', 'Lunch — Xie Lao Wu Leshan beef soup 谢老五跷脚牛肉', 'Xie Lao Wu beef soup', 'The old classic on the Zhanggongqiao food street.',
     "The classic 跷脚牛肉 house on the 张公桥 food street: clear beef soup, 蒸肥肠 steamed pork intestine, 鲜烧牛杂 beef offal. Mild, except the 血旺 blood tofu, which is spicy.",
     ('easy', 'indoor'), ['img/g/food-qiaojiao-2.jpg'], 'Confirm hours before going', 'About ¥35–45 per person', '乐山市中区演武街3号 1F (张公桥大市场)',
     kids='Clear soup; skip the 血旺', elderly='Rooms are upstairs (stairs); tables downstairs', watch='乐山 谢老五跷脚牛肉 总店', mapcity='Leshan', pp='¥35–45'),
  MO('cb', 'cb-d7', 'Lunch — Chuanben beef soup 川犇跷脚牛肉 (by Leshan station)', 'Chuanben (next to the station)', 'Right by Leshan station, so no rush for the 15:00 train. About ¥38.',
     "A 跷脚牛肉 house right next to Leshan high-speed rail station, which takes the rush out of the 15:00 train: 跷脚牛肉小锅 a small pot of clear beef soup, 牛骨汤 beef-bone soup, 红糖饼 brown-sugar cakes. The 临江鳝丝 eel is spicy. Only a handful of reviews, so it is the least-known of the three.",
     ('easy', 'indoor'), [], '10:00–22:00', 'About ¥38 per person', '乐山市中区瑞祥路一段1111号, by the high-speed rail station',
     kids='Mild clear soup', elderly='No extra drive before the train', book='Call 15983366067.' + CONFIRM, watch='乐山 川犇跷脚牛肉 高铁站', en='Chuanben Qiaojiao Beef Leshan', mapcity='Leshan', pp='¥38'),
  MO('gsx', 'gsx-d7', 'Lunch — Gushixiang beef soup 古市香跷脚牛肉 (Suji old town)', 'Gushixiang (old-town house)', 'The heritage house in Suji old town, 25 min west. Four floors with rooms.',
     "The best-known 跷脚牛肉 house, in 苏稽 old town about 25 min west of the Buddha: a four-storey wooden building with a main hall and private rooms, serving 4,000–5,000 people a day at holidays. The broth is clear and peppery, with the chilli as a side dip; 粉蒸牛肉 steamed beef usually comes with chilli. Also 甜皮鸭, 红糖饼, 冰粉.",
     ('easy', 'indoor', 'book'), ['img/g/food-qiaojiao-3.jpg'], '10:00–20:30', 'About ¥60–67 per person', '乐山市市中区苏稽镇桂花路85–89号',
     kids='Clear soup; the broth is peppery', elderly='Wooden building: ask about stairs', book='Call 0833-2565466. It is the wrong way from the station, so keep the van.', watch='乐山 古市香跷脚牛肉 苏稽', en='Gushixiang Qiaojiao Beef Suji', mapcity='Leshan', pp='¥60–67'))
decisions[-1]['onlyIf'] = 'd-d7:leshan'   # the page shows this vote on Sunday only while Leshan is locked in or leading
MEAL('m-d7din', D[7], '19:00', '20:30', 'Sunday dinner', 'After the big day out. These are all near the W (the second Chengdu stay is leaning that way):',
  MO('dd', 'dd-d7', 'Dinner — Diandang Chaoshan beef hot pot 掂档 (Yofun mall, by the W)', 'Chaoshan beef hot pot (by the W)', "Clear-broth beef hot pot a few minutes' walk from the W. Not spicy.",
     "Chaoshan clear-broth beef hot pot in the 悠方 mall next to the W, a few minutes' walk: 吊龙 beef, 手打牛肉丸 hand-beaten beef balls, 潮汕炸腐竹 fried tofu skin. Nothing spicy unless you add the dip.",
     ('easy', 'indoor', 'book'), ['img/g/food-beefhotpot-2.jpg', 'img/g/food-beefhotpot-1.jpg'], '10:00–22:00', 'About ¥105–111 per person', '高新区交子大道 悠方购物中心 5F L506',
     kids='Clear broth; beef balls', elderly='Walk from the W; mall lift', book='Call 028-65188139 to book and confirm a table for 10.', watch='成都 掂档潮汕牛肉火锅 悠方', en='Diandang Chaoshan Beef Hot Pot Yofun', pp='¥105'),
  MO('hqy', 'hqy-d7', 'Dinner — Huajian Qingyan Huaiyang 花间青宴 (Yofun mall)', 'Huajian Qingyan (Huaiyang, mild)', 'Gentle Jiangsu cooking in the same mall as the W. Not spicy.',
     "Huaiyang (Jiangsu) cooking in the 悠方 mall beside the W, so there is no drive at all: 招牌狮子头 lion's-head meatballs, 乾隆九丝汤 shredded soup, 功夫松鼠鱼 sweet-and-sour fish. Nothing spicy. (Skip the 花雕醉熟虾 for the kids: cooked prawns steeped in wine.) A Dec 2025 diner post recommends it for family dinners.",
     ('easy', 'indoor', 'book'), ['img/g/food-lionshead-1.jpg', 'img/g/food-lionshead-2.jpg'], 'Confirm hours when booking', 'Not published; a smart mall restaurant, so probably ¥100+', '高新区交子大道 悠方购物中心 (by the W)',
     kids='Meatballs and sweet fish', elderly='No drive from the hotel', book='Book through 大众点评 or ask the W concierge.' + CONFIRM, watch='成都 花间青宴 悠方', en='Huajian Qingyan Huaiyang Chengdu', pp='¥100+'),
  MO('yzyw', 'yzyw-d7', 'Dinner — Yizuoyiwang Yunnan 一坐一忘 (Chengdu SKP)', 'Yizuoyiwang (Yunnan)', 'Yunnan cooking in SKP, mostly mild. Round tables in the hall.',
     "The well-known Yunnan restaurant in Chengdu SKP: 铜锅牛肝菌焖饭 mushroom rice in a copper pot, 香茅草烤鲈鱼 lemongrass grilled fish, 薄荷牛肉卷 mint beef rolls, 腾冲小锅米线 rice noodles. Mostly mild — a few dishes use chilli, so ask when ordering.",
     ('easy', 'indoor', 'book'), ['img/g/food-crossbridge-1.jpg', 'img/g/food-crossbridge-2.jpg'], '11:00–21:30', 'Not published in Chengdu; the Beijing branch is about ¥149, so it may be over ¥100', '高新区天府大道北段2001号 成都SKP 美食大道 E2006',
     kids='Mild rice and noodles', elderly='Mall lift; round tables in the hall', book='Call 028-60831355 / 60831366.' + CONFIRM, watch='成都 一坐一忘 SKP', en='Yizuoyiwang Yunnan Restaurant Chengdu SKP', pp='¥100+'),
  MO('dhj', 'dhj-d7', 'Dinner — Dinghaiji Cantonese 丁海记粤式大排档 (Gaoxin)', 'Dinghaiji (Cantonese)', 'Cantonese roast meats and congee north of the W. Not spicy.',
     "A Cantonese 大排档 about 10–15 min north of the W: 烧鹅 roast goose, 蜜汁叉烧 honey pork, 砂锅粥 claypot congee, 啫啫芥兰 sizzling greens. Nothing spicy, and easy for a tired evening.",
     ('easy', 'indoor', 'book'), ['img/g/food-roastgoose-2.jpg', 'img/g/food-charsiubao-1.jpg'], 'Confirm hours when booking', 'Not published; 大排档 prices, so likely ¥60–100', '高新区天府大道北段28号 茂业中心A座 1F',
     kids='Roast meats and congee', elderly='Simple, warm food', book='Book through 大众点评.' + CONFIRM + ' Evidence for this branch is thin.', watch='成都 丁海记 粤式大排档 高新', en='Dinghaiji Cantonese Chengdu', pp='¥60–100'))
# --- Chengdu, Mon 21 Dec ---
MEAL('m-d8lunch', D[8], '12:45', '13:45', 'Monday lunch', 'Last lunch in Chengdu, near Chunxi Road and IFS:',
  MO('lus', 'lus-d8', 'Lunch — Lusi Hong Kong café 露斯港式茶餐厅 (Chunxi)', 'Lusi HK café', 'Hong Kong café classics near Chunxi Road. Not spicy, about ¥63.',
     "A Hong Kong cha chaan teng 8–10 min walk from Chunxi Road: 冰火菠萝油 pineapple bun with butter, 咖喱牛腩 curry beef brisket, 烧鹅 roast goose, 云吞面 wonton noodles. Nothing spicy, and a short walk from IFS.",
     ('easy', 'indoor'), ['img/g/food-pineapplebun-1.jpg', 'img/g/food-beefhofun-1.jpg'], 'Confirm hours when booking', 'About ¥63 per person', '锦江区红星路二段 (listings give 12号 or 2号附8号)',
     kids='Familiar food, quick', elderly='Short walk', book='Call 028-86758085 and ask them to join tables for 10.', watch='成都 露斯港式茶餐厅 春熙', en='Lusi Hong Kong Cafe Chengdu', pp='¥63'),
  MO('trsj', 'trsj-d8', 'Lunch — Tongren Siji coconut chicken 同仁四季椰子鸡 (IFS)', 'Coconut chicken hot pot (IFS)', 'Hainan coconut-chicken hot pot in IFS: clear, sweet broth, no chilli.',
     "Coconut-chicken hot pot in IFS, three minutes from the shopping: chicken poached in coconut water, then noodles and vegetables in the sweet broth. Nothing spicy at all, and the broth is a favourite with kids. The dipping sauce is where any heat lives.",
     ('stroller', 'easy', 'indoor', 'book'), ['img/g/food-coconutchicken-1.jpg'], 'Mall hours', 'Not published for this branch; the brand is usually ¥100+', '锦江区红星路三段1号 成都IFS L7',
     kids='Sweet, mild broth', elderly='Light and warm', book='Book through 大众点评.' + CONFIRM + ' Price and hours for this branch are unconfirmed.', watch='成都 同仁四季椰子鸡 IFS', en='Tongren Siji Coconut Chicken Chengdu IFS', pp='¥100+'),
  MO('fqfp', 'fqfp-d8', 'Lunch — Fuqi Feipian 夫妻肺片 (old shop)', 'Fuqi Feipian (spicy classic)', "Chengdu's most famous cold beef dish, in its own old shop. Spicy.",
     "The old shop of Chengdu's most famous dish: 夫妻肺片, sliced beef and offal in chilli oil. Spicy by nature, but there are mild things to order: 樟茶鸭 tea-smoked duck, 蛋烘糕 egg pancakes, 糍粑 rice cakes and clear-broth wontons. It ran 10-person banquet menus at Chinese New Year 2025, so a group fits.",
     ('indoor', 'spicy', 'book'), [], 'Confirm hours when booking', 'About ¥51 per person', '锦江区总府路23号 1–2F, near 王府井',
     kids='Order the mild dishes; the famous one is chilli', elderly='Two floors: ask for the lift', book='Call 028-86617171 and ask for a table for 10.', watch='成都 夫妻肺片 总府路', en='Fuqi Feipian Chengdu', pp='¥51'),
  MO('sqy', 'sqy-d8', 'Lunch — Sanqueyi Chengdu home cooking 三缺一 (Chunxi Road)', 'Sanqueyi (Sichuan, private room)', 'Everyday Sichuan with a private room for 10. Ask for 不辣.',
     "Everyday Chengdu home-style Sichuan with private rooms, near Chunxi Road. Most dishes come in large or small portions, so 10 people can try a lot. Spicy by default: ask for 不辣 for the kids and elderly.",
     ('indoor', 'spicy', 'book'), ['img/g/sichuandishes-2.jpg', 'img/g/food-huiguorou-2.jpg'], '11:00–21:00', 'About ¥100 per person', '锦江区纯阳观街1-41号 1–2F',
     kids='High chairs; ask for 不辣', elderly='Wheelchair access', book='Book a private room for 10.', watch='成都 三缺一 春熙路店', pp='¥100'))
MEAL('m-d8din', D[8], '18:00', '19:45', 'Farewell dinner', 'Last dinner, before the 21:15 check-out and 21:30 airport vans. ✨ Rongle Garden (old centre) is the special one. The other two are in Huayang, about 25 min from the W or 40+ min from a central hotel — or take the bags and go to the airport straight from dinner:',
  MO('rongle', 'dinner-farewell', 'Farewell dinner — Rongle Garden banquet 荣乐园', 'Rongle Garden banquet (mild Sichuan)', 'A proper Sichuan banquet in the mild old style. Pre-order the showpieces.',
     "A proper Sichuan banquet to finish, in the mild old Chengdu (荣派) style: pre-order 开水白菜 cabbage in clear broth and 樟茶鸭 tea-smoked duck, plus 咸烧白 steamed pork belly and 圆子汤 meatball soup. Keep it early; the airport run starts at 21:30.",
     ('indoor', 'easy', 'book'), ['img/g/food-kaishui-2.jpg'], 'Confirm hours when booking', 'About ¥120 per person, more with the banquet dishes', '青羊区文殊院街27号, near Wenshu Monastery',
     kids='Mild dishes', elderly='Older building: ask about stairs to the rooms', book='Book a private room and pre-order 开水白菜 a few days ahead.', watch='成都 荣乐园 文殊院', en='Rongle Garden', pp='¥120–150', special=True),
  MO('dry', 'dry-d8', 'Farewell dinner — Zhuojin new Sichuan banquet 卓锦新川菜 (Huafu)', 'Zhuojin banquet (Huayang)', 'Big banquet restaurant south of the city in Huayang. Set menus for a table of 10.',
     "A large new-Sichuan banquet restaurant in 华阳, south of the city: about 25 min from the W, 40+ min from a central hotel. Ask for a set menu with the spicy dishes left out. Banquet-style rooms; set menus were listed at ¥999–1,588 per table of 10.",
     ('easy', 'indoor', 'book'), [], 'Confirm hours when booking', 'About ¥100–160 per person as a table set menu', '双流区天府大道南段182号 (华府店)',
     kids='Ask for a non-spicy set menu', elderly='Banquet room, no stairs', book='Call 13880802852 (number from an older listing; confirm) and ask for a room for 10 and a mild set menu.', watch='成都 卓锦新川菜 华府店', en='Zhuojin Xin Chuancai Huafu Chengdu', pp='¥100–160', brand='卓锦新川菜'),
  MO('dyl', 'dyl-d8', 'Farewell dinner — Da Ya Li roast duck 大鸭梨烤鸭 (Yuanda mall)', 'Da Ya Li roast duck', 'Beijing roast duck with a banquet hall and high chairs. About ¥104.',
     "Beijing-style roast duck in the 远大购物中心 in 华阳, on the airport side of town: 香酥烤鸭 crisp roast duck with pancakes, 生炒牛肉丝 beef, 素蟹黄豆腐 tofu. Mild, though the menu also has spicy Sichuan dishes to order around. A banquet hall and high chairs are listed.",
     ('easy', 'indoor', 'book'), ['img/g/food-roastduck-2.jpg', 'img/g/food-roastduck-1.jpg'], '11:00–14:00, 17:00–21:00', 'About ¥104 per person', '天府新区天府大道南段 远大购物中心A馆 7F',
     kids='Duck pancakes; high chairs', elderly='Banquet hall, mall lift', book='Book through 大众点评.' + CONFIRM, watch='成都 大鸭梨烤鸭 远大', en='Da Ya Li Roast Duck Chengdu', pp='¥104'))

# ---------- ideas: not on a day; heart the ones you want ----------
I('emei', '', 'Only Emei Mountain theatre city 只有峨眉山', 'Chengdu', 'Show', info="Wang Chaoge's giant immersive theatre village at the foot of Mount Emei (the 'Only' series). Main show 19:30–21:00 (from ¥258). About 2h from Chengdu, so it means a late night or a night in Emei; pairs with the Leshan day trip.", fam=('book',), pic=[])
I('menghui', D[4], "Dream Back to the Tang 梦回大唐", "Xi'an", 'Show', '', '',
  "The indoor Tang court dance-and-music show at Tang Paradise (凤鸣九天剧院). The gentlest option on the list: seated, warm, about an hour, and the ticket includes entry to the park. ⚠ Sources disagree on the start — some say 17:00, most say 19:30 — so confirm the time before counting on an early finish. Qujiang, close to the Westin/W end of town — if this one wins we would move it off the Terracotta day to Wednesday or Friday, where it fits without an hour of driving.",
  ('indoor', 'easy', 'book'), opt='d-xashow:menghui', pic='tangparadise',
  book='¥298 balcony / ¥398 stalls / ¥518 VIP; child ¥158–268 for 1.2–1.5 m; under 1.2 m free without a seat. Park entry is included, and is free anyway for over-65s.')
I('tangdream', '', "Tang Dynasty Dream Chasing 大唐追梦", "Xi'an", 'Show', info="⚠ NOT ON IN DECEMBER. The boat-borne light show on the lake at Tang Paradise runs April to October only — it is outdoors on open water in an unheated boat, so it closes for winter (confirmed four ways). Listed so nobody hunts for it. In season it is 50 min, ¥318–618, park entry included. The indoor 梦回大唐 is the winter stand-in.", fam=('cold', 'book'), pic='tangparadise')
I('xianincident', '', "The Xi'an Incident 12·12 西安事变", "Xi'an", 'Show', info="Immersive re-telling of the 1936 Xi'an Incident, indoors at 瑶光阁剧院 inside Huaqing Palace, Lintong — so it pairs with the Terracotta day. Runs all year (about 11:30 / 14:10 / 16:20, 60 min, ¥258, and the Huaqing Palace entry ticket is separate). ⚠ The audience STANDS for the whole first half while the actors move among them, and only sits for the second half — hard for the grandparents — and the gunfire and explosion effects are loud for a baby.", fam=('indoor', 'book'), pic=[])
I('mengchangan', '', "Dream of Chang'an 梦长安 大唐迎宾盛礼", "Xi'an", 'Show', info="The Tang welcome ceremony staged on the city wall at the South Gate. ⚠ NOT ON in December: the season runs early April to the end of October, Tuesday to Sunday evenings, because it is entirely outdoors on the wall. Listed here only so nobody spends time looking for it — it is ¥280–880, 70 min, if you ever come back in spring.", fam=('cold', 'book'), pic=[])
I('tianfu-idea', '', 'Tianfu Square & Chunxi Road 天府广场', 'Chengdu', 'Shop', info='The central square and main shopping street, walkable from the central Marriott hotels.', fam=('stroller', 'easy'), pic=['img/g/tianfu-1.jpg', 'img/g/tianfu-3.jpg', 'img/chunxi.jpg', 'img/g/chunxi-1.jpg'], key='tianfusquare')
I('jinsha', '', 'Jinsha Site Museum 金沙遗址博物馆', 'Chengdu', 'Sight', info='3,000-year-old Shu kingdom site, home of the golden Sun Bird. Indoor.', fam=('stroller', 'indoor'))
I('qingcheng', '', 'Mount Qingcheng 青城山', 'Chengdu', 'Sight', info='Misty Taoist mountain with a cable car. Many steps and slippery in winter; for fit adults.', fam=('stairs', 'cold'))
I('tangparadise', '', 'Tang Paradise 大唐芙蓉园', "Xi'an", 'Sight', info='A large Tang-style garden by Qujiang Pool, lit at night. Near the W and the Westin.', fam=('stroller', 'cold'))
I('paomo', '', 'Yangrou paomo 羊肉泡馍', "Xi'an", 'Food', info="Tear flatbread into lamb broth: Xi'an's soul food. 老孙家 Lao Sun Jia is the classic.", fam=('easy', 'indoor'))
I('biangbiang', '', 'Biangbiang noodles', "Xi'an", 'Food', info='Belt-wide hand-pulled noodles with chilli oil. Ask for less chilli for kids.', fam=('spicy',))
I('drumtower-in', '', 'Climb the Drum Tower 鼓楼', "Xi'an", 'Sight', info='Steep steps up for the drum performance and views over the Muslim Quarter.', fam=('stairs',), pic='drumtower', key='drumtower')

# ---------- hotels (Marriott Bonvoy) ----------
# Each hotel carousel shows the surrounding area, captioned with what's near.
HGAL = {
 'jw': [('taikooli', 'Taikoo Li shopping streets · short walk'), ('g/chunxi-1', 'Chunxi Road · short walk'), ('ifspanda', 'The IFS climbing panda · short walk'), ('g/tianfu-1', 'Tianfu Square · nearby'), ('g/taikooli-4', 'Daci Temple inside Taikoo Li')],
 'w': [('g/financial-1', "Chengdu Financial City · the hotel's district"), ('g/financialcity-3', 'Chengdu skyline'), ('kuanzhai', 'Old-town sights like Kuanzhai Alley · 25–35 min drive')],
 'ritz': [('g/tianfu-1', 'Tianfu Square · the hotel overlooks it'), ('g/tianfu-3', 'Tianfu Square towers'), ('peoplespark', "People's Park teahouse · short ride"), ('kuanzhai', 'Kuanzhai Alley · short ride')],
 'stregis': [('g/tianfu-2', 'Tianfu Square area · nearby'), ('chunxi', 'Chunxi Road · short ride'), ('g/wenshu-1', 'Wenshu Monastery · short ride')],
 'wxian': [('g/qujiangpool-1', 'Qujiang Pool park · by the hotel'), ('tangparadise', 'Tang Paradise · nearby'), ('g/tangparadise-1', 'Tang Paradise lakeside'), ('wildgoose', 'Big Wild Goose Pagoda · short drive'), ('datang', 'Great Tang All Day Mall · short drive')],
 'westin': [('wildgoose', 'Big Wild Goose Pagoda · next door'), ('g/wildgoose-4', 'The pagoda at night'), ('datang', 'Great Tang All Day Mall · walk (lit up after dark)'), ('g/datang-2', 'Tang sculptures along the night-walk street'), ('g/shaanximuseum-4', 'Shaanxi History Museum · short hop')],
 'jwxa': [('hsr', "Handy for Xi'an North high-speed rail station"), ('belltower', 'Old city (Bell Tower) · a drive away'), ('citywall', 'City Wall · a drive away')],
 'ritzxa': [('citywall', 'Old city wall · a drive away'), ('smallgoose', 'Small Wild Goose Pagoda · short drive'), ('g/shaanximuseum-4', 'Shaanxi History Museum · short drive')],
}
# The hotel's own photos come first (hotlinked from Marriott's image server, credited), then 2 of the neighbourhood.
HOTEL_PHOTOS = json.load(open(os.path.join(HERE, 'hotel_photos.json'), encoding='utf-8'))
def marriott(k):
    if k.startswith('R/'): return 'https://cache.marriott.com/content/dam/marriott-renditions/' + k[2:] + '-hor-wide.jpg?output-quality=70&interpolation=progressive-bilinear&downsize=800px:*'
    return 'https://cache.marriott.com/is/image/marriotts7prod/' + k[2:] + ':Wide-Hor?wid=800&fit=constrain'
def hgal(hid):
    out = [{'src': marriott(k), 'cap': cap + ' · © Marriott'} for k, cap in HOTEL_PHOTOS[hid]]
    for k, cap in HGAL[hid][:2]:
        src = f'img/{k}.jpg'
        assert os.path.exists(os.path.join(HERE, '..', src)), src
        out.append({'src': src, 'cap': cap})
    return out
SHORT = {'jw': 'JW Marriott', 'w': 'W Chengdu', 'ritz': 'Ritz-Carlton', 'stregis': 'St. Regis', 'wxian': "W Xi'an", 'westin': 'Westin', 'jwxa': 'JW Marriott', 'ritzxa': 'Ritz-Carlton'}   # names that fit the nights bar
def H(id, name, cn, area, addr, pros, cons, url, pic, fits, up, upnote, opened, reno):
    return {'id': id, 'name': name, 'cn': cn, 'area': area, 'address': addr, 'pros': pros, 'cons': cons, 'url': url, 
            'img': img(pic), 'gallery': hgal(id), 'fits': fits, 'up': up, 'upnote': upnote, 'opened': opened, 'reno': reno,
            'short': SHORT.get(id, name)}
hotels = {
 'Chengdu': {'title': 'Chengdu · first stay', 'dec': 'h-chengdu', 'city': 'Chengdu', 'nights': 'Sun 13 → Wed 16 Dec (3 nights)', 'start': '2026-12-13', 'n': 3, 'short': 'Chengdu',
  'tip': "Book the first night from Sun 13 Dec and tell the hotel you'll arrive around 2am, so the rooms are held. The second stay (19–21 Dec) has its own vote below: pick the same hotel to leave the big bags with the concierge while you're in Xi'an, or try a second hotel.",
  'options': [
   H('jw', 'JW Marriott Hotel Chengdu', '成都茂业JW万豪酒店', 'Chunxi Road · Taikoo Li', '19 Dongyu Street 东御街19号',
     ['Guests with elite status report upgrades to executive suites', 'Executive lounge and breakfast for Platinum and Titanium', 'Walk to Chunxi Road, Taikoo Li and the IFS panda; Tianfu Square metro nearby'],
     ['About 10 years old by the trip, with no major renovation found', 'Busy shopping district, lively outside at night'],
     'https://www.marriott.com/en-us/hotels/ctumj-jw-marriott-hotel-chengdu/overview/', 'taikooli', 'Best for elites + location',
     4, 'TripAdvisor: Titanium and Ambassador guests upgraded to executive suites with a separate bedroom and two bathrooms. The lounge is included for Platinum and above.',
     'Oct 2016', 'no major renovation found'),
   H('w', 'W Chengdu', '成都W酒店', 'Financial City · Gaoxin (south)', '300 Jiaozi Avenue 交子大道300号',
     ['Newest in Chengdu (2020)', 'Reported to upgrade generously, often to a suite (panda-themed WOW / Fantastic suites)', 'South side: a shorter drive to Tianfu Airport'],
     ['No executive lounge: the elite perk is a lobby-bar happy hour', '25–35 min by car to the old-town sights', 'Nightlife vibe'],
     'https://www.marriott.com/en-us/hotels/ctuwh-w-chengdu/overview/', 'ifspanda', 'Newest + generous, far from sights',
     4, 'SMZDM (Platinum): "generous with upgrades, basically a suite when availability allows". Elites get a lobby-bar happy hour, with no lounge.',
     'Oct 2020', 'new'),
   H('ritz', 'The Ritz-Carlton, Chengdu', '成都富力丽思卡尔顿酒店', 'Tianfu Square · Qingyang', '269 Shuncheng Avenue 顺城大街269号',
     ['Beautiful suites and Club floors over Tianfu Square (55 suites)', "Short ride to People's Park, Kuanzhai and Chunxi Road"],
     ['Platinum members get no Club Lounge or free breakfast at Ritz-Carlton', 'Ritz-Carlton suite upgrades are hard even for Titanium', 'Opened 2013'],
     'https://www.ritzcarlton.com/en/hotels/cturz-the-ritz-carlton-chengdu/overview/', 'chengduhero', 'Luxury, weakest elite perks',
     2, 'Reviewers advise Platinum members to pick the JW or St. Regis, since the Ritz gives them no lounge or breakfast. Suites are possible for Titanium but not dependable.',
     'Oct 2013', 'refurbished 2017 (per Ctrip)'),
   H('stregis', 'The St. Regis Chengdu', '成都瑞吉酒店', 'Near Tianfu Square · Qingyang', '88 Taisheng Road South 太升南路88号',
     ['Spacious rooms and butler service', 'Close to Tianfu Square and Chunxi Road'],
     ['Titanium guests report being told suites are not part of free upgrades', 'Opened 2014, no renovation found', 'Usually the priciest'],
     'https://www.marriott.com/en-us/hotels/ctuxr-the-st-regis-chengdu/overview/', 'chunxi', 'Least likely to upgrade',
     1, 'TripAdvisor and FlyerTalk, backed up on Flyert (飞客): Titanium guests say the hotel told them suites are excluded from complimentary upgrades. One Ambassador did get a suite.',
     'Sep 2014', 'no renovation found'),
  ]},
 "Xi'an": {'dec': 'h-xian', 'city': "Xi'an", 'nights': 'Wed 16 → Sat 19 Dec (3 nights)', 'start': '2026-12-16', 'n': 3,
  'tip': "Stay in Qujiang, near the Big Wild Goose Pagoda and the night-walk street. The W and the Westin are both there, a short ride apart. Mid-December is low season in Xi'an, which helps the upgrade odds.",
  'options': [
   H('wxian', "W Xi'an", '西安W酒店', 'Qujiang Pool', '333 Qujiang Chi East Road 曲江池东路333号',
     ['Built 2018: much newer than the Westin', 'A Jan 2025 Flyert stay was upgraded to a 100+ m² suite by default (free minibar)', 'Very good breakfast; by Qujiang Pool park and Tang Paradise, a short ride to the pagoda'],
     ['Lively W vibe with a nightclub', 'Further from the old city wall and the Muslim Quarter'],
     'https://www.marriott.com/en-us/hotels/xiywh-w-xian/overview/', 'tangparadise', 'Newer + most generous',
     4, 'Flyert (Jan 2025): "suite upgrade by default, without asking or a suite certificate". TripAdvisor: a suite upgrade for a Marriott elite guest.',
     'Aug 2018', 'no renovation needed yet'),
   H('westin', "The Westin Xi'an", '西安威斯汀大酒店', 'Big Wild Goose Pagoda · Qujiang', "66 Ci'en Road 慈恩路66号",
     ['Walk to the Big Wild Goose Pagoda and the night-walk street', 'Platinum guests report suite upgrades; lounge with a strong afternoon tea and evening spread', 'Unusual museum hotel (Neri&Hu design)'],
     ['Oldest of the eight: opened 2012 with no renovation found; reviews say some rooms feel dated'],
     'https://www.marriott.com/en-us/hotels/xiywi-the-westin-xian/overview/', 'wildgoose', 'Best location, oldest rooms',
     4, 'Flyert, TripAdvisor and Trip.com (2025): Platinum guests upgraded to deluxe suites, and many Titanium guests to the executive floor. The lounge is included for Platinum and above.',
     'Mar 2012', 'no renovation found'),
   H('jwxa', "JW Marriott Hotel Xi'an", '西安海荣JW万豪酒店', 'Economic Development Zone (north)', '168 Fengcheng 8th Road 凤城八路168号',
     ['Newest of all (2023)', 'Executive lounge on a high floor', "The nearest of these to Xi'an North station"],
     ['Titanium upgrades reported as corner or executive rooms rather than suites', 'North of the old city: 30+ min to Qujiang sights'],
     'https://www.marriott.com/en-us/hotels/xiyjw-jw-marriott-hotel-xian/overview/', 'belltower', 'Newest, fewer suites, far',
     3, "Flyert: Titanium guests at the Xi'an JW Marriotts usually get panoramic corner or executive rooms, plus lounge access.",
     'Apr 2023', 'new'),
   H('ritzxa', "The Ritz-Carlton, Xi'an", '西安丽思卡尔顿酒店', 'Hi-tech Zone · Gaoxin', '50 Keji 2nd Road 科技二路50号',
     ['Opened 2019; big suites (150 m² on high floors)', 'Quiet business district'],
     ['A 2026 Titanium guest got no automatic upgrade, only one after asking', 'Platinum members get no Club Lounge or breakfast', '20–30 min by car to most sights'],
     'https://www.ritzcarlton.com/en/hotels/xiyrz-the-ritz-carlton-xian/overview/', 'xianhero', 'Least generous here',
     2, 'FlyerTalk (2026): a Titanium guest got no upgrade until asking. Ritz-Carlton gives Platinum members no lounge or breakfast.',
     'Jun 2019', 'no renovation needed yet'),
  ]},
}
elite = [
 "Book each room under a different Platinum/Titanium member's own Bonvoy account, with that person staying in the room. Upgrades, lounge access and breakfast go to the member in the room, so 5 rooms means 5 separate chances at a suite.",
 "Book direct on Marriott.com or the Bonvoy app. Most third-party bookings (Trip.com, Agoda) don't get elite benefits.",
 "Titanium members: put Suite Night Awards on the rooms that matter most (the grandparents' room and the room with the baby). They're confirmed a few days before arrival.",
 'About 1–2 weeks before, email the hotel: a multi-generational family of 10, all Titanium/Platinum, 5 rooms. Ask for connecting or adjacent rooms, suites if available, a cot, and how many people can use the lounge per room.',
 'Chengdu is one hotel with a 3-night + 2-night split: ask them to note the upgrade on both bookings, so you return to the same suite on 19 Dec.',
 "Check the breakfast and lounge rules for children when you book; hotels often cap it at the member plus one guest, and kids' rules vary.",
 'Since 2025 Marriott only promises "an upgrade", not a suite, and upgrades in China are now decided by an algorithm, so treat suites as likely, not guaranteed.',
]
# second Chengdu stay: same hotel list, its own vote (same hotel = bags stay; a different one = experience two hotels)
hotels['Chengdu (2nd stay)'] = dict(hotels['Chengdu'], title='Chengdu · second stay', city='Chengdu', dec='h-chengdu2', fallback='h-chengdu', nights='Sat 19 → Mon 21 Dec (2 nights + the evening)', start='2026-12-19', n=2,
    tip="Pick the same hotel as the first stay to keep it simple (the big bags wait with the concierge while you're in Xi'an), or pick a different one to experience two hotels.")
hotels = {"Chengdu": hotels['Chengdu'], "Xi'an": hotels["Xi'an"], 'Chengdu (2nd stay)': hotels['Chengdu (2nd stay)']}
for cityname, hid, q in (('Chengdu', 'h-chengdu', 'Where should we stay in Chengdu (first stay, 13–16 Dec)?'), ("Xi'an", 'h-xian', "Where should we stay in Xi'an?"), ('Chengdu', 'h-chengdu2', 'Chengdu second stay (19–21 Dec): same hotel, or try another?')):
    decisions.append({'id': hid, 'city': cityname, 'day': '', 'time': '', 'title': cityname + (' hotel, 2nd stay' if hid == 'h-chengdu2' else ' hotel'), 'question': q, 'kind': 'hotel',
      'options': [{'id': h['id'], 'name': h['name'], 'city': cityname, 'blurb': h['fits'], 'fam': [], 'img': h['gallery'][0]['src'], 'gallery': [g['src'] for g in h['gallery']], 'items': []} for h in hotels['Chengdu (2nd stay)' if hid == 'h-chengdu2' else cityname]['options']]})

# ---------- fixed blocks ----------
blocks = []
def B(id, day, type, title, time='', key=None, **kw):
    b = {'id': 'seed:' + id, 'day': day, 'type': type, 'title': title, 'time': time, 'sort': '', 'number': '', 'from': '', 'to': '', 'tentative': False, 'note': '', 'updatedAt': 0}
    b.update(kw); b['lat'], b['lng'] = at(key) if key else (None, None)
    b['mapq'] = {'land': '成都天府国际机场', 'tfu': '成都天府国际机场', 'g1': '成都东站', 'cdvan': '成都东站', 'x1': '西安北站', 'g2': '西安北站', 'x2': '西安北站', 'd2van': '成都大熊猫繁育研究基地'}.get(id, '')
    b['mapen'] = {'land': 'Chengdu Tianfu International Airport', 'tfu': 'Chengdu Tianfu International Airport', 'g1': 'Chengdu East Railway Station', 'cdvan': 'Chengdu East Railway Station', 'x1': "Xi'an North Railway Station", 'g2': "Xi'an North Railway Station", 'x2': "Xi'an North Railway Station", 'd2van': 'Chengdu Research Base of Giant Panda Breeding'}.get(id, '')
    if type == 'hotel': b['dec'] = 'h-xian' if id.startswith('h2') else ('h-chengdu2' if id.startswith('h3') else 'h-chengdu')
    blocks.append(b)
B('mh526', D[0], 'flight', 'Fly to Chengdu Tianfu', '19:00', number='MH526', **{'from': 'KUL', 'to': 'TFU'}, note='Business · lands about 00:05–00:15 Monday · confirm exact times on the e-ticket')
B('land', D[0], 'car', 'Land at Tianfu, immigration, vans to the hotel', '00:15', sort='24:15', key='tfu', tentative=True,
  note='+1 day · pre-book 2 × 7-seat vans (or a 12–14 seat minibus) for 10 people, luggage and pram · about 1h to the city centre')
B('h1in', D[0], 'hotel', 'Check in: {hotel}', '02:00', sort='26:00', tentative=True, note="book this room from Sun 13 Dec so it's held for a ~2am arrival (immigration + bags for 10 take time)")
B('d2van', D[2], 'car', 'Van to the Panda Base', '07:30', key='panda', note='about 30 min from the centre · be there at opening')
B('h1out', D[3], 'hotel', 'Check out of {hotel}', '08:30', note="if the family votes the same hotel for 19 Dec, leave the big bags with the concierge")
B('cdvan', D[3], 'car', 'Vans to Chengdu East station', '08:45', key='cdeast', note='30–35 min on a weekday morning · 10 people with a pram and bags need 45–60 min for real-name gates and security')
B('g1', D[3], 'train', "G-train G1574 Chengdu East → Xi'an North", '10:33', key='cdeast', tentative=True, **{'from': 'Chengdu East 成都东', 'to': "Xi'an North 西安北"},
  note='G1574 10:33 → 14:21 (or G3880 10:32) · daytime trains take 3h50–4h20, the 11:30 lands too late for the pagoda · not booked · tickets open Wed 2 Dec (15 days ahead, counting the travel day) · First or Business class for the grandparents · under-6s ride free without a seat')
B('x1', D[3], 'car', "Vans to the Xi'an hotel", '14:45', key='xianN', note='about 40 min to Qujiang (Westin/W), 40–50 min to the Ritz in Gaoxin')
B('h2in', D[3], 'hotel', 'Check in: {hotel}', '15:30', tentative=True, note='a real rest before the pagoda at 17:15')
B('d4van', D[4], 'car', 'Private van for the Terracotta day', '07:45', tentative=True, note='about 1h each way from Qujiang, 1h15–1h30 from the Ritz in Gaoxin · keep the van all day')
B('h2out', D[6], 'hotel', 'Check out of {hotel}', '12:00', note='pack before breakfast · vans leave 12:15 · Platinum/Titanium late check-out (to 16:00) lets bags and a nap wait in the room')
B('x2', D[6], 'car', "Vans to Xi'an North", '12:15', key='xianN', note='40–50 min from the Ritz · 10 people with a pram need 45–60 min for real-name gates and security; gates close 3 min before departure')
B('g2', D[6], 'train', "D-train D1939 Xi'an North → Chengdu East", '14:06', key='xianN', tentative=True, **{'from': "Xi'an North 西安北", 'to': 'Chengdu East 成都东'},
  note='D1939 14:06 → 17:48 (3h42) · there is no 14:00 train; next are G1975 14:33 and G1573 14:50 · tickets open Sat 5 Dec')
B('h3in', D[6], 'hotel', 'Check in: {hotel}', '18:45', note='second Chengdu stay (its own hotel vote)')
B('h3out', D[8], 'hotel', 'Check out of {hotel}', '21:15', note='keep the rooms till evening: late check-out, or book the night of 21 Dec')
B('tfu', D[8], 'car', 'Vans to Tianfu Airport', '21:30', key='tfu', note='about 1h–1h15 · aim for check-in by 22:45')
B('mh527', D[8], 'flight', 'Fly home to Kuala Lumpur', '01:05', sort='25:05', number='MH527', **{'from': 'TFU', 'to': 'KUL'},
  note='departs just after midnight, so technically Tue 22 Dec · lands about 06:10 · Business · confirm exact times on the e-ticket')

# ---------- before we go ----------
prep = [
 ['Now', 'Vote on hotels, then book each room direct under a different Platinum/Titanium member (tips in the Hotels tab). Ask for connecting rooms and a baby cot.'],
 ['Now', 'Passports valid 6+ months. Malaysians currently enter China visa-free for up to 30 days; re-check nearer the date.'],
 ['Now', 'Set up Alipay (and/or WeChat Pay) with a Malaysian card and get China eSIMs. Install 高德 Amap, Didi and Trip.com.'],
 ['Nov', "Whichever Xi'an show wins the vote, settle it now: 长恨歌 only announces a December season in November (assume no); 驼铃传奇 takes an annual maintenance break that fell on 2–20 Dec in 2024, so check its December dates; 复活的军团 is real-name with max 6 per order, so 10 people need two orders; 赳赳大秦 refuses under-5s and is real-name (passports)."],
 ['Tue 1 Dec', 'Panda Base tickets + shuttle bus for Tue 15 Dec (14 days ahead).'],
 ['Wed 2 Dec', "Train tickets to Xi'an for Wed 16 Dec (rail sales open 15 days ahead, counting the travel day)."],
 ['Sat 5 Dec', "Train back Xi'an → Chengdu for Sat 19 Dec."],
 ['Sun 6 Dec', 'Leshan trains, there and back, for Sun 20 Dec, if Leshan wins the vote.'],
 ['By 6 Dec', "Book vans: Tianfu Airport pickup ~00:15 Mon 14 Dec (10 people + luggage + pram); Wed 16 hotel → Chengdu East 08:45 and Xi'an North → hotel 14:45; the Terracotta day van Thu 17; Sat 19 hotel → Xi'an North 12:15 and Chengdu East → hotel 17:48; a spare van Wed evening for the grandparents and baby; the 21:30 airport run on Mon 21 Dec."],
 ['From 7 Dec', 'Book private rooms 包间 or big tables for the meal places the family picked (3–7 days ahead): 10 people including a baby; ask for a high chair and any minimum spend. Haidilao books in its app.'],
 ['Thu 10 Dec', 'Terracotta Army tickets for Thu 17 Dec (online only, 7 days ahead, passports).'],
 ['Sun 13 Dec', "Shaanxi History Museum tickets for Fri 18 Dec: released 17:00 China time on its WeChat, gone in seconds. Pre-enter every passport before (under-6s and over-65s need none). One person on the phone at KLIA. Sold out? 14 Dec 17:00 releases Sat 19 Dec. Plan B: Small Wild Goose Pagoda + Xi'an Museum (free)."],
 ['Pack', "Chengdu is about 5–12°C and damp; Xi'an about −3–8°C and dry. Thermals, gloves and beanies for everyone; a pram cover and baby carrier; tissues (many toilets have none); the grandparents' medicines in hand luggage."],
 ['Rain/snow', "Xi'an: Wednesday, stay in 曲江大悦城 mall; the Terracotta pits are roofed; Friday, swap the City Wall for Xi'an Museum / Small Wild Goose Pagoda."],
]
family = [['stroller', '👶', 'Stroller-friendly'], ['easy', '🧓', 'Easy walking'], ['stairs', '🪜', 'Lots of stairs'], ['cold', '🧣', 'Outdoors, dress warm'],
          ['indoor', '🏠', 'Indoor & warm'], ['book', '🎟', 'Book ahead'], ['spicy', '🌶', 'Spicy: ask for 微辣 / 不辣'], ['rest', '😴', 'Downtime']]
phrases = [['不辣 / 微辣', 'bù là / wēi là', 'Not spicy / mildly spicy'], ['鸳鸯锅', 'yuān yāng guō', 'Split hot pot with a clear side'], ['热水', 'rè shuǐ', 'Hot water (baby bottles)'],
           ['婴儿床', 'yīng ér chuáng', 'Baby cot'], ['电梯在哪里?', 'diàn tī zài nǎ lǐ', 'Where is the lift?'], ['轮椅', 'lún yǐ', 'Wheelchair'],
           ['洗手间在哪里?', 'xǐ shǒu jiān zài nǎ lǐ', 'Where is the toilet?'], ['包间', 'bāo jiān', 'Private dining room']]

used = {i['img'] for i in items} | {o['img'] for d in decisions for o in d['options']} | {h['img'] for c in hotels.values() for h in c['options']} | {'img/chengduhero.jpg', 'img/xianhero.jpg', 'img/panda.jpg'}
used |= {g for i in items for g in i['gallery']} | {g for d in decisions for o in d['options'] for g in o.get('gallery', []) if not g.startswith('http')} | {g['src'] for c in hotels.values() for h in c['options'] for g in h['gallery'] if not g['src'].startswith('http')}
credits = {k: v for k, v in json.load(open(os.path.join(HERE, 'credits.json'), encoding='utf-8')).items() if f'img/{k}.jpg' in used}
credits.update({'g/' + k: v for k, v in json.load(open(os.path.join(HERE, 'gallery_credits.json'), encoding='utf-8')).items() if f'img/g/{k}.jpg' in used})
unused = sorted(f'img/{k}.jpg' for k in IMG if f'img/{k}.jpg' not in used)
# ---------- details for ticketed items: what someone needs before voting (Tze, 13 Sep: "I do not know what it is from just that one picture") ----------
# Checked 13 Sep 2026 on Bendibao / Dahepiao / Qunar / Ctrip listings; times and prices change by season, so the sheet says "confirm nearer the date".
DETAILS = {
 'p:opera': {'what': "A 90-minute variety show of Sichuan opera highlights in a teahouse theatre: face-changing (masks switch in a blink), fire-spitting, hand-shadow puppets, the rolling-lamp comedy and folk music. Easy to enjoy without understanding Chinese.",
   'when': 'Nightly 20:00', 'length': '90 min', 'price': '¥88–¥498 depending on seat (蜀风雅韵, Culture Park); similar at 锦江剧场 near Chunxi Road',
   'kids': 'Fast and colourful, kids love the face-changing; gongs are loud for the baby, and it ends ~21:30', 'elderly': 'Seated with tea, no walking', 'watch': '蜀风雅韵 川剧变脸'},
 'p:pandatower': {'what': "Chengdu's 339 m TV tower, rebranded Tianfu Panda Tower: a 1-minute lift to the 230 m indoor deck for the city lights, with riverside bars below.",
   'when': 'Winter 10:00–21:00 (check last entry)', 'length': 'About 1 hour', 'price': '¥80 standard lift / ¥100 sightseeing lift; under 1.2 m free, discounts for 1.2–1.4 m and over-60s',
   'kids': 'Fine, indoor and warm', 'elderly': 'Lift all the way, little walking', 'watch': '天府熊猫塔 夜景'},
 'p:dongjiao': {'what': "A 1950s electronics factory turned art and music park: red-brick halls, chimneys, cafés and the red 'Chengdu wall' photo spot.",
   'when': 'Open all day', 'length': '1–2 hours', 'price': 'Free to enter', 'kids': 'Open space to run around', 'elderly': 'Flat paths, cafés to sit in', 'watch': '东郊记忆 拍照'},
 'p:qianguqing': {'what': "Songcheng's indoor song-and-dance spectacle of Xi'an's history from the Zhou to the Tang dynasties: rain falling on stage, flying sets, horses and hundreds of dancers.",
   'when': 'Usually 13:00 / 15:30 / 17:30 / 19:00 (varies by day)', 'length': 'About 60 min', 'price': '¥278 / ¥328 / ¥580 by seat; under 1.2 m or under 6 free without a seat',
   'kids': 'Big effects, short enough', 'elderly': 'About a 20-min walk from the park gate to the theatre', 'watch': '西安千古情 演出'},
 'p:tangshow': {'what': "Xi'an's classic Tang-court dinner show at 唐乐宫: a seated dinner, then costumed palace music and dance with a live traditional orchestra.",
   'when': 'Dinner from 18:50, show 《大唐女皇》 19:30–20:40 (19:00 / 20:30 on double-show days)', 'length': 'Show about 70 min', 'price': 'Dinner + show ¥350 (dumpling banquet) / ¥550 (palace banquet)',
   'kids': 'Seated the whole evening; finishes 20:40', 'elderly': 'Warm, comfortable, no walking', 'watch': '唐乐宫 仿唐乐舞', 'photo': 'Photo: a Tang dance performance, not this theatre.'},
 'p:gongyan': {'what': "Dinner inside the show: Tang palace dishes served while dance, aerial acts and light play on a revolving stage around the tables. You can dress in Tang costume first.",
   'when': 'Evening 19:00 (lunch sitting 12:00)', 'length': 'About 2 hours incl. a 15-min interval', 'price': 'From about ¥263 per person with the meal; children pay adult price; costume styling extra (kids\' costumes for ages 6–16)',
   'kids': 'Very photogenic; long sitting for the baby', 'elderly': 'Seated at tables throughout', 'watch': '大明宫宴', 'photo': 'Photo: a similar Tang performance, not this venue. Tap a video to see it.'},
 'p:changan12': {'what': "An indoor Tang-dynasty market street: costumed performers, snack stalls, costume rental and photo corners, based on the TV drama.",
   'when': '10:00–22:00', 'length': '2–3 hours', 'price': 'Entry ¥68 adult / ¥38 child (1.2 m+, under 18); under 1.2 m free. Re-priced March 2026 — older pages still say ¥128. Entry covers all ~100 performances including 极乐之宴 (a 15-min Tang banquet tableau); only the immersive game costs extra',
   'kids': 'Lots to look at; crowded at night', 'elderly': 'Indoor and warm, but on your feet', 'watch': '长安十二时辰 主题街区', 'photo': 'Photo: the Great Tang All Day Mall next door, not the street itself.'},
 'p:everlasting': {'what': "Xi'an's most famous show: an outdoor dance-drama staged on the real lake at Huaqing Palace, with Mount Li as the backdrop. The story of Emperor Xuanzong and Yang Guifei, told with a rising lake stage, water, fire and light.",
   'when': '⚠ Winter is the problem. The regular season runs mid-March to end-October. A heated-seat winter edition (冰火长恨歌) ran 1 Dec–28 Feb in 2024–25, sessions 18:30 / 19:55 / 21:20 / 22:45. Whether it runs in December 2026 is not announced either way. Checked Sep 2026 — only knowable in November.',
   'length': '70 min', 'price': 'From ¥249; under 1.3 m free without a seat. The show ticket does not include daytime entry to Huaqing Palace',
   'kids': 'Spectacular, but outdoors at night in the cold — only worth it if a December run is confirmed', 'elderly': 'Seated throughout; dress very warmly, it is an open-air hillside',
   'getting': 'Lintong, about 1 hour from the city and next to the Terracotta Army, so it follows straight on from Thursday',
   'watch': '冰火长恨歌', 'photo': 'First three are 长恨歌 publicity/key art from a ticket site, not the official site, and none shows the outdoor lake stage; the rest are Huaqing Palace itself, including the lake the stage sits on.'},
 'p:daqin': {'what': "A large indoor 'epic fantasy' production about the rise of the Qin dynasty, by the same company as 长恨歌. Moving seats, projection and stage machinery rather than a traditional stage show — closer to a theme-park ride with a story.",
   'when': 'Daily 14:45 / 16:45 / 19:45, year-round (it paused only 4–9 Jan 2026 for maintenance). Checked Sep 2026', 'length': '80 min, no interval',
   'price': 'C ¥338 / B ¥388 / A ¥458 / 贵宾B ¥588 / 贵宾A ¥688; children 5+ pay full price — so roughly ¥3,400–4,600 for the eight who can go. Real-name ticketing since March 2026, so passports',
   'kids': '⚠ Under-5s are refused outright — the baby cannot go in. Children 5+ pay the adult price. Every seat has a safety belt',
   'elderly': '⚠ The venue advises against it for anyone 75 or over, and for high blood pressure, heart disease, pregnancy or claustrophobia. No leaving mid-show. Check before booking for Ah Ma and Ah Gong',
   'getting': 'Fengdong New City, west of the city (沣东大道 × 天台路) — about 30–40 min from the Bell Tower and the opposite side of town from the Terracotta Army',
   'book': 'Book 10–15 days ahead on 大麦 / 猫眼 or the official site jjdq.changhenge.cn',
   'watch': '赳赳大秦', 'photo': 'Publicity stills carrying the 赳赳大秦 watermark, from a ticket site (not the official site). Tap a video for the real thing.'},
 'p:tuoling': {'what': "An indoor Silk Road epic: real camels and horses on stage, an avalanche, a sandstorm and fire, following a caravan out of Chang'an. Seven acts in a 3,000-seat theatre whose seating bank ROTATES to face each scene.",
   'when': 'Four to six sessions a day between about 10:30 and 19:45; they change weekly. ⚠ The theatre also takes an annual maintenance break — it fell on 2–20 December in 2024 and 5–30 January in 2026. The 2026–27 dates are not announced. Checked Sep 2026',
   'length': 'About 70 min', 'price': '¥288–458 by tier; under 1.2 m free on a lap, one per adult. Usually non-refundable once issued',
   'kids': '⚠ Free on a lap, but loud percussion, water mist in the front rows and startling effects — the operator warns young children may be frightened',
   'elderly': "⚠ The venue's own notice asks anyone with heart disease, high blood pressure or difficulty walking to think twice: the auditorium rotates and it is a long walk from the car park. If you go, buy a top tier for the shortest walk",
   'getting': '华夏大剧院, 灞桥区华文路1518号 — about 30 min from the Terracotta Army and on the way back to the city, so it fits Thursday',
   'watch': '驼铃传奇 演出', 'photo': 'No photo here — tap a video to see it.'},
 'p:menghui': {'what': "Tang Paradise's indoor theatre show: Tang court dance and music in a seated theatre rather than out on the lake.",
   'when': '⚠ Sources disagree: some list 17:00–18:00, most list 19:30–20:20. It IS in the winter and Spring-Festival schedules either way. Confirm when booking. Checked Sep 2026', 'length': '50–60 min',
   'price': '¥298 balcony / ¥398 stalls / ¥518 VIP; child ¥158–268 for 1.2–1.5 m; under 1.2 m free without a seat. The ticket includes entry to Tang Paradise',
   'kids': 'Seated and only an hour; an early finish for the baby',
   'elderly': 'The easiest show on this list: seated and indoors, about an hour. Tang Paradise entry is free for over-65s anyway. If the 19:30 time is the right one it is a later night than it looks',
   'getting': '凤鸣九天剧院 inside Tang Paradise, Qujiang — close to the Westin/W end of town',
   'watch': '梦回大唐 大唐芙蓉园', 'photo': 'Photos show Tang Paradise, the park the theatre sits in.'},
 'p:tangdream': {'what': "A boat-borne light and water spectacular on the lake at Tang Paradise: the audience rides in Tang-style barges between floating stages.",
   'when': '⚠ NOT ON IN DECEMBER. April to October only, about 20:00–21:20. Confirmed four ways: the 2026 relaunch was announced for April, it was marked suspended in January, and it is absent from both the Spring-Festival and 2026 lantern-festival line-ups. Checked Sep 2026',
   'length': '50 min', 'price': 'In season ¥318–618 adult / ¥168–318 child, park entry included',
   'kids': 'Moot for December', 'elderly': 'Moot for December — and it is an open, unheated boat',
   'getting': 'Tang Paradise, Qujiang, about 7.6 km from the Bell Tower',
   'watch': '大唐追梦 大唐芙蓉园', 'photo': 'Photos show Tang Paradise, the park, not the show.'},
 'p:juntuan': {'what': "China's first immersive multimedia war epic: four acts over 70 minutes following two Qin soldiers, Hei Fu and Jing, from the oldest surviving Chinese family letter. A 7,000 m² set with 360° projection, a troop review and a city assault.",
   'when': 'Several sessions between about 11:30 and 17:00, set day by day — published listings disagree with each other, so confirm for your date. Venue open 09:00–18:30 all year, indoors, so it does not stop for winter. Checked Sep 2026',
   'length': '70 min', 'price': '¥268 (often 20% off on the official channel); under 1.2 m free without a seat; real-name tickets, max 6 per order',
   'kids': '⚠ Battle scenes are loud and the floor vibrates — a lot for a baby in arms',
   'elderly': '⚠ 70 minutes standing and walking with no allocated seats, right after the Terracotta pits. A separate elderly/children route is mentioned in some guides but is not published by the theatre — ask when booking',
   'getting': '大秦剧场, 临潼区秦陵北路166号 — right beside the Terracotta Army, so it adds no extra driving on Thursday',
   'book': 'Check you are buying 《复活的军团》 and not 《永生的军团》, which has used the same theatre',
   'watch': '复活的军团 演出', 'photo': 'No photo here — the operator blocks them. Tap 小红书 or YouTube to see the real thing.'},
 'p:xianincident': {'what': "An immersive 'live-action picture' of the 1936 Xi'an Incident, when Chiang Kai-shek was seized at Huaqing Palace — staged indoors on the spot where it happened.",
   'when': 'About 11:30 / 14:10 / 16:20 daily, all year round (indoor, so it does not stop for winter). Checked Sep 2026', 'length': '60 min',
   'price': '¥258; the Huaqing Palace entry ticket is separate unless you buy a combo (¥80 in winter, not the ¥120 peak price); under 1.2 m free without a seat',
   'kids': '⚠ Heavy gunfire and explosion sound design — hard on a baby',
   'elderly': '⚠ The audience STANDS through the whole first half while the actors move among them; only the second half is seated, and seats are not numbered',
   'getting': '瑶光阁剧院 inside Huaqing Palace, Lintong — about an hour east of the city, so it only makes sense on the Terracotta day',
   'watch': '12·12 西安事变 实景影画', 'photo': 'No photo here — tap a video to see it.'},
 'p:mengchangan': {'what': "The Tang welcome ceremony on the city wall at the South Gate: drums, costumed guards and a court reception staged across the plaza, moat gate and barbican.",
   'when': '⚠ NOT ON IN DECEMBER. The season runs early April to the end of October, Tuesday to Sunday, 20:00–21:10 (later in midsummer). It is entirely outdoors on the wall, which is why it closes for winter. Checked Sep 2026',
   'length': '70 min', 'price': '¥280 (C/D), ¥380 (A/B), ¥880 VIP; under 1.2 m free without a seat',
   'kids': 'Outdoors and late', 'elderly': 'Outdoors, and a walk between the plaza and the barbican',
   'getting': 'Yongningmen South Gate, about 1.5 km south of the Bell Tower — walkable, but moot for a December trip',
   'watch': '梦长安 大唐迎宾盛礼', 'photo': 'No photo here — tap a video to see it.'},
 'p:emei': {'what': "Wang Chaoge's giant immersive theatre village at the foot of Mount Emei: you walk through dozens of small stages and courtyards, then watch the main show.",
   'when': 'Main show 19:30–21:00', 'length': 'Allow 3 hours on site', 'price': 'From ¥258', 'kids': 'Lots of walking between stages', 'elderly': 'Walking and stairs between stages',
   'getting': 'About 2 hours from Chengdu: a late night or a night in Emei; pairs with the Leshan day trip', 'watch': '只有峨眉山 演出'},
}
for it in items:
    if it['id'] == 'p:leshan': it['was'] = {'end': '14:00'}   # phones that locked Leshan before 14 Sep still hold the old end
    WAS = {'p:terracotta': {'time': '09:00'}, 'p:tangshow': {'time': '18:00', 'end': '21:40'}, 'p:gongyan': {'time': '18:45', 'end': '20:45'}, 'p:hanfu': {'time': '08:30', 'end': '11:15'},
           'p:lunch-d6': {'time': '13:15', 'end': '13:45'}}   # Xi'an review applied 15 Sep
    if it['id'] in WAS: it['was'] = WAS[it['id']]
DETAILS.update(MEAL_DET)
for it in items:
    if it['id'] in DETAILS: it['details'] = DETAILS[it['id']]
seed = {'trip': TRIP, 'elite': elite, 'days': days, 'items': items, 'blocks': blocks, 'decisions': decisions, 'hotels': hotels, 'prep': prep, 'family': family, 'phrases': phrases, 'credits': credits}
json.dump(seed, open(os.path.join(HERE, 'seed.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
ids = {i['id'] for i in items}
bad = [x for d in decisions for o in d['options'] for x in o['items'] if x not in ids]
assert not bad, bad
for i in items:
    if i['opt']:
        did, oid = i['opt'].split(':'); assert any(d['id'] == did and any(o['id'] == oid and i['id'] in o['items'] for o in d['options']) for d in decisions), i['id']
print(f"days {len(days)} | items {len(items)} ({sum(1 for i in items if i['status']=='scheduled' and not i['opt'])} fixed, {sum(1 for i in items if i['opt'])} vote options, {sum(1 for i in items if not i['day'])} ideas) | decisions {len(decisions)} | blocks {len(blocks)}")
print('no coords:', [i['id'] for i in items if not i['lat']])
print('no image:', [i['id'] for i in items if not i['img']] + [o['id'] for d in decisions for o in d['options'] if not o['img']])
print('unused images:', unused)
