<script>/* v200:得意を表示(親方・おかみさん・部屋付き親方・トレーナー。マネージャーは v198)。能力が 14 以上で「得意」、17 以上で「名人」。経験(年)を積むと能力が上がり、得意が増える(数字は推定) */
const TOKN={net:'顔の広さ',jim:'事務',eig:'営業',osh:'押しの指導',yot:'四つの指導',waz:'技の指導',tai:'体づくり',sei:'弟子の相談役',meki:'見る目',chk:'ちゃんこ上手',koen:'後援会のつきあい',keiri:'お金のやりくり',hito:'弟子への目配り'};
const TRTOK={gym:['筋力づくり','けがの予防','スピードづくり'],mental:['気持ちの切りかえ','場所前の集中','緊張のほぐし方'],diet:['体重の増やし方','疲れを抜く食事','減量の指導'],clinic:['ひざ・腰の手入れ','古傷のケア','はり・きゅう']};
function tokL(sk,keys){return keys.filter(k=>sk[k]!=null&&sk[k]>=14).sort((a,b)=>sk[b]-sk[a]).slice(0,3).map(k=>[TOKN[k],sk[k]>=17]);}
function tokH(L,none){if(!L.length)return none?'<div class="tokr"><span class="mute kaku" style="font-size:12px">'+none+'</span></div>':'';return '<div class="tokr">'+L.map(([t,m])=>'<span class="tokt'+(m?' tm':'')+'">'+(m?'名人 ':'得意 ')+t+'</span>').join('')+'</div>';}
function trTok(k){const y=((G.conY||{})[k]||0);const L=TRTOK[k]||[];return L.slice(0,Math.min(L.length,1+Math.floor(y/2)));}
/* 経験で伸びる:年に 1 回(初場所の前)。部屋付き親方・親方・マネージャーは、いちばん得意なものか、ほかの 1 つが +1(最大 18)。トレーナーは契約の年数を数える */
function tokYear(){const up=(sk,keys,p,who)=>{if(Math.random()>p)return;const before=tokL(sk,keys).map(x=>x.join());const top=keys.slice().sort((a,b)=>sk[b]-sk[a]);const k=Math.random()<.6?top[0]:pick(keys);if(sk[k]>=18)return;sk[k]++;const after=tokL(sk,keys);const nw=after.find(x=>!before.includes(x.join()));if(nw)addNews(who+'に、新しく「'+(nw[1]?'名人 ':'得意 ')+nw[0]+'」が付きました(経験を積んだため)。');};
 const h=me();if(h&&h.oy)up(h.oy,['osh','yot','waz','tai','sei','meki'],.5,h.n+'親方');
 (G.staff||[]).forEach(s=>{if(s.role==='co')up(s.sk,['osh','yot','waz','tai','sei','meki'],.5,s.n.replace(/^元・/,'')+'親方');if(s.role==='sc'){mgSpec(s,0);up(s.sk,['meki','net','jim','eig'],.4,'マネージャーの'+s.n);}});
 G.conY=G.conY||{};for(const k in (G.con||{}))if(G.con[k]){const b=trTok(k).length;G.conY[k]=(G.conY[k]||0)+1;const a=trTok(k);if(a.length>b)addNews(({gym:'ジムのトレーナー',mental:'メンタルトレーナー',diet:'管理栄養士',clinic:'治療院の先生'})[k]+'に、新しく「得意 '+a[a.length-1]+'」が付きました(部屋との付き合いが長くなったため)。');}}
(function(){
 const op=okamiPanel;okamiPanel=function(){let h=op();try{const o=G.okami;if(o)h=h.replace('</span></h2><div class="sks">','</span></h2>'+tokH(tokL(o.sk,['chk','koen','keiri','hito']),'まだ得意と言えるものはありません')+'<div class="sks">');}catch(e){}return h;};
 function deco(){try{
  if(UI.view==='staff'){const h2=[...document.querySelectorAll('.pn>h2')].find(x=>x.firstChild&&x.firstChild.textContent==='親方');const pn=h2&&h2.parentElement;
   if(pn&&!pn.querySelector('.tokr')){const k=pn.querySelector('.kaku');if(k)k.insertAdjacentHTML('afterend',tokH(tokL(me().oy,['osh','yot','waz','tai','sei','meki']),'まだ得意と言えるものはありません'));}
   G.staff.filter(s=>s.role==='co').forEach(s=>{document.querySelectorAll('.sr .n>span').forEach(sp=>{if(sp.textContent!==s.n)return;const n=sp.parentElement;if(n.querySelector('.tokr'))return;const L=tokL(s.sk,['osh','yot','waz','tai','sei','meki']);if(L.length)n.insertAdjacentHTML('beforeend',tokH(L));});});}
  document.querySelectorAll('button[onclick^="setCon("]').forEach(bt=>{const k=(bt.getAttribute('onclick').match(/setCon\('(\w+)'\)/)||[])[1];if(!k||!TRTOK[k]||!(G.con&&G.con[k])||bt.querySelector('.trtk'))return;bt.insertAdjacentHTML('beforeend','<span class="trtk">'+trTok(k).map(x=>'得意 '+x).join('・')+'</span>');});
 }catch(e){}}
 const R0=render;render=function(){const x=R0.apply(this,arguments);deco();return x;};
})();
</script><style>.tokr{display:flex;flex-wrap:wrap;gap:5px;margin:4px 0 2px}.tokt{display:inline-block;background:var(--kin,#c9a24a);color:#1a1611;border-radius:9px;padding:0 8px;font-size:12px;font-weight:700}.tokt.tm{background:#b5361f;color:#fff}.sr .n .tokr{margin:2px 0 0}.trtk{display:block;font-size:11px;color:var(--kin,#c9a24a);margin-top:2px;font-weight:400}</style>
