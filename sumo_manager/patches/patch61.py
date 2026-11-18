# 取組の組み方:横綱・大関は序盤〜中盤に三役・前頭上位と、横綱・大関どうしは終盤に  v57 -> v58
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v57</title>', '<title>Sumo Manager v58</title>')
rep("const APPV=57;\nconst SAVE='sumoManager57',SAVE56", "const APPV=58;\nconst SAVE='sumoManager58',SAVE57='sumoManager57',SAVE56")
rep('[SAVE56,SAVE55', '[SAVE57,SAVE56,SAVE55')
rep(" if(g.v===56){g.v=57;}\n return g.v===57?g:null;}", " if(g.v===56){g.v=57;}\n if(g.v===57){g.v=58;}\n return g.v===58?g:null;}")
rep('G={v:57,', 'G={v:58,')
NEW = r'''  carry=[];
  // 幕内:横綱・大関(上位)は、上位どうしの取組を残り日数ぎりぎりまで後ろへ回し(大関どうしを先に、横綱どうしを最後に)、
  // それ以外の日は、上位でない力士のうち番付の高い順(11 日目以降は勝ち星の多い順)に当てる
  if(d===0){const isT=id=>{const t=G.R[id].t;return t==='Y'||t==='O';};const T=pool.filter(isT);const left=15-day;
   const remOf=a=>{const fa=opps(a);return T.filter(c=>c!==a&&ok(a,c,fa)).length;};
   const need=T.filter(a=>remOf(a)>=left).sort((a,b)=>G.R[b].pos-G.R[a].pos);
   need.forEach(a=>{if(used[a])return;const fa=opps(a);const cs=T.filter(c=>c!==a&&!used[c]&&ok(a,c,fa)).sort((x,y)=>(remOf(y)>=left)-(remOf(x)>=left)||G.R[y].pos-G.R[x].pos);
    if(cs.length){used[a]=used[cs[0]]=1;pairs.push(Object.assign([a,cs[0]],{day:day}));}});
   const NT=pool.filter(id=>!isT(id));const ord=day>10?NT.slice().sort((a,b)=>(B.rec[b].w-B.rec[a].w)||(G.R[a].pos-G.R[b].pos)):NT.slice().sort((a,b)=>G.R[a].pos-G.R[b].pos);
   T.slice().sort((a,b)=>G.R[a].pos-G.R[b].pos).forEach(a=>{if(used[a])return;const fa=opps(a);const c=ord.find(c=>!used[c]&&ok(a,c,fa));if(c!=null){used[a]=used[c]=1;pairs.push(Object.assign([a,c],{day:day}));}});}
'''
rep("  carry=[];\n  for(let i=0;i<pool.length;i++){", NEW + "  for(let i=0;i<pool.length;i++){")
# 番付の上乗せを組み方に合わせて調整(測定に合わせた推定)
rep('const BZ={Y:.01,O:.003,S:.006,K:.004};','const BZ={Y:.004,O:.002,S:.008,K:.006};')
# 大関で 11 勝以上したときの伸びしろの上乗せ(v31)をやめる:横綱が強くなりすぎるため
rep("  if(r.t==='O'&&c.w>=11)PHYS.concat(TECH).forEach(k=>{r.cap[k]=Math.min(20,r.cap[k]+.15*R(.5,1.5));});\n","")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
