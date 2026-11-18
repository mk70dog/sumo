/* --- 部屋の注目選手とまわりの後押し(v45) --- */
function oshiR(){let r=G.oshi!=null?G.R[G.oshi]:null;if(!r||r.ret||r.h!==0)r=heyaTop();return r;}
function oshiSeed(r){if(r.okv===undefined)r.okv=Math.round(R(-20,20));if(r.jnv===undefined)r.jnv=Math.round(R(-20,20));return r;}
function oshiSch(r){return [r.hs,r.uni].filter(Boolean);}
function oshiItems(r){oshiSeed(r);const L=[];const ok=G.okami;const o=own();const per=r.per||'';
 const lastMk=r.mkc||0;const sus=r.susp>0;
 // 1 おかみさん(いなければ師匠)
 if(ok){let v=(per==='真面目'?25:per==='職人肌'?12:per==='おっとり'?8:(per==='豪快'||per==='気分屋')?-15:0)+(r.tr-50)*.6+r.okv+(ok.sk.hito-9)*2-(sus?40:0);
  if(v<=-12)v=Math.min(v,-20);const t=v>=25?'お気に入り':v<=-20?'叱られがち':'ふつう';
  const s=v>=25?pick0(r,['ちゃんこ番を休まない。差し入れの礼状も自分で書く','けがのときも明るく、部屋の雑用を進んでやる','おかみさんの用事に真っ先に手を挙げる']):v<=-20?pick0(r,['門限を破って叱られた','ちゃんこ番を抜け出しがち','あいさつの声が小さいと注意された']):'特に目立たない。言われたことはきちんとやる';
  L.push({k:'ok',lb:'おかみさん',v,t,s});}
 else{const v=(r.tr-50)*1.2;L.push({k:'ok',lb:'師匠',v,t:v>=20?'信頼が厚い':v<=-20?'信頼が薄い':'ふつう',s:'師匠からの信頼 '+Math.round(r.tr)});}
 // 2 部屋の人望
 const sen=o.filter(x=>x.pos>r.pos).length/Math.max(1,o.length-1);
 {let v=(per==='おっとり'||per==='真面目'?15:per==='豪快'?(sen>.6?-10:5):per==='野心家'?-8:per==='繊細'?-5:0)+(r.tr-50)*.4+r.jnv+(r.d<=1?10:0)-(sus?35:0);
  const big=sen>.6;const t=v>=22?'人望あつい':v<=-18?(big?'弟弟子に厳しすぎる':'部屋で浮き気味'):'ふつう';
  const s=v>=22?(big?'弟弟子の稽古によく胸を出す。付け人からも慕われる':'兄弟子にかわいがられ、同年代のまとめ役'):v<=-18?(big?'稽古場で声を荒らげることが多く、若い衆が萎縮':'稽古のあとは一人でいることが多い'):'目立った評判はない';
  L.push({k:'jin',lb:'部屋の人望',v,t,s});}
 // 3 ほかの部屋とのつながり
 {const sc=oshiSch(r);const AI=G.order.map(i=>G.R[i]).filter(x=>x&&!x.ret&&x.h>0);
  const ss=AI.filter(x=>sc.length&&oshiSch(x).some(y=>sc.includes(y)));const hm=AI.filter(x=>x.home&&x.home===r.home&&x.d<=2);
  const hs=new Set(ss.concat(hm).map(x=>x.h));const n=hs.size;const v=n>=2?Math.min(60,n*12):(n===0&&r.d<=2?-20:0);
  const ex=ss.slice(0,2).map(x=>x.n+'('+G.heya[x.h].n+')');
  L.push({k:'tsu',lb:'ほかの部屋',v,t:n?'つながり '+n+' 部屋':'つながり少ない',s:n?(ss.length?'同じ学校:'+ex.join('・')+(ss.length>2?' ほか':''):'')+(hm.length?(ss.length?'/':'')+'同じ出身('+r.home+') '+hm.length+' 人':''):(r.d<=2?'同じ学校・同じ出身の力士がいない。出稽古で胸を借りる相手が少ない':'同じ学校・同じ出身の力士はまだいない')});}
 // 4 同期
 {const dk=G.order.map(i=>G.R[i]).filter(x=>x&&x!==r&&!x.ret&&x.join===r.join&&(r.join||1)>1).sort((a,b)=>a.pos-b.pos);
  if(!dk.length)L.push({k:'doki',lb:'同期',v:0,t:'同期なし',s:'同じ場所に入門した力士がいない(記録の前に入門)'});
  else{const b=dk[0];const df=r.pos-b.pos;const v=df>24?-30:df>0?20:30;
   L.push({k:'doki',lb:'同期',v,t:df>40?'差をつけられ焦り':df>0?'競い合う':'同期の出世頭',s:df>24?'同期の '+b.n+'('+G.heya[b.h].n+'・'+b.rkS+')に大きく先を越された':df>0?b.n+'('+G.heya[b.h].n+'・'+b.rkS+')が少し先を行く。負けまいと稽古に熱':'同期 '+(dk.length+1)+' 人のなかで番付がいちばん上'});}}
 // 5 後援会
 {const best=r.best||999;let mem=0;if(r.d<=1||best<=divStart(2))mem=Math.round(40+(r.pop||20)*3+(r.d===0?80:r.d===1?30:0)+(r.t?150:0));
  let v=mem?25:0;if(mem&&(lastMk>=3||(r.d>=2&&r.d<=3)))v=-25;
  L.push({k:'koe',lb:'後援会',v,t:mem?(v<0?'会員が減り気味':'個人後援会 '+mem+' 人'):'まだない',s:mem?(v<0?(r.d>=2?'関取から落ちて、会費の更新をやめる人が出ている':'負け越しが続き、会費の更新をやめる人が出ている'):(r.home||'地元')+'の後援会。場所前に激励会'):'関取になると地元に後援会ができることが多い'});}
 // 6 ファン
 {const p=r.pop||20;let v=p>=30?30:0;let t=p>=30?'声援 多い':p>=15?'声援 ふつう':'まだ知られていない';let s='人気 '+Math.round(p)+(r.home?'。'+r.home+'の人が応援':'');
  if(sus||(lastMk>=2&&p>=20)){v=Math.min(v,-25);t='厳しい声';s=sus?'謹慎を受けて、ネットで批判が出ている':'負け越しが続き、ネットで厳しい書き込み';}
  else if(p>=30&&lastMk>=1){v=-20;t='期待が重荷';s='人気 '+Math.round(p)+'。期待の声が大きく、負けると落ち込みやすい';}
  L.push({k:'fan',lb:'ファン',v,t,s});}
 L.forEach(x=>{x.v=Math.round(cl(x.v,-100,100));x.c=x.v>=20?'p':x.v<=-18?'n':'0';});return L;}
function pick0(r,a){return a[(r.id*7+3)%a.length];}
/* 後押しの効き目:1 週ごとに気力へ。よい項目 1 つ +0.2、悪い項目 1 つ -0.2(合計で ±0.8 まで。推定) */
function oshiWeek(){if(!G||G.phase!=='train')return;own().forEach(r=>{const L=oshiItems(r);let d=0;L.forEach(x=>{if(x.c==='p')d+=.2;else if(x.c==='n')d-=.2;});r.mor=cl(r.mor+cl(d,-.8,.8),0,100);});}
