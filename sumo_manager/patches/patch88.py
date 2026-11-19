# v84 -> v85:設定を 1 つにそろえる(ダルマさん「設定を統一する」)
# スタート画面の「設定」も、ゲームの中の「⚙ 設定」も同じ中身・同じ順番:画面の色 → 文字の形 → GitHub の鍵 → 保存データ(ゲームの記録があるとき)→ 不具合の報告 → アプリ。
# スタート画面の「画面の色」ボタンは「設定」にまとめて外す。スタート画面の設定はモーダルではなく 1 枚の画面(押したあともそのまま表示が変わる)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v84</title>', '<title>Grand Sumo Manager v85</title>')
rep("const APPV=84;\nconst SAVE='sumoManager84',SAVE83", "const APPV=85;\nconst SAVE='sumoManager85',SAVE84='sumoManager84',SAVE83")
rep('[SAVE83,SAVE82', '[SAVE84,SAVE83,SAVE82')
rep(" if(g.v===83){g.v=84;}\n return g.v===84?g:null;}", " if(g.v===83){g.v=84;}\n if(g.v===84){g.v=85;}\n return g.v===85?g:null;}")
rep('G={v:84,', 'G={v:85,')
rep('st-tr"><button class="st-upd" onclick="topSettings()">設定</button><button class="st-upd" onclick="skinSheet()">画面の色</button>', 'st-tr"><button class="st-upd" onclick="topSettings()">⚙ 設定</button>')
JS = r'''<script>
/* v85:設定を 1 つに(スタート画面とゲームの中で同じ中身) */
function setBody(){return skinPanel()+fontPanel()+gistKeyHTML()+(G?sysSaveHTML():'')+sysLogHTML()+sysAppHTML();}
sysHTML=function(){return '<div class="pn sysh"><h2>⚙ 設定</h2><p class="kaku mute">画面の色・文字の形・GitHub の鍵・保存データ・不具合の報告・アプリの更新をまとめています。スタート画面の「⚙ 設定」と同じ中身です。</p></div>'+setBody();};
function topSettings(){goStart('set');}
const setR0=render0;render0=function(){if((!G||UI.title)&&UI.start==='set'){document.body.classList.remove('st-top');
  $('#app').innerHTML='<div class="st-bg4"></div><div class="st-wrap wide st-set"><div class="st-h">⚙ 設定</div><button class="st-back" onclick="goStart(null)">← 最初の画面にもどる</button>'+setBody()+'</div>';return;}
 setR0();};
</script>
<style id="setUnify">.st-set .pn{position:relative;z-index:2}</style>
'''
i = s.rfind('</body>')
s = s[:i] + JS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
