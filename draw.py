"""news-23 b70 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, 31 stories. PIL only; run: python3 draw.py -> entry.png
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"

def f_serif_b(s): return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", s)
def f_serif(s): return ImageFont.truetype(FD + "DejaVuSerif.ttf", s)
def f_sans(s): return ImageFont.truetype(FD + "DejaVuSans.ttf", s)
def f_sans_b(s): return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)

BLACK = (17, 17, 17); WHITE = (255, 255, 255); GOLD = (212, 175, 55)
RED = (176, 0, 32); DARKRED = (140, 20, 20); BLUE = (29, 78, 216)
NAVY = (15, 30, 58); TEAL = (14, 124, 123); CREAM = (245, 239, 224)
GRAY = (90, 90, 90); LGRAY = (230, 230, 230); GREEN = (11, 122, 91)
BROWN = (139, 90, 43); PURPLE = (109, 40, 217); ORANGE = (245, 158, 11)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def tw(text, font):
    return d.textlength(text, font=font)

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(x0, x1, y, text, font, fill):
    d.text(((x0 + x1 - tw(text, font)) / 2, y), text, font=font, fill=fill)

def chip(x_right, y, text, fill):
    # chip box right-aligned at x_right, height 13
    w = tw(text, f_sans_b(9)) + 10
    d.rounded_rectangle([x_right - w, y, x_right, y + 13], radius=3, fill=fill)
    d.text((x_right - w + 5, y + 2), text, font=f_sans_b(9), fill=WHITE)

# ---------- masthead ----------
d.rectangle([0, 0, W, 52], fill=BLACK)
d.text((12, 6), "THE WORLD TODAY", font=f_serif_b(40), fill=WHITE)
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - tw(dt, f_sans_b(15)) - 12, 18), dt, font=f_sans_b(15), fill=GOLD)

# ---------- kicker ----------
d.text((12, 56), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=f_sans_b(15), fill=RED)

# ---------- number strip (2 rows x 5) ----------
strip = [
    [("-3.3%", RED, "KOSPI"), ("5.3", BLUE, "US-CHINA POWER GAP"),
     ("11,762", (0, 128, 0), "EBOLA CASES, DRC"), ("10T won", BROWN, "SEOUL STABILISATION FUND"),
     ("2%", PURPLE, "BILLIONAIRE TAX IN PARIS")],
    [("$450M", PURPLE, "SKUBAL DEAL"), ("165", RED, "RUSSIAN MISSILES/WEEK"),
     ("12,000", BLUE, "CLEARED IN MANCHESTER"), ("264 kg", BROWN, "EXPLOSIVES SEIZED"),
     ("$107.3B", PURPLE, "ANTHROPIC IPO")],
]
for r, row in enumerate(strip):
    yv = 75 + r * 25
    for c, (val, col, lab) in enumerate(row):
        x = c * 205 + 4
        d.text((x, yv), val, font=f_sans_b(17), fill=col)
        d.text((x, yv + 18), lab, font=f_sans_b(8), fill=BLACK)

# ---------- region bar ----------
regs = [("ASIA-PACIFIC 7", GREEN, 231), ("AMERICAS 8", BLUE, 264),
        ("MIDDLE EAST 6", BROWN, 198), ("EUROPE 5", PURPLE, 165),
        ("AFRICA 3", RED, 99), ("WORLD 2", (75, 85, 99), 67)]
x = 0
for name, col, w in regs:
    d.rectangle([x, 128, x + w, 148], fill=col)
    center(x, x + w, 133, name, f_sans_b(12), WHITE)
    x += w

# ---------- UTC strip ----------
d.text((8, 150), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
       font=f_sans(10), fill=GRAY)
d.text((W - tw("~ APPROX", f_sans(10)) - 8, 150), "~ APPROX", font=f_sans(10), fill=GRAY)

# ---------- hero scenes ----------
COLS = [(0, 336), (340, 676), (680, 1024)]
# scene 1: Kospi
x0, x1 = COLS[0]
d.rectangle([x0, 162, x1, 300], fill=NAVY)
d.text((x0 + 8, 168), "-3.3%", font=f_sans_b(30), fill=(255, 80, 80))
import random
random.seed(7)
bx = x0 + 6
while bx < x1 - 20:
    bw = random.randint(22, 34); bh = random.randint(28, 58)
    d.rectangle([bx, 272 - bh, bx + bw, 272], fill=(24, 48, 88))
    for wy in range(272 - bh + 5, 268, 9):
        for wx in range(bx + 4, bx + bw - 3, 8):
            if random.random() < 0.6:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 90))
    bx += bw + 3
pts = [(x0 + 8, 248), (x0 + 45, 232), (x0 + 85, 244), (x0 + 125, 222),
       (x0 + 165, 238), (x0 + 205, 226), (x0 + 245, 240), (x0 + 285, 224),
       (x0 + 322, 236)]
d.line(pts, fill=ORANGE, width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 220, 130))
d.rectangle([x0, 282, x1, 300], fill=BLACK)
d.text((x0 + 8, 286), "KOSPI 4,708.54   \u00b7   -161 PTS", font=f_sans_b(11), fill=WHITE)

# scene 2: Guterres
x0, x1 = COLS[1]
d.rectangle([x0, 162, x1, 300], fill=TEAL)
for i, ln in enumerate(["150 DELEGATES", "BACK A RISK", "FRAMEWORK"]):
    d.text((x0 + 12, 172 + i * 32), ln, font=f_sans_b(26), fill=GOLD)
cx, cy, r = x1 - 52, 228, 36
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=WHITE, width=1)
d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=1)
d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=WHITE, width=1)
d.rectangle([x0, 282, x1, 300], fill=BLACK)
d.text((x0 + 8, 286), "UN   \u00b7   BRIDGETOWN", font=f_sans_b(11), fill=WHITE)

# scene 3: Power Index
x0, x1 = COLS[2]
d.rectangle([x0, 162, x1, 300], fill=CREAM)
d.text((x0 + 8, 168), "NARROWEST SINCE 2018", font=f_sans_b(11), fill=BLACK)
d.text((x1 - tw("GAP 5.3", f_sans_b(11)) - 8, 168), "GAP 5.3", font=f_sans_b(11), fill=(176, 141, 30))
base = 278
bars = [("78.9", "US", NAVY, 70, 710), ("73.6", "CHINA", RED, 65, 810),
        ("40.5", "INDIA", (176, 141, 30), 36, 910)]
for val, lab, col, bh, bx in bars:
    d.rectangle([bx, base - bh, bx + 70, base], fill=col)
    if bh >= 60:
        center(bx, bx + 70, base - bh + 6, val, f_sans_b(13), WHITE)
        center(bx, bx + 70, base - 16, lab, f_sans_b(10), WHITE)
    else:
        center(bx, bx + 70, base - bh - 16, val, f_sans_b(13), BLACK)
        center(bx, bx + 70, base - 16, lab, f_sans_b(10), WHITE)
d.rectangle([x0, 282, x1, 300], fill=BLACK)
d.text((x0 + 8, 286), "ASIA POWER INDEX 2026", font=f_sans_b(11), fill=WHITE)

# ---------- hero text blocks ----------
heroes = [
    (1, "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED", BLUE),
    (2, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED", BLUE),
    (3, "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", BLUE),
]
for (num, head, body, src, ch, chcol), (x0, x1) in zip(heroes, COLS):
    cy = 318
    d.ellipse([x0 + 2, cy - 11, x0 + 24, cy + 11], fill=RED)
    d.text((x0 + 8, cy - 8), str(num), font=f_sans_b(12), fill=WHITE)
    lines = wrap(head, f_serif_b(17), x1 - x0 - 32)
    for i, ln in enumerate(lines[:2]):
        d.text((x0 + 30, 306 + i * 20), ln, font=f_serif_b(17), fill=BLACK)
    blines = wrap(body, f_sans(11), x1 - x0 - 6)
    for i, ln in enumerate(blines[:2]):
        d.text((x0 + 2, 352 + i * 14), ln, font=f_sans(11), fill=BLACK)
    d.text((x0 + 2, 384), src, font=f_sans(9), fill=GRAY)
    chip(x1 - 2, 382, ch, chcol)

# ---------- MORE bar ----------
d.rectangle([0, 396, W, 414], fill=BLACK)
d.text((8, 399), "MORE OF THE DAY  \u2014  10 STORIES", font=f_sans_b(12), fill=WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", RED, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", BLUE),
    ("FBI", DARKRED, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", BLUE),
    ("WHITE HOUSE", BROWN, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", BLUE),
    ("MARKETS", BLUE, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", BLUE),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", BLUE),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", BLUE),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", BLUE),
    ("TECH", BLUE, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", BLUE),
    ("EUROPE", PURPLE, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", (75, 85, 99), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", RED),
]
for i, (cat, ccol, head, body, src, ch, chcol) in enumerate(cards):
    row, col = divmod(i, 5)
    x0 = col * 205 + 2
    y0 = 418 + row * 74
    d.rectangle([x0, y0, x0 + 200, y0 + 15], fill=ccol)
    d.text((x0 + 4, y0 + 2), cat, font=f_sans_b(9), fill=WHITE)
    d.text((x0 + 200 - tw(str(i + 1), f_sans_b(9)) - 4, y0 + 2), str(i + 1), font=f_sans_b(9), fill=WHITE)
    hlines = wrap(head, f_sans_b(12), 196)
    for j, ln in enumerate(hlines[:2]):
        d.text((x0 + 2, y0 + 19 + j * 14), ln, font=f_sans_b(12), fill=BLACK)
    d.text((x0 + 2, y0 + 50), body, font=f_sans(10), fill=BLACK)
    d.text((x0 + 2, y0 + 62), src, font=f_sans(8), fill=GRAY)
    chip(x0 + 200, y0 + 60, ch, chcol)

# ---------- map + ALSO ----------
d.rectangle([0, 566, 336, 584], fill=BLACK)
d.text((8, 569), "WHERE IT HAPPENED", font=f_sans_b(12), fill=WHITE)
d.rectangle([340, 566, W, 584], fill=BLACK)
d.text((348, 569), "ALSO ON MONDAY", font=f_sans_b(12), fill=WHITE)
# map grid
d.rectangle([0, 584, 336, 800], fill=(248, 248, 245))
for gx in range(0, 337, 24):
    d.line([(gx, 584), (gx, 800)], fill=LGRAY, width=1)
for gy in range(584, 801, 24):
    d.line([(0, gy), (336, gy)], fill=LGRAY, width=1)
d.ellipse([10, 610, 190, 780], fill=(190, 220, 170))
d.ellipse([150, 600, 330, 770], fill=(190, 220, 170))
d.ellipse([150, 740, 260, 800], fill=(190, 220, 170))
pins = {1: (280, 640), 2: (95, 718), 3: (300, 620), 4: (60, 660),
        5: (110, 700), 6: (250, 700), 7: (140, 640), 8: (30, 700),
        9: (70, 748), 10: (122, 744), 11: (270, 670), 12: (290, 690),
        13: (310, 650)}
for n, (px, py) in pins.items():
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    t = str(n)
    d.text((px - tw(t, f_sans_b(9)) / 2, py - 6), t, font=f_sans_b(9), fill=WHITE)
leg = ["Pins 1-13:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing",
       "4 Washington  \u00b7  5 New York  \u00b7  6 Tehran  \u00b7  7 Chicago",
       "8 SF  \u00b7  9 Denver  \u00b7  10 Austin  \u00b7  11 Warsaw  \u00b7  12 Kyiv  \u00b7  13 Moscow"]
for i, ln in enumerate(leg):
    d.text((8, 762 + i * 12), ln, font=f_sans(8), fill=BLACK)

also_l = ["14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
          "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
          "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
          "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
          "22. Iran war: no deal in sight"]
also_r = ["23. Lebanon seizes 264 kg explosives", "24. Bahrain: strike hits plant, 2 hurt",
          "25. Sudan: defences down drones", "26. DRC: fighting traps Ebola teams",
          "27. Bangladesh: Hasina jailed if she returns", "28. Seoul minister quits in exam row",
          "29. SK Telecom -7.3% as hype cools", "30. China eases margin rules",
          "31. Seoul readies 10T-won fund"]
for i, ln in enumerate(also_l):
    d.text((344, 590 + i * 23), ln, font=f_sans(11), fill=BLACK)
for i, ln in enumerate(also_r):
    d.text((684, 590 + i * 23), ln, font=f_sans(11), fill=BLACK)

# ---------- DATE CHECK ----------
d.rectangle([8, 804, 1016, 860], outline=RED, width=2)
d.text((14, 808), "DATE CHECK", font=f_sans_b(13), fill=RED)
rt = "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY"
d.text((1016 - tw(rt, f_sans_b(10)) - 6, 810), rt, font=f_sans_b(10), fill=RED)
d.text((14, 826), "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU-Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
       font=f_sans(11), fill=BLACK)
d.text((14, 842), "NOT YET:  Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=f_sans(11), fill=BLACK)

# ---------- footer ----------
d.text((8, 866), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=f_sans(9), fill=GRAY)
d.text((8, 880), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
       font=f_sans(9), fill=GRAY)
d.text((8, 894), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=f_sans(9), fill=GRAY)

# ---------- bottom bar ----------
d.rectangle([0, 968, W, H], fill=BLACK)
bt = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
center(0, W, 990, bt, f_sans_b(15), GOLD)

img.save("entry.png")
print("saved entry.png", img.size)
