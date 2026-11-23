# v149 -> v150:実在の力士・部屋の「乱数で決めていた隠れた値」を、裏付けのある材料から決めるか、全員同じにする(ダルマさん「無作為や裏付けが無いものはなくす」→「実施」→「続ける」)。
#   成長型:30 歳以上で幕内にいる力士=持続(長く強さを保っている)、ほか=普通。けがしやすさ ip:全員 10(けがの差は v99 の過去 5 年の記録 injProne で付く)。
#   安定感 cons:直近 6 場所(休場のあった場所を除く)の勝率のばらつき(data/rec6_2026.txt)。取組数による自然なぶれで割って比べる。4 場所以上ない力士は 10。
#   研究熱心 ap・bm:全員 10。疲れ・調子・気力の始め:全員同じ(20・57・55)。体脂肪:身長と体重だけから(揺れなし)、筋肉の伸びしろも揺れなし。
#   よその部屋:育成の上手さ q=今の弟子のうち関取経験者(最高位が十両以上、DEBUT)の数から、厳しさ hard=報道の裏付けがないので全部屋 なし。数式はすべて推定。
import sys, os, json, statistics as st
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=149;\nconst SAVE='sumoManager149',SAVE148", "const APPV=150;\nconst SAVE='sumoManager150',SAVE149='sumoManager149',SAVE148")
rep('[SAVE148,SAVE147', '[SAVE149,SAVE148,SAVE147')
rep('<title>Grand Sumo Manager v149', '<title>Grand Sumo Manager v150')
d = {}
for l in open(os.path.join(here, '..', 'data', 'rec6_2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    f = l.strip().split('|')
    if len(f) < 7: continue
    w, lo, ab = int(f[4]), int(f[5]), int(f[6]); n = w + lo
    if n < 4 or ab > 0: continue  # 休場のあった場所は、けがで勝率が崩れるので除く
    full = 7 if f[1] == 'S' else 15
    d.setdefault(f[3], []).append((w / n, (0.25 / full) ** .5))
CONS = {}
for k, v in d.items():
    if len(v) < 4: continue
    z = st.pstdev([x[0] for x in v]) / (sum(x[1] for x in v) / len(v))
    CONS[k] = max(4, min(16, round(10 - (z - 1) * 8)))
core = """/* v150:実在の力士・部屋の隠れた値(推定の決め方。引き継ぎ資料に説明) */
const REALCONS=""" + json.dumps(CONS, ensure_ascii=False, separators=(',', ':')) + """;/* 直近 6 場所の勝率のばらつき÷取組数による自然なぶれ→安定感 4〜16 */
function realTraits(r,t,i){r.real=1;r.gt=(r.age>=30&&i<42)?3:1;r.ip=10;r.ap=10;r.bm=10;r.cons=REALCONS[r.n]||10;r.fat=20;r.cond=57;r.mor=55;}
function realQOf(n){let s=0;G.order.forEach(id=>{const r=G.R[id];if(!r||r.ret||!G.heya[r.h]||G.heya[r.h].n!==n)return;const D=DEBUT[r.n];if(D&&/^(横綱|大関|関脇|小結|前頭|十両)/.test(D[1]))s++;});return Math.round(cl(.98+.12*Math.min(1,s/6),.98,1.1)*1000)/1000;}
function realQ(){G.heya.forEach((h,k)=>{if(!h||isPH(k)||h.closed)return;h.q=realQOf(h.n);h.hard=false;});}
"""
rep("function realPop(n,t,i){", core + "function realPop(n,t,i){")
rep("if(fr)r.nat=false;r.pop=realPop(f[1],f[0],i);r.per=REALPER[f[1]]||'ふつう';", "if(fr)r.nat=false;r.pop=realPop(f[1],f[0],i);r.per=REALPER[f[1]]||'ふつう';r.n=f[1];realTraits(r,f[0],i);")
rep(" realMino(G,1);\n buildRanks();\n const o=own();", " realMino(G,1);realQ();\n buildRanks();\n const o=own();")
rep("q:R(.98,1.1),hard:Math.random()<.3,ic:x[1]", "q:1.04,hard:false,ic:x[1]")
rep("{n:P,o2:me0.o2,player:false,q:R(.98,1.1),hard:Math.random()<.3,", "{n:P,o2:me0.o2,player:false,q:realQOf(P),hard:false,")
rep("r.bf=cl(.26+(bmi-38)*.006+randn()*.03,.15,.42);", "r.bf=cl(.26+(bmi-38)*.006+(r.real?0:randn()*.03),.15,.42);")
rep("r.leanMax=Math.max(r.lean+R(4,18),", "r.leanMax=Math.max(r.lean+(r.real?11:R(4,18)),")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, 'CONS', len(CONS))
