"""Rebuild the Partners page on the homepage's shell (nav, type, labels, footer), with real photos and no placeholders."""
B = '/tmp/claude-0/-home-claude/56e6067c-1d8d-5144-a461-fa0e85a4a472/scratchpad/canvas/project/'
m = open(B + 'Main.dc.html').read()
style = m[m.index('<helmet>') + len('<helmet>'):m.index('</helmet>')]
nav = m[m.index('<nav aria-label="Main"'):m.index('</sc-if>', m.index('<sc-if value="{{ menuOpen }}"')) + len('</sc-if>')]
footer = m[m.index('<footer id="contact"'):m.index('</footer>') + len('</footer>')]
for a, b in (('href="#work"', 'href="Main.dc.html#work"'), ('href="#top"', 'href="Main.dc.html"')):
    nav = nav.replace(a, b); footer = footer.replace(a, b)
nav = nav.replace('<a href="Sponsors.dc.html" class="ul" style="text-decoration: none">Partners</a>',
                  '<a href="Sponsors.dc.html" class="ul" aria-current="page" style="text-decoration: none; color: #C9B6FF">Partners</a>')
wrap_open = m[m.index('<div', m.index('</helmet>')):m.index('>', m.index('<div', m.index('</helmet>'))) + 1]

IMG = {'proton': '6bb899dac57c68d4b8cbd5057c8cdeb3', 'dodgebots': 'f9c7f0690cc0feed9f86957634bd5dd2', 'servo': '9b3a05a1b2d2975ba970069407cba1dc',
       'robocon': 'c21941f15354f1e5b8d685f3e51290c7', 'talk': '070bf9d9fcce43beced7c1819aa8c31a', 'ecx': '75952b6a9ba8ab27f4f02576f2b65d09'}
LOGOS = [('dfb53f4ab5afa546fd6f573e59ef4997', 'Jeffrey Cheah Foundation'), ('39a3ff91dfce64e9fa58a1ab731fce85', 'Campus with a Conscience'),
         ('16c70f434d40e49313b883be7b2f5761', 'Sunway College')]

css = """
.pp .wrap{max-width:1360px;margin:0 auto;padding:0 24px}
.pp h2{margin:0;font-weight:500;font-size:clamp(36px,4.6vw,64px);letter-spacing:-0.03em;line-height:1.02}
.pp .hero{position:relative;overflow:hidden;background:#0B0B0C;color:#FFFFFF}
.pp .hero img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%}
.pp .hero .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,0.93) 0%,rgba(11,11,12,0.8) 45%,rgba(11,11,12,0.45) 100%),linear-gradient(180deg,rgba(11,11,12,0) 55%,rgba(11,11,12,0.95) 100%)}
.pp .hero .wrap{position:relative;z-index:1;padding-top:110px;padding-bottom:56px}
.pp h1{margin:20px 0 0;font-weight:500;font-size:clamp(46px,7.2vw,112px);line-height:.95;letter-spacing:-0.035em;max-width:13ch}
.pp h1 span{color:#A98BF5}
.pp .lede{margin:28px 0 0;max-width:600px;font-size:clamp(17px,1.5vw,20px);line-height:1.6;color:#C2C0CA}
.pp .btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}
.pp .btn{display:inline-flex;align-items:center;gap:10px;padding:15px 22px;font-size:15px;font-weight:500;text-decoration:none;transition:background-color .2s,color .2s,border-color .2s}
.pp .btn.pri{background:#7852C1;color:#FFFFFF;border:1px solid #7852C1}.pp .btn.pri:hover{background:#6A44BE}
.pp .btn.sec{border:1px solid #FFFFFF;color:#FFFFFF}.pp .btn.sec:hover{background:#FFFFFF;color:#0B0B0C}
.pp .stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:88px;border-top:1px solid rgba(255,255,255,0.18)}
.pp .stats > div{padding:18px 20px 4px 0}
.pp .stats > div + div{padding-left:20px;border-left:1px solid rgba(255,255,255,0.18)}
.pp .stats b{display:block;margin-top:10px;font-weight:500;font-size:clamp(34px,4vw,56px);letter-spacing:-0.03em;line-height:1}
.pp .note{margin:18px 0 0;font-size:13px;color:#8E8C95}
.pp .light{background:#EEECE8;color:#0B0B0C;padding:120px 0}
.pp .head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:18px 40px;margin-bottom:48px}
.pp .head p{margin:0;max-width:460px;color:#4A4752;font-size:16px;line-height:1.6}
.pp .feature{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);background:#FFFFFF;border:1px solid #DCD8D0}
.pp .feature .ph{min-height:360px;overflow:hidden}
.pp .ph img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.pp .feature:hover .ph img,.pp .rec:hover .ph img{transform:scale(1.04)}
.pp .feature .tx{padding:36px 36px 32px;display:flex;flex-direction:column}
.pp .feature h3{margin:12px 0 12px;font-weight:500;font-size:32px;letter-spacing:-0.02em}
.pp .feature p,.pp .rec p{margin:0;color:#4A4752;font-size:15px;line-height:1.6}
.pp .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto;padding-top:24px}
.pp .chips span{padding:7px 11px;border:1px solid #CFCAD8;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#3A3842}
.pp .grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin-top:20px}
.pp .rec{background:#FFFFFF;border:1px solid #DCD8D0}
.pp .rec .ph{aspect-ratio:4 / 3;overflow:hidden;background:#17171A}
.pp .rec .tx{padding:20px 20px 24px}
.pp .rec h3{margin:10px 0 8px;font-weight:500;font-size:20px;letter-spacing:-0.01em;line-height:1.25}
.pp .dark{position:relative;overflow:hidden;background:#0B0B0C;color:#FFFFFF;padding:120px 0}
.pp .dark .glow{position:absolute;width:900px;height:900px;right:-300px;top:-300px;border-radius:50%;background:radial-gradient(circle,rgba(120,82,193,0.22),rgba(120,82,193,0) 66%);pointer-events:none}
.pp .dark .head p{color:#A9A6AE}
.pp .tiers{position:relative;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.pp .tier{padding:26px 22px 26px;background:rgba(255,255,255,0.03);border:1px solid #2E2C34;display:flex;flex-direction:column}
.pp .tier.top{border-color:#7852C1;background:rgba(120,82,193,0.10)}
.pp .tier .nm{display:flex;justify-content:space-between;align-items:center;gap:12px}
.pp .tier .tag{padding:5px 9px;border:1px solid #A98BF5;color:#C9B6FF;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.pp .tier .pr{margin:16px 0 6px;font-weight:500;font-size:44px;letter-spacing:-0.03em;line-height:1}
.pp .tier ul{margin:0;padding:0;list-style:none;border-top:1px solid #2E2C34}
.pp .tier li{padding:11px 0;border-bottom:1px solid #2E2C34;font-size:15px;line-height:1.5;color:#C9C6CF;display:flex;gap:12px}
.pp .tier li::before{content:"";flex:0 0 6px;height:6px;margin-top:8px;background:#A98BF5}
.pp .inkind{position:relative;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:20px 40px;margin-top:20px;padding:28px;border:1px solid #2E2C34}
.pp .inkind p{margin:8px 0 0;max-width:700px;color:#C9C6CF;font-size:15px;line-height:1.6}
.pp .steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid #0B0B0C}
.pp .steps li{list-style:none;padding:22px 24px 8px 0}
.pp .steps li + li{padding-left:24px;border-left:1px solid #CFCAD8}
.pp .steps .n{font-weight:500;font-size:15px;color:#6A44BE}
.pp .steps h3{margin:12px 0 8px;font-weight:500;font-size:21px;letter-spacing:-0.01em}
.pp .steps p{margin:0;color:#4A4752;font-size:15px;line-height:1.55}
.pp .plate{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px 48px;margin-top:88px;padding-top:28px;border-top:1px solid #CFCAD8}
.pp .plate .slab{font-size:14px;font-weight:500;color:#6B6862;white-space:nowrap}
.pp .plate .logos{display:flex;flex-wrap:wrap;align-items:center;gap:28px 56px}
.pp .plate .logos div{height:64px;display:flex;align-items:center}
.pp .plate img{display:block;max-width:100%;max-height:100%;width:auto;height:auto}
.pp .talk{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px 72px;align-items:start}
.pp .who{padding:22px 0;border-top:1px solid #2E2C34}
.pp .who b{display:block;margin-top:8px;font-weight:500;font-size:22px}
.pp .who span{color:#A9A6AE;font-size:15px}
.pp .row{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px 0;border-top:1px solid #2E2C34;color:#FFFFFF;text-decoration:none;transition:padding-left .25s,color .2s}
.pp .row:hover{padding-left:8px;color:#C9B6FF}
.pp .row small{display:block;margin-bottom:6px}
.pp .row strong{font-weight:500;font-size:clamp(17px,1.6vw,21px);word-break:break-word}
.pp .rows .row:last-child{border-bottom:1px solid #2E2C34}
@media (max-width: 980px){.pp .grid4{grid-template-columns:repeat(2,minmax(0,1fr))}.pp .tiers{grid-template-columns:minmax(0,1fr)}.pp .steps{grid-template-columns:repeat(2,minmax(0,1fr))}.pp .steps li:nth-child(3){padding-left:0;border-left:0}.pp .talk{grid-template-columns:minmax(0,1fr)}}
@media (max-width: 760px){.pp .hero .wrap{padding-top:72px}.pp .stats{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:56px}.pp .stats > div:nth-child(3){padding-left:0;border-left:0}.pp .stats > div:nth-child(n+3){border-top:1px solid rgba(255,255,255,0.18)}
.pp .light,.pp .dark{padding:84px 0}.pp .feature{grid-template-columns:minmax(0,1fr)}.pp .feature .ph{min-height:0;aspect-ratio:4 / 3}.pp .feature .tx{padding:24px 22px}
.pp .grid4{grid-template-columns:minmax(0,1fr)}.pp .steps{grid-template-columns:minmax(0,1fr)}.pp .steps li + li{padding-left:0;border-left:0;border-top:1px solid #CFCAD8}
.pp .plate{margin-top:64px;gap:16px}.pp .plate .logos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;width:100%}.pp .plate .logos div{height:48px;justify-content:center}}
"""
css += """
.pp .tier .pl{margin:0 0 20px;font-size:14px;color:#A9A6AE}
.pp .all{position:relative;margin:16px 0 0;padding:18px 22px;border:1px solid #2E2C34;color:#C9C6CF;font-size:15px;line-height:1.6}
.pp .all b{color:#FFFFFF;font-weight:500}
.pp .why{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid #0B0B0C}
.pp .why > div{padding:24px 28px 8px 0}
.pp .why > div + div{padding-left:28px;border-left:1px solid #CFCAD8}
.pp .why h3,.pp .goes h3{margin:0 0 10px;font-weight:500;font-size:22px;letter-spacing:-0.01em;line-height:1.25}
.pp .why p,.pp .goes p{margin:0;color:#4A4752;font-size:15px;line-height:1.6}
.pp .goes{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:72px}
.pp .goes > div{padding:22px 22px 24px;border:1px solid #CFCAD8}
.pp .goes h3{font-size:18px}
@media (max-width: 1100px){.pp .tiers{grid-template-columns:repeat(2,minmax(0,1fr))}.pp .goes{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width: 760px){.pp .tiers,.pp .goes{grid-template-columns:minmax(0,1fr)}.pp .why{grid-template-columns:minmax(0,1fr)}.pp .why > div + div{padding-left:0;border-left:0;border-top:1px solid #CFCAD8}}
"""
style = style.replace('</style>', css + '</style>')

def rec(img, tag, title, text, alt):
    return (f'<article class="rec rv"><div class="ph"><img src="/_blob/{IMG[img]}" alt="{alt}" loading="lazy"></div>'
            f'<div class="tx"><span class="lb" style="color: #6A44BE">{tag}</span><h3>{title}</h3><p>{text}</p></div></article>')

def tier(name, price, items, top=False):
    lis = ''.join(f'<li>{i}</li>' for i in items)
    tag = '<span class="tag">Highest visibility</span>' if top else ''
    return (f'<article class="tier{" top" if top else ""} rv"><div class="nm"><span class="lb" style="color: #C9B6FF">{name}</span>{tag}</div>'
            f'<div class="pr">{price}</div><ul>{lis}</ul></article>')

TIERS = [
 ('Diamond', 'RM8,000', '1 place', True, ['Names 3 workshops (first pick) and 1 NGO outreach session',
   'A standalone post each semester, tagged in every workshop post', 'Feature article in The Circuit each semester, logo in every issue',
   'Top row, largest logo on the club T-shirt; standalone bunting at every booth and showcase', 'Emcee mention at the start and end of every workshop and event',
   'Custom 3D-printed plaque, presented on stage']),
 ('Platinum', 'RM5,000', '2 places', False, ['Names 2 workshops and 1 NGO outreach session', 'Two standalone posts a year, tagged in posts for its workshops',
   'One feature article a year in The Circuit, logo in every issue', 'Second row on the T-shirt; top row of the shared bunting',
   'Emcee mention at its workshops, its outreach session and major events', '3D-printed plaque']),
 ('Gold', 'RM2,500', '3 places', False, ['Names 1 workshop', 'One standalone post a year', 'Logo in every issue of The Circuit',
   'Third row on the T-shirt; middle row of the shared bunting', 'Emcee mention at its named workshop', '3D-printed token']),
 ('Silver', 'RM1,000', '6 places', False, ['A shared post with the other Silver partners', 'Listed in the sponsor footer of The Circuit',
   'Bottom row on the T-shirt and the shared bunting', 'Emcee mention at the end of major events', 'Framed certificate of appreciation']),
]
def tier(name, price, places, top, items):
    lis = ''.join(f'<li>{i}</li>' for i in items)
    tag = '<span class="tag">First pick</span>' if top else ''
    return (f'<article class="tier{" top" if top else ""} rv"><div class="nm"><span class="lb" style="color: #C9B6FF">{name}</span>{tag}</div>'
            f'<div class="pr">{price}</div><p class="pl">a year · {places}</p><ul>{lis}</ul></article>')

logos = ''.join(f'<div><img src="/_blob/{i}" alt="{a}" loading="lazy"></div>' for i, a in LOGOS)

body = f"""{wrap_open}
{nav}

<main class="pp">
<!-- ======= HERO ======= -->
<section id="top" class="hero">
<img class="bg" src="/_blob/c28be5801fac3081433e07fcf7b60a1b" alt="" aria-hidden="true">
<div class="shade" aria-hidden="true"></div>
<div class="wrap">
<div class="lb dash" style="color: #A98BF5">Partnerships · 2026/2027</div>
<h1>Partner with <span>Sunway Robotics Club.</span></h1>
<p class="lede">A year-long partnership puts your name on the workshops and outreach sessions we run, your hardware in members' hands, and a report you can use for CSR at the end of every semester.</p>
<div class="btns">
<a class="btn pri" href="#talk">Request the proposal →</a>
<a class="btn sec" href="#tiers">See the tiers</a>
</div>
<div class="stats" id="reach">
<div><span class="lb" style="color: #A9A6AE">Members</span><b>400+</b></div>
<div><span class="lb" style="color: #A9A6AE">Instagram followers</span><b>1,000+</b></div>
<div><span class="lb" style="color: #A9A6AE">Monthly impressions</span><b>15K+</b></div>
<div><span class="lb" style="color: #A9A6AE">Per campus showcase</span><b>800+</b></div>
</div>
</div>
</section>

<!-- ======= WHY ======= -->
<section class="light">
<div class="wrap">
<div class="head">
<div><div class="lb dash" style="color: #6A44BE; margin-bottom: 18px">Why partner with us</div><h2 class="rv">More than a logo on a banner</h2></div>
<p>Ten hands-on workshops a year, robots built for Robocon and combat robotics, an outreach session with a partner NGO each semester, and industry visits and talks.</p>
</div>
<div class="why">
<div class="rv"><h3>Your name on what we build</h3><p>Partners name our workshops and outreach sessions, so your brand is attached to something members and children actually make.</p></div>
<div class="rv2"><h3>Your hardware in members' hands</h3><p>Donated components go straight into workshop kits. Members learn on your parts and keep using them in their own projects.</p></div>
<div class="rv3"><h3>Impact you can report</h3><p>Every partner gets an end-of-semester report with photos, attendance and a spending breakdown, ready for your CSR or ESG reporting.</p></div>
</div>
<div class="head" style="margin: 96px 0 0"><div><div class="lb dash" style="color: #6A44BE">Where your sponsorship goes</div></div></div>
<div class="goes" style="margin-top: 28px">
<div class="rv"><h3>Hardware &amp; components</h3><p>Microcontrollers, motor drivers, sensors, servos, custom PCBs and batteries.</p></div>
<div class="rv2"><h3>Prototyping &amp; fabrication</h3><p>3D printing filament, laser cutting and workshop tooling.</p></div>
<div class="rv3"><h3>Community outreach</h3><p>Build kits and transport for NGO outreach sessions.</p></div>
<div class="rv"><h3>Member development</h3><p>Entry fees and transport for external robotics competitions.</p></div>
</div>
</div>
</section>

<!-- ======= TIERS ======= -->
<section id="tiers" class="dark">
<div class="glow" aria-hidden="true"></div>
<div class="wrap" style="position: relative">
<div class="head">
<div><div class="lb dash" style="color: #A98BF5; margin-bottom: 18px">Annual partnership tiers</div><h2 class="rv">Four ways to take part</h2></div>
<p>Each tier covers the 2026/2027 academic year and has a fixed number of places, so the benefits stay meaningful.</p>
</div>
<div class="tiers">
{''.join(tier(*t) for t in TIERS)}
</div>
<p class="all rv"><b>Every tier:</b> your logo on the slides of every workshop and on the pit kit banner that travels with our teams to competitions, plus an end-of-semester report three times a year.</p>
<div class="inkind rv">
<div><span class="lb" style="color: #C9B6FF">In-kind support</span>
<p>This year we're looking for a 3D printer and electronics components: microcontrollers, sensors, servos and motors. Contributions are valued at retail price and matched to the tier of the same value, and a donated 3D printer carries your name in our lab.</p></div>
<a class="btn sec" href="#talk">Discuss in-kind support →</a>
</div>
</div>
</section>

<!-- ======= HOW IT WORKS ======= -->
<section class="light">
<div class="wrap">
<div class="head"><div><div class="lb dash" style="color: #6A44BE; margin-bottom: 18px">How it works</div><h2 class="rv">From first email to first workshop</h2></div></div>
<ol class="steps" style="margin: 0; padding: 0">
<li class="rv"><span class="n">01</span><h3>Request the proposal</h3><p>Email us and we'll send the full 2026/2027 proposal with every benefit by tier.</p></li>
<li class="rv2"><span class="n">02</span><h3>Choose a tier</h3><p>Pick a monetary tier or an in-kind package, and the workshops you'd like to name.</p></li>
<li class="rv3"><span class="n">03</span><h3>Sign the commitment form</h3><p>Sign the form in the proposal and email it back. We'll issue an official invoice.</p></li>
<li class="rv"><span class="n">04</span><h3>Send your brand assets</h3><p>Logo (AI, SVG or transparent PNG, at least 900 × 900 px), a short company profile and your social links.</p></li>
</ol>
<div class="plate rv"><span class="slab">With support from</span><div class="logos">{logos}</div></div>
</div>
</section>

<!-- ======= CONTACT ======= -->
<section id="talk" class="dark">
<div class="glow" aria-hidden="true"></div>
<div class="wrap talk" style="position: relative">
<div>
<div class="lb dash" style="color: #A98BF5; margin-bottom: 18px">Contact</div>
<h2 class="rv">Let's talk <span style="color: #A98BF5">partnership.</span></h2>
<div class="who" style="margin-top: 40px"><span class="lb" style="color: #A9A6AE">Contact person</span><b>Christopher Chan Yan Kai</b><span>President, Sunway Robotics Club</span></div>
</div>
<div class="rows">
<a class="row" href="mailto:sunwayroboticsclub@gmail.com"><span><small class="lb" style="color: #A9A6AE">Email</small><strong>sunwayroboticsclub@gmail.com</strong></span><span>→</span></a>
<a class="row" href="tel:+60166217383"><span><small class="lb" style="color: #A9A6AE">Phone / WhatsApp</small><strong>+60 16-621 7383</strong></span><span>→</span></a>
<a class="row" href="https://www.linkedin.com/in/sunwayrobotics/"><span><small class="lb" style="color: #A9A6AE">LinkedIn</small><strong>Sunway Robotics Club</strong></span><span>↗</span></a>
<a class="row" href="https://www.instagram.com/sunwayrobotics/"><span><small class="lb" style="color: #A9A6AE">Instagram</small><strong>@sunwayrobotics</strong></span><span>↗</span></a>
</div>
</div>
</section>
</main>

{footer}

</div>"""

logic = '''<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1440,"height":4800}}'>
class Component extends DCLogic {
  constructor(props) {
    super(props);
    this.state = { menu: false };
  }
  renderVals() {
    const menu = this.state.menu;
    return {
      menuOpen: menu,
      menuClosed: !menu,
      menuAria: menu ? 'Close menu' : 'Open menu',
      menuExpanded: menu ? 'true' : 'false',
      toggleMenu: () => this.setState({ menu: !menu }),
      closeMenu: () => this.setState({ menu: false })
    };
  }
}
</script>'''
head = m[:m.index('<helmet>')]
head = head.replace(head[head.index('<title>'):head.index('</title>') + 8], '<title>Partner with Sunway Robotics Club</title>')
out = head + '<helmet>' + style + '</helmet>\n' + body + '\n</x-dc>\n' + logic + '\n</body>\n</html>\n'
open(B + 'Sponsors.dc.html', 'w').write(out)
print(len(out))
