<script>
/* 見本 hb1〜hb5:ホーム(部屋)画面の背景に錦絵(稽古場)。やることは上と左右に分け、土俵(と土俵の上の力士・親方)には何も重ねない。
   URL の #hb1〜#hb5 で切りかえ(なければ hb1)。土俵の位置は絵の座標(横 195〜948、縦 320〜896 / 1200×896)から計算して、空いているところに札を置く。 */
const HB_IMG='data:image/jpeg;base64,__HBIMG__';
const HB_BOX={x0:195,x1:948,y0:320,W:1200,H:896};
function hbV(){const m=(location.hash||'').match(/hb(\d)/);return m?+m[1]:1;}
function hbTodo(row){const L=[];/* row=横一列(上の帯用) */
 const ev=G.ev.length?'<span class="hbev">親方の悩みごと '+G.ev.length+' 件<small>下で答えられます</small></span>':'';
 let t='',sub='',bt='';
 if(G.phase==='train'){t='稽古 第'+G.wk+'週';sub=bname(G.bnum)+'の初日まであと '+(WEEKS-G.wk+1)+' 週';bt='<button class="btn main" onclick="doWeekUI()">1 週間を過ごす</button><button class="btn ai" onclick="doToBasho()">初日まで進める</button><button class="btn" onclick="go(\'keiko\')">稽古を決める</button>';}
 else if(G.phase==='basho'){t='本場所の最中';sub=G.B.day?G.B.day+'日目まで':'初日前';bt='<button class="btn main" onclick="go(\'basho\')">本場所の画面へ</button>';}
 else{t='場所を終えて';sub=G.ev.length?'出来事に答えると進めます':'';bt='<button class="btn main" onclick="doNext()">番付発表へ進む</button>';}
 if(row)return '<div class="hbp hbt line"><div class="hbk">今週やること</div><div class="hbln"><h3>'+t+'<small>'+sub+'</small></h3>'+(G.phase==='train'?weekDots():'')+'<div class="hbb row">'+bt+'</div>'+ev+'</div></div>';
 return '<div class="hbp hbt"><div class="hbk">今週やること</div><h3>'+t+'<small>'+sub+'</small></h3>'+(G.phase==='train'?weekDots():'')+'<div class="hbb">'+bt+'</div>'+(ev?'<div>'+ev+'</div>':'')+'</div>';}
function hbOshi(){const r=oshiR();if(!r)return '';return '<div class="hbp hbo"><div class="hbk">★ 注目選手<button class="chg" onclick="oshiPick()">変える</button></div><h3><a onclick="showR('+r.id+')">'+esc(r.n)+'</a><small>'+esc(r.rk)+'・'+Math.floor(r.age)+' 歳</small></h3><div class="hbg">'+oshiGoal(r)+'</div>'+oshiTags(r)+'</div>';}
function hbKoe(){return '<div class="hbp hbv"><div class="hbk">部屋の声<small>押すと話が聞けます</small></div><div class="kp">'+koePeople().map((p,i)=>'<button onclick="koeModal('+i+')">'+esc(p.who)+' <small>'+esc(p.role)+'</small></button>').join('')+'</div></div>';}
function hbYosu(){const o=own();const sek=o.filter(r=>r.d<=1);const lg=(G.log||[])[0]||'';
 return '<div class="hbp hby"><div class="hbk">部屋の様子</div><div class="hbl"><b>関取</b>'+(sek.length?sek.map(r=>esc(r.n)+'('+esc(r.rk)+')').join('、'):'なし')+'</div><div class="hbl"><b>弟子</b>'+o.length+' 人・部屋付き親方 '+G.staff.filter(s=>s.role==='co').length+' 人</div><div class="hbl hbn"><b>日誌</b>'+esc(lg.replace(/^〔[^〕]*〕/,''))+'</div></div>';}
function hbDiary(){const L=(G.log||[]).slice(0,3);return '<div class="hbp hbd"><div class="hbk">部屋日誌</div>'+L.map(t=>'<div class="hbl">'+esc(t.replace(/^〔[^〕]*〕/,''))+'</div>').join('')+'</div>';}
const HBL={
 1:{fit:'contain',name:'左右の札',top:()=>hbTodo(true),left:()=>hbOshi(),right:()=>hbKoe()+hbYosu()},
 2:{fit:'cover',name:'上に帯',top:()=>hbTodo(true),left:()=>hbKoe(),right:()=>hbOshi()+hbYosu()},
 3:{fit:'contain',name:'掛け軸',cls:'kake',top:()=>'<div class="hbban">'+esc(me().n)+'部屋・'+bname(G.bnum)+'・'+phaseText()+weekDots()+'</div>',left:()=>hbTodo(false)+hbKoe(),right:()=>hbOshi()+hbYosu()},
 4:{fit:'contain',name:'三枚の札',top:()=>'<div class="hb3">'+hbTodo(false)+hbOshi()+hbDiary()+'</div>',left:()=>hbKoe(),right:()=>hbYosu()},
 5:{fit:'cover',name:'すっきり',top:()=>hbTodo(true),left:()=>'',right:()=>hbOshi()}
};
function hbStage(){const v=HBL[hbV()]||HBL[1];
 return '<div class="hbs '+(v.cls||'')+' f'+v.fit+'" data-fit="'+v.fit+'"><div class="hbblur"></div><div class="hbimg"></div>'+
  '<div class="hbslot hbtop">'+v.top()+'</div><div class="hbslot hbleft">'+v.left()+'</div><div class="hbslot hbright">'+v.right()+'</div>'+
  '<div class="hbcap">見本 hb'+hbV()+'「'+v.name+'」 背景:江戸時代の錦絵(相撲部屋の稽古場)</div></div>';}
/* 土俵の位置から、上・左・右の空きを計算して札の大きさを決める。狭い画面では絵の下に並べる */
function hbFit(){const st=document.querySelector('.hbs');if(!st)return;const W=st.clientWidth;const top=st.getBoundingClientRect().top+scrollY;
 let H=Math.max(480,Math.min(innerHeight-Math.max(0,top-scrollY)-8,900));const fit=st.dataset.fit;
 let s,ox,oy;if(fit==='contain'){s=H/HB_BOX.H;if(HB_BOX.W*s>W){s=W/HB_BOX.W;H=HB_BOX.H*s;}ox=(W-HB_BOX.W*s)/2;oy=0;}else{s=Math.max(W/HB_BOX.W,H/HB_BOX.H);ox=(W-HB_BOX.W*s)/2;oy=H-HB_BOX.H*s;}
 const L=ox+HB_BOX.x0*s,Rr=W-(ox+HB_BOX.x1*s),T=oy+HB_BOX.y0*s;
 st.style.height=H+'px';const im=st.querySelector('.hbimg');im.style.cssText='left:'+ox+'px;top:'+oy+'px;width:'+(HB_BOX.W*s)+'px;height:'+(HB_BOX.H*s)+'px';
 const nar=L<170&&Rr<170;st.classList.toggle('nar',nar);
 const t=st.querySelector('.hbtop'),l=st.querySelector('.hbleft'),r=st.querySelector('.hbright');
 if(nar){[t,l,r].forEach(x=>x.style.cssText='');return;}
 const g=8;t.style.cssText='left:'+g+'px;right:'+g+'px;top:'+g+'px;height:'+Math.max(0,T-2*g)+'px';
 l.style.cssText='left:'+g+'px;top:'+(T)+'px;bottom:'+g+'px;width:'+Math.max(0,L-2*g)+'px';
 r.style.cssText='right:'+g+'px;top:'+(T)+'px;bottom:'+g+'px;width:'+Math.max(0,Rr-2*g)+'px';
 // 上の帯に入りきらない分は、左右の欄へ(土俵の高さより上の分も使えるよう、左右は帯の下から)
 if(t.children.length&&t.scrollHeight>t.clientHeight+4&&!st.dataset.out){st.dataset.out=1;const box=document.createElement('div');box.className='hbout';while(t.firstChild)box.appendChild(t.firstChild);st.before(box);return hbFit();}
}
const hbR0=render0;
render0=function(){hbR0();if(!G||UI.title||UI.view!=='home'||G.mp)return;const app=$('#app');
 const oc=app.querySelector(':scope > .oc');if(oc)oc.remove();
 [...app.querySelectorAll(':scope > .pn')].forEach(p=>{const h=p.querySelector('h2');const t=h?h.textContent:'';if(/^稽古 第|^部屋の声|^本場所の最中/.test(t))p.remove();});
 const nav=app.querySelector('.nav')||app.children[1];nav.insertAdjacentHTML('afterend',hbStage());requestAnimationFrame(hbFit);};
addEventListener('resize',()=>requestAnimationFrame(hbFit));addEventListener('hashchange',()=>render());
</script>
<style>
.hbs{position:relative;margin:0 0 12px;border-radius:10px;overflow:hidden;background:#2b2018}
.hbs .hbblur{position:absolute;inset:-20px;background:url(__HBURL__) center/cover;filter:blur(18px) brightness(.55)}
.hbs.fcover .hbblur{display:none}
.hbs .hbimg{position:absolute;background:url(__HBURL__) center/100% 100% no-repeat}
.hbslot{position:absolute;display:flex;flex-direction:column;gap:8px;overflow:auto;z-index:2}
.hbtop{flex-direction:row;align-items:flex-start;justify-content:center}
.hbtop>.hbp{flex:0 1 auto;max-width:720px}
.hbslot.hbleft,.hbslot.hbright{justify-content:flex-start}
.hbp{background:rgba(251,246,234,.93);border:1px solid rgba(120,80,40,.45);border-radius:8px;padding:8px 10px;box-shadow:0 2px 8px rgba(0,0,0,.25);color:#2a1d12;font-size:13px;line-height:1.5}
.hbp h3{margin:2px 0 4px;font-size:16px}.hbp h3 small{font-size:11px;font-weight:normal;margin-left:6px;color:#6b5a48}
.hbk{font-size:12px;font-weight:bold;color:#9a2b1d;border-bottom:1px dashed rgba(120,80,40,.4);margin-bottom:4px;display:flex;align-items:center;gap:6px}
.hbk small{font-weight:normal;color:#6b5a48}.hbk .chg{margin-left:auto;font-size:11px}
.hbb{display:flex;flex-direction:column;gap:6px;margin-top:6px}.hbb.row{flex-direction:row;flex-wrap:wrap}.hbb .btn{margin:0;padding:6px 12px;font-size:14px}
.hbt .daybar{margin:4px 0}
.hbt.line{padding:4px 10px}.hbt.line .hbk{border:none;margin:0}.hbln{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.hbln h3{margin:0;white-space:nowrap}.hbln .daybar{width:120px;margin:0}.hbln .hbb{margin:0}.hbln .hbev{margin:0}
.hbev{display:inline-block;margin-top:6px;background:#9a2b1d;color:#fff;border-radius:6px;padding:3px 8px;font-size:12px}.hbev small{margin-left:6px;opacity:.85}
.hbg{font-size:12px;margin-bottom:4px}.hbo .otg{display:flex;flex-wrap:wrap;gap:3px}.hbo .otag{font-size:11px}
.hbv .kp{display:flex;flex-wrap:wrap;gap:4px}.hbv .kp button{font-size:12px;padding:3px 8px}
.hbl{font-size:12px;margin:2px 0}.hbl b{color:#6b5a48;margin-right:6px;font-weight:normal}.hbn{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.hbout{display:flex;justify-content:center;margin:0 0 8px}.hbout>.hbp{max-width:100%}
.hbcap{position:absolute;right:8px;bottom:4px;font-size:10px;color:#f3e6c8;text-shadow:0 1px 2px #000;z-index:3}
.hb3{display:flex;gap:8px;width:100%;align-items:flex-start}.hb3>.hbp{flex:1;max-height:100%;overflow:auto}
.hbban{align-self:flex-start;background:rgba(40,25,15,.82);color:#f3e6c8;border:1px solid #c9a24a;border-radius:6px;padding:6px 12px;font-size:14px}.hbban .daybar{margin-top:4px}
/* 掛け軸 */
.kake .hbleft>.hbp,.kake .hbright>.hbp{border:none;border-left:6px solid #5a3a22;border-right:6px solid #5a3a22;border-radius:2px;position:relative;margin:10px 0;background:linear-gradient(#f6eedb,#efe3c6)}
.kake .hbleft>.hbp::before,.kake .hbright>.hbp::before,.kake .hbleft>.hbp::after,.kake .hbright>.hbp::after{content:'';position:absolute;left:-10px;right:-10px;height:8px;background:#3b2414;border-radius:4px}
.kake .hbleft>.hbp::before,.kake .hbright>.hbp::before{top:-8px}.kake .hbleft>.hbp::after,.kake .hbright>.hbp::after{bottom:-8px}
/* 狭い画面:絵の上には何も置かず、下に並べる */
.hbs.nar{overflow:visible;background:none}.hbs.nar .hbblur{display:none}
.hbs.nar .hbimg{position:relative;display:block;left:auto!important;top:auto!important;width:100%!important;aspect-ratio:1200/896;height:auto!important;border-radius:10px}
.hbs.nar{height:auto!important}.hbs.nar .hbslot{position:static;margin-top:8px}.hbs.nar .hbtop{flex-direction:column}.hbs.nar .hb3{flex-direction:column}.hbs.nar .hbout{display:flex;justify-content:center;margin:0 0 8px}.hbout>.hbp{max-width:100%}
.hbcap{position:static;color:#6b5a48;text-shadow:none}
</style>
