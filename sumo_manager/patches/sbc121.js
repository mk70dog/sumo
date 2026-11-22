<script>
/* v121:勝負の点は「部屋で育てた力士」だけを数えられる(G.mp.sb.c='ik')。始めたとき幕下以下だった力士と、そのあと入った力士だけ。
   始めからいる関取・横綱・大関の地位・昇進・優勝・三賞は数えない。年間評価(部屋全体)も数えない。新幕下 1 点を足す(両方の数え方)。
   選ぶ画面は見本 sbc2(タイルの下に「点の数え方」の札 2 つ)。v120 までに始めた二人相撲は c がないので今までどおり「全員」。 */
UI.mpSb=UI.mpSb||{k:1,y:10,g:'yok'};if(!UI.mpSb.c)UI.mpSb.c='ik';
const SBC_T={ik:'育てた力士だけ',all:'全員'};
const SBC_D={ik:'始めたときに幕下以下だった力士と、そのあと入った力士だけを数えます。始めからいる関取・横綱の点は入りません。大きな部屋とも対等に競えます。',all:'始めからいる関取・横綱も数えます。始めの部屋の強さの差がそのまま点に出ます。'};
function sbIkOn(sb){return !!(sb&&sb.c==='ik'&&sb.st0);}
function sbIk(sb,id){if(!sbIkOn(sb))return true;const v=sb.st0[id];return v==null||v<=1;}
sbMake=function(){if(G&&G.mp&&G.mp.role==='host'&&!G.mp.sb){const o=UI.mpSb||{k:1,y:10,g:'yok',c:'ik'};G.mp.sb={k:o.k,y:o.y,g:o.g,c:o.k===4?'all':(o.c||'ik')};}};
const sbT0=sbTitle;sbTitle=function(sb){const t=sbT0(sb);return sb&&sb.c==='ik'&&sb.k!==4?t+'(育てた力士)':t;};
const sbI0=sbInit;sbInit=function(){const m=G&&G.mp,sb=m&&m.sb;const go=sb&&m.role==='host'&&m.gh>0&&sb.b0==null;sbI0();
 if(go&&sb.b0!=null&&sb.c==='ik'){sb.st0={};Object.values(G.R).forEach(r=>{if(r&&!r.ret)sb.st0[r.id]=rankLv(r);});save();}};
sbPts=function(h){const sb=sbOf();const items=[];let p=0;const add=(t,n,v)=>{if(n){items.push([t,n,n*v]);p+=n*v;}};
 let sk=0,sy=0,oz=0,yk=0,nj=0,nm=0,nb=0,top=1;
 G.order.forEach(id=>{const r=G.R[id];if(!r||r.h!==h||r.d>2||!sbIk(sb,id))return;const rc=G.lastRec&&G.lastRec[id];if(!rc)return;
  const H=r.hist||[];const nw=H.length>=2&&H[H.length-1].b===G.bnum,pre=nw?H.slice(0,-1):null;
  if(r.d===2){if(nw&&!pre.some(x=>x.d<=2))nb++;return;}
  if(r.t==='Y')yk++;else if(r.t==='O')oz++;else if(r.t)sy++;else sk++;top=Math.max(top,rankLv(r));
  if(nw){if(r.d===1&&!pre.some(x=>x.d<=1))nj++;if(r.d===0&&!pre.some(x=>x.d===0))nm++;}});
 add('関取(平幕・十両)',sk,1);add('三役',sy,2);add('大関',oz,3);add('横綱',yk,5);
 const L=G.last||{};const yu=(L.yu||[]).filter(y=>y.h===h&&y.d<=1&&sbIk(sb,y.id));const y0=yu.filter(y=>y.d===0).length,y1=yu.filter(y=>y.d===1).length;
 add('幕内優勝',y0,10);add('十両優勝',y1,3);
 add('三賞',(L.sansho||[]).filter(x=>x.h===h&&sbIk(sb,x.id)).length,2);
 add('新幕下',nb,1);add('新十両',nj,2);add('新入幕',nm,3);
 if(!sbIkOn(sb)&&G.bnum%6===0){const yr=pv(h,'yr');const l=yr&&yr[yr.length-1];if(l&&l.y===Math.floor((G.bnum-1)/6)+1){const v={S:10,A:5,B:2}[l.g]||0;if(v){items.push(['年間評価 '+l.g,1,v]);p+=v;}}}
 const sc=(pv(h,'ev')||[]).filter(e=>e.k==='scand').length;if(sc){items.push(['不祥事',sc,-5*sc]);p-=5*sc;}
 return {p:p,items:items,sk:sk+sy+oz+yk,top:top,yu:y0,nj:nj};};
sbEval=function(){const sb=sbOf();if(!sb||sb.done||sb.b0==null||!(G.mp.gh>0))return;const gh=G.mp.gh;
 if(sb.k===1){if(sb.n>=sb.y*6){sb.res={a:sb.ta,g:sb.tg};sbDone(sb.ta>sb.tg?'a':sb.ta<sb.tg?'g':'t',sb.y+' 年('+sb.y*6+' 場所)が終わり、点数は '+sbNm(0)+' '+sb.ta+' 点・'+sbNm(gh)+' '+sb.tg+' 点でした。');}return;}
 if(sb.k!==2)return;let a,g,why;
 if(sb.g==='yok'){const f=h=>Object.values(G.R).some(r=>r.h===h&&!r.ret&&r.t==='Y'&&!(sb.y0||[]).includes(r.id)&&sbIk(sb,r.id));a=f(0);g=f(gh);why='先に横綱を出しました。';}
 else if(sb.g==='yu3'){a=sb.yu.a>=3;g=sb.yu.g>=3;why='先に幕内優勝 3 回に届きました。';}
 else{a=sb.nj.a>=5;g=sb.nj.g>=5;why='先に新十両 5 人に届きました。';}
 if(a&&g){const w=sb.g==='sk5'&&sb.nj.a!==sb.nj.g?(sb.nj.a>sb.nj.g?'a':'g'):'t';sbDone(w,'ふたりが同じ場所で目標に届きました。');}
 else if(a)sbDone('a',why);else if(g)sbDone('g',why);};
sbProg=function(h){const sb=sbOf(),k=h===0?'a':'g';
 if(sb.g==='yok'){let lv=1;Object.values(G.R).forEach(r=>{if(r.h!==h||r.ret||!sbIk(sb,r.id))return;let l=rankLv(r);if(l===6&&(sb.y0||[]).includes(r.id))l=5;lv=Math.max(lv,l);});return {v:SB_POS[lv-1],t:lv>=6?'横綱に届いた':SB_LV[lv-1]+'まで',lv:lv};}
 const n=sb.g==='yu3'?sb.yu[k]:sb.nj[k],m=sb.g==='yu3'?3:5;return {v:Math.min(100,n/m*100),t:n+' / '+m+(sb.g==='yu3'?' 回':' 人'),lv:n};};
/* 選ぶ画面:タイルの下に「点の数え方」の札 2 つ(見本 sbc2) */
const sbP121=sbPanel;sbPanel=function(){let h=sbP121();const o=UI.mpSb;if(!o.c)o.c='ik';if(o.k===4)return h;
 const card=c=>'<button class="sbcc'+(o.c===c?' on':'')+'" onclick="sbSet(\'c\',\''+c+'\')"><b>'+(o.c===c?'◉ ':'○ ')+SBC_T[c]+(c==='ik'?' <em>おすすめ</em>':'')+'</b><small>'+SBC_D[c]+'</small></button>';
 const box='<div class="sbcbox"><div class="hd3">点の数え方</div><div class="sbcg">'+card('ik')+card('all')+'</div></div>';
 const i=h.indexOf('<div class="hd"><span class="no">2</span>');return i<0?h+box:h.slice(0,i)+box+h.slice(i);};
/* 子の参加の画面・記録の欄に数え方を出す */
const sbGH121=mpGuestHTML;mpGuestHTML=function(){let o=sbGH121();const sb=sbOf();
 if(sb&&sb.c&&sb.k!==4&&MPG.gh<0&&!MPG.dk&&!UI.mpDk)o=o.replace(' 親が決めた形です。',' 点の数え方:'+SBC_T[sb.c]+'。親が決めた形です。');return o;};
const sbCd121=sbCard;sbCard=function(){const h=sbCd121();const sb=sbOf();if(!h||!sb||!sb.c||sb.k===4)return h;
 return h.replace('</h3>','</h3><p class="mute" style="margin:-4px 0 8px">点の数え方:'+esc(SBC_T[sb.c])+(sb.c==='ik'?'(始めたときに幕下以下だった力士と、そのあと入った力士だけ)':'')+'</p>');};
</script>
<style id="sbc121">.sbcbox{margin:4px 0 10px}.sbcbox .hd3{font:bold 16px sans-serif;color:#ffe9a8;margin:2px 0 6px}
.sbcg{display:grid;grid-template-columns:1fr 1fr;gap:10px}@media(max-width:700px){.sbcg{grid-template-columns:1fr}}
.sbcc{display:block!important;width:100%!important;text-align:left!important;background:#2a2116!important;border:2px solid #6b5630!important;border-radius:10px!important;color:#e9dcc0!important;padding:10px 12px!important;font-family:sans-serif!important;cursor:pointer;margin:0!important}
.sbcc b{display:block;font-size:17px}.sbcc em{font-style:normal;font-size:11px;background:#7a1d10;color:#fff;padding:1px 8px;border-radius:9px;margin-left:4px;vertical-align:middle}.sbcc small{display:block;font-size:12px;opacity:.85;margin-top:4px;line-height:1.5}
.sbcc.on{background:#f3e7c9!important;border-color:#c9a24a!important;color:#1a140c!important}</style>
