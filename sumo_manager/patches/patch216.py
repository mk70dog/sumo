# v212 -> v213:土俵の物語(実在の力士の出来事を出典つきで年表に、ゲームの中の出来事も書き足す。人気の上乗せ)。
#   元データ data/story2026.txt、部品 patches/sto216_ui.js。炎鵬の性格を負けず嫌いに(data/per2026.txt)。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=212;\nconst SAVE='sumoManager212',SAVE211", "const APPV=213;\nconst SAVE='sumoManager213',SAVE212='sumoManager212',SAVE211")
rep('[SAVE211,SAVE210', '[SAVE212,SAVE211,SAVE210')
rep('<title>Grand Sumo Manager v212', '<title>Grand Sumo Manager v213')
# 物語のデータ
D = {}
for l in open(os.path.join(here, '..', 'data', 'story2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.rstrip('\n').split('|'); n = a[0]
    d = D.setdefault(n, {'sum': '', 'kind': {}, 'ev': []})
    if a[1] == 'まとめ': d['sum'] = a[2]
    elif a[1] == '型': d['kind'][a[2]] = [int(x) if x.isdigit() else x for x in a[3:]] or [1]
    else: d['ev'].append([a[1], a[2], a[3] if len(a) > 3 else ''])
# 人気の上乗せ(物語の主人公。推定):炎鵬=史上初の復活、王鵬=名門の血筋、高安=悲願を追う元大関
rep("return Math.round(cl(base+k+v+rr+cr,0,100));}", "return Math.round(cl(base+k+v+rr+cr+(STORYP[n]||0),0,100));}\nconst STORYP={\"炎鵬\":16,\"王鵬\":6,\"高安\":3};/* v213:物語の人気の上乗せ(推定) */")
rep("function realTraits(r,t,i){r.real=1;", "function realTraits(r,t,i){r.real=1;r.stP=1;")
rep("for(const id in g.R){const r=g.R[id];if(r.real&&r.per==='ふつう'&&REALPER[r.n])r.per=REALPER[r.n];}",
    "for(const id in g.R){const r=g.R[id];if(r.real&&r.per==='ふつう'&&REALPER[r.n])r.per=REALPER[r.n];if(r.real&&r.n==='炎鵬'&&r.per==='明るい')r.per='負けず嫌い';if(r.real&&!r.stP){r.stP=1;if(STORYP[r.n])r.pop=cl((r.pop||20)+STORYP[r.n],0,100);}}")
P = {}
for l in open(os.path.join(here, '..', 'data', 'per2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.strip().split('|'); P[a[0]] = a[1]
i = s.index('const REALPER='); j = s.index(';', i)
s = s[:i] + 'const REALPER=' + json.dumps(P, ensure_ascii=False, separators=(',', ':')) + s[j:]
# 関取の引退の見直し:35 歳を過ぎた関取は、勝ち越していても毎場所 4 割で引退していた(v212 の測定で 35 歳以上の関取は平均 0.3 人。
#   実際の 2026 年九州場所は 6 人=高安 36・玉鷲 42・千代翔馬 35・正代 35・竜電 36・佐田の海 39)。数字は推定(測定で 2.3〜2.8 人)
rep("else if(r.d<=1){if(r.age>=38)p=1;else if(r.age>=35)p=.4;else if(r.d===1&&r.age>=33&&mk)p=.25;}",
    "else if(r.d<=1){if(r.age>=41)p=.5;else if(r.age>=35)p=.02+.015*(r.age-35)+(mk?.05:0)+(r.d===1&&mk?.06:0)+(rc.ab>=8?.15:0);else if(r.d===1&&r.age>=33&&mk)p=.12;}")
# よその部屋の力士にも物語を出す
rep("・取り口:'+styleName(r)+(r.inj?'・<span class=\"shu\">けがあり</span>':'')+'</p>';", "・取り口:'+styleName(r)+(r.inj?'・<span class=\"shu\">けがあり</span>':'')+'</p>'+(typeof storyHTML==='function'?storyHTML(r):'');")
ui = open(os.path.join(here, 'sto216_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', '<script>window.STORYD=' + json.dumps(D, ensure_ascii=False) + ';\n' + ui + '</script>\n</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, '物語', len(D), '人')
