/* --- 上から見た土俵(立ち合いから決着までを動かす)  kaiga13 --- */
/* 座標:土俵の中心 (0,0)、俵の内側が半径 1。東 = 左(-x)、西 = 右(+x)、正面 = 下(+y)。 */
function dhType(k){k=k||'';if(/うっちゃり|打っ棄り/.test(k))return 'uchari';if(/投げ|捻り|ひねり|掬い|すくい|網打ち|櫓|首投げ|小股/.test(k))return 'nage';if(/はたき|叩き|引き落とし|引っ掛け|肩透かし|突き落とし|とったり|叩き込み|はたき込み|送り/.test(k))return k.indexOf('送り')>=0?'okuri':'hiki';if(/突き出し|突き倒し|押し出し|押し倒し/.test(k))return 'oshi';if(/倒れ|浴びせ/.test(k))return 'yoritaoshi';return 'yori';}
function dhRand(seed){let s=seed>>>0||1;return ()=>{s=(s*1103515245+12345)>>>0;return (s>>>8)/16777216;};}
/* 戻り値:{E:[[t,x,y,fall]], W:[...], ph:[[t,文]], out:[x,y], how:'出た'|'倒れた'} winE=東が勝ち */
function dhPlan(k,winE,seed,nE,nW){const rnd=dhRand(seed),T=dhType(k);const sg=winE?1:-1;/* 勝った側が押す向き(東勝ちなら +x へ) */
 const ang=(rnd()-.5)*1.4;/* 寄っていく方角のぶれ */ const dir=[Math.cos(ang)*sg,Math.sin(ang)];
 const P=[];let c=[0,0];const add=(t,cx,cy,d,ln)=>{P.push([t,cx,cy,d,ln]);};
 const WN=winE?nE:nW,LN=winE?nW:nE;const ph=[[0,'仕切り'],[.12,'立ち合い']];
 add(0,0,0,.24,0);add(.12,0,0,.075,0);
 /* 攻防:中央付近でもみ合う */
 let a1=(rnd()-.5)*.5;c=[dir[0]*.18+(rnd()-.5)*.1,dir[1]*.18+(rnd()-.5)*.25];add(.3,c[0],c[1],.075,0);
 const zan=rnd()<.45&&T!=='okuri';/* 土俵際で一度残す */
 if(zan){const e=[dir[0]*.72,dir[1]*.72];add(.46,e[0],e[1],.075,0);ph.push([.36,WN+'が前へ出る']);ph.push([.46,LN+'が土俵際で残す']);c=[dir[0]*.25-dir[1]*.2,dir[1]*.25+dir[0]*.2];add(.6,c[0],c[1],.075,0);ph.push([.56,'中央へ押し戻す']);}
 else{c=[c[0]-dir[1]*.15,c[1]+dir[0]*.15];add(.5,c[0],c[1],.075,0);ph.push([.32,'もみ合う']);}
 /* 決着 */
 let out,how='出た';const last=P[P.length-1];const t0=last[0];
 const pairAt=(t,cx,cy,d,fall,fx,fy)=>P.push([t,cx,cy,d,0,fall,fx,fy]);
 if(T==='yori'||T==='oshi'||T==='yoritaoshi'||T==='okuri'){const sp=T==='oshi'?.32:.08;
  const e=[dir[0]*.93,dir[1]*.93];add(t0+(1-t0)*.75,e[0],e[1],sp,0);out=[dir[0]*1.18,dir[1]*1.18];
  ph.push([t0+.05,T==='oshi'?WN+'が一気に押す':T==='okuri'?WN+'が後ろに回る':WN+'が寄って出る']);ph.push([.95,k+'。'+WN+'の勝ち']);
  if(T==='yoritaoshi')how='倒れた';}
 else if(T==='nage'){const piv=[last[1],last[2]];add(t0+(1-t0)*.4,piv[0],piv[1],.075,0);ph.push([t0+.05,WN+'が上手を引いて振る']);
  const ra=Math.atan2(-dir[1],-dir[0])+(rnd()<.5?1:-1)*2.1;out=[piv[0]+Math.cos(ra)*.32,piv[1]+Math.sin(ra)*.32];how='倒れた';ph.push([.95,k+'。'+WN+'の勝ち']);}
 else if(T==='hiki'){ph.push([t0+.05,WN+'が引いて'+LN+'が前に落ちる']);const piv=[last[1],last[2]];add(t0+(1-t0)*.4,piv[0],piv[1],.075,0);
  out=[piv[0]-dir[0]*.42+dir[1]*.12,piv[1]-dir[1]*.42-dir[0]*.12];how='落ちた';ph.push([.95,k+'。'+WN+'の勝ち']);}
 else if(T==='uchari'){const e=[-dir[0]*.92,-dir[1]*.92];add(t0+(1-t0)*.6,e[0],e[1],.075,0);ph.push([t0+.03,LN+'が寄って出る']);ph.push([t0+(1-t0)*.62,WN+'が土俵際で体を入れ替える']);
  out=[-dir[0]*.95-dir[1]*.32,-dir[1]*.95+dir[0]*.32];out=[out[0]*1.15,out[1]*1.15];ph.push([.95,k+'。'+WN+'の大逆転']);}
 return {P,out,how,T,winE,dir,ph};}
/* t(0〜1)での 2 人の位置 */
function dhPos(pl,t){const P=pl.P;let i=0;while(i<P.length-1&&P[i+1][0]<=t)i++;const a=P[i],b=P[Math.min(i+1,P.length-1)];const u=b[0]>a[0]?Math.min(1,Math.max(0,(t-a[0])/(b[0]-a[0]))):1;const e=u*u*(3-2*u);
 const cx=a[1]+(b[1]-a[1])*e,cy=a[2]+(b[2]-a[2])*e,d=a[3]+(b[3]-a[3])*e;
 const lastT=P[P.length-1][0];const dx=pl.dir[0],dy=pl.dir[1];
 let W=[cx-dx*d,cy-dy*d],L=[cx+dx*d,cy+dy*d];/* 勝った側は押す向きの後ろ、負けた側は前 */
 if(t>lastT){const u2=Math.min(1,(t-lastT)/(1-lastT));const e2=u2*u2*(3-2*u2);const fw=W,fl=L;L=[fl[0]+(pl.out[0]-fl[0])*e2,fl[1]+(pl.out[1]-fl[1])*e2];
  if(pl.T==='hiki')W=[fw[0]+dy*.12*e2,fw[1]-dx*.12*e2];else if(pl.T!=='nage')W=[fw[0]+(pl.out[0]-fw[0])*.35*e2,fw[1]+(pl.out[1]-fw[1])*.35*e2];}
 return pl.winE?{E:W,Wst:L}:{E:L,Wst:W};}
function dhSVG(id,nE,nW){return '<svg class="dhy" id="'+id+'" viewBox="-150 -150 300 300"><rect x="-150" y="-150" width="300" height="300" fill="#e8dcc0" rx="10"/><circle r="128" fill="#d6c093"/><circle r="112" fill="#dcc79c" stroke="#8a6a3a" stroke-width="7"/>'+
 '<line x1="-12" y1="-12" x2="-12" y2="12" stroke="#fff" stroke-width="3"/><line x1="12" y1="-12" x2="12" y2="12" stroke="#fff" stroke-width="3"/>'+
 '<text y="146" text-anchor="middle" font-size="12" fill="#5a4a33">正面</text><text y="-138" text-anchor="middle" font-size="12" fill="#5a4a33">向正面</text><text x="-146" y="4" font-size="12" fill="#5a4a33">東</text><text x="134" y="4" font-size="12" fill="#5a4a33">西</text>'+
 '<polyline class="pe" fill="none" stroke="#b5361f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/><polyline class="pw" fill="none" stroke="#2d4d7a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/>'+
 '<g class="mk" opacity="0"><circle r="16" fill="none" stroke="#b5361f" stroke-width="3"/><text class="mkt" y="30" text-anchor="middle" font-size="12" font-weight="bold" fill="#b5361f"></text></g>'+
 '<g class="ge"><circle r="11" fill="#b5361f"/><text y="4" text-anchor="middle" font-size="11" fill="#fff">'+esc((nE||'東').slice(0,1))+'</text></g><g class="gw"><circle r="11" fill="#2d4d7a"/><text y="4" text-anchor="middle" font-size="11" fill="#fff">'+esc((nW||'西').slice(0,1))+'</text></g></svg>';}
function dhPlay(id,pl,phEl,dur){const sv=document.getElementById(id);if(!sv)return;dur=dur||4200;const S=112;const pe=sv.querySelector('.pe'),pw=sv.querySelector('.pw'),ge=sv.querySelector('.ge'),gw=sv.querySelector('.gw'),mk=sv.querySelector('.mk');
 const tr={E:[],W:[]};mk.setAttribute('opacity',0);let t0=null,lastPh=-1;if(sv._raf)cancelAnimationFrame(sv._raf);
 const step=ts=>{if(t0===null)t0=ts;const t=Math.min(1,(ts-t0)/dur);const p=dhPos(pl,t);const e=[p.E[0]*S,p.E[1]*S],w=[p.Wst[0]*S,p.Wst[1]*S];
  tr.E.push(e[0].toFixed(1)+','+e[1].toFixed(1));tr.W.push(w[0].toFixed(1)+','+w[1].toFixed(1));pe.setAttribute('points',tr.E.join(' '));pw.setAttribute('points',tr.W.join(' '));
  ge.setAttribute('transform','translate('+e[0]+','+e[1]+')');gw.setAttribute('transform','translate('+w[0]+','+w[1]+')');
  if(phEl){let k=-1;pl.ph.forEach((x,i)=>{if(t>=x[0])k=i;});if(k!==lastPh){lastPh=k;phEl.innerHTML=pl.ph.slice(0,k+1).map((x,i)=>'<li'+(i===k?' class="now"':'')+'>'+esc(x[1])+'</li>').join('');}}
  if(t<1)sv._raf=requestAnimationFrame(step);else{const lo=pl.winE?w:e;mk.setAttribute('transform','translate('+lo[0]+','+lo[1]+')');const mt=sv.querySelector('.mkt');mt.textContent='ここで'+pl.how;mt.setAttribute('text-anchor',lo[0]>50?'end':lo[0]<-50?'start':'middle');mt.setAttribute('x',lo[0]>50?14:lo[0]<-50?-14:0);mt.setAttribute('y',lo[1]>60?-22:30);mk.setAttribute('opacity',1);}};
 sv._raf=requestAnimationFrame(step);}
