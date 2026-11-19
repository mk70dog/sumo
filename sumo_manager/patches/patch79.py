# v75 -> v76:二世・三世力士(ダルマさん「実施」)
# 実際:親子関取は過去 14 組(デイリー 2026/5/13)。2 世力士は珍しくない(デイリー 2026/4/25)。親子 3 代関取は琴ノ若(現・琴櫻)と王鵬(デイリー 2020/11/25)。
# v75 の測定(35 年・4 シード):二世の関取 37%(全体 17%)、親子関取が 1 回のプレイで 35 年に 8 組ほど=実際の 3〜4 倍(推定の比較)。
# 直し(推定):①父の素質を受け継ぐ割合 0.5→0.3 ②子が角界に入る割合 自分の部屋 0.35→0.25・ほか 0.15→0.08 ③三世(祖父の記録)
#   ④注目(人気 +8、三世は +12)と重圧(4 割の二世・三世は大一番で −0.2)⑤実名スタートの二世・三世を経歴データの家族の欄から登録(四股名だけ)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v75</title>', '<title>Sumo Manager v76</title>')
rep("const APPV=75;\nconst SAVE='sumoManager75',SAVE74", "const APPV=76;\nconst SAVE='sumoManager76',SAVE75='sumoManager75',SAVE74")
rep('[SAVE74,SAVE73', '[SAVE75,SAVE74,SAVE73')
rep(" if(g.v===74){g.v=75;}\n return g.v===75?g:null;}", " if(g.v===74){g.v=75;}\n if(g.v===75){if(g.real)for(const id in g.R){const r=g.R[id];if(r&&!r.nisei)realFam(r);}g.v=76;}\n return g.v===76?g:null;}")
rep('G={v:75,', 'G={v:76,')
rep("if(r.best<42&&G.kids.length<80&&Math.random()<(r.h===0?.35:.15)){", "if(r.best<42&&G.kids.length<80&&Math.random()<(r.h===0?.25:.08)){")
rep("G.kids.push({f:r.n,own:r.h===0,br:bestRank(r),", "G.kids.push({f:r.n,g:r.nisei?{f:r.nisei.f,br:r.nisei.br}:null,own:r.h===0,br:bestRank(r),")
rep("function mkNisei(k,h){\n const r=mkR({T:R(2.5,4.5),room:roomOf(KIND.中学),age:15,h:h,style:Math.random()<.6?k.sty:undefined});\n const p0=potOf(r),d=.5*k.p+.5*p0-p0;",
    "function mkNisei(k,h){\n const r=mkR({T:R(2.5,4.5),room:roomOf(KIND.中学),age:15,h:h,style:Math.random()<.6?k.sty:undefined});\n const p0=potOf(r),d=.3*k.p+.7*p0-p0;")
rep("r.kind='中学';r.nisei={f:k.f,br:k.br};return r;}", "r.kind='中学';r.nisei={f:k.f,br:k.br,g:k.g||null,pr:Math.random()<.4?1:0};r.pop=(r.pop||20)+(k.g?12:8);return r;}")
# 実名スタート:経歴の家族の欄(父・祖父)から
rep("  realAdj(r,X);\n", "  realAdj(r,X);realFam(r);\n")
rep("function realAdj(r,X){", """function realFam(r){if(typeof KEI==='undefined')return;const K=KEI[r.n];if(!K||!K[6])return;const t=K[6];
 const f=t.match(/(?:^|;)父:([^;(]+)\\(([^)]+)\\)/),g=t.match(/(?:^|;)祖父:([^;(]+)\\(([^)]+)\\)/);if(!f)return;
 r.nisei={f:f[1],br:f[2],g:g?{f:g[1],br:g[2]}:null,pr:0,real:1};}
function realAdj(r,X){""")
# 重圧:大一番で −0.2(二世・三世の 4 割)
rep("r._pr=big?(r.a.sho-10)*.09-(r.per==='繊細'?.4:0):0;", "r._pr=big?(r.a.sho-10)*.09-(r.per==='繊細'?.4:0)-(r.nisei&&r.nisei.pr?.2:0):0;")
# 画面
rep("<dt>父</dt><dd>'+esc(r.nisei.f)+'('+esc(r.nisei.br)+')</dd>'", "<dt>父</dt><dd>'+esc(r.nisei.f)+'('+esc(r.nisei.br)+')'+(r.nisei.g?'・<b>三世</b>':'・二世')+'</dd>'+(r.nisei.g?'<dt>祖父</dt><dd>'+esc(r.nisei.g.f)+'('+esc(r.nisei.g.br)+')</dd>':'')")
rep("'<span class=\"tag kin\">二世</span>'", "'<span class=\"tag kin\">'+(p.nisei.g?'三世':'二世')+'</span>'")
rep(")の息子が入門を考えているそうです。「新弟子」に二世の候補が加わりました。'", ")の息子が入門を考えているそうです。「新弟子」に'+(k.g?'三世(祖父は'+k.g.f+')':'二世')+'の候補が加わりました。'")
rep("esc(p.nisei.br)+')", "esc(p.nisei.br)+')'+(p.nisei.g?'・祖父:'+esc(p.nisei.g.f)+'('+esc(p.nisei.g.br)+')':'')+'")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
