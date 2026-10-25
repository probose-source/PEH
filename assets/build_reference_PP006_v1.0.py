"""PEH Precision Point No. 006 - "Why do white pasterns get scratches easily?" monologue (Jarnathan, eleven_v4).
Build stamp PP006-v1.0 (2026-10-24). Visual recipe: hook = speed ramp (0.5x -> 1.6x),
callouts = counting tally (plants) + circled detail on a freeze + checklist + building equation,
end card = plain brand field."""
import subprocess, os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

R = "/home/claude/pp006/"
B = R + "broll/"
F = "/home/claude/peh/assets/fonts/"
OUT = R + "build/"
os.makedirs(OUT, exist_ok=True)
STAMP = "PP006-v1.0"
NAME = "PP006_white-pasterns_v1.0"
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

VO_LEN = 48.24
END_START = 44.87      # end card under "Read the horse's side of the story... in the white socks."
TOTAL = VO_LEN + 2.4

fill = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
grade = ",eq=brightness=-0.03:saturation=0.95"
segs = []
def enc(name, src, ss, d, rate=1.0, pre=""):
    run(f'ffmpeg -v error -y -ss {ss} -t {d * rate + 0.3} -i "{src}" -an -vf "{pre}setpts=PTS/{rate},{fill}{grade},fps={FPS},format=yuv420p" -t {d} '
        f'-c:v libx264 -preset veryfast -crf 18 {OUT}{name}.mp4')
cursor = 0.0
def shot(name, until, src, ss, rate=1.0, pre=""):
    global cursor
    d = until - cursor
    enc(name, src, ss, d, rate, pre); segs.append((name, cursor, d)); cursor = until

HAF1 = B + "12321350.mp4"   # Brixiv - chestnut draft, flaxen mane, white lower legs, grazing in a sunny paddock (1920x1080)
HAF2 = B + "12320486.mp4"   # Brixiv - same horse, second take
CLOV = B + "11575736.mp4"   # Hom Tamang - clover heads close-up in a meadow
GRAZ = B + "5087755.mp4"    # Tima Miroshnichenko - bay grazing, muzzle in the grass, close
YOUNG = B + "13068631.mp4"  # Dmitry Marchenkov - young horses at a paddock fence; chestnut with white hind pasterns
WALK = B + "8624794.mp4"    # RDNE Stock project - woman leading a horse in a sand pen
STALL = B + "7671485.mp4"   # Anastasia Shuraeva - chestnut with a blaze, head over the stall door, calm
CLOV2 = B + "8745474.mp4"   # Roman Odintsov - clover heads at dusk
cx = lambda x: f"crop=607:1080:{x}:0,"

# s01 hook: speed ramp on the white legs + grazing head (0.5x then 1.6x)
enc("s01a", HAF1, 9.0, 2.0, rate=0.5, pre=cx(500)); enc("s01b", HAF1, 10.0, 1.62, rate=1.6, pre=cx(500))
segs += [("s01a", 0.0, 2.0), ("s01b", 2.0, 1.62)]; cursor = 3.62
shot("s02", 6.13, HAF2, 2.0, pre=cx(150))          # check the pasture before the leg: head in the grass, front legs
shot("s03", 9.94, CLOV, 0.0)                        # plant tally over clover heads
shot("s04", 12.70, GRAZ, 0.8)                       # eaten: muzzle in the grass
shot("s05", 14.85, HAF1, 27.0, pre=cx(820))         # sunlight: sunlit barrel and white hind legs
# s06 freeze with circled pastern: sharp 1080-wide panel on a blurred field
run(f'ffmpeg -v error -y -ss 5.0 -i "{HAF1}" -frames:v 1 {OUT}fz_src.png')
src = Image.open(OUT + "fz_src.png").convert("RGB")
bg = src.resize((3413, 1920)).crop((1166, 0, 2246, 1920)).filter(ImageFilter.GaussianBlur(30))
bg = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.45)
panel = src.crop((300, 0, 1380, 1080))
bg.paste(panel, (0, 420)); bg.save(OUT + "fz.png")
PAST = (950 - 300, 905 + 420)   # near fore pastern on the panel
shot_d = 20.05 - 14.85
run(f'ffmpeg -v error -y -loop 1 -t {shot_d} -i {OUT}fz.png -vf "eq=brightness=-0.03:saturation=0.95,fps={FPS},format=yuv420p" -t {shot_d} -c:v libx264 -preset veryfast -crf 18 {OUT}s06.mp4')
segs.append(("s06", 14.85, shot_d)); cursor = 20.05
shot("s07", 23.79, YOUNG, 0.0)                      # Swiss vets, young horses
shot("s08", 27.11, HAF2, 10.0, pre=cx(700))         # white pasterns flared more often: white legs in the grass
d9 = 31.99 - cursor
run(f'ffmpeg -v error -y -ss 18.2 -t {d9 + 0.3} -i "{YOUNG}" -an -filter_complex "[0:v]split[a][b];[a]{fill},boxblur=30:3,eq=brightness=-0.12:saturation=0.9[bg];[b]crop=720:640:0:480,scale=1080:960{grade}[fg];[bg][fg]overlay=0:470,fps={FPS},format=yuv420p" -t {d9} -c:v libx264 -preset veryfast -crf 18 {OUT}s09.mp4')
segs.append(("s09", cursor, d9)); cursor = 31.99                      # same horse, only the white legs: chestnut with white hind pasterns, chestnut front legs (checked at 19.5 s)
shot("s10", 38.31, WALK, 0.0)                       # walk the paddocks with your barn manager
shot("s11", 41.92, STALL, 2.0)                      # bring the pattern to your vet
shot("s12", END_START, CLOV2, 2.0)                  # clover + sun + pink skin

# end card: plain brand field
im = Image.new("RGB", (W, H), GREEN); d = ImageDraw.Draw(im)
logo = LOGO.copy(); logo = logo.resize((360, int(360 * logo.height / logo.width)), Image.LANCZOS); im.paste(logo, ((W - logo.width) // 2, 300), logo)
def ctext(d, y, txt, f, fill, shadow=True):
    w = d.textlength(txt, font=f); x = (W - w) / 2
    if shadow: d.text((x + 3, y + 3), txt, font=f, fill=(0, 0, 0))
    d.text((x, y), txt, font=f, fill=fill)
ctext(d, 790, "PRECISION EQUINE HEALTH", font("CormorantGaramond-SemiBold.ttf", 66), GOLD)
ctext(d, 900, "Read the horse’s side of the story", font("CormorantGaramond-MediumItalic.ttf", 70), IVORY)
ctext(d, 985, "in the white socks.", font("CormorantGaramond-MediumItalic.ttf", 70), IVORY)
ctext(d, 1100, "We measure. Your veterinarian diagnoses.", font("CormorantGaramond-SemiBold.ttf", 58), TEAL, False)
ctext(d, 1215, "For more, join the private group", font("CormorantGaramond-SemiBold.ttf", 68), GOLD)
box_f = font("CormorantGaramond-Bold.ttf", 60); txt = "Precision Equine Health on Facebook"
tw = d.textlength(txt, font=box_f)
d.rounded_rectangle([(W - tw) / 2 - 40, 1320, (W + tw) / 2 + 40, 1430], 55, outline=GOLD, width=3)
d.text(((W - tw) / 2, 1340), txt, font=box_f, fill=IVORY)
im.save(OUT + "end.png")
ed = TOTAL - END_START
run(f'ffmpeg -v error -y -loop 1 -t {ed} -i {OUT}end.png -vf "fade=t=in:st=0:d=0.5,fps={FPS},format=yuv420p" -t {ed} -c:v libx264 -preset veryfast -crf 18 {OUT}s13.mp4')
segs.append(("s13", END_START, ed))

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
    for i, t in enumerate(["WHY DO WHITE PASTERNS", "GET SCRATCHES EASILY?"]):
        w = d.textlength(t, font=f1); y = 270 + i * 88
        assert 60 + w + 60 < 1020, t
        d.rounded_rectangle([60, y, 60 + w + 60, y + 82], 14, fill=GREEN); d.text((90, y + 6), t, font=f1, fill=IVORY)
    t2 = "PRECISION POINT · No. 006"; w2 = d.textlength(t2, font=f2)
    d.rounded_rectangle([60, 454, 60 + w2 + 50, 532], 10, fill=GOLD); d.text((85, 463), t2, font=f2, fill=GREEN)
overlay("chrome", 0, END_START, chrome)

def scrim(d, im):
    d.rounded_rectangle([40, 1080, 760, 1240], 22, fill=(10, 10, 8, 130))
    lg = LOGO.copy(); lg.thumbnail((130, 140)); im.paste(lg, (60, 1090), lg)
    d.text((200, 1096), "Precision Equine Health", font=font("CormorantGaramond-SemiBold.ttf", 60), fill=IVORY)
    d.text((200, 1166), "Hear the horse’s side.", font=font("CormorantGaramond-Italic.ttf", 56), fill=GOLD)
for i, (a, b) in enumerate([(3.62, 6.13), (9.94, 14.85), (20.05, 23.79), (38.31, 41.92)]):
    overlay(f"scrim{i}", a, b, scrim)

fCap = font("CormorantGaramond-Bold.ttf", 94)
def cap(txt, key):
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
                c = GOLD if key and w_ in key.split() else WHITE
                d.text((x + 4, y + 4), w_, font=fCap, fill=(0, 0, 0, 220)); d.text((x, y), w_, font=fCap, fill=c)
                x += d.textlength(w_ + " ", font=fCap)
            y += 100
    return fn
caps = [
    (0.05, 0.83, "Why do", ""), (0.83, 1.62, "white pasterns", "white pasterns"), (1.62, 2.30, "get scratches", "scratches"), (2.30, 2.97, "so easily?", "easily?", "+"),
    (3.62, 4.55, "Check the pasture", "pasture"), (4.55, 5.48, "before the leg.", "leg.", "+"),
    (9.94, 10.58, "Eaten,", "Eaten,"), (10.58, 11.30, "their compounds", "compounds"), (11.30, 12.13, "reach the skin…", "skin…", "+"),
    (12.71, 13.40, "and sunlight", "sunlight"), (13.40, 14.27, "switches them on.", "on.", "+"),
    (20.05, 20.90, "Swiss vets checked", "Swiss"), (20.90, 21.94, "young horses", "young"), (21.94, 22.55, "every week", "week"), (22.55, 23.24, "through the fall.", "fall.", "+"),
    (27.12, 28.03, "Same horse,", ""), (28.03, 29.07, "same field,", ""), (29.07, 30.31, "only the white legs flare?", "white", "+"), (30.85, 31.42, "That’s a clue.", "clue.", "+"),
    (38.31, 39.54, "Many causes look alike.", "alike.", "+"), (40.12, 40.80, "Bring the pattern", "pattern"), (40.80, 41.49, "to your vet.", "vet.", "+"),
]
for k, c in enumerate(caps):
    a, b, txt, key = c[:4]; tail = 0.12 if len(c) > 4 else 0.0
    overlay(f"cap{k:02d}", a, b + tail, cap(txt, key))

def panel(d, y0, y1, x0=60, x1=W - 60): d.rounded_rectangle([x0, y0, x1, y1], 26, fill=(10, 10, 8, 175))
def ltext(d, x, y, t, f, fill): d.text((x + 3, y + 3), t, font=f, fill=(0, 0, 0, 210)); d.text((x, y), t, font=f, fill=fill)
fB = font("CormorantGaramond-Bold.ttf", 96); fS = font("CormorantGaramond-SemiBold.ttf", 68)

# plant tally (counting, one by one)
plants = ["St. John’s wort", "Buckwheat", "Some clovers"]
def tally(n):
    def fn(d, im):
        panel(d, 1060, 1560)
        ctext(d, 1080, "PASTURE PLANTS", font("CormorantGaramond-Bold.ttf", 66), GOLD, False)
        for j in range(n):
            y = 1180 + 120 * j
            d.ellipse([120, y + 34, 156, y + 70], fill=TEAL)
            ltext(d, 190, y, plants[j], fB, IVORY)
    return fn
overlay("tally1", 6.13, 7.60, tally(1)); overlay("tally2", 7.60, 8.59, tally(2)); overlay("tally3", 8.59, 9.94, tally(3))

# melanin card + circled pastern on the freeze
def melanin(stage):
    def fn(d, im):
        panel(d, 620, 1010 if stage == 2 else 900)
        ctext(d, 645, "DARK SKIN = MELANIN", font("CormorantGaramond-Bold.ttf", 82), IVORY, False)
        ctext(d, 770, "built-in sunscreen", fS, GOLD, False)
        if stage == 2:
            ctext(d, 880, "WHITE SOCKS: NONE", font("CormorantGaramond-Bold.ttf", 86), TEAL, False)
            x, y = PAST
            for r_ in (95, 98, 101, 104, 107):
                d.ellipse([x - r_, y - r_ * 0.8, x + r_, y + r_ * 0.8], outline=TEAL, width=4)
    return fn
overlay("mel1", 14.85, 18.36, melanin(1)); overlay("mel2", 18.36, 20.05, melanin(2))

# study card
def study(d, im):
    panel(d, 1040, 1520)
    ctext(d, 1068, "WHITE PASTERNS", font("CormorantGaramond-Bold.ttf", 104), TEAL, False)
    ctext(d, 1200, "flared more often", fS, IVORY, False)
    ctext(d, 1280, "than dark ones", fS, IVORY, False)
    ctext(d, 1400, "Veterinary Dermatology", font("CormorantGaramond-SemiBoldItalic.ttf", 60), GOLD, False)
overlay("study", 23.79, 27.11, study)

# checklist
items = ["Walk the paddocks", "Photo: white + dark legs", "Every week"]
def check(n):
    def fn(d, im):
        panel(d, 1040, 1520)
        ctext(d, 1060, "WITH YOUR BARN MANAGER", font("CormorantGaramond-Bold.ttf", 66), GOLD, False)
        for j in range(n):
            y = 1160 + 115 * j
            d.line([(115, y + 46), (142, y + 74), (186, y + 18)], fill=TEAL, width=10)
            ltext(d, 215, y, items[j], font("CormorantGaramond-Bold.ttf", 84), IVORY)
    return fn
overlay("chk1", 31.99, 34.31, check(1)); overlay("chk2", 34.31, 37.18, check(2)); overlay("chk3", 37.18, 38.31, check(3))

# building equation
def eq(n):
    def fn(d, im):
        panel(d, 1040, 1500)
        parts = [("CLOVER", GOLD), ("+ SUN", IVORY), ("+ PINK SKIN", TEAL)]
        for j in range(n):
            ctext(d, 1065 + 140 * j, parts[j][0], font("CormorantGaramond-Bold.ttf", 120), parts[j][1], False)
    return fn
overlay("eq1", 41.92, 42.58, eq(1)); overlay("eq2", 42.58, 43.45, eq(2)); overlay("eq3", 43.45, END_START, eq(3))

# width check: nothing over 960 px
for p, a, b in ovs:
    bbox = Image.open(p).getbbox()
    if bbox and (bbox[2] > 1050 or bbox[0] < 30): print("EDGE", p, bbox)

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
    f'-r {FPS} -c:a aac -b:a 160k -movflags +faststart -metadata comment="{STAMP}" -t {TOTAL} {R}{NAME}.mp4')
json.dump({"segs": segs, "END_START": END_START, "TOTAL": TOTAL, "stamp": STAMP}, open(OUT + "timing.json", "w"), indent=1)
print("done", round(TOTAL, 2))
