# 横綱昇進を横審の内規どおりに  v31 -> v32
# 内規:「大関で2場所連続優勝、またはそれに準ずる好成績」。数字の基準はない。
#   2場所連続優勝 → 必ず昇進(1990年以降、連続優勝の大関はすべて昇進。しんぶん赤旗 2003)。
#   準ずる成績:一方が優勝、もう一方が優勝同点か優勝次点(どちらも大関)で、2場所の合計25勝以上(推定)。
#     豊昇龍 13勝次点+12勝優勝=25 で昇進(時事)、貴景勝 12勝同点+12勝優勝=24 で見送り(東スポ・神戸新聞)。
#   v31 の「3場所36勝」は内規にないので外す。幕内の優勝同点・優勝次点を記録し、最近の成績に出す。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v31</title>', '<title>Sumo Manager v32</title>')
rep("const APPV=31;\nconst SAVE='sumoManager31',SAVE30", "const APPV=32;\nconst SAVE='sumoManager32',SAVE31='sumoManager31',SAVE30")
rep('[SAVE30,SAVE29', '[SAVE31,SAVE30,SAVE29')
rep(" if(g.v===30){g.v=31;}\n return g.v===31?g:null;}", " if(g.v===30){g.v=31;}\n if(g.v===31){g.v=32;}\n return g.v===32?g:null;}")
rep('G={v:31,', 'G={v:32,')
rep("  const r=G.R[win];r.yu[d]++;B.rec[win].yu=true;const rc=B.rec[win];",
    "  const r=G.R[win];r.yu[d]++;B.rec[win].yu=true;const rc=B.rec[win];\n"
    "  if(d===0){if(top.length>1)top.forEach(x=>{if(x!==win)B.rec[x].jn=1;});else{let m2=-1;ids.forEach(x=>{if(x!==win)m2=Math.max(m2,B.rec[x].w);});ids.forEach(x=>{if(x!==win&&B.rec[x].w===m2)B.rec[x].jn=2;});}}")
rep("w:rc.w,l:rc.l,ab:rc.ab,yu:!!rc.yu,pos:r.pos});", "w:rc.w,l:rc.l,ab:rc.ab,yu:!!rc.yu,jn:rc.jn||0,pos:r.pos});")
rep("if(r.t==='O'&&kk(id)&&c.yu&&c.w>=12){const h=r.hist.slice(-3);const p=h[h.length-2];if(p&&p.t==='O'&&(p.yu?p.w>=11:p.w>=12)&&p.w+c.w>=26&&(h.length<3||h.reduce((x,y)=>x+y.w,0)>=36))nt[id]='Y';}",
    "if(r.t==='O'&&kk(id)){const h=r.hist.slice(-2);if(h.length===2&&h[0].t==='O'&&h[1].t==='O'){const a=h[0],b=h[1];if((a.yu&&b.yu)||(((a.yu&&b.jn)||(b.yu&&a.jn))&&a.w+b.w>=25))nt[id]='Y';}}")
rep("(x.yu?' <span class=\"tag shu\">優勝</span>':'')", "(x.yu?' <span class=\"tag shu\">優勝</span>':x.jn===1?' <span class=\"tag\">優勝同点</span>':x.jn===2?' <span class=\"tag\">優勝次点</span>':'')")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
