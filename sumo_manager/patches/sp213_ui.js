/* v210 後援会・タニマチ・出稽古・巡業を本物らしく(数字はすべて推定)。
   ・化粧まわしは後援者・タニマチ・出身地・出身校から贈られることが多い → 新入幕・新三役のときの「二本目の化粧まわし」
   ・後援会長やタニマチの頼みごと(地元の祭り・会社の催し・子ども相撲教室・病院の慰問)
   ・タニマチ同士の張り合い、後援会の親睦ゴルフ(年 1 回)
   ・出稽古先とのつきあい(通うほど深まり、相手の部屋からも来る)
   ・巡業で地元の近くを回ると大きな声援(序二段でも沸く)。けがで休む関取は診断書を出して休む */
(function(){
const nid=()=>Math.random().toString(36).slice(2,8);
const tms=()=>((typeof spInit==='function'?spInit():{}).tm||[]);
const kai=()=>(typeof spInit==='function'?spInit().kai:null);
const sekiOK=()=>own().filter(r=>r.d<=1&&!r.inj);
const pref=x=>String(x||'').replace(/(県|府|都)$/,'');
/* ---------- 出来事 ---------- */
Object.assign(EVT,{
 kesho2:{t:'二本目の化粧まわし',
  d:e=>{const r=G.R[e.rid];return r?r.n+'の'+(e.why==='S'?'新三役':'新入幕')+'を祝って、化粧まわしを贈りたいという申し出が届きました。どこから受けますか(ほかは丁寧にお礼を伝えます)。':'';},
  c:e=>(e.opt||[]).map(o=>o.t),
  ap:(e,i)=>{const r=G.R[e.rid];const o=(e.opt||[])[i];if(!r||!o)return '';r.kesho2=(r.kesho2||0)+1;r.pop=cl((r.pop||20)+3,0,100);
   if(o.k==='tm'){const t=tms().find(x=>x.n===o.n);if(t){t.cl=cl(t.cl+8,0,100);if(!t.enk&&Math.random()<.4)t.enk=1;}return 'タニマチの'+o.n+'さんから化粧まわしが贈られました。親しさが深まりましたが、宴席の誘いも増えそうです。';}
   if(o.k==='home'){G.sup+=8;r.pop=cl((r.pop||20)+4,0,100);return r.home+'の後援者一同から化粧まわしが贈られました。地元の応援がいっそう熱くなりました(後援会 +8 人)。';}
   if(o.k==='sch'){G.rel=G.rel||{};G.rel[o.n]=cl((G.rel[o.n]||0)+8,0,100);return '母校の'+schLabel(o.n)+'から化粧まわしが贈られました。学校との関係が深まりました(+8)。';}
   const K=kai();if(K)K.cl=cl(K.cl+6,0,100);G.sup+=4;return '後援会一同から化粧まわしが贈られました。後援会長も喜んでいます。';}},
 tanomi:{t:'後援者からの頼みごと',
  d:e=>{const r=G.R[e.rid];return e.who+'から「'+e.what+'に、'+(r?r.n:'関取')+'に来てもらえないか」と頼まれました。受けると関係が深まりますが、その週は稽古が手薄になります。';},
  c:e=>['関取を行かせる','若い衆を代わりに行かせる','丁寧に断る'],
  ap:(e,i)=>{const r=G.R[e.rid];const t=e.tn?tms().find(x=>x.n===e.tn):null;const K=kai();const up=v=>{if(t)t.cl=cl(t.cl+v,0,100);else if(K)K.cl=cl(K.cl+v,0,100);};
   if(i===0){up(10);if(r){r.fat=cl(r.fat+5,0,100);r.cond=cl(r.cond-3,0,100);r.pop=cl((r.pop||20)+2,0,100);}G.sup+=e.ji?6:3;if(e.ji)G.rep=cl(G.rep+1,0,100);
    return (r?r.n:'関取')+'が'+e.what+'に出ました。'+(e.ji?'訪ねた先で大変喜ばれ、部屋の評判も上がりました。':'たいへん喜ばれました。')+'少し疲れが残っています。';}
   if(i===1){up(3);const y=own().filter(x=>x.d>=2).sort((a,b)=>a.pos-b.pos)[0];if(y)y.mor=cl(y.mor+3,0,100);return (y?y.n:'若い衆')+'が代わりに行きました。少し物足りなさそうでしたが、感謝されました。';}
   up(-10);return '丁寧にお断りしました。少し残念そうでした。';}},
 tmriv:{t:'タニマチ同士の張り合い',
  d:e=>'タニマチの'+e.a+'さんと'+e.b+'さんが、どちらが部屋を支えているかで張り合っています。祝賀会の席順でもめそうです。',
  c:e=>[e.a+'さんを立てる',e.b+'さんを立てる','親方が二人を招いて席を設ける(20 万円)'],
  ap:(e,i)=>{const A=tms().find(x=>x.n===e.a),B=tms().find(x=>x.n===e.b);if(!A||!B)return '';
   if(i===0){A.cl=cl(A.cl+8,0,100);B.cl=cl(B.cl-15,0,100);return A.n+'さんは満足そうですが、'+B.n+'さんは少し距離を置くようになりました。';}
   if(i===1){B.cl=cl(B.cl+8,0,100);A.cl=cl(A.cl-15,0,100);return B.n+'さんは満足そうですが、'+A.n+'さんは少し距離を置くようになりました。';}
   G.money-=20;A.cl=cl(A.cl+3,0,100);B.cl=cl(B.cl+3,0,100);G.tmp.away=(G.tmp.away||0)+1;return '親方が二人を招いて席を設け、どちらの顔も立てました。今週は親方が部屋を空けます。';}},
 golf:{t:'後援会の親睦ゴルフ',
  d:()=>'夏の後援会の親睦ゴルフ(年 1 回)のお誘いです。会員と顔を合わせる場で、後援会長も楽しみにしています。',
  c:()=>['親方と関取で出る(費用 15 万円)','親方だけ出る(費用 5 万円)','欠席する'],
  ap:(e,i)=>{const K=kai();const sk=own().filter(r=>r.d<=1);
   if(i===0){G.money-=15;if(K)K.cl=cl(K.cl+6,0,100);const n=6+sk.length*3;G.sup+=n;if(Math.random()<.35)G.supC=(G.supC||0)+1;sk.forEach(r=>{r.fat=cl(r.fat+3,0,100);r.mor=cl(r.mor+2,0,100);});tms().forEach(t=>t.cl=cl(t.cl+2,0,100));return '和やかな会になり、後援会員が '+n+' 人増えました。関取は少し日に焼けました。';}
   if(i===1){G.money-=5;if(K)K.cl=cl(K.cl+3,0,100);G.sup+=3;return '親方が出て、会員と親しく話しました(後援会 +3 人)。';}
   if(K)K.cl=cl(K.cl-5,0,100);return '欠席しました。後援会長は少し寂しそうでした。';}}
});
const ASK=[['地元の夏祭りの土俵入り',0],['会社の創立記念の催し',0],['子ども相撲教室',1],['病院への慰問',1],['商店街の餅つき',0],['ふるさとの小学校の訪問',1]];
/* 場所が終わったあとに出来事を足す */
const v7=v7Basho;v7Basho=function(sum){const r0=v7.apply(this,arguments);try{forP(()=>{if(!isPH(ME()))return;spAfter();});}catch(e){console.error(e);}return r0;};
function spAfter(){const T=tms(),K=kai();const sk=sekiOK();
 /* 頼みごと(場所ごと 3 割ほど) */
 if(sk.length&&!G.ev.some(e=>e.k==='tanomi')&&Math.random()<.3){const a=pick(ASK);const t=T.filter(x=>x.cl>=30);const useT=t.length&&Math.random()<.6;const tt=useT?pick(t):null;
  G.ev.push({k:'tanomi',id:nid(),rid:pick(sk).id,what:a[0],ji:a[1],tn:tt?tt.n:null,who:tt?'タニマチの'+tt.n+'さん('+tt.job+')':(K?'後援会長の'+K.n+'さん':'後援会')});}
 /* タニマチ同士の張り合い */
 if(T.length>=2&&!G.ev.some(e=>e.k==='tmriv')&&Math.random()<.07){const s=T.slice().sort(()=>Math.random()-.5);G.ev.push({k:'tmriv',id:nid(),a:s[0].n,b:s[1].n});}
 /* 親睦ゴルフ(名古屋場所のあと) */
 if((G.bnum-1)%6===3&&!G.ev.some(e=>e.k==='golf'))G.ev.push({k:'golf',id:nid()});}
/* 番付発表:新入幕・新三役で二本目の化粧まわし */
const nc0=nextCycle;nextCycle=function(){const old={};try{own().forEach(r=>{old[r.id]=[r.d,r.t];});}catch(e){}
 const res=nc0.apply(this,arguments);
 try{if(res!==false&&isPH(ME()))own().forEach(r=>{const o=old[r.id];if(!o||G.ev.some(e=>e.k==='kesho2'&&e.rid===r.id))return;
  const newM=r.d===0&&o[0]>0&&!(typeof wasLv==='function'&&wasLv(r,3)&&r.kesho2);const newS=(r.t==='S'||r.t==='K')&&!(o[1]==='S'||o[1]==='K'||o[1]==='O'||o[1]==='Y')&&!(typeof wasLv==='function'&&wasLv(r,4));
  if(!newM&&!newS)return;const opt=[];const t=tms().filter(x=>x.cl>=40).sort((a,b)=>b.cl-a.cl)[0];if(t)opt.push({k:'tm',n:t.n,t:'タニマチの'+t.n+'さん('+t.job+')から'});
  opt.push({k:'home',t:'出身地('+r.home+')の後援者一同から'});const sc=[r.uni,r.hs].find(n=>n&&typeof schOf==='function'&&schOf(n));if(sc)opt.push({k:'sch',n:sc,t:'母校('+schLabel(sc)+')から'});
  opt.push({k:'kai',t:'部屋の後援会一同から'});G.ev.push({k:'kesho2',id:nid(),rid:r.id,why:newS?'S':'M',opt:opt});});}catch(e){console.error(e);}
 return res;};
/* ---------- 出稽古先とのつきあい ---------- */
function dekR(h){return ((G.dekR||{})[h])||0;}
const di0=dekInfo;dekInfo=function(){const x=di0();if(x&&x.h!=null)x.q*=1+Math.min(.1,dekR(x.h)/300);return x;};
const dw0=doWeek;doWeek=function(){const tr=G&&G.phase==='train';let n=0,h=null;
 if(tr){try{const d=di0();if(d){h=d.h;n=ownAll().filter(r=>r.menu==='出'&&!(r.inj&&r.inj.s>=2)).length;}}catch(e){}}
 const res=dw0.apply(this,arguments);
 try{if(tr&&h!=null&&n>0){G.dekR=G.dekR||{};const b=dekR(h);G.dekR[h]=Math.min(100,b+Math.min(3,.6*n));
   if(b<20&&G.dekR[h]>=20)addNews(G.heya[h].n+'部屋とのつきあいが深まりました。向こうの関取も出稽古に来てくれるようになりそうです。');}
  if(tr&&G.dekR){const L=Object.keys(G.dekR).filter(k=>G.dekR[k]>=20&&G.heya[k]&&!G.heya[k].closed);
   if(L.length&&Math.random()<.08){const k=+pick(L);const c=G.order.filter(id=>{const r=G.R[id];return r&&r.h===k&&r.d<=1&&!r.ret;}).length;
    if(c){ownAll().filter(r=>r.d<=2&&!r.inj).forEach(r=>{for(const kk in MENU['申'].w)grow(r,kk,.004*MENU['申'].w[kk]);r.cond=cl(r.cond+3,0,100);});G.dekR[k]=Math.min(100,G.dekR[k]+1);
     addNews(G.heya[k].n+'部屋の関取が出稽古に来ました。いつもと違う相手と胸を合わせ、関取と幕下の調子が上がりました。');}}}}catch(e){console.error(e);}
 return res;};
/* ---------- 巡業:地元の声援・けがで休む関取 ---------- */
const te0=tourEnd;tourEnd=function(){const T=G._tr;const ti=tourInfo();const last=!!(T&&T.size&&ti&&G.wk===ti[1]);const res=te0.apply(this,arguments);
 try{if(last){const L=[...T].map(id=>G.R[id]).filter(Boolean);const hit=L.filter(r=>!r.fr&&Math.random()<.25);
   hit.forEach(r=>{r.pop=cl((r.pop||20)+(r.d<=1?4:6),0,100);r.mor=cl(r.mor+4,0,100);G.sup+=r.d<=1?6:3;});
   if(hit.length)addNews(ti[2]+'で地元('+hit.map(r=>pref(r.home)).filter((x,i,a)=>a.indexOf(x)===i).join('・')+')の近くを回り、'+hit.map(r=>r.n).join('・')+'に大きな声援が送られました。');
   const ab=own().filter(r=>r.d<=1&&r.inj&&!T.has(r.id));if(ab.length)addNews(ab.map(r=>r.n).join('・')+'は、けがのため診断書を出して'+ti[2]+'を休みました。');}}catch(e){console.error(e);}
 return res;};
/* ---------- 稽古タブ:出稽古先とのつきあい ---------- */
const kh0=keikoHTML;keikoHTML=function(){let h=kh0();try{const L=Object.keys(G.dekR||{}).map(k=>[+k,G.dekR[k]]).filter(x=>x[1]>=1&&G.heya[x[0]]&&!G.heya[x[0]].closed).sort((a,b)=>b[1]-a[1]).slice(0,5);
 if(L.length)h+='<div class="pn"><h2>出稽古先とのつきあい<span class="sub">数字は推定</span></h2>'+L.map(x=>'<div class="dkr"><b>'+esc(G.heya[x[0]].n)+'部屋</b><span class="gg"><i style="width:'+Math.round(x[1])+'%"></i></span><span>'+(x[1]>=50?'親しい':x[1]>=20?'行き来がある':'顔なじみ')+'</span></div>').join('')+
  '<div class="mute" style="font-size:12px">通うほど出稽古の効き目が上がり(最大 +10%)、「行き来がある」(20 以上)になると相手の部屋の関取も出稽古に来るようになります。</div></div>';}catch(e){}return h;};
document.head.insertAdjacentHTML('beforeend','<style>.dkr{display:grid;grid-template-columns:9em 1fr 7em;gap:8px;align-items:center;font-size:14px;margin:3px 0}.dkr .gg{width:100%}</style>');
window.dekR=dekR;
})();
