"""Line-art illustrations for the 'What we do' rows (inline SVG, CSS-animated)."""
V = '#A98BF5'; DIM = '#4A3F70'; BG = '#111113'; GRID = '#1E1C25'; LBL = '#77748A'; HI = '#EDE7FF'
MONO = "JetBrains Mono, monospace"

def frame(n, title, aria, inner):
    pid = f'ilg{n}'
    return (f'<svg class="il" viewBox="0 0 400 300" role="img" aria-label="{aria}" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block">'
            f'<defs><pattern id="{pid}" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{GRID}" stroke-width="1"></path></pattern></defs>'
            f'<rect width="400" height="300" fill="{BG}"></rect><rect width="400" height="300" fill="url(#{pid})"></rect>'
            + inner +
            f'<text x="16" y="24" font-family="{MONO}" font-size="9" letter-spacing="1" fill="{LBL}">FIG. {n:02d} — {title}</text>'
            f'<path d="M8 8H20M8 8V20M392 8H380M392 8V20M8 292H20M8 292V280M392 292H380M392 292V280" stroke="{DIM}" stroke-width="1" fill="none"></path>'
            '</svg>')

def joint(x, y, r=9):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BG}" stroke="{V}" stroke-width="2"></circle>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.3:.1f}" fill="{V}"></circle>')

def tube(x1, y1, x2, y2, w=12):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{V}" stroke-width="{w}" stroke-linecap="round"></line>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BG}" stroke-width="{w-3}" stroke-linecap="round"></line>')

def t(x, y, s, size=8, fill=LBL, anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" letter-spacing="0.8" fill="{fill}" text-anchor="{anchor}">{s}</text>'

# 01 workshops: servo arm + ESP32
w = []
w.append(f'<path d="M110 206A40 40 0 0 1 150 166" fill="none" stroke="{DIM}" stroke-width="1" stroke-dasharray="3 4"></path>')
w.append(t(102, 176, 'J1', 9))
w.append(f'<rect x="108" y="238" width="84" height="10" fill="none" stroke="{V}" stroke-width="2"></rect>')
w.append(f'<rect x="134" y="212" width="32" height="26" rx="3" fill="{BG}" stroke="{V}" stroke-width="2"></rect>')
w.append(f'<g style="transform-origin: 150px 206px; animation: ilSwing 6s ease-in-out infinite">')
w.append(tube(150, 206, 214, 128))
w.append(f'<g style="transform-origin: 214px 128px; animation: ilSwing2 6s ease-in-out infinite">')
w.append(tube(214, 128, 296, 146, 10))
w.append(f'<path d="M296 146V166M286 166H306M286 166V178M306 166V178" stroke="{V}" stroke-width="2" fill="none" stroke-linecap="round"></path>')
w.append(joint(296, 146, 7))
w.append('</g>')
w.append(joint(214, 128, 9))
w.append('</g>')
w.append(joint(150, 206, 11))
w.append(f'<rect x="248" y="226" width="96" height="36" fill="none" stroke="{DIM}" stroke-width="1.5"></rect>')
w.append(''.join(f'<line x1="{254+i*8}" y1="226" x2="{254+i*8}" y2="220" stroke="{DIM}" stroke-width="1.5"></line>' for i in range(11)))
w.append(f'<rect x="282" y="234" width="28" height="20" fill="none" stroke="{V}" stroke-width="1.5"></rect>')
w.append(t(296, 274, 'ESP32 · BLE', 8, LBL, 'middle'))
w.append(f'<path d="M248 244C224 244 214 246 192 244" fill="none" stroke="{V}" stroke-width="1.5" stroke-dasharray="4 6" style="animation: ilFlow 2.4s linear infinite"></path>')
w.append(f'<rect x="324" y="96" width="44" height="80" rx="8" fill="none" stroke="{DIM}" stroke-width="1.5"></rect>')
w.append(f'<circle cx="346" cy="150" r="12" fill="none" stroke="{V}" stroke-width="1.5"></circle><circle cx="346" cy="150" r="4" fill="{V}" style="animation: ilNudge 3s ease-in-out infinite"></circle>')
w.append(t(346, 90, 'PHONE', 8, LBL, 'middle'))
W1 = frame(1, 'WORKSHOPS', 'Line drawing of a servo robot arm wired to an ESP32 board and controlled from a phone', ''.join(w))

# 02 projects: LED matrix tetris
p = []
ox, oy, c, cols, rows = 128, 44, 16, 9, 14
stack = {(r, cc) for r, cc in [(13,0),(13,1),(13,2),(13,3),(13,5),(13,6),(13,7),(13,8),(12,0),(12,1),(12,4),(12,5),(12,6),(12,8),(11,0),(11,4),(11,5),(10,4)]}
p.append(f'<rect x="{ox-10}" y="{oy-10}" width="{cols*c+20}" height="{rows*c+20}" fill="none" stroke="{V}" stroke-width="2"></rect>')
for r in range(rows):
    for cc in range(cols):
        lit = (r, cc) in stack
        p.append(f'<circle cx="{ox+cc*c+c/2}" cy="{oy+r*c+c/2}" r="5" fill="{V if lit else "#221F2C"}"></circle>')
piece = [(0,1),(1,0),(1,1),(1,2)]  # T piece, lands on rows 8-9
p.append('<g style="animation: ilDrop 4.8s steps(8, end) infinite">')
for r, cc in piece:
    p.append(f'<circle cx="{ox+(cc+1)*c+c/2}" cy="{oy+(r+10)*c+c/2}" r="5.5" fill="{HI}"></circle>')
p.append('</g>')
p.append(f'<rect x="300" y="44" width="72" height="62" fill="none" stroke="{DIM}" stroke-width="1.5"></rect>' + t(336, 60, 'NEXT', 8, LBL, 'middle'))
for r, cc in [(0,0),(1,0),(2,0),(2,1)]:
    p.append(f'<rect x="{326+cc*10}" y="{68+r*10}" width="8" height="8" fill="{V}"></rect>')
p.append(t(300, 132, 'SCORE', 8) + t(300, 148, '004200', 11, HI))
p.append(t(300, 176, 'LINES', 8) + t(300, 192, '017', 11, HI))
p.append(t(300, 262, '8 × MAX7219', 8))
p.append(f'<path d="M40 60H96M40 60V250M40 250H96" fill="none" stroke="{DIM}" stroke-width="1" stroke-dasharray="3 4"></path>' + t(30, 160, '32 × 16', 8, LBL, 'middle').replace('<text', '<text transform="rotate(-90 30 160)"'))
W2 = frame(2, 'PROJECTS', 'An LED matrix playing Tetris, with a falling piece and a score panel', ''.join(p))

# 03 competitions we host: arena top-down + bracket
h = []
h.append(f'<rect x="76" y="52" width="196" height="196" fill="none" stroke="{V}" stroke-width="6" stroke-dasharray="10 8"></rect>')
h.append(f'<rect x="88" y="64" width="172" height="172" fill="none" stroke="{DIM}" stroke-width="1"></rect>')
h.append(f'<circle cx="174" cy="150" r="46" fill="none" stroke="{DIM}" stroke-width="1" stroke-dasharray="3 5"></circle>')
h.append(f'<path d="M174 64V236M88 150H260" stroke="{GRID}" stroke-width="1"></path>')
def bot(rot):
    return (f'<g transform="rotate({rot} 174 150)"><g transform="translate(232 150)">'
            f'<polygon points="-14,-13 14,-13 14,13 -14,13" fill="{BG}" stroke="{V}" stroke-width="2"></polygon>'
            f'<polygon points="-14,13 -14,-13 -24,13" fill="{V}"></polygon>'
            f'<rect x="-10" y="-18" width="12" height="5" fill="{V}"></rect><rect x="-10" y="13" width="12" height="5" fill="{V}"></rect></g></g>')
h.append(f'<g style="transform-origin: 174px 150px; animation: ilOrbit 10s linear infinite">' + bot(0) + bot(180) +
         f'<path d="M174 92A58 58 0 0 1 232 150" fill="none" stroke="{HI}" stroke-width="1.2" stroke-dasharray="2 5" opacity="0.6"></path></g>')
bx = 300
h.append(f'<path d="M{bx} 80H{bx+20}V110H{bx+40}M{bx} 140H{bx+20}V110M{bx} 170H{bx+20}V200H{bx+40}M{bx} 230H{bx+20}V200M{bx+40} 110H{bx+52}V155H{bx+70}M{bx+40} 200H{bx+52}V155" fill="none" stroke="{DIM}" stroke-width="1.5"></path>')
h.append(f'<circle cx="{bx+74}" cy="155" r="5" fill="{V}" style="transform-origin: {bx+74}px 155px; animation: ilPulse 2s ease-in-out infinite"></circle>')
h.append(t(176, 272, 'DODGEBOTS · KNOCKOUT · 12 TEAMS', 8, LBL, 'middle'))
W3 = frame(3, 'COMPETITIONS WE HOST', 'Top-down drawing of a robot arena with two robots circling, next to a knockout bracket', ''.join(h))

# 04 competitions we enter: road to Robocon timeline
e = []
e.append(f'<path d="M44 168H356" stroke="{DIM}" stroke-width="2" stroke-dasharray="4 6"></path>')
e.append(f'<path d="M44 168H200" stroke="{V}" stroke-width="2"></path>')
nodes = [(64, 'ROBOCON MY', '2025 · UTHM', True), (184, 'VIBATHON', '2026 · RUNNER-UP', False), (334, 'ABU ROBOCON', '2027 · SOLO', True)]
for i, (x, a, b, up) in enumerate(nodes):
    last = i == 2
    e.append(f'<circle cx="{x}" cy="168" r="{8 if last else 6}" fill="{BG if last else V}" stroke="{V}" stroke-width="2"></circle>')
    if last:
        e.append(f'<circle cx="{x}" cy="168" r="8" fill="none" stroke="{V}" stroke-width="1.5" style="transform-origin: {x}px 168px; animation: ilRing 2.2s ease-out infinite"></circle>')
        e.append(f'<path d="M{x} 160V112M{x} 112H{x+26}L{x+20} 120L{x+26} 128H{x}" fill="none" stroke="{V}" stroke-width="2" stroke-linejoin="round"></path>')
    ty = 136 if up and not last else (100 if last else 200)
    anchor = 'end' if last else 'middle'
    xx = x - 6 if last else x
    if not up and not last: e.append(f'<line x1="{x}" y1="174" x2="{x}" y2="186" stroke="{DIM}" stroke-width="1"></line>')
    if up and not last: e.append(f'<line x1="{x}" y1="148" x2="{x}" y2="162" stroke="{DIM}" stroke-width="1"></line>')
    e.append(t(xx, ty, a, 9, HI, anchor) + t(xx, ty + 14, b, 8, LBL, anchor))
e.append(f'<g style="animation: ilRoll 5s ease-in-out infinite"><g transform="translate(206 148)">'
         f'<rect x="0" y="0" width="30" height="14" rx="3" fill="{BG}" stroke="{V}" stroke-width="2"></rect>'
         f'<line x1="15" y1="0" x2="15" y2="-10" stroke="{V}" stroke-width="2"></line><circle cx="15" cy="-12" r="2.5" fill="{V}"></circle>'
         f'<circle cx="7" cy="18" r="4" fill="{BG}" stroke="{V}" stroke-width="2"></circle><circle cx="23" cy="18" r="4" fill="{BG}" stroke="{V}" stroke-width="2"></circle></g></g>')
e.append(t(200, 262, 'T – 29 AUG 2027', 9, V, 'middle'))
W4 = frame(4, 'COMPETITIONS WE ENTER', 'A timeline from Robocon Malaysia 2025 through the 2026 Vibathon to ABU Robocon 2027, with a small robot driving along it', ''.join(e))

# 05 talks & visits: microphone + factory
k = []
k.append(f'<rect x="78" y="70" width="34" height="58" rx="17" fill="{BG}" stroke="{V}" stroke-width="2"></rect>')
k.append(''.join(f'<line x1="84" y1="{82+i*8}" x2="106" y2="{82+i*8}" stroke="{DIM}" stroke-width="1.2"></line>' for i in range(5)))
k.append(f'<path d="M66 108A29 29 0 0 0 124 108M95 137V168M76 170H114" fill="none" stroke="{V}" stroke-width="2" stroke-linecap="round"></path>')
for i, r in enumerate((44, 58, 72)):
    k.append(f'<path d="M{95+r*0.55:.0f} {99-r*0.6:.0f}A{r} {r} 0 0 1 {95+r*0.55:.0f} {99+r*0.6:.0f}" fill="none" stroke="{V}" stroke-width="1.5" style="animation: ilBlink 1.8s ease-in-out {i*0.3:.1f}s infinite"></path>')
for i in range(9):
    hgt = [18, 30, 22, 38, 26, 34, 16, 28, 20][i]
    k.append(f'<rect x="{58+i*9}" y="{236-hgt}" width="5" height="{hgt}" fill="{V}" style="transform-origin: {60.5+i*9}px 236px; animation: ilEq {0.9+0.13*i:.2f}s ease-in-out infinite"></rect>')
k.append(t(95, 256, 'INSIDE THE ARENA', 8, LBL, 'middle'))
k.append(f'<line x1="186" y1="56" x2="186" y2="250" stroke="{DIM}" stroke-width="1" stroke-dasharray="2 5"></line>')
k.append(f'<path d="M212 196V136L240 116V136L268 116V136L296 116V136L324 116V96H338V136L366 116V196Z" fill="none" stroke="{V}" stroke-width="2" stroke-linejoin="round"></path>')
k.append(f'<path d="M338 92C344 84 334 78 342 70" fill="none" stroke="{DIM}" stroke-width="1.5" style="animation: ilBlink 2.4s ease-in-out infinite"></path>')
k.append(f'<line x1="206" y1="216" x2="372" y2="216" stroke="{V}" stroke-width="2"></line>')
k.append(''.join(f'<circle cx="{214+i*20}" cy="222" r="4" fill="none" stroke="{DIM}" stroke-width="1.5"></circle>' for i in range(9)))
k.append(f'<clipPath id="ilc5"><rect x="206" y="190" width="166" height="30"></rect></clipPath><g clip-path="url(#ilc5)"><g style="animation: ilConvey 4s linear infinite">' + ''.join(f'<rect x="{196+i*44}" y="202" width="16" height="14" fill="{BG}" stroke="{V}" stroke-width="1.5"></rect>' for i in range(5)) + '</g></g>')
k.append(f'<path d="M232 196V172L252 156L268 170" fill="none" stroke="{HI}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>{joint(232, 172, 4)}{joint(252, 156, 4)}')
k.append(t(289, 256, 'FESTO · PROTON', 8, LBL, 'middle'))
W5 = frame(5, 'TALKS &amp; VISITS', 'A microphone with sound waves next to a factory with a conveyor and robot arm', ''.join(k))

# 06 the circuit: newsletter page with signal traces
c6 = []
c6.append(f'<rect x="140" y="44" width="124" height="176" fill="{BG}" stroke="{V}" stroke-width="2"></rect>')
c6.append(t(152, 66, 'THE CIRCUIT', 10, HI) + t(152, 80, 'ISSUE 01 · WEEKLY', 7, LBL))
c6.append(f'<line x1="152" y1="88" x2="252" y2="88" stroke="{DIM}" stroke-width="1"></line>')
c6.append(f'<rect x="152" y="98" width="100" height="44" fill="none" stroke="{DIM}" stroke-width="1"></rect><path d="M152 142L184 116L204 132L226 112L252 136" fill="none" stroke="{V}" stroke-width="1.5"></path>')
c6.append(''.join(f'<rect x="152" y="{152+i*10}" width="{[100, 86, 96, 62, 92, 74][i]}" height="3" fill="#2A2635"></rect>' for i in range(6)))
traces = ['M140 80H104V60H56', 'M140 120H86V150H44', 'M140 196H112V236H60', 'M264 70H306V52H352', 'M264 132H322V170H360', 'M264 204H296V246H346']
for i, d in enumerate(traces):
    c6.append(f'<path d="{d}" fill="none" stroke="{DIM}" stroke-width="2"></path>')
    c6.append(f'<path d="{d}" fill="none" stroke="{HI}" stroke-width="2" stroke-dasharray="8 140" style="animation: ilFlow2 {2.2+0.35*i:.2f}s linear {0.4*i:.1f}s infinite"></path>')
    ex, ey = d.split('H')[-1], None
for (x, y) in [(56, 60), (44, 150), (60, 236), (352, 52), (360, 170), (346, 246)]:
    c6.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{BG}" stroke="{V}" stroke-width="2"></circle>')
c6.append(t(202, 262, 'BUILT · COMING UP · WORTH APPLYING FOR', 7, LBL, 'middle'))
W6 = frame(6, 'THE CIRCUIT', 'A newsletter page with circuit traces carrying signals out to the edges', ''.join(c6))

CSS = ('@keyframes ilSwing{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(9deg)}}'
       '@keyframes ilSwing2{0%,100%{transform:rotate(12deg)}50%{transform:rotate(-14deg)}}'
       '@keyframes ilNudge{0%,100%{transform:translate(0,0)}25%{transform:translate(4px,-4px)}75%{transform:translate(-4px,3px)}}'
       '@keyframes ilDrop{0%{transform:translateY(-128px)}100%{transform:translateY(0)}}'
       '@keyframes ilOrbit{to{transform:rotate(360deg)}}'
       '@keyframes ilPulse{0%,100%{transform:scale(1);opacity:.6}50%{transform:scale(1.5);opacity:1}}'
       '@keyframes ilRing{0%{transform:scale(1);opacity:.9}100%{transform:scale(2.6);opacity:0}}'
       '@keyframes ilRoll{0%,100%{transform:translateX(0)}50%{transform:translateX(84px)}}'
       '@keyframes ilEq{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}'
       '@keyframes ilBlink{0%,100%{opacity:.2}50%{opacity:1}}'
       '@keyframes ilConvey{to{transform:translateX(44px)}}'
       '@keyframes ilFlow{to{stroke-dashoffset:-20}}'
       '@keyframes ilFlow2{from{stroke-dashoffset:148}to{stroke-dashoffset:0}}'
       '.wrow .wimg svg{transition:transform .9s cubic-bezier(.2,.7,.2,1)}.wrow:hover .wimg svg{transform:scale(1.04)}'
       '@media (prefers-reduced-motion: reduce){.il *{animation:none !important}}')
ROWS = {'Workshops': W1, 'Projects': W2, 'Competitions we host': W3, 'Competitions we enter': W4, 'Talks &amp; visits': W5, 'The Circuit': W6}

if __name__ == '__main__':
    import sys
    html = '<!doctype html><html><head><style>body{margin:0;background:#EEECE8;display:grid;grid-template-columns:repeat(3,400px);gap:10px;padding:10px}' + CSS + '</style></head><body>' + ''.join(f'<div style="position:relative;width:400px;height:300px">{v}</div>' for v in ROWS.values()) + '</body></html>'
    open(sys.argv[1], 'w').write(html)
