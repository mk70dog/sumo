# v135 -> v136:横綱審議委員会と綱取り(横審の会合と票・綱取りの場所・伝達式の口上・横審の記録)。ダルマさん「実施」。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=135;\nconst SAVE='sumoManager135',SAVE134", "const APPV=136;\nconst SAVE='sumoManager136',SAVE135='sumoManager135',SAVE134")
rep('[SAVE134,SAVE133', '[SAVE135,SAVE134,SAVE133')
rep('<title>Grand Sumo Manager v135', '<title>Grand Sumo Manager v136')
core = open(os.path.join(here, 'ys136_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n")
rep("if((a.yu&&b.yu)||(((a.yu&&b.jn)||(b.yu&&a.jn))&&a.w+b.w>=25))nt[id]='Y';", "if(ysJudge(r,a,b))nt[id]='Y';")
rep("G.ev.push({k:'tsuna',rid:r.id});", "G.ev.push({k:'dentatsu',rid:r.id},{k:'tsuna',rid:r.id});")
rep("r.susp=T.s>=3?2:1;addNews(G.heya", "r.susp=T.s>=3?2:1;r.scN=(r.scN||0)+1;addNews(G.heya")
rep("Object.assign(EVT,ST_EVT,RT_EVT,FM_EVT);coEvt();", "Object.assign(EVT,ST_EVT,RT_EVT,FM_EVT,YS_EVT);coEvt();ysEvt();")
ui = open(os.path.join(here, 'ys136_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
