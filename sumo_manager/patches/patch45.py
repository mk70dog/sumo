# 大器晩成:素質の低い若い力士が、ごくまれに伸びしろの上限を大きく上げる  v41 -> v42
# 実際:関取になるのは全力士の 8〜10%、学生相撲出身は半数以上(Number 2016/5/6)。中卒の叩き上げでも関取・幕内になる例がある
#   (高田川部屋の輝・竜電・白鷹山、Number 2018/3/31)。v41 では素質 C・D から関取が 1 人も出なかった。
# 対象:24 歳以下・幕下以下・素質 B 以下(伸びしろ 13.5 未満)。一生に 1 度まで。場所ごとに判定。
# 起きやすさ(推定):若いほど・稽古の量(r.ld)が多いほど・心(我慢 gam・向上心 pro・研究 ken)が強いほど・自分の部屋は稽古場の段階で少し上がる。
# 上がる幅:上限が 2〜4、素質 C・D はその分を足して B〜A まで(推定)。素質 B は起きやすさを半分ほどに(推定)。自分の部屋の弟子なら部屋付き親方(いなければ師匠)の声で知らせ、力士の画面に「大器晩成」の印。
import sys
src, dst = sys.argv[1], sys.argv[2]
P0 = sys.argv[3] if len(sys.argv) > 3 else '.014'
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v41</title>', '<title>Sumo Manager v42</title>')
rep("const APPV=41;\nconst SAVE='sumoManager41',SAVE40", "const APPV=42;\nconst SAVE='sumoManager42',SAVE41='sumoManager41',SAVE40")
rep('[SAVE40,SAVE39', '[SAVE41,SAVE40,SAVE39')
rep(" if(g.v===40){g.v=41;}\n return g.v===41?g:null;}", " if(g.v===40){g.v=41;}\n if(g.v===41){g.v=42;}\n return g.v===42?g:null;}")
rep('G={v:41,', 'G={v:42,')
rep("function nextCycle(){",
    "const DAIKI_P="+P0+";\n"
    "function daiki(){G.order.forEach(id=>{const r=G.R[id];if(!r||r.ret||r.daiki||r.d<=1||r.age>24||!r.cap)return;const pt=potOf(r);if(pt>=13.5)return;\n"
    " const L=r.ld||[];const n=Math.min(6,L.length);const ld=n?L.slice(-n).reduce((a,b)=>a+b,0)/n:2;const mind=((r.a.gam||10)+(r.a.pro||10)+(r.a.ken||10))/3;\n"
    " const p=DAIKI_P*(r.age<=19?1.4:r.age<=21?1:.6)*(.6+.2*ld)*(.6+mind/25)*(r.h===0?(.85+.1*((G.fac&&G.fac.keiko)||1)):1)*(pt>=11?.45:1);\n"
    " if(Math.random()>=p)return;const up=R(2,4)+Math.max(0,11-pt)*.6;PHYS.concat(TECH).forEach(k=>{r.cap[k]=Math.min(20,r.cap[k]+up*R(.7,1.3));});r.daiki=G.bnum;\n"
    " if(r.h===0){const co=G.staff.find(x=>x.role==='co');addNews((co?co.n+'(部屋付き親方)':me().o.replace(/[((].*$/,'')+'親方')+'「'+r.n+'が稽古で急に力をつけてきた。大器晩成かもしれない」');}});}\n"
    "function nextCycle(){")
rep(" computeBanzuke(G.lastRec);\n kyuFloor();", " computeBanzuke(G.lastRec);\n kyuFloor();\n daiki();")
rep("・素質 <b class=\"kin\">'+potTxt(r)+'</b>", "・素質 <b class=\"kin\">'+potTxt(r)+'</b>'+(r.daiki?' <span class=\"tag shu\">大器晩成</span>':'')+'")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
