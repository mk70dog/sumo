# v63 -> v64:実在の力士の能力を実データから(直近 6 場所の成績・出世の速さ・最高位との差・得意技・若手の勢い)
# 補正値は tools/mkrealx.py が data/rec6_2026.txt・data/rikishi_debut.csv から作る patches/realx67.json
import sys, json
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v63</title>', '<title>Sumo Manager v64</title>')
rep("const APPV=63;\nconst SAVE='sumoManager63',SAVE62", "const APPV=64;\nconst SAVE='sumoManager64',SAVE63='sumoManager63',SAVE62")
rep('[SAVE62,SAVE61', '[SAVE63,SAVE62,SAVE61')
rep(" if(g.v===62){g.v=63;}\n return g.v===63?g:null;}", " if(g.v===62){g.v=63;}\n if(g.v===63){g.v=64;}\n return g.v===64?g:null;}")
rep('G={v:63,', 'G={v:64,')
X = open('patches/realx67.json', encoding='utf-8').read().strip()
# 補正値の表と得意技 → 能力
rep("const REALB=[", "/* v64:実在の力士の補正(dT=力の補正、rm=伸びしろ、fast=伸びる速さ、iki=勢いの場所数、old=最盛期を過ぎた) */\nconst REALX=" + X + ";\n"
    "const WZK=[[/上手投げ|下手投げ|投げ/,'nag'],[/いなし|肩透かし|引き/,'hik'],[/足取り|足技/,'ash'],[/突っ張り|突き/,'tsk'],[/押し/,'tac'],[/寄り/,'yor'],[/モロ差し/,'mig'],[/モロ差し/,'hid']];\n"
    "function realAdj(r,X){\n"
    " if(r.wz){const ks={};WZK.forEach(([re,k])=>{if(re.test(r.wz))ks[k]=1;});for(const k in ks){r.a[k]=cl(r.a[k]+1.5,1,19.5);r.cap[k]=cl(Math.max(r.cap[k],r.a[k])+0,r.a[k],20);}}\n"
    " if(X.old){PHYS.concat(TECH).forEach(k=>{r.cap[k]=r.a[k];});['sho','rei'].forEach(k=>{r.a[k]=cl(r.a[k]+.8,1,19.5);r.cap[k]=Math.max(r.cap[k],r.a[k]);});r.old5=1;}\n"
    " if(X.fast)r.fast=X.fast;if(X.iki)r.iki=X.iki;}\n"
    "const REALB=[")
rep("let room=age<20?R(1,7):age<24?R(0,4):age<28?R(0,2):0;if(age<25&&i<190)room+=R(.5,2.5);",
    "let room=age<20?R(1,7):age<24?R(0,4):age<28?R(0,2):0;if(age<25&&i<190)room+=R(.5,2.5);\n  const X=REALX[f[1]]||{};T+=X.dT||0;room=Math.max(0,room+(X.rm||0));if(X.old)room=0;")
rep("if(h===0){r.kn=40;r.menu='申';r.tr=55;}\n  G.names[r.n]=1;", "realAdj(r,X);\n  if(h===0){r.kn=40;r.menu='申';r.tr=55;}\n  G.names[r.n]=1;")
# 伸びる速さ(26 歳まで)
rep("if(isOwn)gm*=coMul(r);for(const k in M.w)", "if(isOwn)gm*=coMul(r);if(r.fast&&r.age<26)gm*=r.fast;for(const k in M.w)")
# 勢い:最初の数場所は調子がよい方に出やすい
rep("if(r.h===0&&r.d<=1&&coL('seki').length)r.bfm*=.6;}", "if(r.h===0&&r.d<=1&&coL('seki').length)r.bfm*=.6;if(r.iki>0){r.bfm+=.015;r.iki--;}}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
