/* ========== v146:2026 年九州場所の実際の成績を入れて、場所が終わったところから始める ==========
 実名モード(newGameReal)の最後に rkReplay():九州場所の番付のまま場所を開き、全 592 人の実際の勝ち・負け・休みを入れて endBasho() を通す。
 そのあと「番付発表へ進む」を押すと、ゲームの番付の決め方で 2027 年初場所の番付を作る(正式な番付は例年 12 月下旬に発表。それまでは推定の番付)。
 出典:成績=相撲データベース sumodb の番付ページ(Banzuke.aspx?b=202611、2026-11-23 読み取り。data/kyushu2026.txt)。
   優勝・決定戦=NHK・共同通信(幕内 大の里 13 勝 2 敗、若元春との決定戦に勝つ/十両 若隆景 14 勝 1 敗)、時事通信・観戦ガイド(幕下 栃武蔵・三段目 和歌ノ富士・序二段 一翔(城勝雄との決定戦に勝つ)・序ノ口 砂武蔵)。
   三賞=時事通信(殊勲 熱海富士/敢闘 金峰山・玉鷲/技能 若元春)。
 推定のもの:日ごとの星の並び(公表の形で取り込んでいないので空けておく)、休場した力士のけがの部位と重さ(休んだ日数から:全休=重い、半分以上=中くらい)。
 金星・場所後の引退は入れていない(2026-11-23 時点で引退の発表は見つからず)。 */
const RK11=__RK11__;
const RK11YU=['大の里','若隆景','栃武蔵','和歌ノ富士','一翔','砂武蔵'];
const RK11SH=[['熱海富士','殊勲賞'],['金峰山','敢闘賞'],['玉鷲','敢闘賞'],['若元春','技能賞']];
function rkReplay(){
 if(!G||!G.real||G.bnum!==6||G._rk11||G.phase!=='train')return;
 if(typeof UI!=='undefined'&&UI.mode==='two')return;/* 二人相撲は今まで通り九州場所の前から(子の参加の流れが場所前を前提にしているため) */
 const log0=G.log.slice(),ev0=G.ev.slice();
 startBasho();const B=G.B;
 G.order.forEach(id=>{const r=G.R[id],c=B.rec[id],x=RK11[r.n];if(!x)return;c.w=x[0];c.l=x[1];c.ab=x[2];c.ky=x[2]>0;c.res=Array(15).fill(null);});
 B.day=15;B.cur=[];B.next=[];
 G._rkYu=RK11YU;G._rkSh=RK11SH;
 try{endBasho();}finally{delete G._rkYu;delete G._rkSh;}
 G._rk11=1;
 // 休場した力士:けがが残っている(部位は四股名から決まる推定。重さは休んだ日数から)
 G.order.forEach(id=>{const r=G.R[id],x=RK11[r.n];if(!x||!(x[2]>0)||r.ret)return;const full=r.d<=1?15:7;
  const s=x[2]>=full?3:x[2]>=full/2?2:1;let hs=0;for(const c of r.n+'202611')hs=(hs*31+c.charCodeAt(0))|0;const u=hhR(hs,3)*100;let acc=0,p=PARTS[0];
  for(let i=0;i<PARTS.length;i++){acc+=[30,22,16,18,14][i];if(u<acc){p=PARTS[i];break;}}
  const wk=s===1?2:s===2?5:9;if(!r.inj)r.inj={p:p,s:s,wk:wk,t:wk,est:1};r.ij=r.ij||[];r.ij.push({b:G.bnum,ym:202611,p:p,s:s,est:1});});
 G.log=log0;G.ev=ev0.concat(G.ev.filter(e=>!ev0.includes(e)));
 const y=G.last&&G.last.yu||[];
 addNews('2026 年九州場所は、実際の成績を入れて終えたところから始めます(全員の勝ち負け・休場・優勝・三賞が実際のとおり)。幕内は'+(y[0]?y[0].n:'')+'が若元春との優勝決定戦を制して優勝。');
 addNews('「番付発表へ進む」を押すと、ゲームの番付の決め方で 2027 年初場所の番付ができます(正式な番付は例年 12 月下旬に発表。それまでは推定の番付です)。');
}
