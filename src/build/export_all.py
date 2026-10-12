"""Export the three .dc.html pages as linked standalone HTML files (images/video embedded)."""
import re, base64, io, sys, os
from PIL import Image
B = '/tmp/claude-0/-home-claude/56e6067c-1d8d-5144-a461-fa0e85a4a472/scratchpad/'
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else B + 'out/site/'
os.makedirs(OUTDIR, exist_ok=True)
IMG = B + 'img/'
SITE = os.environ.get('SITE') == '1'
PAGES = ({'Main.dc.html': 'index.html', 'Newsletter.dc.html': 'the-circuit.html', 'Sponsors.dc.html': 'partners.html'} if SITE else
         {'Main.dc.html': 'src-website-home.html', 'Newsletter.dc.html': 'src-the-circuit.html', 'Sponsors.dc.html': 'src-partners.html'})
TITLES = {'Main.dc.html': 'Sunway Robotics Club — a space to build, for everyone',
          'Newsletter.dc.html': 'The Circuit — Sunway Robotics Club weekly newsletter',
          'Sponsors.dc.html': 'Partner with Sunway Robotics Club'}

blobs = {
    'd5a189f1a62492049e2fcbeaccb5505e': (IMG + 'pcb_wide.jpg', 'image/jpeg', True),
    '7c9e85d6686d3dbb18d56e4a71b7925d': (IMG + 'pcb_wide2.jpg', 'image/jpeg', True),
    '98af6eaff0664d1765e3454ed6a687dd': (IMG + 'arena_wide.jpg', 'image/jpeg', True),
    'a9713452ccd110548c632b359bf45159': (IMG + 'blueprint_wide.jpg', 'image/jpeg', True),
    'ce5c76518d966e948c5fdad15b702b93': (IMG + 'card_booth.jpg', 'image/jpeg', True),
}
for line in open(B + 'hero/web/blobs.txt'):
    if line.strip():
        i, p, mt = line.split(); blobs[i] = (p, mt, False)
for line in open(B + 'photos/blobs.txt'):
    if line.strip():
        i, f = line.split()
        blobs[i] = (B + 'photos/' + f, 'image/png' if f.endswith('.png') else 'image/jpeg', not f.endswith('.png'))

def embed(body):
    for k, (path, mt, recompress) in blobs.items():
        if '/_blob/' + k not in body: continue
        if SITE:
            os.makedirs(OUTDIR + 'assets', exist_ok=True)
            name = os.path.basename(path)
            if recompress:
                im = Image.open(path); im.thumbnail((2000, 2000) if 'wide' in path else (960, 1200))
                name = os.path.splitext(name)[0] + '.jpg'; im.convert('RGB').save(OUTDIR + 'assets/' + name, 'JPEG', quality=80, optimize=True, progressive=True)
            else:
                open(OUTDIR + 'assets/' + name, 'wb').write(open(path, 'rb').read())
            body = body.replace('/_blob/' + k, 'assets/' + name)
            continue
        if recompress:
            im = Image.open(path); im.thumbnail((1600, 1600) if 'wide' in path else (720, 900))
            buf = io.BytesIO(); im.save(buf, 'JPEG', quality=74, optimize=True, progressive=True); raw = buf.getvalue()
        else:
            raw = open(path, 'rb').read()
        body = body.replace('/_blob/' + k, 'data:' + mt + ';base64,' + base64.b64encode(raw).decode())
    return body

FAV = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%2728 29 190 277%27%3E%3Crect x=%2732%27 y=%2733%27 width=%27182%27 height=%27269%27 fill=%27%230B0B0C%27 stroke=%27%23A98BF5%27 stroke-width=%2716%27/%3E%3Cpolygon points=%2790,64 156,64 156,136 90,136%27 fill=%27%23A98BF5%27/%3E%3Cpolygon points=%2765,162 183,162 183,242%27 fill=%27%23A98BF5%27/%3E%3Cpolygon points=%2765,204 65,282 182,282%27 fill=%27%23A98BF5%27/%3E%3C/svg%3E">\n<meta name="description" content="Sunway Robotics Club: a student robotics lab at Sunway University, Bandar Sunway, Malaysia. Workshops, projects and competitions, open to everyone.">\n<meta property="og:title" content="Sunway Robotics Club">\n<meta property="og:description" content="A space to build, for everyone.">\n'
MQ = '(max-width: 760px), (orientation: portrait)'
JS = r'''<script>
(function(){
  var S={menu:false,done:false};
  function pad(n){return String(n).padStart(2,'0');}
  function V(){
    var d=new Date(Date.now()+8*3600000);
    var days=Math.max(0,Math.ceil((new Date('2027-08-29T00:00:00+08:00').getTime()-Date.now())/86400000));
    return {menuOpen:S.menu,menuClosed:!S.menu,menuExpanded:S.menu?'true':'false',menuAria:S.menu?'Close menu':'Open menu',
      done:S.done,notDone:!S.done,showRender:true,daysLeft:String(days),
      clock:pad(d.getUTCHours())+':'+pad(d.getUTCMinutes())+':'+pad(d.getUTCSeconds())+' — '+d.getUTCFullYear()+'-'+pad(d.getUTCMonth()+1)+'-'+pad(d.getUTCDate())};
  }
  function render(){
    var v=V();
    document.querySelectorAll('x-if').forEach(function(e){e.hidden=!v[e.getAttribute('data-if')];});
    document.querySelectorAll('[data-text]').forEach(function(e){e.textContent=v[e.getAttribute('data-text')];});
    document.querySelectorAll('[data-bind]').forEach(function(e){e.getAttribute('data-bind').split(',').forEach(function(p){var kv=p.split(':');e.setAttribute(kv[0],v[kv[1]]);});});
    document.documentElement.style.overflow=S.menu?'hidden':'';
  }
  var A={toggleMenu:function(){S.menu=!S.menu;},closeMenu:function(){S.menu=false;},submit:function(e){e.preventDefault();S.done=true;},
    scrollPrev:function(){var h=document.querySelector('#work .hs');if(h)h.scrollBy({left:-h.clientWidth*0.9,behavior:'smooth'});},
    scrollNext:function(){var h=document.querySelector('#work .hs');if(h)h.scrollBy({left:h.clientWidth*0.9,behavior:'smooth'});}};
  document.addEventListener('click',function(e){var t=e.target.closest('[data-on-click]');if(t){A[t.getAttribute('data-on-click')](e);render();}});
  document.addEventListener('submit',function(e){var t=e.target.closest('[data-on-submit]');if(t){A[t.getAttribute('data-on-submit')](e);render();}});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&S.menu){S.menu=false;render();}});
  render(); setInterval(render,1000);
  var vd=document.querySelector('.herovid');
  if(vd){var mob=window.matchMedia&&window.matchMedia('MQ').matches;if(mob&&vd.dataset.mposter)vd.poster=vd.dataset.mposter;
    var ss=vd.querySelectorAll('source');var want=mob?ss[0]:ss[ss.length-1];if(want&&vd.currentSrc&&vd.currentSrc!==want.src){vd.src=want.src;}
    vd.muted=true;var pr=vd.play();if(pr&&pr.catch)pr.catch(function(){});}
})();
</script>'''.replace('MQ', MQ)

for src_name, out_name in PAGES.items():
    src = open(B + 'canvas/project/' + src_name).read()
    head = src.split('<helmet>')[1].split('</helmet>')[0]
    body = src.split('</helmet>')[1].split('</x-dc>')[0]
    # hero: drop the unused stand-in / placeholder variants
    body = re.sub(r'<sc-if value="\{\{ showStandIn \}\}".*?</svg>\n</sc-if>\n', '', body, flags=re.S)
    body = re.sub(r'<sc-if value="\{\{ showVideo \}\}".*?</sc-if>\n', '', body, flags=re.S)
    body = body.replace('ref="{{ setVid }}" autoPlay="{{ true }}" muted="{{ true }}" loop="{{ true }}" playsInline="{{ true }}"', 'autoplay muted loop playsinline preload="auto"')
    body = body.replace('</source>', '')
    # conditionals
    body = re.sub(r'<sc-if value="\{\{ (\w+) \}\}" hint-placeholder-val="\{\{ (true|false) \}\}">',
                  lambda m: '<x-if data-if="%s"%s>' % (m.group(1), '' if m.group(2) == 'true' else ' hidden'), body)
    body = body.replace('</sc-if>', '</x-if>')
    # events
    body = re.sub(r'onClick="\{\{ (\w+) \}\}"', r'data-on-click="\1"', body)
    body = re.sub(r'onSubmit="\{\{ (\w+) \}\}"', r'data-on-submit="\1"', body)
    # bound attributes: collect per tag
    def bind_tag(m):
        tag = m.group(0)
        pairs = re.findall(r'([a-zA-Z-]+)="\{\{ (\w+) \}\}"', tag)
        if not pairs: return tag
        for a, n in pairs:
            tag = tag.replace('%s="{{ %s }}"' % (a, n), '')
        return tag[:-1].rstrip() + ' data-bind="%s">' % ','.join('%s:%s' % p for p in pairs)
    body = re.sub(r'<[a-zA-Z][^<>]*\{\{[^<>]*>', bind_tag, body)
    # text holes
    body = re.sub(r'\{\{ (\w+) \}\}', r'<span data-text="\1"></span>', body)
    # page links
    for a, b in PAGES.items():
        body = body.replace('href="' + a, 'href="' + b)
    body = embed(body)
    left = re.findall(r'\{\{[^}]*\}\}|<sc-|/_blob/|\.dc\.html', body)
    html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>' + TITLES[src_name] + '</title>\n' + FAV + head +
            '<style>html{scroll-behavior:smooth}[hidden]{display:none !important}x-if{display:contents}</style>\n</head>\n<body>\n'
            + body.strip() + '\n' + JS + '\n</body>\n</html>\n')
    open(OUTDIR + out_name, 'w').write(html)
    print(out_name, len(html) // 1024, 'KB', 'leftovers:', left[:5])
