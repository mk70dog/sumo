<script>
/* v136 画面:本場所の画面に「綱取り」、記録の画面に「横綱審議委員会」 */
var YS_V=window.YS_V||1;
function ysRows(){return G.order.map(i=>G.R[i]).filter(r=>r&&!r.ret&&ysTsuna(r));}
function ysCard(r){const h=ysTsuna(r);const rc=G.B&&G.B.rec&&G.B.rec[r.id];const H=r.hist||[];const c=H[H.length-2];const now=rc?rc.w+'勝'+(rc.l+rc.ab)+'敗':'場所前';
 const cw=rc?rc.w:0;const t3=(c?c.w:0)+h.w+cw;const need=Math.max(0,36-t3);const own=r.h===ME();
 const ls=rc?rc.l+rc.ab:0,left=rc?Math.max(0,15-rc.w-ls):15;const proj=rc?Math.round(rc.w+left*.65):13;const p=ls>=4?0:ysP(r,h,{w:proj,yu:true},c);
 const body='<div class="ysr"><b class="nm clk2" onclick="showR('+r.id+')">'+esc(r.n)+'</b> <span class="mute">大関・'+esc(G.heya[r.h].n)+'部屋</span>'+(own?'<span class="yso">自分の部屋</span>':'')+'</div>'+
  '<div class="ysg"><div><small>前の場所</small><b>'+h.w+'勝'+(h.yu?'・優勝':h.jn===1?'・優勝同点':'・次点')+'</b></div><div><small>今場所</small><b>'+now+'</b></div><div><small>3 場所の目安</small><b>'+(need?'あと '+need+' 勝で 36 勝':'36 勝に届く')+'</b></div></div>'+
  '<div class="kaku" style="font-size:12px;margin-top:4px">'+(h.yu?'優勝すれば 2 場所連続優勝で推薦。優勝を逃しても、優勝同点・次点なら横審の会合':'優勝すれば横審の会合。13 勝以上の優勝なら賛成が集まりやすい')+'(いまの見込み:'+(p>=.75?'高い':p>=.5?'五分五分':'厳しい')+')。'+((r.scN||0)?'不祥事の記録 '+r.scN+' 回が響く。':'')+'</div>';
 return YS_V===2?'<tr><td class="nm">'+esc(r.n)+'</td><td>'+h.w+'勝'+(h.yu?'(優勝)':'')+'</td><td>'+now+'</td><td>'+(p>=.75?'高い':p>=.5?'五分五分':'厳しい')+'</td></tr>':'<div class="ysc">'+body+'</div>';}
function ysHTML(){const L=ysRows();if(!L.length)return '';
 if(YS_V===2)return '<div class="pn ysp"><h2>綱取り</h2><table class="tb"><tr><th>大関</th><th>前の場所</th><th>今場所</th><th>見込み</th></tr>'+L.map(ysCard).join('')+'</table><p class="mute kaku" style="font-size:12px">横審の内規:大関で 2 場所連続優勝、またはそれに準ずる成績(準ずる成績は委員の 3 分の 2 以上の賛成)。</p></div>';
 return '<div class="pn ysp"><h2>綱取り</h2><p class="mute kaku" style="font-size:12px;margin:0 0 4px">横審の内規:大関で 2 場所連続優勝、またはそれに準ずる成績(準ずる成績は委員の 3 分の 2 以上の賛成)。目安の 36 勝は、最近の横綱の昇進前 3 場所の多くが 36〜38 勝だったことから(推定)。</p>'+L.map(ysCard).join('')+'</div>';}
const ysB0=bashoHTML;bashoHTML=function(){const h=ysB0();let x='';try{x=ysHTML();}catch(e){}if(!x)return h;const i=h.indexOf('<div class="pn');return i<0?x+h:h.slice(0,i)+x+h.slice(i);};
function ysLogHTML(){const L=(G.ys||[]).slice().reverse();if(!L.length)return '';
 return '<div class="pn"><h2>横綱審議委員会<span class="sub">横綱推薦の会合の記録</span></h2><table class="tb"><tr><th>場所</th><th>大関</th><th>直前 3 場所</th><th>結果</th></tr>'+L.slice(0,15).map(x=>'<tr><td>'+esc(bname(x.b-1))+'後</td><td class="nm">'+esc(x.n)+'</td><td>'+x.w.map((w,i)=>w==null?'—':w+(x.yu[i]?'(優)':'')).join('・')+'</td><td>'+(x.ok?'<b class="shu">推薦</b>':'見送り')+(x.yes!=null&&x.yes!==9?'(賛成 '+x.yes+'・反対 '+x.no+')':x.ok?'(満場一致)':'')+'</td></tr>').join('')+'</table></div>';}
const ysK0=kirokuHTML;kirokuHTML=function(){const h=ysK0();const i=h.indexOf('<div class="grid2"><div class="pn"><h2>幕内優勝の歴史');const x=ysLogHTML();return i<0?h+x:h.slice(0,i)+x+h.slice(i);};
</script><style>
.ysc{border:2px solid #c9a24a;border-radius:8px;padding:8px 10px;margin:6px 0;background:linear-gradient(#fffaf0,#f8eed6);color:#1a140c}.ysr{margin-bottom:4px}.yso{background:#7a1d10;color:#fff;border-radius:8px;padding:0 6px;font-size:12px;margin-left:6px}
.ysg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.ysg div{background:#fff;border:1px solid #e2d2a8;border-radius:6px;padding:4px 6px}.ysg small{display:block;font-size:11px;color:#8a7040}.ysg b{font-size:14px}
</style>
