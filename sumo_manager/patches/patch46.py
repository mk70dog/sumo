# 部屋付き親方として独立するモード(見本 dokuritsu)  v42 -> v43
# 新設の条件:「横綱・大関以上」「三役25場所以上」「幕内60場所以上」(相撲ファンのブログ。協会の正式文書は未確認)→ 最高位 小結以上で 65 歳前の部屋付き親方(推定)。
# 内弟子:連れて行けるのは自分の内弟子が原則(日刊ゲンダイ)→ 親方の引退より後に入門したと考えられる力士(生年と学歴から推定。学歴不明は高卒入門)。
# 人数 1〜8(武隈 3・押尾川 3・音羽山 2・安治川 1・中村 8、マネーポスト・文藝春秋)。関取も可(中村部屋は幕内友風・新十両嘉陽)。横綱・大関は不可。
# 始め:自己資金 1000 万円+最高位の上乗せ(横綱 1500・大関 1000・三役 500)、借りもの、施設 1・1・1・2、一門は元の部屋と同じ(推定)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
core = open(os.path.join(here,'dok46_core.js'),encoding='utf-8').read()
ui = open(os.path.join(here,'dok46_ui.js'),encoding='utf-8').read()
rep('<title>Sumo Manager v42</title>', '<title>Sumo Manager v43</title>')
rep("const APPV=42;\nconst SAVE='sumoManager42',SAVE41", "const APPV=43;\nconst SAVE='sumoManager43',SAVE42='sumoManager42',SAVE41")
rep('[SAVE41,SAVE40', '[SAVE42,SAVE41,SAVE40')
rep(" if(g.v===41){g.v=42;}\n return g.v===42?g:null;}", " if(g.v===41){g.v=42;}\n if(g.v===42){g.v=43;}\n return g.v===43?g:null;}")
rep('G={v:42,', 'G={v:43,')
rep("/* ========== 画面 ========== */", core+"/* ========== 画面 ========== */")
rep("function heyaClose(){", ui.replace("const DOKMON={'横綱':1500,'大関':1000,'関脇':500,'小結':500};","")+"function heyaClose(){")
rep("UI.start==='real'?realStartHTML():startHTML()","UI.start==='real'?realStartHTML():UI.start==='dok'?dokHTML():startHTML()")
rep("(UI.start==='real'?' wide':'')","(UI.start==='real'||UI.start==='dok'?' wide':'')")
rep("(0?'<button class=\"st-new\"","'<button class=\"st-dok\" onclick=\"goStart(\\'dok\\')\"><b>部屋付き親方として独立する</b><small>実在の部屋付き親方を選び、内弟子を連れて新しい部屋を興します。</small></button>'+(0?'<button class=\"st-new\"")
rep(".st-go .st-real{background:rgba(179,38,30,.92)}",".st-go .st-real{background:rgba(179,38,30,.92)}.st-go .st-dok{background:rgba(32,72,52,.92)}.dkw{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:4px 10px;max-height:34vh;overflow:auto;border:1px solid var(--line);border-radius:4px;padding:6px 8px}.dkc{display:flex!important;align-items:center;gap:6px;margin:0!important;font:14px var(--kaku)!important}.dkc span{color:#7d7365;font-size:12px}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok')
