# v68 -> v69:能力 20 項目の見直し(見本 nou2)
# 足す:腰の重さ(kos・体)、前さばき(mae・技)/隠れた資質へ移す:研究熱心(ken)・プロ意識(pro)(数値は残し、伸び方に効く)
# まとめる:大一番(bm)を勝負強さ(sho)に。画面は 5 つの箱(体・押し・四つ・技・心)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v68</title>', '<title>Sumo Manager v69</title>')
rep("const APPV=68;\nconst SAVE='sumoManager68',SAVE67", "const APPV=69;\nconst SAVE='sumoManager69',SAVE68='sumoManager68',SAVE67")
rep('[SAVE67,SAVE66', '[SAVE68,SAVE67,SAVE66')
rep(" if(g.v===67){g.v=68;}\n return g.v===68?g:null;}", " if(g.v===67){g.v=68;}\n if(g.v===68){mig69(g);g.v=69;}\n return g.v===69?g:null;}")
rep('G={v:68,', 'G={v:69,')
# 項目の表
rep("['rec','回復力','体'],", "['rec','回復力','体'],['kos','腰の重さ','体'],")
rep("['tsk','突き押し','技'],", "['tsk','突き押し','技'],['mae','前さばき','技'],")
rep("['ken','研究熱心','心']", "['ken','研究熱心','隠']")
rep("['pro','プロ意識','心']", "['pro','プロ意識','隠']")
rep("const PHYS=['str','exp','end','flx','rec'],TECH=['tac','tsk','mig'", "const PHYS=['str','exp','end','flx','rec','kos'],TECH=['tac','tsk','mae','mig'")
rep("['tac','tsk','hik'].forEach(k=>CAT[k]='osh');", "['tac','tsk','mae','hik'].forEach(k=>CAT[k]='osh');")
# 型ごとの傾向(推定):押し=前さばき・腰、四つ=腰の重さ・前さばき、技能=腰は軽め
rep(" 押:{str:1,exp:1.5,tac:1.5,tsk:3,", " 押:{str:1,exp:1.5,tac:1.5,tsk:3,mae:1.5,kos:.5,")
rep(" 右:{str:1.5,end:.5,mig:3,", " 右:{str:1.5,end:.5,kos:1.5,mae:1,mig:3,")
rep(" 左:{str:1.5,end:.5,hid:3,", " 左:{str:1.5,end:.5,kos:1.5,mae:1,hid:3,")
rep(" 技:{flx:2,exp:1,nag:2,", " 技:{flx:2,exp:1,kos:-1,mae:.5,nag:2,")
# 総合力の重み:研究熱心・プロ意識は外し、腰の重さ・前さばきを足す
rep("sho:.3,gam:.3,pro:.1,ken:.1};", "sho:.3,gam:.3,kos:.5,mae:.5};")
# 稽古:四股・てっぽう=腰の重さ・前さばき(おっつけ)、ぶつかり=腰、申し合い・三番・出稽古=前さばき
rep("基:{n:'四股・てっぽう',w:{flx:1,str:.6,tsk:.5,end:.7,gam:.6,pro:.5,tgw:.3}", "基:{n:'四股・てっぽう',w:{flx:1,str:.6,tsk:.5,end:.7,gam:.6,pro:.5,tgw:.3,kos:.8,mae:.5}")
rep("ぶ:{n:'ぶつかり稽古',w:{end:1,str:.7,gam:1,tos:.7,yor:.5,rec:.4}", "ぶ:{n:'ぶつかり稽古',w:{end:1,str:.7,gam:1,tos:.7,yor:.5,rec:.4,kos:.6}")
rep("申:{n:'申し合い',w:{tac:1,tsk:.7,", "申:{n:'申し合い',w:{tac:1,tsk:.7,mae:.6,")
rep("三:{n:'三番稽古',w:{tac:.8,tsk:.6,", "三:{n:'三番稽古',w:{tac:.8,tsk:.6,mae:.7,kos:.3,")
rep("出:{n:'出稽古',w:{tac:1.1,tsk:.8,", "出:{n:'出稽古',w:{tac:1.1,tsk:.8,mae:.6,")
rep("const MENU_T={n:'巡業',w:{tac:.5,tsk:.4,", "const MENU_T={n:'巡業',w:{tac:.5,tsk:.4,mae:.3,")
# 取組:大一番は勝負強さにまとめる
rep("r._pr=big?(r.a.sho-10)*.05+(r.bm-10)*.04-(r.per==='繊細'?.4:0):0;", "r._pr=big?(r.a.sho-10)*.09-(r.per==='繊細'?.4:0):0;")
# 取組:差し手争い・おっつけに前さばき
rep("const s=sig(((gripSk(Y,sd[y])*.5+E(Y,'exp')*.2+E(Y,'tac')*.3)-(E(O,'tsk')*.6+E(O,'exp')*.4))/2.4",
    "const s=sig(((gripSk(Y,sd[y])*.45+E(Y,'exp')*.15+E(Y,'tac')*.15+E(Y,'mae')*.25)-(E(O,'tsk')*.5+E(O,'exp')*.3+E(O,'mae')*.2))/2.4")
rep("const sk=r=>E(r,'tac')*.4+E(r,'flx')*.3+E(r,'exp')*.3;", "const sk=r=>E(r,'tac')*.25+E(r,'mae')*.35+E(r,'flx')*.2+E(r,'exp')*.2;")
# 取組:攻め(押しは前さばきを少し)、こらえ(腰の重さ)
rep("const off=form==='O'?E(r,'tsk')*.45+E(r,'str')*.3+E(r,'exp')*.25+wfOf(r)", "const off=form==='O'?E(r,'tsk')*.4+E(r,'mae')*.1+E(r,'str')*.25+E(r,'exp')*.25+wfOf(r)")
rep("const hold=E(r,'gam')*.35+E(r,'flx')*.25+E(r,'end')*.2+E(r,'str')*.2;", "const hold=E(r,'gam')*.25+E(r,'kos')*.3+E(r,'flx')*.2+E(r,'end')*.15+E(r,'str')*.1;")
# 古い保存データ:腰の重さ・前さばきを今の能力から作る
rep("function mig18(g){", """function mig69(g){for(const id in g.R){const r=g.R[id];if(!r||!r.a||r.a.kos!=null)continue;
  const kos=(x)=>x.str*.5+x.gam*.25+x.end*.25+((r.wT||150)>170?1:0),mae=(x)=>x.tac*.4+x.yor*.3+Math.max(x.mig,x.hid)*.3;
  r.a.kos=Math.min(19.5,kos(r.a));r.a.mae=Math.min(19.5,mae(r.a));if(r.cap){r.cap.kos=Math.max(r.a.kos,Math.min(20,kos(r.cap)));r.cap.mae=Math.max(r.a.mae,Math.min(20,mae(r.cap)));}}}
function mig18(g){""")
# 画面:能力の欄を 5 つの箱に
rep("""<div class="atw">'+['体','技','心'].map(g=>'<div class="atc"><div class="atg">'+g+'</div>'+AT.filter(x=>x[2]===g).map(""",
    """<div class="atw5">'+[['体',x=>x[2]==='体'],['押し',x=>CAT[x[0]]==='osh'],['四つ',x=>CAT[x[0]]==='yot'],['技',x=>CAT[x[0]]==='waz'],['心',x=>x[2]==='心']].map(([g,fl])=>'<div class="atc"><div class="atg">'+g+'</div>'+AT.filter(fl).map(""")
# 隠れた資質:大一番 → 研究熱心・プロ意識
rep("hidRow(r,'大一番',75,r.bm>=14?'大一番に強い':r.bm<=6?'大一番に弱い':'ふつう')",
    "hidRow(r,'研究熱心',45,r.a.ken>=14?'よく研究する(研究の稽古がよく伸びる)':r.a.ken<=6?'研究はしない':'ふつう')+hidRow(r,'プロ意識',45,r.a.pro>=14?'自己管理が行き届く(稽古の伸びが良い)':r.a.pro<=6?'自己管理が甘い':'ふつう')")
rep(".atw{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}", ".atw{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.atw5{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
