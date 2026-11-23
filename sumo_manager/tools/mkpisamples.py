# 見本 pi1〜pi3:力士の画面の絵の置き方。スタッフの画面(桐山親方)はどれも同じ。
# 使い方:cd sumo_manager; python3 tools/mkpisamples.py
base=open('sumo_manager_v135.html',encoding='utf-8').read()
N={1:'案1:縦の名札の代わりに絵(下に四股名)',2:'案2:絵と縦の名札を並べる',3:'案3:右上に小さな絵'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('伊勢ヶ濱');UI.title=0;UI.start=0;
 const r=G.order.map(i=>G.R[i]).find(x=>x.n===(location.hash.slice(1)?decodeURIComponent(location.hash.slice(1)):'錦富士'));go('rikishi');showR(r.id);window.__ok=1;}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    s=base.replace('<script>\n/* v135:','<script>window.PI_V=%d;</script><script>\n/* v135:'%k,1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 pi%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v135','<title>見本 pi%d'%k,1)
    open('samples/pi%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
