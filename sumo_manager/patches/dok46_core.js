/* 部屋付き親方として独立する(v43)。いったん元の部屋で始めてから、選んだ内弟子と親方だけを新しい部屋に移す。 */
const DOKMON={'横綱':1500,'大関':1000,'関脇':500,'小結':500};
function newGameDok(en,wsN,oyT){
 const T=TOSHI.find(t=>t[0]===en&&t[3]!==1);if(!T)return newGameReal(REALH[0][0]);
 const P=T[2];newGameReal(P,oyT);
 const me0=G.heya[0];const H=REALH.find(x=>x[0]===P);
 const iP=G.heya.length;G.heya.push({n:P,o2:me0.o2,player:false,q:R(.98,1.1),hard:Math.random()<.3,ic:me0.ic,oa:me0.age,gen:1,loc:me0.loc,est:me0.est,hist:me0.hist});
 G.hs.tot.push(0);G.hs.yr.push(0);
 const keep=new Set(wsN);G.order.forEach(id=>{const r=G.R[id];if(r.h===0&&!keep.has(r.n)){r.h=iP;}});
 const top=Object.keys(DOKMON).find(k=>T[5].indexOf(k)===0);
 me0.n=en;me0.o=en+'(元・'+T[4]+')';me0.o2=T[4];me0.age=realAge(T[6]);me0.gen=1;me0.est=2026;me0.hist='2026 年、'+P+'部屋から独立して創設。';
 me0.oy=Object.assign({},me0.oy);{const b0=H&&H[4]?(H[4]==='Y'?1.5:.8):0,b1=top==='横綱'?1.5:top==='大関'?.8:0;for(const k in me0.oy)me0.oy[k]=Math.round(me0.oy[k]-b0+b1);}
 // 部屋付き親方は元の部屋に残る。独立する親方の記録を新しい部屋の師匠にする
 G.staff.filter(x=>x.role==='co').forEach(x=>{G.myoL=(G.myoL||[]).filter(m=>m.h!==x.sid);});G.staff=G.staff.filter(x=>x.role!=='co');
 if(G.toshi){G.toshi.forEach(t=>{if(t.heya===P&&t.shi&&t.gen0)delete t.gen0;});const t=G.toshi.find(x=>x.n===en);if(t){t.heya=en;t.shi=1;t.gen0=1;G.post=postLv(t.post);G.mePost=t.post;}}
 if(G.myo){if(G.myo[P])G.myo[P].st='ai';if(G.myo[en])G.myo[en].st='own';}
 const o=own();const sek=o.filter(r=>r.d<=1).length;
 G.fac={keiko:1,iryo:1,shoku:1,shuku:2};G.capB=Math.max(0,o.length+3-(4+3*G.fac.shuku));G.bld={k:'rent'};
 G.money=1000+(top?DOKMON[top]:0);G.sup=(top==='横綱'?600:top==='大関'?400:top?200:100)+o.length*12+sek*60;G.supC=Math.round(2+o.length/3+sek*4);G.rep=cl(15+sek*5,0,90);
 G.supFee={i:2.1,c:20,t:''};G.dok={from:P,b:G.bnum};
 G.log=[];addNews(bname(G.bnum)+'の番付から始めます。'+en+'親方(元'+T[4]+')が'+P+'部屋から独立し、'+en+'部屋を興しました。内弟子 '+o.length+' 人(関取 '+sek+' 人)、資金 '+man(G.money)+'(自己資金・推定)、建物は借りもの。');
 addNews('力士・部屋・親方・一門は 2026 年の実在のものです。独立はゲーム内の架空の出来事です。');
}
