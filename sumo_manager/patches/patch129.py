# v125 -> v126:親方の「指導の色」と「親方におまかせ」(ダルマさん「基本的には親方や部屋付き親方などが自動的に稽古のメニューなどは対応する。親方の特性によって取り方や成長も変わる?」→ 設計案 →「実施」)。
# 計算は patches/kc126_core.js(本体の doWeek の前に入れる)、画面は patches/kc126_ui.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=125;\nconst SAVE='sumoManager125',SAVE124", "const APPV=126;\nconst SAVE='sumoManager126',SAVE125='sumoManager125',SAVE124")
rep('[SAVE124,SAVE123', '[SAVE125,SAVE124,SAVE123')
rep('<title>Grand Sumo Manager v125', '<title>Grand Sumo Manager v126')
core = open(os.path.join(here, 'kc126_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n kcWeek();\n")
rep("for(const k in M.w)grow(r,k,gm*M.w[k]", "for(const k in M.w)grow(r,k,gm*M.w[k]*kcTilt(r,k)")
rep("if(isOwn)gm*=coMul(r);", "if(isOwn)gm*=coMul(r);gm*=kcG(r);")
rep("const pI=0.00735*M.i*I.i*KD.i*", "const pI=0.00735*M.i*I.i*KD.i*kcI(r)*")
rep(" bcDay();\n B.last=bouts;", " bcDay();kcBasho();\n B.last=bouts;")
rep("const MPX_RK={menu:1,it:1,pm:1,wplan:1,injPol:1,sh:1,tac:1,bca:1,bcp:1};", "const MPX_RK={menu:1,it:1,pm:1,wplan:1,injPol:1,sh:1,tac:1,bca:1,bcp:1,kMan:1};")
# 「親方におまかせ」はプレイヤーごとの設定(二人相撲で親と子が別々に持つ)
rep("'dok','subX','_psup'];", "'dok','subX','_psup','kAuto'];")
rep("const MPX_PK={dekH:1,kDays:1,meal:1,coAs:1,kpol:1,meSel:1,rengoOff:1};", "const MPX_PK={dekH:1,kDays:1,meal:1,coAs:1,kpol:1,meSel:1,rengoOff:1,kAuto:1};")
ui = open(os.path.join(here, 'kc126_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
