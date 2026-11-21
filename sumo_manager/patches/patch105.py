# v101 -> v102:二人相撲の「勝負の形」を選べるように(ダルマさん「選択制にするのは?」→ 見本 sb0〜sb3 →「実施」)。
# ①点数勝負(5・10・20 年)②先に目標に届いたほうの勝ち(横綱を出す/幕内優勝 3 回/新十両 5 人)③部屋番付 ④記録だけ。
# 親が始めるときに選び(G.mp.sb)、子の参加の画面にも出る。帯に点数・進み具合、記録に「勝負」欄、決着でお知らせ。点数のきまりは推定。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v101</title>', '<title>Grand Sumo Manager v102</title>')
rep("const APPV=101;\nconst SAVE='sumoManager101',SAVE100", "const APPV=102;\nconst SAVE='sumoManager102',SAVE101='sumoManager101',SAVE100")
rep('[SAVE100,SAVE99', '[SAVE101,SAVE100,SAVE99')
rep(" return g.v===101?g:null;}", " if(g.v===101){g.v=102;}\n return g.v===102?g:null;}")
rep('G={v:101,', 'G={v:102,')
ui = open(os.path.join(here, 'shobu102_ui.html'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
