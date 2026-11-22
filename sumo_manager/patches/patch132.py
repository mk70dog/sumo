# v128 -> v129:取り口を作る長い計画(型づくり)。ダルマさん「実施」。計算は patches/tk129_core.js、画面は patches/tk129_ui.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=128;\nconst SAVE='sumoManager128',SAVE127", "const APPV=129;\nconst SAVE='sumoManager129',SAVE128='sumoManager128',SAVE127")
rep('[SAVE127,SAVE126', '[SAVE128,SAVE127,SAVE126')
rep('<title>Grand Sumo Manager v128', '<title>Grand Sumo Manager v129')
core = open(os.path.join(here, 'tk129_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n kcWeek();\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n kcWeek();forP(tkWeek);\n")
rep("grow(r,k,gm*M.w[k]*kcTilt(r,k)", "grow(r,k,gm*M.w[k]*kcTilt(r,k)*tkTilt(r,k)")
rep("return off+hold*.5-tire;", "return off+tkB(r,form,gS)+hold*.5-tire;")
rep("kMan:1,mkP:1};", "kMan:1,mkP:1,tkP:1};")
ui = open(os.path.join(here, 'tk129_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
