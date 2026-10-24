"""PEH Precision Point No. 005 - "Two viruses. One syringe." monologue (Jarnathan, eleven_v4).
Build stamp PP005-v1.1 (2026-10-24). Visual recipe: hook = hard cut on the beat (horse -> syringe),
callouts = two-row comparison card + label checklist, end card = blurred still of the last shot."""
import subprocess, os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

R = "/home/claude/pp005/"
B = R + "broll/"
F = "/home/claude/peh/assets/fonts/"
OUT = R + "build/"
os.makedirs(OUT, exist_ok=True)
STAMP = "PP005-v1.1"
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

# ---------------- timeline (from silencedetect on the VO) ----------------
VO_LEN = 38.43
END_START = 35.0            # end card under "For more, join the private Precision Equine Health group."
TOTAL = VO_LEN + 2.4

# ---------------- footage ----------------
fill = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
grade = ",eq=brightness=-0.03:saturation=0.95"
segs = []
def seg_play(name, src, ss, d, rate=1.0, pre=""):
    src_d = d * rate
    run(f'ffmpeg -v error -y -ss {ss} -t {src_d + 0.3} -i "{src}" -an -vf "{pre}setpts=PTS/{rate},{fill}{grade},fps={FPS},format=yuv420p" -t {d} '
        f'-c:v libx264 -preset veryfast -crf 18 {OUT}{name}.mp4')
cursor = 0.0
def shot(name, until, src, ss, rate=1.0, pre=""):
    global cursor
    d = until - cursor
    if d <= 0.05: return
    seg_play(name, src, ss, d, rate, pre)
    segs.append((name, cursor, d)); cursor = until

SIL = B + "17619635-hd_1080_1920_30fps.mp4"      # Sofi Verasaluse - horse silhouetted against the sun
SYR = B + "7581432-hd_1080_2048_25fps.mp4"       # cottonbro studio - syringe drawn from a vial (the one non-horse shot)
FENCE = B + "19037020-hd_1080_1920_30fps.mp4"    # Karography - chestnut horse over a fence, muzzle to camera
STALL = B + "32979054-1440_2560_30fps.mp4"    # Ebahir - buckskin horse with head over the stall door, calm, ears forward (v1.1: replaces Pexels 20002354, head-shaking = distress)
RUN = B + "7030396-uhd.mp4"                      # Joshua Woroniecki - horse cantering in a paddock, rows of horse trailers behind
PADD = B + "11981586-hd_1080_1920_30fps.mp4"     # Marcelo Rodrigo - horses standing in a paddock, long shadows
RIDER = B + "15393690-uhd_1440_2560_50fps.mp4"   # Baris Karagoz - rider and horse silhouetted at sunset
# 4K landscape -> centre crop to 9:16 before the standard fill
RUNC1 = "crop=1215:2160:850:0,"
RUNC2 = "crop=1215:2160:1240:0,"

shot("s01", 2.65,  SIL, 1.0)                   # hook: horse against the sun
shot("s02", 4.49,  SYR, 2.0)                   # "in one syringe." hard cut
shot("s03", 8.16,  FENCE, 0.5)                 # influenza: caught and cleared (alert horse, face to camera)
shot("s04", 13.31, STALL, 5.0)                 # EHV-1: carried for life (calm horse over the stall door)
shot("s05", 16.32, RUN, 10.0, pre=RUNC1)        # reactivated by transport and hard work (cantering, trailers behind)
shot("s06", 19.56, SIL, 5.0)                   # flu vaccine does nothing for EHV-1
shot("s07", 24.53, FENCE, 15.5)                # nasal shedding / pregnant mares (muzzle over the fence)
shot("s08", 28.28, PADD, 2.0)                  # not labeled for EHM
shot("s09", 31.63, RUN, 20.0, pre=RUNC2)        # last winter's multi-state outbreak (trailer row behind)
shot("s10", END_START, RIDER, 0.5, rate=0.5)   # the shadow line, slow motion

# end card: blurred still of the last shot
run(f'ffmpeg -v error -y -ss 3.4 -i "{RIDER}" -frames:v 1 -vf "{fill}{grade}" {OUT}last.png')
im = Image.open(OUT + "last.png").convert("RGB").filter(ImageFilter.GaussianBlur(28))
dark = Image.new("RGB", (W, H), INK); im = Image.blend(im, dark, 0.55)
d = ImageDraw.Draw(im)
logo = LOGO.copy(); logo = logo.resize((360, int(360 * logo.height / logo.width)), Image.LANCZOS); im.paste(logo, ((W - logo.width) // 2, 330), logo)
def ctext(d, y, txt, f, fill, shadow=True):
    w = d.textlength(txt, font=f); x = (W - w) / 2
    if shadow: d.text((x + 3, y + 3), txt, font=f, fill=(0, 0, 0, 210))
    d.text((x, y), txt, font=f, fill=fill)
ctext(d, 840, "PRECISION EQUINE HEALTH", font("CormorantGaramond-SemiBold.ttf", 66), GOLD)
ctext(d, 950, "Between the belief and the label,", font("CormorantGaramond-MediumItalic.ttf", 70), IVORY)
ctext(d, 1035, "falls the shadow.", font("CormorantGaramond-MediumItalic.ttf", 70), IVORY)
ctext(d, 1180, "For more, join the private group", font("CormorantGaramond-SemiBold.ttf", 68), GOLD)
box_f = font("CormorantGaramond-Bold.ttf", 60); txt = "Precision Equine Health on Facebook"
tw = d.textlength(txt, font=box_f)
d.rounded_rectangle([(W - tw) / 2 - 40, 1290, (W + tw) / 2 + 40, 1400], 55, outline=GOLD, width=3)
d.text(((W - tw) / 2, 1310), txt, font=box_f, fill=IVORY)
im.save(OUT + "end.png")
ed = TOTAL - END_START
run(f'ffmpeg -v error -y -loop 1 -t {ed} -i {OUT}end.png -vf "fade=t=in:st=0:d=0.5,fps={FPS},format=yuv420p" -t {ed} -c:v libx264 -preset veryfast -crf 18 {OUT}s11.mp4')
segs.append(("s11", END_START, ed))

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
    for i, t in enumerate(["TWO VIRUSES.", "ONE SYRINGE."]):
        w = d.textlength(t, font=f1); y = 270 + i * 88
        d.rounded_rectangle([60, y, 60 + w + 60, y + 82], 14, fill=GREEN); d.text((90, y + 6), t, font=f1, fill=IVORY)
    t2 = "PRECISION POINT · No. 005"; w2 = d.textlength(t2, font=f2)
    d.rounded_rectangle([60, 454, 60 + w2 + 50, 532], 10, fill=GOLD); d.text((85, 463), t2, font=f2, fill=GREEN)
overlay("chrome", 0, END_START, chrome)
def scrim(d, im):
    d.rounded_rectangle([40, 1080, 760, 1240], 22, fill=(10, 10, 8, 130))
    lg = LOGO.copy(); lg.thumbnail((130, 140)); im.paste(lg, (60, 1090), lg)
    d.text((200, 1096), "Precision Equine Health", font=font("CormorantGaramond-SemiBold.ttf", 60), fill=IVORY)
    d.text((200, 1166), "Hear the horse’s side.", font=font("CormorantGaramond-Italic.ttf", 56), fill=GOLD)
overlay("scrim_a", 0, 19.56, scrim)
overlay("scrim_b", 28.28, END_START, scrim)

fCap = font("CormorantGaramond-Bold.ttf", 94)
def cap(txt, key, italic=False):
    fc = font("CormorantGaramond-BoldItalic.ttf", 94) if italic else fCap
    def fn(d, im):
        words = txt.split(); lines, cur = [], []
        for w_ in words:
            tt = " ".join(cur + [w_])
            if d.textlength(tt, font=fc) <= 960: cur.append(w_)
            else: lines.append(cur); cur = [w_]
        lines.append(cur)
        y = 1300 if len(lines) == 1 else 1255
        for ln in lines:
            full = " ".join(ln); x = (W - d.textlength(full, font=fc)) / 2
            for w_ in ln:
                c = GOLD if key and w_ in key.split() else WHITE
                d.text((x + 4, y + 4), w_, font=fc, fill=(0, 0, 0, 220)); d.text((x, y), w_, font=fc, fill=c)
                x += d.textlength(w_ + " ", font=fc)
            y += 100
    return fn

# karaoke chunks: (t0, t1, text, keyword) - boundaries on detected pauses; "+" = last chunk of a line (+0.12 hold)
caps = [
    (0.30, 1.10, "Flu and rhino", "Flu rhino"), (1.10, 2.65, "are two different viruses", "two different"), (2.65, 3.70, "in one syringe.", "one syringe.", "+"),
    (4.49, 5.14, "Influenza:", "Influenza:"), (5.70, 6.56, "your horse catches it,", "catches"), (6.84, 7.52, "and clears it.", "clears", "+"),
    (8.16, 9.14, "EHV-1:", "EHV-1:"), (9.79, 11.40, "a herpesvirus most horses", "herpesvirus"), (11.40, 12.95, "already carry for life,", "for life,"),
    (13.31, 14.60, "reactivated by transport", "transport"), (14.60, 15.68, "and hard work.", "hard work.", "+"),
    (16.32, 17.82, "The flu vaccine does nothing", "nothing"), (17.98, 18.87, "for EHV-1.", "EHV-1.", "+"),
    (24.53, 25.70, "It is not labeled against", "not labeled"), (25.70, 26.87, "the neurological form,", "neurological"), (27.23, 27.76, "EHM.", "EHM.", "+"),
    (28.28, 29.40, "The form behind", ""), (29.40, 31.04, "last winter’s multi-state outbreak.", "multi-state", "+"),
]
k = 0
for c in caps:
    a, b, txt, key = c[:4]; tail = 0.12 if len(c) > 4 else 0.0
    overlay(f"cap{k}", a, b + tail, cap(txt, key)); k += 1
# the Eliot line in italic
overlay("cap_e1", 31.63, 33.32, cap("Between the belief and the label,", "belief label,", italic=True))
overlay("cap_e2", 33.70, 34.41 + 0.3, cap("falls the shadow.", "shadow.", italic=True))

# ---- callouts (each replaces the caption while up) ----
fH, fB, fS = font("CormorantGaramond-Bold.ttf", 120), font("CormorantGaramond-SemiBold.ttf", 70), font("CormorantGaramond-Italic.ttf", 58)
def panel(d, y0, y1): d.rounded_rectangle([60, y0, W - 60, y1], 26, fill=(10, 10, 8, 170))
def ltext(d, x, y, t, f, fill): d.text((x + 3, y + 3), t, font=f, fill=(0, 0, 0, 210)); d.text((x, y), t, font=f, fill=fill)

# comparison card: row 1 influenza (19.56-24.13 is used for the checklist instead), shown 19.56..24.13? No: card over sentences 5; see below
def card(rows):
    def fn(d, im):
        panel(d, 1080, 1080 + 110 + 150 * len(rows))
        ctext(d, 1095, "TWO VIRUSES", font("CormorantGaramond-Bold.ttf", 64), GOLD, False)
        for i, (name, what, col) in enumerate(rows):
            y = 1180 + 150 * i
            ltext(d, 110, y, name, font("CormorantGaramond-Bold.ttf", 86), col)
            ltext(d, 110, y + 82, what, fB, IVORY)
    return fn
overlay("card1", 19.56, 21.0, card([("Influenza", "caught, then cleared", IVORY), ("EHV-1", "carried for life · reactivated", TEAL)]))

def vaccine(n):
    def fn(d, im):
        panel(d, 1080, 1510)
        ctext(d, 1096, "THE EHV-1 VACCINE", font("CormorantGaramond-Bold.ttf", 72), GOLD, False)
        items = [("✓", "less nasal shedding", TEAL), ("✓", "protects pregnant mares", TEAL), ("✗", "not labeled for EHM", GOLD)]
        for j in range(n):
            mark, t, col = items[j]; y = 1200 + 100 * j
            if mark == "✓": d.line([(125, y + 40), (150, y + 66), (190, y + 14)], fill=col, width=9)
            else: d.line([(130, y + 16), (185, y + 68)], fill=col, width=9); d.line([(185, y + 16), (130, y + 68)], fill=col, width=9)
            ltext(d, 210, y, t, font("CormorantGaramond-SemiBold.ttf", 72), IVORY)
    return fn
overlay("vac1", 21.0, 22.6, vaccine(1))
overlay("vac2", 22.6, 24.13 + 0.3, vaccine(2))
# "not labeled" row rides with the caption from 24.53 (caption carries the spoken words; the card returns with 3 rows)
overlay("vac3", 27.76, 28.28, vaccine(3))

def neq(d, im):
    panel(d, 660, 980)
    f96 = font("CormorantGaramond-Bold.ttf", 100)
    t = "FLU VACCINE  ≠  EHV-1"
    while d.textlength(t, font=f96) > 940: f96 = font("CormorantGaramond-Bold.ttf", f96.size - 4)
    ctext(d, 672, t, f96, TEAL, False)
    ctext(d, 850, "different virus, different vaccine", fB, IVORY, False)
overlay("neq", 16.32, 19.56 - 0.1, neq)
# the ≠ card covers the caption for sentence 4: keep the words on the card itself (done).  Remove the two sentence-4 captions:
ovs[:] = [o for o in ovs if not (o[0].endswith("cap11.png") or o[0].endswith("cap12.png"))]

def src(d, im):
    panel(d, 1270, 1400)
    ctext(d, 1285, "Sources: EDCC · AAEP vaccination guidelines", font("CormorantGaramond-SemiBold.ttf", 58), GOLD, False)
# source line replaces the caption area only when no caption is up: show during the EHM card window (card is mid-frame, source lower third)
overlay("src", 24.53, 31.04, src)
# during 24.53-31.04 captions are up in the lower third too -> move the source line up under the title tag instead
ovs[:] = [o for o in ovs if not o[0].endswith("src.png")]
def src2(d, im):
    t = "EDCC · AAEP vaccination guidelines"; f = font("CormorantGaramond-SemiBold.ttf", 56); w = d.textlength(t, font=f)
    d.rounded_rectangle([60, 560, 60 + w + 50, 636], 10, fill=(10, 10, 8, 170)); d.text((85, 568), t, font=f, fill=GOLD)
overlay("src2", 19.56, 31.04, src2)

# ---------------- final mux ----------------
inputs = " ".join(f'-i "{p}"' for p, _, _ in ovs)
chain, last = [], "0:v"
for i, (p, a, b) in enumerate(ovs):
    nl = f"v{i}"; chain.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{a:.2f},{b - 0.04:.2f})'[{nl}]"); last = nl
na = len(ovs) + 1
fc = ";".join(chain) + (
    f";[{na}:a]volume=1.0,apad,atrim=0:{TOTAL}[vo]"
    f";[{na + 1}:a]volume=0.11,afade=t=out:st={TOTAL - 2.4}:d=2.2,atrim=0:{TOTAL}[mus]"
    f";[vo][mus]amix=inputs=2:duration=longest:normalize=0,atrim=0:{TOTAL}[aout]")
run(f'ffmpeg -v error -y -i {OUT}base.mp4 {inputs} -i {R}vo.wav -stream_loop -1 -i {R}music.mp3 '
    f'-filter_complex "{fc}" -map "[{last}]" -map "[aout]" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p '
    f'-r {FPS} -c:a aac -b:a 160k -movflags +faststart -metadata comment="{STAMP}" -t {TOTAL} {R}PP005_two-viruses-one-syringe_v1.1.mp4')
json.dump({"segs": segs, "END_START": END_START, "TOTAL": TOTAL, "stamp": STAMP}, open(OUT + "timing.json", "w"), indent=1)
print("done", round(TOTAL, 2))
