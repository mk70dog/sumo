/* v213 土俵の物語(ダルマさん「スポーツは物語。記録より記憶」)。
   実在の力士の実際の出来事(出典つき、data/story2026.txt)を力士の画面に年表で出し、
   ゲームの中で起きたことも物語として書き足していく。人気の上がり幅はすべて推定(ふつうの優勝・三賞の人気の上がり方に上乗せする分)。 */
(function(){
const SD=window.STORYD||{};
function kinds(r){const D=SD[r.n];return (D&&r.real)?D.kind:{};}
function sx(r,t){r.stoX=r.stoX||[];r.stoX.push({b:G.bnum,t:t});if(r.stoX.length>40)r.stoX.shift();}
function pp(r,v){r.pop=cl((r.pop||20)+v,0,100);}
window.storySx=sx;
function storyHTML(r){const D=r.real?SD[r.n]:null;const X=r.stoX||[];if(!D&&!X.length)return '';
 const rows=(D?D.ev.map(e=>[e[0],e[1],e[2],1]):[]).concat(X.map(x=>[bname(x.b),x.t,'',0]));
 return '<div class="sty"><h3>土俵の物語</h3>'+(D&&D.sum?'<p class="stys">'+esc(D.sum)+'</p>':'')+
  '<ol class="styl">'+rows.map(e=>'<li class="'+(e[3]?'re':'ge')+'"><b>'+esc(e[0])+'</b><span>'+esc(e[1])+(e[2]?'<small>'+esc(e[2])+'</small>':'')+'</span></li>').join('')+'</ol>'+
  (D?'<p class="styn">白い行は実際の出来事(出典つき)。金色の行は、このゲームの中で起きたことです。</p>':'')+'</div>';}
window.storyHTML=storyHTML;
const st0=stHTML;stHTML=function(r){let a='';try{a=storyHTML(r);}catch(e){console.error(e);}return a+st0(r);};
/* 場所中:悲願の力士が終盤まで優勝争いに残ると、館内がわく */
const ad0=advanceDay;advanceDay=function(){const res=ad0.apply(this,arguments);try{const B=G.B;if(B&&B.day>=13&&B.day<15){
  const ids=divIds(0);let mx=0;ids.forEach(id=>{mx=Math.max(mx,B.rec[id].w);});
  ids.forEach(id=>{const r=G.R[id];const K=kinds(r);const rc=B.rec[id];if(!K.higan||(r.hg&&r.hg.done)||rc.ky||B['_hg'+id])return;
   if(rc.w>=mx-1){B['_hg'+id]=1;addNews('館内に「'+r.n+'コール」。'+B.day+'日目を終えて '+rc.w+' 勝、悲願の賜杯へ優勝争いに残っています。');}});}}catch(e){console.error(e);}return res;};
/* 場所のあと */
const eb0=endBasho;endBasho=function(){const B=G.B;const rk=!!G._rkYu;const r0=eb0.apply(this,arguments);try{if(!rk)storyBasho(B);}catch(e){console.error(e);}return r0;};
function storyBasho(B){if(!B)return;const S=G.last||{sansho:[],kin:[]};
 Object.values(G.R).forEach(r=>{if(!r||r.ret||!r.real||!SD[r.n])return;const rc=B.rec[r.id];if(!rc)return;const K=kinds(r);const kk=rc.w>rc.l+rc.ab;
  if(K.higan&&r.d===0){r.hg=r.hg||{j:K.higan[0],k:K.higan[1],done:0};const H=r.hg;
   if(!H.done){
    if(rc.yu){H.done=1;pp(r,6);sx(r,'悲願の幕内初優勝。優勝次点 '+H.j+' 回、決定戦 '+H.k+' 度の涙を越えて');addNews('🏆 '+r.n+'、悲願の初優勝!優勝次点 '+H.j+' 回を越えての賜杯に、館内は総立ちになりました。');}
    else if(rc.jn===1){H.k++;H.j++;pp(r,2);sx(r,'優勝決定戦で敗れる(決定戦はこれで '+H.k+' 戦全敗、優勝次点 '+H.j+' 回)');addNews(r.n+'、またも決定戦で涙。優勝次点は '+H.j+' 回に。それでも館内からは温かい拍手が送られました。');}
    else if(rc.jn===2){H.j++;pp(r,1);sx(r,'優勝次点('+H.j+' 回目)。あと一歩、賜杯に届かず');}}}
  if(K.fukkatsu&&r.d<=1){
   if(rc.yu&&r.d===1){pp(r,3);sx(r,'十両優勝。どん底からの歩みが、また一つ実を結ぶ');addNews(r.n+'が十両優勝。序ノ口からはい上がった男に、大きな拍手が送られました。');}
   else if(kk&&!r.fkK){r.fkK=1;pp(r,2);sx(r,'関取に戻って初めての勝ち越し');}}
  if(K.kettou){const kin=(S.kin||[]).filter(k=>k[0]===r.id).length,sh=(S.sansho||[]).filter(x=>x.id===r.id).length;
   if(rc.yu&&r.d===0){pp(r,5);sx(r,'幕内優勝。祖父・'+K.kettou[0]+'と同じ賜杯を抱く');addNews('🏆 「'+K.kettou[0]+'の孫」'+r.n+'が幕内優勝。祖父と同じ賜杯を抱きました。');}
   else if(kin){pp(r,3);sx(r,'金星。「'+K.kettou[0]+'の孫」が横綱を倒す');}
   else if(sh){pp(r,2);sx(r,'三賞を受ける');}}});}
/* 番付発表:再入幕・大関昇進 */
const nc0=nextCycle;nextCycle=function(){const old={};try{Object.values(G.R).forEach(r=>{if(r&&r.real&&SD[r.n])old[r.id]=[r.d,r.t];});}catch(e){}
 const res=nc0.apply(this,arguments);
 try{if(res!==false)Object.keys(old).forEach(id=>{const r=G.R[id];if(!r||r.ret)return;const o=old[id];const K=kinds(r);
  if(K.fukkatsu&&r.d===0&&o[0]>0){pp(r,5);sx(r,'再入幕。序ノ口からはい上がり、ふたたび幕内へ');addNews(r.n+'が再入幕。脊髄の大けがで序ノ口まで落ちた男が、幕内に帰ってきました。');}
  if(K.kettou&&r.t==='O'&&o[1]!=='O'&&o[1]!=='Y'){pp(r,4);sx(r,'大関に昇進。祖父・'+K.kettou[0]+'の背中にまた近づく');}
  if(K.higan&&r.d===0&&o[0]===0&&r.retW){}});}catch(e){console.error(e);}
 return res;};
document.head.insertAdjacentHTML('beforeend','<style>.sty{margin:10px 0;padding:10px 12px;border-left:4px solid #c9a24a;border-radius:6px;background:rgba(201,162,74,.08)}.sty h3{margin:0 0 4px}.stys{margin:2px 0 8px;font-size:15px;line-height:1.7}.styl{list-style:none;margin:0;padding:0}.styl li{display:grid;grid-template-columns:7.5em 1fr;gap:8px;padding:4px 0;border-top:1px dashed rgba(128,128,128,.3);font-size:14px;line-height:1.5}.styl li b{font-weight:600;opacity:.8}.styl li small{display:block;font-size:11px;opacity:.6}.styl li.ge b,.styl li.ge span{color:#c9a24a}.styn{font-size:11px;opacity:.65;margin:6px 0 0}</style>');
})();
