# 若者頭・世話人・マネージャー(見本 staff3:部屋の人の図)  v58 -> v59
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v58</title>', '<title>Sumo Manager v59</title>')
rep("const APPV=58;\nconst SAVE='sumoManager58',SAVE57", "const APPV=59;\nconst SAVE='sumoManager59',SAVE58='sumoManager58',SAVE57")
rep('[SAVE57,SAVE56', '[SAVE58,SAVE57,SAVE56')
rep(" if(g.v===57){g.v=58;}\n return g.v===58?g:null;}", " if(g.v===57){g.v=58;}\n if(g.v===58){g.v=59;}\n return g.v===59?g:null;}")
rep('G={v:58,', 'G={v:59,')
CORE = r'''/* 若者頭・世話人(協会の嘱託職員。部屋に所属し、給料は協会から)。効き目の数字は推定 */
function swN(){return (G.ura||[]).filter(u=>u.k==='世話人'&&u.heya===me().n).length;}
function wkgEnsure(){if(G.wkgDone)return;G.wkgDone=1;if(!G.wkg&&own().length>=20)G.wkg={n:shikona(),mo:'幕下 '+RI(3,40)+' 枚目',age:RI(35,55),kaku:1};}
function wkgBasho(){wkgEnsure();if(G.wkg){G.wkg.age+=1/6;if(G.wkg.age>=65){addNews('若者頭の'+G.wkg.n+'が定年(65 歳)で協会を退きました。');G.wkg=null;}}}
function wkgRetire(r){if(r.h!==0||(r.best==null)||r.best>=divStart(3)||r.age<25||(r.tr==null?50:r.tr)<50||myoOK(r))return;
 if(!G.wkg&&own().length>=15&&Math.random()<.35){G.wkg={n:r.n,mo:bestRank(r),age:Math.floor(r.age),own:1};addNews('引退した'+r.n+'は、師匠の推薦で若者頭として部屋に残ることになりました。');return;}
 if(swN()<1&&own().length>=12&&Math.random()<.12){G.ura=G.ura||[];G.ura.push({k:'世話人',n:r.n,rk:'世話人',heya:me().n,own:1});addNews('引退した'+r.n+'は、師匠の推薦で世話人として部屋に残ることになりました。');}}
'''
rep("function v13Basho(sum){", CORE + "function v13Basho(sum){wkgBasho();")
# 若者頭:入門 2 年以内にやめる確率 −15%、兄弟子の暴力の芽に気づきやすい(+0.15)
rep("  p=cl(p,.003,.08);\n", "  if(G.wkg)p*=.85;\n  p=cl(p,.003,.08);\n")
rep("if(Math.random()<.5+(G.okami?G.okami.sk.hito*.02:0))G.ev.push({k:'ijime'", "if(Math.random()<.5+(G.okami?G.okami.sk.hito*.02:0)+(G.wkg?.15:0))G.ev.push({k:'ijime'")
# 世話人:自分の部屋の力士の疲れのたまり方 −3%
rep(" // 疲労\n r.fat=cl(", " // 疲労\n const fat0=r.fat;r.fat=cl(")
rep("if(isOwn){r.mor=cl(r.mor+PM[r.pm||'昼'].m,0,100);", "if(isOwn&&r.fat>fat0&&swN())r.fat=fat0+(r.fat-fat0)*.97;\n if(isOwn){r.mor=cl(r.mor+PM[r.pm||'昼'].m,0,100);")
# 引退した自分の部屋の力士が若者頭・世話人に
rep(" kidRoll(r);\n", " kidRoll(r);\n wkgRetire(r);\n")
# 新弟子の情報:マネージャーの人脈の効き目を半分に、部屋付き親方の人脈を足す
rep("function infoWeek(mg,spring){const net=mg.reduce((t,s)=>t+s.sk.net,0)*.004;", "function infoWeek(mg,spring){const net=mg.reduce((t,s)=>t+s.sk.net,0)*.002+Math.min(4,G.staff.filter(s=>s.role==='co').length)*.005;")
# 画面:部屋の裏方の欄を「部屋の人の図」に
OLD_START = " {const U=uraOf(me().n);if(U.length||G.toshi)h+='<div class=\"pn\"><h2>部屋の裏方"
i = s.index(OLD_START); j = s.index("\n", i)
s = s[:i] + " h+=orgHTML();" + s[j:]
rep("'<p class=\"kaku mute\" style=\"font-size:13px\">部屋付き親方:稽古の指導(得意分野が効く)と力士の見極め。トレーナー:医療はけがを減らして治りを早め、調整は疲れを抜く。ちゃんこ長:栄養で体作りと回復。マネージャー:候補に会いに行けて(目利きで見立てが正確に)、人脈で情報が増える。</p></div>'",
    "'<p class=\"kaku mute\" style=\"font-size:13px\">部屋付き親方:稽古の指導(得意分野が効く)と力士の見極め。人脈で新弟子の情報も入る。マネージャー:部屋が自分で契約する人(協会員ではない)。事務・後援会との連絡・新弟子探しの手伝い。候補に会いに行けて(目利きで見立てが正確に)、人脈で情報が少し増える。</p></div>'")
UI = r'''function orgHTML(){wkgEnsure();const U=uraOf(me().n);const co=G.staff.filter(s=>s.role==='co'),sc=G.staff.filter(s=>s.role==='sc');const sw=U.filter(u=>u.k==='世話人'),yb=U.filter(u=>u.k!=='世話人');const o=own();const young=o.filter(r=>r.d>=2).length;
 const bx=(t,who,ef,h)=>'<div class="bx'+(h?' h':'')+'"><b>'+t+'</b>'+who+'<div class="sub2">'+ef+'</div></div>';
 const W=G.wkg;
 return '<div class="pn"><h2>部屋の人の図<span class="sub">枠が赤=部屋が雇う人</span></h2><div class="org"><div class="top bx"><b>師匠</b>'+esc(me().o)+'</div><div class="ln"></div>'+
  '<div class="row">'+bx('部屋付き親方',co.length?co.map(s=>esc(s.n)+(s.myo?'(年寄 '+esc(s.myo)+')':'')).join('、'):'いません','稽古の指導・新弟子の人脈')+bx('おかみさん',G.okami?esc(G.okami.n):'いません','後援会・お金・弟子の相談')+bx('マネージャー',sc.length?sc.map(s=>esc(s.n)).join('、'):'いません','事務・新弟子探しの手伝い',1)+'</div><div class="ln" style="margin-top:6px"></div>'+
  '<div class="row">'+bx('若者頭',W?esc(W.n)+(W.kaku?'(架空)':'')+'・元'+esc(W.mo)+'・'+Math.floor(W.age)+'歳':'いません',W?'入門 2 年以内にやめる人 −15%':'弟子が多い部屋に置かれる')+bx('世話人',sw.length?sw.map(u=>esc(u.n)).join('、'):'いません',sw.length?'若い衆の雑用が減る(疲れ −3%)':'用具と雑務の係')+bx('行司・呼出・床山',yb.length?yb.map(u=>esc(u.n)).join('・'):'いません','本場所の仕事')+'</div><div class="ln" style="margin-top:6px"></div>'+
  '<div class="top bx"><b>力士 '+o.length+' 人</b>関取 '+o.filter(r=>r.d<=1).length+'・若い衆 '+young+'</div></div>'+
  '<ul class="kaku" style="font-size:13px;padding-left:18px;margin:6px 0 0"><li><b>部屋付き親方</b>:稽古場で弟子を指導する。名跡があれば跡継ぎ・独立の候補。本場所では審判や警備などの協会の仕事も。給料は協会。</li><li><b>若者頭</b>:幕下以下の若い衆の生活と稽古を見張る監督役。兄弟子の暴力の芽にも気づきやすい。給料は協会。</li><li><b>世話人</b>:用具の運び・保管と部屋の雑務。若者頭の助手。本場所では木戸(入口)や役員室の係。給料は協会。</li><li><b>マネージャー</b>:部屋が自分で契約する人(協会員ではない)。給料は部屋。</li></ul>'+
  '<p class="kaku mute" style="font-size:13px;margin-top:6px">新弟子探しの主役は親方と部屋付き親方の人脈(後援会・学校の監督・同郷・先輩のつながり)。若者頭・世話人は、自分の部屋で幕下以上まで上がって引退した力士から、師匠の推薦でなれることがあります。行司・呼出・床山・世話人は 2026 年 11 月時点の実在の人(協会の公式一覧から。本名は載せていません)。若者頭は公開の一覧が見つからず、架空の人です。効き目の数字は推定。</p></div>';}
'''
rep("function staffHTML(){", UI + "function staffHTML(){")
CSS = '''.org{position:relative;padding:6px 0}.org .top{text-align:center;margin:0 auto 6px;max-width:260px}
.org .bx{border:1.5px solid var(--sumi);border-radius:8px;padding:6px 8px;background:var(--paper);text-align:center;font-size:14px}
.org .bx b{display:block;font-size:15px}.org .bx.h{border-color:var(--shu)}
.org .row{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin-top:10px}
.org .ln{height:14px;border-left:2px solid var(--line);width:0;margin:0 auto}.org .sub2{margin-top:6px;font-size:12px;color:var(--mute)}
</style>'''
k = s.index('</style>')
s = s[:k] + CSS + s[k+len('</style>'):]
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
