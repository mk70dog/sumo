# v127 -> v128:部屋の年表と殿堂(「お任せで実施」の 2 つ目)。計算は patches/hy128_core.js、画面は patches/hy128_ui.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=127;\nconst SAVE='sumoManager127',SAVE126", "const APPV=128;\nconst SAVE='sumoManager128',SAVE127='sumoManager127',SAVE126")
rep('[SAVE126,SAVE125', '[SAVE127,SAVE126,SAVE125')
rep('<title>Grand Sumo Manager v127', '<title>Grand Sumo Manager v128')
core = open(os.path.join(here, 'hy128_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n kcWeek();\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n kcWeek();\n")
rep(" stCycle(old,msgs);\n", " stCycle(old,msgs);hySek();\n")
rep("own:isPH(r.h),oh:r.h};\n G.retired.unshift(info);", "own:isPH(r.h),oh:r.h,deb:hyDeb(r),sek:r.sekD||null,st:isPH(r.h)?hyNote(r):null};\n G.retired.unshift(info);")
rep("'dok','subX','_psup','kAuto'];", "'dok','subX','_psup','kAuto','skS'];")
ui = open(os.path.join(here, 'hy128_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
