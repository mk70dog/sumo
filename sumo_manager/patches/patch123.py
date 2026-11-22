# v120:稽古の見直しの残り(稽古日・一門の連合稽古・横審の稽古総見)+秋巡業を 4 週に。v119 → v120
import sys
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: raise SystemExit('一致数がちがう(%d/%d): %s'%(c,n,a[:80]))
    s=s.replace(a,b)
rep("const APPV=119;\nconst SAVE='sumoManager119',SAVE118", "const APPV=120;\nconst SAVE='sumoManager120',SAVE119='sumoManager119',SAVE118")
rep('[SAVE118,SAVE117', '[SAVE119,SAVE118,SAVE117')
rep('<title>Grand Sumo Manager v119','<title>Grand Sumo Manager v120')
# 秋巡業は 10 月 1 日〜27 日ごろ(4 週)
rep("11:[1,3,'秋巡業']","11:[1,4,'秋巡業']")
rep("秋場所のあと(秋巡業・3 週)","秋場所のあと(秋巡業・4 週)")
# 稽古日(推定):週 6 日=今まで。週 5 日 伸び .92・疲れ -4・けが .9、週 4 日 伸び .82・疲れ -8・けが .8
rep("function MKEYS(){","const KDAY={6:{g:1,f:0,i:1},5:{g:.92,f:-4,i:.9},4:{g:.82,f:-8,i:.8}};\nfunction MKEYS(){")
rep(" if(isOwn&&mk==='出'&&G._dek){"," const KD=isOwn?(KDAY[G.kDays||6]||KDAY[6]):KDAY[6];if(isOwn&&mk!=='休'&&mk!=='巡')gm*=KD.g;\n /* 一門の連合稽古(第 5 週)・横審の稽古総見(東京場所の前の第 6 週) */\n const RG=isOwn&&mk!=='休'&&mk!=='巡'&&!r.inj&&G.wk===WEEKS-1&&me().ic>=0&&!G.rengoOff&&(r.d<=1||(r.d===2&&r.pos<DIVS[0].sz+DIVS[1].sz+15))?1:0;\n const SK=isOwn&&mk!=='休'&&!r.inj&&G.wk===WEEKS&&[1,5,9].includes(MONTH[(G.bnum-1)%6])&&r.d===0?1:0;\n if(RG||SK){for(const k in MENU['申'].w)grow(r,k,gm*MENU['申'].w[k]*.25*H.cf[CAT[k]]);if(isOwn){G._rg=G._rg||{r:0,s:0};if(RG)G._rg.r++;if(SK)G._rg.s++;}}\n if(isOwn&&mk==='出'&&G._dek){")
rep("+(kiso?2:0)+(isOwn&&mk==='出'&&G.wk<WEEKS-1?3:0),0,100);","+(kiso?2:0)+(isOwn&&mk==='出'&&G.wk<WEEKS-1?3:0)+(isOwn&&mk!=='休'?KD.f:0)+((RG||SK)?3:0),0,100);")
rep("+(isOwn&&mk==='出'&&G.wk>=WEEKS-1?4:0);r.cond=cl(","+(isOwn&&mk==='出'&&G.wk>=WEEKS-1?4:0)+((RG||SK)?4:0);r.cond=cl(")
rep(" const pI=0.00735*M.i*I.i*"," const pI=0.00735*M.i*I.i*KD.i*")
# 週の最後に知らせる
rep("  shiteiWeek();\n  tourEnd();","  shiteiWeek();\n  tourEnd();\n  if(G._rg){if(G._rg.r)addNews('一門の連合稽古に '+G._rg.r+' 人が参加しました。ほかの部屋の関取と相撲を取り、調子が上がりました。');if(G._rg.s){addNews('横綱審議委員会の稽古総見に幕内力士 '+G._rg.s+' 人が参加しました。');G.rep=cl(G.rep+.5,0,100);}G._rg=null;}")
d=__file__.replace('patch123.py','')
rep(open(d+'kt119.js',encoding='utf-8').read(),open(d+'kt120.js',encoding='utf-8').read())
open(dst,'w',encoding='utf-8').write(s)
print('ok')
