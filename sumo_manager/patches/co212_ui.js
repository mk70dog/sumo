/* v209 部屋付き親方を一人の人物に:出身地・出身校・性格、つながりで新弟子探し、自分から動く、弟子への助言、弟子とのつながり。数字はすべて推定。
   実在の親方の出身地は TOSHI(協会の年寄の表)、出身校は日本語版ウィキペディアで確かめた分だけ COSCH に入れる(本名は入れない) */
(function(){
/* 出身校(高校, 大学)。'中学卒' は中学卒業で入門。'' は調べがついていない */
const COSCH={朝乃若:['愛工大名電','近畿大学'],五城楼:['東北(中退)',''],起利錦:['中学卒',''],大碇:['京都学園','同志社大学'],琴稲妻:['中学卒',''],普天王:['文徳','日本大学'],
 旭里:['中学卒',''],高見盛:['弘前実業','日本大学'],石浦:['','日本大学'],旭富士:['五所川原商業','近畿大学(中退)'],武雄山:['愛工大名電','明治大学'],智乃花:['','日本大学'],
 出島:['金沢市立工業','中央大学'],土佐ノ海:['高知','同志社大学'],敷島:['船橋古和釜',''],誉富士:['五所川原農林','近畿大学'],栃煌山:['明徳義塾',''],宝富士:['','近畿大学']};
const CHARA={mendo:['面倒見がいい','弟子とのつながりが早く深まる。声をかけることが多い'],shoku:['職人肌','助言がよく効く。人づきあいは少なめ'],kao:['顔が広い','新弟子の情報や母校とのつきあいが多い'],nek:['熱血','やる気を上げるのがうまい。助言も多い']};
const STY={osh:'押し',yot:'四つ',waz:'技'};
const ADV={osh:[['tsk','「押す手は脇を締めろ。はず押しで起こせ」'],['tac','「立ち合いは頭から当たれ。腰を引くな」']],
 yot:[['yor','「まわしを取ったら頭をつけて、すぐ寄れ」'],['mig','「右を差したら、もう離すな」'],['hid','「左のおっつけで相手の右を殺せ」']],
 waz:[['nag','「投げは崩してから打て。焦るな」'],['ash','「足の運びが雑だ。すり足をもう一度」'],['tgw','「土俵際こそ、最後まで足を残せ」']],
 tai:[['str','「四股の数をもっと増やせ」'],['end','「最後の一番で息が上がっている。もう一番取れ」']],
 sei:[['rei','「負けた相撲こそ、よく思い出せ」'],['tos','「気持ちで負けるな。土俵に上がったら迷うな」']]};
const pref=x=>String(x||'').replace(/(県|府|都)$/,'');
const schKey=x=>{if(!x)return null;const n=String(x).replace(/\(.*\)/,'');return (typeof schOf==='function'&&schOf(n))?n:null;};
const isCo=s=>s&&s.role==='co';
const cnm=s=>String(s.n||'').replace(/^元・/,'').replace(/^先代\(|\)$/g,'');
/* 人物の情報をそろえる */
function coEnsure(s){if(!isCo(s)||s.prof)return s;const nm=cnm(s);const P={};
 const T=(typeof TOSHI!=='undefined')?TOSHI.find(t=>t[4]===nm):null;
 const own=Object.values(G.R||{}).find(r=>r.n===nm&&r.h===ME());
 if(T){P.hm=pref(T[8]);P.src='実在';}else if(own){P.hm=own.fr?own.home:pref(own.home);P.hs=own.hs||'';P.uni=own.uni||'';P.src='部屋育ち';}
 else{P.hm=pick(REG[RI(0,5)].p);P.src='架空';}
 if(COSCH[nm]){P.hs=COSCH[nm][0];P.uni=COSCH[nm][1];}
 else if(P.src==='架空'){const H=SCH.filter(x=>x[1]==='高'),U=SCH.filter(x=>x[1]==='大');P.hs=Math.random()<.55?pick(H)[0]:'中学卒';P.uni=P.hs!=='中学卒'&&Math.random()<.4?pick(U)[0]:'';}
 const k=['osh','yot','waz'].sort((a,b)=>(s.sk[b]||0)-(s.sk[a]||0))[0];P.sty=STY[k];P.k=k;
 P.ch=pick(Object.keys(CHARA));s.prof=P;if(s.auto==null)s.auto=1;
 [P.hs,P.uni].forEach(n=>{const kk=schKey(n);if(kk){G.rel=G.rel||{};G.rel[kk]=Math.max(G.rel[kk]||0,20);}});
 return s;}
const cos=()=>(G.staff||[]).filter(isCo).map(coEnsure);
const away=s=>typeof kenAway==='function'&&kenAway('s'+s.sid);
/* つながり */
function bd(sid,rid){return ((G.cobd||{})[sid]||{})[rid]||0;}
function bdAdd(sid,rid,v){G.cobd=G.cobd||{};const m=G.cobd[sid]=G.cobd[sid]||{};m[rid]=Math.max(0,Math.min(100,(m[rid]||0)+v));}
const BDL=v=>v>=70?'師弟の絆':v>=45?'信頼':v>=20?'目をかけている':'まだ浅い';
function match(s,r){const P=s.prof;let m=[];if(P.hm&&pref(r.home)===P.hm)m.push('同郷');
 const sc=[P.hs,P.uni].map(x=>String(x||'').replace(/\(.*\)/,'')).filter(x=>x&&x!=='中学卒');if(sc.some(x=>x===r.hs||x===r.uni))m.push('同じ学校');
 try{const st=styleName(r);if(st&&st.indexOf(P.sty.charAt(0))>=0)m.push('同じ取り口');}catch(e){}return m;}
function bestBd(r){let b=0,s0=null;cos().forEach(s=>{const v=bd(s.sid,r.id);if(v>b){b=v;s0=s;}});return [b,s0];}
/* 毎週:つながりが深まる・自分から動く・情報が入る */
function coLife(){const L=cos();if(!L.length)return;const o=ownAll();const spring=((G.bnum-1)%6===1)?1.4:1;
 L.forEach(s=>{if(away(s))return;const P=s.prof,a=coA(s);const f=P.ch==='mendo'?1.3:P.ch==='shoku'?.85:1;
  o.forEach(r=>{let v=.08;if(a.t==='one'&&a.r===r.id)v+=1.2;const m=match(s,r);v+=m.length*.25;bdAdd(s.sid,r.id,v*f);
   if(bd(s.sid,r.id)>=45&&Math.random()<.3)r.tr=Math.min(100,(r.tr==null?50:r.tr)+.15);
   const lv=rankLv(r);if(r._cbl!=null&&lv>r._cbl&&lv>=2&&bd(s.sid,r.id)>=45){addNews(r.n+'の昇進に、元・'+cnm(s)+'親方も「よくやった」と目を細めていました。');bdAdd(s.sid,r.id,5);}});
  /* 自分から動く(週に 3 割ほど) */
  if(s.auto!==0&&Math.random()<(P.ch==='nek'||P.ch==='mendo'?.22:.17)){
   const W=P.ch==='kao'?[['koe',2],['adv',2],['sch',3],['pro',3]]:P.ch==='shoku'?[['koe',1],['adv',5],['sch',1],['pro',1]]:P.ch==='mendo'?[['koe',4],['adv',3],['sch',1],['pro',1]]:[['koe',3],['adv',4],['sch',1],['pro',1]];
   const act=wpick(W);
   if(act==='koe'&&o.length){const r=o.slice().sort((x,y)=>(x.mor||50)-(y.mor||50))[0];r.mor=Math.min(100,(r.mor||50)+(P.ch==='nek'?5:3));bdAdd(s.sid,r.id,3);
    addNews('元・'+cnm(s)+'親方が、元気のない'+r.n+'に声をかけていました。');}
   else if(act==='adv'&&o.length){coAdvise(s,null);}
   else if(act==='sch'){const sc=[P.hs,P.uni].map(schKey).filter(Boolean);if(sc.length){const k=pick(sc);G.rel[k]=Math.min(100,(G.rel[k]||0)+3);addNews('元・'+cnm(s)+'親方が母校の'+schLabel(k)+'相撲部に顔を出しました(関係 +3)。');}else coAdvise(s,null);}
   else if(act==='pro'){const c=(G.pros||[]).filter(p=>p.r&&(pref(p.r.home)===P.hm||(p.sch&&[P.hs,P.uni].some(x=>String(x||'').replace(/\(.*\)/,'')===p.sch))));
    if(c.length){const p=pick(c);viewPros(p,s.sk.meki||10);p.int=Math.max(0,p.int-2);p.coSame=1;addNews('元・'+cnm(s)+'親方が、'+(pref(p.r.home)===P.hm?'同郷の':'後輩にあたる')+'新弟子候補の'+p.n+'を見に行きました(見立てが正確に)。');}else coAdvise(s,null);}}
  /* つながりから新弟子の情報 */
  if((G.pros||[]).length<18&&Math.random()<(P.ch==='kao'?.02:.01)*spring){const sc=[P.hs,P.uni].map(schKey).filter(Boolean);let p=null,src='';
   if(sc.length&&G.ama&&Math.random()<.6){const k=pick(sc);const c=G.ama.filter(x=>x.sch===k&&((x.kind==='高'&&x.yr>=3)||(x.kind==='大'&&x.yr>=4))&&!G.pros.some(q=>q.amaId===x.id));
    if(c.length){const a=pick(c);p=prosFromAma(a,'');p.amaId=a.id;src='元・'+cnm(s)+'親方の母校('+schLabel(k)+')の監督から紹介';}}
   if(!p&&P.hm&&REG.slice(0,6).some(g=>g.p.includes(P.hm))){p=mkProspect(prefReg(P.hm));p.r.home=P.hm;src='元・'+cnm(s)+'親方の地元('+P.hm+')のつながり';}
   if(p){p.src=src;p.coSame=1;viewPros(p,s.sk.meki||10);G.pros.push(p);addNews(src+'で、新弟子候補の情報が入りました('+p.n+')。');}}});
 o.forEach(r=>{r._cbl=rankLv(r);});}
/* 助言 */
function coAdvise(s,rid){const o=ownAll();if(!o.length)return;coEnsure(s);const P=s.prof;
 let r=rid!=null?G.R[rid]:null;if(!r){const sc=o.map(x=>[x,bd(s.sid,x.id)+match(s,x).length*15+Math.random()*20]).sort((a,b)=>b[1]-a[1]);r=sc[0][0];}
 const sk=Object.keys(ADV).filter(k=>s.sk[k]!=null).sort((a,b)=>s.sk[b]-s.sk[a]);const k=Math.random()<.65?sk[0]:pick(sk);const A=pick(ADV[k]);
 const b=bd(s.sid,r.id);const g=.35*(1+b/100)*(P.ch==='shoku'?1.3:1)*(.6+(s.sk[k]||10)/25);grow(r,A[0],g);r.mor=Math.min(100,(r.mor||50)+1);
 r.coAdv=r.coAdv||[];r.coAdv.unshift({b:G.bnum,w:G.wk,n:cnm(s),t:A[1],k:A[0]});if(r.coAdv.length>8)r.coAdv.length=8;bdAdd(s.sid,r.id,4);
 addNews('元・'+cnm(s)+'親方が'+r.n+'に'+A[1]+'と助言しました。');}
window.coAdviseNow=function(sid,rid){const s=G.staff.find(x=>x.sid===sid);if(!s)return;if(away(s))return alertM('助言','いまは研修中です。');
 if(G.coAdvW&&G.coAdvW[sid]===G.wn)return alertM('助言','この親方は今週もう助言しました。');G.coAdvW=G.coAdvW||{};G.coAdvW[sid]=G.wn;coAdvise(s,rid==null?null:+rid);save();render();
 const r=rid!=null?G.R[+rid]:null;const x=(r||ownAll().find(q=>q.coAdv&&q.coAdv[0]&&q.coAdv[0].b===G.bnum&&q.coAdv[0].w===G.wk&&q.coAdv[0].n===cnm(s)));
 if(x&&x.coAdv&&x.coAdv[0])alertM('助言','元・'+cnm(s)+'親方が'+x.n+'に'+x.coAdv[0].t+'と助言しました。');};
window.coAutoSet=function(sid,v){const s=G.staff.find(x=>x.sid===sid);if(s){s.auto=v?1:0;save();render();}};
/* 伸び・勧誘への効き目 */
const cm0=coMul;coMul=function(r){let m=cm0(r);if(r&&r.h===ME())m*=1+bestBd(r)[0]/2500;return m;};
const ob0=offerBonus;offerBonus=function(p){let b=ob0(p);const L=cos();if(p.sch&&L.some(s=>[s.prof.hs,s.prof.uni].some(x=>String(x||'').replace(/\(.*\)/,'')===p.sch)))b+=.05;
 if(p.r&&L.some(s=>s.prof.hm===pref(p.r.home)))b+=.03;if(p.coSame)b+=.02;return b;};
const dw0=doWeek;doWeek=function(){const ph=G&&G.phase;const r=dw0.apply(this,arguments);try{if(ph==='train')coLife();}catch(e){console.error(e);}return r;};
/* スタッフ画面:人物とつながり */
const sh0=staffHTML;staffHTML=function(){const L=cos();let h=sh0();if(!L.length)return h;const o=ownAll();
 const rows=L.map(s=>{const P=s.prof;const top=o.map(r=>[r,bd(s.sid,r.id)]).filter(x=>x[1]>=5).sort((a,b)=>b[1]-a[1]).slice(0,3);
  const sch=[P.hs,P.uni].filter(Boolean).map(x=>x==='中学卒'?'中学卒業で入門':(schKey(x)?schLabel(schKey(x)):(/大学/.test(x)?x:x+'高校'))).join('・')||'<span class="mute">(調べがついていない)</span>';
  return '<div class="cop"><div class="coh"><b>元・'+esc(cnm(s))+'親方</b><span class="mute">'+esc(s.mo||'')+'・'+Math.floor(s.age||0)+'歳</span>'+(away(s)?'<span class="tokt">研修中</span>':'')+
   '<label class="coa"><input type="checkbox" '+(s.auto!==0?'checked':'')+' onchange="coAutoSet('+s.sid+',this.checked)"> 自分から動く</label></div>'+
   '<div class="cog"><span>出身</span><b>'+esc(P.hm||'?')+'</b><span>出身校</span><b>'+sch+'</b><span>取り口</span><b>'+esc(P.sty)+'</b><span>性格</span><b>'+CHARA[P.ch][0]+'</b></div>'+
   '<div class="mute" style="font-size:12px">'+CHARA[P.ch][1]+'</div>'+
   '<div class="cob"><span class="mute">つながりの深い弟子:</span> '+(top.length?top.map(x=>esc(x[0].n)+'<span class="cbl">'+BDL(x[1])+'</span>').join(' '):'<span class="mute">まだいません</span>')+'</div>'+
   '<div class="btns" style="margin-top:4px"><select id="coadv_'+s.sid+'"><option value="">おまかせで選ぶ</option>'+o.map(r=>'<option value="'+r.id+'">'+esc(r.n)+'('+esc(r.rkS||'')+')</option>').join('')+'</select><button class="btn sm" onclick="coAdviseNow('+s.sid+',document.getElementById(\'coadv_'+s.sid+'\').value||null)">助言させる(週 1 回)</button></div></div>';}).join('');
 return h+'<div class="pn"><h2>部屋付き親方の人物と弟子とのつながり<span class="sub">数字は推定</span></h2><div class="hl" style="font-size:13px">・母校や地元とのつながりから新弟子の情報が入り、母校の後輩・同郷の候補は勧誘が少し決まりやすくなります。<br>・「自分から動く」にすると、週に 1 回くらい、声かけ・助言・母校への顔出し・候補の下見を自分でします(費用はかかりません)。<br>・つながりが深いほど助言がよく効き、伸びが少し良くなり、弟子の信頼も上がります。</div><div class="cops">'+rows+'</div></div>';};
/* 力士の詳細:親方とのつながりと助言 */
const sr0=showR;showR=function(id){sr0(id);try{const r=G.R[id];if(!r||r.h!==ME())return;const L=cos();if(!L.length)return;const box=document.getElementById('mbox');if(!box)return;
 const li=L.map(s=>{const v=bd(s.sid,r.id),m=match(s,r);return '<div>元・'+esc(cnm(s))+'親方:<b>'+BDL(v)+'</b> <span class="gg"><i style="width:'+Math.round(v)+'%"></i></span>'+(m.length?' <span class="mute">'+m.join('・')+'</span>':'')+'</div>';}).join('');
 const ad=(r.coAdv||[]).slice(0,4).map(a=>'<div class="mute" style="font-size:13px">'+esc(bname(a.b).replace(/^\d+年 /,''))+(a.w?' 第'+a.w+'週':'')+' 元・'+esc(a.n)+'親方 '+esc(a.t)+'</div>').join('');
 box.insertAdjacentHTML('beforeend','<div class="pn" style="margin-top:8px"><h2>部屋付き親方とのつながり</h2>'+li+(ad?'<h3 class="kin" style="margin-top:6px">最近の助言</h3>'+ad:'')+'</div>');}catch(e){}};
window.coEnsure=coEnsure;window.coBd=bd;window.coLife=coLife;
document.head.insertAdjacentHTML('beforeend','<style>.cops{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:8px}.cop{border:1px solid rgba(120,80,40,.35);border-radius:8px;padding:8px;background:rgba(255,255,255,.04)}'+
 '.coh{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}.coh b{font-size:16px}.coa{margin-left:auto;font-size:13px;white-space:nowrap}.cog{display:grid;grid-template-columns:4em 1fr;gap:2px 8px;font-size:14px;margin:4px 0}.cog span{opacity:.65;font-size:12px}'+
 '.cob{font-size:13px;margin-top:4px}.cbl{display:inline-block;font-size:11px;border:1px solid currentColor;border-radius:8px;padding:0 5px;margin:0 6px 0 3px;opacity:.85}.cop select{max-width:14em}@media (max-width:760px){.cops{grid-template-columns:1fr}}</style>');
})();
