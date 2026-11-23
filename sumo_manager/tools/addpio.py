# 師匠・親方の絵を v142 用に足す。使い方:python3 tools/addpio.py 元の四股名 画像ファイル
import sys,io,base64,json
from PIL import Image
k,f=sys.argv[1],sys.argv[2]
d=json.load(open('data/portraits142.json'))
im=Image.open(f).convert('RGB');w,h=im.size;im=im.resize((320,round(h*320/w)),Image.LANCZOS)
b=io.BytesIO();im.save(b,'JPEG',quality=72);d[k]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
json.dump(d,open('data/portraits142.json','w'),ensure_ascii=False)
open('patches/pi142_ui.js','w').write('<script>/* v142:師匠の絵('+'・'.join(d)+')。師匠は元の四股名で PIMGO に入れる。 */Object.assign(PIMGO,'+json.dumps(d,ensure_ascii=False)+');</script>\n')
print(k,im.size,list(d))
