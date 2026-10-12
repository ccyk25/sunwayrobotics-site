from PIL import Image, ImageOps, ImageChops
import pillow_heif, numpy as np, os
pillow_heif.register_heif_opener()
B='/tmp/claude-0/-home-claude/56e6067c-1d8d-5144-a461-fa0e85a4a472/scratchpad/'
SRC=B+'photos_in/src website/'; OUT=B+'photos/'
def load(n): return ImageOps.exif_transpose(Image.open(SRC+n)).convert('RGB')
def crop(im, ar, fx=.5, fy=.5):
    w,h=im.size
    if w/h > ar: nw=int(h*ar); x=int(min(max(fx*w-nw/2,0),w-nw)); return im.crop((x,0,x+nw,h))
    nh=int(w/ar); y=int(min(max(fy*h-nh/2,0),h-nh)); return im.crop((0,y,w,y+nh))
def grade(im):
    # natural colour: gentle contrast + a touch of saturation, no lifted shadows
    from PIL import ImageEnhance
    im = ImageEnhance.Contrast(im).enhance(1.07)
    im = ImageEnhance.Color(im).enhance(1.06)
    return im
def save(im, name, maxw, maxh):
    im=grade(im); im.thumbnail((maxw,maxh), Image.LANCZOS); im.save(OUT+name, 'JPEG', quality=88, optimize=True, progressive=True, subsampling=0); print(name, im.size)
C=(960,1200); R=(1200,900); W=(2400,2400)
cards=[('card_vibathon.jpg','mercedes vibathon.jpeg',.37,.5),('card_robocon.jpg','robocon team pic.png',.5,.5),
 ('card_dodgebots.jpg','dodgebot.HEIC',.5,.55),('card_talk.jpg','combat robot talk.heic',.36,.5),
 ('card_servo.jpg','servo arm worshop.jpg',.5,.55),('card_ottobot.jpg','ottobots.png',.5,.5),
 ('card_tetris.jpg','tetris 2.JPG',.5,.5),('card_plc.jpg','plc worshop 1.jpeg',.55,.5),
 ('card_turtlebot.jpg','turtlebot worshop.jpeg',.5,.6),('card_3d.jpg','3d model workshop.HEIC',.5,.5),
 ('card_festo.jpg','festo vst.HEIC',.5,.5),('card_proton.jpg','proton vst.HEIC',.5,.5)]
for o,s,fx,fy in cards: save(crop(load(s),4/5,fx,fy),o,*C)
rows=[('row_workshops.jpg','plc worshop 2.jpeg',.5,.5),('row_projects.jpg','tetris.png',.5,.5),('row_host.jpg','dodgebot.HEIC',.5,.62),
 ('row_enter.jpg','mercedes vibathon.jpeg',.5,.5),('row_talks.jpg','combat robot talk.heic',.5,.5),('row_circuit.jpg','turtlebot worshop.jpeg',.5,.6)]
for o,s,fx,fy in rows: save(crop(load(s),4/3,fx,fy),o,*R)
for o,s in [('wide_band.jpg','3d model workshop.HEIC'),('wide_next.jpg','robocon team pic.png'),('wide_join.jpg','proton vst.HEIC')]: save(load(s),o,*W)
for o,s in [('logo_jcf.png','JCF EXTERNAL   .jpg'),('logo_cwac.png','CWAC_logo.jpg'),('logo_sunwaycollege.png','Sunway-College-logo 2022.jpg')]:
    im=load(s); bg=Image.new('RGB',im.size,(255,255,255)); bb=ImageChops.difference(im,bg).convert('L').point(lambda v:255 if v>18 else 0).getbbox()
    im=im.crop(bb); im.thumbnail((640,320),Image.LANCZOS); im.save(OUT+o,optimize=True); print(o,im.size)

save(crop(load('ecx group.jpg'),4/5,.47,.5),'card_ecx2.jpg',960,1200)
save(load('ecx faculty.jpg'),'wide_join3.jpg',2400,2400)
