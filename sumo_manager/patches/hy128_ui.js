<script>
/* v128 画面:記録の画面のいちばん上に「部屋の歩み」(殿堂・年表・部屋の記録) */
var HY_V=window.HY_V||3;
function hyLv(s){s=s||'';return /横綱/.test(s)?6:/大関/.test(s)?5:/関脇|小結/.test(s)?4:/前頭/.test(s)?3:/十両/.test(s)?2:1;}
function hyYr(b){const y=Math.floor((b-1)/6)+1;return G.y0?(G.y0+y-1)+'年':y+'年目';}
function hyPeople(){const m=ME();const A=own().map(r=>({n:r.n,rk:bestRankAll(r)||r.rk,yu:r.yu.slice(),sh:r.sansho||0,kin:r.kin||0,cw:r.cw,cl:r.cl,act:1,deb:hyDeb(r),sek:r.sekD||null,st:hyNote(r),now:r.rk,id:r.id}));
 const Rt=G.retired.filter(x=>x.oh!=null?x.oh===m:(x.own&&!G.P)).map(x=>({n:x.n,rk:x.bestRk,yu:x.yu||[0,0,0,0,0,0],sh:x.sansho||0,kin:x.kin||0,cw:x.cw,cl:x.cl,act:0,b:x.b,age:x.age,deb:x.deb||null,sek:x.sek||null,st:x.st||[]}));
 return A.concat(Rt).map(p=>Object.assign(p,{lv:hyLv(p.rk)}));}
function hyHall(P){return P.filter(p=>p.lv>=5||p.yu[0]>0).sort((a,b)=>b.lv-a.lv||b.yu[0]-a.yu[0]||b.cw-a.cw);}
function hySeki(P){return P.filter(p=>p.lv>=2).sort((a,b)=>b.lv-a.lv||b.cw-a.cw);}
function hyYears(P){const Y={};const add=(b,t,c)=>{if(b==null||b<1)return;const y=Math.floor((b-1)/6)+1;(Y[y]=Y[y]||{ev:[],in:0}).ev.push({b:b,t:t,c:c});};
 P.forEach(p=>{(p.st||[]).forEach(x=>{if(x.k==='in'){const y=Math.floor((x.b-1)/6)+1;(Y[y]=Y[y]||{ev:[],in:0}).in++;return;}
   if(x.k==='up'&&!/^(新十両|新入幕|新三役|大関|横綱)/.test(x.t))return;if(x.k==='yu'&&!/^(幕内|十両)/.test(x.t))return;
   add(x.b,p.n+':'+x.t,x.k);});
  if(!p.act&&p.lv>=2)add(p.b,p.n+'('+p.rk+')が引退','rt');});
 (G.yr||[]).forEach(r=>{const o=Y[r.y]=Y[r.y]||{ev:[],in:0};o.yr=r;});
 return Object.keys(Y).map(Number).sort((a,b)=>b-a).map(y=>Object.assign({y:y},Y[y]));}
function hyRec(P){const best=(f,ok)=>{let x=null;P.forEach(p=>{const v=f(p);if(v!=null&&(ok?ok(v):v>0)&&(!x||v>x[1]))x=[p,v];});return x;};
 const fast=(()=>{let x=null;P.forEach(p=>{if(p.deb>1&&p.sek&&p.sek>p.deb){const v=p.sek-p.deb;if(!x||v<x[1])x=[p,v];}});return x;})();
 const sk=G.skS||{c:0,m:0};const R=[];
 const w=best(p=>p.cw);if(w)R.push(['最多勝利',w[0].n,'通算 '+w[1]+' 勝']);
 const y=best(p=>p.yu[0]);if(y)R.push(['最多 幕内優勝',y[0].n,y[1]+' 回']);
 const ya=best(p=>p.yu.reduce((a,b)=>a+b,0));if(ya)R.push(['最多 優勝(全部の段)',ya[0].n,ya[1]+' 回']);
 const s=best(p=>p.sh);if(s)R.push(['最多 三賞',s[0].n,s[1]+' 回']);
 const k=best(p=>p.kin);if(k)R.push(['最多 金星',k[0].n,k[1]+' 個']);
 if(fast)R.push(['最速 新十両',fast[0].n,'初土俵から '+fast[1]+' 場所(前相撲からの実際の最速は 6 場所)']);
 R.push(['関取が続いた場所','いま '+sk.c+' 場所','いちばん長い '+sk.m+' 場所',1]);
 return R;}
function hyEvRow(e){const c={up:'#b5361f',yu:'#c9a24a',sh:'#3f6b4a',fk:'#d0641c',rt:'#555'}[e.c]||'#888';return '<div class="hye"><i style="background:'+c+'"></i>'+esc(e.t)+'</div>';}
function hyYearBlock(Y,n){return Y.slice(0,n).map(o=>'<div class="hyy"><div class="hyyl"><b>'+hyYr(o.y*6)+'</b>'+(o.yr?'<span>評価 '+o.yr.g+'・'+o.yr.rk+' 位</span><span>関取 '+o.yr.sk+'・弟子 '+o.yr.di+'</span>':'')+(o.in?'<span>入門 '+o.in+' 人</span>':'')+'</div><div class="hyyr">'+(o.ev.length?o.ev.sort((a,b)=>a.b-b.b).map(hyEvRow).join(''):'<span class="mute">大きな出来事はなし</span>')+'</div></div>').join('');}
function hyCard(p){const yu=p.yu.map((c,d)=>c?DN[d]+c:'').filter(x=>x).join('・');
 return '<div class="hyc lv'+p.lv+'"><div class="hycn">'+esc(p.n)+'</div><div class="hycr">'+esc(p.rk)+'</div><div class="mute" style="font-size:12px">'+(yu?'優勝 '+yu+'<br>':'')+(p.sh?'三賞 '+p.sh+'・':'')+'通算 '+p.cw+'勝'+(p.act?'・現役':'・'+hyYr(p.b)+'引退')+'</div></div>';}
function hySekTable(S){return '<div style="overflow-x:auto"><table class="tb"><tr><th>四股名</th><th>最高位</th><th>優勝</th><th>三賞</th><th>通算</th><th></th></tr>'+S.map(p=>'<tr><td class="nm">'+esc(p.n)+'</td><td>'+esc(p.rk)+'</td><td class="num">'+(p.yu.reduce((a,b)=>a+b,0)||'')+'</td><td class="num">'+(p.sh||'')+'</td><td class="wl">'+p.cw+'勝'+p.cl+'敗</td><td class="hyrt2">'+(p.act?'<span class="tag">現役</span>':'<span class="mute">'+hyYr(p.b)+'引退</span>')+'</td></tr>').join('')+'</table></div>';}
function hyRecTable(R){return '<table class="tb hyrt">'+R.map(x=>'<tr><td>'+x[0]+'</td><td'+(x[3]?'':' class="nm"')+'>'+esc(x[1])+'</td><td>'+esc(x[2])+'</td></tr>').join('')+'</table>';}
function hyPanel(){const P=hyPeople(),H=hyHall(P),S=hySeki(P),Y=hyYears(P),R=hyRec(P);const n=UI.hyAll?60:5;
 const more=Y.length>5&&!UI.hyAll?'<button class="btn sm" onclick="UI.hyAll=1;render()">年表をすべて見る('+Y.length+' 年)</button>':'';
 const hall=H.length?'<div class="hyh">'+H.map(hyCard).join('')+'</div>':'<p class="mute kaku">まだいません。横綱・大関・幕内優勝の弟子が殿堂に入ります。</p>';
 const head='<h2>部屋の歩み<span class="sub">'+esc(me().n)+'部屋・歴代の関取 '+S.length+' 人</span></h2>';
 if(HY_V===2){const t=UI.hyT||'hall';const tb=(k,l)=>'<button class="pc'+(t===k?' on':'')+'" onclick="UI.hyT=\''+k+'\';render()">'+l+'</button>';
  return '<div class="pn hyp">'+head+'<div style="margin-bottom:6px">'+tb('hall','殿堂')+tb('nen','年表')+tb('seki','歴代の関取')+tb('rec','部屋の記録')+'</div>'+
   (t==='hall'?hall:t==='nen'?hyYearBlock(Y,n)+more:t==='seki'?(S.length?hySekTable(S):'<p class="mute kaku">まだいません。</p>'):hyRecTable(R))+'</div>';}
 if(HY_V===3)return '<div class="pn hyp">'+head+'<h3>殿堂</h3>'+hall+'<div class="grid2"><div><h3>年表</h3>'+hyYearBlock(Y,n)+more+'</div><div><h3>部屋の記録</h3>'+hyRecTable(R)+'<h3>歴代の関取</h3>'+(S.length?hySekTable(S.slice(0,12)):'<p class="mute kaku">まだいません。</p>')+'</div></div></div>';
 return '<div class="pn hyp">'+head+'<h3>殿堂</h3>'+hall+'<h3>部屋の記録</h3>'+hyRecTable(R)+'<h3>年表</h3>'+hyYearBlock(Y,n)+more+'<details><summary>歴代の関取('+S.length+' 人)</summary>'+(S.length?hySekTable(S):'')+'</details></div>';}
const hyK0=kirokuHTML;kirokuHTML=function(){return hyPanel()+hyK0();};
</script><style>
.hyp .pc{display:inline-block!important;width:auto!important;font:13px sans-serif!important;padding:4px 12px!important;border-radius:14px!important;border:1px solid #8a7040!important;background:#fff!important;color:#1a140c!important;margin:2px!important}.hyp .pc.on{background:#7a1d10!important;border-color:#7a1d10!important;color:#fff!important;font-weight:bold}
.hyh{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin:4px 0 8px}
.hyc{border:2px solid #c9a24a;border-radius:8px;padding:6px 8px;background:linear-gradient(#fffaf0,#f6ead0);color:#1a140c}.hyc.lv6{border-color:#7a1d10;background:linear-gradient(#fff6e0,#ecd59c)}.hycn{font:bold 18px serif}.hycr{color:#7a1d10;font-size:13px}
.hyy{display:grid;grid-template-columns:110px 1fr;gap:8px;border-bottom:1px dotted var(--line);padding:4px 0;font-size:13px}.hyyl span{display:block;font-size:11px;color:var(--mute,#777)}.hye{padding:1px 0}.hye i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:middle}
.hyrt td:first-child{white-space:nowrap;color:#7a1d10}.hyrt .nm{white-space:nowrap}.hyrt2{white-space:nowrap;font-size:12px}
@media(max-width:500px){.hyy{grid-template-columns:84px 1fr}}
</style>
