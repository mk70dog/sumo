# 新しい画面の色「漆黒・朱」「漆黒・金」「漆黒・銀」(見本 shikkoku7・8・10:ボタンは枠だけ色)  v39 -> v40
# 墨の夜(sk-yoru)の決まりを写し、こげ茶を抜いた真っ黒に置きかえる。選んでいるタブ・紺と赤のボタン・上の帯の札は、中は黒のまま枠と文字だけ色。
# 色の一覧の小さな絵は patches/urushi43_img.json(なければ空)。
import sys, os, re, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v39</title>', '<title>Sumo Manager v40</title>')
rep("const APPV=39;\nconst SAVE='sumoManager39',SAVE38", "const APPV=40;\nconst SAVE='sumoManager40',SAVE39='sumoManager39',SAVE38")
rep('[SAVE38,SAVE37', '[SAVE39,SAVE38,SAVE37')
rep(" if(g.v===38){g.v=39;}\n return g.v===39?g:null;}", " if(g.v===38){g.v=39;}\n if(g.v===39){g.v=40;}\n return g.v===40?g:null;}")
rep('G={v:39,', 'G={v:40,')
R = open(os.path.join(here, 'yoru_rules43.css'), encoding='utf-8').read()
base={'#16130f':'#050505','#1f1b16':'#0c0c0c','#24201a':'#121212','#2e2921':'#1a1a1a','#3a342b':'#222222','#4a4236':'#2c2c2c',
 '#ece4d3':'#f2f2f2','#eee6d6':'#f2f2f2','#c9bfac':'#c4c4c4','#b8ab95':'#bdbdbd','#968b78':'#8a8a8a','#0d0b09':'#080808',
 '#3a332a':'#1e1e1e','#2c2620':'#111111','#5a5040':'#3a3a3a','#302a22':'#161616','#221d16':'#101010','#1c1814':'#0e0e0e','#b8a984':'#a8a8a8'}
SK=[('urushi','漆黒・朱','#e04a2e','#ff7a5c'),('urushik','漆黒・金','#d4af4a','#ecd07a'),('urushig','漆黒・銀','#c8c8c8','#efefef')]
CSS='/* 漆黒(v40) */\n'
for key,nm,a,a2 in SK:
    m={'#6a5a3e':'#3a3a3a','#e0583c':a,'#f07a5e':a2,'#8a2b1a':'#151515','#6b1f12':a,'#c8432a':'#151515','#9e2d18':a,'#4a2a22':'#1c1c1c','#2e2716':'#1e1e1e','#6b5a2e':'#3a3a3a','#f1d38e':'#e6e6e6','#d9b25e':a2}
    css=R.replace('body.sk-yoru','body.sk-'+key)
    for x,y in list(base.items())+list(m.items()):
        css=re.sub(re.escape(x)+r'\b',y,css,flags=re.I)
    U='body.sk-'+key+' '
    css+=(f"\n{U}#nav button.on,{U}.btn.ai,{U}.divbtn button.on,{U}.btn.main{{background:#121212;border:1.5px solid {a};border-bottom-width:3px;color:{a2}}}"
          f"{U}.btn.main{{border-width:2px;border-bottom-width:4px;color:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.6),0 0 10px {a}55}}"
          f"{U}#hdr .cal{{background:transparent;border:1.5px solid {a};color:{a2}}}")
    if key=='urushig': css+=f"{U}#nav button .bd{{color:#111}}"
    CSS+=css+'\n'
rep('</style>', CSS+'</style>')
rep("['banzuke','番付(白黒)',['#000000','#ffffff','#b00000']]];",
    "['banzuke','番付(白黒)',['#000000','#ffffff','#b00000']]"+''.join(",['%s','%s',['#000000','#121212','%s']]"%(k,n,a) for k,n,a,_ in SK)+"];")
p=os.path.join(here,'urushi43_img.json'); img=json.load(open(p)) if os.path.exists(p) else {}
rep('SKIMG={"std":', 'SKIMG={'+''.join('"%s": %s, '%(k,json.dumps(img.get(k,''))) for k,_,_,_ in SK)+'"std":')
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
