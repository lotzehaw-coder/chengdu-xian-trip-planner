# Chengdu · Xi'an Family Trip Planner

A shared planner for a family of 10 (baby, kids and grandparents) going to Chengdu and Xi'an, 13–22 Dec 2026. It's built in the same style as the [Jiangnan planner](https://lotzehaw-coder.github.io/jiangnan-trip-planner/).

**Live:** https://lotzehaw-coder.github.io/chengdu-xian-trip-planner/

It's one file (`index.html`) plus photos in `img/`. There's no backend and no accounts; everything is stored in each person's own browser.

## What's in it

- **Itinerary**: nine colour-coded days (Chengdu green, Xi'an terracotta, travel slate), with MH526/MH527, trains, vans and hotel check-ins as fixed blocks. Tap a stop to see the photo, the book-ahead note, Map (opens 高德地图 Amap directly), a ❤, your own note, a new time or a move to another day. Tap the dot to tick a stop done; during the trip the hero shows *up next* in China time. A **Before we go** checklist gives the booking dates (panda tickets, trains, Terracotta Army, the Shaanxi History Museum). The **Family guide** explains the icons (👶 stroller-friendly, 🧓 easy walking, 🪜 stairs, 🧣 cold, 🏠 indoor, 🎟 book ahead, 🌶 spicy) and has phrases to show waiters and drivers.
- **Vote**: seven open slots (evenings, afternoons, the Sunday day trip, the last morning), each with 2–4 photo options. Extra ideas can be ❤'d.
- **Hotels**: four Marriott Bonvoy options per city with pros and cons for a family, and a vote for each city.
- **Share**: *Send my votes on WhatsApp* posts a short summary plus a link. When the organiser taps the link, that person's votes are counted on their phone. Messages can also be pasted in bulk. Results can be copied back to the group.

## Running the vote

1. Share the link in the family WhatsApp group.
2. Each person enters their name, votes, and taps **Send my votes on WhatsApp**.
3. The organiser taps each person's link (or pastes the messages into **Share → Count everyone's votes**).
4. Once a slot has a clear winner, the organiser taps **Lock in**, and the winning option's stops go onto the itinerary.
5. To hand the full plan (locks, moves, notes, votes) to a co-planner: **Share → Export plan**, send the file, and they **Import & merge**.

## Editing the plan

All the content lives in `tools/seed.py`: days, stops, vote options, hotels, the checklist and phrases.

```bash
cd tools
python seed.py      # -> seed.json
python build.py     # seed.json + template.html -> ../index.html (checks JS syntax with node)
```

Then commit and push. Stops nobody has touched follow the seed; anything someone moved or edited is left alone.

To add or replace a photo, add an entry to `tools/image_queries.json` (a search query, or `"pin": "File:<exact Commons file name>"`) and run `python fetch_images.py <id> --force`. Photos come from Wikimedia Commons under CC0 / CC BY / CC BY-SA, and the credits are listed in the app under **Share → About → Photo credits**.

Coordinates come from Wikipedia (WGS-84) and are converted to GCJ-02 for Chinese maps. Stops without coordinates, mostly restaurants, open a name search in Amap instead.

## Confirmed vs not

- **Booked:** MH526 KUL→TFU on Sun 13 Dec (lands just after midnight), and MH527 TFU→KUL departing just after midnight (so technically Tue 22 Dec). Check the exact times on the e-ticket.
- **Not booked:** hotels, trains, vans and all tickets. These are marked *tentative*.
