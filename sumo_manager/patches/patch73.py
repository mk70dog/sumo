# v69 -> v70:腰の重さ・前さばきを「生まれ+積み重ね」に
# 腰の重さ=稽古で積む分(r.a.kos)+体格の分(体重・重心の低さ・生まれつきの骨格)。前さばき=稽古の分+器用さ(生まれつき、小さめ)
# 使い方:python3 patch73.py 前.html 後.html [見せ方 1/2/3、既定 1]
import sys
src, dst = sys.argv[1], sys.argv[2]
V = int(sys.argv[3]) if len(sys.argv) > 3 else 1
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v69</title>', '<title>Sumo Manager v70</title>')
rep("const APPV=69;\nconst SAVE='sumoManager69',SAVE68", "const APPV=70;\nconst SAVE='sumoManager70',SAVE69='sumoManager69',SAVE68")
rep('[SAVE68,SAVE67', '[SAVE69,SAVE68,SAVE67')
rep(" if(g.v===68){mig69(g);g.v=69;}\n return g.v===69?g:null;}", " if(g.v===68){mig69(g);g.v=69;}\n if(g.v===69){g.v=70;}\n return g.v===70?g:null;}")
rep('G={v:69,', 'G={v:70,')
# 生まれの分(推定):体重 150kg を 0 に 1kg あたり 0.025、BMI 45 を 0 に 1 あたり 0.05(重心の低さの目安)、骨格・股関節の生まれつき ±0.8(力士ごとに固定)。合計 −2〜+3
CORE = r'''
function hhR(id,s){let x=(Math.imul(id|0,2654435761)+Math.imul(s,40503))>>>0;x^=x>>>15;x=Math.imul(x,2246822519)>>>0;x^=x>>>13;return (x>>>0)%10000/10000;}
function kbOf(r){const w=r.w||r.wT||150,h=(r.ht||183)/100;return cl((w-150)*.025+(w/(h*h)-45)*.05+(hhR(r.id,1)-.5)*1.6,-2,3);}
function mgOf(r){return (hhR(r.id,2)-.5)*1.2;}
function inb(r,k){return k==='kos'?kbOf(r):k==='mae'?mgOf(r):0;}
function atTot(r,k){return cl(r.a[k]+inb(r,k),1,20);}
'''
rep("function E(r,k){return Math.max(.5,(r.a[k]-injPen(r,k))*r._f+r._pr);}",
    CORE + "function E(r,k){return Math.max(.5,((k==='kos'||k==='mae'?atTot(r,k):r.a[k])-injPen(r,k))*r._f+r._pr);}")
# 積み重ねの分は、四股・鉄砲などの基礎・ぶつかり・三番をしない週は少しずつ落ちる(推定 1 週 0.005)
rep(" if(mk!=='休'&&mk!=='研')AK.forEach(k=>grow(r,k,gm*.12*H.cf[CAT[k]]));\n decline(r,1);",
    " if(mk!=='休'&&mk!=='研')AK.forEach(k=>grow(r,k,gm*.12*H.cf[CAT[k]]));\n if(!(M.w&&M.w.kos)&&r.a.kos!=null)r.a.kos=Math.max(1,r.a.kos-.005);\n decline(r,1);")
# 実在の力士:押し・寄りが得意なら腰の重さ、押し・突き・おっつけ・差しが得意なら前さばきを高めに(+1.5、新しく始めたとき)
rep("[/寄り/,'yor'],", "[/寄り/,'yor'],[/押し|寄り/,'kos'],[/押し|突|おっつけ|差/,'mae'],")
# 画面:腰の重さ・前さばきは合計を出し、生まれの分を見せる
ROW = {
1: "'<div class=\"atr\"><span>'+x[1]+'<small class=\"atk\">稽古 '+Math.round(v)+'・'+lb+' '+sg+'</small></span><b class=\"'+ac(t)+'\">'+Math.round(t)+'</b><i></i></div>'",
2: "'<div class=\"atr\"><span>'+x[1]+' <em class=\"atp '+(ib>=.5?'pu':ib<=-.5?'mi':'')+'\">'+lb+sg+'</em></span><b class=\"'+ac(t)+'\">'+Math.round(t)+'</b><i></i></div>'",
3: "'<div class=\"atr\"><span>'+x[1]+'</span><b class=\"'+ac(t)+'\">'+Math.round(t)+'</b><i></i></div><div class=\"atbar\"><u style=\"width:'+(Math.max(0,Math.min(v,t))/20*100).toFixed(1)+'%\"></u>'+(ib>0?'<s style=\"width:'+(Math.min(ib,20-v)/20*100).toFixed(1)+'%\"></s>':'')+'<span>稽古 '+Math.round(v)+'・'+lb+' '+sg+'</span></div>'",
}[V]
rep("AT.filter(fl).map(x=>{const v=r.a[x[0]];const pen=injPen(r,x[0]);return '<div class=\"atr\">",
    "AT.filter(fl).map(x=>{const v=r.a[x[0]];const pen=injPen(r,x[0]);if(x[0]==='kos'||x[0]==='mae'){const ib=inb(r,x[0]),t=atTot(r,x[0]),lb=x[0]==='kos'?'体格':'器用さ',sg=(ib>=0?'+':'−')+Math.abs(ib).toFixed(1);return " + ROW + ";}return '<div class=\"atr\">")
CSS = ".atk{display:block;font-size:10px;color:var(--mute);letter-spacing:0;line-height:1.1}" \
      ".atp{font-style:normal;font-size:10px;padding:0 3px;border-radius:3px;border:1px solid var(--line);color:var(--mute);white-space:nowrap}.atp.pu{color:var(--shu);border-color:var(--shu)}.atp.mi{color:var(--ai);border-color:var(--ai)}" \
      ".atbar{position:relative;height:13px;background:var(--line);border-radius:2px;margin:0 0 3px;overflow:hidden;display:flex}.atbar u{display:block;background:var(--ai);opacity:.55}.atbar s{display:block;background:var(--shu);opacity:.7}.atbar span{position:absolute;left:4px;top:0;font-size:9.5px;line-height:13px;color:var(--sumi);font-family:var(--kaku)}"
rep(".atw5{display:grid;", CSS + ".atw5{display:grid;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, 'V', V)
