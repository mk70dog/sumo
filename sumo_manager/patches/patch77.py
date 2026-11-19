# v73 -> v74:助言と苦手意識の効き方を直す(ダルマさん「実施」)
# 20 年・10 シードの測定で v72 から横綱の優勝が 48→59% に増えた(実際 45%)。原因は助言(強い部屋ほど多い)と苦手意識(弱い側が強い相手に負け続けてつく)。
# 直し:助言は格上(裏の総合で相手が上)に挑むときだけ、苦手意識は相手が格上でない(総合の差 0.5 以内か格下)ときだけ効く。試し版で横綱 51.7%・平幕 14.5%。
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
rep('<title>Sumo Manager v73</title>', '<title>Sumo Manager v74</title>')
rep("const APPV=73;\nconst SAVE='sumoManager73',SAVE72", "const APPV=74;\nconst SAVE='sumoManager74',SAVE73='sumoManager73',SAVE72")
rep('[SAVE72,SAVE71', '[SAVE73,SAVE72,SAVE71')
rep(" if(g.v===72){g.v=73;}\n return g.v===73?g:null;}", " if(g.v===72){g.v=73;}\n if(g.v===73){g.v=74;}\n return g.v===74?g:null;}")
rep('G={v:73,', 'G={v:74,')
rep("function nigate(r,o){const t=h2rOf(r,o);return t.length>=4&&t.split('x').length-1>=4;}",
    "function nigate(r,o){const t=h2rOf(r,o);return t.length>=4&&t.split('x').length-1>=4&&ovr(o)-ovr(r)<=.5;}\nfunction advOn(r,o){return ovr(o)>ovr(r)?advMate(r,o):null;}")
rep("r._pr+=kenB(r)+(advMate(r,o)?.15:0)", "r._pr+=kenB(r)+(advOn(r,o)?.15:0)")
rep("const m=advMate(a,o);if(m)L.push(", "const m=advOn(a,o);if(m)L.push(")
rep("(勝てば消えます)。</div>", "(勝てば消えます。格上の相手には苦手意識はつきません)。</div>")
rep("に勝ち越している)</div>「", "に勝ち越している。格上に挑むときの助言)</div>「")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst)
