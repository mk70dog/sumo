# 見本 top1・top2:スタート画面に「一人相撲」「二人相撲」(ダルマさんの案)。v77 に見本用の表示だけを足す。
base=open('sumo_manager_v77.html',encoding='utf-8').read()
CSS='''<style>
.mode{display:flex;gap:10px;flex:1 1 100%}
.st-go .mode button{flex:1;text-align:center;font-family:Dela,sans-serif;font-size:clamp(22px,6vw,34px);padding:12px 8px;border-radius:10px;border:2px solid #c9a24a;background:#1d1a16cc;color:#f3e7c9;letter-spacing:.15em}
.st-go .mode button.on{background:#9c2a22;color:#fff;border-color:#f3c64a}
.mode button small{display:block;font:12px sans-serif;letter-spacing:0;opacity:.85;margin-top:4px}
.st-go button.big{text-align:center;padding:22px 16px}.st-go button.big b{font-family:Dela,sans-serif;font-size:clamp(34px,7vw,56px);letter-spacing:.2em;font-weight:400}.big2{display:flex;flex-direction:column;gap:14px;max-width:560px;margin:0 auto}
.big2 button{font-family:Dela,sans-serif;font-size:clamp(34px,10vw,56px);padding:18px;border-radius:12px;border:3px solid #c9a24a;background:#1d1a16dd;color:#fff;letter-spacing:.25em}
.big2 button small{display:block;font:14px sans-serif;letter-spacing:0;opacity:.85;margin-top:6px}
.mpo{background:#1d1a16cc;color:#f3e7c9;border:1px solid #c9a24a;border-radius:10px;padding:10px 14px;max-width:700px;margin:0 auto;font-size:14px}
</style>'''
JS=r'''<script>
(function(){const V='__V__';let M='one';
 const opt2='<button class="st-real"><b>親になって新しく始める</b><small>実在の部屋を選んで世界を作ります。合言葉が出るので、相手に伝えます。</small></button><button class="st-dok"><b>合言葉で参加する</b><small>相手から聞いた合言葉を入れて、残りの部屋から選びます。</small></button><button class="st-cont"><b>続きから(二人相撲)</b><small>木瀬部屋 対 伊勢ノ海部屋・2027年 初場所・稽古 第2週/GitHub の鍵は最初に 1 回だけ入れます</small></button>';
 const back='<button class="st-cont" onclick="__m(\'top\')" style="opacity:.85"><b>← 一人相撲・二人相撲を選び直す</b></button>';
 const T=topHTML;
 topHTML=function(){let h=T();const m=h.match(/<div class="st-go">([\s\S]*?)<\/div><div class="st-credit">/);const one=m[1];
  const put=x=>h.replace(m[0],'<div class="st-go">'+x+'</div><div class="st-credit">');
  if(V==='top1'){const sw='<div class="mode"><button class="'+(M==='one'?'on':'')+'" onclick="__m(\'one\')">一人相撲<small>ひとりで部屋を見守る</small></button><button class="'+(M==='two'?'on':'')+'" onclick="__m(\'two\')">二人相撲<small>ふたりで別々の部屋を持つ</small></button></div>';return put(sw+(M==='two'?opt2:one));}
  if(M==='one')return put(back+one);if(M==='two')return put(back+opt2);
  return put('<button class="st-real big" onclick="__m(\'one\')"><b>一人相撲</b><small>ひとりで部屋を見守る</small></button><button class="st-dok big" onclick="__m(\'two\')"><b>二人相撲</b><small>ふたりで別々の部屋を持ち、同じ番付で戦う</small></button>');};
 window.__m=k=>{M=k;render();};if(V==='top2')M='top';
 window.addEventListener('load',()=>setTimeout(()=>{try{localStorage.clear();newGameReal('木瀬');save();UI.title=true;UI.start=null;render();}catch(e){console.error(e)}},300));})();
</script>'''
NOTE={'top1':'top1:上に「一人相撲|二人相撲」の切りかえ。押すと下の選択肢が変わる','top2':'top2:最初は「一人相撲」「二人相撲」の 2 つだけ。押すと次の画面'}
for k,n in NOTE.items():
    s=base.replace('</body>',CSS+JS.replace('__V__',k)+'<div style="position:fixed;left:6px;bottom:6px;background:#000c;color:#fff;font:13px sans-serif;padding:4px 8px;border-radius:6px;z-index:9999">見本 '+n+'</div></body>',1).replace('<title>Sumo Manager v77</title>','<title>見本 %s</title>'%k,1)
    open('samples/%s.html'%k,'w',encoding='utf-8').write(s)
print('ok')
