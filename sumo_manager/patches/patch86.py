# v82 -> v83:①題字が大きすぎて錦絵の力士の顔が隠れるので小さく(画面の高さにも合わせる) ②スタート画面の右上に「設定」(GitHub の鍵など)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v82</title>', '<title>Grand Sumo Manager v83</title>')
rep("const APPV=82;\nconst SAVE='sumoManager82',SAVE81", "const APPV=83;\nconst SAVE='sumoManager83',SAVE82='sumoManager82',SAVE81")
rep('[SAVE81,SAVE80', '[SAVE82,SAVE81,SAVE80')
rep(" if(g.v===81){g.v=82;}\n return g.v===82?g:null;}", " if(g.v===81){g.v=82;}\n if(g.v===82){g.v=83;}\n return g.v===83?g:null;}")
rep('G={v:82,', 'G={v:83,')
rep('st-tr"><button class="st-upd" onclick="skinSheet()">画面の色</button>', 'st-tr"><button class="st-upd" onclick="topSettings()">設定</button><button class="st-upd" onclick="skinSheet()">画面の色</button>')
JS = r'''<script>
/* v83:スタート画面の設定(GitHub の鍵・字の大きさなど) */
function topSettings(){openM('<button class="btn sm x" onclick="closeM()">閉じる</button><h2>設定</h2>'+gistKeyHTML()+'<p class="mute kaku" style="font-size:12px">画面の色は右上の「画面の色」から。保存データの書き出し・読み込みは、ゲームを始めてから「⚙ 設定」で行えます。</p>');}
const tsClr=gistClear;gistClear=function(){tsClr();if(document.querySelector('#mdl.on,#mdl[open]')||UI.title)topSettings();};
</script>
<style id="ttlFit">.t1 b{font-size:min(10.5vw,12vh,120px)!important}.t1 small{font-size:min(2.4vw,2.6vh,22px)!important}.t1{padding:min(1.4vh,12px) min(4vw,40px) min(1.6vh,14px)!important}
.st-title{top:min(5vh,6%)!important}</style>
'''
i = s.rfind('</body>')
s = s[:i] + JS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
