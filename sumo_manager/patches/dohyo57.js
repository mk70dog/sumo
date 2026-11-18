/* --- 上から見た土俵 v3(四角の力士 B・体重で大きさ・色の変化)  kaiga16 --- */
/* 座標:土俵の中心 (0,0)、俵の内側が半径 1。東 = 左(-x)、西 = 右(+x)、正面 = 下(+y)。 */
function dhType(k){k=k||'';if(/うっちゃり|打っ棄り/.test(k))return 'uchari';if(/投げ|捻り|ひねり|掬い|すくい|網打ち|櫓|小股/.test(k))return 'nage';if(/送り/.test(k))return 'okuri';if(/はたき|叩き|引き落とし|引っ掛け|肩透かし|突き落とし|とったり/.test(k))return 'hiki';if(/突き出し|突き倒し|押し出し|押し倒し/.test(k))return 'oshi';if(/倒れ|浴びせ/.test(k))return 'taoshi';return 'yori';}
function dhRand(seed){let s=seed>>>0||1;return ()=>{s=(s*1103515245+12345)>>>0;return (s>>>8)/16777216;};}
/* P の各点:[t, cx, cy, d(2人の間の半分), 構え('tachi'|'yotsu'|'oshi'), 誰が押しているか(1=勝つ側,-1=負ける側,0)] */
function dhPlan(k,winE,seed,nE,nW){let sd=1;const rnd=dhRand(seed),T=dhType(k);const sg=winE?1:-1;const ang=(rnd()-.5)*1.3;const dir=[Math.cos(ang)*sg,Math.sin(ang)];
 const WN=winE?nE:nW,LN=winE?nW:nE;const P=[],ph=[];const st=T==='oshi'||(T==='hiki'&&rnd()<.6)?'oshi':'yotsu';
 const DD=st==='oshi'?.25:.2;const at=(f,a)=>[dir[0]*f-dir[1]*a,dir[1]*f+dir[0]*a];/* f=勝つ側が押す向き、a=横 */
 P.push([0,0,0,.36,'tachi',0]);ph.push([0,'仕切り。両者、手をついた']);
 P.push([.1,0,0,DD,st,0]);ph.push([.1,st==='oshi'?'立ち合い!激しい突っ張りの応酬':'立ち合い!がっぷり四つ']);
 let c=at((rnd()-.5)*.3,(rnd()-.5)*.3);P.push([.2,c[0],c[1],DD,st,0]);
 /* 攻め合い:負ける側が先に攻める場面(シーソー)を入れることがある */
 const sea=rnd()<.6||T==='uchari';let t=.2;
 if(sea){c=at(-.74,(rnd()-.5)*.6);t=.36;P.push([t,c[0],c[1],DD,st,-1]);ph.push([.27,LN+'が攻める!']);ph.push([.34,WN+'、土俵際!残った、残った!']);
  if(T!=='uchari'){c=at(-.05,(rnd()-.5)*.4);t=.5;P.push([t,c[0],c[1],DD,st,1]);ph.push([.42,WN+'、こらえて押し返す']);}}
 const zan=rnd()<.5&&T!=='uchari';
 if(zan){c=at(.76,(rnd()-.5)*.6);t+=.14;P.push([t,c[0],c[1],DD,st,1]);ph.push([t-.06,WN+'が出る!']);ph.push([t-.01,LN+'、俵に足がかかる…残った!']);c=at(.1,(rnd()-.5)*.5);t+=.12;P.push([t,c[0],c[1],DD,st,-1]);ph.push([t-.06,LN+'、回り込んで中央へ']);}
 if(!sea&&!zan){c=at(.15,(rnd()-.5)*.5);t=.45;P.push([t,c[0],c[1],DD,st,0]);ph.push([.3,'土俵中央で動かない…']);}
 /* 決着 */
 let out,how='出た';const L=P[P.length-1];const t0=L[0];const fin=Math.max(t0+.12,.82);
 if(T==='uchari'){const e=at(-.9,(rnd()-.5)*.4);P.push([fin,e[0],e[1],DD,st,-1]);ph.push([t0+.04,LN+'が一気に寄る!']);ph.push([fin-.03,WN+'、俵の上で体を入れ替えた!']);out=at(-1.2,(rnd()<.5?1:-1)*.45);ph.push([.97,k+'!'+WN+'の大逆転']);}
 else if(T==='nage'){P.push([fin,L[1],L[2],DD,st,1]);ph.push([t0+.04,WN+'、上手を引いた']);ph.push([fin-.03,'振った!']);const piv=[L[1],L[2]];sd=rnd()<.5?1:-1;const ra=Math.atan2(dir[1],dir[0])+sd*2.3;out=[piv[0]+Math.cos(ra)*.9,piv[1]+Math.sin(ra)*.9];how='ひっくり返った';ph.push([.97,k+'!'+WN+'の勝ち']);}
 else if(T==='hiki'){P.push([fin,L[1],L[2],.12,st,-1]);ph.push([t0+.04,LN+'が前に出る']);ph.push([fin-.03,WN+'、引いた!']);out=[L[1]-dir[0]*.5+dir[1]*.15,L[2]-dir[1]*.5-dir[0]*.15];how='落ちた';ph.push([.97,k+'!'+WN+'の勝ち']);}
 else{const e=at(.93,(rnd()-.5)*.5);P.push([fin,e[0],e[1],T==='oshi'?.17:.11,T==='okuri'?'yotsu':st,1]);ph.push([t0+.04,T==='okuri'?WN+'が後ろに回った!':T==='oshi'?WN+'が一気に突き放す!':WN+'が寄って出る!']);ph.push([fin-.04,LN+'、俵に足が…']);out=at(1.22,(rnd()-.5)*.3);if(T==='taoshi')how='倒れた';ph.push([.97,k+'!'+WN+'の勝ち']);}
 return {P,out,how,T,winE,dir,ph,k,WN,LN,fin,sd};}
function dhAt(pl,t){const P=pl.P;let i=0;while(i<P.length-1&&P[i+1][0]<=t)i++;const a=P[i],b=P[Math.min(i+1,P.length-1)];const u=b[0]>a[0]?Math.min(1,Math.max(0,(t-a[0])/(b[0]-a[0]))):1;const e=u*u*(3-2*u);
 const cx=a[1]+(b[1]-a[1])*e,cy=a[2]+(b[2]-a[2])*e,d=a[3]+(b[3]-a[3])*e;const dx=pl.dir[0],dy=pl.dir[1];
 let W=[cx-dx*d,cy-dy*d],Lo=[cx+dx*d,cy+dy*d];let stance=(e<.5?a:b)[4],push=(e<.5?a:b)[5],fall=0;
 const lastT=P[P.length-1][0];
 let spin=0,flip=1,air=0;
 if(t>lastT&&pl.T==='nage'){const u2=Math.min(1,(t-lastT)/(1-lastT));const e2=u2<.75?u2/.75:1;const piv=W;const a0=Math.atan2(Lo[1]-piv[1],Lo[0]-piv[0]),a1=Math.atan2(pl.out[1]-piv[1],pl.out[0]-piv[0]);let da=a1-a0;if(da>Math.PI)da-=2*Math.PI;if(da<-Math.PI)da+=2*Math.PI;const ee=e2*e2*(3-2*e2);const rr=Math.hypot(Lo[0]-piv[0],Lo[1]-piv[1])+(Math.hypot(pl.out[0]-piv[0],pl.out[1]-piv[1])-Math.hypot(Lo[0]-piv[0],Lo[1]-piv[1]))*ee;const aa=a0+da*ee;Lo=[piv[0]+Math.cos(aa)*rr,piv[1]+Math.sin(aa)*rr];spin=pl.sd*540*ee;flip=Math.cos(Math.PI*ee);air=u2<.75?Math.sin(Math.PI*e2):0;fall=ee;stance='free';const r0=pl.winE?{E:W,W:Lo}:{E:Lo,W:W};return Object.assign(r0,{stance,push:0,fall:0,lose:pl.winE?'W':'E',spin,flip,air,land:u2>=.75});}
 if(t>lastT){const u2=Math.min(1,(t-lastT)/(1-lastT));const e2=1-Math.pow(1-u2,3);fall=e2;Lo=[Lo[0]+(pl.out[0]-Lo[0])*e2,Lo[1]+(pl.out[1]-Lo[1])*e2];
  if(pl.T==='hiki')W=[W[0]+dy*.15*e2,W[1]-dx*.15*e2];else if(pl.T!=='nage')W=[W[0]+(pl.out[0]-W[0])*.3*e2,W[1]+(pl.out[1]-W[1])*.3*e2];stance=pl.T==='oshi'?'oshi':'free';}
 return pl.winE?{E:W,W:Lo,stance,push:push*(1),fall,lose:'W'}:{E:Lo,W:W,stance,push:-push,fall,lose:'E'};}

/* 四角の力士(B):体重で大きさ。背中側にまわしの色の帯。 */
function dhSide(kg){return 46*Math.pow((kg||160)/160,.8);}
function dhRik(cls,col,nm,kg){const s=dhSide(kg),h=s/2;return '<g class="'+cls+'" data-h="'+h.toFixed(1)+'"><g class="rot"><g class="arms"><line class="a1" stroke="#c99a6a" stroke-width="'+Math.max(6,s*.17).toFixed(1)+'" stroke-linecap="round"/><line class="a2" stroke="#c99a6a" stroke-width="'+Math.max(6,s*.17).toFixed(1)+'" stroke-linecap="round"/><circle class="h1" r="'+Math.max(5,s*.12).toFixed(1)+'" fill="#f0c998" stroke="#5a3a1a" stroke-width="1.5"/><circle class="h2" r="'+Math.max(5,s*.12).toFixed(1)+'" fill="#f0c998" stroke="#5a3a1a" stroke-width="1.5"/><g class="bst" opacity="0"></g></g>'+
 '<rect class="aura" x="'+(-h-7)+'" y="'+(-h-7)+'" width="'+(s+14)+'" height="'+(s+14)+'" rx="10" fill="none" stroke="#ff8a1f" stroke-width="5" opacity="0"/>'+
 '<rect class="bd" x="'+(-h)+'" y="'+(-h)+'" width="'+s+'" height="'+s+'" rx="4" fill="#f0c998" stroke="#5a3a1a" stroke-width="2"/><rect x="'+(-h)+'" y="'+(-h)+'" width="'+(s*.28)+'" height="'+s+'" fill="'+col+'"/>'+
 '<ellipse cx="'+(h*.4)+'" rx="'+(s*.2)+'" ry="'+(s*.18)+'" fill="#2b2420"/><ellipse cx="'+(h*.15)+'" rx="'+(s*.12)+'" ry="'+(s*.06)+'" fill="#000"/></g>'+
 '<text class="nm" y="'+(-h-14)+'" text-anchor="middle" font-size="13" font-weight="bold" fill="'+col+'" stroke="#fff8ea" stroke-width="3" paint-order="stroke">'+esc(nm)+'</text><text class="tg" y="'+(h+22)+'" text-anchor="middle" font-size="12" font-weight="bold" fill="#8a5a00" stroke="#fff8ea" stroke-width="3" paint-order="stroke"></text></g>';}
function dhSVG(id,nE,nW,kE,kW){return '<div class="dhw" id="'+id+'w"><svg class="dhy" id="'+id+'" viewBox="-170 -170 340 340"><defs><radialGradient id="'+id+'g"><stop offset="0" stop-color="#e3cfa3"/><stop offset="1" stop-color="#d2b98a"/></radialGradient></defs><rect x="-170" y="-170" width="340" height="340" fill="#e8dcc0" rx="10"/><circle r="150" fill="#cdb37f"/><circle r="135" fill="url(#'+id+'g)"/><circle class="tw" r="135" fill="none" stroke="#8a6a3a" stroke-width="9"/>'+
 '<line x1="-14" y1="-14" x2="-14" y2="14" stroke="#fff" stroke-width="3"/><line x1="14" y1="-14" x2="14" y2="14" stroke="#fff" stroke-width="3"/>'+
 '<text y="166" text-anchor="middle" font-size="12" fill="#5a4a33">正面</text><text y="-158" text-anchor="middle" font-size="12" fill="#5a4a33">向正面</text><text x="-166" y="4" font-size="12" fill="#5a4a33">東</text><text x="152" y="4" font-size="12" fill="#5a4a33">西</text>'+
 '<circle class="fl" r="10" fill="#fff" opacity="0"/><g class="dust"><g class="dd"><circle r="16" fill="#f3e8cf"/><circle cx="22" cy="10" r="12" fill="#f3e8cf"/><circle cx="-20" cy="12" r="13" fill="#f3e8cf"/><circle cx="8" cy="-22" r="11" fill="#f3e8cf"/><circle cx="-14" cy="-18" r="10" fill="#f3e8cf"/><circle cx="26" cy="-10" r="8" fill="#f3e8cf"/></g></g>'+dhRik('ge','#b5361f',nE,kE)+dhRik('gw','#2d4d7a',nW,kW)+
 '<g class="mk" opacity="0"><circle r="40" fill="none" stroke="#b5361f" stroke-width="3" stroke-dasharray="6 4"/><text class="mkt" y="58" text-anchor="middle" font-size="13" font-weight="bold" fill="#b5361f" stroke="#fff8ea" stroke-width="3" paint-order="stroke"></text></g>'+
 '<g class="stamp" opacity="0"><rect x="-70" y="-22" width="140" height="44" rx="6" fill="#fff8ea" stroke="#b5361f" stroke-width="4"/><text class="stt" y="9" text-anchor="middle" font-size="24" font-weight="bold" fill="#b5361f" font-family="serif"></text></g>'+
 '<text class="zan" y="-92" text-anchor="middle" font-size="26" font-weight="bold" fill="#b5361f" stroke="#fff8ea" stroke-width="4" paint-order="stroke" opacity="0">残った!</text></svg>'+
 '<div class="dhbar"><span class="be">'+esc(nE)+'</span><i><b></b></i><span class="bw">'+esc(nW)+'</span></div>'+
 '<div class="dhlg"><span><i style="background:#ffb36b"></i>調子が上がった</span><span><i style="background:#ffe14a"></i>突っ張りが炸裂</span><span><i style="background:#e0a82e;border-radius:50%"></i>まわしをしっかりつかんだ</span></div></div>';}
function mix(a,b,u){const pa=[1,3,5].map(i=>parseInt(a.substr(i,2),16)),pb=[1,3,5].map(i=>parseInt(b.substr(i,2),16));return 'rgb('+pa.map((x,i)=>Math.round(x+(pb[i]-x)*u)).join(',')+')';}
/* fx:{heat 0〜1, burst 0〜1(突っ張りの当たり), grip 0|1} */
function dhPose(g,p,q,stance,ph,pushing,fallen,fx){const S=135;const h=+g.dataset.h;const x=p[0]*S,y=p[1]*S;let a=Math.atan2(q[1]-p[1],q[0]-p[0])*180/Math.PI;g.setAttribute('transform','translate('+x.toFixed(1)+','+y.toFixed(1)+')');
 const rot=g.querySelector('.rot');const sc=1+(fx.air||0)*.55;const fy=fx.flip===undefined?1:(Math.abs(fx.flip)<.12?(fx.flip<0?-.12:.12):fx.flip);rot.setAttribute('transform','rotate('+(a+(fx.spin||0)).toFixed(1)+')'+(fallen?' scale('+(1-.2*fallen)+')':'')+' scale('+sc.toFixed(2)+','+(fy*sc).toFixed(2)+')');g.querySelector('.bd').setAttribute('fill',fy<0?'#d9a87a':mix('#f0c998','#ffa060',fx.heat||0));
 let h1,h2;const dist=Math.hypot(q[0]-p[0],q[1]-p[1])*S;let ext=[0,0];
 if(stance==='tachi'){h1=[h+7,-h*.55];h2=[h+7,h*.55];}
 else if(stance==='oshi'){const r1=Math.max(0,Math.sin(ph*14)),r2=Math.max(0,Math.sin(ph*14+Math.PI));ext=[r1,r2];const L=Math.max(h+6,dist-h*.9);h1=[h+6+r1*(L-h-6),-h*.45];h2=[h+6+r2*(L-h-6),h*.45];}
 else if(stance==='yotsu'){const L=Math.min(dist*.8,h*2.2);h1=[L,-h-6];h2=[L,h+6];}
 else{h1=[h,-h-10];h2=[h,h+10];}
 const a1=g.querySelector('.a1'),a2=g.querySelector('.a2');a1.setAttribute('x1',h*.3);a1.setAttribute('y1',-h*.75);a1.setAttribute('x2',h1[0]);a1.setAttribute('y2',h1[1]);a2.setAttribute('x1',h*.3);a2.setAttribute('y1',h*.75);a2.setAttribute('x2',h2[0]);a2.setAttribute('y2',h2[1]);
 const c1=g.querySelector('.h1'),c2=g.querySelector('.h2');c1.setAttribute('cx',h1[0]);c1.setAttribute('cy',h1[1]);c2.setAttribute('cx',h2[0]);c2.setAttribute('cy',h2[1]);
 /* 色の変化 */
 const heat=fx.heat||0;const au=g.querySelector('.aura');au.setAttribute('opacity',heat>.55?((heat-.55)/.45*(.6+.4*Math.sin(ph*9))).toFixed(2):0);
 const hit1=stance==='oshi'&&ext[0]>.92&&fx.burst,hit2=stance==='oshi'&&ext[1]>.92&&fx.burst;
 const gc=fx.grip&&stance==='yotsu';
 [[c1,hit1],[c2,hit2]].forEach(([c,hit],i)=>{c.setAttribute('fill',hit?'#ffe14a':gc?'#e0a82e':'#f0c998');c.setAttribute('stroke',hit?'#ff7a00':gc?'#8a5a00':'#5a3a1a');c.setAttribute('stroke-width',hit||gc?3:1.5);});
 const bs=g.querySelector('.bst');if(hit1||hit2){const hp=hit1?h1:h2;bs.innerHTML='<path d="M0,-11 L3,-3 L11,-3 L5,2 L8,10 L0,5 L-8,10 L-5,2 L-11,-3 L-3,-3Z" fill="#ffe14a" stroke="#ff7a00" stroke-width="1.5" transform="translate('+(hp[0]+9)+','+hp[1]+')"/>';bs.setAttribute('opacity',1);}else bs.setAttribute('opacity',0);
 const tg=g.querySelector('.tg');tg.textContent=fx.tag||'';}
function dhPlay(id,pl,phEl,dur){const sv=document.getElementById(id);if(!sv)return;const wr=document.getElementById(id+'w');dur=dur||5200;const S=135;
 const q=c=>sv.querySelector(c);const ge=q('.ge'),gw=q('.gw'),mk=q('.mk'),st=q('.stamp'),zan=q('.zan'),tw=q('.tw'),fl=q('.fl'),bar=wr.querySelector('.dhbar b');
 [mk,st,zan,fl].forEach(e=>e.setAttribute('opacity',0));tw.setAttribute('stroke','#8a6a3a');wr.classList.remove('shake','boom');
 const rnd=dhRand(pl.P.length*97+Math.round(pl.dir[0]*1000));
 /* まわしをつかむ時:勝つ側は早め、負ける側は半分くらい */
 const gW=.16+rnd()*.15,gL=rnd()<.5?.2+rnd()*.25:9;const gripE=pl.winE?gW:gL,gripW=pl.winE?gL:gW;
 const fxE={heat:0,burst:1,grip:0,tag:''},fxW={heat:0,burst:1,grip:0,tag:''};sv._landed=0;let tagT={E:0,W:0};
 let pt=0,last=null,lastPh=-1,hit=0;if(sv._raf)cancelAnimationFrame(sv._raf);
 const step=ts=>{const dt=last===null?0:Math.min(50,ts-last);last=ts;
  const p0=dhAt(pl,pt);const rmax=Math.max(Math.hypot(p0.E[0],p0.E[1]),Math.hypot(p0.W[0],p0.W[1]));
  let sp=1;if(rmax>.72)sp=.5;if(pt>pl.fin-.05&&pt<pl.fin+.01)sp=.25;else if(pl.T==='nage'&&pt>=pl.fin+.01)sp=.55;else if(pt>=pl.fin&&pt<pl.fin+.06)sp=.25;if(pt<.1)sp=.8;
  const ppt=pt;pt=Math.min(1,pt+dt/dur*sp);const p=dhAt(pl,pt);
  /* 調子:前に出ている側が上がり、下がっている側が下がる */
  const cx=(p.E[0]+p.W[0])/2,cy=(p.E[1]+p.W[1])/2;const pc=dhAt(pl,ppt);const mv=((cx-(pc.E[0]+pc.W[0])/2)*pl.dir[0]+(cy-(pc.E[1]+pc.W[1])/2)*pl.dir[1])*(pl.winE?1:-1);/* 東が前へ出た量 */
  fxE.heat=Math.max(0,Math.min(1,fxE.heat+mv*6-dt/9000));fxW.heat=Math.max(0,Math.min(1,fxW.heat-mv*6-dt/9000));
  if(pt>=gripE&&!fxE.grip&&p.stance==='yotsu'){fxE.grip=1;fxE.tag=pt<.5?'上手をつかんだ!':'まわしを引きつけた!';tagT.E=ts;}
  if(pt>=gripW&&!fxW.grip&&p.stance==='yotsu'){fxW.grip=1;fxW.tag='上手をつかんだ!';tagT.W=ts;}
  if(p.stance==='oshi'){if(!fxE.tag&&p.push>0){fxE.tag='突っ張り炸裂!';tagT.E=ts;}if(!fxW.tag&&p.push<0){fxW.tag='突っ張り炸裂!';tagT.W=ts;}}
  if(ts-tagT.E>1500)fxE.tag='';if(ts-tagT.W>1500)fxW.tag='';
  if(fxE.heat>.7&&!fxE.hot){fxE.hot=1;fxE.tag='勢いに乗った!';tagT.E=ts;}if(fxW.heat>.7&&!fxW.hot){fxW.hot=1;fxW.tag='勢いに乗った!';tagT.W=ts;}
  fxE.burst=p.push>=0;fxW.burst=p.push<=0;
  const lf=p.lose==='E'?fxE:fxW;if(p.spin!==undefined){lf.spin=p.spin;lf.flip=p.flip;lf.air=p.air;if(p.air>.1)lf.tag='';}
  if(p.land&&!sv._landed){sv._landed=1;wr.classList.remove('shake');void wr.offsetWidth;wr.classList.add('shake');const lo=p.lose==='E'?p.E:p.W;const du=q('.dust');du.setAttribute('transform','translate('+(lo[0]*S)+','+(lo[1]*S)+')');du.classList.remove('go');void du.getBoundingClientRect();du.classList.add('go');setTimeout(()=>wr.classList.remove('shake'),300);}
  dhPose(ge,p.E,p.W,p.stance,pt*dur/1000,p.push>0,p.lose==='E'?p.fall:0,fxE);dhPose(gw,p.W,p.E,p.stance,pt*dur/1000+.5,p.push<0,p.lose==='W'?p.fall:0,fxW);
  const adv=(cx*pl.dir[0]+cy*pl.dir[1])*(pl.winE?1:-1);bar.style.width=(50+Math.max(-48,Math.min(48,adv*55)))+'%';
  if(!hit&&pt>=.1){hit=1;wr.classList.add('shake');fl.setAttribute('cx',cx*S);fl.setAttribute('cy',cy*S);fl.setAttribute('opacity',.9);setTimeout(()=>{fl.setAttribute('opacity',0);wr.classList.remove('shake');},260);}
  const edge=rmax>.8&&pt<pl.fin+.02;tw.setAttribute('stroke',edge?'#d23a1f':'#8a6a3a');zan.setAttribute('opacity',edge?(.6+.4*Math.sin(ts/90)):0);
  if(phEl){let k=-1;pl.ph.forEach((x,i)=>{if(pt>=x[0])k=i;});if(k!==lastPh){lastPh=k;phEl.innerHTML=pl.ph.slice(0,k+1).map((x,i)=>'<li'+(i===k?' class="now"':'')+'>'+esc(x[1])+'</li>').join('');phEl.scrollTop=1e5;}}
  if(pt<1)sv._raf=requestAnimationFrame(step);
  else{const lo=p.lose==='E'?p.E:p.W;mk.setAttribute('transform','translate('+(lo[0]*S)+','+(lo[1]*S)+')');q('.mkt').textContent='ここで'+pl.how;mk.setAttribute('opacity',1);
   q('.stt').textContent=pl.k;st.setAttribute('transform','translate(0,-70) rotate(-6)');st.setAttribute('opacity',1);wr.classList.add('boom');zan.setAttribute('opacity',0);tw.setAttribute('stroke','#8a6a3a');
   if(phEl){phEl.innerHTML+='<li class="now crowd">館内がどよめく</li>';}}};
 sv._raf=requestAnimationFrame(step);}
const DH_CSS='.dhw{position:relative}.dhy{width:100%;height:auto;display:block}.dhw.shake .dhy{animation:dhs .26s}@keyframes dhs{0%,100%{transform:none}25%{transform:translate(-4px,2px)}50%{transform:translate(4px,-2px)}75%{transform:translate(-2px,1px)}}.dhw.boom .stamp{animation:dhb .5s}.dust .dd{opacity:0;transform-box:fill-box;transform-origin:center}.dust.go .dd{animation:dust 1.1s ease-out}@keyframes dust{0%{opacity:.95;transform:scale(.3)}100%{opacity:0;transform:scale(2.2)}}@keyframes dhb{0%{opacity:0}40%{opacity:1}100%{opacity:1}}'+
 '.dhbar{display:flex;align-items:center;gap:6px;font:12px sans-serif;margin-top:6px}.dhbar i{flex:1;height:10px;background:#2d4d7a;border-radius:5px;overflow:hidden;display:block}.dhbar b{display:block;height:100%;width:50%;background:#b5361f;transition:width .15s}.dhbar .be{color:#b5361f;font-weight:bold}.dhbar .bw{color:#2d4d7a;font-weight:bold}'+
 '.dhlg{display:flex;flex-wrap:wrap;gap:12px;font:12px sans-serif;color:#5a4a33;margin-top:6px}.dhlg i{display:inline-block;width:12px;height:12px;border:1px solid #8a5a00;margin-right:4px;vertical-align:-2px}';
