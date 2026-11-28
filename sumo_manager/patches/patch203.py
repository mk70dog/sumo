# v199 -> v200:親方・おかみさん・部屋付き親方・トレーナーの得意を表示、経験で増える
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=199;\nconst SAVE='sumoManager199',SAVE198", "const APPV=200;\nconst SAVE='sumoManager200',SAVE199='sumoManager199',SAVE198")
rep('[SAVE198,SAVE197', '[SAVE199,SAVE198,SAVE197')
rep('<title>Grand Sumo Manager v199', '<title>Grand Sumo Manager v200')

# v200:得意の表示と経験での伸び(年に 1 回 tokYear)
rep("G.sup+=(G._psup||0);","G.sup+=(G._psup||0);if(G.bnum%6===0)try{tokYear();}catch(e){}")
ui = open(os.path.join(here,'tok200_ui.js'),encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
