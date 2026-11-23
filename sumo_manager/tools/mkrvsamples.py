# 見本 rv1・rv2:力士の画面の「ライバル」(札/表)。本場所の「因縁の一番」と記録の「土俵の時代」はどちらも同じ。
# 使い方:cd sumo_manager; python3 tools/mkrvsamples.py
base=open('sumo_manager_v132.html',encoding='utf-8').read()
N={1:'案1:ライバルを札で(対戦成績を大きく・直近の結果・きっかけ)',2:'案2:ライバルを表で 1 行ずつ'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('伊勢ヶ濱');UI.title=0;UI.start=0;
 for(let b=0;b<30;b++){while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();let g=0;while(G.ev.length&&g++<60)resolveEv(G.ev[0].id,0);if(!nextCycle()){G.ev=[];nextCycle();}}
 const o=own().filter(r=>r.d<=1);let r=o.find(x=>rvOf(x).length)||o[0];if(!rvOf(r).length){const y=G.order.map(i=>G.R[i]).find(x=>x.d<=1&&x.h!==r.h);G.rv.push({a:r.id,b:y.id,b0:G.bnum-3,k:'doki'});r.h2h=r.h2h||{};r.h2h[y.id]=r.h2h[y.id]||[5,4];r.h2r=r.h2r||{};r.h2r[y.id]='oxoox';}
 const y=G.order.map(i=>G.R[i]).find(x=>x.d<=1&&x.h!==r.h&&!rvPair(r,x));G.rv.push({a:r.id,b:y.id,b0:G.bnum-8,k:'yu'});r.h2h[y.id]=[7,8];r.h2r[y.id]='xxoxo';
 if(!G.era.length)G.era.push({n:'見本時代',a:r.id,b:y.id,an:r.n,bn:y.n,b0:G.bnum-6,b1:G.bnum});
 go('keiko');showR(r.id);const m=document.querySelector('.rvp');if(m)m.scrollIntoView();window.__ok=1;}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    s=base.replace('<script>\n/* v132 画面','<script>window.RV_V=%d;</script><script>\n/* v132 画面'%k,1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 rv%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v132','<title>見本 rv%d'%k,1)
    open('samples/rv%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
