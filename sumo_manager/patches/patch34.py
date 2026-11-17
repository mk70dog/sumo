# 現実とのマッチング(4):横綱昇進の基準・大関の伸び  v30 -> v31
# 横審の内規は「大関で2場所連続優勝、またはそれに準ずる好成績」(準ずる成績での推薦は出席委員の3分の2以上の決議が必要。デイリー 2025/1/27)。
#   千代の富士以降、昇進3場所の合計35勝以下で横綱になった例はない(神戸新聞 2023/1)。
#   v30 は横綱が少ないと「前の場所10勝+優勝13勝」でも昇進でき、弱い横綱が平幕に負けて金星が年 約20(現実は推定 年8前後)。
#   v31:優勝(12勝以上)かつ前の場所も大関で、優勝11勝以上 または 12勝以上、2場所で26勝以上、3場所で36勝以上。
#   横綱が減る分、大関で11勝以上した力士は伸びしろ(上限)が少し上がる(推定。大関の地位で力をつける様子の代わり)。
import sys
src, dst = sys.argv[1], sys.argv[2]
B = sys.argv[3] if len(sys.argv) > 3 else '.15'
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v30</title>', '<title>Sumo Manager v31</title>')
rep("const APPV=30;\nconst SAVE='sumoManager30',SAVE29", "const APPV=31;\nconst SAVE='sumoManager31',SAVE30='sumoManager30',SAVE29")
rep('[SAVE29,SAVE28', '[SAVE30,SAVE29,SAVE28')
rep(" if(g.v===29){g.v=30;}\n return g.v===30?g:null;}", " if(g.v===29){g.v=30;}\n if(g.v===30){g.v=31;}\n return g.v===31?g:null;}")
rep('G={v:30,', 'G={v:31,')
rep("if(r.t==='O'&&kk(id)&&c.yu&&c.w>=13){const h=r.hist.slice(-2);if(h.length===2){const p=h[0];const ok=nY===0?p.w>=10:nY<=2?p.w>=11:!!p.yu;if(ok)nt[id]='Y';}}",
    "if(r.t==='O'&&c.w>=11)PHYS.concat(TECH).forEach(k=>{r.cap[k]=Math.min(20,r.cap[k]+"+B+"*R(.5,1.5));});\n"
    "  if(r.t==='O'&&kk(id)&&c.yu&&c.w>=12){const h=r.hist.slice(-3);const p=h[h.length-2];if(p&&p.t==='O'&&(p.yu?p.w>=11:p.w>=12)&&p.w+c.w>=26&&(h.length<3||h.reduce((x,y)=>x+y.w,0)>=36))nt[id]='Y';}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
