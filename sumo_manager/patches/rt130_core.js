/* ========== v130:引退の相談の見直し ==========
 ①相談の理由を見せる(rtWhy:年齢・けが・関取からの陥落・負け越し続き・気力・親方との関係・燃え尽き)。
 ②親方から切り出す(rtTalk、稽古の期間に 1 場所 1 回):引退を勧める(受けると「この場所を最後に」= r.rtLast)/条件付きで続けさせる/励ます。
 ③「もう一場所」に条件:勝ち越せなければ引退(r.rtC.k='kk')、3 場所のうちに関取の番付に戻れなければ引退('sek')。
 ④引退後の道(関取でない、または名跡の道がない弟子):世話人として残る(引退した十両・幕下から師匠の推薦。嘱託職員=Wikipedia「世話人」)、
   部屋のマネージャー、ちゃんこ店の開店を後押し、一般の仕事への道を一緒に探す(セカンドキャリア)、本人に任せる。
   世話人 G.sewa(プレイヤーごと、2 人まで):若い衆の面倒を見る(幕下以下の気力 +0.5・信頼 +0.2/場所)。65 歳で退く。数字は推定。 */
function rtLvRk(s){s=s||'';return /横綱|大関|関脇|小結|前頭/.test(s)?3:/十両/.test(s)?2:/幕下/.test(s)?1:0;}
function rtWhy(r){const W=[];const H=(r.hist||[]).slice(-3);
 if(r.age>=35)W.push('体力の衰え('+Math.floor(r.age)+'歳)');
 if(r.inj&&r.inj.s>=2)W.push('けが('+r.inj.p+')が長引いている');
 if(r.fall)W.push('関取から落ちた');
 if(H.length===3&&H.every(h=>h.w<h.l+h.ab))W.push('負け越しが 3 場所続いている');
 if(r.moeE&&G.bnum-(r.moeC||0)<=15)W.push('念願の地位のあと、気持ちが切れかけている');
 if(r.mor<30)W.push('気持ちが続かない');
 if((r.tr==null?50:r.tr)<25)W.push('親方とうまくいっていない');
 if(!W.length)W.push(r.d>=3&&r.age>=25?'番付が上がらず、先が見えない':'これからの人生を考えたい');
 return W;}
/* 本人の様子(力士の画面) */
function rtMood(r){const w=rtWhy(r);const risk=(r.age>=36?3:r.age>=33?2:r.age>=30?1:0)+(r.inj&&r.inj.s>=2?1:0)+(r.fall?1:0)+(r.mor<30?1:0)+((r.tr==null?50:r.tr)<25?1:0)+((r.hist||[]).slice(-3).filter(h=>h.w<h.l+h.ab).length>=3?1:0);
 return [risk>=3?2:risk>=1?1:0,w];}
function rtTarget(){return G.phase==='train'?G.bnum:G.bnum+1;}
/* 親方から切り出す */
function rtCanTalk(r){return r&&isPH(r.h)&&!r.ret&&G.phase==='train'&&r.rtTk!==G.bnum&&!r.rtLast;}
function rtAccept(r){return cl(.15+(r.age-28)*.06+(50-r.mor)*.008+(r.inj&&r.inj.s>=2?.15:0)+(r.fall?.1:0)+((r.tr==null?50:r.tr)-50)*.006,.05,.95);}
function rtTalk(id,k){const r=G.R[id];if(!rtCanTalk(r))return '';r.rtTk=G.bnum;let m;
 if(k==='sus'){if(Math.random()<rtAccept(r)){r.rtLast=G.bnum;stPush(r,'tk','親方に引退を勧められ、この場所を最後と決める');m=r.n+'は親方の言葉を受け止め、「この場所を最後にします」と決めました。';}
  else{r.tr=cl((r.tr==null?50:r.tr)-6,0,100);r.mor=cl(r.mor-4,0,100);stPush(r,'tk','親方に引退を勧められるが、続けると答える');m=r.n+'は「まだやれます」と答えました。信頼が少し下がりました。';}}
 else if(k==='kk'){r.rtC={k:'kk',b:G.bnum};r.mor=cl(r.mor+3,0,100);stPush(r,'tk','「この場所で勝ち越せなければ引退」と親方と約束');m=r.n+'と「この場所で勝ち越せなければ引退」と約束しました。';}
 else{r.mor=cl(r.mor+(r.mor<60?8:3),0,100);r.tr=cl((r.tr==null?50:r.tr)+1,0,100);m='親方は'+r.n+'を励ましました。気力が上がりました。';}
 addNews(m);return m;}
/* 場所のあと(retireCheck の中、プレイヤーの部屋):約束と「この場所を最後に」。true なら確率の判定はしない */
function rtCheck(r,rc){
 if(r.rtLast&&G.bnum>=r.rtLast){doRetire(r,'この場所を最後に');return true;}
 const c=r.rtC;if(!c)return false;if(G.bnum<c.b)return true;
 if(c.k==='kk'){if(rc.w>rc.l+rc.ab){r.rtC=null;r.mor=cl(r.mor+10,0,100);r.stay=true;stPush(r,'tk','約束の場所で勝ち越し、現役を続ける');addNews(r.n+'は約束の場所で勝ち越しました。現役を続けます。');return true;}
  r.rtC=null;doRetire(r,'約束の場所で勝ち越せず');return true;}
 if(r.d<=1){r.rtC=null;r.mor=cl(r.mor+10,0,100);r.stay=true;stPush(r,'tk','約束どおり関取に戻り、現役を続ける');addNews(r.n+'は約束どおり関取に戻りました。現役を続けます。');return true;}
 if(G.bnum>=c.b+2){r.rtC=null;doRetire(r,'約束の 3 場所で関取に戻れず');return true;}
 return true;}
/* 引退後の道 */
function rtPathPush(r){if(r.h!==ME())return false;G.ev.push({k:'rtPath',n:r.n,rk:bestRank(r),lv:rtLvRk(bestRank(r)),age:Math.floor(r.age),cash:Math.round(r.cash||0),pop:Math.round(r.pop||0),w:r.w,tr:Math.round(r.tr==null?50:r.tr),id:Math.random().toString(36).slice(2,8)});return true;}
function rtPathC(e){const L=[];G.sewa=G.sewa||[];
 if((e.lv===1||e.lv===2)&&e.age>=24&&e.tr>=40&&G.sewa.length<2)L.push('世話人として部屋に残す(師匠として推薦する)');
 if(G.staff.filter(s=>s.role==='sc').length<ROLE.sc.max)L.push('部屋のマネージャーとして雇う');
 L.push('ちゃんこ店の開店を後押しする(20 万円)','一般の仕事への道を一緒に探す(10 万円)','本人に任せる');return L;}
function rtCycle(){G.sewa=G.sewa||[];G.sewa.forEach(s=>{s.age+=1/6;});const out=G.sewa.filter(s=>s.age>=65);out.forEach(s=>addNews('世話人の'+s.n+'が 65 歳で退きました。'));G.sewa=G.sewa.filter(s=>s.age<65);
 if(G.sewa.length)own().forEach(r=>{if(r.d>=2){r.mor=cl(r.mor+.5*G.sewa.length,0,100);r.tr=cl((r.tr==null?50:r.tr)+.2*G.sewa.length,0,100);}});}
const RT_EVT={
 retire:{t:'引退の相談',d:e=>{const r=G.R[e.rid];if(!r)return '';return r.n+'('+r.rk+'・'+Math.floor(r.age)+'歳)から、引退したいと相談がありました。理由:'+rtWhy(r).join('・')+'。';},
  c:e=>{const r=G.R[e.rid];const L=['引退を認める','もう一場所がんばらせる','もう一場所。勝ち越せなければ引退と約束する'];if(r&&r.d>=2&&r.fall)L.push('3 場所のうちに関取に戻れなければ引退と約束する');L.push('引退を認め、第二の人生を一緒に考える(10 万円)');return L;},
  ap:(e,i)=>{const r=G.R[e.rid];if(!r)return'';const L=RT_EVT.retire.c(e);const c=L[i]||L[0];
   if(c==='引退を認める'){doRetire(r,'本人の希望');return'';}
   if(c.indexOf('第二の人生')>=0){G.money-=10;trAdd(r,10,'');G.jin=cl((G.jin==null?50:G.jin)+2,0,100);own().forEach(x=>{if(x!==r)x.tr=cl(x.tr+1,0,100);});doRetire(r,'本人の希望');return '親方は'+r.n+'と次の仕事について一緒に考えました。その姿を、ほかの弟子たちも見ていました。';}
   if(c.indexOf('勝ち越せなければ')>=0){r.rtC={k:'kk',b:rtTarget()};r.stay=true;r.mor=cl(r.mor+2,0,100);stPush(r,'tk','引退を相談し、「次の場所で勝ち越せなければ引退」と約束');return r.n+'と「次の場所で勝ち越せなければ引退」と約束しました。本人も腹をくくったようです。';}
   if(c.indexOf('関取に戻れなければ')>=0){r.rtC={k:'sek',b:rtTarget()};r.stay=true;r.mor=cl(r.mor+4,0,100);stPush(r,'tk','引退を相談し、「3 場所のうちに関取に戻れなければ引退」と約束');return r.n+'と「3 場所のうちに関取に戻れなければ引退」と約束しました。';}
   r.stay=true;r.mor=cl(r.mor-8,0,100);if((r.tr==null?50:r.tr)<40)trAdd(r,-4,'引退を引き止められた');return r.n+'はもう一場所、土俵に上がります。';}},
 rtPath:{t:'引退後の道',d:e=>'引退した'+e.n+'('+e.rk+'・'+e.age+'歳)の、これからの道を一緒に考えます。協会に親方として残るには年寄名跡が必要です。名跡がなくても、引退した十両・幕下の力士は、師匠の推薦で世話人(協会の嘱託)として残る道があります。',
  c:e=>rtPathC(e),
  ap:(e,i)=>{const L=rtPathC(e);const c=L[i]||'本人に任せる';
   if(c.indexOf('世話人')>=0){G.sewa.push({n:e.n,b:G.bnum,age:e.age,rk:e.rk});return e.n+'は世話人として部屋に残り、若い衆の面倒を見ることになりました。';}
   if(c.indexOf('マネージャー')>=0){const s=mkStaff('sc',RI(7,12));s.n='元・'+e.n;s.age=e.age;G.staff.push(s);return e.n+'は部屋のマネージャーになりました(給与 '+man(s.sal)+'/場所)。';}
   if(c.indexOf('ちゃんこ店')>=0){G.money-=20;const n=8+Math.round(e.pop/8);G.sup+=n;return e.n+'はちゃんこ店を開きました。店に部屋のひいき筋が集まり、後援会員が '+n+' 人増えました。';}
   if(c.indexOf('一般の仕事')>=0){G.money-=10;G.jin=cl((G.jin==null?50:G.jin)+1.5,0,100);own().forEach(x=>{x.tr=cl((x.tr==null?50:x.tr)+.5,0,100);});return '親方は'+e.n+'の就職先を一緒に探しました。弟子の親たちのあいだで、親方の評判が上がりました。';}
   return secondLife({n:e.n,cash:e.cash,pop:e.pop,age:e.age,w:e.w}).replace('引退した','');}}
};
