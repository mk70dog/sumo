# v126 -> v127:弟子ひとりひとりの物語(目標・壁・転機・歩み)。ダルマさん「他に重視する項目は?」→ 提案 →「お任せで実施」。
# 計算は patches/st127_core.js、画面は patches/st127_ui.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=126;\nconst SAVE='sumoManager126',SAVE125", "const APPV=127;\nconst SAVE='sumoManager127',SAVE126='sumoManager126',SAVE125")
rep('[SAVE125,SAVE124', '[SAVE126,SAVE125,SAVE124')
rep('<title>Grand Sumo Manager v126', '<title>Grand Sumo Manager v127')
core = open(os.path.join(here, 'st127_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n kcWeek();\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n kcWeek();\n")
rep("if(isOwn)gm*=coMul(r);gm*=kcG(r);", "if(isOwn)gm*=coMul(r);gm*=kcG(r)*stG(r);")
rep(" G.news=msgs;msgs.forEach(m=>addNews(m));});", " stCycle(old,msgs);\n G.news=msgs;msgs.forEach(m=>addNews(m));});")
rep("/* ========== 画面", "Object.assign(EVT,ST_EVT);\n/* ========== 画面")
rep("bca:1,bcp:1,kMan:1};", "bca:1,bcp:1,kMan:1,mkP:1};")
rep("  h+=hyoPanel(r);\n", "  h+=hyoPanel(r);h+=stHTML(r);\n")
ui = open(os.path.join(here, 'st127_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
