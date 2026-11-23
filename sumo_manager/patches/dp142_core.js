/* ========== v142:独立の段取り(① 師匠に打ち明ける → ② 弟子に声をかける → ③ 理事会 → ④ 門出) ==========
 実在の例:新しい部屋は日本相撲協会の理事会で承認される(荒磯部屋 2021、中村部屋 2024)。
   中村部屋の独立では内弟子 8 人が移り、2 人は元の部屋に残った(マネーポスト 2024)。
   力士の移籍は独立や閉鎖のときに限られるので、「あとから移ってくる」は入れない。
 数字はすべて推定:
   師匠が渋る 25%(ついて来る見込み −0.05、元の部屋との関係 cool +1 で始まる)。
   返事:見込み p(札 9 割・8 割・6.5 割)。すぐ来る p×0.7、迷う 残りの 55%、残る その他。
   迷ったとき:方針を語る 0.5(同じ大学・親子・内弟子なら +0.3)、親御さんに会う 0.5(同郷・同じ高校・親子なら +0.3)、
     答えを待つ p(門出の前に答えが出る)。
   残る力士への再説得(1 人 1 回):0.55・0.45・0.35。断られると cool +1、評判 −1。 */
function dpBase(w,sb){return (w.sc>=3?.9:w.sc>=2?.8:.65)-(sb?.05:0);}
function dpPick(a,w){const h=(w.o||0)+(w.n.charCodeAt(0)%2);return a[h%a.length];}
function dpSeki(w){return /横綱|大関|関脇|小結|前頭|十両/.test(w.rk||'');}
const DPL={go:['すぐ行きます。親方についていくと決めていました。','よろしくお願いします。新しい部屋で、一から頑張ります。','親方に教わった相撲を続けたいので、ついて行きます。'],
 mayo:['親方についていきたい気持ちはあります。ただ、稽古相手がいなくなるのが少し怖いんです。','少し考えさせてください。親にも相談したいです。','今の部屋には世話になった兄弟子がいて……すぐには決められません。'],
 stay:['兄弟子たちと稽古を続けたいです。','今の部屋で育ててもらった恩があるので、残ります。','@今の環境を変えたくありません。'],
 yes:['親方の話を聞いて決めました。ついて行きます。','親とも話して、決めました。お願いします。','答えが出ました。親方について行きます。'],
 no:['すみません。やはり残ります。','よく考えましたが、今の部屋で頑張ります。']};
function dpLn(k,w){if(k==='go'&&w.tg.includes('親子'))return '父の部屋で相撲を取ります。よろしくお願いします。';return dpPick(DPL[k],w).replace('@',dpSeki(w)?'関取として番付を守りたいので、':'関取を目前に、');}
function dpStart(x,names,oyT,rnd){const r=rnd||Math.random;const L=dokWs(x).filter(w=>names.includes(w.n)).map((w,i)=>({o:i,n:w.n,rk:w.rk,age:w.age,sc:w.sc,tg:w.tg.slice(),ans:null,fin:null,ln:'',how:''}));
 const sb=r()<.25;return {n:x.n,sh:x.sh,par:x.par,ms:((REALH.find(h=>h[0]===x.par)||[])[2])||'',t:oyT,sb:sb,L:L,i:0,st:1,cool:sb?1:0,fail:0};}
function dpAns(d,i,rnd){const r=rnd||Math.random;const w=d.L[i];if(!w||w.ans)return;const p=dpBase(w,d.sb),a=p*.7,x=r();
 w.ans=x<a?'go':x<a+(1-a)*.55?'mayo':'stay';w.ln=dpLn(w.ans,w);if(w.ans!=='mayo')w.fin=w.ans;}
function dpMayP(w,k,sb){if(k===2)return dpBase(w,sb);const re=k===0?/大$|大学|親子|内弟子/:/同郷|高校|親子/;return cl(.5+(w.tg.some(t=>re.test(t))?.3:0)-(sb?.05:0),.1,.9);}
function dpMay(d,i,k,rnd){const r=rnd||Math.random;const w=d.L[i];if(!w||w.ans!=='mayo'||w.fin)return;w.how=['方針を語った','親御さんに会った','答えを待つ'][k];
 if(k===2){w.fin='wait';w.ln='少し時間をください。門出までに答えを出します。';return;}
 if(r()<dpMayP(w,k,d.sb)){w.fin='go';w.ln=dpLn('yes',w);}else{w.fin='stay';w.ln=dpLn('no',w);}}
function dpSum(d,rnd){const r=rnd||Math.random;if(d.sum)return;d.sum=1;
 d.L.forEach(w=>{if(w.fin==='wait'){if(r()<dpBase(w,d.sb)){w.fin='go';w.ln='答えが出ました。親方について行きます。';}else{w.fin='stay';w.ln='考えましたが、今の部屋に残ります。';}}});
 if(d.L.length&&!d.L.some(w=>w.fin==='go')){const w=d.L.slice().sort((a,b)=>b.sc-a.sc)[0];w.fin='go';w.ln='……やっぱり、親方について行きます。';}}
function dpPerP(w,sb){return (w.sc>=3?.55:w.sc>=2?.45:.35)-(sb?.05:0);}
function dpPer(d,n,rnd){const r=rnd||Math.random;const w=d.L.find(x=>x.n===n);if(!w||w.fin!=='stay'||w.per)return;w.per=1;
 if(r()<dpPerP(w,d.sb)){w.fin='go';w.ln='親方の熱意に負けました。ついて行きます。';}else{d.cool++;d.fail++;w.ln='何度言われても、気持ちは変わりません。';}}
function dpGoN(d){return d.L.filter(w=>w.fin==='go').map(w=>w.n);}
function dpStayN(d){return d.L.filter(w=>w.fin!=='go').map(w=>w.n);}
function dpFin(d){const go=dpGoN(d),st=dpStayN(d);newGameDok(d.n,go,d.t);
 G.dok=G.dok||{};G.dok.cool=(G.dok.cool||0)+d.cool;G.dok.stay=st;G.dok.sb=d.sb?1:0;if(d.fail)G.rep=cl(G.rep-d.fail,0,100);
 G.order.forEach(id=>{const r=G.R[id];if(r&&r.h===ME()&&go.includes(r.n)){try{stPush(r,'tk','師匠の独立について行き、新しい部屋に移る');}catch(z){}}});
 addNews('日本相撲協会の理事会で、'+d.n+'部屋の新設が承認されました。'+d.par+'部屋から独立し、力士 '+go.length+' 人とともに出発します。'+(st.length?st.join('・')+'は元の部屋に残りました。':''));}
