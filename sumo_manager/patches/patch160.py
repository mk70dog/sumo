# v156 -> v157:横綱・大関どうしの取組の抜けを直す(ダルマさん「3年間回した時の優勝力士 番付を確認」→「実施」)。
#   上位どうしの取組を後ろへ回すとき、残りの日数ぎりぎりではなく 2 日早めに組み始める
#   (横綱・大関が 5 人だと総当たりに 5 日かかり、ぎりぎりだと日が足りずに当たらないまま終わっていた)。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=156;\nconst SAVE='sumoManager156',SAVE155", "const APPV=157;\nconst SAVE='sumoManager157',SAVE156='sumoManager156',SAVE155")
rep('[SAVE155,SAVE154', '[SAVE156,SAVE155,SAVE154')
rep('<title>Grand Sumo Manager v156', '<title>Grand Sumo Manager v157')
rep("const need=T.filter(a=>remOf(a)>=left).sort(", "const need=T.filter(a=>remOf(a)>=left-2).sort(")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
