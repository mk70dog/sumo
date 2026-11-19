# v74 -> v75:合口(あいくち。力士の組み合わせごとの生まれつきの相性)(ダルマさん「実施」)
# ダルマさん「格下が上に勝てないのは普通。同格や格下だが、なぜかこの相手とは合口が悪いことがある」。
# 実際の例:稀勢の里は把瑠都に 6 勝 21 敗(Number 2023/7/16)、栃東に 0 勝 5 敗(Number 2025/3/1)。豊昇龍は格下の安青錦に 1 勝 4 敗(日刊ゲンダイ)。大の里は阿炎に連敗(東スポ)。
# 仕組み(推定):組み合わせの 1 割ほどで、片方が +0.3・もう片方が −0.3(合計 0。番付と関係なく決まるので上位だけが得をしない)。見えないが、対戦成績から画面に出る。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v74</title>', '<title>Sumo Manager v75</title>')
rep("const APPV=74;\nconst SAVE='sumoManager74',SAVE73", "const APPV=75;\nconst SAVE='sumoManager75',SAVE74='sumoManager74',SAVE73")
rep('[SAVE73,SAVE72', '[SAVE74,SAVE73,SAVE72')
rep(" if(g.v===73){g.v=74;}\n return g.v===74?g:null;}", " if(g.v===73){g.v=74;}\n if(g.v===74){g.v=75;}\n return g.v===75?g:null;}")
rep('G={v:74,', 'G={v:75,')
rep("function advOn(r,o){",
    "function aikuchi(r,o){const lo=Math.min(r.id,o.id),hi=Math.max(r.id,o.id);const x=hhR(Math.imul(lo,7919)+hi,11);const v=x<.05?.3:x>.95?-.3:0;return r.id===lo?v:-v;}\nfunction advOn(r,o){")
rep("r._pr+=kenB(r)+(advOn(r,o)?.15:0)", "r._pr+=kenB(r)+aikuchi(r,o)+(advOn(r,o)?.15:0)")
# 画面:対戦 6 番以上で、力の差のわりに大きく勝ち越し・負け越している組み合わせに出す
rep(" const dw=Math.round((a.w||150)-(o.w||150));if(Math.abs(dw)>=40)",
    " {const hx=(a.h2h&&a.h2h[o.id])||[0,0];const n=hx[0]+hx[1],d=ovr(o)-ovr(a);if(n>=6){if(hx[1]-hx[0]>=3&&d<=.5)L.push('<div class=\"shu kaku\" style=\"font-size:13px\">合口:この相手とは合口が悪いようです(対戦 '+hx[0]+'勝'+hx[1]+'敗。力の差のわりに負けている)</div>');else if(hx[0]-hx[1]>=3&&d>=-.5)L.push('<div class=\"kaku\" style=\"font-size:13px;color:#b5651d\">合口:この相手とは合口が良いようです(対戦 '+hx[0]+'勝'+hx[1]+'敗)</div>');}}\n const dw=Math.round((a.w||150)-(o.w||150));if(Math.abs(dw)>=40)")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
