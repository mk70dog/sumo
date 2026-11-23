# 絵を 1 枚足す新しい版を作る。使い方:python3 tools/newpi.py 新しい版 パッチ番号 表 キー 画像 "説明"
#   表 = PIMG(力士=四股名、部屋付き親方=年寄名) か PIMGO(師匠・親方=元の四股名)
import sys,io,base64,json
from PIL import Image
v,pn,tb,k,f,note=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]
im=Image.open(f).convert('RGB');w,h=im.size;im=im.resize((320,round(h*320/w)),Image.LANCZOS)
b=io.BytesIO();im.save(b,'JPEG',quality=72);d={k:'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()}
json.dump(d,open('data/portraits%d.json'%v,'w'),ensure_ascii=False)
open('patches/pi%d_ui.js'%v,'w').write('<script>/* v%d:%s */Object.assign(%s,%s);</script>\n'%(v,note,tb,json.dumps(d,ensure_ascii=False)))
p=v-1
open('patches/patch%d.py'%pn,'w').write('''# v%d -> v%d:%s
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %%d (期待 %%d): %%r' %% (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=%d;\\nconst SAVE='sumoManager%d',SAVE%d", "const APPV=%d;\\nconst SAVE='sumoManager%d',SAVE%d='sumoManager%d',SAVE%d")
rep('[SAVE%d,SAVE%d', '[SAVE%d,SAVE%d,SAVE%d')
rep('<title>Grand Sumo Manager v%d', '<title>Grand Sumo Manager v%d')
ui = open(os.path.join(here, 'pi%d_ui.js'), encoding='utf-8').read()
rep('</body>\\n</html>', ui + '</body>\\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
'''%(p,v,note,p,p,p-1,v,v,p,p,p-1,p-1,p-2,p,p-1,p-2,p,v,v))
print(im.size)
