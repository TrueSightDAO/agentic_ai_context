import math, io, urllib.request
from PIL import Image, ImageDraw, ImageFont
UA={'User-Agent':'TrueSightDAO-brochure/1.0 (sophia@truesight.me)'}
def deg2tile(lat,lon,z):
    n=2**z; x=(lon+180.0)/360.0*n
    y=(1.0-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2.0*n
    return x,y
def fetch(x,y,z):
    for h in 'abc':
        try:
            r=urllib.request.Request(f'https://{h}.tile.openstreetmap.org/{z}/{x}/{y}.png',headers=UA)
            return Image.open(io.BytesIO(urllib.request.urlopen(r,timeout=25).read())).convert('RGB')
        except: continue
    return Image.new('RGB',(256,256),(235,235,235))
def basemap(z,clat,clon,W,H):
    cx,cy=deg2tile(clat,clon,z); px=int(cx*256-W/2); py=int(cy*256-H/2)
    tx0=px//256; ty0=py//256; tx1=(px+W)//256; ty1=(py+H)//256
    cv=Image.new('RGB',((tx1-tx0+1)*256,(ty1-ty0+1)*256),(255,255,255))
    for tx in range(tx0,tx1+1):
        for ty in range(ty0,ty1+1):
            cv.paste(fetch(tx,ty,z),((tx-tx0)*256,(ty-ty0)*256))
    return cv.crop((px-tx0*256,py-ty0*256,px-tx0*256+W,py-ty0*256+H)),(px,py)
def ll2px(la,lo,z,px,py):
    x,y=deg2tile(la,lo,z); return (x*256-px,y*256-py)
def fnt(sz,bold=True):
    p='/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'%('-Bold' if bold else '')
    try: return ImageFont.truetype(p,sz)
    except: return ImageFont.load_default()
def pin(d,x,y,num,color):
    r=16
    d.ellipse([x-r+2,y-r+3,x+r+2,y+r+3],fill=(0,0,0,70))
    d.ellipse([x-r,y-r,x+r,y+r],fill=color+(255,),outline=(255,255,255,255),width=3)
    f=fnt(17); t=str(num); tb=d.textbbox((0,0),t,font=f)
    d.text((x-(tb[2]-tb[0])/2-tb[0],y-(tb[3]-tb[1])/2-tb[1]-1),t,font=f,fill=(255,255,255,255))
CAP=(178,34,34); MUS=(20,90,150); NAT=(20,120,70); LOG=(95,95,95); CUL=(150,80,150)

def make(z,clat,clon,W,H,pts,groups,out,heading,sub):
    PAD=380
    lay,(px,py)=basemap(z,clat,clon,W,H)
    cv=Image.new('RGB',(W+PAD,H),(255,255,255)); cv.paste(lay,(0,0))
    d=ImageDraw.Draw(cv,'RGBA')
    for n,la,lo,c,_,_ in pts:
        x,y=ll2px(la,lo,z,px,py); pin(d,x,y,n,c)
    lx=W+26; ly=46
    d.text((lx,ly),heading,font=fnt(21),fill=(25,25,25)); ly+=34
    d.text((lx,ly),sub,font=fnt(12,False),fill=(110,110,110)); ly+=40
    for gtitle,gcolor,items in groups:
        d.text((lx,ly),gtitle,font=fnt(12),fill=gcolor); ly+=22
        for n,name,place in items:
            d.ellipse([lx,ly+2,lx+17,ly+19],fill=gcolor+(255,),outline=(255,255,255,255),width=2)
            f=fnt(13); tb=d.textbbox((0,0),str(n),font=f)
            d.text((lx+8.5-(tb[2]-tb[0])/2-tb[0],ly+10-(tb[3]-tb[1])/2-tb[1]),str(n),font=f,fill=(255,255,255))
            d.text((lx+26,ly),name,font=fnt(14),fill=(20,20,20))
            d.text((lx+26,ly+18),place,font=fnt(11,False),fill=(120,120,120))
            ly+=48
        ly+=6
    cv.save(out); print(out, cv.size)

# ---- TOWN (South Itacaré) ----
town=[
 (1,-14.27911,-38.99291,CAP,'Pra\u00e7a dos Cachorros',''),
 (2,-14.28042,-38.99044,CAP,'Rua Pituba',''),
 (3,-14.27488,-38.99114,CAP,'Mirante do Xar\u00e9u',''),
 (4,-14.27600,-38.98833,MUS,'Mais Que Nada',''),
 (5,-14.27654,-38.99624,MUS,'Mar\u00e9 Alta',''),
 (6,-14.27985,-38.99329,MUS,'Casa Mar\u00e9',''),
 (7,-14.28392,-38.98511,NAT,'Praia do Resende',''),
 (8,-14.27659,-38.99594,NAT,'Praia da Coroa',''),
 (9,-14.28162,-38.99522,LOG,'Rodovi\u00e1ria',''),
 (10,-14.27706,-38.99833,CUL,'Porto de Tr\u00e1s',''),
]
tg=[('CAPOEIRA',CAP,[(1,'Pra\u00e7a dos Cachorros','Sat roda \u00b7 Santos Dumont'),
                     (2,'Rua Pituba','Fri roda \u00b7 Caf\u00e9 Caramelo'),
                     (3,'Mirante do Xar\u00e9u','Sun sunset \u00b7 P\u00f4r do Sol')]),
    ('SAMBA & FORR\u00d3',MUS,[(4,'Mais Que Nada','Mon 21:00 \u00b7 P\u00e1tio-Bar'),
                     (5,'Mar\u00e9 Alta','Tue 21:00 \u00b7 Orla'),
                     (6,'Casa Mar\u00e9','Mon 18:00 \u00b7 forr\u00f3')]),
    ('CACAO & BEACH',NAT,[(7,'Praia do Resende','cacao ceremony'),
                     (8,'Praia da Coroa','beach \u00b7 boat'),
                     (9,'Rodovi\u00e1ria','bus terminal')]),
    ('QUILOMBO',CUL,[(10,'Porto de Tr\u00e1s','Feira Quilombola \u00b7 capoeira Angola')])]
make(15,-14.2792,-38.9925,1500,1040,town,tg,'map_town.png','SOUTH ITACAR\u00c9','Where the itinerary happens \u00b7 street-level pins')

# ---- REGION (Cacao Coast) ----
reg=[
 (1,-14.7926,-39.04538,NAT,'Ilh\u00e9us',''),
 (2,-14.79317,-39.27503,NAT,'Itabuna',''),
 (3,-14.27794,-38.99557,CAP,'Itacar\u00e9',''),
 (4,-14.3725,-39.23902,NAT,'Taboquinhas',''),
]
rg=[('THE CACAO COAST',NAT,[(1,'Ilh\u00e9us (IOS)','arrival \u00b7 CIC \u00b7 Santos'),
                            (2,'Itabuna','Coopercabruca \u00b7 Black King'),
                            (3,'Itacar\u00e9','farms \u00b7 culture \u00b7 base'),
                            (4,'Taboquinhas','Vila Rosa cacao estate')])]
make(10,-14.54,-39.13,1500,780,reg,rg,'map_region.png','THE CACAO COAST','South Bahia \u00b7 the journey corridor')
