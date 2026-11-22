/* ========== v127:弟子ひとりひとりの物語(目標・壁・転機) ==========
 ・目標:親方が力士ごとに「次の目標」と「期限(場所数)」を立てる。高め(早く上へ)と、じっくり(期限を長く・今の地位を守る)の 2 つから、
   親方が年齢と勢いで選ぶ。プレイヤーは力士の画面で選び直せる(r.mkP 'h'|'j'、無ければ親方まかせ)。
   届いたら 気力 +10・信頼 +4、届かなければ 気力 −4・信頼 −1(数字は推定)。
 ・壁:同じ地位(幕下上位・十両・平幕)に 6 場所以上いて、勝ち負けがほぼ五分のとき「壁」の出来事。どう手を打つかを選ぶ(3 場所効く)。
   実際にも十両と幕下は待遇が大きく違い「天国と地獄」と言われ、幕下上位は最も競争が厳しい地位とされる。
 ・転機:けが・陥落からの返り咲き(復活)、大器晩成、遅咲きの昇進のあとの燃え尽き。
 ・歩み:初土俵・昇進・優勝・三賞・目標・壁・転機を、力士ごとに年表として残す(r.sto、最大 40 件)。 */
const STLV={2:'新十両',3:'新入幕',4:'新三役',5:'大関',6:'横綱'};
const STLVB={2:'関取',3:'幕内',4:'三役',5:'大関'};
function stPush(r,k,t,b){if(!r.sto)r.sto=[];r.sto.push({b:b==null?G.bnum:b,k:k,t:t});if(r.sto.length>40)r.sto.splice(0,r.sto.length-40);}
function stBest(r){let m=rankLv(r);(r.hist||[]).forEach(h=>{m=Math.max(m,rankLv({t:h.t,d:h.d}));});return Math.max(m,r.stB||0);}
function stMk15(r){return r.d<2||(r.d===2&&r.pos-divStart(2)+1<=15);}
/* 年表を、残っている成績から作り直す(前の版のセーブ・入門したての力士) */
function stInit(r){if(r.sto)return false;r.sto=[];const H=r.hist||[];
 stPush(r,'in','初土俵',H.length?H[0].b:G.bnum);
 let bd=9,bl=1;H.forEach(h=>{const lv=rankLv({t:h.t,d:h.d});
  if(h.d<bd&&bd!==9&&h.d>=2)stPush(r,'up',DIVS[h.d].n+'に上がる',h.b);
  if(lv>bl&&lv>=2)stPush(r,'up',STLV[lv]+'('+h.rk+')',h.b);
  if(h.yu)stPush(r,'yu',DN[h.d]+'優勝('+h.w+'勝'+(h.l+h.ab)+'敗)',h.b);
  bd=Math.min(bd,h.d);bl=Math.max(bl,lv);});
 r.stB=bl;r.stD=Math.min(bd,r.d);r._ss=r.sansho||0;return true;}
/* 目標の候補 [高め, じっくり] */
function stCand(r){const lv=rankLv(r),best=stBest(r),out=[];
 const mk=(k,o)=>Object.assign({k:k},o);
 if(best>=2&&lv<best&&lv<=3){const tl=lv<2?2:Math.min(best,lv+1);
  out.push(mk('lv',{lv:tl,n:6,tx:STLVB[tl]+'に返り咲く',bk:1}));out.push(mk('lv',{lv:tl,n:12,tx:STLVB[tl]+'に返り咲く(じっくり)',bk:1}));return out;}
 const kk=mk('kk',{c:3,n:6,tx:'勝ち越しを 3 回(6 場所のうちに)'});
 if(r.d>=3){const n={5:3,4:6,3:8}[r.d];out.push(mk('d',{d:r.d-1,n:n,tx:DIVS[r.d-1].n+'に上がる'}));out.push(r.d===5?mk('d',{d:4,n:6,tx:'序二段に上がる(じっくり)'}):kk);return out;}
 if(r.d===2&&!stMk15(r)){out.push(mk('p15',{n:4,tx:'幕下上位(15 枚目以内)に上がる'}));out.push(kk);return out;}
 if(r.d===2){out.push(mk('lv',{lv:2,n:4,tx:'新十両(関取になる)'}));out.push(mk('lv',{lv:2,n:8,tx:'新十両(じっくり)'}));return out;}
 if(r.d===1){out.push(mk('lv',{lv:3,n:6,tx:'新入幕'}));out.push(mk('keep',{lv:2,n:6,tx:'十両に定着する(6 場所)'}));return out;}
 if(r.t==='Y'){out.push(mk('yu',{n:6,tx:'幕内優勝'}));out.push(mk('w10',{c:3,n:6,tx:'二桁勝利を 3 回(横綱の責任)'}));return out;}
 if(r.t==='O'){out.push(mk('yu',{n:9,tx:'幕内優勝(綱とりへ)'}));out.push(mk('keep',{lv:5,n:6,tx:'大関を守る(6 場所)'}));return out;}
 if(r.t){out.push(mk('lv',{lv:5,n:9,tx:'大関に上がる'}));out.push(mk('keep',{lv:4,n:4,tx:'三役に定着する(4 場所)'}));return out;}
 out.push(mk('lv',{lv:4,n:8,tx:'三役に上がる'}));out.push(mk('keep',{lv:3,n:6,tx:'幕内に定着する(6 場所)'}));return out;}
/* 親方が選ぶ:若いか、勢いがあれば高め */
function stAutoPick(r){const H=(r.hist||[]).slice(-3);const net=H.reduce((a,h)=>a+h.w-h.l-h.ab,0);
 return net>=3&&r.age<=30?0:1;}
function stSet(r,keepB){const C=stCand(r);const i=r.mkP==='h'?0:r.mkP==='j'?1:stAutoPick(r);const g=C[i]||C[0];
 r.mk=Object.assign({},g,{b0:keepB&&r.mk?r.mk.b0:G.bnum,y0:r.yu[0],pk:i});}
function stDone(r,g){if(g.k==='d')return r.d<=g.d;if(g.k==='p15')return stMk15(r);if(g.k==='lv')return rankLv(r)>=g.lv;if(g.k==='yu')return r.yu[0]>g.y0;
 if(g.k==='kk')return (r.hist||[]).filter(h=>h.b>=g.b0&&h.w>h.l+h.ab).length>=g.c;
 if(g.k==='w10')return (r.hist||[]).filter(h=>h.b>=g.b0&&h.w>=10).length>=g.c;return false;}
function stLeft(r){const g=r.mk;return g?Math.max(0,g.n-(G.bnum-g.b0)):0;}
function stGoal(r){if(!r.mk){stSet(r);return;}const g=r.mk,el=G.bnum-g.b0;
 let res=0;if(g.k==='keep'){if(rankLv(r)<g.lv)res=-1;else if(el>=g.n)res=1;}else if(stDone(r,g))res=1;else if(el>=g.n)res=-1;
 if(!res)return;
 if(res>0){r.mor=cl(r.mor+10,0,100);r.tr=cl((r.tr==null?50:r.tr)+4,0,100);r.mkW=(r.mkW||0)+1;
  const kb=r.kb&&G.bnum-r.kb.b<=8;stPush(r,'ok','目標達成:'+g.tx+(kb?'(壁を越えた)':''));if(kb){r.mor=cl(r.mor+5,0,100);r.kb=null;}
  addNews('🎯 '+r.n+'が目標「'+g.tx+'」に届きました。'+(kb?'壁を越えました。':''));}
 else{r.mor=cl(r.mor-4,0,100);r.tr=cl((r.tr==null?50:r.tr)-1,0,100);r.mkF=(r.mkF||0)+1;stPush(r,'ng','目標に届かず:'+g.tx);}
 r.mk=null;stSet(r);}
/* 壁:同じ地位に長くいて、勝ち負けがほぼ五分 */
function stKabe(r){if(r.inj||r.age<20||r.age>34||r.d>2||r.t==='Y'||r.t==='O'||r.t==='S'||r.t==='K')return;
 if(r.d===2&&r.pos-divStart(2)+1>20)return;if(G.bnum-(r.kbB||-99)<12)return;
 const H=(r.hist||[]).slice(-6);if(H.length<6||H.some(h=>h.d!==r.d||h.t))return;
 const net=H.slice(-6).reduce((a,h)=>a+h.w-h.l-h.ab,0);if(Math.abs(net)>5)return;
 if(Math.random()>=.5)return;r.kbB=G.bnum;G.ev.push({k:'kabe',rid:r.id});}
function stKabeName(r){return r.d===2?'十両の手前の壁(幕下上位)':r.d===1?'十両の壁(幕内に上がれない)':'三役の壁(平幕から上がれない)';}
/* 燃え尽き:遅咲き(29 歳以上)で幕内以上の新しい地位に上がったあと、3 場所続けて負け越し */
function stMoe(r){if(!r.moeC||r.moeE||G.bnum-r.moeC>12)return;const H=(r.hist||[]).slice(-3);
 if(H.length<3||H.some(h=>h.b<r.moeC||h.w>=h.l+h.ab+1||h.ab>=8))return;r.moeE=1;G.ev.push({k:'moe',rid:r.id});}
/* 番付発表のあと(nextCycle の中、プレイヤーごと) */
function stCycle(old,msgs){own().forEach(r=>{const fresh=stInit(r);const o=old[r.id];const H=r.hist||[],h=H[H.length-1];
 if(!fresh&&o&&h&&h.b===G.bnum-1){
  if(h.yu)stPush(r,'yu',DN[h.d]+'優勝('+h.w+'勝'+(h.l+h.ab)+'敗)',h.b);
  if((r.sansho||0)>(r._ss||0))stPush(r,'sh','三賞',h.b);
  const lvO=rankLv({t:o.t,d:o.d}),lvN=rankLv(r);
  if(r.d<(r.stD==null?9:r.stD)&&r.d>=2)stPush(r,'up',DIVS[r.d].n+'に上がる');
  if(lvN>(r.stB||1)&&lvN>=2){stPush(r,'up',STLV[lvN]+'('+r.rk+')');if(lvN>=3&&r.age>=29)r.moeC=G.bnum;}
  if(lvN<lvO&&lvO>=2&&lvN<2){stPush(r,'dn','関取から落ちる。実際にも、ここで引退を選ぶ力士は多い');r.fall={lv:lvO,inj:!!(h.ab>=8||r.inj)};}
  if(o.t==='O'&&r.t!=='O'&&r.t!=='Y')stPush(r,'dn','大関から落ちる');
  if(r.fall&&lvN>=r.fall.lv){stPush(r,'fk','復活:'+(r.fall.inj?'けがを乗り越えて':'')+STLVB[r.fall.lv]+'に返り咲き');r.mor=cl(r.mor+10,0,100);
   msgs.push('🔥 '+r.n+'が'+(r.fall.inj?'けがを乗り越えて':'')+STLVB[r.fall.lv]+'に返り咲きました。');r.fall=null;}
  if(r.daiki===G.bnum-1)stPush(r,'dk','大器晩成:稽古で急に力をつける');}
 r._ss=r.sansho||0;r.stD=Math.min(r.stD==null?9:r.stD,r.d);r.stB=Math.max(r.stB||1,rankLv(r));
 stGoal(r);stKabe(r);stMoe(r);});}
/* 壁を破る手(3 場所のあいだ伸びが良くなる) */
function stG(r){const k=r.kb;if(!k||G.bnum-k.b>=3)return 1;return k.c===0?1.12:k.c===1?1.08:1;}
const ST_EVT={
 kabe:{t:'壁にぶつかっている',d:e=>{const r=G.R[e.rid];return r?r.n+'('+r.rk+')は、'+stKabeName(r)+'にぶつかっています。ここ 6 場所、同じところで勝ったり負けたりです。親方としてどう手を打ちますか。':'';},
  c:['出稽古で強い相手にもまれる(費用 10 万円)','親方が付きっきりで基本を見直す','気分を変える(ふるさとで休ませる)','何もしないで見守る'],
  init:e=>{if(!G.R[e.rid])return false;},
  ap:(e,i)=>{const r=G.R[e.rid];if(!r)return '';stPush(r,'kb','壁:'+stKabeName(r)+'(手:'+['出稽古','基本の見直し','気分転換','見守る'][i]+')');
   if(i===0){G.money-=10;r.fat=cl(r.fat+10,0,100);r.kb={b:G.bnum,c:0};return r.n+'はよその部屋の関取にもまれて、毎日へとへとです。3 場所のあいだ、伸びが良くなります。';}
   if(i===1){r.tr=cl((r.tr==null?50:r.tr)+5,0,100);r.kb={b:G.bnum,c:1};return '親方が四股・すり足から見直しました。信頼が深まり、3 場所のあいだ伸びが少し良くなります。';}
   if(i===2){r.mor=cl(r.mor+15,0,100);r.fat=cl(r.fat-20,0,100);r.cond=cl(r.cond+5,0,100);r.kb={b:G.bnum,c:2};return r.n+'はふるさとで少し休み、気持ちが軽くなったようです。';}
   r.mor=cl(r.mor-2,0,100);r.kb={b:G.bnum,c:3};return '本人に任せて見守ることにしました。';}},
 moe:{t:'気持ちが切れかけている',d:e=>{const r=G.R[e.rid];return r?r.n+'は念願の地位に上がってから、3 場所続けて負け越しています。目標を果たして、気持ちが切れかけているようです。':'';},
  c:['次の目標を一緒に決める','しばらく見守る'],init:e=>{if(!G.R[e.rid])return false;},
  ap:(e,i)=>{const r=G.R[e.rid];if(!r)return '';if(i===0){r.mor=cl(r.mor+12,0,100);r.tr=cl((r.tr==null?50:r.tr)+3,0,100);r.mkP=null;r.mk=null;stSet(r);stPush(r,'tk','転機:親方と次の目標「'+r.mk.tx+'」を決める');return '親方と話し合い、次の目標を「'+r.mk.tx+'」に決めました。気力が戻ってきました。';}
   r.mor=cl(r.mor+4,0,100);stPush(r,'tk','転機:燃え尽きかけるが、見守られる');return '見守ることにしました。';}}
};
