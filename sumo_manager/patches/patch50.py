# 文言の見直し(プレイヤーは部屋を見守る存在。親方への呼びかけ・古い呼び名を直す)  v46 -> v47
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v46</title>', '<title>Sumo Manager v47</title>')
rep("const APPV=46;\nconst SAVE='sumoManager46',SAVE45", "const APPV=47;\nconst SAVE='sumoManager47',SAVE46='sumoManager46',SAVE45")
rep('[SAVE45,SAVE44', '[SAVE46,SAVE45,SAVE44')
rep(" if(g.v===45){g.v=46;}\n return g.v===46?g:null;}", " if(g.v===45){g.v=46;}\n if(g.v===46){g.v=47;}\n return g.v===47?g:null;}")
rep('G={v:46,', 'G={v:47,')
rep("定年(65 歳)が近づいています。年寄名跡を持つ部屋付き親方を育てておきましょう。", "定年(65 歳)が近づき、年寄名跡を持つ部屋付き親方の中から後継ぎを考え始めています。")
rep("約 1 年のうちに後継者を決めましょう。", "約 1 年のうちに後継者を決めることになります。")
rep("弟子がいません。「スカウト」で新弟子を探しましょう。", "弟子がいません。「新弟子」で入門の候補が見られます。")
rep("少し軽めにしましょう。", "親方は少し軽めにしようか考えています。")
rep("関心が高い候補は早めに勧誘しましょう。", "関心が高い候補は早めに勧誘したほうがよさそうです。")
rep("関取・幕内・三役・大関・横綱・各段優勝などを目指しましょう。", "関取・幕内・三役・大関・横綱・各段優勝などで記録されます。")
rep("少し時間をおきましょう。", "少し時間をおいたほうがよさそうです。")
rep("親方として部屋を開き、弟子を育てて横綱を目指します。", "新しく開いた部屋で、親方が弟子を育てて横綱を目指す姿を見守ります。")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
