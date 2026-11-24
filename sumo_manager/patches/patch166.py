# v162 -> v163:稽古の「おすすめをまとめて選ぶ」を直す(ダルマさん「おすすめを選ぶは選択式? 選択できないけど」)。
#   1) 押すと全員の稽古は変わっていたが、ボタンに選んだ印が出ず、押せていないように見えた
#      → 今の全員の稽古がそのおすすめと同じなら、そのボタンを金の枠+「✓ 今これ」にする。押したら「全員を〜にしました」と出す。
#   2) 「親方におまかせ」のとき、おすすめで決めた稽古が「口を出した」扱い(r.kMan)にならず、次の週に親方の決めた稽古で上書きされていた
#      (ひとりずつ・番付ごとのボタン ktSet は v1xx から口を出した扱いにしていたが、ktPre だけ抜けていた)→ ktPre も口を出した扱いにする。
#      「おまかせに戻す」は今までどおり使える。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=162;\nconst SAVE='sumoManager162',SAVE161", "const APPV=163;\nconst SAVE='sumoManager163',SAVE162='sumoManager162',SAVE161")
rep('[SAVE161,SAVE160', '[SAVE162,SAVE161,SAVE160')
rep('<title>Grand Sumo Manager v162', '<title>Grand Sumo Manager v163')
BLOCK = r"""<style>
/* v163 おすすめをまとめて選ぶ:今の選びに印 */
.kpre button.on{border:2px solid var(--kin);background:rgba(201,162,74,.16);box-shadow:inset 0 0 0 1px var(--kin)}
.kpre button .pon{float:right;font-size:11px;font-weight:700;color:var(--kin);margin-left:6px}
</style>
<script>
(function(){
const PN={go:'しっかり鍛える',std:'ふつう',fin:'仕上げ',rest:'休ませる'};
const M={go:r=>r.menu===(r.d<=2?'申':'基')&&r.it===2&&r.pm==='筋',std:r=>r.menu==='申'&&r.it===1&&r.pm==='昼',fin:r=>r.menu==='基'&&r.it===0&&r.pm==='昼',rest:r=>r.menu==='休'&&r.it===0&&r.pm==='治'};
const P0=window.ktPre;
if(typeof P0==='function'){window.ktPre=function(p){if(typeof kcSetMan==='function')kcSetMan(ownAll().map(r=>r.id));const x=P0.apply(this,arguments);if(PN[p]&&typeof toast==='function')toast('全員を「'+PN[p]+'」にしました');return x;};}
const R0=render;
render=function(){const x=R0.apply(this,arguments);try{if(UI.view==='keiko'){const L=ownAll();document.querySelectorAll('.kpre button').forEach(b=>{const k=((b.getAttribute('onclick')||'').match(/ktPre\('(\w+)'\)/)||[])[1];if(!k||!M[k])return;const on=L.length>0&&L.every(M[k]);b.classList.toggle('on',on);if(on&&!b.querySelector('.pon'))b.insertAdjacentHTML('afterbegin','<span class="pon">✓ 今これ</span>');});}}catch(e){console.error(e);}return x;};
})();
</script>
</body>"""
i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i+7:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
