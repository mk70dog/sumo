# v141 -> v142:独立の段取りを場面にする(① 師匠に打ち明ける ② 弟子に声をかける ③ 理事会 ④ 門出)。親方・力士の言葉には絵を入れる。朝日山親方(元琴錦)・安治川親方(元安美錦)・荒汐親方(元蒼国来)・浦風親方(元敷島)・雷親方(元垣添)の絵。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=141;\nconst SAVE='sumoManager141',SAVE140", "const APPV=142;\nconst SAVE='sumoManager142',SAVE141='sumoManager141',SAVE140")
rep('[SAVE140,SAVE139', '[SAVE141,SAVE140,SAVE139')
rep('<title>Grand Sumo Manager v141', '<title>Grand Sumo Manager v142')
core = open(os.path.join(here, 'dp142_core.js'), encoding='utf-8').read()
rep('function doWeek(){\n if(G.phase!==\'train\')return;\n', core + 'function doWeek(){\n if(G.phase!==\'train\')return;\n')
ui = open(os.path.join(here, 'dp142_ui.js'), encoding='utf-8').read()
pi = open(os.path.join(here, 'pi142_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + pi + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
