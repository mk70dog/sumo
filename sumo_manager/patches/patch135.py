# v131 -> v132:ライバルと「○○時代」(ダルマさん「ライバルと相性」を選ぶ → 設計案 →「実施」)。計算は patches/rv132_core.js、画面は patches/rv132_ui.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=131;\nconst SAVE='sumoManager131',SAVE130", "const APPV=132;\nconst SAVE='sumoManager132',SAVE131='sumoManager131',SAVE130")
rep('[SAVE130,SAVE129', '[SAVE131,SAVE130,SAVE129')
rep('<title>Grand Sumo Manager v131', '<title>Grand Sumo Manager v132')
core = open(os.path.join(here, 'rv132_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n")
rep("r._pr+=kenB(r)+aikuchi(r,o)+", "r._pr+=kenB(r)+aikuchi(r,o)+rvB(r,o)+")
rep("r.h2r[o.id]=t;}}});", "r.h2r[o.id]=t;}}});rvBout(W,L);")
rep("if(G.bnum%6===1)schRecalc();", "if(G.bnum%6===1)schRecalc();rvPlayoff();rvFind();")
rep("'・対戦 '+hh[0]+'勝'+hh[1]+'敗</div>'+kenH(a,o)+", "'・対戦 '+hh[0]+'勝'+hh[1]+'敗</div>'+rvTag(a,o)+kenH(a,o)+")
ui = open(os.path.join(here, 'rv132_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
