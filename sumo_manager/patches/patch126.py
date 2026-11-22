# v122 -> v123:一人相撲でも「育成の成績」(育成点と育成番付)を記録の画面に(ダルマさん「続ける」→ 設計案 →「実施」→ 見本 ik1〜ik3 →「1 3」)。中身は patches/ik123.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=122;\nconst SAVE='sumoManager122',SAVE121", "const APPV=123;\nconst SAVE='sumoManager123',SAVE122='sumoManager122',SAVE121")
rep('[SAVE121,SAVE120', '[SAVE122,SAVE121,SAVE120')
rep('<title>Grand Sumo Manager v122', '<title>Grand Sumo Manager v123')
ui = open(os.path.join(here, 'ik123.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
