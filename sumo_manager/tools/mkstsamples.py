# 見本 st1〜st3:力士の画面の「目標と歩み」(v127 の本体に ST_V を入れて、8 年進めた部屋で表示する)
# 使い方:cd sumo_manager; python3 tools/mkstsamples.py
base=open('sumo_manager_v127.html',encoding='utf-8').read()
N={1:'案1:目標の箱(選び直せる)の下に、歩みを新しい順に並べる',2:'案2:左に目標、右に歩み(2 列)',3:'案3:物語の文章+目標の箱、年表はたたむ'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('伊勢ヶ濱');UI.title=0;UI.start=0;
 for(let b=0;b<48;b++){while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();let g=0;while(G.ev.length&&g++<60)resolveEv(G.ev[0].id,0);if(!nextCycle()){G.ev=[];nextCycle();}}
 const L=own().slice().sort((a,b)=>(b.sto||[]).length-(a.sto||[]).length);go('keiko');window.__id=L[0].id;showR(L[0].id);
 const m=document.querySelector('.stp');if(m)m.scrollIntoView();}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    inj='<script>window.ST_V=%d;</script>'%k
    s=base.replace('<script>\n/* v127 画面',inj+'<script>\n/* v127 画面',1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 st%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v127','<title>見本 st%d'%k,1)
    open('samples/st%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
