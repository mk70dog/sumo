/* 取組の計算の出来事(b.ev)から動きを作る。p は「最初の力士(b.a)が押している量」(±100 で土俵際) */
function dhPlanEv(b,pk){const ev=b.ev,nar=b.nar||[];const winE=pk.winE;const aIsE=b.a===pk.E.id;const k=b.k;const T=dhType(k);
 const rnd=dhRand(dhSeed(b));const sg=winE?1:-1;const ang=(rnd()-.5)*1.1;const dir=[Math.cos(ang)*sg,Math.sin(ang)];
 const WN=winE?pk.E.n:pk.Wt.n,LN=winE?pk.Wt.n:pk.E.n;const wIdx=b.w===b.a?0:1;/* 勝った力士が ev の何番目(0=a,1=もう一人)か */
 const fw=pv=>(wIdx===0?pv:-pv)/100*.9;/* 勝つ側が前に出ている量(土俵の半径を 1) */
 const form=(ev.find(x=>x.e==='form')||{}).f||'Y';const st=form==='O'?'oshi':'yotsu';const DD=st==='oshi'?.25:.2;
 const P=[[0,0,0,.36,'tachi',0]],ph=[];let lat=0,last=0,lastN=0;
 const steps=ev.filter(x=>x.e!=='form'||true);const nS=Math.max(1,steps.length);const t0=.1,t1=.8;let i=0;
 const at=(f,a)=>[dir[0]*f-dir[1]*a,dir[1]*f+dir[0]*a];
 const grip=[9,9];let sd=rnd()<.5?1:-1,uchi=false;
 const say=(t,n)=>{for(;lastN<n&&lastN<nar.length;lastN++)ph.push([t,nar[lastN]]);};
 ph.push([0,'仕切り。両者、手をついた']);
 steps.forEach(x=>{const t=t0+(t1-t0)*(i++/nS);
  if(x.e==='henka'){if(x.ok){P.push([t,0,0,.3,'tachi',0]);}else{last=fw(x.p);const c=at(last,lat);P.push([t,c[0],c[1],DD,st,1]);}}
  else if(x.e==='tachi'){last=fw(x.p);const c=at(last,lat);P.push([Math.max(t,.1),c[0],c[1],DD,st,Math.sign(last)||0]);}
  else if(x.e==='form'){if(form==='Y'){const g=x.moro>=0?x.moro:x.g;const tg=t+.02;if(g<0){grip[0]=grip[1]=tg;}else{const isE=(g===0)===aIsE;grip[isE?0:1]=tg;}}}
  else if(x.e==='r'||x.p!==undefined){const f=fw(x.p);lat=Math.max(-.5,Math.min(.5,lat+(rnd()-.5)*.25));const c=at(f,lat);P.push([t,c[0],c[1],DD,st,f>last+.02?1:f<last-.02?-1:0]);last=f;
   if(x.e==='nage'&&!x.ok)uchi=uchi;}
  say(t,x.n);});
 const L=P[P.length-1];const fin=Math.max(L[0]+.02,t1);let out,how='出た';
 if(T==='nage'||T==='ashi'){if(T==='ashi')how='倒れた';sd=rnd()<.5?1:-1;const piv=[L[1],L[2]];const ra=Math.atan2(dir[1],dir[0])+sd*2.3;out=[piv[0]+Math.cos(ra)*.62,piv[1]+Math.sin(ra)*.62];how='倒れた';uchi=ev.some(x=>x.e==='nage'&&!x.ok);P.push([fin,L[1],L[2],DD,st,1]);}
 else if(T==='hiki'||ev.some(x=>x.e==='koshi')){sd=rnd()<.5?1:-1;const ch=[L[1]-dir[0]*.2,L[2]-dir[1]*.2];P.push([fin,ch[0],ch[1],DD,'oshi',-1]);out=[ch[0]-dir[0]*.62,ch[1]-dir[1]*.62];how='落ちた';}
 else if(T==='uchari'||ev.some(x=>x.e==='rev'||x.e==='isami')){const e=[L[1],L[2]];P.push([fin,e[0],e[1],DD,st,-1]);out=at(-1.36,(rnd()<.5?1:-1)*.35);if(T!=='uchari'){/* 土俵際の逆転(突き落とし・小手投げなど) */out=at(-.95,(rnd()<.5?1:-1)*.5);how=/投げ/.test(k)?'倒れた':'落ちた';}}
 else{const e=at(.93,lat*.5);P.push([fin,e[0],e[1],T==='oshi'?.3:DD,T==='okuri'?'yotsu':st,1]);out=at(1.4,lat*.3);if(T==='taoshi')how='倒れた';}
 say(fin,nar.length);
 const TT=ev.some(x=>x.e==='koshi')?'hiki':ev.some(x=>x.e==='isami')?'hiki':ev.some(x=>x.e==='rev')&&T!=='uchari'?(/投げ/.test(k)?'nage':'hiki'):T;
 return {P,out,how,T:TT==='ashi'?'nage':TT,winE,dir,ph,k,WN,LN,fin,sd,uchi,grip};}
