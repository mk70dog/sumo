/* ========== v132:ライバルと「○○時代」 ==========
 ・ライバル G.rv=[{a,b,b0,k}](相撲界全体)。番付発表のたびに関取どうしで探す(rvFind):対戦 6 回以上・星の差 2 以内・別の部屋。
   きっかけ k:'po' 優勝決定戦で当たった/'yu' 優勝を争った(優勝と次点)/'doki' 同じ場所の入門/'sek' 同じ場所で新十両/'h2h' 星の取り合い。
   起きやすさ:決定戦 0.6・優勝争い 0.35・同期と同時新十両 0.1・星の取り合い(対戦 8 回以上)0.015(場所ごと)。1 人 2 人まで。どちらかが引退するか、
   2 人とも関取でなくなって 6 場所たつと消える。
 ・因縁の一番:取組の力に +0.12×(0.5+気力/100)(両者とも。kenPrep)。勝てば気力 +3、負ければ −2、人気 +0.5(両者)。
 ・「○○時代」G.era=[{n,a,b,b0,b1}]:横綱・大関の 2 人がライバルで、直近 12 場所の幕内優勝を 2 人で 7 回以上(同じ力士の時代が続いているあいだは新しい時代はできない)、それぞれ 2 回以上。
   名前は年上の四股名の 1 字目+もう 1 人の最後の 1 字(輪島+北の湖=輪湖、柏戸+大鵬=柏鵬 の形)。
 ・実例:輪島と北の湖は毎場所のように優勝を争い「輪湖時代」、対戦は 23 勝 21 敗(Number)。隆の里と千代の富士は同じ場所で新十両、
   隆の里は「心の中では常に意識する存在だった」(Number)。大鵬と柏戸の「柏鵬時代」(SPAIA)。数字はすべて推定。 */
const RVK={po:'優勝決定戦で当たった',yu:'優勝を争った',doki:'同じ場所に入門した同期',sek:'同じ場所で新十両',h2h:'星の取り合いが続く'};
function rvOf(r){return (G.rv||[]).filter(x=>x.a===r.id||x.b===r.id);}
function rvPair(r,o){return (G.rv||[]).find(x=>(x.a===r.id&&x.b===o.id)||(x.a===o.id&&x.b===r.id))||null;}
function rvB(r,o){return rvPair(r,o)?.12*(.5+(r.mor||50)/100):0;}
function rvBout(W,L){const p=rvPair(W,L);if(!p)return;W.mor=cl(W.mor+3,0,100);L.mor=cl(L.mor-2,0,100);W.pop=(W.pop||0)+.5;L.pop=(L.pop||0)+.5;
 p.n=(p.n||0)+1;if(isPH(W.h)&&!p['f'+W.id]){p['f'+W.id]=1;inP(W.h,()=>stPush(W,'rv','ライバル '+L.n+'('+G.heya[L.h].n+')に、ライバルになって初めて勝つ'));}}
function rvFind(){G.rv=G.rv||[];G.era=G.era||[];
 // 消す
 G.rv=G.rv.filter(x=>{const a=G.R[x.a],b=G.R[x.b];if(!a||!b||a.ret||b.ret)return false;if(a.d>1&&b.d>1){x.lo=x.lo||G.bnum;return G.bnum-x.lo<6;}x.lo=0;return true;});
 const cnt=id=>G.rv.filter(x=>x.a===id||x.b===id).length;const sek=G.order.map(i=>G.R[i]).filter(r=>r&&!r.ret&&r.d<=1);
 // 直前の場所の優勝争い
 const last=G.bnum-1;const top=sek.map(r=>[r,(r.hist||[]).find(h=>h.b===last)]).filter(([r,h])=>h&&h.d===0&&(h.yu||h.jn));
 sek.forEach(r=>{if(cnt(r.id)>=2||!r.h2h)return;for(const k in r.h2h){const o=G.R[k];if(!o||o.ret||o.d>1||o.h===r.h||o.id<r.id||cnt(o.id)>=2||rvPair(r,o))continue;
   const x=r.h2h[k];if(x[0]+x[1]<6||Math.abs(x[0]-x[1])>2)continue;
   const hr=(r.hist||[]).find(h=>h.b===last),ho=(o.hist||[]).find(h=>h.b===last);
   let why='h2h',p=x[0]+x[1]>=8?.015:0;
   if(hr&&ho&&hr.d===0&&ho.d===0&&((hr.yu&&ho.jn===1)||(ho.yu&&hr.jn===1))){why='po';p=.6;}
   else if(hr&&ho&&hr.d===0&&ho.d===0&&((hr.yu&&ho.jn)||(ho.yu&&hr.jn))){why='yu';p=.35;}
   else if(r.join&&r.join===o.join&&r.join>1){why='doki';p=.1;}
   else if(r.sekD&&r.sekD===o.sekD){why='sek';p=.1;}
   if(Math.random()>=p)continue;
   G.rv.push({a:r.id,b:o.id,b0:G.bnum,k:why});
   [r,o].forEach(x=>{if(isPH(x.h)){const y=x===r?o:r;inP(x.h,()=>{stPush(x,'rv','ライバル:'+y.n+'('+G.heya[y.h].n+')。きっかけは「'+RVK[why]+'」');addNews('📣 '+x.n+'と'+y.n+'('+G.heya[y.h].n+')が、ライバルと呼ばれるようになりました('+RVK[why]+')。');});}});
   if(cnt(r.id)>=2)break;}});
 // 時代
 const Y12=(G.yusho||[]).filter(y=>y.d===0&&y.b>G.bnum-13);
 G.rv.forEach(x=>{const a=G.R[x.a],b=G.R[x.b];if(!a||!b)return;const big=r=>r.t==='Y'||r.t==='O';if(!big(a)||!big(b))return;
  const ya=Y12.filter(y=>y.n===a.n).length,yb=Y12.filter(y=>y.n===b.n).length;const e=G.era.find(z=>z.a===x.a&&z.b===x.b);
  if(e){if(ya+yb>=3)e.b1=G.bnum;return;}if(ya+yb<7||ya<2||yb<2)return;if(G.era.some(z=>(z.a===x.a||z.b===x.a||z.a===x.b||z.b===x.b)&&G.bnum-z.b1<12))return;
  const [p,q]=a.age>=b.age?[a,b]:[b,a];const pn=p.n.replace(/[0-9]/g,''),qn=q.n.replace(/[0-9]/g,'');let n=pn[0]+qn[qn.length-1];if(pn[0]===qn[qn.length-1])n=pn[0]+qn[0];
  G.era.push({n:n+'時代',a:x.a,b:x.b,an:a.n,bn:b.n,b0:G.bnum,b1:G.bnum});
  forP(()=>{addNews('🏯 '+a.n+'と'+b.n+'が優勝を分け合い、「'+n+'時代」と呼ばれるようになりました。');[a,b].forEach(r=>{if(r.h===ME())stPush(r,'rv','「'+n+'時代」と呼ばれる');});});});
 if(G.era.length>30)G.era=G.era.slice(-30);}
/* 決定戦(endBasho):ライバルとの決定戦を歩みに */
function rvPlayoff(){const last=G.bnum-1;(G.rv||[]).forEach(x=>{const a=G.R[x.a],b=G.R[x.b];if(!a||!b)return;const ha=(a.hist||[]).find(h=>h.b===last),hb=(b.hist||[]).find(h=>h.b===last);
 if(!ha||!hb||ha.d!==0||hb.d!==0)return;const W=ha.yu&&hb.jn===1?a:hb.yu&&ha.jn===1?b:null;if(!W)return;const L=W===a?b:a;
 if(isPH(W.h))inP(W.h,()=>stPush(W,'rv','ライバル '+L.n+'との優勝決定戦を制す'));if(isPH(L.h))inP(L.h,()=>stPush(L,'rv','ライバル '+W.n+'との優勝決定戦に敗れる'));});}
