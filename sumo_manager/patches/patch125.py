# v121 -> v122:二人相撲 第 3 段階=通信が切れたときの扱い(ダルマさん「続ける」→ 設計案 →「実施」→ 見本 cn1〜cn3 →「お任せで実施」=cn1)。
# 中身は patches/mp122.js。親の「相手を待つ時間」(10 分の決め打ち)と「待たずに進める」は、ここで本体の文字を書きかえる。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=121;\nconst SAVE='sumoManager121',SAVE120", "const APPV=122;\nconst SAVE='sumoManager122',SAVE121='sumoManager121',SAVE120")
rep('[SAVE120,SAVE119', '[SAVE121,SAVE120,SAVE119')
rep('<title>Grand Sumo Manager v121', '<title>Grand Sumo Manager v122')
rep("const late=Date.now()-(m.since||Date.now())>10*60*1000;", "const late=!!m.go||Date.now()-(m.since||Date.now())>mpWaitMs();", 2)
rep("m.act=null;m.hReady=0;m.n++;", "m.act=null;m.hReady=0;m.go=0;m.n++;", 2)
rep("の準備が 10 分間なかったので、", "'+(m.go?'の準備を待たずに':'の準備が '+(m.wait||10)+' 分間なかったので、')+'", 2)
ui = open(os.path.join(here, 'mp122.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
