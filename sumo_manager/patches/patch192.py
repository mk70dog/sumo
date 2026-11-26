# v188 -> v189:新弟子の入門の場所ごとの数を実際に近づける(卒業生を春場所の検査に、夏場所の補充を多めに)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=188;\nconst SAVE='sumoManager188',SAVE187", "const APPV=189;\nconst SAVE='sumoManager189',SAVE188='sumoManager188',SAVE187")
rep('[SAVE187,SAVE186', '[SAVE188,SAVE187,SAVE186')
rep('<title>Grand Sumo Manager v188', '<title>Grand Sumo Manager v189')
# v189:卒業生(ほかの部屋)は春場所の新弟子検査 → 夏場所の番付に載る(1 場所遅らせる)。夏場所の検査の補充を少し多めに
rep("r.n=shikona();r.tsuke=p.ama;G.R[r.id]=r;G.aiPend.push(r.id);fate='heya';","r.n=shikona();r.tsuke=p.ama;G.R[r.id]=r;(G.aiPend2=G.aiPend2||[]).push(r.id);fate='heya';")
rep(" G.aiPend=[];\n const need=Math.max(0,TOTAL-25-G.order.length,Math.round((TOTAL-G.order.length)*([.12,1,.3,.2,.25,.1][(G.bnum-1)%6])));"," G.aiPend=[];if(G.aiPend2&&G.aiPend2.length){G.aiPend=G.aiPend2;G.aiPend2=[];}\n const need=Math.max(0,TOTAL-25-G.order.length,Math.round((TOTAL-G.order.length)*([.12,1,.9,.2,.2,.1][(G.bnum-1)%6])));")
rep("G.aiPend.forEach(add);","G.aiPend.forEach(add);(G.aiPend2||[]).forEach(add);")
rep("G.aiPend.forEach(id=>{if(G.R[id]&&G.R[id].h===i)G.R[id].h=to;});","G.aiPend.concat(G.aiPend2||[]).forEach(id=>{if(G.R[id]&&G.R[id].h===i)G.R[id].h=to;});")
ui = ''
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
