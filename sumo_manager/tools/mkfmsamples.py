# 見本 fm1・fm2:力士の画面の「暮らし」(表/小さな札)。
# 使い方:cd sumo_manager; python3 tools/mkfmsamples.py
base=open('sumo_manager_v133.html',encoding='utf-8').read()
N={1:'案1:「暮らし」を表で(住まい・家族・個人後援会・お金)',2:'案2:「暮らし」を小さな札 4 枚で'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');UI.title=0;UI.start=0;
 const r=own().sort((a,b)=>a.pos-b.pos)[0];r.mar=G.bnum;r.muko=1;r.kids=[{b:G.bnum,boy:1}];r.fk=G.bnum;r.inc={tot:520};r.cash=800;r.pop=45;
 go('rikishi');showR(r.id);const m=document.querySelector('.fmp');if(m)m.scrollIntoView();window.__ok=1;}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    s=base.replace('<script>\n/* v133 画面','<script>window.FM_V=%d;</script><script>\n/* v133 画面'%k,1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 fm%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v133','<title>見本 fm%d'%k,1)
    open('samples/fm%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
