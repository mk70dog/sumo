# v106 -> v107:部屋の画面の背景の絵を差しかえ(見本 hb2b。ダルマさん「画像を変更 サンプル」→「ジェミニで作成した画像なので大丈夫 実施」)
# 絵は img/home_keikoba2.jpg(1376×768、ダルマさんが Gemini で作成)。土俵と土俵の上の力士・行司の位置 HB_BOX を測り直した(横 225〜1035・縦 255〜768)。
import sys, os, re, base64
from io import BytesIO
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v106</title>', '<title>Grand Sumo Manager v107</title>')
rep("const APPV=106;\nconst SAVE='sumoManager106',SAVE105", "const APPV=107;\nconst SAVE='sumoManager107',SAVE106='sumoManager106',SAVE105")
rep('[SAVE105,SAVE104', '[SAVE106,SAVE105,SAVE104')
rep(" if(g.v===105){g.v=106;}\n return g.v===106?g:null;}", " if(g.v===105){g.v=106;}\n if(g.v===106){g.v=107;}\n return g.v===107?g:null;}")
rep('G={v:106,', 'G={v:107,')
from PIL import Image
im = Image.open(os.path.join(here, '..', 'img', 'home_keikoba2.jpg')).convert('RGB'); bio = BytesIO(); im.save(bio, 'JPEG', quality=80, optimize=True)
b = base64.b64encode(bio.getvalue()).decode()
old = re.search(r"const HB_IMG='data:image/jpeg;base64,([^']+)'", s).group(1)
rep(old, b, 3)
rep("const HB_BOX={x0:195,x1:948,y0:320,W:1200,H:896};", "const HB_BOX={x0:225,x1:1035,y0:255,W:1376,H:768};")
rep('aspect-ratio:1200/896', 'aspect-ratio:1376/768')
rep("背景:江戸時代の錦絵(相撲部屋の稽古場)", "背景:相撲部屋の稽古場(Gemini で作成した絵)")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, len(s))
