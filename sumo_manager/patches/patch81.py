# v77 -> v78:スタート画面に「一人相撲」「二人相撲」(見本 top2、ダルマさんの案と選択)
# 最初は 2 つだけ。一人相撲を押すと今までの選択肢(続きから・実在の部屋・独立)、二人相撲は準備中(次の段階で作る)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v77</title>', '<title>Sumo Manager v78</title>')
rep("const APPV=77;\nconst SAVE='sumoManager77',SAVE76", "const APPV=78;\nconst SAVE='sumoManager78',SAVE77='sumoManager77',SAVE76")
rep('[SAVE76,SAVE75', '[SAVE77,SAVE76,SAVE75')
rep(" if(g.v===76){g.v=77;}\n return g.v===77?g:null;}", " if(g.v===76){g.v=77;}\n if(g.v===77){g.v=78;}\n return g.v===78?g:null;}")
rep('G={v:77,', 'G={v:78,')
rep("function topHTML(){return", "function topHTML1(){return")
TOP = r'''function topHTML(){const h=topHTML1();const m=h.match(/<div class="st-go">([\s\S]*?)<\/div><div class="st-credit">/);if(!m)return h;
 const put=x=>h.replace(m[0],'<div class="st-go">'+x+'</div><div class="st-credit">');
 const back='<button class="st-cont st-back2" onclick="topMode(null)"><b>← 一人相撲・二人相撲を選び直す</b></button>';
 if(UI.mode==='one')return put(back+m[1]);
 if(UI.mode==='two')return put(back+'<button class="st-real" disabled style="opacity:.6"><b>親になって新しく始める</b><small>準備中です。次の段階で遊べるようになります。</small></button><button class="st-dok" disabled style="opacity:.6"><b>合言葉で参加する</b><small>準備中です。</small></button>');
 return put('<button class="st-real big st-one" onclick="topMode(\'one\')"><b>一人相撲</b><small>ひとりで部屋を見守る</small></button><button class="st-dok big st-two" onclick="topMode(\'two\')"><b>二人相撲</b><small>ふたりで別々の部屋を見守り、同じ番付で戦う(準備中)</small></button>');}
function topMode(k){UI.mode=k;render();window.scrollTo(0,0);}
'''
rep("function nightHTML(body){", TOP + "function nightHTML(body){")
rep("function quitTop(){save();UI.title=true;UI.start=null;", "function quitTop(){save();UI.title=true;UI.start=null;UI.mode=null;")
CSS = "<style id=\"topMode\">.st-go button.big{text-align:center;padding:22px 16px}.st-go button.big b{font-family:Dela,sans-serif;font-size:clamp(34px,7vw,56px);letter-spacing:.2em;font-weight:400}.st-go button.big small{letter-spacing:.1em}.st-go .st-back2{opacity:.85;padding:8px 16px}.st-go .st-back2 b{font-size:clamp(14px,2vw,18px);margin:0}</style>\n"
i = s.rfind('</body>')
s = s[:i] + CSS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
