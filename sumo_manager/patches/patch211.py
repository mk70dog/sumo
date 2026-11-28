# v207 -> v208:新弟子候補に会いに行く(前回との違い・見立ての記録・見る人のくせ・親方が行く効き目・遠方は 2 週)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=207;\nconst SAVE='sumoManager207',SAVE206", "const APPV=208;\nconst SAVE='sumoManager208',SAVE207='sumoManager207',SAVE206")
rep('[SAVE206,SAVE205', '[SAVE207,SAVE206,SAVE205')
rep('<title>Grand Sumo Manager v207', '<title>Grand Sumo Manager v208')
ui = open(os.path.join(here,'vis211_ui.js'),encoding='utf-8').read()
rep('</body>\n</html>', '<script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
