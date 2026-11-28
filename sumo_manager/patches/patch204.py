# v200 -> v201:力士のほかの人も育つ(指導の経験・研修・おかみさんの経験・ちゃんこ長の得意な鍋・付け人の学び・部屋育ちの親方)
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=200;\nconst SAVE='sumoManager200',SAVE199", "const APPV=201;\nconst SAVE='sumoManager201',SAVE200='sumoManager200',SAVE199")
rep('[SAVE199,SAVE198', '[SAVE200,SAVE199,SAVE198')
rep('<title>Grand Sumo Manager v200', '<title>Grand Sumo Manager v201')

# v201:力士のほかの人も育つ
rep("G.ev.push({k:'oyakata',scl:","G.ev.push({k:'oyakata',tkp:(r.tk?r.tk.p:null),scl:")
rep("s.sal=0;m.h=s.sid;G.staff.push(s);","s.sal=0;try{const kk={O:'osh',X:'osh',R:'yot',L:'yot',W:'waz'}[e.tkp]||'tai';s.sk[kk]=Math.min(18,s.sk[kk]+2);s.home=1;}catch(x){}m.h=s.sid;G.staff.push(s);")
ui = open(os.path.join(here,'grow201_ui.js'),encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
