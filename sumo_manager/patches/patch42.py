# 細かいドット(見本 dotall2)・部屋を選ぶ画面にも画面の色(見本 skinstart)  v38 -> v39
# あわせて、v36 の吹き出しと「部屋の声」のボタンを画面の色に合わせる(墨の夜で白く浮いていた)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v38</title>', '<title>Sumo Manager v39</title>')
rep("const APPV=38;\nconst SAVE='sumoManager38',SAVE37", "const APPV=39;\nconst SAVE='sumoManager39',SAVE38='sumoManager38',SAVE37")
rep('[SAVE37,SAVE36', '[SAVE38,SAVE37,SAVE36')
rep(" if(g.v===37){g.v=38;}\n return g.v===38?g:null;}", " if(g.v===37){g.v=38;}\n if(g.v===38){g.v=39;}\n return g.v===39?g:null;}")
rep('G={v:38,', 'G={v:39,')
# 吹き出し・部屋の声のボタンを画面の色に
rep(".sdq{position:relative;background:#fff;color:#2a2018;", ".sdq{position:relative;background:var(--paper);color:var(--sumi);")
rep(".kp button{border:1px solid var(--line);background:#fffaf0;color:#2a2018;", ".kp button{border:1px solid var(--line);background:var(--washi2);color:var(--sumi);")
rep(".kp small{color:#7a6a55}", ".kp small{color:var(--mute)}")
# 細かいドット(dotall2)
BTN=['.btn','#nav button','.divbtn button','.st-go button','.hchip','.kp button','.skins button']
PAN=['.pn','.hcard','.ev','.kr','.stf','.card','#mbox','#hsheet .in','#ssheet .in']
def dots(sel,op,pos=True):
    a=','.join(sel);b=','.join(x+'::before' for x in sel)
    return (a+'{position:relative;isolation:isolate}' if pos else a+'{isolation:isolate}')+b+"{content:'';position:absolute;inset:0;border-radius:inherit;z-index:-1;pointer-events:none;background-image:radial-gradient(currentColor .6px,transparent 1px);background-size:3px 3px;opacity:"+str(op)+"}\n"
DOT='/* 細かいドット(v39) */\n'+dots(BTN,.14)+dots(PAN,.09)+dots(['#hdr'],.16,False)
# 部屋を選ぶ画面にも画面の色(skinstart)
P={'yoru':dict(bg='#24201a',bd='#6a5a3e',tx='#eee6d6',sub='#b8ab95',em='#e0583c',inp='#2e2921'),
   'ai':dict(bg='#f7f9fc',bd='#13284d',tx='#13284d',sub='#4a5a70',em='#b23a2a',inp='#ffffff'),
   'sakura':dict(bg='#fffafb',bd='#c2405a',tx='#3a1f28',sub='#7a5060',em='#c2405a',inp='#ffffff'),
   'nishiki':dict(bg='#fffaee',bd='#a01f14',tx='#2a1a10',sub='#6a4a30',em='#c0261a',inp='#fffdf7'),
   'banzuke':dict(bg='#ffffff',bd='#000000',tx='#000000',sub='#333333',em='#b00000',inp='#ffffff')}
SK='/* 部屋を選ぶ画面にも画面の色(v39) */\n'
for k,c in P.items():
    b='body.sk-'+k+' '
    SK+=(f"{b}.hcard,{b}.st-wrap .start,{b}#hsheet .in,{b}#ssheet .in{{background:{c['bg']};border-color:{c['bd']};color:{c['tx']}}}"
         f"{b}.hcard .s,{b}.st-wrap .start .lead,{b}.st-wrap .start label,{b}#hsheet dt,{b}#hsheet label,{b}#ssheet p{{color:{c['sub']}}}"
         f"{b}.hcard .n em{{color:{c['em']}}}{b}#hsheet .x,{b}#ssheet h2 button{{color:{c['tx']};border-color:{c['bd']}}}"
         f"{b}#hsheet select,{b}.st-wrap .start select,{b}.st-wrap .start input[type=text]{{background:{c['inp']};color:{c['tx']};border-color:{c['bd']}}}\n")
rep('</style>', DOT+SK+'</style>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
