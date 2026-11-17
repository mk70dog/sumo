# オフラインでも遊べるように(サービスワーカー)  v37 -> v38
# リポジトリ直下に sw.js を置き(このパッチの外。sumo/sw.js)、ゲームを https で開いたときに登録する。
# sw.js:ネット優先・つながらないときだけ保存したものを出す。Sumo Manager のファイルだけを扱い、judge/ には何もしない。
# 「アプリを更新」はオフラインのとき「ネットにつながっていないため確かめられません」と出す。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v37</title>', '<title>Sumo Manager v38</title>')
rep("const APPV=37;\nconst SAVE='sumoManager37',SAVE36", "const APPV=38;\nconst SAVE='sumoManager38',SAVE37='sumoManager37',SAVE36")
rep('[SAVE36,SAVE35', '[SAVE37,SAVE36,SAVE35')
rep(" if(g.v===36){g.v=37;}\n return g.v===37?g:null;}", " if(g.v===36){g.v=37;}\n if(g.v===37){g.v=38;}\n return g.v===38?g:null;}")
rep('G={v:37,', 'G={v:38,')
rep(" fetch('latest.json?t='+Date.now(),{cache:'no-store'})",
    " if(navigator.onLine===false){if(manual)alertM('更新を確かめられません','ネットにつながっていないため確かめられません。いまの版(v'+APPV+')のまま遊べます。');return;}\n fetch('latest.json?t='+Date.now(),{cache:'no-store'})")
rep("保存データはそのまま引き継がれます。</p><div class=\"btns\"><button class=\"btn main\" onclick=\"checkUpd(1)\">アプリを更新</button></div></div>';",
    "保存データはそのまま引き継がれます。一度ネットにつないで開いたあとは、オフラインでも遊べます。</p><div class=\"btns\"><button class=\"btn main\" onclick=\"checkUpd(1)\">アプリを更新</button></div></div>';")
rep("render();\ncheckUpd(0);\n</script>", "render();\ncheckUpd(0);\nif('serviceWorker' in navigator&&location.protocol==='https:'){navigator.serviceWorker.register('../sw.js',{scope:'../'}).catch(()=>{});}\n</script>")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
