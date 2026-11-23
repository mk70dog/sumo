# v152 -> v153:部屋の会話(ダルマさん「ホームの画面に親方をはじめ色々な方面から会話形式のコメントをポップアップで表示。独立モード時のはじめのやり取りのような会話形式」→ 見本 cv1〜cv3 →「cv1&3」)。
#   部品は patches/cv153.js(本体のいちばん最後、</body> の前に入れる。homeHTML を包む)。見本は tools/mkconvsamples.py。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=152;\nconst SAVE='sumoManager152',SAVE151", "const APPV=153;\nconst SAVE='sumoManager153',SAVE152='sumoManager152',SAVE151")
rep('[SAVE151,SAVE150', '[SAVE152,SAVE151,SAVE150')
rep('<title>Grand Sumo Manager v152', '<title>Grand Sumo Manager v153')
cv = open(os.path.join(here, 'cv153.js'), encoding='utf-8').read()
rep('</body>', cv + '\n</body>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
