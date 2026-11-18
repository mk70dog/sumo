/* v60 部屋を支える人:後援会長・タニマチ・かかりつけ医・師匠の家族(名前・会社・家族はすべて架空。数字は推定) */
const KAIJOB=['地元の建設会社 会長','老舗旅館の主人','商工会議所 会頭','酒造会社 社長','元市議会議長','地方銀行 元頭取'];
const TMJOB=[['運送会社 会長','m'],['不動産会社 社長','m'],['料亭の女将','f'],['病院の院長','m'],['食品会社 会長','m'],['IT企業 社長','m'],['老舗呉服店 主人','m'],['焼肉店チェーン 社長','m']];
function spName(g){return g==='f'?pick(FAM)+' '+pick(OKN):personName(0);}
function mkKai(){return {n:personName(0),job:pick(KAIJOB),age:RI(58,76),face:RI(6,16),cl:RI(55,80)};}
function mkTm(){const j=pick(TMJOB);return {n:spName(j[1]),job:j[0],cl:RI(35,75),fut:RI(1,3),enk:Math.random()<.35?1:0,b:G.bnum};}
function mkFam(){const a=me().age||45;const L=[];const n=wpick([[0,20],[1,35],[2,35],[3,10]]);const rel=['長男','次男','長女','次女'];let sons=0,dau=0;
 for(let i=0;i<n;i++){const boy=Math.random()<.55;const age=Math.max(0,Math.round(a-RI(26,40)-i*RI(1,4)));L.push({rel:boy?(sons++?'次男':'長男'):(dau++?'次女':'長女'),boy:boy?1:0,age:age,sumo:boy&&Math.random()<.35?1:0});}
 return {kids:L};}
function spInit(){if(G.sp)return G.sp;const sek=own().filter(r=>r.d<=1).length;const n=2+(sek>=1?1:0)+(G.sup>=300?1:0);
 G.sp={kai:mkKai(),tm:[],fam:mkFam(),docN:pick(['すみだ整形クリニック','両国スポーツ整形外科','かめいど整形外科','錦糸町メディカルクリニック'])};for(let i=0;i<n;i++)G.sp.tm.push(mkTm());return G.sp;}
function tmBest(c){return (spInit().tm||[]).filter(t=>t.cl>=(c||50)).sort((a,b)=>b.cl*b.fut-a.cl*a.fut)[0]||null;}
/* 場所ごと:親しさの上下・離れる・新しく付く・後援会長の高齢化・家族の年 */
function spBasho(sum){const P=spInit();const o=own();const sek=o.filter(r=>r.d<=1);
 let d=sek.reduce((t,r)=>{const h=r.hist&&r.hist[r.hist.length-1];if(!h||h.b!==G.bnum)return t;return t+(h.w>h.l?1:-.7);},0);
 if((sum&&sum.yu||[]).some(y=>y.h===0&&y.d<=1))d+=4;
 const scan=G.ev.some(e=>e.k==='scand');if(scan)d-=6;if(!sek.length)d-=1.2;
 P.tm.forEach(t=>{t.cl=cl(t.cl+d*.8+randn()*1.5,0,100);});
 P.tm=P.tm.filter(t=>{if(t.cl<12){addNews('タニマチの'+t.n+'さん('+t.job+')が、部屋の後援から離れました。');return false;}return true;});
 if(P.tm.length<4&&Math.random()<.05+sek.length*.04+(G.rep>60?.04:0)){const t=mkTm();P.tm.push(t);addNews(t.job+'の'+t.n+'さんが、部屋のタニマチになりました。');}
 const K=P.kai;if(K){K.age+=1/6;K.cl=cl(K.cl+d*.4+randn(),0,100);if((K.age>=72&&Math.random()<.04)||K.age>=82||K.cl<15){if(!G.ev.some(e=>e.k==='kaicho'))G.ev.push({k:'kaicho',old:K.n});}}
 P.fam.kids.forEach(k=>{const a0=Math.floor(k.age);k.age+=1/6;
  if(k.boy&&k.sumo&&a0<15&&k.age>=15&&!k.done){k.done=1;G.ev.push({k:'shison',kid:{f:'師匠の'+k.rel,br:'師匠の子',p:Math.round(R(9,14)*10)/10,sty:undefined,gt:RI(0,3),per:pick(PER)},rel:k.rel});}
  if(k.boy&&!k.sumo&&!k.help&&a0<23&&k.age>=23&&Math.random()<.35&&G.staff.filter(s=>s.role==='sc').length<ROLE.sc.max){k.help=1;const s=mkStaff('sc',9);s.n='師匠の'+k.rel;s.sal=Math.round(s.sal*.6);G.staff.push(s);addNews('師匠の'+k.rel+'が、マネージャーとして部屋の仕事を手伝い始めました。');}
  if(!k.boy&&!k.help&&a0<24&&k.age>=24&&Math.random()<.25){k.help=1;addNews('師匠の'+k.rel+'が、おかみさんを手伝って部屋の事務と後援会の連絡をするようになりました。');}});
 // 後援会長の顔の広さ:後援会員と法人
 if(K){G.sup+=Math.round((K.face-10)*.5*(K.cl/70));if(K.face>=14&&Math.random()<.08)G.supC=(G.supC||0)+1;}
}
/* タニマチの紹介で新弟子の情報 */
function tmInfo(add,spring){(spInit().tm||[]).forEach(t=>{if(t.cl>=50&&Math.random()<.006*t.fut*spring)add(mkProspect(RI(0,5)),'タニマチ('+t.n+'さん)の紹介');});}
/* 祝賀会のタニマチのご祝儀(万円) */
function tmShugi(){return Math.round((spInit().tm||[]).reduce((s,t)=>s+t.fut*t.cl/100*12,0));}
/* 宴席の誘い */
function enkaiInit(e){const t=(spInit().tm||[]).filter(x=>x.enk&&x.cl>=40);const sk=own().filter(r=>r.d<=1&&!r.inj);if(!t.length||!sk.length)return false;e.tn=pick(t).n;e.rid=pick(sk).id;}
