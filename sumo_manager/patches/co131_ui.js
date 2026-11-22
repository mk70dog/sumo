<script>
/* v131 画面:スタッフの画面に「こんな親方に来てほしい」、部屋付き親方の札に現役の取り口・指導の色・人柄・教え方・来てくれる見込み */
var CO_V=window.CO_V||1;
function coW(v){return v>=15?'とても良い':v>=12?'良い':v>=8?'ふつう':'いまひとつ';}
const coSkH0=skH;skH=function(s){let h=coSkH0(s);if(s.role!=='co')return h;coInit(s);const inM=G.market.includes(s);let kc='';try{kc=KC[kcOfS(s)].n;}catch(e){}
 h+='<div class="cot">教える型 <b>'+coStyleN(s)+'</b>・指導の色 <b>'+kc+'</b>・人柄 <b class="'+ac(s.hito)+'">'+s.hito+'</b>('+coW(s.hito)+')・教え方 <b class="'+ac(s.tch)+'">'+s.tch+'</b>('+coW(s.tch)+')</div>';
 if(inM){const a=coAcc(s);h+='<div class="cot">'+(s.req?'<span class="coq">条件に合う</span> ':'')+(s.from?esc(s.from)+'部屋から・':'')+'来てくれる見込み <b>'+(a>=.65?'高い':a>=.4?'五分五分':'低い')+'</b></div>';}
 return h;};
function coReqUI(k){const m=coReqSet(k);save();render();if(m!=='OK')alertM('部屋付き親方探し',m);}
function coReqHTML(){const q=G.coReq;const left=q?Math.max(0,2-(G.bnum-q.b)):0;
 const act=q?'<p class="kaku" style="margin:4px 0">いま探している:<b>'+COREQ[q.k][0]+'</b>(あと '+(left+1)+' 回、雇える人に候補が出ます)</p>':'';
 const note='<p class="mute kaku" style="font-size:12px;margin:4px 0">一門の親方衆に声をかけます(交際費 20 万円)。候補が来てくれるかは、部屋の評判・関取の数・同じ一門か・型の合う弟子がいるかで決まります。実際も部屋の移籍は協会の理事会の承認が要り、同じ一門の部屋に移る例が多いです。数字は推定。</p>';
 if(CO_V===2)return '<div class="pn cop"><h2>こんな親方に来てほしい</h2>'+act+'<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center"><select id="coRqS" class="sel">'+Object.keys(COREQ).map(k=>'<option value="'+k+'">'+COREQ[k][0]+'</option>').join('')+'</select><button class="btn sm ai" onclick="coReqUI(document.getElementById(\'coRqS\').value)">声をかける(20 万円)</button></div>'+note+'</div>';
 return '<div class="pn cop"><h2>こんな親方に来てほしい<span class="sub">条件を出して一門に声をかける</span></h2>'+act+'<div class="coqs">'+Object.keys(COREQ).map(k=>'<button class="pc'+(q&&q.k===k?' on':'')+'" onclick="coReqUI(\''+k+'\')">'+COREQ[k][0]+'</button>').join('')+'</div>'+note+'</div>';}
const coSt0=staffHTML;staffHTML=function(){const h=coSt0().split('<span class="kaku">給与 '+man(0)+'/場所</span>').join('<span class="kaku">給与は協会から</span>');const i=h.indexOf('<div class="pn"><h2>雇える人');return i<0?h+coReqHTML():h.slice(0,i)+coReqHTML()+h.slice(i);};
</script><style>
.cot{font:12px sans-serif;margin:3px 0;color:var(--ink,#1a140c)}.coq{background:#7a1d10;color:#fff;border-radius:8px;padding:0 6px}
.cop .pc{display:inline-block!important;width:auto!important;font:13px sans-serif!important;padding:5px 12px!important;border-radius:14px!important;border:1px solid #8a7040!important;background:#fff!important;color:#1a140c!important;margin:2px!important}.cop .pc.on{background:#7a1d10!important;border-color:#7a1d10!important;color:#fff!important;font-weight:bold}
</style>
