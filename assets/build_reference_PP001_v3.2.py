"""PEH Precision Point No. 001 - v3 dialogue (Lauren x Flint), karaoke overlay layout.
Build stamp PP001-v3.2 (logo v2, no speaker pills)"""
import subprocess, os, json
from PIL import Image, ImageDraw, ImageFont

S = "/mnt/user-data/uploads/Desktop/Precision Equine/"
P = S + "Social Media /Fischer and Paige/"
B = "/home/claude/reel/broll/"
F = "/home/claude/fb/font/static/"
R = "/home/claude/reel3/"
OUT = R + "build3/"
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
GOLD, IVORY, TEAL, GREEN, INK = (201, 168, 106), (240, 232, 214), (46, 196, 182), (28, 52, 40), (16, 13, 9)
WHITE = (255, 255, 255)
font = lambda n, s: ImageFont.truetype(F + n, s)
LOGO = Image.open(R + "logo_v2.png").convert("RGBA")
_px = LOGO.load()
for _y in range(LOGO.height):
    for _x in range(LOGO.width):
        r_, g_, b_, a_ = _px[_x, _y]
        if a_ and r_ > 235 and g_ > 235 and b_ > 235: _px[_x, _y] = (r_, g_, b_, 0)

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); raise SystemExit(cmd)

# ---------------- audio timeline ----------------
dur = {}
for i in range(1, 15):
    r = subprocess.run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {R}trim/l{i:02d}.wav', shell=True, capture_output=True, text=True)
    dur[i] = float(r.stdout.strip())
gap_after = {1: .4, 2: .5, 3: .4, 4: .5, 5: .4, 6: .6, 7: .4, 8: .6, 9: .4, 10: .7, 11: 2.5, 12: .9, 13: .4}
st, en = {}, {}
t = 0.3
for i in range(1, 15):
    st[i] = t; en[i] = t + dur[i]; t = en[i] + gap_after.get(i, 0)
END_START = st[14] - 0.15            # end card comes in just before Flint's last line
TOTAL = en[14] + 2.4
print("line starts", {k: round(v, 2) for k, v in st.items()}, "TOTAL", round(TOTAL, 2))

# ---------------- base footage ----------------
fill = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
grade = ",eq=brightness=-0.03:saturation=0.95"
segs = []   # (name, abs_start, dur)
def seg_play(name, src, ss, d, rate=1.0):
    """rate<1 = slow motion, >1 = fast."""
    src_d = d * rate
    run(f'ffmpeg -v error -y -ss {ss} -t {src_d + 0.2} -i "{src}" -an -vf "setpts=PTS/{rate},{fill}{grade},fps={FPS},format=yuv420p" -t {d} '
        f'-c:v libx264 -preset veryfast -crf 18 {OUT}{name}.mp4')
def seg_freeze(name, src, at, d):
    run(f'ffmpeg -v error -y -ss {at} -i "{src}" -frames:v 1 -vf "{fill}{grade}" {OUT}{name}.png')
    run(f'ffmpeg -v error -y -loop 1 -t {d} -i {OUT}{name}.png -vf "fps={FPS},format=yuv420p" -t {d} -c:v libx264 -preset veryfast -crf 18 {OUT}{name}.mp4')

cursor = 0.0
def shot(name, until, kind, src, ss, rate=1.0):
    global cursor
    d = until - cursor
    if d <= 0.05: return
    if kind == "play": seg_play(name, src, ss, d, rate)
    else: seg_freeze(name, src, ss, d)
    segs.append((name, cursor, d)); cursor = until

EC, EA, EB = B + "eating_c.mp4", B + "eating_a.mp4", B + "eating_b.mp4"
TIGER = S + "thank you Tiger.MOV"
shot("s00", 0.9,            "freeze", EC, 2.0)                 # hook: freeze mid-bite
shot("s01", st[2],          "play",   EC, 2.0)                 # ...then it moves
shot("s02", st[3],          "play",   B + "stall_door2.mp4", 0.5)   # horse looks out: reviewing the menu
shot("s03", st[4],          "play",   EC, 8.0)                 # "Reviewing?" sly look
shot("s04", st[4] + 4.34,   "play",   B + "hay_pen2.mp4", 1.0)      # built to graze
shot("s05", st[4] + 7.21,   "play",   EB, 3.0, rate=0.5)       # grain, slow motion
shot("s06", st[5],          "play",   EA, 1.0)                 # ...and a wall
shot("s07", st[6],          "play",   B + "feeding_closeup.mp4", 2.0)  # "It's good grain."
shot("s08", st[6] + 2.79,   "play",   B + "fence_horses.mp4", 3.0)    # path away from nature
shot("s09", st[7],          "play",   EA, 4.0)                 # 5x callout over wood chewing
shot("s10", st[8],          "play",   B + "hay_pen.mp4", 3.0)  # more hay?
shot("s11", st[8] + 1.0,    "play",   P + "IMG_7468.MOV", 0.3, rate=0.5)   # more work: speed ramp (slow)
shot("s12", st[8] + 1.61,   "play",   P + "IMG_7468.MOV", 0.8, rate=1.6)   # ...then fast
shot("s13", st[8] + 6.45,   "play",   P + "IMG_7461.MOV", 7.0)  # morning in the ring (Pro's footage)
shot("s14", st[9],          "play",   B + "hay_pen2.mp4", 6.5)      # tired horse is a polite horse (calm, eating)
shot("s15", st[10],         "play",   EC, 5.0)                 # blame boredom (sheepish)
shot("s16", st[11],         "play",   B + "stable_horse.mp4", 2.0)  # menu + calendar checklist
shot("s17", st[11] + 4.8,   "play",   TIGER, 4.5)              # new tastes? ... Tiger nuzzle
shot("s18", st[13],         "freeze", TIGER, 9.3)              # freeze on the lick: there are always options
shot("s19", END_START,      "play",   TIGER, 10.4)             # that was a little snack (smile)

# end card
im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im)
horse = Image.open(S + "great1.png").convert("RGB").resize((W, W))
m = Image.new("L", (W, W), 0); md = ImageDraw.Draw(m)
for yy in range(W): md.line([(0, yy), (W, yy)], fill=int(150 * (1 - yy / W)))
im.paste(horse, (0, 0), m)
logo = LOGO.copy(); logo = logo.resize((360, int(360 * logo.height / logo.width)), Image.LANCZOS); im.paste(logo, ((W - logo.width) // 2, 300), logo)
def ctext(d, y, txt, f, fill, shadow=True):
    w = d.textlength(txt, font=f); x = (W - w) / 2
    if shadow: d.text((x + 3, y + 3), txt, font=f, fill=(0, 0, 0, 210))
    d.text((x, y), txt, font=f, fill=fill)
ctext(d, 810, "PRECISION EQUINE HEALTH", font("CormorantGaramond-SemiBold.ttf", 66), GOLD)
ctext(d, 920, "That was a little snack.", font("CormorantGaramond-MediumItalic.ttf", 72), IVORY)
ctext(d, 1050, "For the full meal,", font("CormorantGaramond-SemiBold.ttf", 68), GOLD)
ctext(d, 1130, "join the private group", font("CormorantGaramond-SemiBold.ttf", 68), GOLD)
box_f = font("CormorantGaramond-Bold.ttf", 60); txt = "Precision Equine Health on Facebook"
tw = d.textlength(txt, font=box_f)
d.rounded_rectangle([(W - tw) / 2 - 40, 1240, (W + tw) / 2 + 40, 1350], 55, outline=GOLD, width=3)
d.text(((W - tw) / 2, 1260), txt, font=box_f, fill=IVORY)
im.save(OUT + "end.png")
ed = TOTAL - END_START
run(f'ffmpeg -v error -y -loop 1 -t {ed} -i {OUT}end.png -vf "fade=t=in:st=0:d=0.5,fps={FPS},format=yuv420p" -t {ed} -c:v libx264 -preset veryfast -crf 18 {OUT}s20.mp4')
segs.append(("s20", END_START, ed))

names = [s[0] for s in segs]
ins = " ".join(f"-i {OUT}{n}.mp4" for n in names)
run(f"ffmpeg -v error -y {ins} -filter_complex \"{''.join(f'[{i}:v]' for i in range(len(names)))}concat=n={len(names)}:v=1:a=0[v]\" -map [v] -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p {OUT}base.mp4")

# ---------------- overlays ----------------
ovs = []
def overlay(name, a, b, fn):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); fn(d, im)
    im.save(OUT + name + ".png"); ovs.append((OUT + name + ".png", a, b))

# persistent chrome: title tag + logo scrim
def chrome(d, im):
    f1, f2 = font("CormorantGaramond-Bold.ttf", 64), font("CormorantGaramond-SemiBold.ttf", 56)
    for i, t in enumerate(["READ THE STALL,", "LEARN THE HORSE"]):
        w = d.textlength(t, font=f1); y = 270 + i * 86
        d.rounded_rectangle([60, y, 60 + w + 60, y + 80], 14, fill=GREEN); d.text((90, y + 6), t, font=f1, fill=IVORY)
    t2 = "PRECISION POINT · No. 001"; w2 = d.textlength(t2, font=f2)
    d.rounded_rectangle([60, 450, 60 + w2 + 50, 528], 10, fill=GOLD); d.text((85, 459), t2, font=f2, fill=GREEN)
    d.rounded_rectangle([40, 1080, 760, 1240], 22, fill=(10, 10, 8, 130))
    logo = LOGO.copy(); logo.thumbnail((130, 140))
    im.paste(logo, (60, 1090), logo)
    d.text((200, 1096), "Precision Equine Health", font=font("CormorantGaramond-SemiBold.ttf", 60), fill=IVORY)
    d.text((200, 1166), "Hear the horse’s side.", font=font("CormorantGaramond-Italic.ttf", 56), fill=GOLD)
overlay("chrome", 0, END_START, chrome)

# karaoke captions: (line, speaker, [(t0, t1, text, keyword)]) times local to the trimmed line
L, Fl = "LAUREN", "FLINT"
caps = [
    (1, L, [(0, 0.95, "My horse is", ""), (0.95, dur[1], "eating the stall.", "eating")]),
    (2, Fl, [(0, 0.9, "No.", "No."), (0.9, 1.85, "Your horse is", ""), (1.85, dur[2], "reviewing the menu.", "menu.")]),
    (3, L, [(0, dur[3], "Reviewing?", "Reviewing?")]),
    (4, Fl, [(0, 2.0, "A horse is built to graze", "graze"), (2.0, 4.0, "eighteen hours a day.", "eighteen hours"),
             (4.2, 5.3, "You gave him", ""), (5.3, 7.0, "twenty minutes of grain…", "twenty minutes"), (7.1, dur[4], "and a wall.", "wall.")]),
    (5, L, [(0, dur[5], "It’s good grain.", "good")]),
    (6, Fl, [(0, 2.6, "A path away from nature.", "nature.")]),
    (7, L, [(0, dur[7], "So… more hay?", "more hay?")]),
    (8, Fl, [(0, 1.5, "And more work.", "work."), (1.55, 3.2, "A morning in the ring", "ring"), (3.2, 4.15, "and the chewing drops", "drops"),
             (6.4, 7.9, "A tired horse", "tired"), (7.9, dur[8], "is a polite horse.", "polite")]),
    (9, L, [(0, 1.15, "I was about to", ""), (1.15, dur[9], "blame boredom.", "boredom.")]),
    (10, Fl, [(0, 1.45, "Everybody does.", "Everybody")]),
    (11, L, [(0, 1.95, "And if he’s developed…", "developed…"), (1.95, dur[11], "new tastes?", "new tastes?")]),
    (12, Fl, [(0, dur[12] + 0.5, "There are always options.", "options.")]),
]
fCap = font("CormorantGaramond-Bold.ttf", 94); fTag = font("CormorantGaramond-SemiBold.ttf", 56)
def cap(speaker, txt, key):
    def fn(d, im):
        col_key = TEAL if speaker == Fl else GOLD
        words = txt.split(); lines, cur = [], []
        for w_ in words:
            tt = " ".join(cur + [w_])
            if d.textlength(tt, font=fCap) <= 960: cur.append(w_)
            else: lines.append(cur); cur = [w_]
        lines.append(cur)
        y = 1300 if len(lines) == 1 else 1255
        for ln in lines:
            full = " ".join(ln); x = (W - d.textlength(full, font=fCap)) / 2
            for w_ in ln:
                c = col_key if key and w_ in key.split() else WHITE
                d.text((x + 4, y + 4), w_, font=fCap, fill=(0, 0, 0, 220)); d.text((x, y), w_, font=fCap, fill=c)
                x += d.textlength(w_ + " ", font=fCap)
            y += 100
    return fn
k = 0
for ln, sp, chunks in caps:
    for j, (a, b, txt, key) in enumerate(chunks):
        tail = 0.12 if j == len(chunks) - 1 else 0.0
        overlay(f"cap{k}", st[ln] + a, st[ln] + b + tail, cap(sp, txt, key)); k += 1

# punctuated graphics (each replaces the caption while up)
def five(d, im):
    fc, fs, fi = font("CormorantGaramond-Bold.ttf", 190), font("CormorantGaramond-SemiBold.ttf", 68), font("CormorantGaramond-Italic.ttf", 56)
    d.rounded_rectangle([60, 640, W - 60, 1050], 26, fill=(10, 10, 8, 165))
    ctext(d, 630, "5×", fc, TEAL, False)
    ctext(d, 860, "more wood chewing on grain", fs, IVORY, False)
    ctext(d, 950, "Journal of Animal Science", fi, GOLD, False)
overlay("five", st[6] + 2.75, en[6] + 0.3, five)

def drops(d, im):
    f1, fs = font("CormorantGaramond-Bold.ttf", 120), font("CormorantGaramond-SemiBold.ttf", 64)
    d.rounded_rectangle([60, 690, W - 60, 1050], 26, fill=(10, 10, 8, 165))
    ctext(d, 700, "minutes  →  seconds", f1, TEAL, False)
    ctext(d, 860, "of wood chewing", fs, IVORY, False)
    ctext(d, 940, "after a morning’s work", fs, IVORY, False)
overlay("drops", st[8] + 4.15, st[8] + 6.35, drops)

items = ["The menu", "The calendar"]
for n in range(2):
    def chk(d, im, n=n):
        f1 = font("CormorantGaramond-Bold.ttf", 94)
        d.rounded_rectangle([90, 730, W - 90, 1010], 26, fill=(10, 10, 8, 165))
        for j in range(n + 1):
            y = 770 + 120 * j
            d.rounded_rectangle([150, y + 10, 220, y + 80], 12, outline=TEAL, width=6)
            d.line([(165, y + 46), (185, y + 66), (210, y + 24)], fill=TEAL, width=8)
            d.text((260, y - 2), items[j], font=f1, fill=IVORY)
    overlay(f"chk{n}", st[10] + [1.45, 2.5][n], st[10] + [2.5, dur[10] + 0.5][n], chk)

def snackline(d, im):
    pass
# ---------------- final mux ----------------
inputs = " ".join(f'-i "{p}"' for p, _, _ in ovs)
chain, last = [], "0:v"
for i, (p, a, b) in enumerate(ovs):
    nl = f"v{i}"; chain.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{a:.2f},{b - 0.04:.2f})'[{nl}]"); last = nl
na = len(ovs) + 1
vo_in = " ".join(f"-i {R}trim/l{i:02d}.wav" for i in range(1, 15))
vo_chain = ";".join(f"[{na + i - 1}:a]adelay={int(st[i]*1000)}:all=1[d{i}]" for i in range(1, 15))
vo_mix = "".join(f"[d{i}]" for i in range(1, 15)) + "amix=inputs=14:normalize=0,volume=1.0[vo]"
mi = na + 14
fc = ";".join(chain) + ";" + vo_chain + ";" + vo_mix + (
    f";[{mi}:a]volume=0.11,afade=t=out:st={TOTAL - 2.4}:d=2.2,atrim=0:{TOTAL}[mus]"
    f";[vo][mus]amix=inputs=2:duration=longest:normalize=0,atrim=0:{TOTAL}[aout]")
run(f'ffmpeg -v error -y -i {OUT}base.mp4 {inputs} {vo_in} -stream_loop -1 -i /home/claude/reel/music.mp3 '
    f'-filter_complex "{fc}" -map "[{last}]" -map "[aout]" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p '
    f'-r {FPS} -c:a aac -b:a 160k -movflags +faststart -t {TOTAL} {R}PP001_read-the-stall_v3.2.mp4')
json.dump({"st": st, "en": en, "END_START": END_START, "TOTAL": TOTAL}, open(OUT + "timing.json", "w"), indent=1)
print("done", round(TOTAL, 2))
