# 見本 co1・co2:スタッフの画面の「こんな親方に来てほしい」と、部屋付き親方の札(現役の取り口・指導の色・人柄・教え方・来てくれる見込み)。
# 使い方:cd sumo_manager; python3 tools/mkcosamples.py
base=open('sumo_manager_v131.html',encoding='utf-8').read()
N={1:'案1:条件のボタンを並べ、押すと声をかける',2:'案2:条件を選ぶ欄と「声をかける」ボタン 1 つ'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;G.money=3000;coReqSet('osh');
 while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();G.ev=[];nextCycle();go('staff');const m=document.querySelector('.cop');if(m)m.scrollIntoView();window.__ok=1;}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    s=base.replace('<script>\n/* v131 画面','<script>window.CO_V=%d;</script><script>\n/* v131 画面'%k,1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 co%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v131','<title>見本 co%d'%k,1)
    open('samples/co%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
