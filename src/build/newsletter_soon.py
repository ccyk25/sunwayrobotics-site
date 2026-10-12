"""Rebuild The Circuit page as a clean 'coming soon' page that shares the homepage's nav, type and footer."""
B = '/tmp/claude-0/-home-claude/56e6067c-1d8d-5144-a461-fa0e85a4a472/scratchpad/canvas/project/'
m = open(B + 'Main.dc.html').read()
lines = m.split('\n')
style = m[m.index('<helmet>') + len('<helmet>'):m.index('</helmet>')]
nav = m[m.index('<nav aria-label="Main"'):m.index('</sc-if>', m.index('<sc-if value="{{ menuOpen }}"')) + len('</sc-if>')]
footer = m[m.index('<footer id="contact"'):m.index('</footer>') + len('</footer>')]
for a, b in (('href="#work"', 'href="Main.dc.html#work"'), ('href="#top"', 'href="Main.dc.html"')):
    nav = nav.replace(a, b); footer = footer.replace(a, b)
nav = nav.replace('<a href="Newsletter.dc.html" class="ul" style="text-decoration: none">The Circuit</a>',
                  '<a href="Newsletter.dc.html" class="ul" aria-current="page" style="text-decoration: none; color: #C9B6FF">The Circuit</a>')
wrap_open = m[m.index('<div', m.index('</helmet>')):m.index('>', m.index('<div', m.index('</helmet>'))) + 1]

LOGO = ('<svg viewBox="28 29 190 277" aria-hidden="true" class="nlogo">'
        '<rect x="32" y="33" width="182" height="269" fill="none" stroke="#A98BF5" stroke-width="3"></rect>'
        '<polygon points="90,64 156,64 156,136 90,136" fill="none" stroke="#A98BF5" stroke-width="2"></polygon>'
        '<polygon points="65,162 183,162 183,242" fill="none" stroke="#A98BF5" stroke-width="2"></polygon>'
        '<polygon points="65,204 65,282 182,282" fill="none" stroke="#A98BF5" stroke-width="2"></polygon></svg>')

extra_css = '''
.soon{position:relative;overflow:hidden;background:#0B0B0C;color:#FFFFFF;min-height:calc(100vh - 61px);display:flex;align-items:center}
.soon .glow{position:absolute;width:900px;height:900px;right:-300px;top:-260px;border-radius:50%;background:radial-gradient(circle,rgba(120,82,193,0.28),rgba(120,82,193,0) 66%);pointer-events:none}
.soon .glow2{position:absolute;width:700px;height:700px;left:-320px;bottom:-360px;border-radius:50%;background:radial-gradient(circle,rgba(120,82,193,0.16),rgba(120,82,193,0) 66%);pointer-events:none}
.soon .nlogo{position:absolute;right:max(24px,calc((100vw - 1360px)/2 + 24px));top:50%;transform:translateY(-50%);width:min(30vw,340px);height:auto;opacity:.35}
.soon .inner{position:relative;z-index:1;width:100%;max-width:1360px;margin:0 auto;padding:96px 24px 110px}
.soon h1{margin:18px 0 0;font-weight:500;font-size:clamp(56px,9vw,132px);line-height:.95;letter-spacing:-0.03em}
.soon .chip{display:inline-flex;align-items:center;gap:10px;margin-top:28px;padding:9px 16px;border-radius:999px;background:rgba(169,139,245,0.12);border:1px solid rgba(169,139,245,0.35);color:#DCD0FA;font-size:14px;font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.soon .chip i{width:8px;height:8px;border-radius:50%;background:#A98BF5;box-shadow:0 0 0 0 rgba(169,139,245,.6);animation:pulse 2s ease-out infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(169,139,245,.55)}100%{box-shadow:0 0 0 12px rgba(169,139,245,0)}}
.soon p.lede{margin:28px 0 0;max-width:560px;font-size:clamp(17px,1.5vw,20px);line-height:1.6;color:#B9B6C1}
.soon .what{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:56px;max-width:860px}
.soon .what div{padding:20px 22px;border-radius:14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08)}
.soon .what b{display:block;font-weight:600;font-size:16px;margin-bottom:6px;color:#FFFFFF}
.soon .what span{font-size:14px;line-height:1.5;color:#A9A6AE}
.soon .ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:44px}
.soon .cta{display:inline-flex;align-items:center;gap:8px;padding:14px 22px;border-radius:999px;font-size:15px;font-weight:500;text-decoration:none;transition:background-color .2s,color .2s,border-color .2s}
.soon .cta.pri{background:#7852C1;color:#FFFFFF}.soon .cta.pri:hover{background:#6A44BE}
.soon .cta.sec{border:1px solid rgba(255,255,255,0.22);color:#FFFFFF}.soon .cta.sec:hover{border-color:#FFFFFF}
@media (max-width: 760px){.soon .what{grid-template-columns:minmax(0,1fr)}.soon .nlogo{display:none}.soon .inner{padding:72px 24px 96px}}
@media (prefers-reduced-motion: reduce){.soon .chip i{animation:none}}
'''
style = style.replace('</style>', extra_css + '</style>')

body = f'''{wrap_open}
{nav}

<!-- ======= THE CIRCUIT: COMING SOON ======= -->
<main id="top" class="soon">
<div class="glow" aria-hidden="true"></div><div class="glow2" aria-hidden="true"></div>
{LOGO}
<div class="inner">
<div class="lb dash" style="color: #A98BF5">The Circuit · Newsletter</div>
<h1>Coming soon.</h1>
<div class="chip"><i aria-hidden="true"></i>First issue in the works</div>
<p class="lede">The Circuit is the Sunway Robotics Club newsletter: what members are building, what's coming up, and opportunities worth applying for, all in one short read.</p>
<div class="what">
<div><b>From the lab</b><span>Builds, workshops and the people behind them.</span></div>
<div><b>Coming up</b><span>Events and competitions to put in your calendar.</span></div>
<div><b>Opportunities</b><span>Programmes, roles and calls worth applying for.</span></div>
</div>
<div class="ctas">
<a class="cta pri" href="https://www.instagram.com/sunwayrobotics/">Follow us for the launch ↗</a>
<a class="cta sec" href="Main.dc.html">Back to home</a>
</div>
</div>
</main>

{footer}

</div>'''

logic = m[m.index('<script type="text/x-dc"'):m.index('</script>', m.index('<script type="text/x-dc"')) + len('</script>')]
logic_new = '''<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1440,"height":1400}}'>
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
head = m[:m.index('<helmet>')].replace('<title>' + m[m.index('<title>') + 7:m.index('</title>')] + '</title>', '<title>The Circuit — Sunway Robotics Club newsletter</title>')
out = head + '<helmet>' + style + '</helmet>\n' + body + '\n</x-dc>\n' + logic_new + '\n</body>\n</html>\n'
open(B + 'Newsletter.dc.html', 'w').write(out)
print(len(out), '{{' in body)
