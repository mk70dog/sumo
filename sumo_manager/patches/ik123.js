<script>
/* v123:育成の成績(一人相撲でも)。見本 ik1+ik3 の組み合わせ。
   数えるのは「始めたとき(この版を初めて開いて最初の場所が終わったとき)に幕下以下だった力士」と、そのあと入った力士(r.ik0 がない力士)。
   点(二人相撲の「育てた力士だけ」と同じ。推定):関取 1・三役 2・大関 3・横綱 5(場所ごと)、新幕下 1・新十両 2・新入幕 3、幕内優勝 10・十両優勝 3・三賞 2。
   不祥事・年間評価は入れない(ほかの部屋と同じ決まりでくらべるため)。全部屋を数え、年の終わり(九州場所)に育成番付(順位)を記録。記録として見るだけで、お金には効かない。
   「初めて〇〇」はふだんの記録(hist は AI の力士だと 6 場所しか残らない)ではなく、届いた段の印 r.ikF(1 幕下・2 十両・3 幕内・4 三役)で見る。 */
function ikLvNow(r){return r.d===0?3:r.d===1?2:r.d===2?1:0;}
function ikInit(){if(!G||G.ik)return;G.ik={b0:G.bnum,tot:{},yr:{},c:{},y:[],rp:{}};
 const b1=divStart(1),b2=divStart(2),b3=divStart(3);
 Object.values(G.R).forEach(r=>{if(!r||r.ret)return;let lv=ikLvNow(r);const b=r.best;
  if(b!=null){if(b<b1)lv=Math.max(lv,3);else if(b<b2)lv=Math.max(lv,2);else if(b<b3)lv=Math.max(lv,1);}
  r.ikF=lv;if(r.t||r.san)r.ikS=1;if(ikLvNow(r)>=2)r.ik0=1;});}
function ikC(h){const c=G.ik.c;return c[h]||(c[h]={nb:0,nj:0,nm:0,san:0,yu:0,sh:0});}
function ikBasho(){if(!G)return;if(!G.ik)ikInit();const L=G.last||{};const yr=G.ik.yr,tot=G.ik.tot;
 const add=(r,v,lab,ck)=>{if(v){yr[r.h]=(yr[r.h]||0)+v;tot[r.h]=(tot[r.h]||0)+v;r.ikp=(r.ikp||0)+v;}
  if(lab){r.ikw=r.ikw||[];if(!r.ikw.includes(lab)){r.ikw.push(lab);if(r.ikw.length>4)r.ikw.shift();}}if(ck)ikC(r.h)[ck]++;
  if((v||lab)&&isPH(r.h)){const RP=G.ik.rp||(G.ik.rp={});const m=RP[r.h]||(RP[r.h]={});m[r.id]={n:r.n,p:r.ikp||0,w:(r.ikw||[]).slice()};}};
 G.order.forEach(id=>{const r=G.R[id];if(!r||r.ik0||r.d>2)return;const lv=ikLvNow(r),f=r.ikF||0;
  if(lv>f){if(f<1&&lv>=1)add(r,1,'新幕下','nb');if(f<2&&lv>=2)add(r,2,'新十両','nj');if(f<3&&lv>=3)add(r,3,'新入幕','nm');r.ikF=lv;}
  if(r.t&&!r.ikS){r.ikS=1;add(r,0,'新三役','san');}
  if(r.d<=1)add(r,r.t==='Y'?5:r.t==='O'?3:r.t?2:1);});
 (L.yu||[]).forEach(y=>{if(y.d>1)return;const r=G.R[y.id];if(!r||r.ik0)return;add(r,y.d===0?10:3,y.d===0?'幕内優勝':'十両優勝','yu');});
 (L.sansho||[]).forEach(x=>{const r=G.R[x.id];if(!r||r.ik0)return;add(r,2,'三賞','sh');});
 if(G.bnum%6===0){const p=G.heya.map((h,i)=>h.closed?null:Math.round(yr[i]||0));G.ik.y.push({y:curYear(),p:p});if(G.ik.y.length>60)G.ik.y.shift();G.ik.yr={};}}
function ikRank(p,h){if(p[h]==null)return null;let n=0,k=1;p.forEach((v,i)=>{if(v==null)return;n++;if(v>p[h])k++;});return {rk:k,n:n};}
const ikEB=endBasho;endBasho=function(){const r=ikEB.apply(this,arguments);try{ikBasho();}catch(e){try{sysLog('育成点',e);}catch(x){}}return r;};
['newGameReal','newGameDok','newGame'].forEach(k=>{const f=window[k];if(typeof f!=='function')return;window[k]=function(){const r=f.apply(this,arguments);try{if(G&&!G.ik)ikInit();}catch(e){}return r;};});
/* 記録の画面 */
function ikChart(h,Y){const n=Y.length;if(n<2)return '<p class="mute" style="font-size:12px">2 年分たまると、順位の移り変わりのグラフが出ます。</p>';
 const R=Y.map(x=>ikRank(x.p,h)),NN=Math.max(...R.map(x=>x?x.n:1)),mx=Math.max(10,...Y.map(x=>x.p[h]||0))*1.15;
 const w=520,hh=170,px=34,X=i=>px+(w-px-14)*i/(n-1),Yr=r=>14+(r-1)/Math.max(1,NN-1)*(hh-40),Yb=v=>hh-22-(hh-40)*v/mx;let g='';
 [1,10,20,30,NN].filter((v,i,a)=>v<=NN&&a.indexOf(v)===i).forEach(r=>{g+='<line x1="'+px+'" x2="'+(w-10)+'" y1="'+Yr(r)+'" y2="'+Yr(r)+'" stroke="#e5dcc6"/><text x="'+(px-4)+'" y="'+(Yr(r)+4)+'" font-size="10" text-anchor="end" fill="#888">'+r+'位</text>';});
 const bw=Math.max(4,Math.min(24,(w-px)/n*.5));
 Y.forEach((x,i)=>{const v=x.p[h]||0;g+='<rect x="'+(X(i)-bw/2)+'" y="'+Yb(v)+'" width="'+bw+'" height="'+(hh-22-Yb(v))+'" fill="#c9a24a55"/>';if(n<=12||i%Math.ceil(n/10)===0||i===n-1)g+='<text x="'+X(i)+'" y="'+(hh-6)+'" font-size="10" text-anchor="middle" fill="#888">'+x.y+'</text>';});
 const pts=R.map((r,i)=>r?X(i)+','+Yr(r.rk):null).filter(Boolean);
 g+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#b5391f" stroke-width="2.5"/>'+R.map((r,i)=>r?'<circle cx="'+X(i)+'" cy="'+Yr(r.rk)+'" r="'+(n>15?2.5:4)+'" fill="#b5391f"/>'+(n<=12?'<text x="'+X(i)+'" y="'+(Yr(r.rk)-8)+'" font-size="11" text-anchor="middle" fill="#b5391f">'+r.rk+'位</text>':''):'').join('');
 return '<svg viewBox="0 0 '+w+' '+hh+'" style="width:100%;max-width:640px">'+g+'</svg><div class="mute" style="font-size:12px"><span style="color:#b5391f">━</span> 育成番付の順位　<span style="color:#c9a24a">■</span> その年の育成点</div>';}
function ikCard(){if(!G)return '';const h=ME();const head='<h2>育成の成績<span class="sub">始めたときに幕下以下だった力士と、そのあと入った力士の点(推定の点数)</span></h2>';
 if(!G.ik)return '<div class="pn ikp">'+head+'<p class="mute">最初の場所が終わると数え始めます。いま関取の力士は数えません。</p></div>';
 const I=G.ik,Y=I.y,tot=Math.round(I.tot[h]||0),now=Math.round(I.yr[h]||0);
 const pNow=G.heya.map((x,i)=>x.closed?null:Math.round(I.yr[i]||0)),rNow=ikRank(pNow,h);
 const last=Y.length?ikRank(Y[Y.length-1].p,h):null,prev=Y.length>1?ikRank(Y[Y.length-2].p,h):null;
 const big=last?'<b>'+last.rk+' 位</b><span>'+last.n+' 部屋中'+(prev?'・その前の年 '+prev.rk+' 位':'')+'</span>':'<b>—</b><span>年の終わり(九州場所)に決まります</span>';
 const yrs=Math.max(0,(G.bnum-I.b0)/6);const c=I.c[h]||{nb:0,nj:0,nm:0,san:0,yu:0,sh:0};
 const top=Object.entries((I.rp||{})[h]||{}).map(([id,x])=>{const r=G.R[id];return {n:r?r.n:x.n,ikp:x.p,ikw:x.w,ret:!r||r.ret||r.h!==h};}).filter(x=>x.ikp>0).sort((a,b)=>b.ikp-a.ikp).slice(0,3);
 return '<div class="pn ikp">'+head+
  '<div class="ikg"><div class="ikb"><small>通算の育成点</small><b>'+tot+'</b><span>'+(yrs>=1?Math.floor(yrs)+' 年':'始めてから')+'</span></div><div class="ikb"><small>今年('+curYear()+' 年・途中)</small><b>'+now+'</b><span>点'+(rNow&&now>0?'・いま '+rNow.rk+' 位':'')+'</span></div><div class="ikb hl"><small>育成番付'+(last?'('+Y[Y.length-1].y+' 年)':'')+'</small>'+big+'</div></div>'+
  '<div class="ikc">'+[['新幕下',c.nb],['新十両',c.nj],['新入幕',c.nm],['新三役以上',c.san],['優勝',c.yu],['三賞',c.sh]].map(x=>'<span>'+x[0]+' <b>'+x[1]+'</b></span>').join('')+'</div>'+
  '<div class="ik3"><div><h4>育成番付の移り変わり</h4>'+ikChart(h,Y.slice(-20))+'</div><div><h4>点の多い力士</h4>'+(top.length?top.map((r,i)=>'<div>'+(i+1)+'. <b class="nm">'+esc(r.n)+'</b> '+Math.round(r.ikp)+' 点'+(r.ret?' <span class="mute">(引退・移籍)</span>':'')+(r.ikw&&r.ikw.length?' <span class="mute">('+esc(r.ikw.join('・'))+')</span>':'')+'</div>').join(''):'<p class="mute" style="font-size:13px">まだいません。新幕下・関取が出ると点が入ります。</p>')+
  (Y.length?'<details style="margin-top:8px"><summary>年ごとの表</summary><table class="tb"><tr><th>年</th><th>育成点</th><th>育成番付</th></tr>'+Y.slice(-20).reverse().map(x=>{const r=ikRank(x.p,h);return '<tr><td>'+x.y+'年</td><td class="num">'+(x.p[h]==null?'—':x.p[h])+'</td><td class="num">'+(r?r.rk+' 位':'—')+'</td></tr>';}).join('')+'</table></details>':'')+'</div></div></div>';}
const ikSC=sbCard;sbCard=function(){let a='';try{a=ikSC();}catch(e){}let b='';try{b=ikCard();}catch(e){try{sysLog('育成の成績',e);}catch(x){}}return a+b;};
</script>
<style id="ik123">.ikp h4{margin:10px 0 4px}.ikg{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:6px 0 10px}@media(max-width:600px){.ikg{grid-template-columns:1fr 1fr}}
.ikb{border:1px solid var(--line);border-radius:10px;padding:8px 12px}.ikb small{display:block;font-size:12px;opacity:.8}.ikb b{font-size:28px}.ikb span{font-size:12px;margin-left:4px}.ikb.hl{border:2px solid var(--ai)}
.ikc{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px}.ikc span{border:1px solid var(--line);border-radius:14px;padding:2px 10px;font-size:13px}
.ik3{display:grid;grid-template-columns:1.4fr 1fr;gap:14px}@media(max-width:700px){.ik3{grid-template-columns:1fr}}</style>
