# メディア情報(見本 media)  v43 -> v44
# 出どころ:協会の発表(必ず本当)・相撲日報(一般紙 85%)・仲の良い記者(80%)・地元の事情通(70%)・スポーツ角界(スポーツ紙 65%)・週刊土俵裏(週刊誌 30%)・ネットのうわさ(20%)。名前は架空、確かさは推定。
# 情報の種類:けがで休場の見込み/引退のうわさ/若手の評判(3 年で関取になれたか)/アマチュアの進路(卒業のとき)/アマチュアの力(1 年で全国 8 強以上)/協会の番付発表。
# 不祥事・独立のうわさは出さない(実在の部屋や親方を扱うため)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
core = open(os.path.join(here,'media47_core.js'),encoding='utf-8').read()
ui = open(os.path.join(here,'media47_ui.js'),encoding='utf-8').read()
rep('<title>Sumo Manager v43</title>', '<title>Sumo Manager v44</title>')
rep("const APPV=43;\nconst SAVE='sumoManager43',SAVE42", "const APPV=44;\nconst SAVE='sumoManager44',SAVE43='sumoManager43',SAVE42")
rep('[SAVE42,SAVE41', '[SAVE43,SAVE42,SAVE41')
rep(" if(g.v===42){g.v=43;}\n return g.v===43?g:null;}", " if(g.v===42){g.v=43;}\n if(g.v===43){g.v=44;}\n return g.v===44?g:null;}")
rep('G={v:43,', 'G={v:44,')
rep("/* ========== 画面 ========== */", core+"/* ========== 画面 ========== */")
rep("function kirokuHTML(){", ui+"function kirokuHTML(){")
rep(" let h='<div class=\"pn\"><h2>達成</h2>'", " let h=mediaHTML()+'<div class=\"pn\"><h2>達成</h2>'")
rep("function doWeek(){\n if(G.phase!=='train')return;", "function doWeek(){\n if(G.phase!=='train')return;\n mWeek();")
rep(" daiki();", " daiki();\n mCycle(old);")
rep("sc.forEach(([a],i)=>{a.rec.push({b:G.bnum,c:code,t:tn,p:i+1});});", "sc.forEach(([a],i)=>{a.rec.push({b:G.bnum,c:code,t:tn,p:i+1});});mAmaRec(sc);")
rep("grad.forEach(a=>{G.ama=G.ama.filter(x=>x!==a);if(G.pros.some(p=>p.amaId===a.id))return;",
    "grad.forEach(a=>{G.ama=G.ama.filter(x=>x!==a);if(G.pros.some(p=>p.amaId===a.id)){mAmaFate(a,'pros');return;}let fate='quit';")
rep("Object.assign(n,{n:a.n,T:a.T+.4,room:Math.max(1,a.room-2),fr:a.fr,home:a.home,age:a.age+.5,rec:a.rec});G.ama.push(n);return;}",
    "Object.assign(n,{n:a.n,T:a.T+.4,room:Math.max(1,a.room-2),fr:a.fr,home:a.home,age:a.age+.5,rec:a.rec});G.ama.push(n);mAmaFate(a,'uni');return;}")
rep("p.src=(G.rel[a.sch]||0)>=25?'監督の紹介':'卒業後に入門';viewPros(p,6);G.pros.push(p);}", "p.src=(G.rel[a.sch]||0)>=25?'監督の紹介':'卒業後に入門';viewPros(p,6);G.pros.push(p);fate='pros';}")
rep("pipeHeya(a.sch);if(r.h<0)return;", "pipeHeya(a.sch);if(r.h<0){mAmaFate(a,'quit');return;}")
rep("r.n=shikona();r.tsuke=p.ama;G.R[r.id]=r;G.aiPend.push(r.id);}}});", "r.n=shikona();r.tsuke=p.ama;G.R[r.id]=r;G.aiPend.push(r.id);fate='heya';}}mAmaFate(a,fate);});")
rep("if(k==='scout'){const nn=G.pros.filter(p=>!p.seen).length;if(nn)bd='<span class=\"bd\">'+nn+'</span>';}",
    "if(k==='scout'){const nn=G.pros.filter(p=>!p.seen).length;if(nn)bd='<span class=\"bd\">'+nn+'</span>';}\n  if(k==='kiroku'&&G.media&&UI.view!=='kiroku'){const nn=G.media.L.filter(x=>x.id>(G.media.seen||0)).length;if(nn)bd='<span class=\"bd\">'+nn+'</span>';}")
rep(".bout{", ".mgrid{display:grid;gap:8px}@media(min-width:760px){.mgrid{grid-template-columns:1fr 1fr}}.mit{border:1px solid var(--line);border-radius:6px;padding:8px 10px;background:var(--paper)}.mit.nw{border-left:4px solid var(--shu)}.mh{display:flex;align-items:center;gap:6px;flex-wrap:wrap}.msrc{color:#fff;font:12px/1.7 var(--kaku);padding:0 6px;border-radius:3px}.mst{color:#c9a24a;font-size:13px;letter-spacing:-1px}.mst i{color:var(--line);font-style:normal}.mwk{margin-left:auto;font:12px var(--kaku);color:var(--mute)}.mt{margin:4px 0 2px;font-size:15px;line-height:1.6}.msub{font:12px var(--kaku);color:var(--mute)}.mres{display:inline-block;margin-top:4px;font:12px/1.6 var(--kaku);padding:0 8px;border-radius:10px;border:1px solid var(--line);color:var(--mute)}.mres.ok{border-color:#3f6b4a;color:#3f6b4a}.mres.ng{border-color:#b5361f;color:#b5361f}\n.bout{")

rep("function sitOut(r){if(r.susp>0)return true;","function sitOut(r){if(r.susp>0)return true;if(r.mKyu===G.bnum&&r.h!==0)return true;")
rep(" if(r.h===0){\n   if(r.age>=40)p=1;"," if(r.mRet&&G.bnum>=r.mRet&&r.h!==0)p=1;\n if(r.h===0){\n   if(r.age>=40)p=1;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
