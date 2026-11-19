# v95 -> v96:独立の内弟子の候補で、親子を優先する(ダルマさん「修正」)
# 力士の家族に「現・○○親方」(父などが部屋付き親方)とあれば、その親方の弟子として扱う:ほかの親方の候補からは外し、その親方なら「親子」3 点。
# 例:藤ノ川・碇潟(父=甲山親方)は春日山・立川親方の候補に出ない。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep('<title>Grand Sumo Manager v95</title>', '<title>Grand Sumo Manager v96</title>')
rep("const APPV=95;\nconst SAVE='sumoManager95',SAVE94", "const APPV=96;\nconst SAVE='sumoManager96',SAVE95='sumoManager95',SAVE94")
rep('[SAVE94,SAVE93', '[SAVE95,SAVE94,SAVE93')
rep(" if(g.v===94){g.v=95;}\n return g.v===95?g:null;}", " if(g.v===94){g.v=95;}\n if(g.v===95){g.v=96;}\n return g.v===96?g:null;}")
rep('G={v:95,', 'G={v:96,')
rep("  let sc=0;const tg=[];\n  if(U.includes(f[1])){sc+=3;tg.push('内弟子(記事あり)');}",
    "  let sc=0;const tg=[];const fm=k&&k[6]?String(k[6]).match(/現・([^)）・]+?)親方/):null;\n  if(fm){if(fm[1]!==x.n)return;sc+=3;tg.push('親子');}\n  if(U.includes(f[1])){sc+=3;tg.push('内弟子(記事あり)');}")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
