# v170 -> v171:上手に遊ぶと強すぎるのを直す(ダルマさん「ある程度困難があったほうがやりがいがあって面白く続けられる」→「実施」)+ 立川親方(元土佐ノ海)・春日山親方(元勢)の絵。
#   調べ:tests/smart.js(賢い自動プレイ)で伊勢ヶ濱が関取 10〜18 人・40 年で幕内優勝 97〜139 回。本物の目安は関取最多 7 人(spaia 24434)。
#   A 育ちの差を縮める:プレイヤーの部屋の育ち(cf)の 1 をこえる分を ×0.55、稽古場の効き .9+.05×段階 → .96+.025×段階(推定)。
#   B いい候補の取り合い:素質(ovr 12 をこえる分)×0.08 だけ誘いが通りにくい。ほかの部屋に出身校の先輩がいて自分の部屋にいなければ −0.08(推定)。
#   C 大きくなるほど目が届きにくい:親方 1 人(師匠+部屋付き親方)あたりの弟子が 20 人をこえると、こえた 1 人ごとに部屋の雰囲気 −1.5(最大 −15)、不祥事 +5%(推定)。
#      出典:文藝春秋 h8152(伊勢ヶ濱親方「師匠 1 人で部屋をやるならば 24、5 人が限界」)。
import sys, os
src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: raise SystemExit('一致数 %d (期待 %d): %r' % (c, n, old[:120]))
    s = s.replace(old, new)
rep("const APPV=170;\nconst SAVE='sumoManager170',SAVE169", "const APPV=171;\nconst SAVE='sumoManager171',SAVE170='sumoManager170',SAVE169")
rep('[SAVE169,SAVE168', '[SAVE170,SAVE169,SAVE168')
rep('<title>Grand Sumo Manager v170', '<title>Grand Sumo Manager v171')
# A
rep(' return {cf:cf,kf:.9+.05*G.fac.keiko', ' for(const k in cf)if(cf[k]>1)cf[k]=1+(cf[k]-1)*.55;\n return {cf:cf,kf:.96+.025*G.fac.keiko')
# B
rep("if(p.sch){b+=(G.rel[p.sch]||0)*.003;if(alumni(0,p.sch))b+=.06;}",
    "if(p.sch){b+=(G.rel[p.sch]||0)*.003;if(alumni(0,p.sch))b+=.06;else if(openAI().some(h=>alumni(h,p.sch)))b-=.08;}\n b-=Math.max(0,potOf(p.r)-12)*.08;")
# C
rep("return Math.min(100,s/w+Math.min(4,o.filter(r=>r.per==='明るい').length*1.5));}",
    "return Math.min(100,s/w+Math.min(4,o.filter(r=>r.per==='明るい').length*1.5))-mgPen();}\n"
    "function mgOver(){const n=ownAll().length,c=1+G.staff.filter(s=>s.role==='co').length;return Math.max(0,n/c-20);}\n"
    "function mgPen(){return Math.min(15,mgOver()*1.5);}")
rep('let p=0.00080*(1+(50-r.tr)/40)*pf*(1+(50-atmo())/120);', 'let p=0.00080*(1+(50-r.tr)/40)*pf*(1+(50-atmo())/120)*(1+mgOver()*.05);')
rep(" p.int+=20;p.cool=G.wn+2;return p.n+'には今回は断られました。2 週たてばまた話ができます。';",
    " {const pt=potOf(p.r);if(pt>=13&&Math.random()<(pt-12)*.15){p.int=100;addNews(p.n+'は、ほかの部屋からも誘われていて、そちらに入門を決めそうです。');return p.n+'には断られました。ほかの部屋からも声がかかっていて、そちらに決めそうです。';}}\n p.int+=20;p.cool=G.wn+2;return p.n+'には今回は断られました。2 週たてばまた話ができます。';")
ui = open(os.path.join(here, 'pi171_ui.js'), encoding='utf-8').read()
rep('</body>\n</html>', ui + '</body>\n</html>')
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
