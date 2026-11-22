# 見本 hy1〜hy3:記録の画面の「部屋の歩み」(殿堂・年表・部屋の記録・歴代の関取)。v128 の本体に HY_V を入れて、15 年進めた部屋で表示する。
# 使い方:cd sumo_manager; python3 tools/mkhysamples.py
base=open('sumo_manager_v128.html',encoding='utf-8').read()
N={1:'案1:殿堂の札 → 部屋の記録 → 年表(新しい年から)、歴代の関取はたたむ',2:'案2:殿堂・年表・歴代の関取・部屋の記録を上のボタンで切りかえ',3:'案3:殿堂の札の下に、左に年表・右に記録と歴代の関取(2 列)'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('伊勢ヶ濱');UI.title=0;UI.start=0;
 for(let b=0;b<90;b++){while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();let g=0;while(G.ev.length&&g++<60)resolveEv(G.ev[0].id,0);if(!nextCycle()){G.ev=[];nextCycle();}}
 UI.hyT='nen';go('kiroku');window.__ok=1;}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    s=base.replace('<script>\n/* v128 画面','<script>window.HY_V=%d;</script><script>\n/* v128 画面'%k,1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 hy%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v128','<title>見本 hy%d'%k,1)
    open('samples/hy%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
