# v157 -> v158:新弟子の画面「学校とのつきあい」をカードの形にする(見本 sk2。ダルマさん「見やすくわかりやすく サンプル」→「2」)。
#   学校名はふつうの字、関係は数字+横棒(20 の所に青い線)+札(紹介してくれる/あと N/まだ遠い)。
#   紹介してくれる学校は金の枠。ボタンに「関係 +5・5 万円」のように効き目と値段を書く。説明は短い札 3〜4 つ。
#   数値や仕組みは変えない(紹介は関係 20 以上、挨拶 +5・5 万円、出稽古 +7・10 万円、1 場所ごとに 0.7 下がる)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=157;\nconst SAVE='sumoManager157',SAVE156", "const APPV=158;\nconst SAVE='sumoManager158',SAVE157='sumoManager157',SAVE156")
rep('[SAVE156,SAVE155', '[SAVE157,SAVE156,SAVE155')
rep('<title>Grand Sumo Manager v157', '<title>Grand Sumo Manager v158')
CSS = """<style>
.skc .lead{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 10px}
.skc .lead span{font-size:13px;padding:4px 10px;border-radius:14px;background:var(--washi2);border:1px solid var(--line);color:var(--sumi2)}
.skc .lead b{color:var(--kin)}
.skc .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.skc .cd{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:10px 12px;display:flex;flex-direction:column;gap:7px}
.skc .cd.ok{border-color:var(--kin);box-shadow:inset 0 0 0 1px var(--kin)}
.skc .hd{display:flex;justify-content:space-between;align-items:flex-start;gap:6px}
.skc .nmx{font-weight:700;font-size:16px;color:var(--sumi);letter-spacing:.02em}
.skc .subx{font-size:12px;color:var(--mute);margin-top:2px}
.skc .obx{display:inline-block;font-size:11px;padding:0 6px;border-radius:8px;border:1px solid var(--kin);color:var(--kin);margin-left:4px}
.skc .st{display:inline-block;font-size:12px;font-weight:700;padding:1px 8px;border-radius:10px;white-space:nowrap}
.skc .st.ok{background:rgba(212,175,74,.18);color:var(--kin);border:1px solid var(--kin)}
.skc .st.near{background:rgba(110,150,210,.15);color:var(--ai);border:1px solid var(--ai)}
.skc .st.far{color:var(--mute);border:1px solid var(--line)}
.skc .rlrow{display:flex;gap:8px;align-items:center}
.skc .rlrow .num{font-size:15px;font-weight:700;min-width:26px;text-align:right;color:var(--sumi)}
.skc .rb{position:relative;flex:1;height:10px;border-radius:5px;background:var(--washi2);border:1px solid var(--line)}
.skc .rb i{position:absolute;left:0;top:0;bottom:0;border-radius:5px;background:var(--kin)}
.skc .rb i.lo{background:var(--mute);opacity:.6}
.skc .rb u{position:absolute;left:20%;top:-4px;bottom:-4px;width:2px;background:var(--ai)}
.skc .act{display:flex;gap:6px}
.skc .act .btn{flex:1;text-align:left;line-height:1.25;padding:6px 10px}
.skc .act .btn small{display:block;font-size:11px;opacity:.75;font-weight:400}
</style>
</head>"""
rep('</head>', CSS)
old_start = "function schoolPanel(){const L=SCH.map(x=>x[0]).sort((a,b)=>(G.rel[b]||0)-(G.rel[a]||0));"
i = s.index(old_start); j = s.index('\nfunction ', i + 10)
assert s.count(old_start) == 1
NEW = r"""function schoolPanel(){const L=SCH.map(x=>x[0]).sort((a,b)=>(G.rel[b]||0)-(G.rel[a]||0)).slice(0,12);
 const rv=n=>Math.round(G.rel[n]||0);
 const st=n=>{const x=rv(n);return x>=20?'<span class="st ok">紹介してくれる</span>':x>=10?'<span class="st near">あと '+(20-x)+'</span>':'<span class="st far">まだ遠い</span>';};
 const sub=n=>{const c=schOf(n),k=c[1]==='高'?'・高校':c[1]==='大'?'・大学':'';const ob=alumni(0,n);return '<div class="subx">'+c[2]+k+(ob?'<span class="obx">部屋の OB '+ob+' 人</span>':'')+'</div>';};
 return '<div class="skc"><h3>学校とのつきあい</h3><div class="lead"><span>関係 <b>20 以上</b> で卒業前の選手を紹介してくれる</span><span>1 場所ごとに <b>少しずつ下がる</b></span><span>挨拶 <b>+5</b>・出稽古 <b>+7</b></span>'+(G.real?'<span>今の弟子の出身校とは最初から関係あり</span>':'')+'</div><div class="grid">'+
 L.map(n=>{const x=rv(n);return '<div class="cd'+(x>=20?' ok':'')+'"><div class="hd"><div><div class="nmx">'+esc(schLabel(n))+'</div>'+sub(n)+'</div>'+st(n)+'</div>'+
  '<div class="rlrow"><span class="num">'+x+'</span><div class="rb"><i class="'+(x<20?'lo':'')+'" style="width:'+Math.min(100,x)+'%"></i><u></u></div></div>'+
  '<div class="act"><button class="btn sm" onclick="relAct(\''+n+'\',\'aisatsu\')">親方が挨拶<small>関係 +5・5 万円</small></button><button class="btn sm" onclick="relAct(\''+n+'\',\'keiko\')">出稽古に招く<small>関係 +7・10 万円</small></button></div></div>';}).join('')+'</div></div>'+amaPanel();}"""
s = s[:i] + NEW + s[j:]
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
