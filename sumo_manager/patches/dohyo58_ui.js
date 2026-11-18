/* --- 取組を上から見た土俵で動かす(見本 kaiga20) --- */
function dhPick(b){const W=G.R[b.w],L=G.R[b.l];const E=W.pos<=L.pos?W:L,Wt=E===W?L:W;return {E,Wt,winE:E===W};}
function dhSeed(b){return (b.w*7919+b.l*104729+G.bnum*31+(G.B?G.B.day:0))>>>0;}
function dhHTML(id,b,withPh){const p=dhPick(b);return '<div class="dhbox"><div>'+dhSVG(id,p.E.n,p.Wt.n,p.E.wT,p.Wt.wT)+'</div>'+(withPh?'<ol class="dhph" id="'+id+'ph"></ol>':'')+'</div>';}
function dhRun(id,b){const p=dhPick(b);const pl=dhPlan(b.k,p.winE,dhSeed(b),p.E.n,p.Wt.n);dhPlay(id,pl,document.getElementById(id+'ph'),5200);}
function dhOpen(src,i){const b=src==='o'?(UI.dhO||[])[i]:(UI.dhT||[])[i];if(!b)return;const p=dhPick(b);
 openM('<h2>'+esc(p.E.n)+' と '+esc(p.Wt.n)+' <span class="sub">'+esc(b.k)+'</span></h2>'+dhHTML('dhm',b,1)+'<div class="row" style="margin-top:8px"><button class="btn" onclick="dhRun(\'dhm\',(UI.'+(src==='o'?'dhO':'dhT')+'||[])['+i+'])">もう一度見る</button><button class="btn" onclick="closeM()">閉じる</button></div>');
 setTimeout(()=>dhRun('dhm',b),60);}
document.head.insertAdjacentHTML('beforeend','<style>'+DH_CSS+'.dhbox{display:grid;grid-template-columns:minmax(260px,420px) 1fr;gap:12px;align-items:start}@media(max-width:640px){.dhbox{grid-template-columns:1fr}}ol.dhph{font:14px/1.8 var(--kaku);margin:0;padding-left:20px;max-height:380px;overflow:auto}ol.dhph li{color:var(--mute)}ol.dhph li.now{color:var(--sumi);font-weight:bold}ol.dhph li.crowd{color:var(--shu)}.dhbtn{font:12px var(--kaku);border:1px solid var(--line);background:var(--paper);color:var(--sumi);border-radius:12px;padding:2px 10px;margin-left:6px;cursor:pointer}.r1 .dhin{margin:6px 0}</style>');
