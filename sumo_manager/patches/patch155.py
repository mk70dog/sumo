# v151 -> v152:性格を報道の言葉に合わせて 10 種類に、効き目も見直し、角界の心のケアを足す(ダルマさん「報道の言葉に合わせて見直し実施」「一緒に見直し」「心のメンテナンスは角界では?」→ 設計案 →「実施」)。
#  ①「おっとり」→「マイペース」、新しく「明るい」「冷静」。架空の新弟子も 10 種類から。
#  ② 効き目:負けず嫌い・豪快の「不祥事や兄弟子の暴力の芽が出やすい」をやめる(性格の言葉からの決めつけ)。マイペース=疲れが抜けやすく、負けても気持ちが揺れにくい。
#     明るい=部屋の雰囲気が少し良くなる・人気が伸びやすい・負けても引きずらない。冷静=大一番の重圧なし(+0.2)・気持ちの上下が小さい。職人肌=相手の研究が 1.3 倍効く。
#  ③ 心のケア:「辞めたいという相談」に「協会のよろず相談窓口を紹介する」(令和 6 年度事業報告)。外部契約に「メンタルトレーニング(関取の個人契約、本人が 1 場所 8 万円)」=大一番の重圧と負けたあとの落ち込みが小さい、繊細な力士によく効く。
#     タニマチの心の支え:親しさ 50 以上のタニマチがいる部屋の関取は、負けたあとの落ち込みが 2 割小さい。数字はすべて推定。
import sys, os, json
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=151;\nconst SAVE='sumoManager151',SAVE150", "const APPV=152;\nconst SAVE='sumoManager152',SAVE151='sumoManager151',SAVE150")
rep('[SAVE150,SAVE149', '[SAVE151,SAVE150,SAVE149')
rep('<title>Grand Sumo Manager v151', '<title>Grand Sumo Manager v152')
# ① 名前と種類
n = s.count('おっとり'); s = s.replace('おっとり', 'マイペース'); print('おっとり→マイペース', n)
rep("const PER=['真面目','負けず嫌い','気分屋','マイペース','野心家','繊細','豪快','職人肌'];", "const PER=['真面目','負けず嫌い','気分屋','マイペース','野心家','繊細','豪快','職人肌','明るい','冷静'];")
P = {}
for l in open(os.path.join(here, '..', 'data', 'per2026.txt'), encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    a = l.strip().split('|'); P[a[0]] = a[1]
i = s.index('const REALPER='); j = s.index(';\n', i)
s = s[:i] + 'const REALPER=' + json.dumps(P, ensure_ascii=False, separators=(',', ':')) + s[j:]
rep("マイペース:'疲れをためにくいが闘志は控えめ'", "マイペース:'疲れをためにくく、負けても気持ちが揺れにくい'")
rep("職人肌:'技の稽古の伸びが良い'}", "職人肌:'技の稽古の伸びが良く、相手の研究がよく効く',明るい:'部屋の雰囲気を明るくし、人気が伸びやすく、負けても引きずらない',冷静:'大一番でも重圧を受けず、気持ちの上下が小さい'}")
rep("for(const id in g.R){const r=g.R[id];if(r.ap==null)", "for(const id in g.R){const r=g.R[id];if(r.per==='おっ'+'とり')r.per='マイペース';if(r.ap==null)")
rep("if(Math.random()<.5&&k.per&&k.per!=='ふつう')r.per=k.per;", "if(Math.random()<.5&&k.per&&k.per!=='ふつう')r.per=(k.per==='おっ'+'とり'?'マイペース':k.per);")
# ② 効き目
rep("   if(r.per==='豪快'||r.per==='負けず嫌い')p*=1.25;if((r.pop||0)>=40)", "   if((r.pop||0)>=40)")
rep("((an.per==='豪快'||an.per==='負けず嫌い')?1.6:1)", "1")
rep("r.mor=cl(r.mor+(won?1.5:(r.per==='負けず嫌い'?-.6:r.per==='繊細'?-2.4:-1.5)),0,100);", "r.mor=cl(r.mor+morAfter(r,won),0,100);")
rep("r._pr=big?(r.a.sho-10)*.09-(r.per==='繊細'?.4:0)", "r._pr=big?(r.a.sho-10)*.09-(r.per==='繊細'?.4:0)+(r.per==='冷静'?.2:0)+(mtOn(r)?(r.per==='繊細'?.25:.1):0)")
rep("r.pop=cl(p0*.9+Math.max(0,g)+Math.min(0,g)*.5+(r.t==='Y'?3:r.d===0?1.5:0),0,100);", "r.pop=cl(p0*.9+Math.max(0,g)+Math.min(0,g)*.5+(r.t==='Y'?3:r.d===0?1.5:0)+(r.per==='明るい'?.6:0),0,100);")
rep("function kenB(r){const p=kenPol(r);if(p==='kei')return 0;return cl((r.a.ken-8)*.03,0,.3)*", "function kenB(r){const p=kenPol(r);if(p==='kei')return 0;return (r.per==='職人肌'?1.3:1)*cl((r.a.ken-8)*.03,0,.3)*")
rep("w+=k;});return s/w;}", "w+=k;});return Math.min(100,s/w+Math.min(4,o.filter(r=>r.per==='明るい').length*1.5));}")
core = """/* v152:勝ち負けのあとの気力(性格・メンタルトレーニング・タニマチの心の支え。数字は推定) */
function mtOn(r){return !!(r&&r.h===ME()&&G.con&&G.con.mental&&r.d<=1);}
function morAfter(r,won){const p=r.per;
 if(won)return (p==='マイペース'||p==='冷静')?1:1.5;
 let d=p==='負けず嫌い'?-.6:p==='繊細'?-2.4:(p==='マイペース'||p==='明るい')?-.8:p==='冷静'?-.9:-1.5;
 if(mtOn(r))d*=p==='繊細'?.5:.7;
 if(r.h===ME()&&r.d<=1&&typeof tmBest==='function'&&tmBest(50))d*=.8;
 return d;}
"""
rep("function atmo(){", core + "function atmo(){")
# ③ よろず相談窓口
rep("c:()=>['じっくり話を聞いて引き留める','親御さんを呼んで話し合う(10 万円)','本人の決意を尊重して送り出す'],",
    "c:()=>['じっくり話を聞いて引き留める','親御さんを呼んで話し合う(10 万円)','本人の決意を尊重して送り出す','協会のよろず相談窓口を紹介する'],")
rep("   G.jin=cl(G.jin+1,0,100);own().forEach(x=>{if(x!==r)x.tr=cl(x.tr+.5,0,100);});return go(r.n+'の決意を尊重し",
    "   if(i===3){if(Math.random()<.3+t/200){trAdd(r,4,'相談窓口で話を聞いてもらった');r.mor=cl(r.mor+3,0,100);return r.n+'は協会のよろず相談窓口で話を聞いてもらい、もう少し続けてみると言いました。';}return go(r.n+'は相談窓口にも行きましたが、気持ちは変わらず部屋を去りました。');}\n   G.jin=cl(G.jin+1,0,100);own().forEach(x=>{if(x!==r)x.tr=cl(x.tr+.5,0,100);});return go(r.n+'の決意を尊重し")
# ③ メンタルトレーニング
rep("const CONN={gym:'トレーニングジム',clinic:'治療院(整体・鍼灸)',diet:'管理栄養士',doc:'かかりつけ医(整形外科)'};",
    "const CONN={gym:'トレーニングジム',clinic:'治療院(整体・鍼灸)',diet:'管理栄養士',doc:'かかりつけ医(整形外科)',mental:'メンタルトレーニング(関取)'};")
rep("['gym','clinic','diet','doc']", "['gym','clinic','diet','doc','mental']", 2)
rep("に効きます。'+(wakaOn()?", "に効きます。メンタルトレーニングは関取が個人で契約するもので、費用は本人が 1 場所 8 万円(部屋の負担なし)。大一番の重圧と負けたあとの落ち込みが小さくなり、繊細な力士によく効きます。'+(wakaOn()?")
rep("if(r.tr<20&&r.d>=2&&Math.random()<.2&&!G.ev.some(e=>e.k==='retire'&&e.rid===r.id))G.ev.push({k:'retire',rid:r.id});});",
    "if(r.tr<20&&r.d>=2&&Math.random()<.2&&!G.ev.some(e=>e.k==='retire'&&e.rid===r.id))G.ev.push({k:'retire',rid:r.id});if(mtOn(r))r.cash=(r.cash||0)-8;});")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', dst, 'per', len(P))
