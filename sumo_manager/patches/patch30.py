# 設計 20:経歴をゲームに使う  v26 -> v27
#  1 血縁 4 親等以内は本割で当たらない(内規。優勝決定戦は別)
#  2 新十両の化粧廻しを「母校から贈ってもらう」
#  3 実名スタートで出身校を経歴データから入れ、学校との関係に反映
#  4 ゲームの中で入門した力士の経歴タブに、学校の大会の成績(8 強以上)と付出の資格
import os, sys, json, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)
DD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data') + os.sep
def load(fn, nf):
    out = []
    for l in open(DD + fn, encoding='utf-8'):
        if l.startswith('#') or not l.strip(): continue
        p = l.rstrip('\n').split('|')
        assert len(p) == nf, (fn, l)
        out.append(p)
    return out
RK = load('keireki2026.txt', 9) + load('keireki_low2026.txt', 9)
TK = load('keireki_toshi2026.txt', 10)

# --- 1 血縁(4 親等以内)の組 ---
BLOOD = re.compile(r'^(父|母|長男|次男|三男|四男|子|兄|弟|姉|妹|祖父|祖母|孫|叔父|伯父|甥|従兄|従弟|いとこ)')
def fam(f):
    out = []
    for x in f.split(';'):
        m = re.match(r'^([^:]+):(.+)$', x)
        if not m: continue
        rel, who = m.group(1), m.group(2)
        if '妻' in rel or '義' in rel or not BLOOD.match(rel): continue
        nm = re.sub(r'[(（].*$', '', who).strip()
        if nm and nm != '元力士': out.append((rel, nm))
    return out
KIN = {}
def link(a, b):
    if a == b: return
    KIN.setdefault(a, set()).add(b); KIN.setdefault(b, set()).add(a)
parents = {}
for p in RK:
    for rel, nm in fam(p[7]):
        link(p[0], nm)
        if rel in ('父', '母'): parents.setdefault(nm, set()).add(p[0])
for p in TK:          # 親方の子どうしは兄弟
    kids = [nm for rel, nm in fam(p[8]) if re.match(r'^(長男|次男|三男|四男|子)', rel)]
    for k in kids: parents.setdefault(p[1], set()).add(k)
for par, kids in parents.items():
    kids = list(kids)
    for i in range(len(kids)):
        for j in range(i + 1, len(kids)): link(kids[i], kids[j])
KINP = {k: sorted(v) for k, v in KIN.items()}
print('血縁の組', sum(len(v) for v in KINP.values()) // 2, sorted(KINP.items())[:12])

# --- 3 出身校(ゲームの学校一覧に合わせる) ---
i = s.index('SCH=[')
SCH = json.loads(s[i + 4:s.index(';', i)].split('\n')[0])
ALIAS = {'新潟海洋': ['海洋高等学校'], '日体大柏': ['日本体育大学柏', '日体大柏'], '学法福島': ['学法福島', '学校法人福島'], '向の岡工業': ['向の岡工業']}
def schHS(t):
    if not t: return ''
    for x in SCH:
        if x[1] != '高': continue
        for a in ALIAS.get(x[0], [x[0]]):
            if a in t: return x[0]
    return ''
def schU(t):
    if not t or '未確認' in t or '中退' in t or '大学院' in t: return ''
    for x in SCH:
        if x[1] == '大' and t.startswith(x[0]): return x[0]
    return ''
KSCH = {}
for p in RK:
    h, u = schHS(p[3]), schU(p[4])
    if h or u: KSCH[p[0]] = [h, u]
print('学校が分かる力士', len(KSCH))

CORE = ('const KINP=' + json.dumps(KINP, ensure_ascii=False, separators=(',', ':')) + ';\n'
        'const KSCH=' + json.dumps(KSCH, ensure_ascii=False, separators=(',', ':')) + ';\n')

# 版
rep('<title>Sumo Manager v26</title>', '<title>Sumo Manager v27</title>')
rep("const APPV=26;\nconst SAVE='sumoManager26',SAVE25", "const APPV=27;\nconst SAVE='sumoManager27',SAVE26='sumoManager26',SAVE25")
rep('[SAVE25,SAVE24', '[SAVE26,SAVE25,SAVE24')
rep("if(g.v===25){for(const id in g.R){const r=g.R[id];if(r&&r.debut&&!r.kk)r.kk=r.n;}g.v=26;}\n return g.v===26?g:null;}",
    "if(g.v===25){for(const id in g.R){const r=g.R[id];if(r&&r.debut&&!r.kk)r.kk=r.n;}g.v=26;}\n if(g.v===26){g.v=27;}\n return g.v===27?g:null;}")
rep('G={v:26,', 'G={v:27,')
rep('const APPV=27;', CORE + 'const APPV=27;')

# 1 血縁は本割で当たらない(優勝決定戦は本割の外なので当たる)
rep("function kin2(a,b){const f=x=>x.nisei?x.nisei.f:(x.fam||'');const p=f(a),q=f(b);return !!p&&p===q;}",
    "function kin2(a,b){const f=x=>x.nisei?x.nisei.f:(x.fam||'');const p=f(a),q=f(b);if(!!p&&p===q)return true;const L=KINP[a.kk||a.n];return !!(L&&b&&L.includes(b.kk||b.n));}")

# 3 実名スタート:出身校を入れる(空いているときだけ)
rep("for(const id in X.R){const r=X.R[id];r.kk=r.n;",
    "for(const id in X.R){const r=X.R[id];r.kk=r.n;const ks=KSCH[r.n];if(ks){if(ks[0]&&!r.hs)r.hs=ks[0];if(ks[1]&&!r.uni)r.uni=ks[1];}")

# 4 新弟子の大会記録を残す(同じ配列を指すので、入門までの結果も載る)
rep("if(a.kind==='高')r.hs=a.sch;else if(a.kind==='大')r.uni=a.sch;",
    "if(a.kind==='高')r.hs=a.sch;else if(a.kind==='大')r.uni=a.sch;r.arec=a.rec;")

# 2 母校から化粧廻し
rep("c:()=>['後援会に贈ってもらう','部屋で作る(150 万円)','兄弟子から借りる'],",
    "c:e=>{const L=['後援会に贈ってもらう','部屋で作る(150 万円)','兄弟子から借りる'];const m=bokou(G.R[e.rid]);if(m)L.push('母校('+m.n+')から贈ってもらう');return L;},")
rep("   r.mor=cl(r.mor-3,0,100);return '兄弟子の化粧廻しを借りて、土俵入りに臨みます。';}}",
    "   if(i===3){const m=bokou(r);if(m){r.pop=cl((r.pop||20)+2,0,100);G.rep=cl(G.rep+1,0,100);r.mor=cl(r.mor+2,0,100);if(m.k){G.rel=G.rel||{};G.rel[m.k]=Math.min(100,(G.rel[m.k]||0)+10);}"
    "return '母校の'+m.n+'から、'+r.n+'に化粧廻しが贈られました(部屋の負担はありません)。'+(m.k?'学校との縁が深まりました。':'');}}\n"
    "   r.mor=cl(r.mor-3,0,100);return '兄弟子の化粧廻しを借りて、土俵入りに臨みます。';}}")
BOKOU = r"""
/* v27 母校(化粧廻しを贈ってくれる学校):大学を優先、なければ高校 */
function bokou(r){if(!r)return null;const K=(typeof KEI!=='undefined')?KEI[r.kk||r.n]:null;
 const ok=t=>t&&!/未確認|中退|大学院/.test(t);const cut=t=>t.replace(/[(（].*$/,'');
 if(K&&ok(K[3]))return {n:cut(K[3]),k:r.uni&&schOf(r.uni)?r.uni:''};
 if(r.uni)return {n:schLabel(r.uni),k:schOf(r.uni)?r.uni:''};
 if(K&&ok(K[2]))return {n:cut(K[2]),k:r.hs&&schOf(r.hs)?r.hs:''};
 if(r.hs)return {n:schLabel(r.hs),k:schOf(r.hs)?r.hs:''};
 return null;}
"""
rep("function kin2(a,b){", BOKOU + "function kin2(a,b){")

# 4 経歴タブ:ゲームの中で入門した力士の大会成績と付出
rep("function keiR(r){const k=keiOf(r);if(k)return keiCard(r.n,k);\n return keiCard(r.n,[r.home||'','',r.hs?r.hs+'高校':'',r.uni||'','','',",
    "function keiAma(r){const L=(r.arec||[]).filter(x=>x.p<=8).map(x=>bname(x.b).split(' ')[0]+' '+x.t+' '+(x.p===1?'優勝':x.p===2?'準優勝':x.p<=4?'ベスト4':'ベスト8'));"
    "if(r.tsuke)L.push((r.tsuke==='MS'?'幕下最下位格付出':'三段目最下位格付出')+'の資格で入門');return L.join(';');}\n"
    "function keiR(r){const k=keiOf(r);if(k)return keiCard(r.n,k);\n return keiCard(r.n,[r.home||'','',r.hs?schLabel(r.hs):'',r.uni||'','',keiAma(r),")

# 経歴データの差し替え(翠富士・千代翔馬の家族の欄を直した)
KEI = {p[0]: p[1:] for p in RK}
KEIT = {p[1]: p[2:] for p in TK}
a = s.index('const KEI='); b = s.index('const KEIT=', a); c = s.index(';\n', b) + 2
s = s[:a] + 'const KEI=' + json.dumps(KEI, ensure_ascii=False, separators=(',', ':')) + ';\nconst KEIT=' + json.dumps(KEIT, ensure_ascii=False, separators=(',', ':')) + ';\n' + s[c:]

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
