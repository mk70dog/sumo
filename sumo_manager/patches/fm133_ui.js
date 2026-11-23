<script>
/* v133 画面:力士の画面に「暮らし」 */
var FM_V=window.FM_V||1;
STK.fm=['#c0607a','家'];
function fmHome(r){return r.mar?'所帯を持って部屋の外で暮らす(稽古は部屋に通う)':r.d<=1?'部屋の個室(関取)':'部屋の大部屋(若い衆)';}
function fmFam(r){if(!r.mar)return '独身';const k=r.kids||[];return (r.muko?'親方の娘と結婚(親方の婿)':'結婚('+bname(r.mar===1?G.bnum:r.mar)+')')+(k.length?'・子ども '+k.length+' 人('+k.map(x=>x.boy?'男':'女').join('・')+')':'');}
function fmHTML(r){if(r.h!==ME()||r.ret)return '';const koe=fmKoe(r);const inc=r.inc?man(r.inc.tot):'—';const cash=man(Math.round(r.cash||0));
 const tags=(r.muko?'<span class="fmt">部屋の跡継ぎ候補</span>':'')+(r.fk&&G.bnum-r.fk<3?'<span class="fmt">父になって奮起中</span>':'');
 if(FM_V===2)return '<div class="fmp"><h3>暮らし'+tags+'</h3><div class="fmg"><div class="fmc"><b>住まい</b>'+fmHome(r)+'</div><div class="fmc"><b>家族</b>'+fmFam(r)+'</div><div class="fmc"><b>個人後援会</b>'+(koe?koe+' 人':'まだない')+'</div><div class="fmc"><b>前の場所の収入</b>'+inc+'・貯金 '+cash+'</div></div></div>';
 return '<div class="fmp"><h3>暮らし'+tags+'</h3><dl class="kv"><dt>住まい</dt><dd>'+fmHome(r)+'</dd><dt>家族</dt><dd>'+fmFam(r)+'</dd><dt>個人後援会</dt><dd>'+(koe?koe+' 人':'まだない(関取になると地元にできることが多い)')+'</dd><dt>お金</dt><dd>前の場所の収入 '+inc+'・貯金 '+cash+'</dd></dl></div>';}
const fmS0=stHTML;stHTML=function(r){return fmS0(r)+fmHTML(r);};
</script><style>
.fmt{display:inline-block;font:12px sans-serif;background:#c0607a;color:#fff;border-radius:8px;padding:0 6px;margin-left:6px;vertical-align:middle}
.fmg{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:6px}.fmc{border:1px solid var(--line);border-radius:6px;padding:4px 8px;font-size:13px}.fmc b{display:block;font-size:12px;color:#c0607a}
</style>
