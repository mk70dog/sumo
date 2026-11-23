# v132 -> v133:力士の私生活と家族(結婚の出来事・子の誕生・師匠の娘との縁談と婿の継承・暮らしの欄)。ダルマさん「実施」。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=132;\nconst SAVE='sumoManager132',SAVE131", "const APPV=133;\nconst SAVE='sumoManager133',SAVE132='sumoManager132',SAVE131")
rep('[SAVE131,SAVE130', '[SAVE132,SAVE131,SAVE130')
rep('<title>Grand Sumo Manager v132', '<title>Grand Sumo Manager v133')
core = open(os.path.join(here, 'fm133_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n")
rep("if(r.d<=1&&!r.mar&&r.age>=25&&(r.cash||0)>=300&&Math.random()<.04){r.mar=1;r.cash-=200;r.mor=cl(r.mor+8,0,100);G.sup+=3;addNews(r.n+'が結婚しました。関取は部屋を出て所帯を持つことができます。');}", "")
rep("gm*=kcG(r)*stG(r);", "gm*=kcG(r)*stG(r)*fmG(r);")
rep("rtCycle();coHitoCycle();\n", "rtCycle();coHitoCycle();fmCycle();\n")
rep("Object.assign(EVT,ST_EVT,RT_EVT);coEvt();", "Object.assign(EVT,ST_EVT,RT_EVT,FM_EVT);coEvt();")
rep("c:e=>shChoices(e).map(x=>x.t),\n  ap:(e,i)=>shChoices(e)[i].f()}", "c:e=>fmMukoChoice(shChoices(e)).map(x=>x.t),\n  ap:(e,i)=>fmMukoChoice(shChoices(e))[i].f()}")
rep("Math.random()<(isPH(r.h)?.25:.08)", "Math.random()<(isPH(r.h)?(r.kids&&r.kids.some(k=>k.boy)?.45:.25):.08)")
ui = open(os.path.join(here, 'fm133_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
