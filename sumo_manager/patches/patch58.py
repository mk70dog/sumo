# システム設定(見本 sys1):見た目・保存データ・不具合の報告・アプリを「⚙ 設定」に集める  v54 -> v55
# 不具合の報告:エラーと主な操作を端末に記録(localStorage の sumoLog、最新 200 件)。「記録をコピー」で版・端末・画面・進み具合と一緒に文章にする。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
js = open(os.path.join(here,'sys58_ui.js'),encoding='utf-8').read()
rep('<title>Sumo Manager v54</title>', '<title>Sumo Manager v55</title>')
rep("const APPV=54;\nconst SAVE='sumoManager54',SAVE53", "const APPV=55;\nconst SAVE='sumoManager55',SAVE54='sumoManager54',SAVE53")
rep('[SAVE53,SAVE52', '[SAVE54,SAVE53,SAVE52')
rep(" if(g.v===53){g.v=54;}\n return g.v===54?g:null;}", " if(g.v===53){g.v=54;}\n if(g.v===54){g.v=55;}\n return g.v===55?g:null;}")
rep('G={v:54,', 'G={v:55,')
rep("const V={home:homeHTML,","const V={sys:sysHTML,home:homeHTML,")
rep("<span class=\"hbtns\"><button class=\"hbtn\" onclick=\"saveNow()\">保存</button>","<span class=\"hbtns\"><button class=\"hbtn gear\" onclick=\"go(\\'sys\\')\">⚙ 設定</button><button class=\"hbtn\" onclick=\"saveNow()\">保存</button>")
i=s.find(" h+='<div class=\"pn\"><h2>記録の保存</h2>");j=s.find("return h;",i)
assert i>0 and j>0
s=s[:i]+" h+='<div class=\"pn\"><p class=\"kaku mute\" style=\"font-size:13px\">保存データ・画面の色・文字の形・アプリの更新は、画面の上の「⚙ 設定」にまとめました。</p></div>';\n "+s[j:]
rep("/* ========== 画面 ========== */","/* ========== 画面 ========== */\n"+js)
# render のエラーも記録
rep("function render(){\n const app=$('#app');","function render(){try{render0();}catch(e){sysLog('エラー',e);throw e;}}\nfunction render0(){\n const app=$('#app');")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
