<script>/* v202:研修を「短い 1 週/長い 3 週」から選ぶ。研修中は部屋にいないので、その人の仕事の効き目が下がる。1 年以内に続けて出すと効きにくい。v201:力士のほかの人も育つ(ダルマさん「力士だけではなく他の関わる人も成長し育てる要素を追加」→案 1〜5「全て実施」)。数字はすべて推定。
 1 部屋付き親方:担当した弟子が勝ち越す・番付が上がると、その型に合う指導の経験がたまり、10 で能力 +1。
 2 研修:親方・部屋付き親方・マネージャー・おかみさんを研修に出す(場所ごとに 1 人 1 回)。部屋付き親方の経験は 1 場所に最大 1.5(付きっきりは 3)、12 で +1。おかみさんの経験は 1 場所に最大 1、10 で +1。次の場所の終わりに選んだ能力 +1(最大 18)。
 3 おかみさん:悩みごとに関わるたびに経験(1 場所に 1 まで)。10 で能力 +1。
 4 ちゃんこ長:2 年(12 場所)務めると、いちばん多く作った鍋が「得意な鍋」に。その鍋のときは栄養 +1。
 5 付け人:関取に付いた週が 24 週たまるごとに、本人の伸び +1%(最大 +5%)。
 (6 部屋育ちの親方:自分の部屋の弟子が部屋付き親方になると、現役時代の型に合う指導 +2。本体を書きかえ) */
const KENC={oy:20,co:20,sc:10,ok:15};
const KENL={s:{n:'短い研修',w:1,c:.5,p:.6},l:{n:'長い研修',w:3,c:1.5,p:1}};
const KENOFF={oy:'稽古の効き目が少し下がる(全員 −5%)',co:'担当の指導が止まる',sc:'新弟子探し・事務・営業が止まる',ok:'部屋の雰囲気が少し下がる'};
function kenAway(id){const x=(G.ken||{})[id];return !!(x&&x.w>0);}
const KENK={oy:['osh','yot','waz','tai','sei','meki'],co:['osh','yot','waz','tai','sei','meki'],sc:['meki','net','jim','eig'],ok:['chk','koen','keiri','hito']};
const KENN=Object.assign({},typeof SKN!=='undefined'?SKN:{},{chk:'ちゃんこ・生活',koen:'後援・挨拶',keiri:'経理',hito:'人柄・目配り'});
const KENW={oy:'協会の指導者講習',co:'ほかの部屋への見学・指導者講習',sc:'経理・営業の勉強会',ok:'おかみさんの会の勉強会'};
function kenWho(){const L=[];const h=me();if(h&&h.oy)L.push({id:'oy',t:'oy',n:h.n+'親方(師匠)',sk:h.oy});
 (G.staff||[]).forEach(s=>{if(s.role==='co'||s.role==='sc')L.push({id:'s'+s.sid,t:s.role,n:s.role==='co'?s.n.replace(/^元・/,'')+'親方':s.n+'(マネージャー)',sk:s.sk,s:s});});
 if(G.okami)L.push({id:'ok',t:'ok',n:G.okami.n+'(おかみさん)',sk:G.okami.sk});return L;}
function kenGo(id,k,L){L=KENL[L]?L:'s';const P=kenWho().find(x=>x.id===id);if(!P)return;G.ken=G.ken||{};if(G.ken[id])return alertM('研修','いまは研修中です。');
 const c=Math.round(KENC[P.t]*KENL[L].c);if(G.money<c)return alertM('研修','資金が足りません。');G.money-=c;G.ken[id]={k:k,b:G.bnum,L:L,w:KENL[L].w};addNews(P.n+'を'+KENW[P.t]+'('+KENL[L].n+'・'+KENL[L].w+' 週)に出しました('+KENN[k]+'。費用 '+man(c)+')。');save();render();}
function kenDone(id,x){const P=kenWho().find(p=>p.id===id);G.kenLast=G.kenLast||{};const rec=G.kenLast[id]!=null&&G.bnum-G.kenLast[id]<6;G.kenLast[id]=G.bnum;if(!P||P.sk[x.k]==null)return;
 let p=(KENL[x.L]||KENL.s).p*(rec?.5:1),up=0;if(Math.random()<p)up=1;if(x.L==='l'&&up&&Math.random()<(rec?.1:.25))up=2;up=Math.min(up,18-P.sk[x.k]);
 if(up>0){P.sk[x.k]+=up;addNews(P.n+'が研修から戻りました。'+KENN[x.k]+'が '+P.sk[x.k]+' に上がりました'+(up>1?'(+2)':'')+'。');}else addNews(P.n+'が研修から戻りました。今回は目に見える成果は出ませんでした'+(rec?'(前の研修から 1 年たっていないため、身に付きにくかった)':'')+'。');}
function kenWeek(){if(!G.ken)return;for(const id in G.ken){const x=G.ken[id];if(x.w==null){continue;}x.w--;if(x.w<=0){delete G.ken[id];kenDone(id,x);}}}
function kenBasho(){if(!G.ken)return;for(const id in G.ken){const x=G.ken[id];if(x.w==null){delete G.ken[id];kenDone(id,{k:x.k,L:'l'});}}}
/* 1:部屋付き親方の経験 */
const TKSK={O:'osh',X:'osh',R:'yot',L:'yot',W:'waz'};
function coXp(sum){(G.staff||[]).forEach(s=>{if(s.role!=='co')return;const a=(typeof coA==='function')?coA(s):{t:'all'};
 let L=own().filter(r=>!r.ret);if(a.t==='one')L=L.filter(r=>r.id===a.r);else if(a.t==='seki')L=L.filter(r=>r.d<=1);else if(a.t==='waka')L=L.filter(r=>r.d>=2);
 s.xp=s.xp||{};let got=0;const cap=a.t==='one'?3:1.5;L.forEach(r=>{if(got>=cap)return;const h=r.hist&&r.hist[r.hist.length-1];if(!h)return;const kk=h.w>h.l+(h.ab||0);if(!kk)return;let k=a.t==='sk'&&a.s?({osh:'osh',yot:'yot',waz:'waz',tai:'tai'}[a.s]||'tai'):(TKSK[(typeof tkOf==='function'?tkOf(r).p:'')]||'tai');
  const v=Math.min(cap-got,(a.t==='one'?3:a.t==='all'?.4:.8)+(h.yu?2:0));got+=v;s.xp[k]=(s.xp[k]||0)+v;if(s.xp[k]>=12&&s.sk[k]<18){s.xp[k]-=12;s.sk[k]++;addNews(s.n.replace(/^元・/,'')+'親方は弟子を指導した経験で、'+SKN[k]+'が '+s.sk[k]+' に上がりました。');}});});}
/* 3:おかみさんの経験 */
const OKEV={ijime:'hito',scand:'hito',retire:'hito',homesick:'hito',quit:'hito',sp:'koen',spons:'koen',tani:'koen',party:'koen',money:'keiri',debt:'keiri',loan:'keiri'};
function okXp(k){const o=G.okami;if(!o)return;if(o.xpB!==G.bnum){o.xpB=G.bnum;o.xpN=0;}if(o.xpN>=1)return;o.xpN++;const s=OKEV[k]||(/kin|money|fin/.test(k)?'keiri':/sup|koen|tani/.test(k)?'koen':/meal|chanko|food/.test(k)?'chk':'hito');o.xp=o.xp||{};o.xp[s]=(o.xp[s]||0)+1;if(o.xp[s]>=10&&o.sk[s]<18){o.xp[s]=0;o.sk[s]++;addNews('おかみさんの'+o.n+'は経験を重ねて、'+KENN[s]+'が '+o.sk[s]+' に上がりました。');}}
/* 4:ちゃんこ長の得意な鍋 */
function chkWeek(){if(G.chk==null||!G.R[G.chk]||G.R[G.chk].ret||G.R[G.chk].h!==ME()){const c=own().filter(r=>r.d>=2).sort((a,b)=>b.age-a.age);if(c.length){G.chk=c[0].id;c[0].chkB=G.bnum;}}const r=G.chk!=null?G.R[G.chk]:null;if(!r||r.ret||r.h!==ME())return;r.nabe=r.nabe||{};const k=(G.meal||{}).k;if(k)r.nabe[k]=(r.nabe[k]||0)+1;
 if(!r.nabeT&&G.bnum-(r.chkB||G.bnum)>=12){const t=Object.keys(r.nabe).sort((a,b)=>r.nabe[b]-r.nabe[a])[0];if(t){r.nabeT=t;addNews('ちゃんこ長の'+r.n+'は、'+t+'鍋が得意になりました。'+t+'の日は栄養が少し良くなります。');}}}
/* 5:付け人の学び */
function tkWeek2(){if(typeof tkAssign!=='function')return;let T;try{T=tkAssign();}catch(e){return;}own().forEach(r=>{const o=T.of[r.id];if(o==null)return;r.tkW=(r.tkW||0)+1;if(r.tkW%24===0&&(r.tkL||0)<.05){r.tkL=Math.round(((r.tkL||0)+.01)*100)/100;const s=G.R[o];if(Math.random()<.5)addNews(r.n+'は付け人として'+(s?s.n+'関':'関取')+'のそばで学び、稽古の伸びが少し良くなりました。');}});}
(function(){
 const dw=doWeek;doWeek=function(){const x=dw.apply(this,arguments);try{if(G.phase==='train'||G.wk){chkWeek();tkWeek2();kenWeek();}}catch(e){}return x;};
 const v7=v7Basho;v7Basho=function(sum){const x=v7.apply(this,arguments);try{forP(()=>{coXp(sum);kenBasho();});}catch(e){}return x;};
 const re=resolveEv;resolveEv=function(id,i){const e=G.ev.find(x=>x.id===id);const k=e&&e.k;const x=re.apply(this,arguments);try{if(k)okXp(k);}catch(e){}return x;};
 const ce=chkEiy;chkEiy=function(){const v=ce.apply(this,arguments);try{const r=G.chk!=null?G.R[G.chk]:null;if(r&&r.nabeT&&G.meal&&G.meal.k===r.nabeT)return v+1;}catch(e){}return v;};
 const cm=coMul;coMul=function(r){let m=cm.apply(this,arguments);if(r&&r.h===ME()){m*=(1+(r.tkL||0));try{if(kenAway('oy'))m*=.95;(G.staff||[]).forEach(s=>{if(s.role!=='co'||!kenAway('s'+s.sid))return;const a=coA(s);if(a.t==='seki'&&r.d<=1)m/=1.06;else if(a.t==='waka'&&r.d>=2)m/=1.05;else if(a.t==='one'&&a.r===r.id)m/=1.12;else if(a.t==='all')m*=.98;});}catch(e){}}return m;};
 const at=atmo;atmo=function(){const v=at.apply(this,arguments);return kenAway('ok')?v-6:v;};
 if(typeof mgEff==='function'){const me0=mgEff;mgEff=function(){const E=me0.apply(this,arguments);try{const M=E.M.filter(s=>!kenAway('s'+s.sid));if(M.length!==E.M.length)return {jim:M.reduce((t,s)=>t+Math.max(0,s.sk.jim-6),0),eig:M.reduce((t,s)=>t+(s.sk.eig-8),0),M:M};}catch(e){}return E;};}
 const st=staffHTML;staffHTML=function(){let h=st();try{const W=kenWho();G.ken=G.ken||{};
  h+='<div class="pn"><h2>研修に出す<span class="sub">短い研修 1 週・長い研修 3 週。研修中は部屋にいません</span></h2><table class="tb ken">'+W.map(P=>{const on=G.ken[P.id];const rec=G.kenLast&&G.kenLast[P.id]!=null&&G.bnum-G.kenLast[P.id]<6;
   const sel='<select id="ken_'+P.id+'">'+KENK[P.t].map(k=>'<option value="'+k+'"'+(P.sk[k]>=18?' disabled':'')+'>'+KENN[k]+' '+P.sk[k]+'</option>').join('')+'</select>';
   const ln='<select id="kenL_'+P.id+'">'+['s','l'].map(L=>'<option value="'+L+'">'+KENL[L].n+'('+KENL[L].w+' 週・'+man(Math.round(KENC[P.t]*KENL[L].c))+')</option>').join('')+'</select>';
   return '<tr><td class="nm">'+esc(P.n)+(P.s&&P.s.home?' <span class="tokt">部屋育ち</span>':'')+'<div class="mute kaku" style="font-size:12px">'+KENW[P.t]+(rec?'・<span style="color:#d9822b">前の研修から 1 年たっていない(身に付きにくい)</span>':'')+'<br>留守のあいだ:'+KENOFF[P.t]+'</div></td><td>'+(on?'<b class="kaku">研修中:'+KENN[on.k]+'(あと '+on.w+' 週)</b>':sel+' '+ln+' <button class="btn sm ai" onclick="kenGo(\''+P.id+'\',document.getElementById(\'ken_'+P.id+'\').value,document.getElementById(\'kenL_'+P.id+'\').value)">研修に出す</button>')+'</td></tr>';}).join('')+'</table>'+
   '<p class="kaku mute" style="font-size:13px">短い研修は能力 +1 が 6 割、長い研修は必ず +1(ときどき +2)。前の研修から 1 年(6 場所)たっていないと効きにくくなります。場所の前の大事な週に出すか、場所のあとの落ち着いた週に出すかを考えましょう。数字は推定です。</p>'+
   '<p class="kaku mute" style="font-size:13px">部屋付き親方は、担当した弟子が勝ち越したり優勝したりすると指導の経験がたまって伸びます(付きっきりの担当がいちばん伸びる)。おかみさんは悩みごとに関わるたびに経験がたまります。ちゃんこ長は 2 年務めると得意な鍋ができ、付け人は関取のそばで学んで稽古の伸びが少し良くなります。</p></div>';}catch(e){}return h;};
 const bp=bodyPanel;bodyPanel=function(){let h=bp();try{const r=G.chk!=null?G.R[G.chk]:null;if(r){const t=r.nabeT?'得意な鍋:'+r.nabeT+(G.meal&&G.meal.k===r.nabeT?'(今の鍋。栄養 +1)':''):'得意な鍋:まだ(あと '+Math.max(0,12-(G.bnum-(r.chkB||G.bnum)))+' 場所)';h=h.replace('今の栄養:','<b class="kaku" style="color:var(--kin,#c9a24a)">'+t+'</b>。今の栄養:');}}catch(e){}return h;};
})();
</script><style>.ken td{vertical-align:middle;padding:6px 4px}.ken select{max-width:180px}</style>
