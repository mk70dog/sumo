# v208 -> v209:部屋付き親方を一人の人物に(出身地・出身校・性格・つながりで新弟子探し・自分から動く・助言・弟子とのつながり)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=208;\nconst SAVE='sumoManager208',SAVE207", "const APPV=209;\nconst SAVE='sumoManager209',SAVE208='sumoManager208',SAVE207")
rep('[SAVE207,SAVE206', '[SAVE208,SAVE207,SAVE206')
rep('<title>Grand Sumo Manager v208', '<title>Grand Sumo Manager v209')
ui = open(os.path.join(here,'co212_ui.js'),encoding='utf-8').read()
rep('</body>\n</html>', '<script>' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
