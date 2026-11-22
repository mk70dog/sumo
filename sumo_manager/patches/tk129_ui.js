<script>
/* v129 画面:力士の画面に「型づくり」、稽古の札に型と段階 */
var TK_V=window.TK_V||1;
const TKGROW={O:['突き・押し','引き・足'],R:['右差し・寄り','投げ・前さばき'],L:['左差し・寄り','投げ・前さばき'],W:['技(投げ・足・手)','柔らかさ・引き・立ち合い'],X:['突き・押しと寄り','投げ・前さばき']};
function tkFitW(r,p){const f=tkFit(r,p);return f>=1.15?'とても合う':f>=1.05?'合う':f>=.95?'ふつう':f>=.85?'やや合わない':'合わない';}
function tkNow(r,t){const s=tkStage(t.v),g=TKGROW[t.p];return s===0?'体と腰(四股・すり足・てっぽう)':s===1?g[0]:s===2?g[1]:'型の仕上げ';}
function tkChip(r){if(!r||r.h!==ME()||r.ret)return '';const t=tkOf(r);return '<div class="kgc"><b>型</b> '+TKPN[t.p]+'・'+TKPS[tkStage(t.v)]+' <span class="mute">'+Math.round(t.v)+'</span></div>';}
function tkPick(id,p){const r=G.R[id];if(!r)return;tkSet(r,p);save();showR(id);}
function tkBtns(r){const t=tkOf(r);const b=(p,l)=>'<button class="pc'+((r.tkP||null)===p?' on':'')+'" onclick="tkPick('+r.id+','+(p?'\''+p+'\'':'null')+')">'+l+'</button>';
 return '<div>'+b(null,'親方にまかせる')+Object.keys(TKPN).map(p=>b(p,TKPN[p]+'<span class="tkf">'+tkFitW(r,p)+'</span>')).join('')+'</div><p class="mute" style="font-size:12px;margin:2px 0">型を変えると、完成度は 4 割に下がります(型を作り直すには年単位かかります)。体格に合う型ほど早く身につきます。数字は推定。</p>';}
function tkStep(t){const s=tkStage(t.v);return '<div class="tks">'+TKPS.map((x,i)=>'<span class="'+(i<s?'dn':i===s?'cu':'')+'">'+x+'</span>').join('<i>›</i>')+'</div>';}
function tkBar(v){return '<span class="tkbar"><i style="width:'+Math.round(v)+'%"></i></span>';}
function tkNext(t){const s=tkStage(t.v);return s>=3?'完成':'あと '+Math.ceil([30,65,90][s]-t.v)+' で「'+TKPS[s+1]+'」';}
function tkHTML(r){if(r.h!==ME()||r.ret)return '';const t=tkOf(r),c=(()=>{try{return kcCoach(r);}catch(e){return null;}})();
 const who=r.tkP?'あなたが決めた型':(c?(c.co?esc(c.n):'師匠')+'が決めた型':'親方が決めた型');
 if(TK_V===2)return '<div class="tkp"><h3>型づくり</h3><p class="kaku" style="margin:2px 0"><b class="tkn">'+TKPN[t.p]+'</b>('+who+')'+tkBar(t.v)+' 完成度 <b>'+Math.round(t.v)+'</b>・'+TKPS[tkStage(t.v)]+'・'+tkNext(t)+'</p><details><summary>型を選び直す</summary>'+tkBtns(r)+'</details></div>';
 if(TK_V===3)return '<div class="tkp"><h3>型づくり</h3><div class="tkg"><div class="tkbig"><div class="tkn">'+TKPN[t.p]+'</div><div class="mute" style="font-size:12px">'+who+'</div><div class="tkpc">'+Math.round(t.v)+'<small>/100</small></div></div><div>'+tkStep(t)+'<p class="kaku" style="margin:4px 0">いま伸ばしているもの:<b>'+tkNow(r,t)+'</b><br>'+tkNext(t)+'。体格との相性:'+tkFitW(r,t.p)+'。<br>取組で自分の形('+(t.p==='O'?'突き押しの攻防':t.p==='R'?'右四つ':t.p==='L'?'左四つ':t.p==='W'?'どの形でも少し':'押し合いでも四つでも')+')になると、完成度に応じて攻めが強くなります。</p></div></div>'+tkBtns(r)+'</div>';
 return '<div class="tkp"><h3>型づくり</h3><p class="kaku" style="margin:2px 0"><b class="tkn">'+TKPN[t.p]+'</b> <span class="mute">('+who+'・体格との相性 '+tkFitW(r,t.p)+')</span></p>'+tkStep(t)+'<p class="kaku" style="margin:4px 0">'+tkBar(t.v)+' 完成度 <b>'+Math.round(t.v)+'</b>・'+tkNext(t)+'。いま伸ばしているもの:'+tkNow(r,t)+'</p>'+tkBtns(r)+'</div>';}
const tkK0=kcCard;kcCard=function(r){return tkK0(r)+tkChip(r);};
const tkS0=stHTML;stHTML=function(r){return tkHTML(r)+tkS0(r);};
</script><style>
.kgc{font:12px sans-serif;margin:3px 0;padding:2px 6px;border-radius:4px;background:#2c3e5c14}
.tkp .pc{display:inline-block!important;width:auto!important;font:13px sans-serif!important;padding:4px 10px!important;border-radius:14px!important;border:1px solid #8a7040!important;background:#fff!important;color:#1a140c!important;margin:2px!important}.tkp .pc.on{background:#7a1d10!important;border-color:#7a1d10!important;color:#fff!important;font-weight:bold}
.tkf{display:block;font-size:10px;opacity:.75}.tkn{font-size:17px;color:var(--ai)}
.tks{display:flex;flex-wrap:wrap;align-items:center;gap:2px;margin:4px 0;font:13px sans-serif}.tks span{padding:3px 10px;border-radius:12px;background:#0001;color:#777}.tks span.dn{background:#c9a24a55;color:#5a4410}.tks span.cu{background:#7a1d10;color:#fff;font-weight:bold}.tks i{color:#aaa;font-style:normal}
.tkbar{display:inline-block;width:110px;height:9px;background:#0002;border-radius:5px;overflow:hidden;vertical-align:middle;margin:0 6px}.tkbar i{display:block;height:100%;background:linear-gradient(90deg,#c9a24a,#7a1d10)}
.tkg{display:grid;grid-template-columns:130px 1fr;gap:10px;align-items:start}.tkbig{border:2px solid #c9a24a;border-radius:8px;padding:6px;text-align:center;background:#fffaf0;color:#1a140c}.tkpc{font:bold 30px serif;color:#7a1d10}.tkpc small{font-size:12px;color:#888}
@media(max-width:500px){.tkg{grid-template-columns:1fr}}
</style>
