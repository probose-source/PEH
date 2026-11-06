# PP013-v1.1 — replaces the drawn stretch diagram (s02, frames 99-237) with a type-only callout over
# real footage, and removes one-frame overlay dropouts/flickers. Audio is v1.0's, untouched.
import subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = sys.argv[1]; FONTS = sys.argv[2]
V10, CLIP, OUT = f"{S}/pp13/v10.mp4", f"{S}/src/40286611.mp4", f"{S}/pp13/PP013_not-a-trick_v1.1.mp4"
W, H, FPS = 1080, 1920, 30
GOLD, IVORY, TEAL, INK = (201, 168, 106), (240, 232, 214), (46, 196, 182), (10, 10, 8)
font = lambda n, s: ImageFont.truetype(f"{FONTS}/CormorantGaramond-{n}.ttf", s)

def frames(path, vf=None, ss=None, n=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", path]
    if vf: cmd += ["-vf", vf]
    if n: cmd += ["-frames:v", str(n)]
    p = subprocess.Popen(cmd + ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while (b := p.stdout.read(W * H * 3)) and len(b) == W * H * 3:
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)

FIX = {238: 239, 414: 413, 668: 667, 783: 784, 850: 849, 896: 897, 908: 909, 973: 974, 715: 714, 1033: 1036, 1034: 1036, 1035: 1036, 1124: 1126, 1125: 1126}   # one-frame dropouts -> neighbor
keep = {g: None for g in list(FIX.values()) + [140]}
for j, f in enumerate(frames(V10)):
    if j in keep: keep[j] = f.copy()

# 2) pill mask from a clean frame (title + series pills, static all episode)
ref = keep[140].astype(int)
m = np.zeros((H, W), bool)
for c in [(27, 51, 38), (201, 167, 106)]:
    m |= (np.abs(ref - c).sum(2) < 30)
m[:250] = False; m[560:] = False
pill = np.zeros((H, W), bool)
for y in range(250, 560):
    xs = np.nonzero(m[y])[0]
    if len(xs) > 60: pill[y, xs.min():xs.max() + 1] = True

# 3) new s02: Pexels 40286611 from 8.0 s (60 fps -> every 2nd frame), softened, type-only callout
A, B = 99, 238
src = list(frames(CLIP, vf="select=not(mod(n\\,2)),setpts=N/30/TB", ss=8.0, n=B - A))
assert len(src) == B - A, len(src)
LINES = ["CHIN TO CHEST", "CHIN TO GIRTH", "CHIN TOWARD THE HIP"]
REVEAL = [A, 138, 177]          # VO onsets 3.30 / 4.61 / 5.90 s
fH, fL = font("SemiBold", 66), font("Bold", 78)
new = {}
for i in range(A, B):
    bg = Image.fromarray(src[i - A]).filter(ImageFilter.GaussianBlur(1.2))
    bg = Image.eval(bg, lambda v: int(v * 0.92)).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rounded_rectangle([60, 1060, W - 60, 1580], 26, fill=(*INK, 185))
    def ct(y, t, f, c):
        tw = d.textlength(t, font=f); assert tw <= 900, (t, tw)
        x = (W - tw) / 2; d.text((x + 3, y + 3), t, font=f, fill=(0, 0, 0, 210)); d.text((x, y), t, font=f, fill=c)
    ct(1100, "THE CARROT STRETCH", fH, GOLD)
    shown = sum(i >= r for r in REVEAL)
    for k in range(shown):
        ct(1215 + k * 112, LINES[k], fL, TEAL if k == shown - 1 else IVORY)
    fr = np.array(Image.alpha_composite(bg, ov).convert("RGB"))
    fr[pill] = keep[140][pill]
    new[i] = fr

# 4) encode, audio from v1.0
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30",
    "-i", "-", "-i", V10, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-metadata", "comment=PP013-v1.1", OUT],
    stdin=subprocess.PIPE)
# 5) s05 freeze (frames 495-714): remove the drawn band + ring, patching from the clean Pexels frame
PATCH = np.load(f"{S}/pp13/bandpatch.npy")[:, :, ::-1].astype(np.float32)   # BGR->RGB, graded to match
MB = np.load(f"{S}/pp13/bandm.npy")[..., None]
N = 0
for j, f in enumerate(frames(V10)):
    f = new.get(j, keep[FIX[j]] if j in FIX else f)
    if 495 <= j <= 714:
        f = np.clip(f * (1 - MB) + PATCH * MB, 0, 255).astype(np.uint8)
    enc.stdin.write(f.tobytes()); N += 1
enc.stdin.close(); enc.wait(); print("frames", N, "->", OUT)
