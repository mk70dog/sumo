/* ========== v147:九州場所の日ごとの星・金星と、実在の力士のこれまでの優勝回数・金星・三賞 ==========
 RK11B:幕内・十両の 15 日間の取組(data/kyushu2026_bouts.txt。出典 観戦ガイド。10 日目の幕内は勝ち数の差から)。
   rkReplay の中で、星取表に相手・決まり手・不戦・休みを入れる。前頭が横綱に勝った一番は金星(藤凌駕・宇良・藤青雲・伯乃富士が豊昇龍から)。
   幕下以下は日ごとの並びが入っていない(勝ち負けの数だけ)。
 RKCAR:これまでの各段優勝・金星・三賞(data/career2026.txt。九州場所の分を含む数)。九州場所の分は場所を終えるときに足されるので、その分を引いて入れる。
   十両以下の各段優勝は 2022 年以降の一覧から取ったので、それより前だけに優勝した人は 0 のまま。十両の力士の金星・三賞は入っていない。 */
const RK11B=__RK11B__;
const RKCAR=__RKCAR__;
function rkCareer(){
 const K={};RK11B.forEach(([d,e,r,w,k])=>{if(r==='○'||r==='●'){const W=r==='○'?e:w,L=r==='○'?w:e;K[W+'|'+L]=1;}});
 G.order.forEach(id=>{const r=G.R[id],c=RKCAR[r.n];if(!c)return;
  for(let d=0;d<6;d++)r.yu[d]=Math.max(0,c[d]-(RK11YU[d]===r.n?1:0));
  r.sansho=Math.max(0,c[7]-RK11SH.filter(x=>x[0]===r.n).length);r.kin=c[6];});}
function rkBouts(B){const id={};G.order.forEach(i=>{id[G.R[i].n]=i;});
 RK11B.forEach(([d,e,r,w,k])=>{const a=id[e],b=id[w];if(a==null||b==null)return;const A=B.rec[a],Bq=B.rec[b];
  if(r==='○'||r==='●'){const W=r==='○'?a:b,L=r==='○'?b:a;B.rec[W].res[d-1]={o:L,r:'○',k:k};B.rec[L].res[d-1]={o:W,r:'●',k:k};
   const WR=G.R[W],LR=G.R[L];if(LR.t==='Y'&&WR.d===0&&!WR.t){B.kin.push([W,L,d]);if(!RKCAR[WR.n])WR.kin++;}}
  else{const W=r==='□'?a:b,L=r==='□'?b:a;B.rec[W].res[d-1]={o:L,r:'□',k:'不戦勝'};B.rec[L].res[d-1]={o:W,r:'■',k:'不戦敗'};}});
 G.order.forEach(i=>{const r=G.R[i],c=B.rec[i];if(r.d>1||!(c.ab>0))return;for(let x=0;x<15;x++)if(!c.res[x])c.res[x]={r:'や'};});}
