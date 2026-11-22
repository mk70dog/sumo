# v120 -> v121:二人相撲の勝負の点を「部屋で育てた力士」だけで数えられるように(ダルマさん「勝負の点数の見直し」→ 設計案 →「実施」→ 見本 sbc1・sbc2 →「2」)。
# あわせて、ホーム画面のアプリの名前(本体の apple-mobile-web-app-title)を「sumo manager」に。中身は patches/sbc121.js。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=120;\nconst SAVE='sumoManager120',SAVE119", "const APPV=121;\nconst SAVE='sumoManager121',SAVE120='sumoManager120',SAVE119")
rep('[SAVE119,SAVE118', '[SAVE120,SAVE119,SAVE118')
rep('<title>Grand Sumo Manager v120', '<title>Grand Sumo Manager v121')
rep('<meta name="apple-mobile-web-app-title" content="Grand Sumo">', '<meta name="apple-mobile-web-app-title" content="sumo manager">')
ui = open(os.path.join(here, 'sbc121.js'), encoding='utf-8').read()
rep('</script></body>\n</html>', '</script>\n' + ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
