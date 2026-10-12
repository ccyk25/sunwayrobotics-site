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

extra_css = """
.soon{position:relative;overflow:hidden;background:#0B0B0C;color:#FFFFFF;min-height:calc(100vh - 61px);display:flex;flex-direction:column}
.soon .pcb{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:70% 50%}
.soon .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(11,11,12,0.94) 0%,rgba(11,11,12,0.78) 42%,rgba(11,11,12,0.28) 100%),linear-gradient(180deg,rgba(11,11,12,0) 60%,rgba(11,11,12,0.9) 100%)}
.soon .glow{position:absolute;width:1000px;height:1000px;right:-320px;top:-380px;border-radius:50%;background:radial-gradient(circle,rgba(120,82,193,0.26),rgba(120,82,193,0) 66%);pointer-events:none}
.soon .glow2{position:absolute;width:760px;height:760px;left:-340px;bottom:-420px;border-radius:50%;background:radial-gradient(circle,rgba(120,82,193,0.14),rgba(120,82,193,0) 66%);pointer-events:none}
.soon .inner{position:relative;z-index:1;flex:1 0 auto;display:flex;flex-direction:column;justify-content:center;width:100%;box-sizing:border-box;max-width:1408px;margin:0 auto;padding:80px 24px 72px}
.soon .row > div{min-width:0;max-width:100%}
.soon h1{margin:22px 0 0;font-weight:500;font-size:clamp(60px,14.5vw,224px);line-height:.88;letter-spacing:-0.045em}
.soon h1 span{color:#A98BF5}
.soon .row{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:28px 48px;margin-top:40px}
.soon .chip{display:inline-flex;align-items:center;gap:10px;padding:9px 16px;background:rgba(11,11,12,0.55);border:1px solid rgba(169,139,245,0.55);color:#DCD0FA;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.soon .chip i{width:8px;height:8px;background:#A98BF5;animation:pulse 2s ease-out infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(169,139,245,.55)}100%{box-shadow:0 0 0 12px rgba(169,139,245,0)}}
.soon p.lede{margin:18px 0 0;max-width:540px;font-size:clamp(17px,1.4vw,19px);line-height:1.6;color:#B9B6C1}
.soon .ctas{display:flex;flex-wrap:wrap;gap:12px}
.soon .cta{display:inline-flex;align-items:center;gap:8px;padding:14px 22px;font-size:15px;font-weight:500;text-decoration:none;transition:background-color .2s,color .2s,border-color .2s}
.soon .cta.pri{background:#7852C1;color:#FFFFFF}.soon .cta.pri:hover{background:#6A44BE}
.soon .cta.sec{border:1px solid #FFFFFF;color:#FFFFFF;background:rgba(11,11,12,0.35)}.soon .cta.sec:hover{background:#FFFFFF;color:#0B0B0C}
/* measuring scale */
.ruler{position:relative;z-index:1;height:46px;overflow:hidden;
 background:
  repeating-linear-gradient(90deg,#9C99A6 0 1px,transparent 1px 100px) left bottom/100% 24px no-repeat,
  repeating-linear-gradient(90deg,#5E5B68 0 1px,transparent 1px 50px) left bottom/100% 15px no-repeat,
  repeating-linear-gradient(90deg,#3A3842 0 1px,transparent 1px 10px) left bottom/100% 8px no-repeat}
.ruler span{position:absolute;bottom:27px;transform:translateX(5px);font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10px;letter-spacing:.04em;color:#7E7B88}
.ruler .cur{position:absolute;bottom:0;width:2px;height:30px;background:#A98BF5;box-shadow:0 0 12px rgba(169,139,245,.8);animation:scan 9s ease-in-out infinite alternate}
.ruler .cur::before{content:"";position:absolute;top:-6px;left:-4px;border:5px solid transparent;border-top:6px solid #A98BF5}
@keyframes scan{from{left:6%}to{left:92%}}
.soon .ruler{background-color:rgba(11,11,12,0.6)}
/* moving words */
.strip{position:relative;z-index:1;overflow:hidden;border-top:1px solid #2A2A2E;background:#0B0B0C}
.strip .track2{display:flex;width:max-content;animation:nlmq 38s linear infinite}
.strip .grp{display:flex;align-items:center;gap:30px;padding:16px 15px;font-size:13px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#8E8C95;white-space:nowrap}
.strip .grp b{color:#FFFFFF;font-weight:600}.strip .grp em{font-style:normal;color:#7852C1}
@keyframes nlmq{to{transform:translateX(-50%)}}
@media (max-width: 760px){.soon .inner{padding:64px 24px 56px}.soon .row{margin-top:28px}}
@media (prefers-reduced-motion: reduce){.soon .chip i,.ruler .cur,.strip .track2{animation:none}}
"""
style = style.replace('</style>', extra_css + '</style>')

nums = ''.join('<span style="left: %dpx">%d</span>' % (i * 100, i * 10) for i in range(0, 40))
words = ['<b>Coming soon</b>', 'From the lab', 'Builds &amp; workshops', 'Coming up', 'Events &amp; competitions', 'Opportunities', 'First issue in the works']
grp = '<div class="grp">' + ''.join(w + '<em>/</em>' for w in words) + '</div>'

body = f"""{wrap_open}
{nav}

<!-- ======= THE CIRCUIT: COMING SOON ======= -->
<main id="top" class="soon">
<img class="pcb" src="/_blob/dac79e1c7f1740164755286178d227e4" alt="" aria-hidden="true"><div class="shade" aria-hidden="true"></div>
<div class="inner">
<div class="lb dash" style="color: #A98BF5">Sunway Robotics Club newsletter</div>
<h1>The <span>Circuit</span></h1>
<div class="row">
<div>
<div class="chip"><i aria-hidden="true"></i>Coming soon</div>
<p class="lede">What members are building, what's coming up, and opportunities worth applying for, all in one short read. The first issue is in the works.</p>
</div>
<div class="ctas">
<a class="cta pri" href="https://www.instagram.com/sunwayrobotics/">Follow us for the launch ↗</a>
<a class="cta sec" href="Main.dc.html">Back to home</a>
</div>
</div>
</div>
<div class="ruler" aria-hidden="true">{nums}<i class="cur"></i></div>
<div class="strip" aria-hidden="true"><div class="track2">{grp}{grp}</div></div>
</main>

{footer}

</div>"""

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
