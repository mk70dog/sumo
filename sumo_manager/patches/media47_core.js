/* メディア情報(v44)。出どころごとに確かさが違い、うわさはあとで当たり外れがわかる。 */
const MSRC={kyo:['協会の発表',5,'#2c3e5c',1],ip:['相撲日報(一般紙)',4,'#3f6b4a',.85],rep:['仲の良い記者',4,'#1f5f7a',.8],loc:['地元の事情通',3,'#5a6b2a',.7],sp:['スポーツ角界(スポーツ紙)',3,'#8a5a1a',.65],sh:['週刊土俵裏(週刊誌)',2,'#6b2e6b',.3],net:['ネットのうわさ',1,'#7d7365',.2]};
function mInit(){if(!G.media)G.media={L:[],st:{},n:1,seen:0};return G.media;}
function mAdd(src,t,chk,sub){const M=mInit();M.L.unshift({id:M.n++,s:src,b:G.bnum,wk:G.phase==='train'?G.wk:0,t:t,sub:sub||'',chk:chk||null,res:chk?null:'fix'});if(M.L.length>80)M.L.length=80;}
function mTrue(s){return Math.random()<MSRC[s][3];}
function mAI(){return G.order.map(id=>G.R[id]).filter(r=>r&&!r.ret&&r.h!==0&&G.heya[r.h]);}
function mHN(r){return G.heya[r.h].n+'部屋';}
function mRes(it,hit,rd){if(it.res)return;it.res=hit?'hit':'miss';it.rd=rd||'';const M=mInit();const a=M.st[it.s]||[0,0];a[1]++;if(hit)a[0]++;M.st[it.s]=a;}
function mWeek(){if(!G||G.phase!=='train'||Math.random()>.6)return;const g=wpick([['inj',3],['ret',2],['young',2],['amaP',2],['amaT',2]]);const AI=mAI();
 if(g==='inj'){const S=pick(['ip','rep','sp','sh','net']);const sek=AI.filter(r=>r.d<=1);const wl=Math.max(0,7-(G.wk||1));const inj=sek.filter(r=>r.inj&&(r.inj.s>=3||r.inj.wk-wl>=4)),ok=sek.filter(r=>!r.inj);const tr=mTrue(S);const r=tr?(inj.length?pick(inj):null):(ok.length?pick(ok):null);if(!r)return;if(tr)r.mKyu=G.bnum;
  mAdd(S,r.n+'('+mHN(r)+'・'+r.rkS+')、'+(r.inj?r.inj.p:pick(['右ひざ','左足首','腰','右肩','左ひじ']))+'のけがで次の場所は休場の見込み。',{k:'kyu',id:r.id,b:G.bnum});}
 else if(g==='ret'){const S=pick(['rep','sp','sh','net']);const old=AI.filter(r=>r.age>=31&&!r.mRet).sort((x,y)=>y.age-x.age).slice(0,6),mid=AI.filter(r=>r.age>=25&&r.age<30&&r.d<=1);const tr=mTrue(S);const r=tr?(old.length?pick(old):null):(mid.length?pick(mid):null);if(!r)return;if(tr)r.mRet=G.bnum+R(0,2);
  mAdd(S,r.n+'('+mHN(r)+'・'+Math.floor(r.age)+' 歳)、近く引退か。周囲に「体が限界」ともらす。',{k:'ret',id:r.id,due:G.bnum+4},'答え合わせは 4 場所のうち');}
 else if(g==='young'){const S=pick(['sp','loc','rep','net']);const c=AI.filter(r=>r.age<=21&&r.d>=2);const good=c.filter(r=>potOf(r)>=15).sort((x,y)=>potOf(y)-potOf(x)).slice(0,4),bad=c.filter(r=>potOf(r)<11.5);const r=mTrue(S)&&good.length?pick(good):(bad.length?pick(bad):null);if(!r)return;
  mAdd(S,mHN(r)+'の'+r.n+'('+Math.floor(r.age)+' 歳・'+r.rkS+')、稽古場で兄弟子を圧倒。将来の関取候補との声。',{k:'sek',id:r.id,due:G.bnum+24},'答え合わせは 4 年のうち(関取になれたか)');}
 else if(g==='amaP'&&G.ama){const S=pick(['loc','sp','ip','net']);const P=G.ama.filter(a=>(a.kind==='高'&&a.yr>=3)||(a.kind==='大'&&a.yr>=4));if(!P.length)return;
  const pf=x=>sig((x.T-(x.kind==='高'?6.2:8))*1.2+(amaQual(x)?1:0));const tr=mTrue(S);const P2=tr?P.filter(x=>{const q=pf(x);return q>.8||q<.2;}):P;if(!P2.length)return;const b=pick(P2);const pro=pf(b);const lk=pro>=.5?1:0;const c=tr?lk:1-lk;
  const a=b;mAdd(S,schLabel(a.sch)+'の'+a.n+'('+a.age+' 歳)、卒業後は'+(c?'大相撲入りへ。':(a.kind==='高'?'大学に進んで相撲を続ける見込み。':'角界には進まない見込み。')),{k:'ama',aid:a.id,c:c},'答え合わせは卒業のとき');}
 else if(g==='amaT'&&G.ama){const S=pick(['loc','loc','sp','net']);const P=G.ama.filter(a=>a.kind!=='社'&&a.yr<=2).sort((x,y)=>y.T-x.T);if(P.length<10)return;const a=mTrue(S)?pick(P.slice(0,3)):pick(P.slice(Math.floor(P.length/2)));
  mAdd(S,(S==='loc'?'近所の':'')+schLabel(a.sch)+'の'+a.n+'('+a.age+' 歳)は伸びる。全国大会でも上位に入る力がある。',{k:'amaT',aid:a.id,n:a.n,due:G.bnum+6},'答え合わせは 1 年のうち(全国 8 強以上)');}}
function mCycle(old){if(!G.media&&!G.real)return;mInit();
 const nj=[],nm=[];G.order.forEach(id=>{const r=G.R[id],o=old[id];if(!r||r.ret||!o)return;if(o.d>=2&&r.d===1)nj.push(r);if(o.d>=1&&r.d===0)nm.push(r);});
 const L=x=>x.slice(0,5).map(r=>r.n+'('+G.heya[r.h].n+')').join('・')+(x.length>5?' ほか':'');
 if(nj.length||nm.length)mAdd('kyo',bname(G.bnum)+'の番付発表。'+(nm.length?'幕内に上がるのは '+L(nm)+'。':'')+(nj.length?'十両に上がるのは '+L(nj)+'。':''));
 G.media.L.forEach(it=>{if(it.res||!it.chk)return;const c=it.chk,r=G.R[c.id];
  if(c.k==='kyu'&&G.bnum>c.b){const h=r&&r.hist?r.hist.find(x=>x.b===c.b):null;if(h)mRes(it,h.ab>0,h.ab>0?'休場した':'出場した('+h.w+'勝'+h.l+'敗)');else mRes(it,!r||r.ret,!r||r.ret?'引退した':'出場した');}
  else if(c.k==='ret'){if(!r||r.ret)mRes(it,true,'引退した');else if(G.bnum>=c.due)mRes(it,false,'まだ現役');}
  else if(c.k==='sek'){if(r&&r.d<=1)mRes(it,true,'関取になった');else if(!r||r.ret)mRes(it,false,'関取になれずに引退');else if(G.bnum>=c.due)mRes(it,false,'4 年で関取になれず');}
  else if(c.k==='amaT'&&G.bnum>=c.due)mRes(it,false,'全国の上位に入れず');});}
function mAmaRec(sc){if(!G.media)return;sc.forEach(([a],i)=>{if(i>=8)return;G.media.L.forEach(it=>{if(!it.res&&it.chk&&it.chk.k==='amaT'&&(it.chk.aid===a.id||it.chk.n===a.n))mRes(it,true,'全国大会で'+(i+1)+'位');});});}
function mAmaFate(a,k){if(!G.media)return;const go=k==='pros'||k==='heya';G.media.L.forEach(it=>{if(!it.res&&it.chk&&it.chk.k==='ama'&&it.chk.aid===a.id)mRes(it,(it.chk.c===1)===go,go?'大相撲に入門':k==='uni'?'大学に進学':'角界には進まず');});}
