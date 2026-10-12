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
.pp .tiers{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.pp .tier{padding:30px 28px 32px;background:rgba(255,255,255,0.03);border:1px solid #2E2C34;display:flex;flex-direction:column}
.pp .tier.top{border-color:#7852C1;background:rgba(120,82,193,0.10)}
.pp .tier .nm{display:flex;justify-content:space-between;align-items:center;gap:12px}
.pp .tier .tag{padding:5px 9px;border:1px solid #A98BF5;color:#C9B6FF;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.pp .tier .pr{margin:18px 0 22px;font-weight:500;font-size:44px;letter-spacing:-0.03em;line-height:1}
.pp .tier ul{margin:0;padding:0;list-style:none;border-top:1px solid #2E2C34}
.pp .tier li{padding:12px 0;border-bottom:1px solid #2E2C34;font-size:15px;line-height:1.5;color:#C9C6CF;display:flex;gap:12px}
.pp .tier li::before{content:"";flex:0 0 6px;height:6px;margin-top:8px;background:#A98BF5}
.pp .inkind{position:relative;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:20px 40px;margin-top:20px;padding:28px;border:1px solid #2E2C34}
.pp .inkind p{margin:8px 0 0;max-width:700px;color:#C9C6CF;font-size:15px;line-height:1.6}
.pp .steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid #0B0B0C}
.pp .steps li{list-style:none;padding:22px 24px 8px 0}
.pp .steps li + li{padding-left:24px;border-left:1px solid #CFCAD8}
.pp .steps .n{font-weight:500;font-size:15px;color:#6A44BE}
.pp .steps h3{margin:12px 0 8px;font-weight:500;font-size:21px;letter-spacing:-0.01em}
.pp .steps p{margin:0;color:#4A4752;font-size:15px;line-height:1.55}
.pp .plate{display:grid;grid-template-columns:auto minmax(0,1fr);align-items:center;gap:20px 48px;margin-top:88px;padding:26px 32px;background:#FFFFFF;border:1px solid #DCD8D0}
.pp .plate .slab{font-size:14px;font-weight:500;color:#6B6862;white-space:nowrap}
.pp .plate .logos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));align-items:center;gap:24px}
.pp .plate .logos div{height:72px;display:flex;align-items:center;justify-content:center}
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
.pp .plate{grid-template-columns:minmax(0,1fr);padding:20px 18px;gap:14px;margin-top:64px}.pp .plate .logos{gap:14px}.pp .plate .logos div{height:52px}}
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

PLAT = ['Dedicated feature post and three story mentions on Instagram and LinkedIn',
        'Standalone bunting, plus the largest top-placed logo on poster, banner, bunting and certificates',
        'Dedicated sponsor slide and top banner placement at the arena',
        'Emcee mentions at opening, award and closing ceremonies on both days',
        'Standalone thank-you post and feature in the highlight video',
        'Framed certificate and 3D-printed award presented on stage', 'Full event photo package']
GOLD = ['One post and two story mentions before the event', 'Top-row logo on poster, banner, bunting and certificates',
        'Side display near the audience area', 'Emcee mentions at the ceremonies', 'Shared thank-you post and logo in the highlight video',
        'Framed certificate and 3D-printed award, delivered after the event', 'Included in the photo highlight set']
SILV = ['Inclusion in the collective sponsor appreciation post', 'Logo on the bottom row of the bunting', 'Logo in the shared sponsor reel on screen',
        'Emcee mention on competition day', 'Framed certificate and thank-you email']

logos = ''.join(f'<div><img src="/_blob/{i}" alt="{a}" loading="lazy"></div>' for i, a in LOGOS)

body = f"""{wrap_open}
{nav}

<main class="pp">
<!-- ======= HERO ======= -->
<section id="top" class="hero">
<img class="bg" src="/_blob/{IMG['proton']}" alt="" aria-hidden="true">
<div class="shade" aria-hidden="true"></div>
<div class="wrap">
<div class="lb dash" style="color: #A98BF5">Partnerships</div>
<h1>Partner with <span>Sunway Robotics Club.</span></h1>
<p class="lede">Sponsorship funds the components, prizes and meals at our workshops and competitions, and puts your brand in front of the people who build there.</p>
<div class="btns">
<a class="btn pri" href="#talk">Request a proposal →</a>
<a class="btn sec" href="#tiers">See the tiers</a>
</div>
<div class="stats" id="reach">
<div><span class="lb" style="color: #A9A6AE">Members</span><b>400+</b></div>
<div><span class="lb" style="color: #A9A6AE">Followers</span><b>1,200+</b></div>
<div><span class="lb" style="color: #A9A6AE">Views in 30 days</span><b>60K+</b></div>
<div><span class="lb" style="color: #A9A6AE">On LinkedIn</span><b>1,000+</b></div>
</div>
<p class="note">Views and LinkedIn connections as of November 2025.</p>
</div>
</section>

<!-- ======= TRACK RECORD ======= -->
<section class="light">
<div class="wrap">
<div class="head">
<div><div class="lb dash" style="color: #6A44BE; margin-bottom: 18px">Track record</div><h2 class="rv">What your support goes into</h2></div>
<p>Workshops, competitions, talks and campus showcases, run by Sunway Robotics Club.</p>
</div>
<article class="feature rv">
<div class="ph"><img src="/_blob/{IMG['dodgebots']}" alt="Dodgebots 2025 participants and organisers on the arena stage" loading="lazy"></div>
<div class="tx">
<span class="lb" style="color: #6A44BE">Flagship event · Nov–Dec 2025</span>
<h3>Dodgebots 2025</h3>
<p>A robotics workshop followed by a knockout tournament. Teams built robots over two weeks with mentor guidance, then competed at The Zone.</p>
<div class="chips"><span>12 teams</span><span>36 participants</span><span>2 event days</span></div>
</div>
</article>
<div class="grid4">
{rec('servo', 'Workshops', 'Servo Arm, Ottobot and LED Tetris', 'Hands-on builds where every participant leaves with a working project.', 'Robot arms built at the Servo Arm Workshop')}
{rec('robocon', 'Competitions', 'Robocon Malaysia 2025 and Vibathon 2026', 'A national Robocon round at UTHM, and runner-up at the Mercedes-Benz Vibathon 2026.', 'The Sunway team at Robocon Malaysia 2025')}
{rec('talk', 'Talks', 'Combat robotics with Fikri', 'A talk for members on designing and building combat robots.', 'Fikri presenting on combat robotics')}
{rec('ecx', 'Campus', 'CnS Week and ECX Week booths', 'Live demos of member projects for visitors across campus.', 'Sunway Robotics Club at ECX Week')}
</div>
</div>
</section>

<!-- ======= TIERS ======= -->
<section id="tiers" class="dark">
<div class="glow" aria-hidden="true"></div>
<div class="wrap" style="position: relative">
<div class="head">
<div><div class="lb dash" style="color: #A98BF5; margin-bottom: 18px">Sponsorship tiers</div><h2 class="rv">Three ways to take part</h2></div>
<p>Example tiers from Dodgebots 2025. Each event has its own proposal, with tiers set to its budget.</p>
</div>
<div class="tiers">
{tier('Platinum', 'RM2,500', PLAT, True)}
{tier('Gold', 'RM1,800', GOLD)}
{tier('Silver', 'RM1,000', SILV)}
</div>
<div class="inkind rv">
<div><span class="lb" style="color: #C9B6FF">Non-monetary sponsorship</span>
<p>We also accept components such as microcontrollers, motors and sensors, as well as meals, prizes and equipment. Benefits are agreed with the committee.</p></div>
<a class="btn sec" href="#talk">Discuss in-kind support →</a>
</div>
</div>
</section>

<!-- ======= HOW IT WORKS ======= -->
<section class="light">
<div class="wrap">
<div class="head"><div><div class="lb dash" style="color: #6A44BE; margin-bottom: 18px">How it works</div><h2 class="rv">From first email to event day</h2></div></div>
<ol class="steps" style="margin: 0; padding: 0">
<li class="rv"><span class="n">01</span><h3>Request a proposal</h3><p>Tell us which event you'd like to support and we'll send its proposal and budget.</p></li>
<li class="rv2"><span class="n">02</span><h3>Choose a tier</h3><p>Pick a monetary tier or an in-kind package.</p></li>
<li class="rv3"><span class="n">03</span><h3>Sign the commitment form</h3><p>Complete the Partnership Commitment Form included with the proposal.</p></li>
<li class="rv"><span class="n">04</span><h3>Send your logos</h3><p>Coloured and black-and-white versions, PNG, at least 900 × 900 px, by the date in the proposal.</p></li>
</ol>
<div class="plate rv"><span class="slab">Supported by</span><div class="logos">{logos}</div></div>
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
<a class="row" href="tel:+60166217383"><span><small class="lb" style="color: #A9A6AE">Phone / WhatsApp</small><strong>016-621 7383</strong></span><span>→</span></a>
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
