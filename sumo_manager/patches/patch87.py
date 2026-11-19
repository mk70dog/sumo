# v83 -> v84:二人相撲の親を「部屋付き親方として独立する」でも始められるように(ダルマさん「2人モード 部屋独立を追加」)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v83</title>', '<title>Grand Sumo Manager v84</title>')
rep("const APPV=83;\nconst SAVE='sumoManager83',SAVE82", "const APPV=84;\nconst SAVE='sumoManager84',SAVE83='sumoManager83',SAVE82")
rep('[SAVE82,SAVE81', '[SAVE83,SAVE82,SAVE81')
rep(" if(g.v===82){g.v=83;}\n return g.v===83?g:null;}", " if(g.v===82){g.v=83;}\n if(g.v===83){g.v=84;}\n return g.v===84?g:null;}")
rep('G={v:83,', 'G={v:84,')
# 親の始め方を 2 つに
rep("function mpNewHost(){if(!mpTok()&&!MPT.mock){alertM('鍵がありません','先に GitHub の鍵を入れてください。');return;}UI.mpNew=1;goStart('real');}",
    "function mpNewHost(k){if(!mpTok()&&!MPT.mock){alertM('鍵がありません','先に GitHub の鍵を入れてください。');return;}UI.mpNew=1;goStart(k||'real');}\n"
    "const mpNGD=newGameDok;newGameDok=function(){mpNGD.apply(this,arguments);if(UI.mpNew){G.mp={role:'host',id:null,gh:-1,n:0,act:null,hReady:0};UI.mpNew=0;setTimeout(mpHostInit,0);}};")
rep("'<button class=\"st-real\" onclick=\"mpNewHost()\"><b>親になって新しく始める</b><small>実在の部屋を選んで世界を作ります。合言葉が出るので、相手に伝えます。</small></button>'",
    "'<button class=\"st-real\" onclick=\"mpNewHost(\\'real\\')\"><b>親:実在の部屋を選んで始める</b><small>実在の部屋を選んで世界を作ります。合言葉が出るので、相手に伝えます。</small></button>'+\n  '<button class=\"st-real st-dok2\" onclick=\"mpNewHost(\\'dok\\')\"><b>親:部屋付き親方として独立して始める</b><small>実在の部屋付き親方を選び、内弟子を連れて新しい部屋を興して世界を作ります。</small></button>'")
# 実在の部屋・独立の画面から「戻る」で二人相撲の画面に戻ったときは、mpNew を消す
rep("function topMode(k){UI.mode=k;", "function topMode(k){UI.mode=k;if(k!=='two')UI.mpNew=0;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
