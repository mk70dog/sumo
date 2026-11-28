# v203 -> v204:予定タブ(今場所までの 6 週・1 年のカレンダー。行事と自分の予定を一つにまとめる)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=203;\nconst SAVE='sumoManager203',SAVE202", "const APPV=204;\nconst SAVE='sumoManager204',SAVE203='sumoManager203',SAVE202")
rep('[SAVE202,SAVE201', '[SAVE203,SAVE202,SAVE201')
rep('<title>Grand Sumo Manager v203', '<title>Grand Sumo Manager v204')
rep("['keiko','稽古'],['basho','本場所']", "['keiko','稽古'],['yotei','予定'],['basho','本場所']")
rep("kiroku:kirokuHTML};", "kiroku:kirokuHTML,yotei:()=>calHTML()};")
rep("#nav{display:grid;grid-template-columns:repeat(9,1fr)", "#nav{display:grid;grid-template-columns:repeat(10,1fr)")
ui = open(os.path.join(here,'cal207_ui.js'),encoding='utf-8').read()
rep('</body>\n</html>', '<script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
