/* ========== v133:力士の私生活と家族 ==========
 ①結婚を出来事に(kekkon):関取・24 歳以上で、場所ごと 7%(前の版の自動の結婚は 25 歳・300 万円・4% で、ほとんど起きなかった)。
   盛大な披露宴(本人 300 万円、後援会 +、部屋にご祝儀 30 万円、人気 +3)/身内だけ(本人 100 万円、気力 +8)/「落ち着くまで待て」(気力 −6・信頼 −3、6 場所後にまた)。
   家族の支え:結婚した力士は気力 35 未満のとき場所ごとに +2。所帯を持って部屋の外で暮らすので、結婚した関取 1 人につき幕下以下の信頼 −0.1/場所。
 ②子の誕生:結婚した力士に場所ごと 4%(3 人まで)。気力 +12、3 場所のあいだ奮起(伸び ×1.05)。男の子がいると、引退後に子が力士になる見込み(二世)が上がる。
   実例:琴桜は大関のとき、長女の誕生が力になったと振り返り、優勝して横綱に(東スポ)。
 ③師匠の娘との縁談(endan):親方の家族(G.sp.fam)に 22〜34 歳の独身の娘がいて、関取・24〜33 歳・独身・信頼 60 以上・幕内経験の弟子がいると場所ごと 5%。
   まとまると婿(r.muko)。親方の定年のとき「婿の○○が引退して部屋を継ぐ」を選べる(名跡の資格があれば。おかみさんは娘)。
   実例:昭和は師匠の娘が有望な関取を婿に迎えて継ぐ例が多く、元琴ノ若は琴櫻の娘と結婚して佐渡ヶ嶽部屋を継いだ(Number)。
 実在の力士(始めの番付にいた力士 r.kk)には、結婚・縁談の出来事は起こさない(私生活を作らないため)。タニマチとの宴席(enkai)は前からある。数字はすべて推定。 */
function fmKoe(r){const best=r.best||999;return (r.d<=1||best<=divStart(2))?Math.round(40+(r.pop||20)*3+(r.d===0?80:r.d===1?30:0)+(r.t?150:0)):0;}
function fmG(r){return r.fk&&G.bnum-r.fk<3?1.05:1;}
function fmDau(){const f=G.sp&&G.sp.fam;if(!f||!f.kids)return null;return f.kids.find(k=>!k.boy&&!k.mar&&k.age>=22&&k.age<=34)||null;}
function fmCycle(){const O=own();const mar=O.filter(r=>r.mar&&r.d<=1).length;
 O.forEach(r=>{
  if(r.mar){if(r.mor<35)r.mor=cl(r.mor+2,0,100);
   r.kids=r.kids||[];if(!r.kk&&r.kids.length<3&&Math.random()<.04){const boy=Math.random()<.5;r.kids.push({b:G.bnum,boy:boy?1:0});r.mor=cl(r.mor+12,0,100);r.fk=G.bnum;
    stPush(r,'fm',(boy?'長男':'長女')+(r.kids.length>1?'(第 '+r.kids.length+' 子)':'')+'が生まれる');addNews('👶 '+r.n+'に'+(boy?'男の子':'女の子')+'が生まれました。「子どものためにも」と稽古に熱が入っています。');}}
  else if(r.mar===undefined||!r.mar){if(r.marW&&G.bnum<r.marW)return;
   if(r.d<=1&&!r.muko&&!r.kk&&r.age>=24&&Math.random()<.07&&!G.ev.some(e=>e.k==='kekkon'))G.ev.push({k:'kekkon',rid:r.id});}
  if(r.d>=2&&mar)r.tr=cl((r.tr==null?50:r.tr)-.1*Math.min(3,mar),0,100);});
 // 縁談
 const d=fmDau();if(d&&!G.ev.some(e=>e.k==='endan')&&Math.random()<.05){const c=O.filter(r=>r.d<=1&&!r.mar&&!r.kk&&r.age>=24&&r.age<=33&&(r.tr==null?50:r.tr)>=60&&(r.best||999)<divStart(1)).sort((a,b)=>a.pos-b.pos)[0];
  if(c)G.ev.push({k:'endan',rid:c.id,rel:d.rel,age:d.age});}
}
function fmMarry(r,big){r.mar=G.bnum;r.cash=(r.cash||0)-(big?300:100);r.mor=cl(r.mor+(big?5:8),0,100);if(big){const n=10+Math.round((r.pop||20)/5);G.sup+=n;G.money+=30;r.pop=cl((r.pop||20)+3,0,100);G.rep=cl(G.rep+1,0,100);return n;}return 0;}
/* 婿が部屋を継ぐ(親方の定年) */
function fmMukoS(r){const a=r.a;return {sid:G.sid++,role:'co',n:'元・'+r.n,mo:bestRank(r),age:Math.floor(r.age),own:true,sk:{osh:Math.round(cl((a.tsk+a.tac)/2*.8+R(0,3),1,20)),yot:Math.round(cl((Math.max(a.mig,a.hid)+a.yor)/2*.8+R(0,3),1,20)),waz:Math.round(cl((a.nag+a.ash+a.tgw)/3*.8+R(0,3),1,20)),tai:Math.round(cl((a.str+a.end)/2*.7+R(0,3),1,20)),sei:Math.round(cl((a.rei+a.pro)/2*.9+R(0,2),1,20)),meki:RI(8,14)},sal:0};}
function fmMukoChoice(L){const r=own().find(x=>x.muko&&!x.ret);if(!r||!myoOK(r)||(r.fr&&!r.nat))return L;
 L.unshift({t:'婿の'+r.n+'('+r.rkS+')が引退して部屋を継ぐ',f:()=>{const s=fmMukoS(r);const ok=G.okami;doRetire(r,'師匠の跡を継ぐため');const m=succeed(s,'ex');G.okami=mkOkami();G.okami.age=Math.max(25,Math.floor(r.age)-RI(0,4));G.okami.n=(G.okami.n)+'(先代の娘)';return m+' 婿として部屋を継ぎ、おかみさんは先代の娘です。';}});return L;}
const FM_EVT={
 kekkon:{t:'結婚の報告',d:e=>{const r=G.R[e.rid];return r?r.n+'('+r.rkS+'・'+Math.floor(r.age)+'歳)が「結婚したい人がいます」と報告に来ました。関取は所帯を持って部屋の外で暮らせます。':'';},
  c:['盛大な披露宴を開く(本人 300 万円。後援会が集まる)','身内だけで式を挙げる(本人 100 万円)','「関取として落ち着くまで待て」と言う'],
  ap:(e,i)=>{const r=G.R[e.rid];if(!r)return '';if(i===0){const n=fmMarry(r,1);stPush(r,'fm','結婚(盛大な披露宴)');return r.n+'の披露宴に後援会や角界の人が大勢集まりました。後援会員が '+n+' 人増え、部屋にもご祝儀 30 万円が届きました。';}
   if(i===1){fmMarry(r,0);stPush(r,'fm','結婚(身内だけの式)');return r.n+'は身内だけで式を挙げました。落ち着いた顔で稽古場に来ています。';}
   r.mor=cl(r.mor-6,0,100);r.tr=cl((r.tr==null?50:r.tr)-3,0,100);r.marW=G.bnum+6;return r.n+'は残念そうに引き下がりました。';}},
 endan:{t:'師匠の娘との縁談',d:e=>{const r=G.R[e.rid];return r?'親方の'+e.rel+'('+e.age+'歳)と、'+r.n+'('+r.rkS+')の縁談が持ち上がりました。まとまれば、'+r.n+'は親方の婿として、将来この部屋を継ぐ第一の候補になります。':'';},
  c:['縁談をまとめる(婿に迎える)','二人の気持ちに任せる','見送る'],
  ap:(e,i)=>{const r=G.R[e.rid];const d=G.sp&&G.sp.fam&&G.sp.fam.kids.find(k=>k.rel===e.rel);if(!r||!d)return '';
   const ok=i===0||(i===1&&Math.random()<.5);if(!ok)return i===1?'二人は話し合い、今回は縁がありませんでした。':'縁談は見送りました。';
   d.mar=r.n;r.mar=G.bnum;r.muko=1;r.mor=cl(r.mor+10,0,100);r.tr=cl((r.tr==null?50:r.tr)+10,0,100);G.sup+=5;stPush(r,'fm','親方の'+e.rel+'と結婚し、親方の婿になる');
   return r.n+'が親方の'+e.rel+'と結婚し、婿になりました。部屋の跡継ぎとして期待が集まります。';}}
};
