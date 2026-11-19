# 見本 jo1〜2:幕内上位(結び前)の取組にも予想印+メディアの表に新聞の「予想の腕」(v67 に見本用の script を足す)
base=open('sumo_manager_v67.html',encoding='utf-8').read()
JS=r'''
<style>
.jor{display:grid;grid-template-columns:1fr auto 1fr;gap:6px;align-items:center;padding:6px 2px;border-bottom:1px dashed var(--line);font-size:14px}
.jor .r{text-align:right}.jor .mm{font-size:12px;color:var(--mute);white-space:nowrap}.jor .mm b{font-size:15px;font-family:serif}
.jor .sm{font-size:11px;color:var(--mute)}
</style>
<script>
(function(){
const V=__V__;
const AB=['日','角','裏'];
const cl2=(i)=>['m0','m1','m2','m3','m4'][i];
function topPairs(){const B=G.B;if(!B||!B.cur)return [];return B.cur.filter(p=>{const a=G.R[p[0]],b=G.R[p[1]];return a&&b&&a.d===0&&b.d===0&&a.h!==0&&b.h!==0&&!B.rec[a.id].ky&&!B.rec[b.id].ky;}).sort((x,y)=>Math.min(G.R[x[0]].pos,G.R[x[1]].pos)-Math.min(G.R[y[0]].pos,G.R[y[1]].pos)).slice(0,5);}
function rowsV1(){return topPairs().map(p=>{const a=G.R[p[0]].pos<G.R[p[1]].pos?G.R[p[0]]:G.R[p[1]],o=a===G.R[p[0]]?G.R[p[1]]:G.R[p[0]];const ps=PAP.map((x,k)=>est(a,o,k));
 const ma=ps.map((q,k)=>AB[k]+'<b class="mk '+cl2(mk(q))+'" style="font-size:15px">'+MK[mk(q)]+'</b>').join(' '),mo=ps.map((q,k)=>AB[k]+'<b class="mk '+cl2(mk(1-q))+'" style="font-size:15px">'+MK[mk(1-q)]+'</b>').join(' ');
 const B=G.B;return '<div class="jor"><div><span class="nm clk2" onclick="showR('+a.id+')">'+esc(a.n)+'</span> <span class="sm">'+esc(a.rkS)+'・'+B.rec[a.id].w+'勝'+B.rec[a.id].l+'敗</span><div class="mm">'+ma+'</div></div><div class="vs" style="color:var(--shu)">対</div><div class="r"><span class="nm clk2" onclick="showR('+o.id+')">'+esc(o.n)+'</span> <span class="sm">'+esc(o.rkS)+'・'+B.rec[o.id].w+'勝'+B.rec[o.id].l+'敗</span><div class="mm">'+mo+'</div></div></div>';}).join('');}
function rowsV2(){return topPairs().map(p=>{const a=G.R[p[0]].pos<G.R[p[1]].pos?G.R[p[0]]:G.R[p[1]],o=a===G.R[p[0]]?G.R[p[1]]:G.R[p[0]];const ps=PAP.map((x,k)=>est(a,o,k));
 return '<div class="nx"><div class="nxm"><div><span class="nm">'+esc(a.n)+'</span><div class="mute" style="font-size:12px">'+esc(a.rkS)+'・'+esc(G.heya[a.h].n)+'</div></div><div class="vs">対</div><div><span class="nm">'+esc(o.n)+'</span><div class="mute" style="font-size:12px">'+esc(o.rkS)+'・'+esc(G.heya[o.h].n)+'</div></div></div><table class="yt"><tr><th></th><th>'+esc(a.n)+'</th><th>'+esc(o.n)+'</th></tr>'+PAP.map((x,k)=>'<tr><td>'+x[0]+'</td><td>'+mkS(mk(ps[k]))+'</td><td>'+mkS(mk(1-ps[k]))+'</td></tr>').join('')+'</table></div>';}).join('');}
const ob=bashoHTML;bashoHTML=function(){const d=document.createElement('div');d.innerHTML=ob();if(!G.B||G.phase!=='basho')return d.innerHTML;
 const pn=[...d.querySelectorAll('.pn')].find(e=>/日目の取組/.test((e.querySelector('h2')||{}).textContent||''));const day=(G.B.day||0)+1;
 const h=V===1?'<div class="pn"><h2>幕内上位の取組<span class="sub">'+day+'日目・結び前 5 番(日=相撲日報・角=スポーツ角界・裏=週刊土俵裏)</span></h2>'+rowsV1()+'</div>'
  :'<div class="pn"><details><summary style="font-weight:700;cursor:pointer">幕内上位の取組と新聞の印('+day+'日目・結び前 5 番)</summary>'+rowsV2()+'</details></div>';
 if(pn)pn.insertAdjacentHTML('afterend',h);return d.innerHTML;};
// メディアの表に「予想の腕」
const om=mediaHTML;mediaHTML=function(){const d=document.createElement('div');d.innerHTML=om();const y=G.yoso;const t=d.querySelectorAll('table.tb');const tb=t[t.length-1];if(!tb)return d.innerHTML;
 const hr=tb.querySelector('tr');if(hr)hr.insertAdjacentHTML('beforeend','<th>予想の腕</th>');
 [...tb.querySelectorAll('tr')].slice(1).forEach(tr=>{const nm=tr.children[1]?tr.children[1].textContent:'';const k=PAP.findIndex(p=>nm.indexOf(p[0])>=0);let c='<td class="mute">―</td>';
  if(k>=0){const s=y&&y.t&&y.t[k];if(s&&s.n>=20){const p=s.h/s.n;const st=p>=.68?5:p>=.62?4:p>=.56?3:p>=.5?2:1;c='<td>'+mStars(st)+' <span style="font-size:12px">'+Math.round(p*100)+'%</span></td>';}else c='<td class="mute" style="font-size:12px">まだ少ない</td>';}
  tr.insertAdjacentHTML('beforeend',c);});
 tb.insertAdjacentHTML('afterend','<p class="mute kaku" style="font-size:12px">「予想の腕」は取組前の予想印の通算の当たり(20 番以上で表示)。うわさの確かさ(左の★)とは別です。</p>');return d.innerHTML;};
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;
 for(let s=0;s<2;s++){while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();while(G.ev.length)resolveEv(G.ev[0].id,0);nextCycle();}
 while(G.phase==='train')doWeek();for(let i=0;i<5;i++)advanceDay();UI.bouts=advanceDay();
 go(location.hash==='#k'?'kiroku':'basho');}catch(e){console.error(e)}},80);});
})();
</script>
'''
NOTE={1:'jo1:部屋の取組の下に「幕内上位の取組」(結び前 5 番、1 行ずつ・3 紙の印を略して並べる)+メディアの表に「予想の腕」',
2:'jo2:「幕内上位の取組と新聞の印」を開くと yoso1 と同じ表(ふだんは閉じている)+メディアの表に「予想の腕」'}
for v in (1,2):
    s=base.replace('</body>',JS.replace('__V__',str(v))+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+NOTE[v]+'</div></body>',1).replace('<title>Sumo Manager v67</title>','<title>見本 jo%d</title>'%v,1)
    open('samples/jo%d.html'%v,'w',encoding='utf-8').write(s)
print('ok')
