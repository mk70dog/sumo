/* v116 部屋の画面の絵の左側に「部屋日誌」(新しい 3 件)を出す。右の「部屋の様子」の日誌の行はなくす。左の欄は絵の上から使う(見本 dy1) */
(function(){
const V=1;
const cut=t=>esc(String(t).replace(/^〔[^〕]*〕/,''));
const when=t=>{const m=String(t).match(/^〔([^〕]*)〕/);return m?m[1]:'';};
hbYosu=function(){const o=own();const sek=o.filter(r=>r.d<=1);
 return '<div class="hbp hby"><div class="hbk">部屋の様子</div><div class="hbl"><b>関取</b>'+(sek.length?sek.map(r=>esc(r.n)+'('+esc(r.rk)+')').join('、'):'なし')+'</div><div class="hbl"><b>弟子</b>'+o.length+' 人・部屋付き親方 '+G.staff.filter(s=>s.role==='co').length+' 人</div></div>';};
function more(){return '<button class="chg" onclick="(function(){const h=[...document.querySelectorAll(\'.pn h2\')].find(x=>x.textContent.includes(\'部屋日誌\'));if(h)h.scrollIntoView({behavior:\'smooth\'});})()">すべて</button>';}
function diary(n,opt){const L=(G.log||[]).slice(0,n);
 return '<div class="hbp hbdy'+(opt.sc?' sc':'')+'"><div class="hbk">部屋日誌'+(opt.more?more():'')+'</div>'+(L.length?L.map((t,i)=>'<div class="dyl'+(i===0&&opt.hi?' hi':'')+'">'+(opt.date&&when(t)?'<small>'+esc(when(t))+'</small>':'')+cut(t)+'</div>').join(''):'<div class="dyl mute">まだありません</div>')+'</div>';}
const koeS=()=>'<div class="hbp hbv"><div class="hbk">部屋の声<small>押すと話が聞けます</small></div><div class="kp dyk">'+koePeople().map((p,i)=>'<button onclick="koeModal('+i+')">'+esc(p.who)+'</button>').join('')+'</div></div>';
/* 左の欄は土俵より上の空きも使う(絵の左上から) */
const _fit=hbFit;hbFit=function(){_fit();const st=document.querySelector('.hbs');if(!st||st.classList.contains('nar'))return;const l=st.querySelector('.hbleft');if(l)l.style.top='10px';};
if(V===1)HBL[2].left=()=>hbKoe()+diary(3,{});
if(V===2)HBL[2].left=()=>diary(5,{hi:1})+koeS();
if(V===3)HBL[2].left=()=>hbKoe()+diary(8,{date:1,sc:1,more:1});
document.head.insertAdjacentHTML('beforeend','<style>.hbdy .dyl{font-size:13px;line-height:1.45;padding:0;margin:0;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.hbdy .dyl+.dyl{margin-top:9px}.hbdy .dyl small{font-size:11px;opacity:.7;margin-right:4px}.hbdy .dyl.hi{font-weight:bold}.hbdy.sc{max-height:360px;overflow-y:auto}.hbdy .hbk .chg{float:right}.kp.dyk{display:grid;grid-template-columns:1fr 1fr;gap:4px}.kp.dyk button{padding:4px 6px;font-size:13px}</style>');
})();
