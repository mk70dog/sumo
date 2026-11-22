# v129 -> v130:引退の相談の見直し(理由・親方から切り出す・条件付きの「もう一場所」・引退後の道と世話人)。ダルマさん「力士の引退の相談などは」→ 案 →「実施」。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=129;\nconst SAVE='sumoManager129',SAVE128", "const APPV=130;\nconst SAVE='sumoManager130',SAVE129='sumoManager129',SAVE128")
rep('[SAVE128,SAVE127', '[SAVE129,SAVE128,SAVE127')
rep('<title>Grand Sumo Manager v129', '<title>Grand Sumo Manager v130')
core = open(os.path.join(here, 'rt130_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n")
rep(" if(r.h===ME()){\n   if(r.age>=40)p=1;", " if(r.h===ME()){\n   if(rtCheck(r,rc))return;\n   if(r.age>=40)p=1;")
rep("addNews(secondLife(r));}", "if(!rtPathPush(r))addNews(secondLife(r));}")
rep(" stCycle(old,msgs);hySek();\n", " stCycle(old,msgs);hySek();rtCycle();\n")
rep("Object.assign(EVT,ST_EVT);", "Object.assign(EVT,ST_EVT,RT_EVT);")
rep("'_psup','kAuto','skS'];", "'_psup','kAuto','skS','sewa'];")
ui = open(os.path.join(here, 'rt130_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
