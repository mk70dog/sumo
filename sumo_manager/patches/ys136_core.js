/* ========== v136:横綱審議委員会と綱取り ==========
 ・横審の内規:大関で 2 場所連続優勝が原則。「それに準ずる成績」で推薦するときは出席委員の 3 分の 2 以上の決議(デイリー 2025/1/27・時事)。
   準ずる成績には数値の基準がなく、昇進直前 3 場所の合計勝ち星がよく比べられる(最近の横綱は 36〜38 勝。33 勝は「最低水準」の声。週刊女性 PRIME)。
 ・ゲーム:大関で 2 場所続けて大関。①2 場所連続優勝 → 推薦(満場一致)。②優勝と優勝同点・次点(決定戦の敗者か次点)で 2 場所 24 勝以上 → 横審の会合。
   委員 9 人(推定)が 1 人ずつ賛否。賛成の見込み = 0.5 +(2 場所の勝ち星−25)×0.15 +(3 場所の勝ち星−36)×0.03 + 直前の場所が優勝 0.08
   − 不祥事の数 ×0.12(0.03〜0.97)。6 人(3 分の 2)以上で推薦。これまでの「優勝+同点・次点で 25 勝以上なら自動で昇進」をこれに置き換える。
 ・綱取りの場所:大関が優勝するか、13 勝以上で優勝同点・次点だった次の場所(ysTsuna)。本場所の画面に「綱取り」の欄。
 ・伝達式:自分の部屋の力士が横綱に上がると、使者を迎えて口上を述べる(出来事 dentatsu)。綱打ちと土俵入りの型(tsuna)は前からある。
 ・不祥事の数 r.scN(自分の部屋は不祥事の出来事、ほかの部屋はニュースの不祥事で数える)。数字はすべて推定。 */
const YS_N=9;
function ysP(r,a,b,c){const t2=a.w+b.w,t3=t2+(c?c.w:10);return cl(.5+(t2-25)*.15+(t3-36)*.03+(b.yu?.08:0)-(r.scN||0)*.12,.03,.97);}
function ysJudge(r,a,b){const H=r.hist||[];const c=H.length>=3?H[H.length-3]:null;const t3=a.w+b.w+(c?c.w:0);
 const log=(ok,yes,why)=>{G.ys=G.ys||[];G.ys.push({b:G.bnum,n:r.n,h:r.h,rk:b.rk,ok:ok?1:0,yes:yes,no:YS_N-yes,why:why,w:[c?c.w:null,a.w,b.w],yu:[c?!!c.yu:false,!!a.yu,!!b.yu]});if(G.ys.length>40)G.ys.shift();
  addNews('🏛 横綱審議委員会:'+r.n+'('+G.heya[r.h].n+')を横綱に'+(ok?'推薦':'推薦せず')+'。'+why+(yes!=null?'(賛成 '+yes+'・反対 '+(YS_N-yes)+')':'')+'。');};
 if(a.yu&&b.yu){log(1,YS_N,'大関で 2 場所連続優勝');return true;}
 const cand=((a.yu&&b.jn)||(b.yu&&a.jn))&&a.w+b.w>=24;if(!cand)return false;
 const p=ysP(r,a,b,c);let yes=0;for(let i=0;i<YS_N;i++)if(Math.random()<p)yes++;const ok=yes*3>=YS_N*2;
 log(ok,yes,'優勝と'+(a.yu?'その次の場所の':'その前の場所の')+'好成績(2 場所 '+(a.w+b.w)+' 勝・3 場所 '+t3+' 勝)を「準ずる成績」と見るか');return ok;}
/* 綱取りの場所か(この場所の番付で大関、前の場所が大関で優勝か 13 勝以上の同点・次点) */
function ysTsuna(r){if(r.t!=='O')return null;const H=r.hist||[];const h=H[H.length-1];if(!h||h.t!=='O')return null;if(h.yu||(h.jn&&h.w>=13))return h;return null;}
function ysVoteBefore(r,cur){const H=r.hist||[];const a=H[H.length-1],c=H[H.length-2]||null;if(!a)return null;const b={w:cur,yu:false};return ysP(r,a,{w:cur,yu:true},c);}
const YS_KOJO=['勇往邁進','質実剛健','一心精進','誠心誠意','百折不撓'];
const YS_EVT={
 dentatsu:{t:'横綱昇進の伝達式',d:e=>{const r=G.R[e.rid];if(!r)return '';if(!e.yj)e.yj=pick(YS_KOJO);return '理事会で横綱昇進が決まり、協会の使者が部屋に昇進を伝えに来ます。親方とおかみさんと並んで、'+r.n+'が口上を述べます。どんな言葉にしますか。';},
  c:e=>{if(!e.yj)e.yj=pick(YS_KOJO);return ['「謹んでお受けいたします。横綱の名を汚さぬよう、一層稽古に精進いたします」','「謹んでお受けいたします。支えてくださった皆さまへの感謝を忘れず、横綱として土俵に尽くします」','「謹んでお受けいたします。'+e.yj+'の精神で、横綱の地位を全うします」'];},
  ap:(e,i)=>{const r=G.R[e.rid];if(!r)return '';const L=YS_EVT.dentatsu.c(e);r.kojo=L[i];stPush(r,'up','横綱昇進の伝達式。口上'+L[i]);
   if(i===0){G.rep=cl(G.rep+2,0,100);return '堂々とした口上でした。協会の評判が上がりました。';}
   if(i===1){G.sup+=15;own().forEach(x=>{if(x!==r)x.tr=cl((x.tr==null?50:x.tr)+2,0,100);});return '感謝の言葉に後援会が沸き、弟子たちも胸を熱くしました。';}
   r.pop=cl((r.pop||20)+8,0,100);return '「'+e.yj+'」の四字熟語が翌日の新聞の見出しを飾りました。';}}
};
function ysEvt(){const sc=EVT.scand;if(!sc||sc._ys)return;sc._ys=1;const a0=sc.ap;sc.ap=(e,i)=>{const r=G.R[e.rid];if(r)r.scN=(r.scN||0)+1;return a0(e,i);};}
