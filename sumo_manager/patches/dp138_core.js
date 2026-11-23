/* ========== v138:独立のとき、残ると言った内弟子を説得する ==========
 独立で選んだ内弟子は、札の数でついて来る見込みが決まる(9 割・8 割・6.5 割、v43〜)。残ると言った力士ごとに出来事 dokPer:
 「もう一度説得する」:成功の見込み = 札が強い 0.55・中 0.45・少ない 0.35 +(親方の評判 jin −50)×0.004(0.15〜0.8)。
   成功すれば新しい部屋に来る(親方への信頼 45)。断られると元の部屋との関係が冷える(G.dok.cool +1:元の部屋への出稽古の効き目 −10%/回、評判 −1)。
 「本人の気持ちを尊重する」:元の部屋に残る(評判 +0.5)。数字は推定。 */
function dpChance(e){return cl((e.sc>=3?.55:e.sc>=2?.45:.35)+((G.jin==null?50:G.jin)-50)*.004,.15,.8);}
const DP_EVT={
 dokPer:{t:'残ると言った内弟子',d:e=>e.n+'は「元の'+(G.dok&&G.dok.from||'')+'部屋に残ります」と言っています。もう一度、新しい部屋に来てくれるよう説得しますか。説得がうまくいく見込みは'+(dpChance(e)>=.5?'五分以上':dpChance(e)>=.35?'やや低め':'低い')+'です。断られると、元の部屋との関係が少し冷えます。',
  c:['もう一度説得する','本人の気持ちを尊重する'],
  ap:(e,i)=>{const from=G.dok&&G.dok.from;const hi=G.heya.findIndex(h=>h.n===from);const r=G.order.map(id=>G.R[id]).find(x=>x&&x.n===e.n&&x.h===hi&&!x.ret);
   if(i===1){G.rep=cl(G.rep+.5,0,100);return e.n+'の気持ちを尊重しました。元の部屋とは良い関係のままです。';}
   if(!r)return e.n+'はもう元の部屋の力士として番付に載っていて、話はまとまりませんでした。';
   if(Math.random()<dpChance(e)){r.h=ME();r.tr=45;r.kn=Math.max(r.kn||0,30);r.menu=r.menu||'申';r.it=r.it==null?1:r.it;r.wplan=r.wplan||1;r.injPol=r.injPol||'任';
    G.capB=Math.max(G.capB||0,own().length+1-(4+3*G.fac.shuku));try{stPush(r,'tk','親方の説得で、独立した部屋について行く');}catch(z){}
    return '親方の熱意が通じ、'+e.n+'が新しい部屋に来てくれることになりました。';}
   G.dok=G.dok||{};G.dok.cool=(G.dok.cool||0)+1;G.rep=cl(G.rep-1,0,100);
   return e.n+'の気持ちは変わりませんでした。元の'+from+'部屋の親方は、少し気を悪くしたようです(元の部屋への出稽古の効き目が下がります)。';}}
};
