# v130 -> v131:部屋付き親方を探して来てもらう(人柄・教え方、条件を出して探す、来てもらう交渉、型との相性)。ダルマさん「実施」。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=130;\nconst SAVE='sumoManager130',SAVE129", "const APPV=131;\nconst SAVE='sumoManager131',SAVE130='sumoManager130',SAVE129")
rep('[SAVE129,SAVE128', '[SAVE130,SAVE129,SAVE128')
rep('<title>Grand Sumo Manager v130', '<title>Grand Sumo Manager v131')
core = open(os.path.join(here, 'co131_core.js'), encoding='utf-8').read()
rep("function doWeek(){\n if(G.phase!=='train')return;\n", core + "function doWeek(){\n if(G.phase!=='train')return;\n")
rep("function refreshMarket(){\n", "function refreshMarket(){refreshMarket0();coReqMake();G.market.forEach(coInit);}\nfunction refreshMarket0(){\n")
rep("co.filter(s=>coA(s).t!=='sk'||coA(s).s===k).map(s=>s.sk[k])", "co.filter(s=>coA(s).t!=='sk'||coA(s).s===k).map(s=>s.sk[k]*coTch(s))")
rep("else if(c==='mou')k=1.05;}catch(e){}", "else if(c==='mou')k=1.05;}catch(e){}k*=coTkFit(r,t.p);")
rep("rtCycle();\n", "rtCycle();coHitoCycle();\n")
rep("Object.assign(EVT,ST_EVT,RT_EVT);", "Object.assign(EVT,ST_EVT,RT_EVT);coEvt();")
rep(" if(G.staff.filter(x=>x.role===s.role).length>=ROLE[s.role].max)return ROLE[s.role].n+'は '+ROLE[s.role].max+' 人までです。';\n",
    " if(G.staff.filter(x=>x.role===s.role).length>=ROLE[s.role].max)return ROLE[s.role].n+'は '+ROLE[s.role].max+' 人までです。';\n if(s.role==='co'&&Math.random()>coAcc(s)){G.market=G.market.filter(x=>x.sid!==sid);const nm=s.n.replace(/^元・/,'')+'親方';addNews(nm+'に部屋付き親方の話をしましたが、「今の部屋に残ります」と断られました。');return nm+'は「今の部屋に残ります」と、話を断りました。';}\n")
rep("sei:'心の指導',", "sei:'心の指導・相談',")
rep("'_psup','kAuto','skS','sewa'];", "'_psup','kAuto','skS','sewa','coReq'];")
ui = open(os.path.join(here, 'co131_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
