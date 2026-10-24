"""PEH equine anatomy reference diagram (points of the horse + hoof + limb), SVG + PNG. Stamp PEH-ANAT-v1.0"""
import os, subprocess
OUT = "/home/claude/anat/"
GREEN, GOLD, IVORY, TEAL, INK = "#1c3428", "#c9a86a", "#f0e8d6", "#2ec4b6", "#100d09"
W, H = 1600, 1120

# Horse profile (facing left), hand-set path in a 1600x1000 frame
horse = ("M 300,430 C 280,380 300,330 350,300 C 380,282 420,280 440,300 C 470,330 500,350 540,360 "
         "C 600,375 680,380 760,380 C 850,380 930,372 1010,376 C 1080,380 1130,400 1170,440 "
         "C 1200,470 1210,520 1200,560 C 1195,600 1180,640 1165,680 L 1150,860 L 1120,860 L 1130,690 "
         "C 1110,650 1090,620 1060,610 L 1020,740 L 1000,860 L 970,860 L 985,730 L 1010,600 "
         "C 940,590 860,590 790,595 C 720,600 660,605 610,600 L 600,720 L 590,860 L 560,860 L 565,720 L 570,610 "
         "C 540,610 520,615 500,625 L 520,740 L 530,860 L 500,860 L 480,740 L 455,620 "
         "C 420,600 380,560 360,520 C 330,520 300,500 290,470 C 285,455 290,440 300,430 Z")
tail = "M 1170,440 C 1230,470 1260,560 1250,660 C 1245,720 1230,780 1210,820 C 1225,760 1230,700 1220,640 C 1210,580 1190,520 1165,480 Z"
mane = "M 440,300 C 500,290 560,300 620,330 C 680,350 740,360 800,366 L 760,380 C 680,380 600,375 540,360 C 500,350 470,330 440,300 Z"

# label: (text, point x,y, label x,y, anchor)
labels = [
    ("Poll", 420, 290, 400, 220, "end"),
    ("Forelock", 345, 300, 330, 240, "end"),
    ("Muzzle", 295, 470, 220, 520, "end"),
    ("Jaw / throatlatch", 400, 420, 330, 600, "end"),
    ("Crest (top of neck)", 560, 330, 560, 230, "middle"),
    ("Neck", 520, 420, 470, 500, "end"),
    ("WITHERS\n(base of the mane, in front of the saddle)", 800, 370, 820, 230, "middle"),
    ("Back", 900, 376, 900, 300, "middle"),
    ("Loin", 1000, 378, 1010, 300, "middle"),
    ("Croup", 1120, 405, 1140, 300, "middle"),
    ("Dock / tail", 1200, 470, 1320, 420, "start"),
    ("Point of hip", 1090, 440, 1340, 500, "start"),
    ("Point of buttock", 1200, 560, 1340, 600, "start"),
    ("Stifle", 1060, 610, 1340, 680, "start"),
    ("Gaskin", 1110, 650, 1340, 740, "start"),
    ("Hock", 1130, 700, 1340, 800, "start"),
    ("Hind cannon", 1140, 790, 1340, 860, "start"),
    ("Shoulder", 540, 480, 300, 740, "end"),
    ("Point of shoulder", 470, 560, 300, 800, "end"),
    ("Barrel / girth", 700, 560, 700, 700, "middle"),
    ("Flank", 980, 560, 980, 720, "middle"),
    ("Elbow", 560, 620, 300, 860, "end"),
    ("Forearm", 505, 680, 300, 920, "end"),
    ("Knee (carpus)", 520, 740, 640, 940, "start"),
    ("Front cannon", 525, 800, 640, 985, "start"),
    ("Fetlock", 528, 845, 640, 1030, "start"),
]
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Georgia, Cormorant Garamond, serif">',
       f'<rect width="{W}" height="{H}" fill="{GREEN}"/>',
       f'<text x="40" y="60" fill="{GOLD}" font-size="40" font-weight="bold">PEH EQUINE ANATOMY REFERENCE · points of the horse</text>',
       f'<text x="40" y="95" fill="{IVORY}" font-size="22">Precision Equine Health · PEH-ANAT-v1.0 · side view, horse facing left · footage must show the part the words name</text>',
       f'<path d="{horse}" fill="#6b4a2b" stroke="{IVORY}" stroke-width="3"/>',
       f'<path d="{mane}" fill="#3a2614"/>', f'<path d="{tail}" fill="#3a2614"/>',
       # eye, nostril, hoof lines
       '<circle cx="360" cy="360" r="9" fill="#100d09"/>', '<ellipse cx="305" cy="455" rx="7" ry="10" fill="#100d09"/>',
       ]
for x1, x2 in [(500, 530), (560, 590), (970, 1000), (1120, 1150)]:
    svg.append(f'<rect x="{x1-6}" y="860" width="{x2-x1+12}" height="28" fill="#2a1a0e" stroke="{IVORY}" stroke-width="2"/>')
# withers highlight
svg.append(f'<circle cx="800" cy="372" r="36" fill="none" stroke="{TEAL}" stroke-width="6"/>')
for text, px, py, lx, ly, anchor in labels:
    col = TEAL if text.startswith("WITHERS") else GOLD
    svg.append(f'<line x1="{px}" y1="{py}" x2="{lx}" y2="{ly + (14 if ly > py else -6)}" stroke="{col}" stroke-width="2"/>')
    svg.append(f'<circle cx="{px}" cy="{py}" r="6" fill="{col}"/>')
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        size = 30 if i == 0 else 22
        svg.append(f'<text x="{lx}" y="{ly + i*26}" fill="{IVORY if i else col}" font-size="{size}" text-anchor="{anchor}" font-weight="{"bold" if i == 0 else "normal"}">{ln}</text>')
svg.append(f'<text x="40" y="{H-60}" fill="{IVORY}" font-size="22">Hoof, side view: toe · quarter · heel · heel bulbs · coronary band (hairline) · hoof wall.  Sole view: frog · bars · sole · white line.</text>')
svg.append(f'<text x="40" y="{H-28}" fill="{IVORY}" font-size="22">Lower limb bones: P1 long pastern · P2 short pastern · P3 coffin bone (apex at the toe) · navicular behind P3.  Pastern = between fetlock and hoof.</text>')
svg.append('</svg>')
open(OUT + "peh-equine-anatomy.svg", "w").write("\n".join(svg))
# PNG via headless chromium
html = f'<html><body style="margin:0">{open(OUT + "peh-equine-anatomy.svg").read()}</body></html>'
open(OUT + "a.html", "w").write(html)
subprocess.run(["node", "-e", f"""
const {{chromium}} = require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});await p.goto('file://{OUT}a.html');await p.screenshot({{path:'{OUT}peh-equine-anatomy.png'}});await b.close();}})();
"""], check=True)
print("ok")
