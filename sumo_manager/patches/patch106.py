# v102 -> v103:二人相撲の「勝負の形」を選ぶ画面を見やすく(ダルマさん「もう少しわかりやすく表示 サンプル×3」→ 見本 sbp1〜sbp3 →「1」)。
# 4 つの形を横並びのタイルに(選んだものは金色+「選択中」)、下に「選んだ形」のまとめ(期間・目標のボタンと決まりの説明)、手順の番号(1 形を選ぶ → 2 始め方)。
# 名前は短く「目標レース」(②)。中身は patches/sbpick103_ui.html(tools/mksbpicksamples.py の sbp1 と同じ)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v102</title>', '<title>Grand Sumo Manager v103</title>')
rep("const APPV=102;\nconst SAVE='sumoManager102',SAVE101", "const APPV=103;\nconst SAVE='sumoManager103',SAVE102='sumoManager102',SAVE101")
rep('[SAVE101,SAVE100', '[SAVE102,SAVE101,SAVE100')
rep(" if(g.v===101){g.v=102;}\n return g.v===102?g:null;}", " if(g.v===101){g.v=102;}\n if(g.v===102){g.v=103;}\n return g.v===103?g:null;}")
rep('G={v:102,', 'G={v:103,')
rep("SB_NAME={1:'点数勝負',2:'先に目標に届いたほうの勝ち'", "SB_NAME={1:'点数勝負',2:'目標レース'")
ui = open(os.path.join(here, 'sbpick103_ui.html'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
