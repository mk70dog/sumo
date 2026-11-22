# 見本 rt1・rt2:力士の画面の「引退について」。v130 の本体に RT_V を入れて表示する。
# 使い方:cd sumo_manager; python3 tools/mkrtsamples.py
base=open('sumo_manager_v130.html',encoding='utf-8').read()
N={1:'案1:「引退について」の欄をいつも出す(様子・思っていること・約束・3 つのボタン)',2:'案2:ふだんはたたみ、見出しに様子だけ。引退が頭をよぎっている力士は開いておく'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;
 go('rikishi');const r=own().sort((a,b)=>b.age-a.age)[0];r.mor=25;showR(r.id);const m=document.querySelector('.rtp');if(m)m.scrollIntoView();window.__ok=1;}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    s=base.replace('<script>\n/* v130 画面','<script>window.RT_V=%d;</script><script>\n/* v130 画面'%k,1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 rt%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v130','<title>見本 rt%d'%k,1)
    open('samples/rt%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
