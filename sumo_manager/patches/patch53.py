# 場所ごとの調子の波(当たり場所・不調の場所)  v49 -> v50
# 場所の始めに力士ごとに r.bfm を決める:ふだんの波(標準偏差 2%)+当たり場所(6%、前の場所に幕内で 10 勝以上なら 15%。力 +6%)+不調の場所(6%。力 -4%)。数値は推定。
# 取組の力(prepF の r._f)に掛ける。自分の部屋の力士は、当たり・不調を場所前のお知らせで伝える。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v49</title>', '<title>Sumo Manager v50</title>')
rep("const APPV=49;\nconst SAVE='sumoManager49',SAVE48", "const APPV=50;\nconst SAVE='sumoManager50',SAVE49='sumoManager49',SAVE48")
rep('[SAVE48,SAVE47', '[SAVE49,SAVE48,SAVE47')
rep(" if(g.v===48){g.v=49;}\n return g.v===49?g:null;}", " if(g.v===48){g.v=49;}\n if(g.v===49){g.v=50;}\n return g.v===50?g:null;}")
rep('G={v:49,', 'G={v:50,')
rep("  if(sitOut(r)){rec.ky=true;days.forEach(x=>rec.res[x-1]={r:'や'});}\n  if(r.h===0)peak(r);",
    "  if(sitOut(r)){rec.ky=true;days.forEach(x=>rec.res[x-1]={r:'や'});}\n  if(r.h===0)peak(r);\n  {const u=Math.random();const lh=r.hist&&r.hist.length?r.hist[r.hist.length-1]:null;const pa=lh&&lh.d===0&&lh.w>=10?.15:.06;r.bfm=randn()*.02+(u<pa?.06:u>1-.06?-.04:0);}")
rep("f*=1+randn()*(.055-r.cons*.0024);r._f=f;", "f*=1+randn()*(.055-r.cons*.0024);f*=1+(r.bfm||0);r._f=f;")
rep("const kys=own().filter(r=>B.rec[r.id].ky);",
    "const kys=own().filter(r=>B.rec[r.id].ky);\n {const hot=own().filter(r=>!B.rec[r.id].ky&&r.bfm>=.05),cold=own().filter(r=>!B.rec[r.id].ky&&r.bfm<=-.035&&r.d<=3);\n  if(hot.length)addNews('稽古場で'+hot.slice(0,3).map(r=>r.n).join('・')+'の体がよく動いています。今場所は期待できそうです。');\n  if(cold.length)addNews(cold.slice(0,3).map(r=>r.n).join('・')+'はどこか体が重そうです。');}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
