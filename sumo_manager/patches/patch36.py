# 横綱の強さ:成績不振での途中休場と、皆勤負け越しでの引退  v32 -> v33
# 実際:優勝争いが求められる横綱は、成績不振になった時点で休場するのが通例(東京スポーツ)。
#   ゲームの横綱(ほかの部屋)は 1 場所も休まず平幕に負け続け、金星が年 17 個(横綱 1 人・1 場所 約 1.6 個)。
#   実際の金星配給は 1 場所平均で 白鵬 0.31・大鵬 0.48・千代の富士 0.49・貴乃花 0.79・北の湖 0.84、
#   稀勢の里 2.25(全休を除く)、照ノ富士 在位 19 場所で 21 個、豊昇龍 2.5(マネーポスト)。平均は 1 個前後と推定。
# ①ほかの部屋の横綱は、12 日目までに 3 敗以上して負けが勝ちの半分以上なら、負けた日に 25% で休場(確率は推定)。
# ②皆勤で負け越した横綱は引退しやすく(28 歳以上 60%、それ未満 35%。推定)。大乃国は 27 歳で 7 勝 8 敗のあと進退伺を出し、
#   理事長に慰留されて続けた(日刊ゲンダイ)。30 歳以上で皆勤 9 勝以下でも 12%。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v32</title>', '<title>Sumo Manager v33</title>')
rep("const APPV=32;\nconst SAVE='sumoManager32',SAVE31", "const APPV=33;\nconst SAVE='sumoManager33',SAVE32='sumoManager32',SAVE31")
rep('[SAVE31,SAVE30', '[SAVE32,SAVE31,SAVE30')
rep(" if(g.v===31){g.v=32;}\n return g.v===32?g:null;}", " if(g.v===31){g.v=32;}\n if(g.v===32){g.v=33;}\n return g.v===33?g:null;}")
rep('G={v:32,', 'G={v:33,')
rep(" return {w:W.id,l:L.id,k:f.k,day:day,nar:f.nar,big:ctx.big};\n}",
    " if(L.t==='Y'&&L.h!==0&&day<=12){const c=B.rec[L.id];if(!c.ky&&c.l>=3&&c.l*3>=day&&Math.random()<.25){goKyujo(L,day);addNews('横綱'+L.n+'が成績不振のため'+(day+1)+'日目から休場します。');}}\n return {w:W.id,l:L.id,k:f.k,day:day,nar:f.nar,big:ctx.big};\n}")
rep("else if(rc.ab>=8&&r.age>=32)p=.15;else if(mk&&r.age>=30)p=.18;",
    "else if(rc.ab>=8&&r.age>=32)p=.15;else if(mk&&rc.ab===0)p=r.age>=28?.6:.35;else if(mk&&r.age>=30)p=.18;else if(rc.ab===0&&rc.w<=9&&r.age>=30)p=.12;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
