"""PEH Precision Point No. 007 - "Your horse's heels want the ground." dialogue
(Lauren = owner, gold; Jarnathan = sage, teal; eleven_v4).
Build stamp PP007-v1.0 (2026-10-25). Source: Moody, Curtis, Northrop & Martin, Front. Vet. Sci. 2026;13:1863433.
Visual recipe: hook = freeze frame (farrier at a shod hoof), callouts = source card + big-number card +
split bar comparison + branded hoof diagram (toe/heel lines) + equation, end card = blurred still of the last shot."""
import subprocess, os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

R = "/home/claude/pp7/"
B = R + "broll/"
T = R + "trim/"
F = "/home/claude/peh/assets/fonts/"
OUT = R + "build/"
os.makedirs(OUT, exist_ok=True)
STAMP = "PP007-v1.0"
NAME = "PP007_heels-want-the-ground_v1.0"
W, H, FPS = 1080, 1920, 30
GOLD, IVORY, TEAL, GREEN, INK = (201, 168, 106), (240, 232, 214), (46, 196, 182), (28, 52, 40), (16, 13, 9)
WHITE = (255, 255, 255)
font = lambda n, s: ImageFont.truetype(F + n, s)
LOGO = Image.open("/home/claude/peh/assets/PEH logo v2.png").convert("RGBA")
_px = LOGO.load()
for _y in range(LOGO.height):
    for _x in range(LOGO.width):
        r_, g_, b_, a_ = _px[_x, _y]
        if a_ and r_ > 235 and g_ > 235 and b_ > 235: _px[_x, _y] = (r_, g_, b_, 0)

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); raise SystemExit(cmd)

# ---------------- audio timeline ----------------
OWNER = {1, 3, 6, 8, 11, 13, 15}
dur = {}
for i in range(1, 17):
    r = subprocess.run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {T}l{i:02d}.wav', shell=True, capture_output=True, text=True)
    dur[i] = float(r.stdout.strip())
gap_after = {1: .45, 2: .4, 3: .45, 4: .4, 5: .5, 6: .4, 7: .5, 8: .4, 9: .45, 10: .65, 11: .4, 12: .5, 13: .4, 14: .6, 15: .4}
st, en = {}, {}
t = 0.6
for i in range(1, 17):
    st[i] = t; en[i] = t + dur[i]; t = en[i] + gap_after.get(i, 0)
END_START = st[16] - 0.1
TOTAL = en[16] + 2.3
print("starts", {k: round(v, 2) for k, v in st.items()}, "TOTAL", round(TOTAL, 2))

# ---------------- footage ----------------
fill = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
grade = ",eq=brightness=-0.03:saturation=0.95"
segs = []
def enc(name, src, ss, d, rate=1.0, pre="", extra=""):
    run(f'ffmpeg -v error -y -ss {ss} -t {d * rate + 0.3} -i "{src}" -an -vf "{pre}setpts=PTS/{rate},{fill}{grade}{extra},fps={FPS},setsar=1,format=yuv420p" -t {d} '
        f'-c:v libx264 -preset veryfast -crf 18 {OUT}{name}.mp4')
def freeze(name, src, at, d, pre=""):
    run(f'ffmpeg -v error -y -ss {at} -i "{src}" -frames:v 1 -vf "{pre}{fill}{grade}" {OUT}{name}.png')
    run(f'ffmpeg -v error -y -loop 1 -t {d} -i {OUT}{name}.png -vf "fps={FPS},setsar=1,format=yuv420p" -t {d} -c:v libx264 -preset veryfast -crf 18 {OUT}{name}.mp4')
cursor = 0.0
SHOTS = []   # (name, start, end, clip, ss, rate, note)
def shot(name, until, src, ss, rate=1.0, pre="", extra="", note=""):
    global cursor
    d = until - cursor
    enc(name, src, ss, d, rate, pre, extra); segs.append((name, cursor, d))
    SHOTS.append((name, cursor, until, os.path.basename(src), ss, rate, note)); cursor = until

FAR = B + "38300093.mp4"    # Jonathan Ellis - farrier in apron, horse's shod front foot between his knees, working the shoe (3840x2160)
BARE = B + "8625248.mp4"    # RDNE Stock project - unshod front hoof standing on sand, low side angle (1920x1080)
CARE = B + "8625401.mp4"    # RDNE Stock project - hands with a hoof brush on a lifted hoof (1280x720)
CHEST = B + "37061843.mp4"  # Joolsmagools - chestnut in a plaid blanket, head over the stall door, calm
BLAZE = B + "37046276.mp4"  # Joolsmagools - chestnut with a blaze over a stall wall, looking at camera
TRACK = B + "18138643.mp4"  # Sofi Verasaluse - racehorses with riders on a dirt training track
GREY = B + "18289246.mp4"   # Sofi Verasaluse - grey racehorse cantering on the dirt track
PADK = B + "27597794.mp4"   # The KRM - racehorse led around the paddock by a handler
GROOM = B + "35529058.mp4"  # İbrahim KARASU - racehorses with grooms in the paddock
HOOD = B + "27409126.mp4"   # The KRM - racehorse in a red hood walked in hand by a handler
PEER = B + "32979055.mp4"   # Ebahir - bay horse looking out of the stall door, still
PICK = B + "7881674.mp4"    # Barbara Olsen - woman holding up a front hoof and picking it out
cF = "crop=1215:2160:1250:0,"
cB = "crop=607:1080:1270:0,"
cC = "crop=405:720:430:0,"

# hook: freeze on the farrier at the shod hoof, then it moves
freeze("s00", FAR, 0.5, 0.9, pre=cF); segs.append(("s00", 0.0, 0.9)); SHOTS.append(("s00", 0.0, 0.9, "38300093.mp4", 0.5, "freeze", "hook freeze: farrier, shod front foot between his knees")); cursor = 0.9
shot("s01", st[1] + 2.45, FAR, 0.5, pre=cF, note="farrier works the shoe")                         # "Shoes came off in September."
shot("s02", st[1] + 4.61, BARE, 4.6, pre=cB, note="unshod front hoof standing on sand")             # "Now the heels look taller."
shot("s03", st[2], FAR, 4.0, pre=cF, note="farrier at the shod foot")                              # "What did my farrier do?"
shot("s04", st[3], CHEST, 3.0, note="chestnut in blanket, head over door")                           # "Probably nothing. The horse did it."
shot("s05", st[4], CARE, 2.0, pre=cC, note="lifted hoof, brush at the sole and heels")              # "Heels don't grow on their own."
shot("s06", st[5], TRACK, 0.3, note="racehorses on the dirt training track")                        # Frontiers... 36 racehorses
shot("s07", st[6], PADK, 4.0, note="racehorse walked in the paddock")                               # 23 barefoot / 13 shod / same trim
shot("s08", st[7], BLAZE, 1.0, note="blaze chestnut looking at camera")                             # "And?"
shot("s09", st[8], BARE, 4.6, rate=0.5, pre=cB, note="unshod hoof on sand, slow")                   # split bar
shot("s10", st[9], PEER, 2.0, note="bay looking out of the stall")                                  # "Five degrees sounds like nothing."
shot("s11", st[10], BARE, 2.4, pre=cB, extra=",boxblur=6:1,eq=brightness=-0.10", note="unshod hoof, softened under the diagram")   # hoof diagram
shot("s12", st[11], BARE, 0.6, rate=0.5, pre=cB, note="unshod front hoof stepping down onto sand, slow motion")      # aphorism + equation
shot("s13", st[12], FAR, 2.55, rate=0.65, pre=cF, note="farrier, shod foot")                       # "So I should pull everyone's shoes?"
shot("s14", st[12] + 5.90, HOOD, 0.0, rate=0.85, note="racehorse in a red hood walked in hand by a handler")                # trimmed every 30 days, never turned out
shot("s15", st[13], FAR, 5.8, rate=0.8, pre=cF, note="farrier finishing at the shoe")               # "shoes go back."
shot("s16", st[14], PICK, 1.0, note="woman holding up a front hoof, checking it")                   # "Then what do I actually check?"
shot("s17", st[15], PADK, 9.0, extra=",boxblur=6:1,eq=brightness=-0.10", note="paddock, softened under the diagram")  # side photo diagram
shot("s18", END_START, CHEST, 9.0, note="chestnut in blanket")                                      # "That was a little snack."

# end card: blurred still of the last shot
run(f'ffmpeg -v error -y -ss 12.0 -i "{CHEST}" -frames:v 1 -vf "{fill}" {OUT}end_src.png')
im = Image.open(OUT + "end_src.png").convert("RGB").filter(ImageFilter.GaussianBlur(26))
im = Image.blend(im, Image.new("RGB", (W, H), GREEN), 0.55); d = ImageDraw.Draw(im)
logo = LOGO.copy(); logo = logo.resize((360, int(360 * logo.height / logo.width)), Image.LANCZOS); im.paste(logo, ((W - logo.width) // 2, 300), logo)
def ctext(d, y, txt, f, fill, shadow=True):
    w = d.textlength(txt, font=f); x = (W - w) / 2
    assert w <= 960, txt
    if shadow: d.text((x + 3, y + 3), txt, font=f, fill=(0, 0, 0))
    d.text((x, y), txt, font=f, fill=fill)
ctext(d, 790, "PRECISION EQUINE HEALTH", font("CormorantGaramond-SemiBold.ttf", 66), GOLD)
ctext(d, 900, "Give the heels", font("CormorantGaramond-MediumItalic.ttf", 74), IVORY)
ctext(d, 985, "their ground.", font("CormorantGaramond-MediumItalic.ttf", 74), IVORY)
ctext(d, 1100, "We measure. Your veterinarian diagnoses.", font("CormorantGaramond-SemiBold.ttf", 58), TEAL)
ctext(d, 1215, "For the full meal, join the group", font("CormorantGaramond-SemiBold.ttf", 66), GOLD)
box_f = font("CormorantGaramond-Bold.ttf", 60); txt = "Precision Equine Health on Facebook"
tw = d.textlength(txt, font=box_f)
d.rounded_rectangle([(W - tw) / 2 - 40, 1320, (W + tw) / 2 + 40, 1430], 55, outline=GOLD, width=3)
d.text(((W - tw) / 2, 1340), txt, font=box_f, fill=IVORY)
im.save(OUT + "end.png")
ed = TOTAL - END_START
run(f'ffmpeg -v error -y -loop 1 -t {ed} -i {OUT}end.png -vf "fade=t=in:st=0:d=0.5,fps={FPS},setsar=1,format=yuv420p" -t {ed} -c:v libx264 -preset veryfast -crf 18 {OUT}s19.mp4')
segs.append(("s19", END_START, ed)); SHOTS.append(("s19", END_START, TOTAL, "end card", 0, 1, "blurred still of 37061843 + CTA"))

names = [s[0] for s in segs]
ins = " ".join(f"-i {OUT}{n}.mp4" for n in names)
run(f"ffmpeg -v error -y {ins} -filter_complex \"{''.join(f'[{i}:v]' for i in range(len(names)))}concat=n={len(names)}:v=1:a=0[v]\" -map [v] -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p {OUT}base.mp4")

# ---------------- overlays ----------------
ovs = []
def overlay(name, a, b, fn):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); fn(d, im)
    im.save(OUT + name + ".png"); ovs.append((OUT + name + ".png", a, b))

def chrome(d, im):
    f1, f2 = font("CormorantGaramond-Bold.ttf", 66), font("CormorantGaramond-SemiBold.ttf", 56)
    for i, t_ in enumerate(["YOUR HORSE’S HEELS", "WANT THE GROUND."]):
        w = d.textlength(t_, font=f1); y = 270 + i * 88
        assert 60 + w + 60 < 1020, t_
        d.rounded_rectangle([60, y, 60 + w + 60, y + 82], 14, fill=GREEN); d.text((90, y + 6), t_, font=f1, fill=IVORY)
    t2 = "PRECISION POINT · No. 007"; w2 = d.textlength(t2, font=f2)
    d.rounded_rectangle([60, 454, 60 + w2 + 50, 532], 10, fill=GOLD); d.text((85, 463), t2, font=f2, fill=GREEN)
overlay("chrome", 0, END_START, chrome)

def panel(d, y0, y1, x0=60, x1=W - 60, a=175): d.rounded_rectangle([x0, y0, x1, y1], 26, fill=(10, 10, 8, a))
def ltext(d, x, y, t_, f, fill): d.text((x + 3, y + 3), t_, font=f, fill=(0, 0, 0, 210)); d.text((x, y), t_, font=f, fill=fill)

def scrim(d, im):
    d.rounded_rectangle([40, 1080, 760, 1240], 22, fill=(10, 10, 8, 130))
    lg = LOGO.copy(); lg.thumbnail((130, 140)); im.paste(lg, (60, 1090), lg)
    d.text((200, 1096), "Precision Equine Health", font=font("CormorantGaramond-SemiBold.ttf", 60), fill=IVORY)
    d.text((200, 1166), "Measure the horse’s side.", font=font("CormorantGaramond-Italic.ttf", 56), fill=GOLD)

# captions (karaoke chunks): (line, start-in-line, end-in-line or None, text, key)
fCap = font("CormorantGaramond-Bold.ttf", 94)
def cap(txt, key, owner):
    acc = GOLD if owner else TEAL
    def fn(d, im):
        words = txt.split(); lines, cur = [], []
        for w_ in words:
            if d.textlength(" ".join(cur + [w_]), font=fCap) <= 960: cur.append(w_)
            else: lines.append(cur); cur = [w_]
        lines.append(cur)
        y = 1300 if len(lines) == 1 else 1255
        for ln in lines:
            x = (W - d.textlength(" ".join(ln), font=fCap)) / 2
            for w_ in ln:
                c = acc if key and w_ in key.split() else WHITE
                d.text((x + 4, y + 4), w_, font=fCap, fill=(0, 0, 0, 220)); d.text((x, y), w_, font=fCap, fill=c)
                x += d.textlength(w_ + " ", font=fCap)
            y += 100
    return fn
C = [  # line, a, b (None = line end), text, key
 (1, 0.00, 1.22, "Shoes came off", "Shoes"), (1, 1.22, 2.45, "in September.", "September."), (1, 2.45, 3.39, "Now the heels", "heels"), (1, 3.39, 4.61, "look taller.", "taller."), (1, 4.61, None, "What did my farrier do?", "farrier"),
 (2, 0.00, 1.40, "Probably nothing.", "nothing."), (2, 1.40, None, "The horse did it.", "horse"),
 (3, 0.00, 0.95, "Heels don’t grow", "Heels"), (3, 0.95, None, "on their own.", "own."),
 (4, 0.00, 1.22, "They do.", "do."),
 (4, 4.70, 5.75, "Thirty-six racehorses", "Thirty-six"), (4, 5.75, None, "in full training.", "training."),
 (6, 0.00, None, "And?", "And?"),
 (8, 0.00, 0.80, "Five degrees", "Five"), (8, 0.80, None, "sounds like nothing.", "nothing."),
 (11, 0.00, 0.80, "So I should", ""), (11, 0.80, None, "pull everyone’s shoes?", "shoes?"),
 (12, 0.00, 0.95, "No.", "No."), (12, 0.95, 2.79, "Trimmed every thirty days,", "thirty"), (12, 2.79, 4.27, "never turned out.", "never"),
 (12, 4.27, 6.18, "If wear outruns growth,", "wear"), (12, 6.18, None, "shoes go back.", "back."),
 (13, 0.00, 0.95, "Then what do I", ""), (13, 0.95, None, "actually check?", "check?"),
 (15, 0.00, None, "That was a little snack.", "snack."),
]
for k, (ln, a, b, txt, key) in enumerate(C):
    A = st[ln] + a; Bv = (st[ln] + b) if b is not None else en[ln] + 0.12
    overlay(f"cap{k:02d}", A, Bv, cap(txt, key, ln in OWNER))

fB = font("CormorantGaramond-Bold.ttf", 96); fS = font("CormorantGaramond-SemiBold.ttf", 68)
# source card (line 4, Frontiers... out this month)
def source(d, im):
    panel(d, 1060, 1440)
    ctext(d, 1085, "Frontiers in", font("CormorantGaramond-BoldItalic.ttf", 92), IVORY, False)
    ctext(d, 1185, "Veterinary Science", font("CormorantGaramond-BoldItalic.ttf", 92), IVORY, False)
    ctext(d, 1310, "October 2026", fS, GOLD, False)
overlay("source", st[4] + 1.22, st[4] + 4.70, source)

# big-number card (line 5)
def groups(n):
    def fn(d, im):
        panel(d, 1040, 1560 if n == 3 else (1400 if n == 2 else 1260))
        ctext(d, 1060, "23 BAREFOOT · 90 DAYS", font("CormorantGaramond-Bold.ttf", 84), TEAL, False)
        if n >= 2: ctext(d, 1180, "13 STAYED SHOD", font("CormorantGaramond-Bold.ttf", 84), GOLD, False)
        if n >= 3:
            ctext(d, 1310, "same farrier", fS, IVORY, False)
            ctext(d, 1400, "same 30-day trim", fS, IVORY, False)
    return fn
overlay("grp1", st[5], st[5] + 3.17, groups(1)); overlay("grp2", st[5] + 3.17, st[5] + 5.07, groups(2)); overlay("grp3", st[5] + 5.07, st[6], groups(3))

# split bar comparison (line 7)
def bars(n):
    def fn(d, im):
        panel(d, 960, 1600)
        ctext(d, 980, "HEEL ANGLE · 90 DAYS", font("CormorantGaramond-Bold.ttf", 74), IVORY, False)
        x0, scale = 130, 22.0       # px per degree
        rows = [("BAREFOOT", 29.97, 34.62, TEAL, "30° → 35°"), ("SHOD", 27.84, 28.00, GOLD, "28° → 28°")]
        for j, (lab, a_, b_, col, txt) in enumerate(rows[:n]):
            y = 1090 + j * 250
            ltext(d, x0, y, lab, font("CormorantGaramond-Bold.ttf", 64), col)
            d.rounded_rectangle([x0, y + 90, x0 + a_ * scale, y + 150], 10, fill=(240, 232, 214, 110))
            d.rounded_rectangle([x0, y + 90, x0 + b_ * scale, y + 150], 10, outline=col, width=6)
            if b_ - a_ > 1: d.rounded_rectangle([x0 + a_ * scale, y + 90, x0 + b_ * scale, y + 150], 6, fill=col)
            ltext(d, x0 + 400, y - 2, txt, font("CormorantGaramond-Bold.ttf", 72), col)
    return fn
overlay("bar1", st[7], st[7] + 4.99, bars(1)); overlay("bar2", st[7] + 4.99, st[8], bars(2))

# branded hoof diagram: side view, toe to the right; toe line at 51 deg, heel line at 30 deg
import math
def hoof(d, ox, gy, toe_lbl, heel_lbl, heel_hi=False, gap=False):
    pt = lambda x, y, ang, L: (x - L * math.cos(math.radians(ang)), y - L * math.sin(math.radians(ang)))
    def bez(p0, p1, p2, n=24):
        return [((1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0], (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]) for t in [i/n for i in range(n+1)]]
    hc = TEAL if heel_hi else IVORY
    tx, hx = ox + 300, ox - 40                       # toe and heel ground contact
    Lt, Lh = 300, 190
    C = pt(tx, gy, 51, Lt)                           # coronet at the toe
    Ht = pt(hx, gy, 30, Lh)                          # heel buttress top, where the bulb begins
    corB = (Ht[0] + 10, Ht[1] - 45)                  # coronet above the heel bulb
    coronet = bez(C, (C[0] - 170, C[1] + 10), corB)
    bulb = bez(corB, (Ht[0] - 70, Ht[1] - 40), Ht)   # heel bulb bulging behind the heel
    capsule = [(tx, gy)] + coronet + bulb[1:] + [(hx, gy)]
    d.polygon(capsule, fill=(240, 232, 214, 55))
    d.line(capsule + [(tx, gy)], fill=IVORY, width=5, joint="curve")
    d.line([(ox - 330, gy), (ox + 420, gy)], fill=(240, 232, 214, 160), width=4)            # ground
    # toe line along the dorsal wall, heel line along the heel wall, both extended
    d.line([(tx, gy), pt(tx, gy, 51, Lt + 70)], fill=GOLD, width=9)
    d.line([(hx, gy), pt(hx, gy, 30, Lh + 90)], fill=hc, width=9)
    d.arc([tx - 90, gy - 90, tx + 90, gy + 90], 180, 231, fill=GOLD, width=5)
    d.arc([hx - 90, gy - 90, hx + 90, gy + 90], 180, 210, fill=hc, width=5)
    fL = font("CormorantGaramond-Bold.ttf", 62)
    ltext(d, min(tx - 100, 1000 - d.textlength(toe_lbl, font=fL)), C[1] - 110, toe_lbl, fL, GOLD)
    ltext(d, ox - 330, gy + 30, heel_lbl, fL, hc)
    if gap:   # bracket between the two angle lines
        d.arc([hx - 160, gy - 160, hx + 160, gy + 160], 210, 231, fill=GOLD, width=4)
    return C, Ht
def diagram(stage):
    def fn(d, im):
        panel(d, 720, 1560)
        ctext(d, 745, "SIDE VIEW · FRONT HOOF", font("CormorantGaramond-Bold.ttf", 66), IVORY, False)
        if stage in (1, 2):
            hoof(d, 520, 1300, "TOE 51° → 51°", "HEEL 30° → 35°" if stage == 2 else "HEEL", heel_hi=stage == 2)
            ctext(d, 1440, "the front held · the back stood up" if stage == 2 else "the front held", fS, GOLD if stage == 1 else TEAL, False)
        else:
            hoof(d, 520, 1300, "TOE ANGLE", "HEEL ANGLE", heel_hi=True, gap=stage == 4)
            if stage == 3: ctext(d, 1440, "side photo · same spot · every trim", fS, GOLD, False)
            else: ctext(d, 1440, "watch the gap close", font("CormorantGaramond-Bold.ttf", 84), TEAL, False)
    return fn
overlay("dia1", st[9], st[9] + 2.35, diagram(1)); overlay("dia2", st[9] + 2.35, st[10], diagram(2))
overlay("dia3", st[14], st[14] + 5.29, diagram(3)); overlay("dia4", st[14] + 5.29, st[15], diagram(4))

# equation (line 10)
def eq(d, im):
    panel(d, 600, 1140)
    ctext(d, 625, "HEELS ON THE GROUND", font("CormorantGaramond-Bold.ttf", 78), GOLD, False)
    ctext(d, 740, "+ 90 DAYS", font("CormorantGaramond-Bold.ttf", 100), IVORY, False)
    ctext(d, 870, "=", font("CormorantGaramond-Bold.ttf", 100), IVORY, False)
    ctext(d, 985, "HEELS THAT STAND UP", font("CormorantGaramond-Bold.ttf", 78), TEAL, False)
overlay("eq", st[10], st[11], eq)

# logo scrim only where no callout is up
busy = [(st[4] + 1.22, st[4] + 4.70), (st[5], st[6]), (st[7], st[8]), (st[9], st[11]), (st[14], st[15])]
free = []
a = 0.0
for b0, b1 in busy + [(END_START, END_START)]:
    if b0 - a > 1.0: free.append((a, b0))
    a = b1
for i, (a, b) in enumerate(free): overlay(f"scrim{i}", a, b, scrim)

for p, a, b in ovs:
    bbox = Image.open(p).getbbox()
    if bbox and (bbox[2] > 1050 or bbox[0] < 30): print("EDGE", p, bbox)

# ---------------- audio ----------------
ains = " ".join(f"-i {T}l{i:02d}.wav" for i in range(1, 17))
af = ";".join(f"[{i - 1}:a]adelay={int(st[i] * 1000)}|{int(st[i] * 1000)}[a{i}]" for i in range(1, 17))
af += ";" + "".join(f"[a{i}]" for i in range(1, 17)) + f"amix=inputs=16:normalize=0,apad,atrim=0:{TOTAL}[vo]"
run(f'ffmpeg -v error -y {ains} -filter_complex "{af}" -map "[vo]" -ar 44100 {R}vo.wav')

inputs = " ".join(f'-i "{p}"' for p, _, _ in ovs)
chain, last = [], "0:v"
for i, (p, a, b) in enumerate(ovs):
    nl = f"v{i}"; chain.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{a:.2f},{b - 0.04:.2f})'[{nl}]"); last = nl
na = len(ovs) + 1
fc = ";".join(chain) + (
    f";[{na}:a]volume=1.0,apad,atrim=0:{TOTAL}[vo]"
    f";[{na + 1}:a]volume=0.11,afade=t=out:st={TOTAL - 2.4}:d=2.2,atrim=0:{TOTAL}[mus]"
    f";[vo][mus]amix=inputs=2:duration=longest:normalize=0,atrim=0:{TOTAL}[aout]")
open(OUT + "fc.txt", "w").write(fc)
run(f'ffmpeg -v error -y -i {OUT}base.mp4 {inputs} -i {R}vo.wav -stream_loop -1 -i {R}music.mp3 '
    f'-filter_complex_script {OUT}fc.txt -map "[{last}]" -map "[aout]" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p '
    f'-r {FPS} -c:a aac -b:a 160k -movflags +faststart -metadata comment="{STAMP}" -t {TOTAL} {R}{NAME}_master.mp4')
json.dump({"segs": segs, "shots": SHOTS, "st": st, "en": en, "END_START": END_START, "TOTAL": TOTAL, "stamp": STAMP}, open(OUT + "timing.json", "w"), indent=1)
print("done", round(TOTAL, 2))
