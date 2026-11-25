# v174 -> v175:伊勢ヶ濱(上手な大部屋)を本物に近づける(ダルマさん「リアル重視」→「実施」)+ 鏡山親方(元多賀竜。追手風部屋の参与)の絵(ダルマさん「鏡山 昇司」)+ 力士の絵 7 枚(日翔志・翔猿・大栄翔・大青山・安青錦・丹治・錦富士〈差し替え〉)。
#   A 後援会:千秋楽の祝賀会で増える会員を 5%+5 人 → 5 人+会員×0.5%(最大 15 人)。親方だけ出るときは 2% → 0.4%(最大 6 人)。
#     自然な人数(80+評判×14)より多いときに戻る速さの下限(1 場所 −25 人)をなくし、増えるときと同じ 8% ずつ戻す(推定)。
#     会費は本物に近い(片男波部屋後援会 会則:個人 一口 3 万円・法人 一口 20 万円)。会員数の出典は見つからず推定。
#   B いい若者の取り合い:素質 13 以上の候補は入門先を決めるのが 1.4 倍早い。断られたときにほかの部屋に決める割合 (素質−12)×15% → ×25%。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=174;\nconst SAVE='sumoManager174',SAVE173", "const APPV=175;\nconst SAVE='sumoManager175',SAVE174='sumoManager174',SAVE173")
rep('[SAVE173,SAVE172', '[SAVE174,SAVE173,SAVE172')
rep('<title>Grand Sumo Manager v174', '<title>Grand Sumo Manager v175')
rep('const n=Math.round(G.sup*.05)+5;G.sup+=n;', 'const n=Math.round(5+Math.min(10,G.sup*.005));G.sup+=n;')
rep('const n=Math.round(G.sup*.02);G.sup+=n;', 'const n=Math.round(Math.min(6,G.sup*.004));G.sup+=n;')
rep('G.sup=Math.max(30,Math.round(G.sup+cl((80+G.rep*14-G.sup)*.08,-25,40)+randn()*3));', 'G.sup=Math.max(30,Math.round(G.sup+Math.min(40,(80+G.rep*14-G.sup)*.08)+randn()*3));')
rep('p.int+=R(1,6)*(1+(potOf(p.r)-9)*.08)*pf;', 'p.int+=R(1,6)*(1+(potOf(p.r)-9)*.08)*pf*(potOf(p.r)>=13?1.4:1);')
rep('if(pt>=13&&Math.random()<(pt-12)*.15)', 'if(pt>=13&&Math.random()<(pt-12)*.25)')
ui = open(os.path.join(here, 'pi175_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
