D='/tmp/claude-0/-home-claude/56e6067c-1d8d-5144-a461-fa0e85a4a472/scratchpad/gen/'
s=''.join(open(D+f).read() for f in ['hero4_head.py','h6_a.py','h6_logo.py','h6_panel.py','h7_arms.py','h9_bg.py','h6_tail.py'])
rep=[("for u, v in ((0, 0.4), (.03, 0.4), (.09, 2.2), (.64, 2.2), (.67, 7), (.73, 3), (1, 3)):","for u, v in ((0, 0.4), (.03, 0.4), (.09, 2.2), (.585, 2.2), (.61, 7), (.67, 3), (1, 3)):"),
("float(os.environ.get('ZOOM0', '0.68')), float(os.environ.get('ZOOM1', '0.84'))","float(os.environ.get('ZOOM0', '0.64')), float(os.environ.get('ZOOM1', '0.81'))"),
("area('rimL', (-8, 4, 5),","area('rimL', (-8, 2.4, 5),"),("area('rimR', (8, 4, 5),","area('rimR', (8, 2.4, 5),"),
("cam.data.dof.aperture_fstop = 5.6","cam.data.dof.aperture_fstop = float(os.environ.get('FSTOP', '4.0'))")]
for a,b in rep:
    assert a in s, a[:40]; s=s.replace(a,b)
open(D+'hero9.py','w').write(s)
