# v148 -> v149:実在の力士の人気と性格を、乱数・番付だけでなく裏付けのある材料から(ダルマさん「宇良より美ノ海の人気が上」「無作為や裏付けが無いものはなくす」→ 設計案 →「実施」)。
#   人気:data/pop2026.txt(懸賞の申し込み本数 2026 年の 4 場所、人気投票 2026・2025)+ 番付 + これまでの実績(RKCAR)。式は推定。
#   性格:data/per2026.txt(報道で人柄がはっきりしている力士だけ)。ほかの実在の力士は「ふつう」(効き目なし)。架空の新弟子は今までどおり。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=148;\nconst SAVE='sumoManager148',SAVE147", "const APPV=149;\nconst SAVE='sumoManager149',SAVE148='sumoManager148',SAVE147")
rep('[SAVE147,SAVE146', '[SAVE148,SAVE147,SAVE146')
rep('<title>Grand Sumo Manager v148', '<title>Grand Sumo Manager v149')
data = os.path.join(here, '..', 'data')
K, V, RR = {}, {}, {}
for l in open(os.path.join(data, 'pop2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    t, a, n, x = l.strip().split('|')
    if t == 'K': K[n] = K.get(n, 0) + int(x)
    elif t == 'V': V[n] = int(x)
    elif t == 'R': RR[n] = int(x)
P = {}
for l in open(os.path.join(data, 'per2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.strip().split('|'); P[a[0]] = a[1]
J = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'))
core = """/* v149:実在の力士の人気と性格(data/pop2026.txt・data/per2026.txt。出典は引き継ぎ資料) */
const POPK=""" + J(K) + """;/* 懸賞の申し込み本数 2026 年夏・名古屋・秋・九州の合計(上位に載った分) */
const POPV=""" + J(V) + """;/* 人気投票 2026 年版の票数(3,498 人) */
const POPR=""" + J(RR) + """;/* 人気投票 2025 年九月場所の順位(1〜5 位) */
const REALPER=""" + J(P) + """;
/* 人気=番付の土台+懸賞(4 場所の平均÷15、20 まで)+投票(票数÷25)+2025 年の順位(6−順位)+実績(幕内優勝 2・十両優勝 0.5・金星 1・三賞 0.7、10 まで)。式は推定 */
function realPop(n,t,i){const base=t==='Y'?50:t==='O'?42:t?32:i<42?22:i<70?14:6;
 const k=Math.min(20,(POPK[n]||0)/4/15),v=(POPV[n]||0)/25,rr=POPR[n]?6-POPR[n]:0;const c=RKCAR[n];
 const cr=c?Math.min(10,c[0]*2+c[1]*.5+c[6]+c[7]*.7):0;return Math.round(cl(base+k+v+rr+cr,0,100));}
"""
rep("const PERD={", core + "const PERD={ふつう:'目立った癖はない(実在の力士で、人柄の裏付けが取れていないため効き目なし)',")
rep("if(fr)r.nat=false;r.pop=f[0]==='Y'?80:f[0]==='O'?65:f[0]?50:i<42?35:i<70?25:15;",
    "if(fr)r.nat=false;r.pop=realPop(f[1],f[0],i);r.per=REALPER[f[1]]||'ふつう';")
rep(" if(Math.random()<.5)r.per=k.per;", " if(Math.random()<.5&&k.per&&k.per!=='ふつう')r.per=k.per;")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, 'K', len(K), 'V', len(V), 'per', len(P))
