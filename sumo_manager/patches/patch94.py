# v90 -> v91:二人相撲の直し(ダルマさん「ランダムにどちらかに来るようにする」「親と子は別の部屋を担当する」)
# ①部屋の閉鎖で移籍を受け入れる誘い・ほかの部屋の二世の候補は、プレイヤーが 2 人のときランダムにどちらかへ(一人用は今までどおり)
# ②子から届いた差分は、子の部屋の力士・子のデータだけに当てる(親の部屋の力士や親のデータは、子からは変えられない)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v90</title>', '<title>Grand Sumo Manager v91</title>')
rep("const APPV=90;\nconst SAVE='sumoManager90',SAVE89", "const APPV=91;\nconst SAVE='sumoManager91',SAVE90='sumoManager90',SAVE89")
rep('[SAVE89,SAVE88', '[SAVE90,SAVE89,SAVE88')
rep(" if(g.v===89){g.v=90;}\n return g.v===90?g:null;}", " if(g.v===89){g.v=90;}\n if(g.v===90){g.v=91;}\n return g.v===91?g:null;}")
rep('G={v:90,', 'G={v:91,')
# ① 移籍の誘い:同じ一門のプレイヤーの部屋のうち 1 つ(2 つ以上ならランダム)
rep(""" if(me().ic>=0&&me().ic===h.ic&&ids.length&&Math.random()<.4&&!G.ev.some(e=>e.k==='iseki')){
  const can=Math.max(0,cap()-ownAll().length);if(can>0){const L=ids.map(id=>G.R[id]).sort((a,b)=>a.pos-b.pos).slice(0,Math.min(can,4)).map(r=>r.id);G.ev.push({k:'iseki',from:h.n,to:to,ids:L});}}}""",
""" {const PC=G.P?G.P.map(p=>p.h).filter(x=>G.heya[x]&&G.heya[x].ic>=0&&G.heya[x].ic===h.ic):(me().ic>=0&&me().ic===h.ic?[ME()]:[]);
 if(PC.length&&ids.length&&Math.random()<.4){const hp=PC.length>1?PC[RI(0,PC.length-1)]:PC[0];inP(hp,()=>{if(G.ev.some(e=>e.k==='iseki'))return;
  const can=Math.max(0,cap()-ownAll().length);if(can>0){const L=ids.map(id=>G.R[id]).sort((a,b)=>a.pos-b.pos).slice(0,Math.min(can,4)).map(r=>r.id);G.ev.push({k:'iseki',from:h.n,to:to,ids:L});}});}}}""")
# ① ほかの部屋の二世の候補
rep("  else{G.pros.unshift(mkNiseiPros(k));addNews(k.f+'('+k.br+')の息子が入門を考えているそうです。「新弟子」に'+(k.g?'三世(祖父は'+k.g.f+')':'二世')+'の候補が加わりました。');}});",
    "  else{const hp=G.P&&G.P.length>1?G.P[RI(0,G.P.length-1)].h:ME();inP(hp,()=>{G.pros.unshift(mkNiseiPros(k));addNews(k.f+'('+k.br+')の息子が入門を考えているそうです。「新弟子」に'+(k.g?'三世(祖父は'+k.g.f+')':'二世')+'の候補が加わりました。');});}});")
# ② 子の差分は子の部屋のものだけ
rep("function mpPut(ops){let n=0;(ops||[]).forEach(op=>{try{const p=op[1];if(!p.length||MP_BLK[p[0]]&&!(p[0]==='B'&&p[1]==='tac'))return;",
"""function mpOK(ops){const gh=G.mp&&G.mp.gh,gi=pI(gh);const ok=new Set();
 (ops||[]).forEach(op=>{const p=op[1];if(p[0]!=='R'||op[0]!=='s')return;const id=p[1];const v=op[2];
  if((p.length===3&&p[2]==='h'&&v===gh)||(p.length===2&&v&&v.h===gh))ok.add(String(id));});
 return p=>{if(p[0]==='P')return +p[1]===gi;
  if(p[0]==='R'){const r=G.R[p[1]];return !r||r.h===gh||ok.has(String(p[1]));}
  if(p[0]==='B'&&p[1]==='tac'){const r=G.R[p[2]];return !r||r.h===gh;}
  if(p[0]==='heya')return p.length===1||+p[1]===gh||!G.heya[+p[1]];
  return true;};}
function mpPut(ops){let n=0;const can=mpOK(ops);(ops||[]).forEach(op=>{try{const p=op[1];if(!p.length||MP_BLK[p[0]]&&!(p[0]==='B'&&p[1]==='tac'))return;if(!can(p))return;""")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
