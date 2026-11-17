# 技の決まりやすさに力の差を効かせる  v33 -> v34
# 引き技・投げ・足技・変化・土俵際の逆転が決まる確率の式で、力の差を割る数を 2(変化は 2.2)→ 1.5(変化は 1.65)に。
#   弱い力士の一発の技は、強い相手には決まりにくくなる(力が同じなら確率は変わらない)。
#   v33 では横綱が平幕に負けた取組の約 3 分の 2 がこうした技だった。数字は測定に合わせた推定。
# 測定(25 年・4 シード平均):決定戦 31→29.5%、優勝 横綱 50・大関 20・三役 14・平幕 17%、金星 横綱 1 人・1 場所 0.97 個。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v33</title>', '<title>Sumo Manager v34</title>')
rep("const APPV=33;\nconst SAVE='sumoManager33',SAVE32", "const APPV=34;\nconst SAVE='sumoManager34',SAVE33='sumoManager33',SAVE32")
rep('[SAVE32,SAVE31', '[SAVE33,SAVE32,SAVE31')
rep(" if(g.v===32){g.v=33;}\n return g.v===33?g:null;}", " if(g.v===32){g.v=33;}\n if(g.v===33){g.v=34;}\n return g.v===34?g:null;}")
rep('G={v:33,', 'G={v:34,')
rep("(E(Y,'rei')*.5+E(Y,'tac')*.2+E(Y,'flx')*.3))/2.2+","(E(Y,'rei')*.5+E(Y,'tac')*.2+E(Y,'flx')*.3))/(DV*1.1)+")
rep("(E(Y,'tac')*.25+E(Y,'flx')*.35+E(Y,'rei')*.4))/2-.25","(E(Y,'tac')*.25+E(Y,'flx')*.35+E(Y,'rei')*.4))/DV-.25")
rep("(E(Y,'flx')*.4+E(Y,'gam')*.3+E(Y,'yor')*.3))/2-.3","(E(Y,'flx')*.4+E(Y,'gam')*.3+E(Y,'yor')*.3))/DV-.3")
rep("(E(Y,'flx')*.5+E(Y,'gam')*.5))/2-.5","(E(Y,'flx')*.5+E(Y,'gam')*.5))/DV-.5")
rep("E(X,'str')*.4))/2-2.5","E(X,'str')*.4))/DV-2.5")
rep("const BE={k:2.5,sd:48};","const BE={k:2.5,sd:48};const DV=1.5;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
