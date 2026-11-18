# 決まり手の表示を「縦書きの札(めくり)+筆文字」に(見本 kaiga25、字は佑字 肅)  v53 -> v54
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v53</title>', '<title>Sumo Manager v54</title>')
rep("const APPV=53;\nconst SAVE='sumoManager53',SAVE52", "const APPV=54;\nconst SAVE='sumoManager54',SAVE53='sumoManager53',SAVE52")
rep('[SAVE52,SAVE51', '[SAVE53,SAVE52,SAVE51')
rep(" if(g.v===52){g.v=53;}\n return g.v===53?g:null;}", " if(g.v===52){g.v=53;}\n if(g.v===53){g.v=54;}\n return g.v===54?g:null;}")
rep('G={v:53,', 'G={v:54,')
rep("q('.stt').textContent=pl.k;st.setAttribute('transform','translate(0,-70) rotate(-6)');st.setAttribute('opacity',1);wr.classList.add('boom');",
    "{const o=wr.querySelector('.kmo');if(o)o.remove();wr.insertAdjacentHTML('beforeend','<div class=\"kmo'+(lo[0]>0?' l':'')+'\"><b>'+esc(pl.k)+'</b><span>'+esc(pl.WN)+'</span></div>');}wr.classList.add('boom');")
rep("wr.classList.remove('shake','boom');", "wr.classList.remove('shake','boom');{const o=wr.querySelector('.kmo');if(o)o.remove();}")
rep("'.dhbox{display:grid;", "'.dhw .kmo{position:absolute;right:5%;top:0;width:13%;min-width:52px;max-width:84px;height:60%;background:linear-gradient(90deg,#e9d7ae,#f6ead0 45%,#e2cfa2);border:3px solid #5a3a1a;border-radius:4px;box-shadow:3px 6px 10px rgba(0,0,0,.35);writing-mode:vertical-rl;display:flex;align-items:center;justify-content:center;gap:8px;padding:10px 0;animation:dhk .55s cubic-bezier(.3,1.4,.5,1) forwards;transform:translateY(-110%);z-index:2}.dhw .kmo:before{content:\"\";position:absolute;top:-30px;left:50%;width:2px;height:30px;background:#5a3a1a}.dhw .kmo b{font:min(34px,6.5vw) YSk,serif;color:#141210;letter-spacing:3px}.dhw .kmo span{font:min(17px,3.6vw) YSk,serif;color:#b5361f;letter-spacing:2px}@keyframes dhk{to{transform:translateY(8%)}}.dhw .kmo.l{right:auto;left:5%}.dhbox{display:grid;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
