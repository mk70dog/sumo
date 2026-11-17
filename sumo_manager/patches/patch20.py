# 部屋の所在地・創設・沿革・規模  v16 -> v17
import os
import sys,json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(old,new,n=1):
    global s
    c=s.count(old)
    if c!=n: raise SystemExit('一致数 %d (期待 %d): %r'%(c,n,old[:80]))
    s=s.replace(old,new)
rows=[l.split('|') for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','heya2026.txt'),encoding='utf-8').read().strip().split('\n')]
assert len(rows)==45
HD=json.dumps({r[0]:[r[1],int(r[2]),r[3]] for r in rows},ensure_ascii=False)
rep('<title>Sumo Manager v16</title>','<title>Sumo Manager v17</title>')
rep("const SAVE='sumoManager16',SAVE15","const SAVE='sumoManager17',SAVE16='sumoManager16',SAVE15")
rep('[SAVE15,SAVE14','[SAVE16,SAVE15,SAVE14')
rep("if(g.v===15){mig16(g);g.v=16;}\n return g.v===16?g:null;}","if(g.v===15){mig16(g);g.v=16;}\n if(g.v===16){mig17(g);g.v=17;}\n return g.v===17?g:null;}")
rep('G={v:16,','G={v:17,')
CORE=r"""/* v17: 部屋の所在地・創設・沿革(2026 年 10 月時点。所在地は土俵の目撃者「相撲部屋 一門 相関図」、創設と沿革は Wikipedia "List of sumo stables" などから要約) */
const HEYAD=__HD__;
const LOCP=['東京都墨田区','東京都江東区','東京都葛飾区','東京都江戸川区','東京都足立区','東京都台東区','千葉県船橋市','埼玉県川口市','茨城県つくば市'];
function curYear(){return (G.y0||2026)+Math.floor(((G.bnum||1)-1)/6);}
function heyaInfoInit(g){const X=g||G;X.heya.forEach((h,i)=>{const d=X.real&&!h.ob?HEYAD[h.n]:null;
 if(d){h.loc=d[0];h.est=d[1];h.hist=d[2];}else if(!h.loc){h.loc=pick(LOCP);h.est=h.ob?((X.y0||2026)+Math.floor((h.ob-1)/6)):RI(1950,2020);h.hist=h.hist||'';}});}
function mig17(g){heyaInfoInit(g);}
function locF(h){const l=(h&&h.loc)||'';return /墨田区|江東区|中央区|台東区|文京区/.test(l)?1.15:/東京都/.test(l)?1:.75;}
function locS(l){return String(l||'').replace(/^東京都/,'');}
function heyaSize(n){return n>=25?'大きな部屋':n>=15?'中くらいの部屋':n>=8?'小さめの部屋':'小さな部屋';}
function heyaInfoHTML(i){const h=G.heya[i];if(!h)return '';const cnt=heyaCnt();const n=cnt[i]||0;const sek=G.order.filter(id=>{const r=G.R[id];return r.h===i&&!r.ret&&r.d<=1;}).length;
 const rk=Object.keys(cnt).filter(k=>!G.heya[k].closed).map(k=>cnt[k]||0).filter(x=>x>n).length+1;
 return '<dl class="kv"><dt>所在地</dt><dd>'+esc(h.loc||'—')+'</dd><dt>創設</dt><dd>'+(h.est?h.est+' 年':'—')+'</dd><dt>沿革</dt><dd>'+esc(h.hist||'—')+'</dd><dt>規模</dt><dd>力士 '+n+' 人(関取 '+sek+' 人)・'+heyaSize(n)+'。人数は全部屋で '+rk+' 番目</dd></dl>';}
function showHeya(i){const h=G.heya[i];if(!h)return;openM('<h2>'+esc(h.n)+'部屋</h2><p class="kaku">'+(h.ic>=0?esc(IC[h.ic])+'一門・':'')+'師匠 '+esc(h.o2?'元・'+h.o2:(h.o||''))+'</p>'+heyaInfoHTML(i)+'<button class="btn main" onclick="closeM()">閉じる</button>');}
function heyaListPanel(){const cnt=heyaCnt();const L=G.heya.map((h,i)=>[h,i]).filter(x=>!x[0].closed).sort((a,b)=>(cnt[b[1]]||0)-(cnt[a[1]]||0));
 return '<div class="pn"><h2>相撲部屋の一覧<span class="sub">'+L.length+' 部屋・人数の多い順</span></h2><div style="overflow-x:auto"><table class="tb"><tr><th>部屋</th><th class="hide-s">一門</th><th>所在地</th><th class="num">創設</th><th class="num">力士</th></tr>'+
  L.map(([h,i])=>'<tr class="clk'+(i===0?' me':'')+'" onclick="showHeya('+i+')"><td class="nm">'+esc(h.n)+'</td><td class="hide-s">'+(h.ic>=0?esc(IC[h.ic]):'無所属')+'</td><td>'+esc(locS(h.loc))+'</td><td class="num">'+(h.est||'—')+'</td><td class="num">'+(cnt[i]||0)+'</td></tr>').join('')+'</table></div><p class="kaku mute" style="font-size:13px">部屋名を押すと、沿革と規模が見られます。所在地・創設・沿革は 2026 年 10 月時点の実在の部屋のもので、ゲームの途中でできた部屋は架空です。</p></div>';}
"""
CORE=CORE.replace('__HD__',HD)
rep('function B_rec(r)',CORE+'function B_rec(r)')
# 家賃・修繕費は場所で変わる
rep("function bldCost(){const b=G.bld||{k:'own'};return b.k==='rent'?60+G.fac.shuku*15:20+G.fac.shuku*6;}",
    "function bldCost(){const b=G.bld||{k:'own'};return Math.round((b.k==='rent'?60+G.fac.shuku*15:20+G.fac.shuku*6)*locF(G.heya[0]));}")
# 独立した部屋の所在地・沿革
rep("G.heya.push(h);const k=G.heya.length-1;G.hs.tot[k]=0;",
    "h.loc=pick(LOCP);h.est=curYear();h.hist=(src?src.n:me().n)+'部屋から独立して創設。';G.heya.push(h);const k=G.heya.length-1;G.hs.tot[k]=0;")
# 開始時
rep(" G.tkPol='old';G.rel={};G.ama=null;amaInit();mig11(G);mig12(G);myoInit(G);refreshMyo();",
    " G.tkPol='old';G.rel={};G.ama=null;amaInit();mig11(G);mig12(G);myoInit(G);refreshMyo();heyaInfoInit(G);")
rep("myoInit(G);refreshMarket();refreshMyo();G.okami=mkOkami();","myoInit(G);heyaInfoInit(G);refreshMarket();refreshMyo();G.okami=mkOkami();")
# 画面
rep(" h+=hsPanel();h+=kyuPanel();"," h+=hsPanel();h+=heyaListPanel();h+=kyuPanel();")
rep("h+=icPanel()+myoPanel();","h+='<div class=\"pn\"><h2>部屋のあらまし</h2>'+heyaInfoHTML(0)+'<p class=\"kaku mute\" style=\"font-size:13px\">家賃や建物の費用は場所で変わります(両国に近い都心は高め、都外は安め)。</p></div>';h+=icPanel()+myoPanel();")
open(dst,'w',encoding='utf-8').write(s);print('ok',len(s))
