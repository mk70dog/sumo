# 部屋の注目選手とまわりの後押し(見本 oshi3)  v44 -> v45
# 注目選手:プレイヤーが追いかける力士(成績には効かない)。部屋画面のいちばん上にカード、本場所の結果でいちばん上。
# 後押し 6 項目(部屋の全員にある):おかみさん(いなければ師匠)・部屋の人望・ほかの部屋・同期・後援会・ファン。
# 追い風/向かい風:1 週ごとに気力 ±0.2/項目(合計 ±0.8 まで。推定)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
core = open(os.path.join(here,'oshi48_core.js'),encoding='utf-8').read()
ui = open(os.path.join(here,'oshi48_ui.js'),encoding='utf-8').read()
rep('<title>Sumo Manager v44</title>', '<title>Sumo Manager v45</title>')
rep("const APPV=44;\nconst SAVE='sumoManager44',SAVE43", "const APPV=45;\nconst SAVE='sumoManager45',SAVE44='sumoManager44',SAVE43")
rep('[SAVE43,SAVE42', '[SAVE44,SAVE43,SAVE42')
rep(" if(g.v===43){g.v=44;}\n return g.v===44?g:null;}", " if(g.v===43){g.v=44;}\n if(g.v===44){g.v=45;g.oshi=null;}\n return g.v===45?g:null;}")
rep('G={v:44,', 'G={v:45,oshi:null,')
rep("/* ========== 画面 ========== */", core+"/* ========== 画面 ========== */")
rep("function homeHTML(){\n let h='';", ui+"function homeHTML(){\n let h=oshiHTML();")
rep("function doWeek(){\n if(G.phase!=='train')return;\n mWeek();", "function doWeek(){\n if(G.phase!=='train')return;\n mWeek();oshiWeek();")
rep("const ob=ob0.map(oRes).map((x,i)=>Object.assign(x,{b:ob0[i]}));", "const ob=ob0.map(oRes).map((x,i)=>Object.assign(x,{b:ob0[i]}));{const os=oshiR();if(os){const k=ob.findIndex(x=>x.m.id===os.id);if(k>0)ob.unshift(ob.splice(k,1)[0]);if(k>=0)ob[0].os=1;}}")
rep("ob.map(x=>'<div class=\"r1\">'+wlBadge(x.win,x.b.fus)+' <b>'+esc(x.m.n)+'</b>", "ob.map(x=>'<div class=\"r1'+(x.os?' os':'')+'\">'+wlBadge(x.win,x.b.fus)+' '+(x.os?'<span class=\"ost\">★</span>':'')+'<b>'+esc(x.m.n)+'</b>")
css = """.oc{border:2px solid var(--shu);border-radius:8px;padding:12px 14px;background:var(--paper);margin-bottom:12px}.oc h2{margin:0 0 6px;font-size:17px;display:flex;align-items:center;gap:8px}.oc h2 .st,.ost{color:var(--shu)}.oc .chg{margin-left:auto;font:12px var(--kaku);border:1px solid var(--line);border-radius:12px;padding:2px 10px;color:var(--mute);background:none;cursor:pointer}.oc .nm{font-size:22px;font-weight:bold;cursor:pointer;color:var(--sumi)}.oc .rk{font:14px var(--kaku);color:var(--mute);margin-left:6px}.oc .goal{margin:6px 0;font:14px var(--kaku)}.oc .goal b{color:var(--shu)}.oc .ms{font:13px var(--kaku);color:var(--sumi2);border-top:1px dashed var(--line);padding-top:6px;margin-top:6px}.ow{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:center}@media(max-width:600px){.ow{grid-template-columns:1fr}}.ol{font:13px/1.6 var(--kaku);padding-left:18px;margin:0}.ol li{margin:3px 0}.ol span{color:var(--mute)}.ol li.sn b{color:var(--ai)}.ob{font-size:11px;border-radius:8px;padding:0 6px;color:#fff!important}.ob.sp{background:var(--shu)}.ob.sn{background:var(--ai)}.ring{position:relative;height:250px}.ring .c{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:88px;height:88px;border-radius:50%;border:3px solid var(--shu);display:flex;align-items:center;justify-content:center;text-align:center;font:bold 15px/1.3 serif;background:var(--paper);color:var(--sumi);z-index:1}.ring .pb{position:absolute;transform:translate(-50%,-50%);width:104px;text-align:center;font:12px/1.4 var(--kaku);border:1px solid var(--line);border-radius:8px;padding:4px;background:var(--paper);color:var(--sumi);z-index:1}.ring .pb b{display:block;font-size:13px}.ring .pb.sp{border:2px solid var(--shu)}.ring .pb.sn{border:2px solid var(--ai)}.ring svg{position:absolute;inset:0;width:100%;height:100%}.r1.os{background:var(--washi2);border-radius:6px;padding-left:6px}.opl{display:flex;flex-wrap:wrap;gap:6px;max-height:50vh;overflow:auto}.opl .btn small{font-size:11px;opacity:.8}
.bout{"""
rep(".bout{", css)
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
