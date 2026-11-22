# 見本 tk1〜tk3:力士の画面の「型づくり」と稽古の札の「型」。v129 の本体に TK_V を入れて、3 年進めた部屋で表示する。
# 使い方:cd sumo_manager; python3 tools/mktksamples.py
base=open('sumo_manager_v129.html',encoding='utf-8').read()
N={1:'案1:型の名前・段階の帯・完成度の棒・型を選ぶボタン(相性つき)',2:'案2:1 行にまとめ、型を選ぶボタンはたたむ',3:'案3:完成度を大きな札で見せ、いま伸ばしているものと取組での効き目を説明'}
JS=r'''<script>
window.addEventListener('load',()=>{setTimeout(()=>{try{localStorage.clear();newGameReal('二所ノ関');UI.title=0;UI.start=0;
 for(let b=0;b<18;b++){while(G.phase==='train')doWeek();while(G.phase==='basho')advanceDay();let g=0;while(G.ev.length&&g++<60)resolveEv(G.ev[0].id,0);if(!nextCycle()){G.ev=[];nextCycle();}}
 go('keiko');const r=own().filter(x=>x.tk).sort((a,b)=>Math.abs(a.tk.v-50)-Math.abs(b.tk.v-50))[0]||own()[0];showR(r.id);const m=document.querySelector('.tkp');if(m)m.scrollIntoView();window.__ok=1;}catch(e){console.error(e)}},300);});
</script>'''
for k,n in N.items():
    s=base.replace('<script>\n/* v129 画面','<script>window.TK_V=%d;</script><script>\n/* v129 画面'%k,1).replace('</body>\n</html>',JS+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999;max-width:60vw">見本 tk%d:%s</div></body>\n</html>'%(k,n),1).replace('<title>Grand Sumo Manager v129','<title>見本 tk%d'%k,1)
    open('samples/tk%d.html'%k,'w',encoding='utf-8').write(s)
print('ok')
