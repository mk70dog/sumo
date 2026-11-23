# v158 -> v159:ホーム(場所後)のスクロールを減らす(見本 sc2。ダルマさん「表示が下すぎる」「全体的に下にスクロールが多いので改良する」→「SC2」)。
#   場所後は「やること(親方の悩みごと・次の場所へ)」を左、「場所を終えて」を右の 2 列にして、錦絵より上に出す。スマホは 1 列(やること→結果)。
#   部屋の成績は「勝ち越し・負け越し・関取の人数」+関取の成績だけ見せ、全員はたたむ。収支は合計の 1 行だけ見せ、内訳はたたむ。
#   たたみの開け閉めは UI に覚える(悩みごとに答えて画面が描き直されても閉じない)。数値や仕組みは変えない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=158;\nconst SAVE='sumoManager158',SAVE157", "const APPV=159;\nconst SAVE='sumoManager159',SAVE158='sumoManager158',SAVE157")
rep('[SAVE157,SAVE156', '[SAVE158,SAVE157,SAVE156')
rep('<title>Grand Sumo Manager v158', '<title>Grand Sumo Manager v159')
rep('</head>', """<style>
/* v159:ホーム(場所後)を 2 列に(見本 sc2) */
.hm2{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start;margin-bottom:12px}
.hm2>div>.pn{margin-top:0;margin-bottom:12px}
.hm2l{position:sticky;top:8px}
.hm2 .todo{border:2px solid var(--kin)}
.hm2 .ecnt{display:inline-block;background:var(--shu);color:#fff;border-radius:10px;padding:0 8px;font-size:12px;margin-left:6px;vertical-align:3px}
.hm2 .sm3{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}
.hm2 .sm3 div{flex:1;min-width:80px;background:var(--washi2);border:1px solid var(--line);border-radius:8px;padding:6px 10px;text-align:center;font-size:12px;color:var(--mute)}
.hm2 .sm3 b{display:block;font-size:20px;color:var(--sumi)}
.hm2 .sm3 .g b{color:var(--midori)}.hm2 .sm3 .r b{color:var(--shu)}
.hm2 details{margin:6px 0 10px;border:1px solid var(--line);border-radius:8px;background:var(--washi2)}
.hm2 details>summary{cursor:pointer;padding:9px 12px;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.hm2 details>summary::-webkit-details-marker{display:none}
.hm2 details>summary::after{content:'▼ ひらく';font-weight:400;font-size:12px;color:var(--mute)}
.hm2 details[open]>summary::after{content:'▲ たたむ'}
.hm2 details>table{margin:0}
@media (max-width:760px){.hm2{grid-template-columns:1fr}.hm2l{position:static}.hm2 h2 .sub{display:none}}
</style>
</head>""")
# 場所後の組み立て
a = s.index("  const L=G.last;\n  h+='<div class=\"pn\"><h2>'+bname(G.bnum)+' 場所を終えて</h2>';")
b = s.index(" }\n const seki=own().filter(r=>r.d<=1);", a)
NEW = r"""  const L=G.last;let R='<div class="pn"><h2>'+bname(G.bnum)+' 場所を終えて</h2>';
  const orow=o=>'<tr class="clk" onclick="showR('+o.id+')"><td>'+esc(o.rk)+'</td><td class="nm">'+esc(o.n)+'</td><td class="wl">'+o.w+'勝'+o.l+'敗'+(o.ab?o.ab+'休':'')+'</td><td>'+(o.kk?'<span class="tag mid">勝ち越し</span>':'<span class="tag shu">負け越し</span>')+'</td></tr>';
  const oth='<tr><th>番付</th><th>四股名</th><th>成績</th><th></th></tr>';
  const kk=L.own.filter(o=>o.kk).length,sek=L.own.filter(o=>/横綱|大関|関脇|小結|前頭|十両/.test(o.rk));
  R+='<h3>部屋の成績</h3><div class="sm3"><div class="g"><b>'+kk+'</b>勝ち越し</div><div class="r"><b>'+(L.own.length-kk)+'</b>負け越し</div><div><b>'+sek.length+'</b>関取</div></div>';
  if(sek.length)R+='<table class="tb">'+oth+sek.map(orow).join('')+'</table>';
  R+='<details'+(UI.hmA?' open':'')+' ontoggle="UI.hmA=this.open"><summary>全員の成績('+L.own.length+' 人)</summary><table class="tb">'+oth+L.own.map(orow).join('')+'</table></details>';
  R+='<h3>各段の優勝</h3><div class="kaku">'+L.yu.map(y=>'<div>'+DN[y.d]+':<b class="'+(y.h===ME()?'shu':'')+'">'+esc(y.n)+'</b>('+esc(y.rk)+'・'+esc(G.heya[y.h].n)+')'+y.w+'勝'+y.l+'敗'+(y.po?' 決定戦':'')+'</div>').join('')+'</div>';
  if(L.sansho.length)R+='<h3>三賞</h3><div class="kaku">'+L.sansho.map(s=>'<div>'+s.t+':<b class="'+(s.h===ME()?'shu':'')+'">'+esc(s.n)+'</b>('+esc(s.rk)+')</div>').join('')+'</div>';
  const F=L.fin;R+='<h3>今場所の収支</h3>'+(F?'<details'+(UI.hmF?' open':'')+' ontoggle="UI.hmF=this.open"><summary><span>収入 '+man(F.tin)+' ・ 支出 '+man(F.tout)+' ・ 差し引き <b class="'+(F.net<0?'shu':'mid')+'">'+(F.net>=0?'+':'')+man(F.net)+'</b></span></summary>'+finHTML(F)+'</details>':finHTML(F))+'</div>';
  let T='';
  if(G.ev.length)T+='<div class="pn todo"><h2>親方の悩みごと<span class="ecnt">'+G.ev.length+' 件</span><span class="sub">決めると次へ進めます</span></h2>'+G.ev.map(e=>{const E=EVT[e.k];return evHead(e,E)+'<div class="btns">'+(typeof E.c==='function'?E.c(e):E.c).map((c,i)=>'<button class="btn sm'+(i===0?' ai':'')+'" onclick="doEv(\''+e.id+'\','+i+')">'+c+'</button>').join('')+'</div></div>';}).join('')+'</div>';
  T+='<div class="pn'+(G.ev.length?'':' todo')+'"><h2>次の場所へ</h2><p class="kaku">番付が発表され、次の場所までの 6 週の稽古期間に入ります。新弟子の勧誘やスタッフの入れ替えもこの間にできます。</p><div class="btns"><button class="btn main" '+(G.ev.length?'disabled':'')+' onclick="doNext()">番付発表へ進む</button><button class="btn" onclick="go(\'scout\')">新弟子</button><button class="btn" onclick="go(\'staff\')">スタッフ</button></div></div>';
  h+='<div class="hm2"><div class="hm2l">'+T+'</div><div class="hm2r">'+R+'</div></div>';
"""
s = s[:a] + NEW + s[b:]
# 錦絵の位置:2 列があれば、ナビのすぐ下に 2 列、その下に錦絵
rep("const nav=app.querySelector('.nav')||app.children[1];nav.insertAdjacentHTML('afterend',hbStage());requestAnimationFrame(hbFit);};",
    "const nav=app.querySelector('.nav')||app.children[1];const hm2=app.querySelector(':scope > .hm2');if(hm2)nav.insertAdjacentElement('afterend',hm2);(hm2||nav).insertAdjacentHTML('afterend',hbStage());requestAnimationFrame(hbFit);};")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
