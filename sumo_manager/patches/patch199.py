# v195 -> v196:部屋の 1 画面の高さを実際の画面の高さに合わせる
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=195;\nconst SAVE='sumoManager195',SAVE194", "const APPV=196;\nconst SAVE='sumoManager196',SAVE195='sumoManager195',SAVE194")
rep('[SAVE194,SAVE193', '[SAVE195,SAVE194,SAVE193')
rep('<title>Grand Sumo Manager v195', '<title>Grand Sumo Manager v196')
# v195 の 1 画面の部分を外す(v196 の js で入れ直す)
i=s.index('<style>/* v195:部屋の画面を iPad で 1 画面に');j=s.index('</script>',i)+len('</script>')
s=s[:i]+s[j:]
ui = open(os.path.join(here, 'fv196_ui.js'), encoding='utf-8').read()

rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
