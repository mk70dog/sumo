# 現実とのマッチング(けが・休場・不祥事)  v27 -> v28
# 実際:十両以上の休場者は 2026 年の夏 7・名古屋 5・秋 6 人(共同通信など)。全体は秋場所の初日に 28 人(協会の休場力士情報)。
# 不祥事:協会の懲戒は年に数件(Wikipedia「日本相撲協会」の処分一覧。2020 年 1 月の 57 件目 → 2025 年 1 月の 74 件目)。暴力が最も多い。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
INJ = float(sys.argv[3]) if len(sys.argv) > 3 else 1.9
SC = float(sys.argv[4]) if len(sys.argv) > 4 else .0013
rep('<title>Sumo Manager v27</title>', '<title>Sumo Manager v28</title>')
rep("const APPV=27;\nconst SAVE='sumoManager27',SAVE26", "const APPV=28;\nconst SAVE='sumoManager28',SAVE27='sumoManager27',SAVE26")
rep('[SAVE26,SAVE25', '[SAVE27,SAVE26,SAVE25')
rep(" if(g.v===26){g.v=27;}\n return g.v===27?g:null;}", " if(g.v===26){g.v=27;}\n if(g.v===27){g.v=28;}\n return g.v===28?g:null;}")
rep('G={v:27,', 'G={v:28,')
# けが:稽古中・取組中の確率を INJ 倍
rep("const pI=.0035*", "const pI=%.5f*" % (.0035 * INJ))
rep("let pr=.0022*", "let pr=%.5f*" % (.0022 * INJ))
# 自分の部屋の不祥事:弟子 1 人・1 場所のもとの確率
rep("let p=.006*(1+(50-r.tr)/40)", "let p=%.5f*(1+(50-r.tr)/40)" % SC)
# 中身の割合:実際の懲戒は暴力が最も多い
rep("const w=[['sns',28],['yoa',28],['ken',18],['bou',10],['tob',6],['dui',6]];if(r.d<=1)w.push(['yao',4]);",
    "const w=[['bou',30],['yoa',25],['sns',12],['ken',12],['dui',8],['tob',6]];if(r.d<=1)w.push(['yao',3]);")
rep("dui:{n:'飲酒運転',s:3}", "dui:{n:'飲酒運転・無免許運転',s:3}")
# ほかの部屋:場所ごと 20% → 35%(年 2 件ほど)、中身の割合も同じ考えで
rep("if(Math.random()<.2){const c=G.order.map(id=>G.R[id]).filter(r=>r.h!==0&&!r.ret&&r.d<=3);",
    "if(Math.random()<.35){const c=G.order.map(id=>G.R[id]).filter(r=>r.h!==0&&!r.ret&&r.d<=3);")
rep("T=SCT[wpick([['sns',3],['yoa',3],['ken',2],['bou',2],['tob',1],['dui',1]])]",
    "T=SCT[wpick([['bou',30],['yoa',25],['sns',12],['ken',12],['dui',8],['tob',6]])]")
# 横審:実際は決議がまれ(稀勢の里は 8 場所連続休場のあと「激励」、白鵬・鶴竜は 2020 年 11 月に「注意」、
# 白鵬は 6 場所連続休場まで進退を待った)。激励 2→4、注意 3→6、引退勧告(よその部屋は引退 70%→50%)4→7 場所に。
rep(" if(r.yc===2&&r.h===0)addNews('横綱審議委員会が'+r.n+'に「激励」を決議しました。');\n if(r.yc===3)addNews('横綱審議委員会が'+r.n+'に「注意」を決議しました。');\n if(r.yc>=4){if(r.h===0){if(!G.ev.some(e=>e.k==='yokoshin'))G.ev.push({k:'yokoshin',rid:r.id});return 0;}return .7;}return 0;}",
    " if(r.yc===4&&r.h===0)addNews('横綱審議委員会が'+r.n+'に「激励」を決議しました。');\n if(r.yc===6)addNews('横綱審議委員会が'+r.n+'に「注意」を決議しました。');\n if(r.yc>=7){if(r.h===0){if(!G.ev.some(e=>e.k==='yokoshin'))G.ev.push({k:'yokoshin',rid:r.id});return 0;}return .5;}return 0;}")

# 横綱の引退:少しでも休むと 31 歳以上で 25% は強すぎた(けがが増えたため)。半分以上休んだ 32 歳以上で 15% に。
rep("else if(rc.ab>0&&r.age>=31)p=.25;", "else if(rc.ab>=8&&r.age>=32)p=.15;")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', INJ, SC)
