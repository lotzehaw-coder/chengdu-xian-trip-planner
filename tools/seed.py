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
MAPQ = {'lunch-mapo': '陈麻婆豆腐', 'peoplespark': '鹤鸣茶社', 'kuanzhai': '宽窄巷子', 'dinner-hotpot': '蜀九香火锅', 'panda': '成都大熊猫繁育研究基地',
  'lunch-longchaoshou': '龙抄手 春熙路', 'dinner-d2': '马旺子', 'wildgoose': '大雁塔', 'dinner-dapaidang': '长安大牌档', 'datang': '大唐不夜城',
  'terracotta': '秦始皇帝陵博物院', 'dinner-defachang': '德发长', 'shaanximuseum': '陕西历史博物馆', 'lunch-noodles': '樊记腊汁肉夹馍', 'citywall': '永宁门',
  'belltower': '西安钟楼', 'night-d6': '春熙路', 'lunch-zhong': '钟水饺', 'opera': '蜀风雅韵', 'jinli-eve': '锦里古街', 'taikooli': '成都远洋太古里',
  'wuhou': '成都武侯祠', 'huaqing': '华清宫', 'muslimquarter': '回民街', 'tangshow': '唐乐宫', 'yongxingfang': '永兴坊', 'hanfu': '大雁塔',
  'smallgoose': '小雁塔', 'leshan-train': '成都东站', 'leshan': '乐山大佛', 'dujiangyan': '都江堰景区', 'dufu': '杜甫草堂', 'sichuanmuseum': '四川博物院',
  'naturalhistory': '成都自然博物馆', 'wenshu': '文殊院', 'shopping': '成都国际金融中心', 'tianfu-idea': '天府广场', 'jinsha': '金沙遗址博物馆',
  'qingcheng': '青城山', 'tangparadise': '大唐芙蓉园', 'paomo': '老孙家泡馍', 'drumtower-in': '西安鼓楼', 'leshan-back': '乐山站'}
# English search for Google Maps (pre-trip reviews in English)
MAPEN = {'lunch-mapo': 'Chen Mapo Tofu', 'peoplespark': "People's Park Chengdu", 'kuanzhai': 'Kuanzhai Alley', 'dinner-hotpot': 'Shu Jiu Xiang Hot Pot',
  'panda': 'Chengdu Research Base of Giant Panda Breeding', 'lunch-longchaoshou': 'Long Chao Shou Chunxi Road', 'dinner-d2': 'Ma Wang Zi restaurant',
  'wildgoose': 'Big Wild Goose Pagoda', 'dinner-dapaidang': "Chang'an Da Pai Dang", 'datang': 'Great Tang All Day Mall', 'terracotta': 'Terracotta Army Museum',
  'dinner-defachang': 'De Fa Chang dumpling restaurant', 'shaanximuseum': 'Shaanxi History Museum', 'lunch-noodles': 'Fanji Roujiamo', 'citywall': "Yongningmen South Gate Xi'an City Wall",
  'belltower': "Bell Tower Xi'an", 'night-d6': 'Chunxi Road', 'lunch-zhong': 'Zhong Shui Jiao', 'opera': 'Shufeng Yayun Sichuan Opera', 'jinli-eve': 'Jinli Ancient Street',
  'taikooli': 'Sino-Ocean Taikoo Li Chengdu', 'wuhou': 'Wuhou Shrine', 'huaqing': 'Huaqing Palace', 'muslimquarter': "Muslim Quarter Xi'an", 'tangshow': 'Tang Dynasty Show Theater',
  'yongxingfang': 'Yongxingfang', 'hanfu': 'Big Wild Goose Pagoda', 'smallgoose': 'Small Wild Goose Pagoda', 'leshan-train': 'Chengdu East Railway Station',
  'leshan': 'Leshan Giant Buddha', 'dujiangyan': 'Dujiangyan Irrigation System', 'dufu': 'Du Fu Thatched Cottage', 'sichuanmuseum': 'Sichuan Museum',
  'naturalhistory': 'Chengdu Natural History Museum', 'wenshu': 'Wenshu Monastery', 'shopping': 'Chengdu IFS', 'tianfu-idea': 'Tianfu Square', 'jinsha': 'Jinsha Site Museum',
  'qingcheng': 'Mount Qingcheng', 'tangparadise': 'Tang Paradise', 'paomo': 'Lao Sun Jia Paomo', 'drumtower-in': "Drum Tower Xi'an", 'leshan-back': 'Leshan Railway Station'}

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
MAPCITY = {'leshan': 'Leshan', 'leshan-back': 'Leshan', 'dujiangyan': 'Dujiangyan', 'qingcheng': 'Dujiangyan'}
def I(id, day, name, city, cat, time='', end='', info='', fam=(), tags=(), key=None, pic=None, opt='', book=''):
    n = order.get(day, 0) + 1; order[day] = n
    lat, lng = at(key or id)
    items.append({'id': 'p:' + id, 'name': name, 'city': city, 'category': cat, 'time': time, 'end': end, 'info': info,
                  'fam': list(fam), 'tags': list(tags), 'img': (gal(pic or id) or [''])[0], 'gallery': gal(pic or id), 'mapq': MAPQ.get(id, ''), 'mapen': MAPEN.get(id, ''), 'mapcity': MAPCITY.get(id, city), 'lat': lat, 'lng': lng, 'address': '', 'book': book,
                  'day': day, 'suggestedDay': day, 'status': 'scheduled' if day and not opt else 'wishlist', 'opt': opt, 'order': n})

# Day 1 — Mon 14 Dec
I('lunch-mapo', D[1], 'Lunch — Chen Mapo Tofu 陈麻婆豆腐', 'Chengdu', 'Food', '12:00', '13:15',
  'The famous name in mapo tofu (several branches; Map lists them). Order some dishes 微辣 (wēi là, mild) or 不辣 (bù là, no chilli) for the kids and elderly.', ('easy', 'spicy'), pic='mapotofu')
I('peoplespark', D[1], "People's Park & Heming Teahouse 人民公园 · 鹤鸣茶社", 'Chengdu', 'Sight', '14:00', '15:30',
  'Chengdu at its most relaxed: bamboo chairs by the lake, a pot of jasmine tea, ear-cleaners doing the rounds, grandparents dancing. Flat paths all the way round.', ('stroller', 'easy'), ('must-see',))
I('kuanzhai', D[1], 'Kuanzhai Alley 宽窄巷子', 'Chengdu', 'Sight', '16:00', '17:30',
  'Three restored Qing-era lanes of courtyard houses, snacks and tea shops. Flat and pram-friendly; busy after 5pm, so hold small hands.', ('stroller', 'easy'))
I('dinner-hotpot', D[1], 'Dinner — Sichuan hot pot 火锅', 'Chengdu', 'Food', '18:00', '19:30',
  'Ask for a 鸳鸯锅 (yuān yāng guō): a split pot with a spicy side and a clear broth side, so the kids and elderly eat from the mild half. Well-known chains: 小龙坎 Xiaolongkan, 蜀九香 Shu Jiu Xiang (several branches; Map lists them).', ('spicy', 'indoor'), pic='hotpot')
# Day 2 — Tue 15 Dec
I('panda', D[2], 'Giant Panda Base 成都大熊猫繁育研究基地', 'Chengdu', 'Sight', '08:00', '11:30',
  'Go at opening: pandas are most active in the cool morning. Use the ¥10 park shuttle bus between enclosures to save little and older legs. The nurseries with cubs are the highlight.',
  ('stroller', 'cold', 'book'), ('must-see',), book="Tickets open 14 days ahead (from Tue 1 Dec) on Trip.com or the base's WeChat mini-program; passport for each person. Book the shuttle bus at the same time.")
I('lunch-longchaoshou', D[2], 'Lunch — Long Chao Shou wontons 龙抄手', 'Chengdu', 'Food', '12:15', '13:15',
  'A Chengdu snack institution on Chunxi Road: wontons in clear or red-oil broth, plus small plates of Chengdu snacks. Gentle food for everyone.', ('easy', 'indoor'), pic='wonton')
I('rest-d2', D[2], 'Back to the hotel — nap & rest', 'Chengdu', 'Rest', '13:30', '15:45',
  'Early start and a long walk: nap time for the baby and a rest for the elderly before the evening.', ('rest',), pic=REST)
I('dinner-d2', D[2], 'Dinner — Sichuan home cooking', 'Chengdu', 'Food', '19:00', '20:30',
  'e.g. 马旺子 Ma Wang Zi. Mild dishes that work for kids: 宫保鸡丁 kung pao chicken, 回锅肉 twice-cooked pork, 蒜蓉空心菜 garlic greens, 蛋炒饭 egg fried rice. Several branches; Map lists them.', ('indoor', 'spicy'), pic='sichuandishes')
# Day 3 — Wed 16 Dec
I('lunch-train', D[3], 'Lunch on the train', 'Travel', 'Food', '12:15', '13:00',
  'Buy buns and snacks at Chengdu East before boarding, or order a hot meal to your seat when booking on Trip.com / 铁路12306. Hot water taps in every carriage for baby bottles.', ('easy',), pic='hsr')
I('wildgoose', D[3], 'Big Wild Goose Pagoda 大雁塔', "Xi'an", 'Sight', '17:15', '18:15',
  'The 7th-century Tang pagoda, beautifully lit at dusk. The squares around it are free and flat; going inside the temple grounds is optional.', ('stroller', 'easy', 'cold'), ('must-see',))
I('dinner-dapaidang', D[3], "Dinner — Chang'an Da Pai Dang 长安大牌档", "Xi'an", 'Food', '18:30', '19:45',
  "Lively Shaanxi restaurant with the Xi'an classics in one place: roujiamo, biangbiang noodles, liangpi, paomo. Staff in costume; kids love it. Several branches near the pagoda.", ('indoor',), pic='biangbiang')
I('datang', D[3], 'Great Tang All Day Mall night walk 大唐不夜城', "Xi'an", 'Night', '19:45', '21:00',
  'A long pedestrian boulevard of Tang-dynasty light sculptures and street performers running south from the pagoda. Flat and wide, fine for strollers and wheelchairs. Very cold after dark in December.', ('stroller', 'easy', 'cold'), ('must-see',))
# Day 4 — Thu 17 Dec
I('terracotta', D[4], 'Terracotta Army 秦始皇兵马俑', "Xi'an", 'Sight', '09:00', '12:30',
  "Start at Pit 1 (the famous rows of 2,000-year-old warriors), then Pits 3 and 2. It's a long walk from the car park to the pits, so pace it for the elderly and bring the baby carrier as well as the stroller. The halls are big and cold in winter.",
  ('stroller', 'cold', 'book'), ('must-see',), book='Online only, up to 7 days ahead (from Thu 10 Dec); passport for each person. Book a private van for the day, about 1h each way.')
I('lunch-lintong', D[4], 'Lunch in Lintong', "Xi'an", 'Food', '12:45', '13:45',
  'Plenty of restaurants near the museum exit. Keep it simple and warm: noodles, dumplings, soup.', ('easy', 'indoor'), pic='biangbiang')
I('dinner-defachang', D[4], 'Dinner — De Fa Chang dumpling banquet 德发长饺子宴', "Xi'an", 'Food', '18:30', '20:00',
  'A long-established restaurant by the Bell Tower serving a banquet of dumplings in many shapes and fillings. Soft, not spicy, fun for kids and grandparents alike.', ('indoor', 'easy'), pic='dumplings')
# Day 5 — Fri 18 Dec
I('shaanximuseum', D[5], 'Shaanxi History Museum 陕西历史博物馆', "Xi'an", 'Sight', '09:00', '11:30',
  "One of China's great museums: Tang gold and silver, murals, Zhou bronzes. Warm and indoor, a good morning for everyone after yesterday's walking.",
  ('stroller', 'indoor', 'book'), ('must-see',), book="Free, but reserve with each person's passport on the museum's WeChat / website. Slots are released a few days ahead (reported 5–7 days); watch from Fri 11 Dec. Closed Mondays in winter.")
I('lunch-noodles', D[5], 'Lunch — biangbiang noodles & roujiamo', "Xi'an", 'Food', '12:00', '13:00',
  "Xi'an's two signatures: belt-wide hand-pulled noodles, and the \"Chinese burger\" of braised meat in a crisp bun (樊记腊汁肉夹馍 Fan Ji is the famous one).", ('easy',), pic='roujiamo')
I('citywall', D[5], 'City Wall at South Gate 永宁门', "Xi'an", 'Sight', '14:00', '15:45',
  'The most complete old city wall in China, about 14km round and wide enough to cycle. Bikes for the energetic; everyone else strolls a short stretch for the view. There are steps up at the gate, so ask at the ticket office for the easiest way up with the grandparents and the pram.', ('stairs', 'cold'), ('must-see',))
I('belltower', D[5], 'Bell & Drum Towers 钟楼 · 鼓楼', "Xi'an", 'Sight', '16:15', '17:15',
  'The two Ming towers at the heart of the old city, lit up at dusk. Seeing them from the square is free and easy; climbing is optional.', ('easy', 'cold'))
# Day 6 — Sat 19 Dec
I('lunch-d6', D[6], "Lunch at Xi'an North station", 'Travel', 'Food', '13:15', '13:45', 'Noodles and buns in the station food court, or pick up food for the train.', ('easy', 'indoor'), pic=[])
I('night-d6', D[6], 'Dinner & Chunxi Road by night 春熙路', 'Chengdu', 'Night', '19:30', '21:00',
  'Walk to the shopping streets for Christmas lights and street snacks: 钟水饺 Zhong dumplings, 糖油果子 sugar-fried dough balls, 冰粉 ice jelly.', ('stroller', 'easy'), pic='chunxi', key='chunxi')
# Day 7 — Sun 20 Dec
I('dinner-d7', D[7], 'Dinner near the hotel', 'Chengdu', 'Food', '19:00', '20:30', 'An easy one after a big day out.', ('easy', 'indoor'), pic=[])
# Day 8 — Mon 21 Dec (most Chengdu museums close on Mondays)
I('lunch-zhong', D[8], 'Lunch — Chengdu snacks 钟水饺 · 担担面', 'Chengdu', 'Food', '12:45', '13:45',
  'Sweet-soy Zhong dumplings, dan dan noodles, 赖汤圆 glutinous rice balls. Order a spread and share.', ('easy', 'indoor'), pic='dumplings')
I('rest-d8', D[8], 'Rest, showers & pack (keep the rooms)', 'Chengdu', 'Rest', '14:00', '17:30',
  'The flight leaves after midnight. Keep the rooms until evening (late check-out, or book the night of 21 Dec) so the baby naps and everyone showers before the airport.', ('rest',), pic=REST)
I('dinner-farewell', D[8], 'Farewell dinner', 'Chengdu', 'Food', '18:00', '19:45',
  'A proper Sichuan banquet to finish: book a private room 包间 for 10. Keep it early; the airport run starts at 21:30.', ('indoor',), pic='hotpot')

# ---------- decisions: the family votes; the organiser locks the winner ----------
decisions = []
def DEC(id, day, time, title, question, options, kind='activity'):
    decisions.append({'id': id, 'day': day, 'time': time, 'title': title, 'question': question, 'kind': kind, 'options': options})
def O(id, name, city, blurb, fam=(), pic=None, its=()):
    return {'id': id, 'name': name, 'city': city, 'blurb': blurb, 'fam': list(fam), 'img': (gal(pic or id) or [''])[0], 'gallery': gal(pic or id), 'items': ['p:' + x for x in its]}

I('opera', D[1], 'Sichuan Opera face-changing show 蜀风雅韵', 'Chengdu', 'Show', '20:00', '21:30',
  "Chengdu's classic evening show in a teahouse theatre: face-changing, fire-spitting, shadow puppets, comic sketches. Seats with tea.", ('indoor', 'book'), opt='d-d1eve:opera', pic='sichuanopera', book='Book 1–2 days ahead on Trip.com.')
I('jinli-eve', D[1], 'Jinli Street lanterns 锦里', 'Chengdu', 'Night', '20:15', '21:15', 'Red lanterns reflected in the ponds, snack stalls, next to Wuhou Shrine. Pretty and short.', ('stroller', 'cold'), opt='d-d1eve:jinli', pic='jinli', key='jinli')
I('earlynight', D[1], 'Early night: jet-lag recovery', 'Chengdu', 'Rest', '20:15', '', 'We landed after midnight. Bath, bed.', ('rest',), opt='d-d1eve:rest', pic=REST)
DEC('d-d1eve', D[1], '20:00', 'Monday evening', 'After hot pot on the first night, what next?', [
  O('opera', 'Sichuan Opera face-changing', 'Chengdu', 'The masks that change in a flash. 1.5h, seats with tea. Late-ish for the baby.', ('indoor', 'book'), 'sichuanopera', ['opera']),
  O('jinli', 'Jinli lanterns stroll', 'Chengdu', 'Short, pretty, lantern-lit old street. About 1 hour.', ('stroller', 'cold'), 'jinli', ['jinli-eve']),
  O('rest', 'Early night', 'Chengdu', 'We land after midnight the night before. Sleep wins.', ('rest',), REST, ['earlynight'])])

I('taikooli', D[2], 'Taikoo Li, Daci Temple & the IFS panda 太古里 · 大慈寺', 'Chengdu', 'Shop', '16:00', '18:30',
  'Low-rise open-air shopping streets around a Buddhist temple, then the giant panda climbing the side of IFS. Christmas lights in December.', ('stroller', 'easy'), opt='d-d2pm:taikoo')
I('wuhou', D[2], 'Wuhou Shrine & Jinli 武侯祠 · 锦里', 'Chengdu', 'Sight', '16:00', '18:30',
  'Memorial temple to the Three Kingdoms heroes (Zhuge Liang, Liu Bei) with red walls and bamboo, then the lantern street next door.', ('stroller', 'easy'), opt='d-d2pm:wuhou')
I('pool-d2', D[2], 'Hotel pool, lounge & free time', 'Chengdu', 'Rest', '16:00', '18:30', "Swim, tea, naps. Save energy for Xi'an.", ('rest',), opt='d-d2pm:rest', pic=REST)
DEC('d-d2pm', D[2], '16:00', 'Tuesday late afternoon', 'After the pandas and a nap:', [
  O('taikoo', 'Taikoo Li + IFS panda', 'Chengdu', 'Shopping streets around an old temple, Christmas lights, the famous climbing panda.', ('stroller', 'easy'), 'taikooli', ['taikooli']),
  O('wuhou', 'Wuhou Shrine + Jinli', 'Chengdu', 'Three Kingdoms temple and bamboo gardens, then the lantern street.', ('stroller', 'easy'), 'wuhou', ['wuhou']),
  O('rest', 'Pool & lounge', 'Chengdu', 'A quiet afternoon at the hotel.', ('rest',), REST, ['pool-d2'])])

I('huaqing', D[4], 'Huaqing Palace 华清宫', "Xi'an", 'Sight', '14:00', '16:00',
  "Tang emperors' hot-spring palace at the foot of Mount Li, next to the Terracotta Army. Gardens and pavilions by a lake.", ('stroller', 'cold'), opt='d-d4pm:huaqing')
I('rest-d4', D[4], 'Back to the hotel to rest', "Xi'an", 'Rest', '14:00', '17:30', 'The Terracotta Army is a long morning on foot. Warm up and nap.', ('rest',), opt='d-d4pm:rest', pic=REST)
DEC('d-d4pm', D[4], '14:00', 'Thursday afternoon', 'After the Terracotta Army:', [
  O('huaqing', 'Huaqing Palace', "Xi'an", 'Imperial hot-spring gardens nearby, no extra long drive.', ('stroller', 'cold'), 'huaqing', ['huaqing']),
  O('rest', 'Hotel & rest', "Xi'an", 'Head back, warm up and nap before the dumpling dinner.', ('rest',), REST, ['rest-d4'])])

I('muslimquarter', D[5], 'Muslim Quarter street food 回民街', "Xi'an", 'Food', '17:30', '19:30',
  'The old Hui neighbourhood behind the Drum Tower: lamb skewers, persimmon cakes, sticky rice cake, pomegranate juice. Very crowded, so bring the baby carrier rather than the stroller.', ('cold',), opt='d-d5eve:muslim')
I('tangshow', D[5], 'Tang Dynasty dinner & show 唐乐宫', "Xi'an", 'Show', '18:00', '21:40',
  'Seated dinner from 18:00, then a big costumed Tang-court music and dance show (about 20:15–21:40). Warm, comfortable, no walking.', ('indoor', 'easy', 'book'), opt='d-d5eve:tang', book='Book a few days ahead on Trip.com.')
I('yongxingfang', D[5], 'Yongxingfang food street 永兴坊', "Xi'an", 'Food', '17:30', '19:30',
  'A calmer, tidier food street by the city wall, with snacks from all over Shaanxi.', ('stroller', 'cold'), opt='d-d5eve:yxf')
DEC('d-d5eve', D[5], '17:30', 'Friday evening', "Last night in Xi'an:", [
  O('muslim', 'Muslim Quarter food crawl', "Xi'an", 'The famous one: loud, crowded, delicious.', ('cold',), 'muslimquarter', ['muslimquarter']),
  O('tang', 'Tang Dynasty dinner show', "Xi'an", 'Sit-down dinner with a big costumed show. Easiest for the grandparents.', ('indoor', 'easy', 'book'), 'tangshow', ['tangshow']),
  O('yxf', 'Yongxingfang food street', "Xi'an", 'Same snacks, fewer crowds, stroller works.', ('stroller', 'cold'), 'yongxingfang', ['yongxingfang'])])

I('hanfu', D[6], 'Tang costume family photoshoot 唐装 · 汉服', "Xi'an", 'Show', '08:30', '11:15',
  "Rent Tang-style robes near the Big Wild Goose Pagoda and take family portraits. Hair and make-up for 10 is slow, so start at opening, or dress just the kids and a few adults. Back for the 12:00 check-out.", ('easy', 'book'), opt='d-d6am:hanfu', pic=['img/g/datang-4.jpg', 'img/g/datang-3.jpg'], book='Book a studio 1–2 days ahead.')
I('smallgoose', D[6], "Small Wild Goose Pagoda & Xi'an Museum 小雁塔 · 西安博物院", "Xi'an", 'Sight', '09:30', '11:30',
  'Quiet temple garden with a slender Tang pagoda, and a free city museum in the same grounds. Calm and flat.', ('stroller', 'easy'), opt='d-d6am:goose')
I('slow-d6', D[6], 'Slow morning, brunch & pack', "Xi'an", 'Rest', '09:30', '11:30', 'Lie-in before the train.', ('rest',), opt='d-d6am:slow', pic=REST)
DEC('d-d6am', D[6], '08:30', 'Saturday morning', 'Before the afternoon train back to Chengdu:', [
  O('hanfu', 'Tang costume family photos', "Xi'an", 'Dress up in Tang robes for portraits by the pagoda. Early start; hair & make-up for 10 takes a while.', ('easy', 'book'), ['img/g/datang-4.jpg', 'img/g/datang-3.jpg'], ['hanfu']),
  O('goose', 'Small Wild Goose Pagoda', "Xi'an", 'Peaceful garden and free museum.', ('stroller', 'easy'), 'smallgoose', ['smallgoose']),
  O('slow', 'Slow morning', "Xi'an", 'Sleep in, brunch, pack.', ('rest',), REST, ['slow-d6'])])

I('leshan-train', D[7], 'G-train Chengdu East → Leshan 乐山', 'Chengdu', 'Travel', '08:30', '09:40', 'About 1 hour, then 30 min by van to the river pier.', ('book',), opt='d-d7:leshan', pic='hsr', key='cdeast',
  book='Train tickets open 15 days ahead counting the travel day: Sun 6 Dec for both the outbound and return trains.')
I('leshan', D[7], 'Leshan Giant Buddha by boat 乐山大佛', 'Chengdu', 'Sight', '10:30', '14:00',
  'The 71m Buddha carved into a riverside cliff 1,200 years ago. The river boat shows the whole figure with no steps, which is best for the baby and grandparents. The path down beside the Buddha is hundreds of steep steps with long queues; optional for the fit.', ('cold',), opt='d-d7:leshan')
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
  "Chengdu's busiest Buddhist temple: incense and quiet courtyards. Its well-known vegetarian restaurant can replace the snack lunch if you prefer.", ('stroller', 'easy'), opt='d-d8am:wenshu')
I('shopping', D[8], 'Last-minute shopping: IFS & Chunxi Road', 'Chengdu', 'Shop', '10:30', '12:30', 'Panda souvenirs, Sichuan pepper and tea to take home.', ('stroller', 'easy', 'indoor'), opt='d-d8am:shop', pic='ifspanda', key='ifs')
I('pool-d8', D[8], 'Pool & slow morning', 'Chengdu', 'Rest', '10:30', '12:30', 'Rest up before the overnight flight.', ('rest',), opt='d-d8am:rest', pic=REST)
DEC('d-d8am', D[8], '10:30', 'Monday morning', 'Last morning (most museums are closed on Mondays):', [
  O('wenshu', 'Wenshu Monastery', 'Chengdu', 'Temple courtyards, incense and ginkgo trees.', ('stroller', 'easy'), 'wenshu', ['wenshu']),
  O('shop', 'Shopping at IFS & Chunxi Rd', 'Chengdu', 'Souvenirs, tea, Sichuan pepper.', ('stroller', 'indoor'), 'ifspanda', ['shopping']),
  O('rest', 'Pool & slow morning', 'Chengdu', 'Save energy for the 1am flight.', ('rest',), REST, ['pool-d8'])])

# ---------- ideas: not on a day; heart the ones you want ----------
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
def H(id, name, cn, area, addr, pros, cons, url, pic, fits, up, upnote, opened, reno):
    return {'id': id, 'name': name, 'cn': cn, 'area': area, 'address': addr, 'pros': pros, 'cons': cons, 'url': url, 
            'img': img(pic), 'gallery': hgal(id), 'fits': fits, 'up': up, 'upnote': upnote, 'opened': opened, 'reno': reno}
hotels = {
 'Chengdu': {'nights': 'Sun 13 → Wed 16 Dec (3 nights) and Sat 19 → Mon 21 Dec (2 nights + the evening)',
  'tip': "Book the same hotel for both Chengdu stays: leave the big suitcases with the concierge while you're in Xi'an and take only overnight bags and the baby things on the train. Book the first night from Sun 13 Dec and tell the hotel you'll arrive around 1:30am, so the rooms are held.",
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
 "Xi'an": {'nights': 'Wed 16 → Sat 19 Dec (3 nights)',
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
for cityname, hid, q in (('Chengdu', 'h-chengdu', 'Where should we stay in Chengdu (both stays)?'), ("Xi'an", 'h-xian', "Where should we stay in Xi'an?")):
    decisions.append({'id': hid, 'day': '', 'time': '', 'title': cityname + ' hotel', 'question': q, 'kind': 'hotel',
      'options': [{'id': h['id'], 'name': h['name'], 'city': cityname, 'blurb': h['fits'], 'fam': [], 'img': h['gallery'][0]['src'], 'gallery': [g['src'] for g in h['gallery']], 'items': []} for h in hotels[cityname]['options']]})

# ---------- fixed blocks ----------
blocks = []
def B(id, day, type, title, time='', key=None, **kw):
    b = {'id': 'seed:' + id, 'day': day, 'type': type, 'title': title, 'time': time, 'sort': '', 'number': '', 'from': '', 'to': '', 'tentative': False, 'note': '', 'updatedAt': 0}
    b.update(kw); b['lat'], b['lng'] = at(key) if key else (None, None)
    b['mapq'] = {'land': '成都天府国际机场', 'tfu': '成都天府国际机场', 'g1': '成都东站', 'x1': '西安北站', 'g2': '西安北站', 'x2': '西安北站', 'd2van': '成都大熊猫繁育研究基地'}.get(id, '')
    b['mapen'] = {'land': 'Chengdu Tianfu International Airport', 'tfu': 'Chengdu Tianfu International Airport', 'g1': 'Chengdu East Railway Station', 'x1': "Xi'an North Railway Station", 'g2': "Xi'an North Railway Station", 'x2': "Xi'an North Railway Station", 'd2van': 'Chengdu Research Base of Giant Panda Breeding'}.get(id, '')
    if type == 'hotel': b['dec'] = 'h-xian' if id.startswith('h2') else 'h-chengdu'
    blocks.append(b)
B('mh526', D[0], 'flight', 'Fly to Chengdu Tianfu', '19:00', number='MH526', **{'from': 'KUL', 'to': 'TFU'}, note='Business · lands about 00:05–00:15 Monday · confirm exact times on the e-ticket')
B('land', D[0], 'car', 'Land at Tianfu, immigration, vans to the hotel', '00:15', sort='24:15', key='tfu', tentative=True,
  note='+1 day · pre-book 2 × 7-seat vans (or a 12–14 seat minibus) for 10 people, luggage and pram · about 1h to the city centre')
B('h1in', D[0], 'hotel', 'Check in: {hotel}', '02:00', sort='26:00', tentative=True, note="book this room from Sun 13 Dec so it's held for a ~2am arrival (immigration + bags for 10 take time)")
B('d2van', D[2], 'car', 'Van to the Panda Base', '07:30', key='panda', note='about 30 min from the centre · be there at opening')
B('h1out', D[3], 'hotel', 'Check out of {hotel}: leave the big bags with the concierge', '09:30', note='back to the same hotel on Sat 19 Dec')
B('g1', D[3], 'train', "G-train Chengdu East → Xi'an North", '11:30', key='cdeast', tentative=True, **{'from': 'Chengdu East 成都东', 'to': "Xi'an North 西安北"},
  note='about 3h10–3h40 · not booked · tickets open Wed 2 Dec (15 days ahead, counting the travel day) · First or Business class for the grandparents · under-6s ride free without a seat')
B('x1', D[3], 'car', "Vans to the Xi'an hotel", '15:45', key='xianN', note='about 40 min to Qujiang')
B('h2in', D[3], 'hotel', 'Check in: {hotel}', '16:30', tentative=True)
B('d4van', D[4], 'car', 'Private van for the Terracotta day', '08:00', tentative=True, note='about 1h each way · keep the van all day')
B('h2out', D[6], 'hotel', 'Check out of {hotel}', '12:00')
B('x2', D[6], 'car', "Vans to Xi'an North", '12:30', key='xianN', note='allow time for station security')
B('g2', D[6], 'train', "G-train Xi'an North → Chengdu East", '14:00', key='xianN', tentative=True, **{'from': "Xi'an North 西安北", 'to': 'Chengdu East 成都东'},
  note='about 3h10–3h40 · tickets open Sat 5 Dec')
B('h3in', D[6], 'hotel', 'Check in: back to {hotel}', '18:15', note='the big bags are waiting')
B('h3out', D[8], 'hotel', 'Check out of {hotel}', '21:15', note='keep the rooms till evening: late check-out, or book the night of 21 Dec')
B('tfu', D[8], 'car', 'Vans to Tianfu Airport', '21:30', key='tfu', note='about 1h–1h15 · aim for check-in by 22:45')
B('mh527', D[8], 'flight', 'Fly home to Kuala Lumpur', '01:05', sort='25:05', number='MH527', **{'from': 'TFU', 'to': 'KUL'},
  note='departs just after midnight, so technically Tue 22 Dec · lands about 06:10 · Business · confirm exact times on the e-ticket')

# ---------- before we go ----------
prep = [
 ['Now', 'Vote on hotels, then book each room direct under a different Platinum/Titanium member (tips in the Hotels tab). Ask for connecting rooms and a baby cot.'],
 ['Now', 'Passports valid 6+ months. Malaysians currently enter China visa-free for up to 30 days; re-check nearer the date.'],
 ['Now', 'Set up Alipay (and/or WeChat Pay) with a Malaysian card and get China eSIMs. Install 高德 Amap, Didi and Trip.com.'],
 ['Tue 1 Dec', 'Panda Base tickets + shuttle bus for Tue 15 Dec (14 days ahead).'],
 ['Wed 2 Dec', "Train tickets to Xi'an for Wed 16 Dec (rail sales open 15 days ahead, counting the travel day)."],
 ['Sat 5 Dec', "Train back Xi'an → Chengdu for Sat 19 Dec."],
 ['Sun 6 Dec', 'Leshan trains, there and back, for Sun 20 Dec, if Leshan wins the vote.'],
 ['By 6 Dec', 'Book vans: Tianfu Airport pickup ~00:15 Mon 14 Dec (10 people + luggage + pram), the Terracotta day van, and the 21:30 airport run on Mon 21 Dec.'],
 ['Thu 10 Dec', 'Terracotta Army tickets for Thu 17 Dec (online only, 7 days ahead, passports).'],
 ['Fri 11 Dec', 'Start watching for Shaanxi History Museum slots for Fri 18 Dec (free, passport per person, released a few days ahead).'],
 ['Pack', "Chengdu is about 5–12°C and damp; Xi'an about −3–8°C and dry. Thermals, gloves and beanies for everyone; a pram cover and baby carrier; tissues (many toilets have none); the grandparents' medicines in hand luggage."],
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
seed = {'elite': elite, 'days': days, 'items': items, 'blocks': blocks, 'decisions': decisions, 'hotels': hotels, 'prep': prep, 'family': family, 'phrases': phrases, 'credits': credits}
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
