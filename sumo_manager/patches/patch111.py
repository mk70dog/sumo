# v108:注目選手を 3 人まで(見本 os2「名前のタブで切りかえ」)。v107 → v108
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=107;\nconst SAVE='sumoManager107',SAVE106", "const APPV=108;\nconst SAVE='sumoManager108',SAVE107='sumoManager107',SAVE106")
rep('[SAVE106,SAVE105', '[SAVE107,SAVE106,SAVE105')
rep('<title>Grand Sumo Manager v107','<title>Grand Sumo Manager v108')
# 1. 注目選手の持ち方:G.oshi は id の配列(3 人まで)。前の版の数字 1 つも読める。選んでいなければ部屋頭
rep("function oshiR(){let r=G.oshi!=null?G.R[G.oshi]:null;if(!r||r.ret||r.h!==ME())r=heyaTop();return r;}",
 "function oshiIds(){let a=G.oshi;if(a==null)a=[];if(!Array.isArray(a))a=[a];return a.filter(id=>{const r=G.R[id];return r&&!r.ret&&r.h===ME();}).slice(0,3);}\n"
 "function oshiL(){const a=oshiIds().map(id=>G.R[id]);if(!a.length){const t=heyaTop();if(t)a.push(t);}return a;}\n"
 "function oshiR(){return oshiL()[0]||null;}\n"
 "function isOshi(r){return !!r&&oshiL().some(x=>x.id===r.id);}")
# 2. 選ぶまど:押した順に①②③、もう一度押すと外れる
rep("""function oshiPick(){const o=own().slice().sort((a,b)=>a.pos-b.pos);const cur=oshiR();
 openM('<h2>注目選手を選ぶ</h2><p class="kaku mute">部屋を見守るうえで、追いかけたい力士を選びます。成績には影響しません。</p><div class="opl">'+o.map(r=>'<button class="btn'+(cur&&cur.id===r.id?' main':'')+'" onclick="G.oshi='+r.id+';save();closeM();render()">'+esc(r.n)+' <small>'+esc(r.rkS)+'</small></button>').join('')+'</div><div class="row" style="margin-top:10px"><button class="btn" onclick="G.oshi=null;save();closeM();render()">部屋頭にもどす(自動)</button><button class="btn" onclick="closeM()">閉じる</button></div>');}""",
"""function oshiPick(){const o=own().slice().sort((a,b)=>a.pos-b.pos);const cur=oshiIds();
 openM('<h2>注目選手を選ぶ(3 人まで)</h2><p class="kaku mute">追いかけたい力士を 3 人まで選びます。押した順に ①②③ になり、もう一度押すと外れます。選ばないときは部屋頭になります。成績には影響しません。</p><div class="opl">'+o.map(r=>{const i=cur.indexOf(r.id);return '<button class="btn'+(i>=0?' main':'')+'" onclick="osTog('+r.id+')">'+(i>=0?'①②③'[i]+' ':'')+esc(r.n)+' <small>'+esc(r.rkS)+'</small></button>';}).join('')+'</div><div class="row" style="margin-top:10px"><button class="btn" onclick="G.oshi=null;save();closeM();render()">部屋頭にもどす(自動)</button><button class="btn" onclick="closeM()">閉じる</button></div>');}
function osTog(id,fromR){let a=oshiIds();const i=a.indexOf(id);if(i>=0)a.splice(i,1);else{if(a.length>=3){toast('注目選手は 3 人までです。どれかを外してください');return;}a.push(id);}G.oshi=a.length?a:null;save();if(fromR)showR(id);else oshiPick();render();}""")
# 3. 力士のまど:注目選手にする/外す
rep("""(oshiR()&&oshiR().id===r.id?'<p class="kaku"><span class="ost">★</span> 注目選手</p>':'<p><button class="btn sm" onclick="G.oshi='+r.id+';save();showR('+r.id+')">★ 注目選手にする</button></p>')""",
"""(oshiIds().includes(r.id)?'<p class="kaku"><span class="ost">★</span> 注目選手 <button class="btn sm" onclick="osTog('+r.id+',1)">注目選手から外す</button></p>':r.h!==ME()?'':(isOshi(r)?'<p class="kaku"><span class="ost">★</span> 注目選手(部屋頭なので自動) <button class="btn sm" onclick="osTog('+r.id+',1)">★ 注目選手にする</button></p>':'<p><button class="btn sm" onclick="osTog('+r.id+',1)">★ 注目選手にする</button> <small class="mute">'+oshiIds().length+'/3 人</small></p>'))""")
# 4. 本場所の結果:注目選手を ①②③ の順でいちばん上に
rep("{const os=oshiR();if(os){const k=ob.findIndex(x=>x.m.id===os.id);if(k>0)ob.unshift(ob.splice(k,1)[0]);if(k>=0)ob[0].os=1;}}",
 "{const L=oshiL();for(let j=L.length-1;j>=0;j--){const k=ob.findIndex(x=>x.m.id===L[j].id);if(k>=0){const x=ob.splice(k,1)[0];x.os=1;ob.unshift(x);}}}")
# 5. 次の取組の並び(2 か所)
rep("{const os=oshiR();if(os){const k=nx.findIndex(p=>p[0]===os.id||p[1]===os.id);if(k>0)nx.unshift(nx.splice(k,1)[0]);}}",
 "{const L=oshiL();for(let j=L.length-1;j>=0;j--){const id=L[j].id;const k=nx.findIndex(p=>p[0]===id||p[1]===id);if(k>=0)nx.unshift(nx.splice(k,1)[0]);}}",2)
# 6. ★と色(次の取組・星取表)
rep("oshiR()&&oshiR().id===a.id","isOshi(a)",2)
rep("oshiR()&&oshiR().id===r.id","isOshi(r)",2)
# 7. 部屋の画面の右の欄:名前のタブで切りかえ(見本 os2)
rep("""function hbOshi(){const r=oshiR();if(!r)return '';return '<div class="hbp hbo"><div class="hbk">★ 注目選手<button class="chg" onclick="oshiPick()">変える</button></div><h3>""",
"""function hbOshi(){const L=oshiL();if(!L.length)return '';const k=Math.min(UI.osTab||0,L.length-1);const r=L[k];return '<div class="hbp hbo"><div class="hbk">★ 注目選手 <small>'+oshiIds().length+'/3 人</small><button class="chg" onclick="oshiPick()">選ぶ</button></div>'+(L.length>1?'<div class="ostab">'+L.map((x,i)=>'<button class="'+(i===k?'on':'')+'" onclick="UI.osTab='+i+';render()">'+esc(x.n)+'</button>').join('')+'</div>':'')+'<h3>""")
rep("</head>","<style>.ostab{display:flex;gap:4px;margin:2px 0 6px}.ostab button{flex:1;min-width:0;font-size:12px;padding:3px 4px;border:1px solid rgba(120,80,40,.4);background:#f3ead6;color:#3a2a1a;border-radius:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}.ostab button.on{background:#9a2b1d;color:#fff;border-color:#9a2b1d}</style></head>")
open(dst,'w',encoding='utf-8').write(s)
print('ok')
