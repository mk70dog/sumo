/* ========== v128:部屋の年表と殿堂 ==========
 ・歴代の弟子(いまの弟子と、引退した弟子)から、部屋の年表・殿堂・部屋の記録をその場で作る(記録の画面)。
 ・引退した弟子の記録に、歩み(昇進・優勝・三賞・復活・初土俵)と、初土俵・新十両の場所を残す(st, deb, sek)。
 ・関取が途切れずにいた場所数(G.skS {c:いま, m:いちばん長い, mb:その終わり})をプレイヤーごとに数える。
   実際に高砂部屋は明治から 139 年続けて関取を出してきたが、2016 年 11 月場所で途絶えた(Number)。
 ・新十両までの最速は所要 6 場所(木瀬部屋の常幸龍ら 3 人)、ふつうは順調でも 3〜5 年(Sportiva 2017)。 */
const HYK={in:1,up:1,yu:1,sh:1,fk:1};
function hyNote(r){return (r.sto||[]).filter(x=>HYK[x.k]).map(x=>({b:x.b,k:x.k,t:x.t}));}
function hyDeb(r){const s=(r.sto||[]).find(x=>x.k==='in');if(s)return s.b;const H=r.hist||[];return H.length&&H.length<150?H[0].b:null;}
function hySek(){if(!G.skS){G.skS={c:0,m:0,mb:0};/* 前の版:いまの弟子の成績から、さかのぼって数える(推定) */
  const H={};own().forEach(r=>(r.hist||[]).forEach(h=>{if(h.d<=1)H[h.b]=1;}));let c=0;for(let b=G.bnum-1;b>0&&H[b];b--)c++;G.skS.c=c;G.skS.m=c;G.skS.mb=c?G.bnum-1:0;}
 const k=G.skS;if(own().some(r=>r.d<=1)){k.c++;if(k.c>=k.m){k.m=k.c;k.mb=G.bnum;}}else k.c=0;}
